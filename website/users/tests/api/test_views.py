from __future__ import annotations

import json
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.conf import settings
from django.test import Client as DjangoClient
from django.urls import reverse

from website.users.models import User
from website.users.tests.factories import UserFactory

if TYPE_CHECKING:
    from django.test import Client


pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return UserFactory.create()


def test_list_users_as_anonymous_user(client: Client):
    response = client.get(reverse("api:list_users"))

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_list_users_as_authenticated_user(client: Client, user: User):
    client.force_login(user)
    # Another user, excluded from the response
    UserFactory.create()

    response = client.get(reverse("api:list_users"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "email": user.email,
            "name": user.name,
            "url": f"/api/users/{user.username}/",
            "username": user.username,
        },
    ]


def test_retrieve_current_user(client: Client, user: User):
    client.force_login(user)

    response = client.get(
        reverse("api:retrieve_current_user"),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }


def test_retrieve_user(client: Client, user: User):
    client.force_login(user)

    response = client.get(
        reverse("api:retrieve_user", kwargs={"username": user.username}),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }


def test_retrieve_another_user(client: Client, user: User):
    client.force_login(user)
    user_2 = UserFactory.create()

    response = client.get(
        reverse("api:retrieve_user", kwargs={"username": user_2.username}),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_update_current_user(client: Client):
    user = UserFactory.create(name="Old")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_current_user"),
        data='{"name": "New Name", "username": "old"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        "email": user.email,
        "name": "New Name",
        "username": "old",
        "url": "/api/users/old/",
    }


def test_update_user(client: Client):
    user = UserFactory.create(name="Old", username="old")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_user", kwargs={"username": "old"}),
        data='{"name": "New Name", "username": "old"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        "email": user.email,
        "name": "New Name",
        "url": "/api/users/old/",
        "username": "old",
    }


@pytest.mark.parametrize("route", ["update_current_user", "update_user"])
@pytest.mark.parametrize(
    ("payload", "status", "expected"),
    [
        ({}, HTTPStatus.OK, ("Old Name", "old")),
        ({"name": "New Name"}, HTTPStatus.OK, ("New Name", "old")),
        ({"username": "new"}, HTTPStatus.OK, ("Old Name", "new")),
        ({"name": None}, HTTPStatus.UNPROCESSABLE_ENTITY, ("Old Name", "old")),
        ({"username": None}, HTTPStatus.UNPROCESSABLE_ENTITY, ("Old Name", "old")),
        ({"name": "x" * 256}, HTTPStatus.UNPROCESSABLE_ENTITY, ("Old Name", "old")),
        ({"username": "x" * 151}, HTTPStatus.UNPROCESSABLE_ENTITY, ("Old Name", "old")),
        ({"is_staff": True}, HTTPStatus.OK, ("Old Name", "old")),
    ],
)
def test_partial_update_preserves_omitted_fields_and_validation(
    client: Client,
    route,
    payload,
    status,
    expected,
):
    user = UserFactory.create(name="Old Name", username="old", is_staff=False)
    client.force_login(user)
    kwargs = {"username": user.username} if route == "update_user" else None

    response = client.patch(
        reverse(f"api:{route}", kwargs=kwargs),
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == status, response.json()
    user.refresh_from_db()
    assert (user.name, user.username) == expected
    assert user.is_staff is False


def test_partial_update_cannot_change_another_user(client: Client, user: User):
    other = UserFactory.create(name="Other Name")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_user", kwargs={"username": other.username}),
        data='{"name": "Changed"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    other.refresh_from_db()
    assert other.name == "Other Name"


@pytest.mark.parametrize("route", ["update_current_user", "update_user"])
@pytest.mark.parametrize("username", ["", "has space", "bad/name", "emoji🙂"])
def test_update_rejects_invalid_username(client: Client, user: User, route, username):
    client.force_login(user)
    original = (user.username, user.name)
    kwargs = {"username": user.username} if route == "update_user" else None

    response = client.patch(
        reverse(f"api:{route}", kwargs=kwargs),
        data=json.dumps({"username": username, "name": "Not saved"}),
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    user.refresh_from_db()
    assert (user.username, user.name) == original


@pytest.mark.parametrize("route", ["update_current_user", "update_user"])
def test_update_rejects_duplicate_username(client: Client, user: User, route):
    other = UserFactory.create()
    client.force_login(user)
    original = (user.username, user.name)
    kwargs = {"username": user.username} if route == "update_user" else None

    response = client.patch(
        reverse(f"api:{route}", kwargs=kwargs),
        data=json.dumps({"username": other.username, "name": "Not saved"}),
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    user.refresh_from_db()
    assert (user.username, user.name) == original


@pytest.mark.parametrize("route", ["update_current_user", "update_user"])
def test_update_requires_csrf_token(user: User, route):
    client = DjangoClient(enforce_csrf_checks=True)
    client.force_login(user)
    original = user.name
    kwargs = {"username": user.username} if route == "update_user" else None

    response = client.patch(
        reverse(f"api:{route}", kwargs=kwargs),
        data='{"name": "Not saved"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    user.refresh_from_db()
    assert user.name == original


@pytest.mark.parametrize("route", ["update_current_user", "update_user"])
@pytest.mark.parametrize("username", ["日本語", "\uff21lice"])
def test_update_accepts_and_normalizes_unicode_username(
    client: Client,
    user: User,
    route,
    username,
):
    client.force_login(user)
    kwargs = {"username": user.username} if route == "update_user" else None

    response = client.patch(
        reverse(f"api:{route}", kwargs=kwargs),
        data=json.dumps({"username": username}),
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK
    user.refresh_from_db()
    assert user.username == user.normalize_username(username)


def test_username_claimed_after_validation_rolls_back(
    client: Client,
    user: User,
    monkeypatch,
):
    original_clean = User.full_clean
    original = (user.username, user.name)

    def competing_claim(instance, *args, **kwargs):
        original_clean(instance, *args, **kwargs)
        UserFactory.create(username="claimed")

    monkeypatch.setattr(User, "full_clean", competing_claim)
    client.force_login(user)

    response = client.patch(
        reverse("api:update_current_user"),
        data='{"username": "claimed", "name": "Not saved"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    user.refresh_from_db()
    assert (user.username, user.name) == original
    assert response.json()["detail"][0]["loc"][-1] == "username"


def test_partial_update_preserves_concurrent_unrelated_changes(
    client: Client,
    user: User,
    monkeypatch,
):
    original_clean = User.full_clean

    def competing_update(instance, *args, **kwargs):
        original_clean(instance, *args, **kwargs)
        User.objects.filter(pk=user.pk).update(name="Concurrent Name")

    monkeypatch.setattr(User, "full_clean", competing_update)
    client.force_login(user)

    response = client.patch(
        reverse("api:update_current_user"),
        data='{"username": "new"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK
    user.refresh_from_db()
    assert (user.username, user.name) == ("new", "Concurrent Name")


@pytest.mark.parametrize("route", ["update_current_user", "update_user"])
@pytest.mark.parametrize("foreign_origin", [False, True])
def test_csrf_token_accepts_same_origin_only(user: User, route, foreign_origin):
    client = DjangoClient(enforce_csrf_checks=True)
    client.get(reverse("account_login"))
    token = client.cookies[settings.CSRF_COOKIE_NAME].value
    client.force_login(user)
    kwargs = {"username": user.username} if route == "update_user" else None
    original = user.name
    headers = {"X-CSRFToken": token}
    if foreign_origin:
        headers["Origin"] = "https://untrusted.example"

    response = client.patch(
        reverse(f"api:{route}", kwargs=kwargs),
        data='{"name": "New Name"}',
        content_type="application/json",
        headers=headers,
    )

    expected = HTTPStatus.FORBIDDEN if foreign_origin else HTTPStatus.OK
    assert response.status_code == expected
    user.refresh_from_db()
    assert user.name == (original if foreign_origin else "New Name")
