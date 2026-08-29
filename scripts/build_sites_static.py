"""Build the public Ether landing page for OpenAI Sites deployment."""

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
    (DIST / "server").mkdir(parents=True)

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
    shutil.copy2(
        ROOT / "website/static/css/project.css",
        CLIENT / "static/css/project.css",
    )
    shutil.copy2(ROOT / "website/static/js/project.js", CLIENT / "static/js/project.js")
    favicon_source = ROOT / "website/static/images/favicons"
    favicon_target = CLIENT / "static/images/favicons"
    for favicon_name in (
        "apple-touch-icon.png",
        "favicon-16x16.png",
        "favicon-32x32.png",
        "favicon.ico",
    ):
        shutil.copy2(favicon_source / favicon_name, favicon_target / favicon_name)
    shutil.copy2(favicon_source / "favicon.ico", CLIENT / "favicon.ico")
    shutil.copy2(ROOT / "website/static/images/og.png", CLIENT / "static/images/og.png")

    worker = """function pageAssetPath(pathname) {
  if (pathname === \"/\" || pathname === \"/index.html\") return \"/index.html\";
  if (pathname.endsWith(\"/\")) return `${pathname}index.html`;
  const finalSegment = pathname.split(\"/\").at(-1);
  if (finalSegment && !finalSegment.includes(\".\")) return `${pathname}/index.html`;
  return pathname;
}

async function renderPage(request, env, url, pathname = url.pathname) {
  const assetUrl = new URL(pageAssetPath(pathname), url);
  const response = await env.ASSETS.fetch(new Request(assetUrl, request));
  if (!response.ok) return response;

  const headers = new Headers(response.headers);
  headers.delete(\"content-length\");
  headers.delete(\"content-encoding\");
  headers.delete(\"etag\");
  headers.set(\"content-type\", \"text/html; charset=utf-8\");
  headers.set(\"cache-control\", \"public, max-age=300\");
  const html = (await response.text()).replaceAll(\"http://testserver\", url.origin);
  return new Response(html, { status: response.status, headers });
}

const worker = {
  async fetch(request, env) {
    const url = new URL(request.url);
    const pagePath = pageAssetPath(url.pathname);
    if (pagePath !== url.pathname || url.pathname.endsWith(\"/index.html\")) {
      return renderPage(request, env, url);
    }
    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) return response;
    if (url.pathname.startsWith(\"/apps/\") || url.pathname.startsWith(\"/ja/apps/\")) {
      return response;
    }
    return renderPage(request, env, url, \"/\");
  },
};
export default worker;
"""
    (DIST / "server/index.js").write_text(worker, encoding="utf-8")
    LOGGER.info("Built Ether site in %s", DIST)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
