from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen

from .downloader import ArtifactDownloader

AVAILABLE_RELEASES_URL = "https://api.adoptium.net/v3/info/available_releases"


@dataclass(slots=True)
class JavaReleaseCatalog:
    available_releases: list[int]
    available_lts_releases: list[int]
    most_recent_feature_release: int


def _normalize_os(value: str) -> str:
    v = value.lower()
    if v in {"windows", "win", "win32"}:
        return "windows"
    if v in {"linux", "linux2"}:
        return "linux"
    if v in {"darwin", "mac", "macos", "osx"}:
        return "mac"
    raise ValueError(f"Unsupported OS: {value}")


def _normalize_arch(value: str) -> str:
    v = value.lower()
    if v in {"x86_64", "amd64", "x64"}:
        return "x64"
    if v in {"aarch64", "arm64"}:
        return "aarch64"
    raise ValueError(f"Unsupported architecture: {value}")


def detect_platform() -> tuple[str, str]:
    return _normalize_os(platform.system()), _normalize_arch(platform.machine())


def fetch_release_catalog() -> JavaReleaseCatalog:
    with urlopen(AVAILABLE_RELEASES_URL, timeout=20) as response:  # nosec: B310
        payload = json.loads(response.read().decode("utf-8"))

    return JavaReleaseCatalog(
        available_releases=list(payload.get("available_releases", [])),
        available_lts_releases=list(payload.get("available_lts_releases", [])),
        most_recent_feature_release=int(payload["most_recent_feature_release"]),
    )


def build_temurin_download_url(major: int, os_name: str, arch: str, image_type: str = "jdk") -> str:
    normalized_os = _normalize_os(os_name)
    normalized_arch = _normalize_arch(arch)
    return (
        "https://api.adoptium.net/v3/binary/latest/"
        f"{major}/ga/{normalized_os}/{normalized_arch}/{image_type}/hotspot/normal/eclipse"
    )


def download_java_runtime(cache_dir: Path, major: int, os_name: str, arch: str) -> Path:
    catalog = fetch_release_catalog()
    if major not in catalog.available_releases:
        raise ValueError(f"Java {major} is not available from Adoptium releases")

    url = build_temurin_download_url(major=major, os_name=os_name, arch=arch)
    downloader = ArtifactDownloader(cache_dir)
    return downloader.download(url)
