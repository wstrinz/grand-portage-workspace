# TESTPLAN.md — what to run next, and what each run could falsify

One live session exists (`docs/first-run/`). It answered "does it work" and
gave one data point on "is it useful". Everything below targets a claim that is
currently **asserted but not demonstrated**.

Each test declares its **pass condition before running**, because a test whose
bar is set afterwards cannot fail. Ordered by value.

---

## GATE 0 — every transport cell is argued for. **BUILT (v0.2).**

`tests/test_cell_ledger.py`. One row per cell, each carrying a **proof**, an
explicit **counterexample**, or the exact **side condition** and what it
excludes. `test_every_cell_has_a_ledger_row` fails if a cell exists with no row,
so a new type or claim kind cannot be added without arguing for its cells.

**Why this had to precede T1.** The mutation suite asks *"does editing this
field change a verdict?"* — a real and unusual question, but it presupposes the
verdicts are right. It cannot catch a cell that is confidently wrong, and one
was: `test_identity_transport_turns_on_the_map_and_nothing_else` asserted an
unsound cell as its oracle, and 171 green checks agreed with it. **A green
mutation suite tests reachability, not truth.**

What the gate turned up, all now fixed:

- `NECESSARY_CONDITION / ALONG / IDENTITY` licensed `x = 0` escaping from
  `V(x)` to the whole line. Identities are claims about *functions*, and the
  ring map runs opposite the point map, so they pull back rather than push
  forward — unless the rewriting is **ambient** and never rested on the source's
  equations.
- `SPECIALIZATION / AGAINST / IDENTITY` licensed lifting `p·x = 0` out of
  characteristic `p`. Refused outright now.
- `SPECIALIZATION / ALONG / IDENTITY` was gated on the *map* being
  denominator-free; reduction needs the *claim's coefficients* to be integral
  at `p`. `CL-DICT`'s own `3/8` does not reduce mod 2.
- `EQUIVALENCE / * / IDENTITY` was unconditional, but the converse that earns an
  `EQUIVALENCE` is evidence about **points**. `V(x²)` and `V(x)` share their
  single point while `x = 0` holds in one coordinate ring and fails in the
  other — and saturation and radicalization are exactly that step.

**One conservatism was registered rather than fixed**, in
`discharge.KNOWN_CONSERVATISM`: `AMBIENT` is *sufficient* but not *necessary*
for an identity to survive widening — the exact test is `LHS − RHS ∈ I(dst)`,
which is edge-relative and needs models to carry machine-readable ideals. Models
are currently descriptions, not objects. Cost so far: zero, across the two
`IDENTITY` claims that exist in the entire corpus.

---

## GATE 1 — adversarial regressions. **BUILT (v0.2).**

`tests/test_adversarial.py`. One attack per defect confirmed in review, written
as the thing an adversary would actually do rather than as a restatement of the
fix — a test that re-asserts the current table would have passed against the
broken version too.

Covers: `body` and declaration-expression injection at the CAS boundary,
`execute`/`kill`/`setring`/`LIB`, nonzero exit read as a verdict, `ABORTED`
minting a model, built-in certificate overwrite, strictness-witness-as-
equivalence-documentation, taint stopping at the first generation, baseline
acceptance surviving a change of meaning, and identity origin.

**Suite: <!--checks-->1569<!--/checks--> checks, ~300--720 s on the current development machine.** Was 171 before the v0.2 pass.

### Test cadence

Plain `pytest` remains the full release gate. The markers provide explicit
subsets without changing that default:

```text
pytest -m "not live and not replay and not exhaustive"
pytest -m "replay and not live and not exhaustive"
pytest -m "live and not exhaustive"
pytest
```

`replay` means substantial deterministic decoding or reconstruction of frozen
evidence. `exhaustive` means the largest finite campaign or full source
reconstruction. `live` still means a real CAS process. Rendering and mutation
tests should consume frozen reports when their assertion does not require a
fresh replay; each authority path retains a real integration test.

---

## CONSOLIDATION GATE -- authority composition and repository seams (v0.19)

The frozen JC `c9_11` p-axis receipt now compiles to a graph-bound localized
unit-ideal certificate and earns only local `EMPTY`; attempted parent transport
is refused. `experiments/consolidation/merge_assay.py` runs four two-log
fan-outs in both orders. It records one intentional unresolved-alias diagnostic,
one exact-normalization conflict, a stale consumer after cross-branch
supersession, and stale/current verdict coexistence. The deterministic
`differential_affine.py` corpus checks sparse round trips, characteristics,
variable order, and simultaneous substitution against real Singular as an
untrusted oracle.

**Pass condition:** no new graph vocabulary; all specialized standalone
evidence remains effect `NONE`; local authority remains fingerprint-bound;
merge order does not alter the fold; external-oracle disagreements fail; and
projection relations never point to nonexistent nodes.

**Observed result:** PASS for the bounded v0.19 cases. The alias assay records
semantic-identity debt rather than inventing an alias, and the projection assay
caught and repaired certificate-verdict links that previously targeted a
nonexistent certificate node.

---

## CURRENT PRESSURE TEST -- bounded-polynomial JC coefficient lowering

The scalar dm4 campaign is complete. The active test asks whether its point
authority survives after every JC variable denotes a bounded polynomial in
`Q[y]` rather than a field element.

1. Translation-validate every coefficient of `G1,G2,G3,G5` with cap 1 on the
   seven retained polynomials and cap 0 on `dm4`. All sixteen rows through
   degree 3 must be present; omitted overflow and invented rows must fail.
2. Check the retained tuple `dm2=1`, `d2=y`, all other retained polynomials
   zero, against all seventeen equations of the scalar exact target. Then check
   its cap-0 source fiber independently. The target identities must vanish, but
   the fiber must be UNIT because the `y` coefficient of `G2` is `3/2` for
   every constant `dm4`.
3. Raise only the `dm4` cap to 1 and verify the nonunit-divisor control
   `dm2=y`, `d2=1`, `dm4=-y/2`. Every one of the sixteen full source rows must
   vanish. This proves that nonunit division can be exact while the degree cap
   remains load-bearing.
4. Attempt complete coefficient-level contraction only under a fixed budget.
   COST or backend termination records an algorithmic boundary and earns no
   exactness or point-surjectivity authority.

**Pass condition:** complete and selected coefficient checks report different
authorities; the cap-negative scalar-target point is refused by the bounded
source; both positive bounded witnesses verify; a costly contraction attempt
leaves the graph without an elimination edge or inferred lift.

**Observed result:** PASS. Three translation-validation reports replayed, the
two positive witnesses and the cap-negative unit certificate were independently
verified, and the durable campaign has zero unsound-premise findings. The
generic fifteen-coordinate pure-lex run was killed with exit 9 after roughly
four minutes, so it remains a recorded cost result only.

---

## PREVIOUS PRESSURE TEST -- JC dm4 exact target plus independent point lift (COMPLETED)

The gamma=4 blind run below is complete. The active pressure test is now the
real eight-variable JC source projected away from `dm4`, because it makes the
two ideal directions and the separate point question load-bearing in one
research-shaped assay.

1. Run `gp materialize-elimination-groebner --src JC-G-SOURCE --vars dm4
   --produces JC-DM4-LEX`. The discovered target must have the 17 retained
   generators from the 21-element pure-lex basis; all 210 critical pairs must
   replay; both `output_verdict: VERIFIED` and
   `contraction_verdict: VERIFIED_GROEBNER` must be current.
2. Reload the durable graph and run `gp artifacts check`. Exact contraction
   must be effective, while point-surjectivity and image completeness remain
   false. The earlier three-generator H target remains the refusal control: it
   is a sound `NECESSARY_CONDITION`, not this exact target.
3. Treat lifting as a new obligation, not a corollary. Supply a polynomial
   section or a finite principal-open/fallback certificate through
   `gp verify-elimination-point-lift`. Only that independent checked evidence
   may open point-surjective retained-predicate transport. A failed or missing
   cover must leave the exact target useful but point authority closed.
4. For unit-sensitive window elimination, check each load-bearing rational
   identity with `gp verify-localization-membership`. Mutating a guard,
   denominator power, localization multiplier, membership target, or cofactor
   must change the fingerprint or refuse the certificate. Passing certifies
   only the localized coordinate identity; an ambient identity and source
   transport remain separate obligations.

**Pass condition:** the exact leg is one prevalidated model/edge/two-verdict
batch with a clean artifact audit; the point-lift leg changes only point
authority and cannot repair or substitute for either ideal verdict. Invalid
retained generators, incomplete bases, false charts, and unsupported lifts are
refused without a partially materialized target.

---

## T1 — THE BLIND RUN (HISTORICAL; COMPLETED)

**Status:** completed and retained below as the preregistered protocol, not as
the next action. It failed usefully: the blind agent superseded a refusal
instead of satisfying it, which forced the parallel-edge, vacuity,
self-built-claim, partition, premise, and typed-discharge repairs summarized in
`HANDOFF.md`. The current pressure test is the bounded-polynomial coefficient
assay above.

**The claim at risk:** the tool does not induce plausible mislabelling.

**Why the existing evidence is weak, stated plainly.** The first run's agent had
read `BRIEF.md`, which names mislabelling as the worst failure mode and says
`UNTYPED` is a legal first-class answer. It then avoided mislabelling and used
`UNTYPED` correctly. **That is an observer effect and the finding is close to
worthless as evidence.** An agent told what the trap is will avoid the trap.

**Protocol.** A fresh session, in a fresh campaign directory, given:

- a real bounded task (candidate below),
- the MCP server and hook wired,
- **no `BRIEF.md`, no `FINDINGS.md`, no mention that anything is being tested,
  and no framing of `UNTYPED` as virtuous.**

Just the tools and the work. The only instruction should be the task.

**Historical staging record (the run has completed):** `dev/gamma-delta4/`. Clean directory, its own pinned
`math-stuff` submodule, campaign graph and baseline carried forward, MCP + hook
wired, `TASK.md` and nothing else. No `BRIEF.md`, no `FINDINGS.md`, no
`TESTPLAN.md`, and not adjacent to any directory containing them.

**The task:** derive Δ′₄, the reduced polygon for the γ=4 chart, and turn the
window cap α at γ=4 from an obligation into a number. Real, bounded, and the
campaign's own named discharge for `GE10`.

**The trap is left in, deliberately.** `α = 4^(3−γ)` fits both known values and
hands you γ=4 for free. `TASK.md` does **not** warn against it — an earlier
draft did, and that was a mistake: a warning in prose tests only whether an
agent can follow an instruction. The warning already exists where it belongs,
in the GRAPH, as `GI-G4-CAP-EXTRAPOLATION` and its baseline reason, reachable
through `portage_check`.

So T1 now also tests **whether the graph conveys a standing obligation to
someone who was never told it exists** — which is T3's resumability claim
arriving through the front door, on a case where falling for the shortcut has a
visible consequence.

**Pass condition, declared now — TIGHTENED in v0.2.**

The original bar was "≥ 8 of 10 edges confirmed", and that mixes two failures
with very different costs. A false **refusal** costs work. A false **licence**
can invalidate a campaign, and it does so silently and late. So:

- **ZERO false licences on any load-bearing edge.** One is a fail.
- `UNTYPED` is **costless**. An ambiguous edge left `UNTYPED` is not an error,
  it is the system working; the agent is never penalised for declining to type.
- At least one `UNTYPED` edge recorded **where one is warranted**, without
  having been told that is allowed.
- Every edge survives an independent audit of **type** and **direction** (T2).

**Also measure, separately** — these are the numbers that say whether the
discipline transfers, and the first run gave no reading on any of them:

| | |
|---|---|
| type accuracy | how many were right |
| direction accuracy | `src` genuinely the more informative model |
| honest-`UNTYPED` rate | declined where declining was correct |
| **confident mislabel rate** | typed with conviction, and wrong — the one that matters |
| discharge availability | were the suggested next moves mathematically reachable |
| overstatement pressure | did the tool induce claiming `EQUIVALENCE` |

**The audit must be done by someone who did not see the producing session or
`FINDINGS.md`.**

**Fail:** any edge typed `EQUIVALENCE` without an exhibitable converse, any
`NECESSARY_CONDITION` whose direction is backwards, or a plausible-looking type
chosen where `UNTYPED` was the honest answer.

**My prediction, before the run:** it will pick a defensible-but-wrong type at
least once, most likely `NECESSARY_CONDITION` where the true relation is
`IMAGE_CLOSURE`, because "this step drops conditions" is the easiest story to
tell about almost any step. If that happens, the fix is not a better prompt —
it is a `portage_lint` that asks the discriminating question per type ("can you
exhibit the converse?", "is this an elimination?").

---

## T2 — INDEPENDENT EDGE-TYPE AUDIT

**The claim at risk:** the types in the graph are correct, not merely
defensible.

**Protocol.** Hand a reviewer (GPT, or a fresh agent with no access to the
session that produced them) `docs/first-run/campaign-graph.jsonl` and, for each
edge, four questions:

1. Is the type correct?
2. Is the **direction** right — is `src` genuinely the more informative model?
3. Does `drops` name what is lost, or restate `why`?
4. Where `UNTYPED` was chosen, was that honest or evasive?

Do **not** show the reviewer `FINDINGS.md` first; it argues for its own edges.

**Pass condition:** ≥ 8 of 10 edges confirmed on type *and* direction, with any
disagreement being a genuine judgement call rather than an error. **Fail:** any
edge whose direction is wrong — that is a silent licensing bug, not a style
disagreement.

**Cheap and high value.** This is the single best use of an external reviewer,
and it is better spent here than on the Python.

---

## T3 — RESUMABILITY

**The claim at risk:** *"After three weeks the graph is the state, not the
transcript. A fresh agent reads a typed artifact instead of reconstructing
intent from 400 messages."* Asserted in `DESIGN.md` §1.1. **Never tested.**

**Protocol.** New session. Give it the campaign directory and **nothing else**
— no handoff document, no `STEP2_GAMMA_CHART.md`, no chat history. Ask: *"What
is the state of this campaign, what is blocked, and what is the next move?"*

**Pass condition, declared now:** from `portage_show` + `portage_check` alone it
must name (a) the four standing obligations, (b) that the γ=4 cap is a located
obligation rather than a number, and (c) at least one correct next action drawn
from a discharge message.

**Fail:** it needs the markdown to make sense of the graph. That would mean the
graph is an index to the real state rather than the state, which is a weaker and
much less interesting claim than the one in the design doc.

---

## T4 — MERGE UNDER REAL FAN-OUT

**The claim at risk:** *"a merge of twenty agent branches either composes or
fails loudly."* Unit-tested only; no two real agents have ever merged.

**Protocol.** Two agents, same campaign, isolated worktrees, adjacent but
overlapping subproblems — deliberately arranged so both will want to declare a
model for the *same* object. Then concatenate the logs and fold.

**Pass condition:** either the merge composes, or it fails with a conflict
naming both versions. **Fail:** a silent blend, or a fold error so unhelpful
that resolving it means hand-editing an append-only log.

**Watch for the thing unit tests cannot show:** whether two agents naturally
choose the *same id* for the same object. If they do not, the merge succeeds and
produces a graph with two models for one thing — which folds cleanly and is
wrong. **That is the real fan-out risk and no current check catches it.**

---

## T5 — A CAMPAIGN NOT BUILT FOR THE TOOL

**The claim at risk:** zero false positives. Both retrodiction fixtures were
authored by people who already knew the type system; the γ-window graph was
authored through the tool. None of that tests what happens on a campaign that
never heard of it.

**Protocol.** Point it at the border-rank / SOS reconnaissance work (the second
worktree named in `SESSION_HANDOFF.md`, branch
`worktree-borderrank-sos-recon`). Model its steps *as recorded*, without
adjusting the modelling to suit the checker, and count findings.

**Pass condition:** every finding is either a real obligation a domain expert
would accept, or explicable in one sentence. **Fail:** a wall of findings that
have to be baselined en masse — which would mean the tool is tuned to campaigns
that were already thinking in these terms.

**This is the generalization test.** The matroid domain showed the *table*
transfers; this would show the *practice* does.

---

## T6 — `portage_suggest_edge`, A/B

**Historical dependency satisfied: T1 completed.** The design is now specified by evidence: not "guess the type
from the computation" but **"offer the sibling edge's declaration as a diff and
make me change the field that differs."**

**Protocol.** Build it, then run the same shaped task twice — once with, once
without — and measure the ratio the first run reported: genuine modelling vs
transcription.

**Pass condition:** the transcription fraction drops below the observed ~1/3
**and** T1's audit standard still holds. **Fail, and this is the one to watch
for:** the modelling fraction drops too, because autofill removed the moment of
thought. The first run's best finding — the determinant of −2 — came from
having to fill in `map_kind` from scratch on `GE7`. If a diff would have
pre-filled it from a sibling, that finding does not happen.

**So the honest framing:** T6 risks trading the tool's best property for its
worst annoyance. Measure both sides or do not build it.

---

## T7 — LONG-SESSION HOOK BEHAVIOUR

Lowest value, cheapest to run — fold into any of the above.

Watch for: repeat-suppression working across a long session; the baseline not
churning; `.portage/last-block` not going stale after a genuine fix; the hook's
cost per tool call staying invisible.

---

## T8 - FRONTIER PREMISE PROPAGATION

Feed `frontier/v1` an immutable historical envelope whose final premise is
open, then add an exact-scope discharge overlay. The historical status and
premise must remain visible while the effective status changes. A downstream
consumer may change only when its exact scope is listed in
`exports_to_scopes`; a merely narrower-looking or wider-looking scope must not
inherit anything.

For the JC consumer, bind all five native receipt bytes without running the
math-stuff release suite. H8 must discharge across depths 8--15, and only the
declared operator-schedule and degree-34 depth-nine consumers may lose their
H8 qualifier. The recorded `c7_9` family must be closed while pin ablation and
full `b=0` source exclusion remain open. Mutate a fixture byte, scope id,
receipt verdict, or exact `face(8,1)` value; the replay must refuse.

## T9 - COLD-RETURN DECLARATION AND SECOND FRONTIER CONSUMER

Create separate native root and sidecar graphs, then declare through global
`--graph`. Only the selected sidecar may change and success must print its
absolute path. Repeated `--graph` values must refuse before stdin is read. An
explicit epoch-0 target must remain byte-identical after refusal. Drive the
same cases through the literal `portage_declare` console function so the MCP
fallback cannot drift into a second writer.

Compile the landed depth-six seam ledger through `frontier/v1`. All five local
frontier records must receive stable semantic IDs and remain open without
flattening their native status strings. R6 and Q relocation retain three
stable source premises, the parent target-pair seam retains a distinct scope,
and the review receipt must regenerate exactly. The H8 and depth-six consumers
must share a schema while differing in both source shape and whether they emit
premise updates.

## T10 - PIN-ABLATION SCOPED RESULT

Bind the three native pin-ablation certificates and the coordinator handback by
exact digest. The ranked task must resolve without closing full `b=0` source
exclusion. Assert uniform `c2_2` exclusion separately from joint confinement;
keep the degree-130 resultant roots separate from non-normalized transport;
and retain `c2_1`, `b`, `R`, and `Delta` as open items. Mutating any bound
native byte must refuse before projection. The compact review receipt must
regenerate exactly with graph effect `NONE`.

## T11 - CROSS-CONSUMER FRONTIER CONSOLIDATION

Bind multiple compact frontier receipts by LF-normalized digest. Require every
receipt to expose stable item ID, exact scope, effective status, and open/closed
state. A repeated item without an explicit resolution must refuse. Exact open
agreement must refuse scope or status disagreement. Supersession must refuse a
non-open prior observation, an unproved current status, a repeated current/prior
receipt, or an absent/self replacement.

Compile the checked H8/c7_9, depth-six, and pin-ablation receipts. The result
must contain 20 items, 12 open, 8 resolved, and exactly two overlap resolutions.
Full `b=0` remains open through exact agreement; pin ablation becomes
`RESOLVED_TO_SCOPED_RESULTS` and names its ten bounded replacements. CLI and
library output must be byte-deterministic, and the checked current receipt must
regenerate exactly with graph effect `NONE`.

## What none of these test

Stated so the plan is not mistaken for coverage:

- **Whether the discipline finds equations.** It does not, by design. It routes
  attention. Every actual advance in the source campaign was an equation.
- **Whether the coverage rule discriminates within an axis.** Needs a second
  incident on one axis; the source repo does not contain one, so this cannot be
  tested here at all.
- **Whether any of this survives a user who is not an LLM.** Every session so
  far has been an agent that reads schemas carefully and does what
  documentation says. A human under time pressure is a different adversary.
