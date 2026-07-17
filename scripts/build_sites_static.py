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


def main() -> None:
    os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/ether-sites-build.sqlite")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")

    import django  # noqa: PLC0415

    django.setup()

    from django.conf import settings  # noqa: PLC0415
    from django.test import Client  # noqa: PLC0415

    settings.ALLOWED_HOSTS = ["testserver"]
    settings.COMPRESS_ENABLED = False
    response = Client().get("/")
    if response.status_code != HTTPStatus.OK:
        message = f"Homepage render failed: HTTP {response.status_code}"
        raise RuntimeError(message)

    shutil.rmtree(DIST, ignore_errors=True)
    (CLIENT / "static" / "css").mkdir(parents=True)
    (CLIENT / "static" / "js").mkdir(parents=True)
    (CLIENT / "static" / "images" / "favicons").mkdir(parents=True)
    (DIST / "server").mkdir(parents=True)

    (CLIENT / "index.html").write_bytes(response.content)
    shutil.copy2(
        ROOT / "website/static/css/project.css",
        CLIENT / "static/css/project.css",
    )
    shutil.copy2(ROOT / "website/static/js/project.js", CLIENT / "static/js/project.js")
    shutil.copy2(
        ROOT / "website/static/images/favicons/favicon.ico",
        CLIENT / "static/images/favicons/favicon.ico",
    )
    shutil.copy2(ROOT / "website/static/images/og.png", CLIENT / "static/images/og.png")

    worker = """async function renderPage(request, env, url) {
  const assetUrl = new URL(\"/index.html\", url);
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
    if (url.pathname === \"/\" || url.pathname === \"/index.html\") {
      return renderPage(request, env, url);
    }
    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) return response;
    return renderPage(request, env, url);
  },
};
export default worker;
"""
    (DIST / "server/index.js").write_text(worker, encoding="utf-8")
    LOGGER.info("Built Ether site in %s", DIST)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
