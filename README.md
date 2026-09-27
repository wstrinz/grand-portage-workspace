# Grand Portage 0.50

Private local rework workspace. Phase 0 groundwork only; no kernel implementation yet.

Read `BACKBRIEF.md`, `DECISIONS.md`, and `docs/GP-0.50-REWORK-PACKET.md`.
The source packet is retained verbatim; approved clarifications are in DECISIONS.md.

Workspace: F:\repos\grandportage-0.50. Keep build outputs, caches and scratch data on F: where practical. Existing source repositories stay in place and are read-only inputs.

The v0.37 oracle is pinned in oracle/PIN.json. There is no remote configured for this repository. Do not publish before the packet's approval gates.

Phase 0b remains pending until Will completes or confirms SWEEP-SOURCES.md.
Current progress and gaps: reports/PHASE-0-STATUS.md.

First corpus batch: reports/PHASE-0A-BATCH-1.md; case catalog: corpus/README.md.
Replay: .venv/Scripts/python.exe -B tools/check-corpus.py --run-oracle.
Private freeze patch: reports/freeze-v0.37.1/freeze-docs.patch (prepared only).
