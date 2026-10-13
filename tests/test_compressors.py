"""Exercise file reads and real compression with deprecations treated as errors."""

import re
from typing import TYPE_CHECKING

import pytest
from compressor import cache as compressor_cache
from compressor import storage
from compressor.conf import settings as compressor_settings
from compressor.exceptions import UncompressableFileError
from compressor.utils import get_class
from django.core.cache import caches
from django.template import Context
from django.template import Template
from django.test import RequestFactory
from django.views import defaults

if TYPE_CHECKING:
    from django.http import HttpResponse

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")


@pytest.fixture(params=["css", "js"])
def compressor(request):
    kind = request.param
    return get_class(compressor_settings.COMPRESSORS[kind])(kind)


@pytest.mark.parametrize(
    ("encoded", "charset", "expected"),
    [
        (b"", "utf-8", ""),
        ("/* 日本語 */\r\nbody {}\r".encode(), "utf-8", "/* 日本語 */\r\nbody {}\r"),
        (b"\xef\xbb\xbfbody {}\n", "utf-8", "body {}\n"),
        ("/* café */".encode("latin-1"), "latin-1", "/* café */"),
    ],
)
def test_file_content_preserves_encoding_bom_and_newlines(
    compressor,
    tmp_path,
    encoded,
    charset,
    expected,
):
    source = tmp_path / "source.txt"
    source.write_bytes(encoded)
    assert compressor.get_filecontent(str(source), charset) == expected


def test_invalid_encoding_reports_a_compression_error(compressor, tmp_path):
    source = tmp_path / "invalid.txt"
    source.write_bytes(b"\xff")
    with pytest.raises(UncompressableFileError, match="utf-8"):
        compressor.get_filecontent(str(source), "utf-8")


def test_missing_file_is_not_silently_ignored(compressor, tmp_path):
    with pytest.raises(FileNotFoundError):
        compressor.get_filecontent(str(tmp_path / "missing.txt"), "utf-8")


@pytest.fixture
def compression_root(settings, tmp_path, monkeypatch):
    settings.DEBUG = False
    settings.COMPRESS_ENABLED = True
    settings.COMPRESS_OFFLINE = False
    settings.COMPRESS_ROOT = str(tmp_path)
    settings.COMPRESS_URL = "/static/"
    settings.STATIC_URL = "/static/"
    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}
    }
    # Compressor retains its first resolved cache, even after CACHES changes.
    # Earlier page requests must not reuse URLs from a different output root.
    monkeypatch.setattr(compressor_cache, "cache", caches["default"])
    # Exercise the production filters with local output instead of Amazon S3.
    settings.COMPRESS_FILTERS = {
        "css": [
            "compressor.filters.css_default.CssAbsoluteFilter",
            "compressor.filters.cssmin.rCSSMinFilter",
        ],
        "js": ["compressor.filters.jsmin.JSMinFilter"],
    }
    monkeypatch.setattr(
        storage,
        "default_storage",
        storage.CompressorFileStorage(location=tmp_path, base_url="/static/"),
    )
    return tmp_path


@pytest.mark.parametrize(
    ("kind", "source", "tag", "expected"),
    [
        (
            "css",
            b"\xef\xbb\xbf/* comment */\r\nbody { color: red; }\r\n",
            '<link rel="stylesheet" href="/static/source.css">',
            "body{color:red}",
        ),
        (
            "js",
            b"\xef\xbb\xbf// comment\r\nwindow.answer = 42;\r\n",
            '<script defer src="/static/source.js"></script>',
            "window.answer=42;;",  # Upstream adds a separator between JS inputs.
        ),
    ],
)
def test_template_tag_compresses_files(compression_root, kind, source, tag, expected):
    (compression_root / f"source.{kind}").write_bytes(source)
    template = Template(
        "{% load compress %}{% compress " + kind + " %}" + tag + "{% endcompress %}",
    )
    rendered = template.render(Context())
    output_files = list((compression_root / "CACHE" / kind).glob(f"*.{kind}"))
    assert len(output_files) == 1
    output = output_files[0]
    assert output.read_text(encoding="utf-8") == expected
    assert f"/static/{output.relative_to(compression_root).as_posix()}" in rendered
    if kind == "js":
        assert "defer" in rendered


@pytest.mark.parametrize("status", [404, 500])
def test_error_pages_generate_css_and_js(compression_root, status):
    request = RequestFactory().get("/missing-page/")
    response: HttpResponse
    if status == 404:  # noqa: PLR2004 - HTTP status being exercised.
        response = defaults.page_not_found(request, Exception("Test-only missing page"))
    else:
        response = defaults.server_error(request)
    assert response.status_code == status
    html = response.content.decode()
    for kind in ("css", "js"):
        generated = re.findall(rf'/static/(CACHE/{kind}/[^"\s]+\.{kind})', html)
        assert generated, html
        for filename in generated:
            assert (compression_root / filename).read_text(encoding="utf-8").strip()
