# Architecture

## Implemented modules

```text
eren_launcher/
  auth.py             -> account session persistence
  bedrock.py          -> bedrock addon-profile persistence
  cli.py              -> command interface
  downloader.py       -> artifact cache + SHA1 verification
  gui.py              -> XMCL-style desktop UI shell
  instance_store.py   -> java instance persistence
  java_manager.py     -> Java catalog + runtime download (online/offline cache)
  launch.py           -> launch context + command creation
  manifest.py         -> Mojang version manifest integration
  microsoft_oauth.py  -> Microsoft device-code flow primitives
  process_runner.py   -> launch execution + structured JSONL logs
  providers.py        -> Modrinth + CurseForge providers
  resolver.py         -> dependency graph + conflict detection
  runtime.py          -> Java runtime detection
```

## Security and compliance
- Launch command creation is blocked unless ownership is verified.
- No cracked mode exists in command surface.
- Provider APIs are official endpoints (keys/tokens required where applicable).
- Artifact validation supports SHA1 verification before cache acceptance.

- Bedrock launch command path is auth-free (uses Bedrock built-in account flow).
