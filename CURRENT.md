# Grand Portage current state

This is the cold-start page. It contains only current facts. The design rationale
lives in `DESIGN.md` and `ARCHITECTURE.md`; the chronological implementation
record remains in `HANDOFF.md` and `HISTORY/`.

## Release boundary

- Package version: <!--version-->0.29.0<!--/version-->.
- Graph format: <!--graph-format-->6<!--/graph-format-->.
- Kernel epoch: <!--kernel-epoch-->11<!--/kernel-epoch-->.
- Test collection: <!--checks-->1498<!--/checks--> checks.

Plain `pytest` is the conceptual full release gate. The ordinary edit loop is
`pytest -m "not live and not replay and not exhaustive"`; deterministic frozen
campaign replay and real-CAS checks have separate `replay` and `live` lanes,
and the largest finite reconstructions are marked `exhaustive`.

The v0.29 development record is under `review/v0.29/`; the prior v0.28 release
record remains under `review/v0.28/`. The release gate separates
ordinary deterministic, frozen replay, exhaustive reconstruction, and live
WSL/Singular lanes so every collected test is accounted for without making
backend availability implicit.

Graph syntax compatibility and mathematical authority are separate. A readable
old event does not automatically retain a current verifier verdict.

## Smallest true description

Grand Portage is a certifying compiler and durable campaign graph for exact-
affine computational arguments. Its semantic nucleus has six relation types and
four model-claim kinds. It records model-changing operations, exact evidence,
and the scope of conclusions earned by that evidence. It refuses transport that
the declared loss does not support.

The repository is larger than the nucleus. `ARCHITECTURE.md` names the four
trust zones and the dependency rules between them.

## Current authority

Graph authority comes from the folded graph plus current verifier verdicts.
Standalone evidence reports do not mutate a graph and do not license claim
transport merely because they say `VERIFIED`.

The most important graph-bound authorities currently include:

- exact unit-ideal and localized-unit-ideal certificates;
- verified image-contraction and point-lift evidence;
- verified mapped coordinate equivalences;
- checked partitions and multi-premise inferences;
- exact witnesses and scoped claim certificates.

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
