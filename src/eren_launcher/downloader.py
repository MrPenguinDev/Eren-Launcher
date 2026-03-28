from __future__ import annotations

import hashlib
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


class ArtifactDownloader:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _filename_for(self, url: str) -> str:
        parsed = urlparse(url)
        name = Path(parsed.path).name or "artifact.bin"
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
        return f"{digest}-{name}"

    def cached_path_for(self, url: str) -> Path:
        return self.cache_dir / self._filename_for(url)

    def download(self, url: str, expected_sha1: str | None = None, offline: bool = False) -> Path:
        out = self.cached_path_for(url)
        if out.exists() and (expected_sha1 is None or self._sha1(out) == expected_sha1):
            return out

        if offline:
            raise FileNotFoundError(f"Offline mode enabled and artifact is not cached: {out}")

        with urlopen(url, timeout=30) as response:  # nosec: B310
            data = response.read()
        out.write_bytes(data)

        if expected_sha1 and self._sha1(out) != expected_sha1:
            out.unlink(missing_ok=True)
            raise ValueError("Checksum mismatch for downloaded artifact")
        return out

    @staticmethod
    def _sha1(path: Path) -> str:
        h = hashlib.sha1()
        h.update(path.read_bytes())
        return h.hexdigest()
