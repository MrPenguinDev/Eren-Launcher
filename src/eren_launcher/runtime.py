from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass


@dataclass(slots=True)
class JavaRuntimeInfo:
    executable: str
    major: int
    raw_version: str


def detect_java_runtime(executable: str = "java") -> JavaRuntimeInfo:
    proc = subprocess.run(
        [executable, "-version"],
        check=False,
        capture_output=True,
        text=True,
    )
    output = (proc.stderr or "") + "\n" + (proc.stdout or "")
    match = re.search(r'version\s+"([^"]+)"', output)
    if not match:
        raise RuntimeError(f"Could not parse Java version from: {output.strip()}")

    raw = match.group(1)
    major = int(raw.split(".")[0]) if not raw.startswith("1.") else int(raw.split(".")[1])
    return JavaRuntimeInfo(executable=executable, major=major, raw_version=raw)
