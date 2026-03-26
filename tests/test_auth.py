from pathlib import Path

from eren_launcher.auth import AccountSession, SessionStore
from eren_launcher.launch import LaunchContext


def test_session_store_roundtrip(tmp_path: Path) -> None:
    store = SessionStore(tmp_path)
    saved = store.save(
        "main",
        AccountSession(
            username="Steve",
            uuid="uuid",
            access_token="token",
            ownership_verified=True,
        ),
    )

    assert saved.exists()
    loaded = store.load("main")
    assert loaded.username == "Steve"
    assert loaded.ownership_verified is True


def test_launch_context_conversion() -> None:
    ctx = LaunchContext("Alex", "uuid2", "token2", True)
    session = ctx.to_account_session()
    back = LaunchContext.from_account_session(session)
    assert back.username == "Alex"
