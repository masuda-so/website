"""Build the public Ether site as static files for deployment."""

from __future__ import annotations

import logging
import os
import shutil
import sys
from http import HTTPStatus
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DIST = ROOT / "dist"
CLIENT = DIST / "client"
LOGGER = logging.getLogger(__name__)
APP_SLUGS = ("weave", "vault", "ukiyo", "grace", "still")
APP_DOCUMENTS = ("privacy", "terms", "support")
APP_LANGUAGES = ("en", "ja")
# Pages are rendered against the real public host so absolute URLs are correct in
# the generated files themselves. The apps embed these fixed URLs, so the host is
# a constant rather than a build-time option.
SITE_HOST = "ether-llc.com"
# The pages load only their own scripts, stylesheets and images, plus Google
# Fonts, and use no inline scripts or style attributes.
CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "style-src 'self' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'"
)


def main() -> None:
    os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/ether-sites-build.sqlite")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")

    import django  # noqa: PLC0415

    django.setup()

    from django.conf import settings  # noqa: PLC0415
    from django.test import Client  # noqa: PLC0415

    settings.ALLOWED_HOSTS = [SITE_HOST]
    settings.COMPRESS_ENABLED = False
    shutil.rmtree(DIST, ignore_errors=True)
    (CLIENT / "static" / "css").mkdir(parents=True)
    (CLIENT / "static" / "js").mkdir(parents=True)
    (CLIENT / "static" / "images" / "favicons").mkdir(parents=True)

    routes = [("/", CLIENT / "index.html")]
    for language in APP_LANGUAGES:
        prefix = "" if language == "en" else "/ja"
        output_prefix = CLIENT if language == "en" else CLIENT / "ja"
        routes.extend(
            (
                f"{prefix}/apps/{app_slug}/{document}/",
                output_prefix / "apps" / app_slug / document / "index.html",
            )
            for app_slug in APP_SLUGS
            for document in APP_DOCUMENTS
        )
    client = Client(SERVER_NAME=SITE_HOST)
    for route, output_path in routes:
        response = client.get(route, secure=True)
        if response.status_code != HTTPStatus.OK:
            message = f"Page render failed for {route}: HTTP {response.status_code}"
            raise RuntimeError(message)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
    sitemap_entries = "".join(
        f"  <url><loc>https://{SITE_HOST}{route}</loc></url>\n" for route, _ in routes
    )
    (CLIENT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_entries}"
        "</urlset>\n",
        encoding="utf-8",
    )
    (CLIENT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: https://{SITE_HOST}/sitemap.xml\n",
        encoding="utf-8",
    )
    # Cloudflare Workers Static Assets reads this file and applies the headers;
    # it is not served as an asset. Vercel does not read it.
    (CLIENT / "_headers").write_text(
        "/*\n"
        f"  Content-Security-Policy: {CONTENT_SECURITY_POLICY}\n"
        "  Strict-Transport-Security: max-age=63072000\n"
        "  X-Content-Type-Options: nosniff\n"
        "  X-Frame-Options: DENY\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n",
        encoding="utf-8",
    )
    shutil.copy2(
        ROOT / "website/static/css/project.css",
        CLIENT / "static/css/project.css",
    )
    shutil.copy2(ROOT / "website/static/js/project.js", CLIENT / "static/js/project.js")
    shutil.copytree(ROOT / "website/static/images/apps", CLIENT / "static/images/apps")
    shutil.copy2(ROOT / "THIRD_PARTY_NOTICES.md", CLIENT / "third-party-notices.txt")
    favicon_source = ROOT / "website/static/images/favicons"
    favicon_target = CLIENT / "static/images/favicons"
    for favicon_name in (
        "ether.svg",
        "apple-touch-icon.png",
        "favicon-16x16.png",
        "favicon-32x32.png",
        "favicon.ico",
    ):
        shutil.copy2(favicon_source / favicon_name, favicon_target / favicon_name)
    shutil.copy2(favicon_source / "favicon.ico", CLIENT / "favicon.ico")
    shutil.copy2(ROOT / "website/static/images/og.png", CLIENT / "static/images/og.png")

    LOGGER.info("Built Ether site in %s", DIST)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
