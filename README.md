# Eren Launcher

A legal, extensible Minecraft launcher for Android/Linux/Windows workflows.

> This project does **not** provide cracked login, ownership bypass, or DRM circumvention.

## Java runtime support (online + offline)
The launcher supports downloading any available Temurin Java feature release and can work in offline mode using cached catalog/artifacts.

Commands:
```bash
# Update catalog from network and list releases
PYTHONPATH=src python -m eren_launcher.cli java-releases

# List releases from local cache only
PYTHONPATH=src python -m eren_launcher.cli java-releases --offline

# Download Java for current platform
PYTHONPATH=src python -m eren_launcher.cli download-java --major 21

# Download Java from cache only (no network)
PYTHONPATH=src python -m eren_launcher.cli download-java --major 21 --offline
```

## Bedrock note
Bedrock launch building does not require launcher auth, because account/session is handled in Bedrock itself:
```bash
PYTHONPATH=src python -m eren_launcher.cli save-bedrock-profile mobile pack_a pack_b
PYTHONPATH=src python -m eren_launcher.cli build-bedrock-launch mobile
```

## UI status
The desktop UI is a full XMCL-style shell with dashboard, sidebar navigation, and instance/details panels.
