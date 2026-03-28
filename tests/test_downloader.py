import hashlib
from pathlib import Path
from unittest.mock import patch

import pytest

from eren_launcher.downloader import ArtifactDownloader


class _Resp:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return self._data


def test_download_and_verify(tmp_path: Path) -> None:
    data = b"abc"
    sha1 = hashlib.sha1(data).hexdigest()

    with patch("eren_launcher.downloader.urlopen", return_value=_Resp(data)):
        dl = ArtifactDownloader(tmp_path)
        out = dl.download("https://example.com/file.jar", expected_sha1=sha1)

    assert out.exists()
    assert out.read_bytes() == data


def test_download_checksum_mismatch(tmp_path: Path) -> None:
    with patch("eren_launcher.downloader.urlopen", return_value=_Resp(b"bad")):
        dl = ArtifactDownloader(tmp_path)
        with pytest.raises(ValueError):
            dl.download("https://example.com/file.jar", expected_sha1="deadbeef")


def test_offline_uses_cache(tmp_path: Path) -> None:
    dl = ArtifactDownloader(tmp_path)
    cached = dl.cached_path_for("https://example.com/file.jar")
    cached.write_bytes(b"cached")

    out = dl.download("https://example.com/file.jar", offline=True)
    assert out == cached


def test_offline_missing_cache_raises(tmp_path: Path) -> None:
    dl = ArtifactDownloader(tmp_path)
    with pytest.raises(FileNotFoundError):
        dl.download("https://example.com/file.jar", offline=True)
