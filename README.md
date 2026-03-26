# Eren Launcher

A legal, extensible Minecraft launcher for Android/Linux/Windows workflows.

> This project does **not** provide cracked login, ownership bypass, or DRM circumvention.

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

## Core capabilities
- Microsoft OAuth device-code flow core.
- CurseForge + Modrinth metadata provider wiring.
- Artifact download cache with SHA1 verification.
- Launch command generation + process execution with structured JSONL logs.
- Instance/session/profile persistence.
