"""Build the public Ether landing page for OpenAI Sites deployment."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DIST = ROOT / "dist"
CLIENT = DIST / "client"


def main() -> None:
    os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/ether-sites-build.sqlite")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")

    import django

    django.setup()

    from django.conf import settings
    from django.test import Client

    settings.ALLOWED_HOSTS = ["testserver"]
    settings.COMPRESS_ENABLED = False
    response = Client().get("/")
    if response.status_code != 200:
        raise RuntimeError(f"Homepage render failed: HTTP {response.status_code}")

    shutil.rmtree(DIST, ignore_errors=True)
    (CLIENT / "static" / "css").mkdir(parents=True)
    (CLIENT / "static" / "js").mkdir(parents=True)
    (CLIENT / "static" / "images" / "favicons").mkdir(parents=True)
    (DIST / "server").mkdir(parents=True)

    (CLIENT / "index.html").write_bytes(response.content)
    shutil.copy2(ROOT / "website/static/css/project.css", CLIENT / "static/css/project.css")
    shutil.copy2(ROOT / "website/static/js/project.js", CLIENT / "static/js/project.js")
    shutil.copy2(
        ROOT / "website/static/images/favicons/favicon.ico",
        CLIENT / "static/images/favicons/favicon.ico",
    )

    worker = """const worker = {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === \"/\") {
      url.pathname = \"/index.html\";
      return env.ASSETS.fetch(new Request(url, request));
    }
    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) return response;
    url.pathname = \"/index.html\";
    return env.ASSETS.fetch(new Request(url, request));
  },
};
export default worker;
"""
    (DIST / "server/index.js").write_text(worker, encoding="utf-8")
    print(f"Built Ether site in {DIST}")


if __name__ == "__main__":
    main()
