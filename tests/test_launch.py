import pytest

from eren_launcher.launch import LaunchContext, build_java_launch_command
from eren_launcher.models import InstanceConfig


def test_requires_ownership_verification() -> None:
    cfg = InstanceConfig(name="main", minecraft_version="1.21.5")
    ctx = LaunchContext(
        username="player",
        uuid="uuid",
        access_token="token",
        ownership_verified=False,
    )

    with pytest.raises(PermissionError):
        build_java_launch_command(cfg, ctx)


def test_builds_launch_command() -> None:
    cfg = InstanceConfig(name="main", minecraft_version="1.21.5")
    ctx = LaunchContext(
        username="player",
        uuid="uuid",
        access_token="token",
        ownership_verified=True,
    )

    command = build_java_launch_command(cfg, ctx)
    assert "--username" in command
    assert "player" in command
    assert "--version" in command
    assert "1.21.5" in command
