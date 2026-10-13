"""Use Python's text I/O while upstream django-compressor uses codecs.open()."""

from pathlib import Path

from compressor.css import CssCompressor as BaseCssCompressor
from compressor.exceptions import UncompressableFileError
from compressor.js import JsCompressor as BaseJsCompressor


class TextFileCompressorMixin:
    def get_filecontent(self, filename: str, charset: str) -> str:
        # Preserve upstream UTF-8 BOM removal and unmodified line endings.
        encoding = "utf-8-sig" if charset == "utf-8" else charset
        with Path(filename).open(encoding=encoding, newline="") as source:
            try:
                return source.read()
            except (OSError, UnicodeDecodeError) as error:
                message = f"Cannot read '{filename}' with charset {encoding}: {error}"
                raise UncompressableFileError(message) from error


class CssCompressor(TextFileCompressorMixin, BaseCssCompressor):
    """Keep upstream CSS processing with a non-deprecated text reader."""


class JsCompressor(TextFileCompressorMixin, BaseJsCompressor):
    """Keep upstream JavaScript processing with a non-deprecated text reader."""
