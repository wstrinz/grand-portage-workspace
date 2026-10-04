# Sol handoff: GP v0.32 release and epoch 12

Prepared 2026-09-09 after the user approved the preflight and Phase A
implementation. Updated 2026-09-12 after the release and the next architecture
review. This handoff does not create another task, switch a model, or start a
campaign.

## Start here

Phase A shipped as **v0.32.0, graph format 7, kernel epoch 11** from workspace
commit `cca5b05`; the compiled public mirror and GitHub Release were published.
The independent Lane Watch directive delivery remains a separate repository and
deployment concern. Do not couple it to GP's semantic release sequence.

Post-release Match4 hardening is preserved as commit `a475aeb`: `gp review`, a
pre-CAS free-symbol refusal for witnesses, and a zero-ring/vacuous-identity
diagnostic. Its deterministic suite passed 1,633 tests with 59 deselected, its
focused gate passed 358 tests with 13 deselected, and its real WSL/Singular gate
passed 9 tests with 20 deselected. It changes no graph format, epoch, transport
cell, or authority rule.

The v0.33 authority boundary is implemented at commit `5698ebb` and released
with the Match4 hardening. All ten fold-time verdict subjects pass through one
sealed binder; graph format 7, kernel epoch 11, existing verdict judgments, and
serialized graph behavior remain unchanged. The broad direction for B was
approved, but the original packet is not an executable specification. The
preflight found mathematical counterexamples. Freeze the corrected concrete
rules, migration table and answer keys before coding epoch 12. Do not silently
revert to the packet's single-order/boolean-migration rules.

Read in this order (paths relative to the GP repository unless absolute):

1. This handoff.
2. `review/v0.32/README.md` and `review/v0.32/validation.txt`: current implementation and exact results.
3. `docs/WORK.md`: operational schema, CLI, accounting-only mode and authority boundaries.
4. `review/v0.32-preflight/README.md`: accepted packet corrections, counterexamples and mandatory B matrix.
5. `CURRENT.md`, `ARCHITECTURE.md`, `REVIEW.md`, `COMPATIBILITY.md`: existing release and trust boundaries.
6. Original packet and DK follow-up sources listed below, for the complete B1 answer-key table.

The preflight README is a historical planning record: its statements that no
product code changed or that UNRESOLVED still needs designing describe that
stage. The current v0.32 release notes and this handoff supersede those status
statements. Preserve the historical evidence files.

## Workspaces and source custody

- GP: `$DEV/grand-portage`.
  At handoff preparation: branch `master`, HEAD
  `fa5644dd6f50cf904ad2c1be5f37e7371fe9bf0d` (v0.31.2), with Phase A in the
  working tree. The release later froze that work at `cca5b05` (v0.32.0).
- DK: `$DEV/math-research/campaigns/dk-retrodiction`.
  Pinned commit `b876fe4ed5c8963a0e8c19e18c829821c0686654`.
  Its tracked worktree remained clean. Treat campaign inputs as immutable.
  Read `followup/README.md`, `followup/06-field-class.md`, the field-class-probe
  directory, `followup/01-transports-verbatim.md`, `followup/04-adjacency.md`,
  `transports/`, `misuse/`, and the fixture README.
- Lane Watch: `$DEV/math-research/infrastructure/agent-observer`.
  Separate repository, six changed/new files listed below.
- Original packet attachment:
  `$HOME/.codex/attachments/b11bfb14-08d7-441f-8cb5-55968e552880/pasted-text.txt`.

At handoff preparation, no cfg23 or configuration-23-4 files were edited and no
coordinator message, live directive, math campaign action, service restart,
commit, push, tag, or remote publication had been performed. That sentence is a
historical custody fact, not the current release state. Inspect fresh status
before continuing and preserve later user changes.

## Implemented Phase A

| Area | Files and behavior |
|---|---|
| D1 | `grandportage/store.py`: all family premise kinds refuse with a discharge before model lookup. Family PREDICATE is the actual minimal frozen crash. Successful family/model composition is reserved for B. |
| D3 | Live non-COUNT claims refuse `splits`, `groups`, `method`, `proves`, including empty values. Guard runs after supersession resolution so explicitly retired malformed DK dispositions remain readable. Shared `rests_on`, `asserts_count`, lifecycle `why` retain legitimate uses. |
| D2 | `grandportage/cas.py`: one simultaneous constant Singular map replaces nested substitutions. Ring-variable coordinate rejection and CASProgram boundary remain. Construction has bounded nesting; arithmetic still has backend budgets/timeouts. |
| Supersession | `grandportage/kernel.py`: model licensing fields now include existing field/domain/characteristic/universe/embedding/guards/localization/pending/elimination/component semantics. Semantic changes require RELICENSE. No transport-table change. |
| History | `grandportage/cli.py`: all supported supersedable entity types, model-inclusive tally, branching successors, cycle-bounded rendering. Frozen ledger now shows the sixth/model chain. |
| Work | New `grandportage/work.py`, CLI `gp work`, CLI/MCP display. Separate append-only `grand-portage-work/v1` sidecar, attempt IDs, family/locus, reason, structured budget, UTC timestamp, explicit resolution. Strict validation, exclusive writer lock, fsync, missing-final-newline repair. No graph/coverage/verifier authority. |
| Accounting | `check.run_accounting`, `gp check --seam unchecked`, MCP equivalent. Explicit rule selection; open premises remain visible. Text banner even in quiet mode, JSON seam marker, no clean inferences, unchecked receipts rejected for full-check comparison. Structural load guards and ordinary full checks/hooks remain. |
| Release | Version metadata 0.32.0, updated marked docs, `docs/WORK.md`, release records, frozen fixture manifest, new acceptance tests and CLI replay script. CI gains a pinned live Singular lane. |

Work storage: `.portage/graph.jsonl` uses `.portage/work.jsonl`; an explicit
`other.jsonl` uses `other.jsonl.work.jsonl`. Resolution records operational
completion only; evidence must still be recorded separately. Malformed logs
refuse instead of disappearing. Abandoned writer locks require explicit recovery.
The mathematical hook does not consume this operational sidecar.

New tests: `tests/test_guard_release.py`, `tests/test_work_accounting.py`.
Frozen inputs: `tests/fixtures/dk_retrodiction/`, LF hashes in `manifest.json`.
Original expected outputs remain historical; new tests assert the reviewed deltas.
`transports/verbatim-v0.31.2.md` is copied original source output, not a regenerated golden.
One old mock in `tests/test_adversarial.py` was adjusted to inspect/evaluate the
new simultaneous map instead of searching nested-substitution text; the actual
true/false witness assertions were preserved.

## Acceptance facts that must survive

- Ledger: 57 claims, 52 live, `DOUBT:D-E5-GAP` first; F-TRADE unflagged.
- Model history adds `M-E1-RING --RELICENSE--> M-E1-RING-2`; six chains total.
- X8 and X10 keep open-premise refusals; the model-scoped X9 control remains clean.
- D1 now refuses usefully; D3-before now refuses; D3-after retains coverage debt.
- Both 96- and 97-variable witnesses now verify, each repeated three times.
- Misuse BAD-1 and dishonest BAD-2-count remain accepted. Honest BAD-2b-count
  retains its finding. PREDICATE BAD-2/BAD-2b now refuse inert COUNT fields.
  Do not claim the original misuse suite universally refused these inputs.
- STALE_OVERLAP on the DK pair is deliberately deferred: action exclusions
  and missing portable template certificates concern different populations/
  propositions/evidence obligations. Counts and prose do not prove containment.
- Phase A does not fix the legacy C-to-R field-scope loophole, add new scope
  vocabulary, alter `base_changes`, or relax the P0 point-universe guard.

## Validation already completed

All **1,685 current Python tests** are accounted for across disjoint lanes:

- Final deterministic: **1,626 passed, 59 deselected**, 96.22 seconds.
- Live/replay/exhaustive with `GP_REQUIRE_LIVE=1`: **59 passed**, 485.01 seconds.
  Its deselected count was 1,625 because it ran before the final extra
  deterministic newline regression was added. Live code did not change afterward.
- CLI replay: **33 commands passed** with separate init/declare/verify/check
  exit codes and full stdout/stderr; six actual VERIFIED witness results.
- Lean: **28 jobs, build successful**, two existing linter warnings.
- Wheel built; version metadata and inclusion of `grandportage/work.py` verified.
  `tmp/v032-dist/grandportage-0.32.0-py3-none-any.whl` (ignored build artifact).
  SHA256 `adf919c99bd5e602014f346544d1ca5fd7c786f4f2d1ad7f803a0601c47973e9`.
- Both edited repositories passed `git diff --check`.
- New remote CI workflow has **not** run yet.

Evidence: `review/v0.32/validation.txt`, `guard-replay.json`, `observations.json`.
Baseline evidence lives separately in `review/v0.32-preflight/`; do not overwrite it.
No need to repeat the entire validated suite merely to read this handoff.
Run relevant checks after changes and the established release gate when shipping.

Useful PowerShell commands, from GP unless noted:

```powershell
python -m pytest -q -m "not live and not replay and not exhaustive"
$env:GP_REQUIRE_LIVE='1'
python -m pytest -q -m "live or replay or exhaustive"
python scripts/replay_guard_fixtures.py --live --output tmp/guard-replay-next.json
python -m grandportage.cli docs
python -m pip wheel . --no-deps --no-build-isolation --no-cache-dir --wheel-dir tmp/v032-dist
# From GP/lean:
$env:ELAN_HOME='$ELAN_HOME'
lake build
```

Installed real backend is WSL Singular 4.2.1 (4212). The Ubuntu 22.04 CI lane
pins Singular and companion packages to `1:4.2.1-p3+ds-1`. WSL/live tools needed
sandbox escalation here. Pip's user cache was inaccessible; `--no-cache-dir`
succeeded. PowerShell aliases `gp`; use `python -m grandportage.cli` for reliable
invocation. DK git reads may need per-command
`-c safe.directory=$DEV/math-research/campaigns/dk-retrodiction`.

## Independent Lane Watch implementation

Changed tracked files:

- `src/coordinator-session-service.ts`
- `src/campaign-action-router.ts`
- `src/campaign.ts`
- `src/ui/CoordinatorConsole.svelte`

New files: `tests/directive.test.ts`, `DIRECTIVES.md`.

Action `coordinator.directive.record` uses the existing action/event path.
It stores exact operator text (up to 12,000 characters), actor, UTC timestamp,
event UUID, coordinator thread and latest completed assistant response from the
sanitized conversation view. The recommendation records message/turn/source and
its 20,000-character view limit; absent recommendation is explicit null. This
is a snapshot of the current response, not a new semantic recommendation parser.
Attachment changes while reading refuse. It sends no message and starts no turn.
The UI has Record as directive and displays the last 20 events in append order;
all events remain stored. Display uses normal escaped Svelte text.

Validated: 28 tests / 188 expectations across directive, campaign-adviser and
architecture-boundaries; TypeScript exit 0; Svelte 0 errors/0 warnings. No live
browser interaction or deployed-service smoke test was performed. Staging helpers
under GP `tmp/lane-directive/` are ignored scratch, not the product source.
Do not reapply their installer over already-applied changes.

## Next steps in order

1. Preserve the released v0.33 authority boundary and its characterization
   fixtures; do not bypass it when adding new evidence reach.
2. Candidate v0.34 / epoch 12: freeze rules and expected outputs before
   implementation, using the concrete corrections below plus the complete
   preflight matrix. Implement vocabulary/closed validation and pure judgments;
   certificate reach and migration; explicit family/model composition;
   CLI/MCP/schema/Lean parity; DK replay and `SEAM.md` from checked examples.
   Acceptance fixtures precede each change.
3. After the receipt boundary, add minimal proof slices and authority-aware diff
   from that single source of truth. Treat truth-maintenance algorithms as an
   implementation aid for support slicing and invalidation, never as a source of
   mathematical licenses.
4. Independently finish Lane Watch delivery through its normal workflow. A
   service restart and live smoke test were not recorded here; do not imply one.
5. T2 is a separate bounded customer exercise, not yet selected or launched:
   candidates are the 28_5 ceiling, E5 generative bridge, or 19_4 sector reproof.
   Measure changed decisions/open slots and custody commits per accepted claim
   against the pinned DK proxy of 189. ARR15 retrodiction follows B.

## Epoch-12 rules still needing a concrete contract

The preflight's recommendations were approved in direction; detailed schemas,
function signatures and per-certificate migration have not been written yet.
This is the next design work, not a reason to reopen settled Phase A choices.

- Use one field vocabulary with distinct judgments for concrete compatible
  extension, universal certificate instantiation, and witness transport.
  A real witness to x^2-2 cannot generalize to ANY_ORDERED (Q has no root).
  A complex witness to x^2+1 cannot generalize to ANY_CHAR_0 or R. If the
  original single-order constraint is insisted upon, stop with these counterexamples.
- Preserve `point_universe`, `witness_field`, exact coordinates, selected
  embeddings and coefficient maps. Q-defined closure points can require i;
  comparing Q <= R alone would falsely license real existence. Missing universe
  is not automatically BASE. Define how about/compute/presentation/closure relate.
- General number-field coefficient computation is not supplied merely by
  existing number-field witness support. Reuse supported exact domains, define
  aliases, reject contradictory old/new declarations and ambiguous embeddings.
- Reach must be certificate-specific, evidence-bound and currently justified.
  Uniform ORDERED differs from a sign at one selected root. CHAR_0 retains
  coefficients, localization/chart coverage and embedding obligations.
  FIELD_SPECIFIC is not a fallback for failed evidence. Search/cap/timeout and
  NO_RATIONAL_POINT_SEARCH cannot earn EMPTY authority; use UNRESOLVED for work.
- Do not blanket-migrate true -> CHAR_0 or false -> FIELD_SPECIFIC. In
  characteristic 2, 2*x-1 generates the unit ideal but has rational root 1/2.
  Preserve finite-characteristic/reduction semantics and historical readability,
  with explicit authority invalidation and an auditable conversion table.
- Check endpoint field scope across every point-carrying edge, equivalence,
  partition, same_as and multi-edge path, plus CLI/MCP/probe/verifier/reload.
  Fixing BASE_EXTENSION alone leaves alternate paths. Keep the kernel model-blind
  via validated semantic facts at the authority-binding boundary.
- Define family/model composition explicitly: enumeration debt, evidence
  direction, stale premises, EXCLUSIONS-only evidence and open E5 must remain
  load-bearing. `established_by` provenance and an evidence ladder are not a
  numeric theorem-authority order. Test premise permutations, not just one order.
- Preserve P0 false descent, selected-root/sign controls, identity descent and
  chart coverage. Add positive explicitly typed Q->R and compatible real K->R
  cases; frozen X3 and legacy omitted-universe cases are not those positives.
- New semantic fields belong in validation, migration, fingerprints,
  supersession, schema/help/export and Lean epoch shadow. A changed receipt
  context must stale old authority. No unrelated package-wide refactor is needed.

## Suggested opening instruction for the next task/session

> Continue the approved Grand Portage work using
> `$DEV/grand-portage/review/v0.32/SOL-HANDOFF.md` as your starting
> point and `DESIGN_DIRECTION.md` for the current sequencing rationale. Phase A
> v0.33.0 is released with Match4 hardening and the output-preserving
> authority-binding nucleus. Preserve that boundary, the accepted preflight
> corrections, and immutable DK fixtures while freezing B's concrete rules and
> expectations. Do not implement the original single-order or blanket boolean
> migration.
