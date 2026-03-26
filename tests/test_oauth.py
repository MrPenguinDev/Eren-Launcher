import json
from unittest.mock import patch

from eren_launcher.microsoft_oauth import MicrosoftOAuthDeviceFlow


class _Resp:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_request_device_code() -> None:
    payload = {
        "device_code": "d",
        "user_code": "u",
        "verification_uri": "https://microsoft.com/devicelogin",
        "expires_in": 900,
        "interval": 5,
        "message": "login",
    }
    with patch("eren_launcher.microsoft_oauth.urlopen", return_value=_Resp(payload)):
        response = MicrosoftOAuthDeviceFlow("client-id").request_device_code()
    assert response.device_code == "d"


def test_poll_for_token() -> None:
    payload = {
        "access_token": "access",
        "refresh_token": "refresh",
        "expires_in": 3600,
        "token_type": "Bearer",
    }
    with patch("eren_launcher.microsoft_oauth.urlopen", return_value=_Resp(payload)):
        token = MicrosoftOAuthDeviceFlow("client-id").poll_for_token("code", timeout_seconds=1)
    assert token.access_token == "access"
