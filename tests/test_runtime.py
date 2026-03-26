from unittest.mock import patch

from eren_launcher.runtime import detect_java_runtime


class _Proc:
    def __init__(self, stderr: str = "", stdout: str = "") -> None:
        self.stderr = stderr
        self.stdout = stdout


def test_detect_java_runtime_modern() -> None:
    with patch("subprocess.run", return_value=_Proc(stderr='openjdk version "21.0.4"')):
        info = detect_java_runtime("java")

    assert info.major == 21
    assert info.raw_version == "21.0.4"


def test_detect_java_runtime_legacy() -> None:
    with patch("subprocess.run", return_value=_Proc(stderr='java version "1.8.0_402"')):
        info = detect_java_runtime("java")

    assert info.major == 8
