from __future__ import annotations

from dataclasses import dataclass

from .auth import AccountSession
from .models import InstanceConfig


@dataclass(slots=True)
class LaunchContext:
    username: str
    uuid: str
    access_token: str
    ownership_verified: bool

    def to_account_session(self) -> AccountSession:
        return AccountSession(
            username=self.username,
            uuid=self.uuid,
            access_token=self.access_token,
            ownership_verified=self.ownership_verified,
        )

    @classmethod
    def from_account_session(cls, session: AccountSession) -> "LaunchContext":
        return cls(
            username=session.username,
            uuid=session.uuid,
            access_token=session.access_token,
            ownership_verified=session.ownership_verified,
        )


def build_java_launch_command(config: InstanceConfig, ctx: LaunchContext) -> list[str]:
    if not ctx.ownership_verified:
        raise PermissionError("Minecraft ownership verification is required.")

    if config.loader not in {"vanilla", "fabric", "quilt", "forge", "neoforge"}:
        raise ValueError(f"Unsupported loader: {config.loader}")

    return [
        config.java_path,
        f"-Xms{config.min_memory_mb}M",
        f"-Xmx{config.max_memory_mb}M",
        "-Dminecraft.launcher.brand=eren-launcher",
        "-Dminecraft.launcher.version=0.1.0",
        "net.minecraft.client.main.Main",
        "--username",
        ctx.username,
        "--version",
        config.minecraft_version,
        "--gameDir",
        str(config.game_dir),
        "--accessToken",
        ctx.access_token,
        "--uuid",
        ctx.uuid,
    ]


def build_bedrock_launch_command(profile_name: str, packs: list[str]) -> list[str]:
    """Builds a bedrock workflow command without launcher auth requirements."""
    command = ["bedrock", "--profile", profile_name]
    for pack in packs:
        command.extend(["--pack", pack])
    return command
