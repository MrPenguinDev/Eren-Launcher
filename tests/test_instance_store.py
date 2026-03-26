from pathlib import Path

from eren_launcher.instance_store import InstanceStore
from eren_launcher.models import InstanceConfig


def test_save_and_load_instance(tmp_path: Path) -> None:
    store = InstanceStore(tmp_path)
    config = InstanceConfig(name="main", minecraft_version="1.21.5", loader="fabric")

    store.save(config)
    loaded = store.load("main")

    assert loaded.name == "main"
    assert loaded.minecraft_version == "1.21.5"
    assert loaded.loader == "fabric"


def test_list_instances(tmp_path: Path) -> None:
    store = InstanceStore(tmp_path)
    store.save(InstanceConfig(name="b", minecraft_version="1.20.6"))
    store.save(InstanceConfig(name="a", minecraft_version="1.21.1"))

    assert store.list_instances() == ["a", "b"]
