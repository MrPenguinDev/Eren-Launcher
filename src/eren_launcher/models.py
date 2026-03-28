from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class InstanceConfig:
    name: str
    minecraft_version: str
    loader: str = "vanilla"
    min_memory_mb: int = 1024
    max_memory_mb: int = 4096
    java_path: str = "java"
    game_dir: Path = field(default_factory=Path)


SUPPORTED_LOADERS = {"vanilla", "fabric", "quilt", "forge", "neoforge"}
