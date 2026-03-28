from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(slots=True)
class SearchResult:
    source: str
    project_id: str
    slug: str
    title: str


class MetadataProvider(Protocol):
    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        ...


class ModrinthProvider:
    base_url = "https://api.modrinth.com/v2/search"

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        params = urlencode({"query": query, "limit": limit})
        with urlopen(f"{self.base_url}?{params}", timeout=20) as response:  # nosec: B310
            payload = json.loads(response.read().decode("utf-8"))

        hits = payload.get("hits", [])
        return [
            SearchResult(
                source="modrinth",
                project_id=item.get("project_id", ""),
                slug=item.get("slug", ""),
                title=item.get("title", ""),
            )
            for item in hits
        ]


class CurseForgeProvider:
    base_url = "https://api.curseforge.com/v1/mods/search"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("CurseForge API key is required.")
        self.api_key = api_key

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        params = urlencode({"gameId": 432, "searchFilter": query, "pageSize": limit})
        req = Request(f"{self.base_url}?{params}", headers={"x-api-key": self.api_key})
        with urlopen(req, timeout=20) as response:  # nosec: B310
            payload = json.loads(response.read().decode("utf-8"))

        data = payload.get("data", [])
        return [
            SearchResult(
                source="curseforge",
                project_id=str(item.get("id", "")),
                slug=item.get("slug", ""),
                title=item.get("name", ""),
            )
            for item in data
        ]
