from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AccountSession:
    username: str
    uuid: str
    access_token: str
    ownership_verified: bool


class SessionStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, session: AccountSession) -> Path:
        out = self.root / f"{name}.json"
        out.write_text(
            json.dumps(
                {
                    "username": session.username,
                    "uuid": session.uuid,
                    "access_token": session.access_token,
                    "ownership_verified": session.ownership_verified,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return out

    def load(self, name: str) -> AccountSession:
        path = self.root / f"{name}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return AccountSession(
            username=payload["username"],
            uuid=payload["uuid"],
            access_token=payload["access_token"],
            ownership_verified=payload["ownership_verified"],
        )
