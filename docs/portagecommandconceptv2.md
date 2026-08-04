# Portage Command

## Campaign operations over Grand Portage — concept note, v2

**Status:** Implemented v0 campaign substrate; cold-agent experiment pending
**Date:** 2026-08-04
**Supersedes:** "Math the Autobattler RTS" concept packet (2026-08-04)

---

## 1. Thesis

Grand Portage answers: *what is known, at what exact scope, through which
transformations, and what may legally be transported?* The campaign layer
answers a different question: *what should be done next, by whom, at what
cost, and what would count as useful?*

The product is a research operations console: an issue tracker whose issues
are typed mathematical obligations carrying frozen inputs, replay commands,
required mutations, and authority ceilings — plus a ledger of attacks and
outcomes, and verification debt made visible. Nothing like this exists
between raw transcripts and a finished paper, and campaign-scale work needs
it.

The RTS projection — territory, frontier, fog — is a *view* of that console.
It is worth building eventually and worth deferring indefinitely. The
previous draft spent most of its imagination on the projection, which is
cheap, and hand-waved the campaign compiler, which is expensive. This draft
inverts that.

---

## 2. The starting line, stated honestly

The previous draft proposed as "Phase A" a read-only campaign view derived
from frontier bundles, with every visual object linked to an exact semantic
ID. That phase is substantially **built**:

- `gp project` emits `grand-portage-projection/v2`, marked
  `DERIVED_READ_MODEL_ONLY`, rejected as kernel input;
- `gp visualize` renders the Three.js explorer with tours, focus views,
  layer toggles, and exact-record inspection;
- `gp frontier` / `gp frontier-bundle` produce exact-scope receipts with
  fail-closed overlap resolution;
- `gp evidence` renders the shared contract manifest with graph effects and
  containment boundaries.

More importantly, the campaign packet already exists as **practice**. The
`review/` directory — the LSEM cold retest packet, the cold web review, the
promotion firewall — is hand-authored packets in all but name: frozen
digests, exact replay commands, explicit authority boundaries, "nothing in
this licenses H3." The proposal below is a formalization of things already
done by hand, not an invention of a new workflow. That is the strongest
available evidence that the schema will survive contact.

The open work therefore starts at the packet schema, not the visualizer. The
first provisional implementation now lives in `grandportage/campaign.py` with
`gp campaign-packet` and `gp campaign-ledger`. It is intentionally `v0`: the
current JC and matroid fixtures exercise the seam before any schema is frozen.

---

## 3. The architectural seam

Four layers, and where they live in the existing trust architecture:

1. **GP authority kernel** — mathematical legality. Zones 1–3 of
   ARCHITECTURE.md. Unchanged by anything in this document.
2. **Campaign compiler** — translates frontier items into work packets.
3. **Planner** — decides which packets to attack, with what resources.
4. **Projection** — console UI, and eventually the RTS view.

Layers 2–4 are all **zone 4: adapters and read surfaces**. They inherit its
rules — treated as untrusted producers or derived views; may consume trusted
layers, never define their mathematics — with one addition that the whole
design turns on:

> Workers return artifacts, not authority. Planners return suggestions, not
> authority. Campaign records carry graph effect `NONE`, always.

The existing discipline extends without modification: the campaign layer is
to strategy what a CAS backend is to computation — useful, replaceable, and
never load-bearing for a mathematical conclusion.

Everything below this line is campaign metadata. Nothing below this line is
mathematics.

---

## 4. The provisional core object: `campaign-packet/v0`

### 4.1 The derivation rule

A packet is not a free-form document. One implementation discovery changed
the original sketch: `frontier-bundle/v1` deliberately retains only semantic
ID, exact scope ID, status, and open/closed state. It does **not** retain the
full proposition or acceptance interface, and should not be enlarged merely
for campaign convenience.

The complete task therefore lives in a separate, digest-bound catalog. A
packet composes four independently visible blocks:

```
packet = exact bundle observation (GP, by digest)
       ⊕ task-catalog entry (campaign description, by digest)
       ⊕ source receipt's evidence-envelope ceiling (GP, by digest)
       ⊕ planning block (campaign metadata, advisory)
```

This settles, structurally, the question of which packet fields belong to GP
authority and which are campaign metadata. The observation and evidence
envelope are GP-derived and quoted by fingerprint. The task description and
planning block are advisory catalog data. A packet whose observation, source
receipt, catalog, or envelope drifts is invalid.

Several attack packets may legally target one open frontier observation. That
is the normal case during narrowing: the weighted-projective classification,
the failed `D`-ansatz compression, and the active `Q_(5,1)=0` hyperplane task
all attack `JC.H3.SOURCE.REMAINING_COEFFICIENT_MAP` without pretending to be
three different mathematical obligations.

### 4.2 Schema sketch

```yaml
schema: campaign-packet/v0
authority: DERIVED_READ_MODEL_ONLY
graph_effect: NONE
packet_id: JC.H3.SIGMA.Q51_HYPERPLANE.CLASSIFY.v0

# --- Block 1: exact compact frontier observation ---
frontier_binding:
  bundle: {sha256: sha256:..., input_fingerprint: sha256:...}
  observation:
    id: JC.H3.SOURCE.REMAINING_COEFFICIENT_MAP
    scope_id: JC.H3.SOURCE.TARGET_PAIR.SEAM
    state: OPEN
    status: OPEN_REMAINING_COEFFICIENT_MAP
  source_receipt: {id: source-target-first-value, sha256: sha256:...}

# --- Block 2: task catalog, itself digest-bound ---
catalog_binding: {sha256: sha256:...}
statement:
  proposition: <exact statement>
  scope: <coefficient domain, variables, guards, assumptions>
inputs:
  artifacts:
    - id: source_target_pair
      path: d2_plane_72_108/source_target_pair.json
      sha256: sha256:...
    - id: normalized_root_convention
      path: d2_plane_72_108/normalized_root_convention.md
      sha256: sha256:...

# --- Block 3: acceptance interface ---
requested_output:
  acceptable_forms:
    - sparse_rational_nullstellensatz_certificate
    - exact_hyperplane_component_classification
    - bounded_interface_blocker
  must_identify:
    - substitutions
    - localization_guards
    - exact_relation_at_each_stage
acceptance:
  kind: NATIVE_REPLAY                  # or GP_EVIDENCE_CONTRACT
  replay:
    command: python exact_checker.py --verify
    success: all exact checks and declared refusal mutations pass
  required_mutations:                   # acceptance criteria, not suggestions
    - id: mutate_target_coefficient
      description: alter one bound target coefficient
    - id: mutate_normalization_sign
      description: reverse the declared normalization sign
    - id: remove_unit_guard
      description: remove one required localization guard
    - id: mutate_output_digest
      description: change one byte of the returned certificate
authority_ceiling:                     # quoted from evidence_envelope
  source_receipt: source-target-first-value
  boundary: <verbatim authority_boundary>

# --- Block 4: planning (advisory, graph effect NONE) ---
planning:
  maturity: DECOMPOSABLE
  cost_class: LARGE           # coarse classes only; see §6
  lifecycle: ACTIVE
  downstream: [<frontier ids this might unblock>]
  attack_log: [<receipt ids of prior attempts, successful or not>]
```

### 4.3 Three properties worth naming

**The packet is a contract, not a prompt.** Human briefs and agent prompts
test fixtures, and review forms are all *generated* from the same packet, so
they cannot drift from each other. This is the projection discipline applied
to instructions.

**Required mutations are acceptance criteria.** A submitted artifact is
accepted only if replay succeeds *and* each listed mutation is rejected.
This is property-based testing for proofs, and it has a direct precedent:
the retrodiction gate's twenty-odd mutations that assert the gate has teeth.
A packet without mutations is a packet that cannot distinguish a right
answer from a confident one.

**The ceiling is quoted, not authored.** The boundary comes from the selected
source receipt's `evidence_envelope`, not from the compact frontier
observation. A worker cannot exceed it because exceeding it produces a
declaration GP refuses to fold — the packet contains a courtesy copy of a wall
that already exists.

**Native replay remains legitimate.** Not every useful research task already
maps to a named GP evidence contract. `acceptance.kind` therefore distinguishes
`NATIVE_REPLAY` from `GP_EVIDENCE_CONTRACT`; the campaign layer does not invent
a kernel contract merely to packetize a task.

The older `frontier/v1` fields `estimated_cost`, `potential_impact`,
`blocked_downstream`, and `smallest_next_artifact` are treated as legacy
advisory hints. The campaign catalog owns maturity, cost class, lifecycle, and
attack history; no planner should silently combine two competing estimates.

---

## 5. Frontier maturity

The planner's real decision is not a score. It is a classification — which
of four states a frontier item is in, and what work class that state
implies.

**Packetized.** The missing object is exact; an unfamiliar worker could
attempt it from the packet alone. Work class: direct attack.

**Decomposable.** Semantically clear, but several competing packetizations
exist. Work class: generate and compare bounded attack proposals.

**Unpacketized.** The boundary is understood but no productive local task is
known. Work class: packetization, not proof assault. Deploying a large
solver here is the canonical resource-allocation error.

**Fog.** The right representation, invariant, or even the right obligation
is unclear. Work class: examples, prior art, reformulation. Progress here is
map improvement, and the ledger (§7) must be able to credit it, or the
campaign will systematically starve the phase where most real progress
begins.

One quantity is first-class across all four states: **verification debt** —
artifacts produced but not yet replayed, checked, and folded. Verification
capacity is scarce and must be scheduled like any other resource. A campaign
that generates faster than it checks is not ahead; it is in debt, and the
console should show that number the way a build shows failing tests.

---

## 6. What the planner is *not*

The previous draft proposed a priority formula: probability of success times
frontier impact times information gain, over the sum of four cost terms.
This is deleted, deliberately.

None of the numerator terms can be estimated with enough reliability to
justify arithmetic on them, and a formula built from unestimatable inputs is
fake precision that will nonetheless be optimized the moment it is
displayed. The failure mode is worse than uselessness: any visible scalar
becomes the game, and §9's metric-capture risk arrives on day one wearing
the planner's uniform.

What replaces it: coarse cost classes (small / medium / large / siege),
explicit downstream-unlock lists, the maturity classification, and prose
arguments recorded in the packet's planning block. A human or an agent can
argue "this medium-cost packet unblocks three others and reduces debt" in
words that can be reviewed, disagreed with, and learned from. If a learned
planner ever earns its way in, it earns it by retrodiction against a ledger
of such decisions — the same way every other component of this system has
had to earn authority.

---

## 7. The campaign loop and its ledger

1. GP compiles the frontier (existing: `gp frontier-bundle`).
2. The compiler classifies items by maturity and emits/refreshes packets.
3. Attacks run — human, agent, CAS — and return content-addressed receipts.
4. Replay and mutation testing accept or reject artifacts.
5. GP folds accepted evidence and determines exact authority (existing).
6. The frontier recompiles; the overlay and packets refresh.
7. Every attempt, accepted or not, lands in the **campaign ledger**.

The ledger is the memory the current practice lacks: which packets were
attacked, by what, at what cost, with what outcome. It records value in
*categories*, never as a scalar score: frontier closure; scope expansion;
proof compression; negative theorems ruling out attack families;
counterexamples to unsafe inferences; improved packetization; independent
replication; debt reduction. A campaign is evaluated by reading its ledger,
not by a number — for the same reason findings have derived severities
rather than hand-assigned ones.

Failed attacks are ledger entries, not embarrassments. "Three independent
agents failed this packet the same way" is information about the packet.

The implemented `campaign-ledger/v0` is deterministic and optionally binds a
prior ledger. Every prior attempt must reappear byte-for-byte; disappearance,
changed packet fingerprints, or rewritten outcomes fail closed. Checked
artifacts and useful refutations require a passing replay plus every mutation
named by the packet. `PENDING_VERIFICATION` artifacts are counted explicitly
as debt. `campaign-overlay/v0` projects maturity, lifecycle, outcomes, and debt
for the future console, still at graph effect `NONE`.

---

## 8. The experiment that decides the architecture

Define the **cold-agent rate**: the probability that a competent worker with
no campaign context, given only the packet, returns an artifact that passes
replay and all required mutations without exceeding the ceiling.

Do not publish that scalar alone. Every trial must also land in an outcome
matrix: accepted artifact, useful refutation, correct refusal, packet defect,
worker defect, unverifiable return, or pending verification. The aggregate
rate gates distribution; the matrix explains whether packetization or worker
execution is the bottleneck.

This one number gates everything downstream:

- **High rate** → packets are genuine contracts; parallel and distributed
  execution becomes live; the Galaxy Zoo direction (§11) is worth designing.
- **Low rate** → the bottleneck is packetization itself; effort goes to
  packet templates and decomposition assistance, and nothing should be spent
  on planners, formations, or distribution until the rate moves.

This is the EXPERIMENT-B pattern — 88% measured on 57 live edges, and the
errors reshaped the design — applied to the campaign layer. It is cheap to
run: it needs a handful of normalized packets and a handful of cold
sessions, both of which Phase 1 produces anyway.

A note on multi-agent topologies, which the previous draft elaborated into
thirteen unit types and seven named formations: whether any topology beats
one careful agent with a good packet is exactly the kind of claim this
project's own discipline says to measure, not assume. Formations are a
Phase-3 experiment with the ledger as its instrument, not a design
commitment. The taxonomy is deleted until it has data.

---

## 9. Build sequence

**Phase 1 — normalize what exists. IMPLEMENTED AT v0.**
`campaign-task-catalog/v0`, `campaign-packet/v0`, `campaign-ledger/v0`, and
`campaign-overlay/v0` now have fail-closed validators. Human and agent views
are generated from the same packet fingerprint. The first JC corpus records
the weighted-projective counterexample and `D`-ansatz refutation as useful
map-redrawing outcomes while leaving the `Q_(5,1)=0` mission active. A matroid
retrodiction packet exercises the same schema without JC vocabulary.

The explorer layer remains deliberately unbuilt. Phase 2 should first show
that the packet and outcome vocabulary survives cold use; otherwise the UI
would merely make an untested contract attractive.

Explicitly rejected: the previous draft's simulated-outcomes prototype.
Simulation would test the interface vocabulary against an invented
distribution of outcomes and tune the console to fiction. The fixtures,
receipts, and hand-authored packets are real; use them.

**Phase 2 — measure the cold-agent rate.**
Run cold sessions against the normalized packets. Log every failure mode
into the ledger. Distinguish packet defects (ambiguous statement, missing
convention, wrong acceptable-forms list) from worker defects. Build the
packet template library out of what failed.

*Kill criterion, written now:* if after two rounds of template repair the
cold rate stays low **and** the failures are not attributable to packet
defects, then expert decomposition is not transferable through this
contract format, the distributed direction is dead, and the campaign layer
contracts to a private console. That would be worth knowing early and is a
respectable outcome.

**Phase 3 — packetization assistance.**
For unpacketized nodes, have agents propose decompositions; require each
proposal to state deliverables, replay, dependencies, and ceiling; select by
human review and adversarial comparison. Measure whether proposed packets
achieve the cold rate that hand-authored ones do. This phase is also where
formation experiments belong, if anywhere: same packet, different
topologies, ledger decides.

**Phase 4 — limited distributed trial.**
Only if Phase 2 gates open. Publish a few bounded, independently replayable
missions; accept outside submissions; test attribution, deduplication, and
adversarial inputs. Trust attaches to checked artifacts, not credentials —
the acceptance pipeline is already the security model.

**Phase 5 — the RTS projection.**
Last, and optional. See §12.

---

## 10. The second-domain requirement

Every live fixture except the matroid retrodiction is JC H3. A campaign
layer grown solely on JC will be JC-shaped in ways invisible from inside:
the packet fields, the maturity heuristics, the template library will all
quietly assume affine elimination campaigns.

The mitigation is to run the second domain *early*, not at the end: by
Phase 2, at least one non-JC frontier — the matroid fixture is the obvious
candidate — should have packets in the same schema, and the cold-agent
trials should include them. If the schema needs domain-specific fields that
early, better to learn it before the template library calcifies.

---

## 11. The distributed direction, with its bottleneck named

A public campaign could distribute bounded authority requests to outside
operators — human or AI. A contributor consumes exact inputs, obeys
conventions, returns an accepted output form with replayable evidence,
survives the required mutations, and stays under the ceiling. Suitable work:
finite tedious case enumeration, alternate-backend replication, certificate
reconstruction, independent mutation testing, formalization of small
transport lemmas, counterexample searches against proposed inference rules.

The previous draft said the quiet part correctly and this draft repeats it
louder: **the bottleneck is expert decomposition.** The distributed system
is viable exactly when the campaign compiler can emit packets whose
completion has precise mathematical meaning — which is why the cold-agent
rate (§8) is the gate, and why governance questions (attribution, embargo,
conflicting submissions, credit) are deferred until that gate opens. They
are real questions with no urgency.

---

## 12. The RTS projection, deferred but specified

When it is built, the projection renders the console state in territorial
vocabulary. The parts of the previous draft worth keeping:

**The map is not binary.** Open/solved coloring would be a lie. The
encoding must distinguish, at minimum: incorporated certified conclusions
(solid); conditional results with active guards (striped); one-way
projections (outline); verified artifacts with graph effect `NONE`
(translucent); independently replicated or formally hardened results
(double border); claimed transport awaiting verification (dashed bridge);
refuted transport (broken bridge); known hazard families (warning hatch);
finite residuals (satellites); unpacketized regions (fog).

**The lesson the interface exists to teach:** a result is usable only
through the exact paths along which its authority transports. Every visual
object drills down to its exact statement, scope, and receipt — the
explorer already enforces this, and the projection inherits it.

**Spectator replay** is the sleeper feature for outreach: the ledger
replayed as strategic narrative — a normalization opened a fast route but
stranded an invariant fibre; a field-scope error rolled back an apparent
kill; a scout showed the current gate cannot see the remaining component.
A faithful intermediate between transcripts and a paper, generated from
records rather than written after the fact.

**A caution carried forward:** the martial metaphor is incomplete.
Mathematical progress often redraws the map rather than conquering it. Fog
work, reformulation, and compression must read as advances in the
projection, or the projection will train its users to make exactly the
resource-allocation errors §5 warns about.

---

## 13. Risks

**Specification risk.** A perfectly verified answer to the wrong model is
worthless. Modeling remains ~95% of the cost — measured, not estimated —
and the campaign layer inherits that ratio. Nothing here reduces it; the
claim is only that packets make the modeling *inspectable*.

**Metric capture.** Any visible score will be optimized. Mitigations are
structural, not aspirational: no priority scalar (§6), value recorded in
categories (§7), campaign records at graph effect `NONE` always.

**Verification bottleneck.** Cheap generation plus expensive review yields
an impressive-looking, epistemically stagnant campaign. Debt is displayed
first-class and scheduled against.

**False legibility.** A clean map conceals unresolved assumptions. The
drill-down invariant — every pixel to its exact record — is the defense,
and it is already the explorer's rule.

**JC-shape.** Named as its own risk because it is the likeliest silent
failure. See §10.

**Kernel sprawl via the back door.** Campaign convenience must never
justify a new relation type or evidence contract. Promotion continues to go
through the existing gate: independent consumers, adversarial controls,
kernel-epoch review. The campaign layer gets no vote.

---

## 14. Open questions

1. What is the smallest useful packet type hierarchy — is one schema with
   optional blocks enough, or do map-materialization, replication, and
   enumeration packets genuinely diverge?
2. How is packetization quality evaluated beyond the cold-agent rate —
   is there a measurable notion of a packet that *succeeds but shouldn't
   have* (accepted artifact, wrong obligation)?
3. Should expected information gain be recorded at all, or refused the way
   the priority formula was refused?
4. How do negative results alter the overlay — is "this attack family
   cannot distinguish the remaining cases" a maturity transition, a hazard
   annotation, or both?
5. What is the right relationship to Lean Blueprint and formal dependency
   graphs — import, export, or deliberate independence?
6. Can the compiler eventually synthesize high-quality packets, or is
   expert decomposition irreducibly central? (Phase 3 is the experiment.)
7. Which second domain, and how early? (§10 argues: matroid, Phase 2.)

---

## 15. Immediate decisions

Do not build: the game engine into GP; a simulated prototype; a priority
formula; a formations framework; distributed infrastructure ahead of the
cold-agent gate.

Built now: the provisional task catalog and packet compiler; deterministic
human/agent views; append-only attempt ledger; campaign overlay read model;
three JC packets; one matroid packet; adversarial mutation coverage.

Do next, in order: run the first cold-agent trials; classify their failures;
repair the templates once; then add one explorer overlay layer if the packet
contract remains useful. Freeze `v1` only after that evidence exists.

The seam to preserve is the one already preserved everywhere else in this
project:

> Grand Portage knows the legal frontier. The campaign layer learns how to
> turn that frontier into work. Neither borrows the other's authority.
