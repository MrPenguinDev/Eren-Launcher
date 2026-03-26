from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.request import urlopen

VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"


@dataclass(slots=True)
class MinecraftVersion:
    version_id: str
    type: str
    release_time: str


def fetch_versions(limit: int = 20) -> list[MinecraftVersion]:
    with urlopen(VERSION_MANIFEST_URL, timeout=15) as response:  # nosec: B310
        payload = json.loads(response.read().decode("utf-8"))

    versions = [
        MinecraftVersion(
            version_id=item["id"],
            type=item["type"],
            release_time=item["releaseTime"],
        )
        for item in payload.get("versions", [])
    ]
    return versions[:limit]
