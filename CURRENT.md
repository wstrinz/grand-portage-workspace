# Grand Portage current state

This is the cold-start page. It contains only current facts. The design rationale
lives in `DESIGN.md` and `ARCHITECTURE.md`; the chronological implementation
record remains in `HANDOFF.md` and `HISTORY/`.

The historical v0.32 continuation handoff remains at
`review/v0.32/SOL-HANDOFF.md`; Phase A and the v0.33 authority-binding
checkpoint have shipped. v0.34 implements the accepted epoch-12 field-reach
and family/model composition contract. `DESIGN_DIRECTION.md` holds the
prior-art reassessment and the sequence beyond this boundary.

## Release boundary

- Package version: <!--version-->0.35.0<!--/version-->.
- Graph format: <!--graph-format-->8<!--/graph-format-->.
- Kernel epoch: <!--kernel-epoch-->12<!--/kernel-epoch-->.
- Test collection: <!--checks-->1762<!--/checks--> checks.

Plain `pytest` is the conceptual full release gate. The ordinary edit loop is
`pytest -m "not live and not replay and not exhaustive"`; deterministic frozen
campaign replay and real-CAS checks have separate `replay` and `live` lanes,
and the largest finite reconstructions are marked `exhaustive`.

The v0.34 semantic release record is under `review/v0.34/`; its executable
contract and checked seam observations are under `review/v0.34-preflight/`.
The v0.33 authority-boundary release record remains under `review/v0.33/`.
Operational work records and accounting-only checks are described in
`docs/WORK.md`. v0.33 also ships `gp review` as the cold-reader-safe full
history surface, refuses free witness parameters before CAS execution, and
labels quotient identities as vacuous when a current verified unit-ideal
anchor already proves the model is the zero ring. These are diagnostics only;
they change no graph format, kernel epoch, transport cell, or authority rule.
The release gate separates
ordinary deterministic, frozen replay, exhaustive reconstruction, and live
WSL/Singular lanes so every collected test is accounted for without making
backend availability implicit.

## Release sequence

The post-v0.34 preservation-atlas work is recorded in
[`docs/ATLAS-WORK.md`](docs/ATLAS-WORK.md), with a
[`56-cell mapping`](docs/ATLAS-MAPPING-V0.md) and
[`research program`](docs/PRESERVATION-ATLAS-PROGRAM.md).
It corrects the certificate summary in `gp table`, adds Lean semantic laws and
a 139-decision reach comparison, and changes no transport licence or epoch.
This work has not been cut as a new release.
The [certificate-interpreter continuation](docs/CERTIFICATE-INTERPRETER-V0.md)
adds a syntactic derivation/evaluation proof, a concrete integer interpretation,
an unordered counterexample, and composed-path tests using the same SOS fixture.

The Match4 hardening remained a within-version diagnostic checkpoint until it
was included alongside the completed authority-boundary work in v0.33.

- **v0.33:** extracts one internal authority-binding nucleus and routes every
  existing fold-time verdict projection through it. Characterization tests
  preserve graph bytes, current judgments, format 7, and kernel epoch 11.
- **v0.34 / epoch 12:** implements explicit field context, verifier-earned
  structured certificate reach, replay-only rational SOS identities, and the
  first exact family-to-model bridge. Historical certificate booleans migrate
  through a named conservative table; unknown kinds become `NONE`.
- **After that boundary:** build minimal proof slices and authority-aware diffing;
  introduce typed claim fragments and physical regime modules only when live
  cross-regime use fixes their contracts.

The authority nucleus precedes certificate expansion because it is the seam that
must decide whether checked evidence is current, correctly bound, and licensed.
Family-to-model composition is the first explicit cross-regime test. The full
acceptance matrix and counterexamples remain in the v0.32 preflight and handoff.

The v0.33 release routes every fold-time verdict
projection through sealed `CheckedEvidence` and `AuthorityReceipt` values in
`grandportage.authority`. Subject-specific proof objects replay before the
receipt is minted; stale and malformed evidence projects nothing; rejected
elimination and point-lift proof objects remain current history without erasing
earlier authority. Receipts are retained only on the folded in-memory graph, so
format 7 and epoch 11 remain unchanged. The release deliberately does not
reclassify the pure checker's transport decisions as persisted receipts.

The v0.34 release builds on that boundary. `model.about` separates the field
whose points are discussed from the exact `compute_in` domain; EMPTY transport
uses reach projected by a current verifier receipt, not a global certificate
boolean. The point-context gate applies across every point-carrying edge and
`same_as`. A `family_bridge` composes a family premise into one model only when
exact enumeration, proved coverage, exhibited membership, and the inference's
bridge mapping all agree.

Graph syntax compatibility and mathematical authority are separate. A readable
old event does not automatically retain a current verifier verdict.

## Smallest true description

Grand Portage is a proof-carrying transport calculus for computational
mathematics, coupled to an event-sourced authority system. Today it is
implemented as a certifying compiler and durable campaign graph for exact-affine
computational arguments. Its semantic nucleus has six surface relation types and
four model-claim kinds; point transport already compiles those surface types from
smaller relation capabilities. It records model-changing operations, exact
evidence, and the scope of conclusions earned by that evidence, and refuses
transport that the declared loss does not support.

The repository is larger than the nucleus. `ARCHITECTURE.md` names the four
trust zones and the dependency rules between them.

## Current authority

Graph authority comes from the folded graph plus current verifier verdicts.
Standalone evidence reports do not mutate a graph and do not license claim
transport merely because they say `VERIFIED`.

The most important graph-bound authorities currently include:

- verifier-native execution provenance for closed solver-free contracts,
  without requiring or fabricating a Singular execution;
- independently replayed `selected_real_interval_v2` Sturm receipts;
- `simple_number_field_v1` quadratic/cubic extension-valued point witnesses;
- visible, retryable `UNVERIFIED` attempt state across every verdict subject;

- exact unit-ideal and localized-unit-ideal certificates;
- verified image-contraction and point-lift evidence;
- verified mapped coordinate equivalences;
- checked partitions and multi-premise inferences;
- exact witnesses and scoped claim certificates.
- selected REAL algebraic embeddings and replayable exact sign receipts on
  `REAL_CLOSURE` models.
- derived identity verdicts whose retained cofactor equations replay exactly,
  independent of whether a reader can currently launch the discovery CAS.

Field-relative `EMPTY` claims are actionable debt unless their model declares
both a coefficient domain and a point universe. This is a structural scope
anchor, not a claim that GP understands the geometric force of every
certificate kind.

Several newer exact checkers intentionally stop before graph authority:

- finite Laurent lowering and its coefficient pipeline;
- factor-power and factor/affine contradiction receipts;
- derived projections and visualization.

Their reports state their licenses and open obligations explicitly.

The public source release is now compiled from an immutable Git commit through
`public-snapshot-v1.json`. Every tracked path must be classified public,
private, or generated; unclassified and multiply classified paths fail closed.
The resulting `PUBLIC-SNAPSHOT-RECEIPT.json` binds every exported byte while
workspace handoffs, coordinator packets, private planning, and local
configuration remain outside the mirror.

## Live composition frontier

The signed-off JC composition frontier, native fixtures, exact adapters, and
campaign review history moved to the optional
[`grandportage-jc-campaign`](https://github.com/wstrinz/grandportage-jc-campaign)
companion in v0.28. The core repository retains the generic graph, verifier,
transport, frontier, packet, dossier, release, and publication machinery.
Campaign mathematics does not become tool authority through that extraction.

## Active release discipline

The consolidation milestone is complete. New work should consume or bind
specific open authority objects under the same discipline:

- no new edge types;
- no new claim kinds;
- no new graph fields unless a live binding is otherwise inexpressible;
- no new evidence schema unless it closes an existing composition gap;
- specialized evidence should compile to an existing smaller authority
  certificate whenever possible.

## Derived proof frontier

The generic `frontier/v1` and `frontier-bundle/v1` read surfaces compile exact
receipt observations and explicit overlap resolutions into deterministic,
content-addressed research boundaries. They remain
`DERIVED_READ_MODEL_ONLY`, have graph effect `NONE`, and refuse implicit
last-writer-wins behavior. Domain-neutral tests cover agreement, supersession,
scope mismatch, digest drift, and missing-resolution controls. Historical JC
consumers and their consolidated frontier moved to the companion repository.

## Portage Command v0

The first research-operations substrate is implemented in
`grandportage/campaign.py`. `gp campaign-packet` binds one exact bundle
observation, its source receipt and evidence-envelope ceiling, and a complete
task-catalog entry. It emits deterministic JSON, human briefs, or agent prompts
with one packet fingerprint. `gp campaign-ledger` validates checked outcomes,
useful refutations, refusal categories, mutation coverage, prior-ledger
extension, and verification debt; `--overlay` emits the future console layer.
Every surface is `DERIVED_READ_MODEL_ONLY` with graph effect `NONE`.

The domain-neutral matroid base-extension retrodiction exercises the complete
packet and ledger schema. The extracted companion retains the earlier JC pilot
as runnable historical evidence.

The RTS projection, planner, distribution layer, and `v1` schema freeze remain
deferred. The v0.28 cold trial is recorded under `review/v0.28/`; its packet
digest defect led directly to pre-emission source-binding verification.

## Campaign dossier v0

The first closeout/restart surface now lives in `grandportage/dossier.py`.
`gp campaign-dossier` compiles a graded campaign portrait, theorem-facing leaf
price cards, an artifact/replay inventory, and named closeout profiles. It is
strictly `DERIVED_READ_MODEL_ONLY` with graph effect `NONE`.

Source audit distinguishes an unchecked portable dossier, an unavailable
checkout, commit or digest drift, a matching dirty tree, and a matching clean
tree. Profiles can require a clean current source, exact claim grades, fully
priced open leaves, closed leaves, present artifacts, and passing replays.
Reconnaissance artifacts cannot be used as load-bearing support for proved,
checked, conditional, or cited claims. Open leaves require a next accepted
object and an explicit resume condition; retired representations require exact
reasons.

The self-contained synthetic fixture demonstrates a short-of-summit publication
flag alongside a blocked gold flag. Campaign-specific portraits and terminal
profiles now live in the companion repository.

## Campaign release v0

The archival release layer now lives in `grandportage/release.py`.
`gp campaign-release` binds an exact dossier input, chooses one closeout
profile, computes its transitive canonical-source and evidence coverage, and
reports replay, licensing, public-disposition, source, and profile debt. It is
strictly `DERIVED_READ_MODEL_ONLY` with graph effect `NONE`.

Only a projected-ready profile observed at a clean matching source can be
materialized. The writer rechecks every selected digest, stages into a new
directory, and emits `manifest.json`, `SHA256SUMS`, and `REPLAY.md` before an
atomic rename. It refuses existing destinations, unsafe/case-colliding paths,
unclear licenses, non-public artifacts, missing coverage, and load-bearing
evidence without a passing exact replay lane.

The synthetic fixture exercises successful archive construction and then runs
its packaged checker from inside the archive. Replay lanes now bind their exact
working directory, runtime, external dependencies, network policy, receipts,
and content-addressed checker/input/certificate/environment closure. A separate
replay-kit gate can materialize reproducibility closure without pretending an
unfinished publication profile is ready.

The extracted companion retains the signed-off publication draft, generated
portrait audit, replay-resource lock, and archive pressure tests. The core
synthetic fixture exercises successful archive construction and replay without
embedding one campaign's payloads.

## Campaign publication v0

`grandportage/publication.py` projects the same release observation into exact
portrait dependency cards and manuscript-ready portrait, residual-price,
retired-representation, replay, and blocker tables. `gp campaign-publication`
can emit the complete structured JSON or render a full report, portrait audit,
or manuscript tables as deterministic Markdown.

The projection preserves claim scopes, the proved/conditional distinction,
assumptions, consumers, evidence grades and roles, replay lanes, archive paths,
and license status. It repeatedly marks itself
`DERIVED_READ_MODEL_ONLY`; editorial tables do not become a manuscript or
mathematical authority. Output writes are atomic and protect both the release
input and existing files by default.

The companion retains the campaign-specific publication adapter and formal
consumer checks. Before either provisional schema freezes, another independent
campaign must exercise the same claim grades, price cards, terminal profiles,
and public-release path.

## Experiments

- The preregistered LSEM cold return completed in a separate context-free task.
  It oriented correctly, requested no unseal, preserved the original graph,
  declared one narrow R3 inference, and finished with zero findings. The strict
  verdict is `INCONCLUSIVE`: literal `portage_declare` was unavailable, the
  first mutation attempt correctly refused the epoch-0 log, and documented
  global `--graph` did not redirect `gp.exe declare`; an isolated epoch-1 root
  succeeded on the third attempt. The full ledger is
  `portage-depot/campaigns/lsem-census/L3-RETURN.md`.
  The measured defects are now repaired for current tasks: transactional
  declaration accepts one exact `--graph` write target, refuses repeated
  targets before reading stdin, always prints the destination, and a literal
  `portage_declare`/`portage-declare` console entry point reaches the same path.
  Epoch-0 append refusal remains unchanged and intentional.
- The v0.19 fan-out assay covers semantic aliases, normalized id collisions,
  cross-branch supersession, and stale/current verdict coexistence. The exact
  checker also agrees with a deterministic Singular differential corpus.
- Visualization is a derived read surface only. Its next features should be
  selected from measured cold-review failures, not graphical novelty.

Run `python -m grandportage.cli docs` after changing the package version,
format, epoch, or test collection. Tests reject drift in the marked fields.
