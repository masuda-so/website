from http import HTTPStatus

import pytest

from scripts.build_sites_static import SITE_HOST
from website.app_documents import APP_RECORDS
from website.app_documents import DOCUMENT_LABELS
from website.app_documents import DOCUMENT_LABELS_JA


@pytest.fixture(autouse=True)
def _disable_template_compression(settings) -> None:
    settings.COMPRESS_ENABLED = False
    settings.DATABASES["default"]["ATOMIC_REQUESTS"] = False


def test_home_declares_its_japanese_language(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert b'<html lang="ja">' in response.content


@pytest.mark.parametrize("app_slug", APP_RECORDS)
@pytest.mark.parametrize("document", DOCUMENT_LABELS)
@pytest.mark.parametrize(
    "locale_case",
    [
        ("", DOCUMENT_LABELS, b'<html lang="en">'),
        ("/ja", DOCUMENT_LABELS_JA, b'<html lang="ja">'),
    ],
)
def test_app_document_routes_are_public(
    client,
    app_slug,
    document,
    locale_case,
):
    prefix, labels, html_language = locale_case
    response = client.get(f"{prefix}/apps/{app_slug}/{document}/")

    assert response.status_code == HTTPStatus.OK
    assert APP_RECORDS[app_slug].name.encode() in response.content
    assert labels[document].encode() in response.content
    assert html_language in response.content


@pytest.mark.parametrize("app_slug", APP_RECORDS)
@pytest.mark.parametrize("prefix", ["", "/ja"])
def test_app_documents_link_the_three_fixed_routes(client, app_slug, prefix):
    response = client.get(f"{prefix}/apps/{app_slug}/privacy/")

    assert response.status_code == HTTPStatus.OK
    for document in DOCUMENT_LABELS:
        assert f"{prefix}/apps/{app_slug}/{document}/".encode() in response.content


def test_photo_privacy_is_app_specific(client):
    weave = client.get("/apps/weave/privacy/")
    ukiyo = client.get("/apps/ukiyo/privacy/")

    assert b"does not integrate with your photo library" in weave.content
    assert b"system picker gives the app only the item you select" in ukiyo.content


def test_vault_copy_matches_implemented_search(client):
    response = client.get("/apps/vault/privacy/")

    assert b"notebook with search and on-device assistance" in response.content
    assert b"weighted search" not in response.content


def test_support_page_uses_existing_public_issue_tracker(client):
    response = client.get("/apps/grace/support/")

    assert response.status_code == HTTPStatus.OK
    assert b"https://github.com/masuda-so/grace/issues" in response.content
    assert b"The issue tracker is public" in response.content


def test_still_documents_are_available(client):
    response = client.get("/apps/still/privacy/")

    assert response.status_code == HTTPStatus.OK
    assert b"completed pause start times" in response.content


def test_language_versions_are_cross_linked(client):
    english = client.get("/apps/grace/privacy/")
    japanese = client.get("/ja/apps/grace/privacy/")

    for response in (english, japanese):
        assert b'hreflang="en"' in response.content
        assert b'hreflang="ja"' in response.content
        assert b"http://testserver/apps/grace/privacy/" in response.content
        assert b"http://testserver/ja/apps/grace/privacy/" in response.content
    assert "アプリが保存するデータ".encode() in japanese.content
    assert b"Data stored by the app" not in japanese.content


def test_document_navigation_and_image_metadata_are_localized(client):
    english = client.get("/apps/grace/privacy/")
    japanese = client.get("/ja/apps/grace/privacy/")

    assert b'aria-label="Grace documents"' in english.content
    assert 'aria-label="Graceの文書"'.encode() in japanese.content
    assert b"Turn ideas into value" in english.content
    assert "アイデアを、価値へ。".encode() in japanese.content
    assert b'name="twitter:image:alt"' in english.content
    assert b'name="twitter:image:alt"' in japanese.content


def test_public_build_host_is_used_for_canonical_links(client, settings):
    settings.ALLOWED_HOSTS = [SITE_HOST]

    response = client.get(
        "/ja/apps/grace/privacy/",
        secure=True,
        HTTP_HOST=SITE_HOST,
    )

    assert response.status_code == HTTPStatus.OK
    assert b"https://ether-llc.com/ja/apps/grace/privacy/" in response.content
    assert b"https://ether-llc.com/apps/grace/privacy/" in response.content
    assert b"testserver" not in response.content


@pytest.mark.parametrize(
    "path",
    [
        "/apps/unknown/privacy/",
        "/apps/weave/cookies/",
        "/ja/apps/unknown/privacy/",
    ],
)
def test_unknown_app_documents_return_not_found(client, path):
    assert client.get(path).status_code == HTTPStatus.NOT_FOUND


GRACE_STORE_URL = b"https://apps.apple.com/jp/app/grace-gratitude-journal/id6807439542"
GRACE_STORE_URL_NEUTRAL = (
    b"https://apps.apple.com/app/grace-gratitude-journal/id6807439542"
)


@pytest.mark.parametrize(
    "locale_case",
    [
        (
            "",
            b'<html lang="en">',
            b"app-store-badge-en.svg",
            "Grace: Gratitude Journal",
            GRACE_STORE_URL_NEUTRAL,
        ),
        (
            "/ja",
            b'<html lang="ja">',
            b"app-store-badge-ja.svg",
            "Grace: 感謝日記",
            GRACE_STORE_URL,
        ),
    ],
)
def test_grace_product_page_links_to_the_app_store(client, locale_case):
    prefix, html_language, badge, store_name, store_url = locale_case
    response = client.get(f"{prefix}/apps/grace/")

    assert response.status_code == HTTPStatus.OK
    assert html_language in response.content
    assert store_name.encode() in response.content
    assert badge in response.content
    # Exactly one badge per layout, linking to the Japanese storefront URL.
    assert response.content.count(b'class="app-store-badge"') == 1
    assert store_url in response.content
    assert b'class="trademark-credit"' in response.content
    for document in DOCUMENT_LABELS:
        assert f"{prefix}/apps/grace/{document}/".encode() in response.content


def test_grace_product_page_versions_are_cross_linked(client):
    english = client.get("/apps/grace/")
    japanese = client.get("/ja/apps/grace/")

    for response in (english, japanese):
        assert b'hreflang="en"' in response.content
        assert b'hreflang="ja"' in response.content
        assert b"http://testserver/apps/grace/" in response.content
        assert b"http://testserver/ja/apps/grace/" in response.content
    assert b'content="ja_JP"' in japanese.content
    assert b'content="en_US"' in english.content


def test_grace_product_page_does_not_state_prices(client):
    response = client.get("/ja/apps/grace/")

    assert "¥".encode() not in response.content
    assert b"$" not in response.content


def test_home_routes_visitors_to_grace(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.content.count(b'class="app-store-badge"') == 1
    assert b"app-store-badge-ja.svg" in response.content
    assert GRACE_STORE_URL in response.content
    assert b"/ja/apps/grace/" in response.content
    assert b'class="trademark-credit"' in response.content


@pytest.mark.parametrize("path", ["/apps/vault/", "/ja/apps/still/", "/apps/unknown/"])
def test_apps_without_a_product_page_return_not_found(client, path):
    assert client.get(path).status_code == HTTPStatus.NOT_FOUND
