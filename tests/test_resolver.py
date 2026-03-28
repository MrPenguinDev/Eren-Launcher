import pytest

from eren_launcher.resolver import PackageNode, detect_conflicts, resolve_install_order


def test_resolve_install_order() -> None:
    graph = {
        "fabric-api": PackageNode("fabric-api"),
        "sodium": PackageNode("sodium", depends_on={"fabric-api"}),
        "iris": PackageNode("iris", depends_on={"sodium"}),
    }

    order = resolve_install_order({"iris"}, graph)
    assert order == ["fabric-api", "sodium", "iris"]


def test_detect_conflicts() -> None:
    graph = {
        "a": PackageNode("a", conflicts_with={"b"}),
        "b": PackageNode("b"),
    }
    assert detect_conflicts({"a", "b"}, graph) == [("a", "b")]


def test_cycle_detection() -> None:
    graph = {
        "a": PackageNode("a", depends_on={"b"}),
        "b": PackageNode("b", depends_on={"a"}),
    }
    with pytest.raises(ValueError):
        resolve_install_order({"a"}, graph)
