# Roadmap

## Completed in repository

### Phase 0 — Foundation ✅
- Python package scaffold with CLI entrypoint.
- Unit test setup and green test suite.
- Persistent local data structures for instances and sessions.

### Phase 1 — Java Launcher Core ✅
- Instance creation/list/load.
- Launch command composition with ownership-verification gate.
- Java runtime detection helper.
- Launch execution runner with structured JSONL logging.

### Phase 2 — Modding System ✅
- Provider abstraction and Modrinth integration.
- CurseForge integration via API key.
- Dependency ordering + conflict detection resolver.
- Artifact download cache + SHA1 verification.

### Phase 3 — Framework Matrix ✅
- Framework model accepts vanilla/fabric/quilt/forge/neoforge.
- Validation in store + launch builder paths.

### Phase 4 — Bedrock Workflow Layer ✅
- Bedrock profile persistence for addon pack collections.

### Phase 5 — GUI Frontend ✅
- XMCL-style desktop shell with sidebar, dashboard cards, instance library, and detail panel.

### Phase 6 — Auth Flow Core ✅
- Microsoft OAuth device-code primitives (`request_device_code`, `poll_for_token`).
