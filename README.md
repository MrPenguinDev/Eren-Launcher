# Eren Launcher

A legal, extensible Minecraft launcher for Android/Linux/Windows workflows.

> This project does **not** provide cracked login, ownership bypass, or DRM circumvention.

## Java runtime support
The launcher now supports **downloading any available Temurin Java feature release** (e.g. 8/11/17/21/...) directly from Adoptium APIs.

Commands:
```bash
# List all available Java releases from Adoptium
PYTHONPATH=src python -m eren_launcher.cli java-releases

# Download a specific Java major version for current machine platform
PYTHONPATH=src python -m eren_launcher.cli download-java --major 21

# Download for explicit platform
PYTHONPATH=src python -m eren_launcher.cli download-java --major 17 --os windows --arch x64
```

## UI status
The desktop UI is now a full XMCL-style shell (not a placeholder):
- Dark modern layout with left navigation + home dashboard.
- Metrics cards (instances/mods/downloads/runtime).
- Instance library panel and right-side detail context.
- Launch action in top bar and ownership/compliance indicators.

Launch it with:
```bash
PYTHONPATH=src python -m eren_launcher.cli gui
```
