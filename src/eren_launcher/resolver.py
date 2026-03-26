from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PackageNode:
    package_id: str
    depends_on: set[str] = field(default_factory=set)
    conflicts_with: set[str] = field(default_factory=set)


def detect_conflicts(selected: set[str], graph: dict[str, PackageNode]) -> list[tuple[str, str]]:
    conflicts: list[tuple[str, str]] = []
    for pkg in selected:
        node = graph.get(pkg)
        if not node:
            continue
        for other in node.conflicts_with:
            if other in selected:
                conflicts.append((pkg, other))
    dedup = {tuple(sorted(p)) for p in conflicts}
    return sorted(dedup)


def resolve_install_order(selected: set[str], graph: dict[str, PackageNode]) -> list[str]:
    resolved: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(pkg: str) -> None:
        if pkg in visited:
            return
        if pkg in visiting:
            raise ValueError(f"Circular dependency detected at {pkg}")
        if pkg not in graph:
            raise KeyError(f"Unknown package: {pkg}")

        visiting.add(pkg)
        for dep in sorted(graph[pkg].depends_on):
            dfs(dep)
        visiting.remove(pkg)
        visited.add(pkg)
        resolved.append(pkg)

    for item in sorted(selected):
        dfs(item)

    return resolved
