from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class BedrockProfile:
    name: str
    packs: list[str] = field(default_factory=list)


class BedrockProfileStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, profile: BedrockProfile) -> Path:
        path = self.root / f"{profile.name}.json"
        path.write_text(json.dumps({"name": profile.name, "packs": profile.packs}, indent=2), encoding="utf-8")
        return path

    def load(self, name: str) -> BedrockProfile:
        path = self.root / f"{name}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return BedrockProfile(name=payload["name"], packs=list(payload.get("packs", [])))
