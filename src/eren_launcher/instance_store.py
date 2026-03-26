from __future__ import annotations

import json
from pathlib import Path

from .models import InstanceConfig, SUPPORTED_LOADERS


class InstanceStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.instances_dir = self.root / "instances"
        self.instances_dir.mkdir(parents=True, exist_ok=True)

    def save(self, config: InstanceConfig) -> Path:
        if config.loader not in SUPPORTED_LOADERS:
            raise ValueError(f"Unsupported loader: {config.loader}")

        instance_path = self.instances_dir / config.name
        instance_path.mkdir(parents=True, exist_ok=True)

        if not config.game_dir:
            config.game_dir = instance_path / "game"

        payload = {
            "name": config.name,
            "minecraft_version": config.minecraft_version,
            "loader": config.loader,
            "min_memory_mb": config.min_memory_mb,
            "max_memory_mb": config.max_memory_mb,
            "java_path": config.java_path,
            "game_dir": str(config.game_dir),
        }
        out_file = instance_path / "instance.json"
        out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return out_file

    def load(self, name: str) -> InstanceConfig:
        in_file = self.instances_dir / name / "instance.json"
        if not in_file.exists():
            raise FileNotFoundError(f"Instance not found: {name}")

        payload = json.loads(in_file.read_text(encoding="utf-8"))
        return InstanceConfig(
            name=payload["name"],
            minecraft_version=payload["minecraft_version"],
            loader=payload["loader"],
            min_memory_mb=payload["min_memory_mb"],
            max_memory_mb=payload["max_memory_mb"],
            java_path=payload["java_path"],
            game_dir=Path(payload["game_dir"]),
        )

    def list_instances(self) -> list[str]:
        return sorted(p.name for p in self.instances_dir.iterdir() if p.is_dir())
