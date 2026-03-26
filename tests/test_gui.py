from pathlib import Path

from eren_launcher.gui import LauncherGUI
from eren_launcher.instance_store import InstanceStore
from eren_launcher.models import InstanceConfig


def test_gui_reads_instances(tmp_path: Path) -> None:
    store = InstanceStore(tmp_path)
    store.save(InstanceConfig(name="main", minecraft_version="1.21.5"))

    gui = LauncherGUI(tmp_path)
    assert gui.instances == ["main"]
