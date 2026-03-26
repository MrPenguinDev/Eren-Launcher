from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


class LaunchProcessRunner:
    def __init__(self, logs_dir: Path) -> None:
        self.logs_dir = logs_dir
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def run(self, command: list[str], instance_name: str) -> int:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        log_file = self.logs_dir / f"{instance_name}-{timestamp}.jsonl"

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        with log_file.open("w", encoding="utf-8") as handle:
            if process.stdout is None:
                raise RuntimeError("Missing stdout pipe")

            for line in process.stdout:
                record = {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "stream": "stdout",
                    "line": line.rstrip("\n"),
                }
                handle.write(json.dumps(record) + "\n")

        return process.wait()
