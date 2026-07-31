# Kill criteria

**What would show this project is not worth continuing, written down before the
answer is known.**

This document exists for the same reason the cell ledger does. Every transport
cell must carry a proof, a counterexample, a condition, or a declared
conservatism — no cell gets to be licensed because it seemed fine. The ledger
points that discipline at the mathematics. This points it at the project.

The specific failure it guards against: **friction is always reinterpretable as
rigour.** Every time the tool refuses something and a person spends an hour
satisfying it, that hour can be described either as "the tool forced useful
thought" or as "the tool wasted an hour." Both stories fit every observation.
Written in advance, the criteria below decide which story is true. Written
afterwards, they would be chosen to fit whatever happened.

Nothing here is a prediction. Several criteria are already measurable and two
have been measured — one fired and one did not, and the one that fired turned
out to mean something other than what it was written to detect. That is the
document working.

---

## A. Narrow to an audit tool

If these hold after several independent campaigns, Grand Portage should stop
trying to wrap every exploratory computation and become a checkpoint tool used
only at load-bearing transitions. **That is a real product, not a failure** —
it would still catch the class of error that motivated the project.

### A1. Contributors choose `UNTYPED` and never refine it

*Status: **measured, and the measurement was misread.*** See §D1. The raw
number fires and the finding underneath it is a different problem entirely.

### A2. Structured operations cover too little of the actual CAS work

**Measured 2026-07-28 — and neither branch of the decision rule fires
cleanly.** Hand-declared relation types are 88% accurate across 57 live edges
(7 clear mislabels, 6 judgement calls). But the mislabels split into
populations and constructors reach only about half: the largest single category
is five edges where *no operation happened at all* and the author correctly
determined that nothing relates the two models.

So the criterion does not fire, and the useful output was not the rate. It was
that **most observed mislabelling is not about operations**, which argues for
narrowing #27 rather than cancelling or fully funding it. Full write-up in
`EXPERIMENT-B.md`.

### A3. Experts ignore the graph and reread the transcript

Untested. The strongest available evidence would come from a cold return, and
the L3 experiment is sealed until **2026-08-03**.

### A4. Cold resumption is not materially improved

Untested, same seal. This is the single most informative measurement the
project has queued, and it is worth protecting from contamination — which is
why the census is sealed rather than merely left alone.

### A5. False refusals cost more than the errors prevented

Partially measurable now. Both sides of the ledger have entries:

- **Prevented:** a field-scope error that shipped in a public artifact and took
  an independent audit to find; a `SPECIALIZATION` cell licensing a false
  transport; a `RESTRICTION` gate that was insufficient *and* mis-typed.
- **Cost:** at least one false refusal authored by this project and corrected
  the same day — a guard that refused to verify identities at models with no
  ideal, which is precisely where an ambient polynomial identity lives.

No honest ratio yet. Both columns need to keep being recorded, including the
embarrassing one.

Added since: a witness could transport between two **mutually exclusive
branches of a partition** and the checker reported the inference CLEAN. That
goes in the prevented column, and it matters for [B3](#b3) as well — it is a
failure squarely *inside* the boundary this project claims to control, found by
reasoning about the semantics rather than by watching a user. If the errors
that matter were all in the surfaces, this one would not exist.

### A6. Operation validators become as complex as the CAS code

**Live as of v0.18; the strong criterion has not fired.** The exact-affine
validators now occupy substantial modules with dedicated adversarial suites, so
the old trigger ("needs its own test suite") has unambiguously fired. The
project no longer has a uniformly tiny trusted implementation.

The stronger failure described by this criterion is not yet observed. The
validators remain closed-schema, bounded, deterministic replay checkers. They
do not perform heuristic algebraic search, and successful authority still
depends on supplied proof objects and exact graph binding. That is a materially
smaller trust class than the CAS engines they check.

Measure this from now on by: duplicated evidence-envelope logic, unbounded or
heuristic behavior inside a checker, differential disagreements with independent
exact systems, false authority caused by parsing/canonicalization, and whether
new checker code composes into durable conclusions. If specialized evidence
languages keep accumulating without compiling to a smaller shared certificate,
the substantive A6 criterion fires and the project should narrow to checkpoint
auditing.

### A7. The relation vocabulary does not transfer beyond polynomial systems

**Not firing, with real evidence against it.** The six types survived a foreign
campaign in border-rank and another in toric geometry. What broke in those runs
was bookkeeping, grading, and read surfaces — not the edge types. One campaign
did stretch `SPECIALIZATION` to cover an *index* restriction (3 of 527 cases),
which is a genuine misuse, and it is documented in `kernel.py` rather than
quietly accepted.

---

## B. Reconsider the endeavour

Stronger conditions. If these hold, the central thesis is wrong rather than
mis-scoped.

### B1. Run-specific validation cannot meaningfully constrain mislabelling

The core bet. If a validator cannot tell a correctly-typed operation from a
plausibly-mistyped one, then the semantic layer is decoration over an honour
system and the small trusted kernel is trusted for nothing.

*Early evidence, weakly positive:* `verify.identity` caught a real arithmetic
error in a live session — not a mislabelled type, but a false statement that
correct typing would never have surfaced. That is the adjacent win, not the
one that settles B1.

### B2. RO-Crate + Lean blueprints + careful Markdown achieve the same result

The honest competitor, and it has never been run. See [experiment A](#experiment-a).

<a id="b3"></a>
### B3. The principal failures keep happening outside any boundary this can control

*Watch closely — this is the criterion the project's own record argues for.*
Across five live runs the score is **nine interaction defects to zero kernel
errors**, and then an external review found two kernel errors in an afternoon.
The mathematics has been stable for weeks; the *interaction* has failed in a
new way every session. If the errors that matter are consistently in the
surfaces rather than the semantics, a semantic kernel is solving the wrong
problem well.

---

## C. The case gets stronger

Recorded for symmetry — a document that can only kill is as unfalsifiable as
one that can only vindicate.

- The same validators serve several distinct domains.
- Cold agents resume from generated state without reconstructing history.
- Newcomers produce reviewable, creditable contributions experts can reuse.
- Independent reviewers find fewer hidden seams.
- Verified capabilities replace caller-declared certificate labels.
- Users adopt it because it removes CAS boilerplate, not because it is required.

---

## D. Measurements taken

### D1. `UNTYPED` usage — the number fired and meant something else

**Measured 2026-07-27**, across five campaigns: 57 edges, 6 `UNTYPED` (11%),
and zero ever refined away from `UNTYPED`.

> **CORRECTION, 2026-07-28. The "zero refined" figure was a measurement
> artifact.** The script looked for the same edge *id* changing type, and
> supersession never does that — it mints a new id with a back-pointer.
> Checking back-pointers instead finds `E-IV-PD → E-IV-PD-R →
> E-IV-PD-RESTRICT`, a two-step refinement chain from `UNTYPED` to
> `RESTRICTION`, plus `GE11` added as a typed successor to `GE10`. `UNTYPED`
> **is** refined. See `EXPERIMENT-B.md`.
>
> The finding below survives — it was reached by reading all six edges, not
> from the count — but the number that made it look alarming was measuring the
> wrong thing, and a criterion evaluated on a broken measurement is worth no
> more than no criterion at all.

The 11% does not fire A1 — that is a healthy minority, not a habit. The zero
looked damning. Reading all six edges shows it is not the failure A1 describes:

> **Five of the six are not relaxations at all.** They assert that *nothing
> relates* the two models — "Nothing relates the two", "share NOT ONE
> VARIABLE", "two distinct layers that share a NAME and nothing else".

`UNTYPED` means *not yet known*: a promise to type later. These five use it for
*known not to relate*, which is the opposite claim. **They can never be refined,
because no edge type is correct — the correct answer is no edge.** Counting them
as unrefined debt measures a vocabulary gap as if it were laziness.

The sixth, `E-IV-PD`, is the genuine case: a real containment with no word for
it, whose own `discharge_hint` asked for "a `RESTRICTION`/`SUBSET` edge type
whose content is containment alone". That type was subsequently built. The edge
was never refined because its graph was sealed first.

So A1 is **not firing**, and the measurement produced a finding worth more than
the criterion: *the graph has no way to say two things do not relate.*

**Independently corroborated the same night.** An agent investigating whether a
cited proposition supplied a missing premise found that it did not — wrong
model, wrong claim kind, wrong subject — and explicitly declined to record an
edge, reporting: "declaring an `UNTYPED` edge would assert that a map exists and
is merely unclassified, the opposite of what was found." Its central result was
expressible only as a `note`, which the tool's own `gp history` describes as
invisible to every rule in the checker.

Two independent lines of evidence, one from five campaigns of history and one
from a live run, converge on the same missing relation. That is what promoted it
from a review suggestion to queued work.

### D2. Doc-count drift — not firing

Six different check counts were once live across the documentation at the same
time. A marked-span mechanism plus a test now keeps them equal, and that test
has fired on genuine drift several times since — including during the changes
that produced this document.

---

## The experiments

### Experiment A

Grand Portage versus excellent Markdown, matched on model, token budget, solver
access, and stopping criteria. Primary metric is **false licences**, not
findings or prose quality.

*Not scheduled.* Its primary metric needs an answer key, and manufacturing
tasks with known-correct semantic answers is most of the cost.

### Experiment B

Manual type declaration versus operation-derived contracts. Identical tasks run
both ways; measure mislabelling rate and duplicated description.

*Queued, and the gate on the structured-operations investment.* Chosen over A
because it needs **no answer key** — the operation object knows the ground-truth
relation, so declared labels are scored against what the constructor would have
emitted.

**Decision rule, set in advance:** if hand declarations are nearly as accurate
and much cheaper, the frontend investment does not pay and §A applies. If
operation-derived contracts sharply cut mislabelling, that validates the
compiler direction.
