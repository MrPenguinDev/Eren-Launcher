from __future__ import annotations

import json
import time
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEVICE_CODE_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode"
TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"


@dataclass(slots=True)
class DeviceCodeResponse:
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int
    message: str


@dataclass(slots=True)
class TokenResponse:
    access_token: str
    refresh_token: str | None
    expires_in: int
    token_type: str


class MicrosoftOAuthDeviceFlow:
    def __init__(self, client_id: str, scope: str = "XboxLive.signin offline_access") -> None:
        self.client_id = client_id
        self.scope = scope

    def request_device_code(self) -> DeviceCodeResponse:
        body = urlencode({"client_id": self.client_id, "scope": self.scope}).encode("utf-8")
        req = Request(DEVICE_CODE_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urlopen(req, timeout=20) as response:  # nosec: B310
            payload = json.loads(response.read().decode("utf-8"))

        return DeviceCodeResponse(
            device_code=payload["device_code"],
            user_code=payload["user_code"],
            verification_uri=payload["verification_uri"],
            expires_in=payload["expires_in"],
            interval=payload.get("interval", 5),
            message=payload.get("message", ""),
        )

    def poll_for_token(self, device_code: str, interval: int = 5, timeout_seconds: int = 900) -> TokenResponse:
        start = time.time()
        body_template = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": self.client_id,
            "device_code": device_code,
        }

        while time.time() - start < timeout_seconds:
            body = urlencode(body_template).encode("utf-8")
            req = Request(TOKEN_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
            try:
                with urlopen(req, timeout=20) as response:  # nosec: B310
                    payload = json.loads(response.read().decode("utf-8"))
                return TokenResponse(
                    access_token=payload["access_token"],
                    refresh_token=payload.get("refresh_token"),
                    expires_in=payload["expires_in"],
                    token_type=payload.get("token_type", "Bearer"),
                )
            except Exception as exc:  # network/HTTP transient handling
                msg = str(exc)
                if "authorization_pending" in msg or "slow_down" in msg:
                    time.sleep(interval)
                    continue
                raise

        raise TimeoutError("Timed out waiting for Microsoft device authorization")
