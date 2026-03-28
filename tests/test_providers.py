import json
from unittest.mock import patch

from eren_launcher.providers import CurseForgeProvider, ModrinthProvider


class _Resp:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_modrinth_provider() -> None:
    payload = {"hits": [{"project_id": "p1", "slug": "sodium", "title": "Sodium"}]}
    with patch("eren_launcher.providers.urlopen", return_value=_Resp(payload)):
        results = ModrinthProvider().search("sodium", 1)
    assert results[0].project_id == "p1"


def test_curseforge_provider() -> None:
    payload = {"data": [{"id": 1, "slug": "jei", "name": "JEI"}]}
    with patch("eren_launcher.providers.urlopen", return_value=_Resp(payload)):
        results = CurseForgeProvider(api_key="k").search("jei", 1)
    assert results[0].project_id == "1"
