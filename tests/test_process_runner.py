import json
from pathlib import Path

from eren_launcher.process_runner import LaunchProcessRunner


def test_process_runner_writes_jsonl(tmp_path: Path) -> None:
    runner = LaunchProcessRunner(tmp_path)
    code = runner.run(["python", "-c", "print('hello')"], "demo")
    assert code == 0

    logs = list(tmp_path.glob("demo-*.jsonl"))
    assert logs
    line = logs[0].read_text(encoding="utf-8").strip().splitlines()[0]
    parsed = json.loads(line)
    assert parsed["line"] == "hello"
