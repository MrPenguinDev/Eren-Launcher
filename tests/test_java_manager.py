import json
from pathlib import Path
from unittest.mock import patch

import pytest

from eren_launcher.java_manager import (
    JavaReleaseCatalog,
    build_temurin_download_url,
    download_java_runtime,
    fetch_release_catalog,
)


class _Resp:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_fetch_release_catalog_online_then_cache(tmp_path: Path) -> None:
    payload = {
        "available_releases": [8, 11, 17, 21],
        "available_lts_releases": [8, 11, 17, 21],
        "most_recent_feature_release": 25,
    }
    with patch("eren_launcher.java_manager.urlopen", return_value=_Resp(payload)):
        catalog = fetch_release_catalog(cache_dir=tmp_path, offline=False)

    assert catalog.available_releases == [8, 11, 17, 21]

    # offline should load cached catalog
    cached = fetch_release_catalog(cache_dir=tmp_path, offline=True)
    assert cached.most_recent_feature_release == 25


def test_build_temurin_download_url() -> None:
    url = build_temurin_download_url(21, "linux", "x64")
    assert "/21/ga/linux/x64/jdk/" in url


def test_download_java_runtime_validates_release(tmp_path: Path) -> None:
    catalog = JavaReleaseCatalog([8, 11, 17, 21], [8, 11, 17, 21], 25)
    with patch("eren_launcher.java_manager.fetch_release_catalog", return_value=catalog):
        with patch("eren_launcher.java_manager.ArtifactDownloader.download", return_value=tmp_path / "jdk.tar.gz"):
            out = download_java_runtime(tmp_path, major=21, os_name="linux", arch="x64")
    assert out.name == "jdk.tar.gz"


def test_download_java_runtime_unsupported_release(tmp_path: Path) -> None:
    catalog = JavaReleaseCatalog([8, 11, 17, 21], [8, 11, 17, 21], 25)
    with patch("eren_launcher.java_manager.fetch_release_catalog", return_value=catalog):
        with pytest.raises(ValueError):
            download_java_runtime(tmp_path, major=6, os_name="linux", arch="x64")
