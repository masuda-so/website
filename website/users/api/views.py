from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError as ModelValidationError
from django.db import IntegrityError
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import ValidationError

from website.users.api.schema import UpdateUserSchema
from website.users.api.schema import UserSchema
from website.users.models import User

if TYPE_CHECKING:
    from django.db.models import QuerySet

router = Router(tags=["users"])


def _get_users_queryset(request) -> QuerySet[User]:
    return User.objects.filter(pk=request.user.pk)


def _update_profile(user: User, data: UpdateUserSchema) -> User:
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        return user
    for field, value in updates.items():
        setattr(user, field, value)
    # Normalize before validation so the stored value is the one we validate.
    if "username" in updates:
        user.username = User.normalize_username(user.username)
    # Django documents _meta as its model metadata API.
    excluded = {field.name for field in User._meta.fields} - updates.keys()  # noqa: SLF001
    try:
        user.full_clean(exclude=excluded)
    except ModelValidationError as exc:
        raise ValidationError(
            [
                {"loc": ["body", "data", field], "msg": message, "type": "value_error"}
                for field, messages in exc.message_dict.items()
                for message in messages
            ],
        ) from exc
    try:
        with transaction.atomic():
            # A PATCH must not overwrite unrelated concurrent profile changes.
            user.save(update_fields=updates.keys())
    except IntegrityError as exc:
        # A competing update can claim the username after full_clean succeeds.
        if (
            "username" not in updates
            or not User.objects.filter(username=user.username)
            .exclude(pk=user.pk)
            .exists()
        ):
            raise
        raise ValidationError(
            [
                {
                    "loc": ["body", "data", "username"],
                    "msg": "A user with that username already exists.",
                    "type": "value_error",
                },
            ],
        ) from exc
    return user


@router.get("/", response=list[UserSchema])
def list_users(request):
    return _get_users_queryset(request)


@router.get("/me/", response=UserSchema)
def retrieve_current_user(request):
    return request.user


@router.get("/{username}/", response=UserSchema)
def retrieve_user(request, username: str):
    users_qs = _get_users_queryset(request)
    return get_object_or_404(users_qs, username=username)


@router.patch("/me/", response=UserSchema)
def update_current_user(request, data: UpdateUserSchema):
    return _update_profile(request.user, data)


@router.patch("/{username}/", response=UserSchema)
def update_user(request, username: str, data: UpdateUserSchema):
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, username=username)
    return _update_profile(user, data)
