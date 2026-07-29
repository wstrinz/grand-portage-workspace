# HANDOFF.md — read this first

Written for a session with **no prior context**. Everything needed to pick this
up is here or linked from here.

---

## 1. What this is, at the smallest size that is still true

**Grand Portage** records what each modelling step in a computational-algebra
campaign *loses*, and refuses the conclusions that loss does not support.

A computation produces an artifact. The artifact does not carry its own licence
to conclude. A Gröbner basis reducing to `1` is *evidence* of emptiness; what
makes it a *kill* is the certificate attached and the scope that certificate
derives. Conflating those is how the parent project shipped an erratum.

It is the successor to `whetstone/` in the `math-stuff` repo, where the same
discipline exists as three single-file prototypes with their domains hardcoded.
**What is new here: the graph is data, the transport table is the only code.**

Five layers, enforcement in exactly one:

```
agent → MCP server (edge REQUIRED, no declaration → no CAS process)
      → .portage/graph.jsonl  (append-only; the graph is the state)
      → kernel (6 edge types × 2 directions × 4 claim kinds)
      → checker → findings → discharge moves
      → hook (runs after each tool call, exit 2 = refuse)
```

Drop the hook and it is telemetry. Drop the MCP server and it is a linter
nobody runs.

**Age: about seven days. Version 0.4.2. <!--checks-->779<!--/checks--> checks.** Treat
every claim in the docs as provisional.

There is now a **public repo**: `github.com/wstrinz/grandportage`, Apache-2.0,
the tool plus all three fixtures plus `DESIGN.md` / `REVIEW.md` /
`docs/first-run/`. This repo is `grand-portage-workspace` (private) and holds
the two things the public one deliberately omits: `TESTPLAN.md` and this file,
because both describe traps in unrun blind trials.

### Where the last three versions came from

**Every structural change since v0.2 was forced by a live run failing**, not by
review. Worth knowing because it predicts where the next one comes from.

| test | verdict | what it forced |
|---|---|---|
| **T3** resumability | **FAIL** | no read path showed which findings were knowingly accepted, so a fresh agent read a healthy campaign as a failing one → `[CARRIED]` marking, `gp show` printing inferences and certificates, `portage_check`'s advertised-but-unread `full` flag |
| **T1** blind run | **FAIL** | an agent superseded a refusal instead of satisfying it → `PARALLEL-EDGE`, `VACUOUS-CONCLUSION`, `SELF-BUILT`, `partition`, `premises`, typed discharge |
| **T2** external review | 8 defects | the CAS boundary was still bypassable **through the fix for it** |
| **T4** merge fan-out | **PASS / FAIL** | kind laundering, existence on the honour system, `gp merge` |
| **T5** foreign campaign | **PASS** | the `ladder` split, open premise slots, `CITED_PROOF`, `TYPE_MEANS` |
| **L1** toric containment | **premise refuted** | the containment model held but had never been under load → `verify.containment` |
| **W5/L4** identity live-test | 13 defects | **the verifier had no surface at all** → `gp verify`, `portage_verify`, the `verdict` event kind, GATE 3 |
| **GPT-2** prior-art review | 2 kernel errors | `SPECIALIZATION` ignored `identity_origin`; the `RESTRICTION` density gate was insufficient *and* mis-typed |

### The reviews found the mathematics; the runs found the tool

Worth stating because it corrects a complacency this document used to carry.
For five live runs the score was **nine interaction defects to zero kernel
errors**, and I read that as the mathematics being settled. It was not — it was
nobody attacking it. An external review doing actual mathematics against the
table found two false licences in an afternoon (a nodal cubic and a
`p`-torsion example), both confirmed.

So the two channels find different things and neither substitutes for the
other. Live runs find what the tool does to a working user. Adversarial
mathematics finds what the table licenses. **Run both.**

Full results in `portage-depot/testing/`, each with its pass condition written
*before* the run.

**T5 is the one to read if you read one.** It pointed the tool at a border-rank
/ SOS campaign that had never heard of it: **zero false positives**, and the
checker escalated a finding to `UNSOUND_CONCLUSION` by noticing that a
refereed bound recorded elsewhere in the graph contradicted what the inference
would license. That reductio fell out of the fold. **The five edge types
survived foreign mathematics** — contrary to both my prediction and the
external review's, border rank did *not* break the ontology. Everything
*around* the types is what didn't fit.

### Where things are, physically

```
dev/
  grand-portage/            THE TOOL, private. github.com/wstrinz/
                            grand-portage-workspace
  grand-portage-public/     the public mirror, pushed to
                            github.com/wstrinz/grandportage (Apache-2.0).
                            Sync = copy grandportage/ tests/ fixtures/ docs/
                            DESIGN.md README.md REVIEW.md. Root-level files do
                            NOT sync, which is why DESIGN_DIRECTION.md and this
                            file stay private.
  portage-depot/            campaigns + testing evidence. Local only, no remote.
    campaigns/gamma-delta4/   the T1 run. Typing defects LEFT UNREPAIRED --
                              that graph is the evidence.
    campaigns/lsem-census/    the sustained run. See below.
    testing/                  T3/T4/T5 conditions + results, T1 runbook
    campaigns/jc2-chartmap/   the chart-map lead. NEXT: the GGV1 Prop 8.3
                              task extends this graph, which already carries
                              M1_G4, the P_GAMMA partition and INF_G4_HOLE_V2
    campaigns/borderrank/     S2, finished and green
    campaigns/toric-phases/   L1, finished. Refuted its own premise, usefully
    LANES.md                  candidate domains not yet started
    tools/wire_topcom.sh      TOPCOM is apt-installed as `topcom-*`; Sage wants
                              the bare names. Run once per fresh environment
    math-stuff/               one shared submodule, pinned e145e8e
  math-stuff/               THE RESEARCH REPO. READ-ONLY, always.
```

**Anything under a syncing path names no live research domain, on purpose.**
Code comments and test docstrings say "a live campaign" where they mean the
identifiability census, because the census is unpublished and its later
sessions are aimed at results worth first arrival on. Every design lesson
survives the generalisation; only the domain pointer is dropped.

The scrub is done **in this repo, not in the mirror**, so a sync stays a plain
copy. A sync that needs a manual scrub step is a step whose correctness depends
on someone remembering, which is the exact defect class §7 of REVIEW.md
tracks. If you write a new comment citing a campaign, write it generic here —
do not write it specific and plan to strip it later.

The public/private split is about DOMAIN, not about candour. Findings against
the tool itself stay fully specific in public: that is the point of the file.

### THE CENSUS IS SEALED. Do not write to it.

**`campaigns/lsem-census/.portage/` must not be written to before 2026-08-03.**
It is the subject of L3, the cold-return experiment, and its prose and scripts
are moved to `.sealed/`. Protocol and fixed grading criteria:
`portage-depot/testing/L3-PROTOCOL.md`, written before the run.

L3 gates the main JC(2) persistent investigation on three conditions: two
consecutive live sessions with no blocking tool defect (currently **zero of
six**), `portage_declare` working end to end in a real campaign (it has failed
in two consecutive sessions), and the cold return measured. Tool changes during
the gap are expected and are part of the test.

### The sustained run, now sealed

`campaigns/lsem-census` — generic identifiability of linear structural equation
models on small mixed graphs, via Macaulay2's `GraphicalModels`. A **census
rather than a conjecture**, so sessions end when a case finishes instead of
when someone gets stuck, and cases share models so the graph accumulates.

This is the first test of the claim the whole design rests on: *after three
weeks the graph is the state*. Every previous run was a single bounded task.

**The measurement that matters more than the mathematics:** do three or four
cases, let a week pass, return cold with no notes outside `.portage/` and no
scrollback, and time how long until productive. If a returning *human* cannot
resume from the graph, a returning agent certainly cannot.

### `gp migrate` — read this before bumping a required field

Required fields break existing graphs. That bill came due all at once:
`witness_kind` and the `ladder` vocabulary stopped **three live campaign logs**
from folding, including T1's own output.

`gp migrate` fills them with the **ignorance value** — `UNKNOWN`, `ASSERTED`.
The no-silent-defaults principle survives because those are not guesses; they
are true, the claim having been recorded before anyone was asked. Both report
as debt, so migrating makes the graph *louder*.

It **refuses to touch a field whose value is wrong rather than missing** and
exits nonzero. The T5 graph still does not fold for exactly this reason: four
`ladder` values need a human to decide whether they belong in `established_by`,
`caveat`, or are genuine strength claims.

**Candidate 16th design invariant: every required field ships with a migration
that fills the ignorance value.**

**The recurring shape, SIX instances now:** a field that DETERMINES transport
and is taken on the author's word. Certificates (pre-v0.2), `identity_origin`
(pre-v0.3), `kind` (pre-v0.3.1), `ladder` (pre-v0.3.2, found by T5 when a
foreign campaign filled it with seven values and no overlap with the five it
declares), `established_by` (pre-v0.4), and — the deepest — **`V(src) ⊆ V(dst)`
itself** (pre-v0.4.1). Each was found by someone *using* or *exploiting* it,
never by review.

**The sixth is the one that matters most.** Every edge asserts that
containment; the kernel's opening comment says so and all six types are
relaxations in that sense. Nothing ever checked it. L1 found the cost: a flop
is an isomorphism in codimension one, so neither variety contains the other,
and typed `EQUIVALENCE` it *"yields a false conclusion reported clean behind
one prose-dischargeable DEBT"* with *"nothing in the tool [that] would have
stopped me"*. `RESTRICTION` matches a flop on every clause except that one.

Being repaired on branch `w5-structured-models`: models now carry their ideals
(phase 1), and `I(dst) ⊆ I(src)` is checked by reduction (phase 2, verified
against Singular). **Phase 3 remains** — the exact identity condition
`LHS − RHS ∈ I(dst)`, which discharges a second registered conservatism, since
the register already calls `AMBIENT` *sufficient but not necessary*. It is the
same reduction pointed at a claim instead of an edge.

**THE REPAIR RULE, and it is the best general principle in this corpus:** make
it derivable, make it checkable, or make it compose with something already
checked — never "try harder to fill it in correctly." This belongs in
`DESIGN.md`'s design invariants and is currently only here.

**The fifth instance is the one to learn from, because it is a mutation.** The
first four were fields whose VALUE was taken on the author's word. The fifth
was a field whose ABSENCE switched off the check on a neighbour: every key in
`IMPOSSIBLE_EVIDENCE` matches on `established_by`, so omitting it meant the
pair evaluated was `(None, "exact-checked")`, which is in no table and
contradicts nothing. Optionality is not neutral when another rule keys on it.

**AND THE REPAIR IS STILL INCOMPLETE, so this is where to look next.**
`exact-checked` now forces you to say `RAN`, and `RAN` is the only value that
survives against it — but nothing requires a run ARTIFACT. You can still write
`established_by: RAN, ladder: exact-checked` with no evidence anywhere. That is
the honour system with one more word on it. The rule above says derivable *or*
checkable; what shipped is checkable-against-a-neighbour, which is weaker.
Deriving the rung from an artifact needs the run/artifact layer, deferred from
T5 and still deferred.

### What v0.2 changed, and why it is not a feature release

An external review (GPT) plus a working pass found **eight defects, seven of
them inside the parts the project advertises as its guarantees** rather than in
the mathematics. All are fixed; suite went 171 → 251 checks.

| where | was |
|---|---|
| `kernel` IDENTITY row | licensed `x = 0` escaping `V(x)` to the whole line; and lifting `p·x = 0` out of char `p` |
| `kernel` EQUIVALENCE | licensed IDENTITY on the strength of a **point**-level converse; `V(x²)` vs `V(x)` refutes it |
| `cas` boundary | `body` and declaration expressions went to Singular unvalidated — **the exact `poly g0 = ...` defect was rebuildable through the module claiming "there is no string path to a solver"** |
| `cas` verdicts | nonzero exits outside three codes read as `OK`; `ABORTED` minted a model and a semantic edge |
| `check` witness | `witness` was documented as evidence **against** an equivalence and accepted as documentation **for** one |
| `check` taint | one pass, so second-generation taint was invisible — and that is the generation nobody inspects, because the step producing it is clean |
| `store` certificates | a graph event could silently redefine a built-in, changing the field-scope of every emptiness citing it |
| `hook` baseline | keyed by a finding id that is stable by construction, so an acceptance outlived the meaning it was given for |

**The lesson worth carrying:** a green mutation suite tests *reachability*, not
*truth*. It asks "does editing this field change a verdict?" and presupposes the
verdicts are right. `test_identity_transport_turns_on_the_map_and_nothing_else`
asserted an unsound cell as its oracle and 171 checks agreed with it — **the
test's name was the false claim.** Gate 0 (`tests/test_cell_ledger.py`) is the
missing half: one row per cell, each with a proof or a counterexample.

**New concept: `identity_origin`.** An `IDENTITY` claim must say where its
rewriting is valid — `AMBIENT` (holds before this model's equations, travels
both ways), `DERIVED` (follows from them, restricts only), or `UNKNOWN`. Blank
raises at fold time. `UNKNOWN` is the `UNTYPED` bargain one level down: the
honest answer is always available, which is what makes the field requirable.
Unlike `UNTYPED` it has a **mechanical** discharge — `cas_classify_identity`
reduces `LHS − RHS` and answers `AMBIENT` / `DERIVED` / `FALSE_AT_MODEL`, so the
tool names the computation instead of asking the author to introspect.

The retrodiction gates reproduce **identically** — same findings, same clean
inferences — but every `IDENTITY` verdict now rests on a stated reason instead
of a coincidence. `CL-KSYZ-ID` was confirmed `AMBIENT` by re-running
`divisor_syzygy.py` (7/7, C3 residual 0 by symbolic expansion).

---

## 2. Where to start, by what you are doing

| you want to… | do this |
|---|---|
| understand the design | `DESIGN.md`, then `REVIEW.md` (where it is weakest) |
| review / critique it | `REVIEW.md` — written as an attack brief, not a tour |
| know what to run next | `TESTPLAN.md` — 7 tests, pass conditions declared in advance |
| see how it behaves in real use | `docs/first-run/` — the user's own report, the maths, the graph |
| see what an audit found | `docs/first-run/T2-SYNTHESIS.md` — **start here if you only read one thing** |
| run the blind test (T1) | `cd C:\Users\wstri\dev\gamma-delta4 && claude` — see §6 |
| work on the tool | `cd C:\Users\wstri\dev\grand-portage && python -m pytest` (<!--checks-->779<!--/checks--> checks, ~10 s) |

---

## 3. Where things live

```
C:\Users\wstri\dev\
  grand-portage\    THE TOOL.  git@github.com:wstrinz/grand-portage.git (PRIVATE)
                    HEAD 0d24d35, clean, pushed.  171 checks green.
                    Installed editable (`pip install -e .`), so `gp` is on PATH
                    and edits take effect everywhere immediately.
                    Two commands: `gp` and `gport`.  USE `gport` IN POWERSHELL
                    -- `gp` is a built-in alias for Get-ItemProperty and the
                    alias wins.

  grand-portage\lean\   THE SHADOW FORMALISATION.  Lean 4, Mathlib-FREE, so
                    `lake build` is seconds.  Not authoritative: its job is to
                    try to break the ontology, not to bless it.  Does not sync
                    to the public mirror (the sync copies an enumerated list).

                    It has already taken four transport gates apart, and none
                    was the shape it looked:

                      identity_origin       a COROLLARY -- contravariance from
                                            the zero ideal, true in any ring
                      coefficients_in_base  a TYPING ARTIFACT.  The formal
                                            version could not SEE the gate,
                                            because `f g : R` puts
                                            expressibility in the type -- and
                                            that absence is what proved it is
                                            an artifact of claims being strings
                      ring_iso              CARRIES and REFLECTS, decomposed
                                            into three reductions a CAS can run
                      integral              PARTIALITY -- is the map defined

                    THE TYPING-ARTIFACT CLASS NOW HAS TWO MEMBERS, which is
                    the first evidence that it is a class and not one oddity.
                    `ImageClosure.lean` found IMAGE_CLOSURE/ALONG/IDENTITY
                    licensed on DENSITY -- wrong twice over, since a set is
                    dense in its own closure by definition, and the argument
                    concludes about POINTS while an IDENTITY here is ideal
                    membership. The honest argument is the elimination theorem,
                    and what it needs is EXPRESSIBILITY: exactly the same
                    string-vs-term condition as `coefficients_in_base`. Not a
                    fifth gate -- `_MAP_POLYNOMIAL` stays, and expressibility
                    is checked (INEXPRESSIBLE-CONCLUSION) rather than gated,
                    for the same reason the other one is.

                    What it has caught: a bad counterexample of mine, a wrong
                    conjecture of mine, a mislabelling in its own file, a
                    sequential-substitution bug in `verify.ring_iso`, the
                    SPECIALIZATION non-inclusion, the RESTRICTION reading
                    (same ideal, not the localized algebra), and this one.  None of them "the table is
                    correct".  The method is: state what a gate MEANS
                    precisely enough to be wrong, then write the Python
                    verifier against that statement rather than an intuition.

  portage-depot\    Workspace where the FIRST RUN happened.  Local only, no remote.
                    HEAD 9d42f49, clean.  Has math-stuff as a pinned submodule.
                    Contains BRIEF.md and FINDINGS.md — see the T1 warning in §6.

  gamma-delta4\     STAGED AND UNTOUCHED: the blind run (T1).  Local only.
                    HEAD 195d9c5, clean.  See §6.

  math-stuff\       THE RESEARCH REPO.  READ-ONLY as far as this project is
                    concerned.  Nothing here has ever written to it and nothing
                    should.  Currently at a83b19f on branch
                    claude/d2-jacobian-counterexamples-sgp9in.
```

**Submodule pins.** `portage-depot` and `gamma-delta4` both pin `math-stuff` at
`86d8fb0`, deliberately: the campaign graph quotes that repo verbatim and those
quotes are only true against one commit. `math-stuff` has since advanced twice
(`0dd5f71 → 86d8fb0 → a83b19f`). The only cited file that changed is
`F2_TOWER.md`, and the change is a typo fix (`(7,2)` → `(7\5,2)`). **The
citations still hold — this has been checked, do not re-derive it.** Advancing a
pin is a decision, not a sync.

---

## 4. State

**Built and gated.** Kernel, store, checker, discharge, CAS boundary, MCP
server, enforcement hook, verifier. <!--checks-->779<!--/checks--> checks,
live against Singular 4.2.1 via WSL. Two domains of retrodiction (JC(2) and
matroid realizability) against answer keys pinned before this code existed,
reproducing 4+6 flags with zero false positives and 15 clean positive controls.

### The verifier layer, as of 2026-07-28

Three verifiers a week ago, **seven now**, and all four new ones were wired up
over 27–28 July. `gp verify` runs every one that applies and records a `verdict`
event; `gp check` reads the verdicts and **the verdict beats the declaration**
everywhere it disagrees.

| verifier | decides | verdicts |
|---|---|---|
| `containment` | `V(src) ⊆ V(dst)`, by reduction | VERIFIED / NOT_BY_IDEAL |
| `identity` | the rewriting — **and mints cofactors** for a DERIVED one | AMBIENT / DERIVED / REFUTED |
| `unit_ideal` | an EMPTY's certificate, by expansion | VERIFIED / NOT_UNIT |
| `ring_iso` | an EQUIVALENCE's maps, by reduction | VERIFIED / NOT_AN_ISOMORPHISM |
| `point_witness` | a NONEMPTY's `witness_point`, by substitution | VERIFIED / NOT_A_POINT |
| `partition_exhaustiveness` | **that the cases are all the cases** | VERIFIED / NOT_EXHAUSTIVE |
| `operation_output` | that a constructor produced what it claims | VERIFIED / NOT_THE_STATED_OUTPUT |

Two things a fresh session should know before trusting any of it:

- **A certificate is now an artifact, not a word.** A verified membership hands
  back the cofactors, so `g = Σ bᵢfᵢ` can be re-expanded by a checker that
  shares no code path with the search. That is the bridge to a proof assistant:
  Lean checks a polynomial identity and should never run a Gröbner engine.
- **`operation_output` checks one direction only**, and says so. "Nothing was
  invented" is cheap and is the direction that makes EMPTY unsound. "Nothing
  was missed" is as hard as recomputing the answer and is **not** checked.

`operations.py` has a fourth constructor, `decompose`, over `facstd` — the only
decomposition reachable inside the CAS boundary, since `primdecGTZ`,
`minAssGTZ` and `radical` all live in `primdec.lib`. It emits a partition whose
branches were *minted* rather than typed, and whose completeness premise a
verifier re-decides. **Anything a constructor mints carries its own ideal**,
which is the whole of the answer to "should models be required to carry
algebra": no requirement, no migration, and the checkable fraction of a
campaign rises as it uses constructors.

**Tested in anger repeatedly**, and that is where every structural change comes
from — see the table in §1. `docs/first-run/` is the one to read: a real agent
doing real open research, which produced genuine mathematics and a very good
bug report. Five campaigns now exist in `portage-depot/campaigns/`.

**Audited twice.** `docs/first-run/T2-SYNTHESIS.md` — four independent
auditors, four lenses, and **the audit FAILED its declared pass condition on
edge type.** Then an external prior-art review found two false licences in the
transport table itself, both confirmed and both fixed.

**Three gates now guard the classes of defect that keep recurring:**

| gate | what it prevents | how it was earned |
|---|---|---|
| **cell ledger** | a licensed cell with no argument behind it | 171 green checks once agreed with an unsound oracle |
| **GATE 2** (`test_surface_smoke`) | a construct correct everywhere except in being *reachable* | three constructs in a row crashed `gp check` on first live contact |
| **GATE 3** | a message naming a command that does not exist | `gp verify` was promised in two check rules for two releases and did not exist |

GATE 2 and GATE 3 are complements and neither subsumes the other. GATE 2 asks
whether every surface survives every event kind; GATE 3 asks whether every
surface we *name* is real. **Neither asks whether a capability has a surface at
all**, which is how `verify.py` shipped twice while being unreachable from
every user-facing path. If you add a fourth gate, that is the gap.

---

## 5. THE OPEN DECISIONS — these need a human

### D1. Gap B — how to express a case-split edge — **DECIDED AND BUILT (v0.3)**

**Resolved by evidence rather than by choosing.** T1 produced the same defect a
second time, independently: a blind agent typed a γ=4 branch as a total
containment, and its `EMPTY` result landed on the whole parent while its own
prose said "branch". An auditor who had never seen this section picked option 2
— branch models — on the merits and specified it.

Built as a `partition` event naming a parent, its branches, and an
**exhaustiveness claim that must exist in the graph** rather than in a note.
Plus `kernel.transport_over_partition`, because **a case split is not
transport**: per-leg auditing correctly refuses each branch alone (`EMPTY` does
not travel `ALONG` a `NECESSARY_CONDITION`), so it needed a second inference
rule beside the table, cited via `via_partition`.

The original text is kept below because the reasoning is still the record of
why it was left open.

---

*(original, superseded)*

Two independent auditors found that `GE7`/`GE8`/`GE9` are **case branches, not
relaxations**. γ is a function of the counterexample, so `V(src) ⊆ V(dst)` is
false as a total statement — only `V(REDUCED) ∩ {γ=k} ⊆ V(GCHART_Gk)` holds.
The type system has no vocabulary for that, so a branch gets typed as a total
containment and licenses transports that are false off-branch.

**This is the most important open question in the project.** Three candidate
designs, materially different:

1. a `holds_on:` branch condition on the edge
2. model each branch as its own source model (`REDUCED_G3`, `REDUCED_G2`, …)
3. a first-class case-partition construct

Option 3 is closest to what the original whetstone notes pinned as
`MISS-C0-PARTITION` and explicitly put out of scope. **Do not pick one
unilaterally.**

### D2. Should T1 run before or after fixing B? — **DECIDED: before.**

Argument for **before**: if a blind agent hits the same wall independently, that
confirms the gap is systematic rather than one agent's slip. That is evidence
you can only collect once, and fixing B first destroys it.
Argument for **after**: T1 then tests a tool that can express the truth.

**Resolved in the v0.2 session, and the GPT review did not change it.** The
distinction that settled it: v0.2's fixes split into *what the tool licenses*
(table cells, witness polarity) and *boundary/bookkeeping* (CAS validation,
taint, baseline). The second class is invisible to an agent doing honest
modelling, so fixing it costs T1 nothing. The first class had to be fixed
because T1 would otherwise audit against a broken oracle. **Gap B is in
neither** — it is a missing expressive feature, and leaving it open is what
makes T1 informative about it.

**So: T1 is now unblocked and is the next thing to run.**

### D4. Should IDENTITY transport become edge-relative? *(new, not urgent)*

`AMBIENT` is *sufficient* but not *necessary* for a rewriting to survive
widening. The exact condition is `LHS − RHS ∈ I(dst)` — edge-relative — and a
`DERIVED` identity satisfies it whenever it follows from equations the target
keeps. Verified: `x = 0` is `DERIVED` at `V(x,y)` and reduces to 0 at `V(x)`.

**Registered as a deliberate conservatism**, not fixed, because the exact test
needs the target's ideal and **a model in this system carries `desc`, `cite`,
`chart`, `universe`, `declares`, `touches`, `reads` — it is a description, not
an object with equations.** Requiring machine-readable ideals on every model
changes what a model *is*.

Cost so far: **zero**. Two `IDENTITY` claims exist across the whole corpus, both
`AMBIENT`, both licensed; none at all in the matroid domain, the γ-window graph
or the live first-run campaign.

**The upgrade path, when a real false refusal appears:** put the evidence on the
**inference**, not the model — an inference declares it checked the difference
lies in the target's ideal, with the computation attached, and that unlocks the
one cell. Same shape as `certificate` on an `EMPTY` claim. Do not reach for it
before a campaign actually hits the refusal; the point of registering the
conservatism is that it becomes visible when it starts to bite.

### D3. `portage_suggest_edge` — build it or not

The first run's cost split was ~2/3 genuine modelling, 1/3 transcription, and
the transcription was always *"say again what you said for the neighbouring
edge, with one field changed."* So the fix is a **sibling-edge diff**, not
type-guessing.

**But it may destroy the tool's best property.** The single best finding of the
first run — a determinant of −2 showing GGV3's "automorphism" is a 2-fold cover,
and thence the congruence structure GGV3 leaves unexplained — came from having
to fill in `map_kind` *from scratch*. A diff that pre-fills it means that
finding does not happen. `TESTPLAN.md` T6 says: measure both sides or do not
build it.

---

## 6. What is staged and ready: T1, the blind run

`C:\Users\wstri\dev\gamma-delta4\` — clean directory, own pinned submodule,
campaign graph and baseline carried forward, MCP + hook wired, `TASK.md` and
nothing else.

**To run it:** `cd C:\Users\wstri\dev\gamma-delta4` then `claude`. MCP servers
register at session start, so this only works from that directory — starting
anywhere else points `GP_ROOT` at the wrong campaign.

**The task:** derive Δ′₄, the reduced polygon for the γ=4 chart, turning the
window cap α from an obligation into a number. Real, bounded, and the
campaign's own named discharge for `GE10`.

### Preserving blindness — this is the whole point of T1

The first run's agent had read a brief naming mislabelling as the worst failure
mode and blessing `UNTYPED`. It then avoided mislabelling and used `UNTYPED`
correctly. **That is an observer effect and the finding is close to worthless.**

So:

- **Do not let the T1 agent read** `BRIEF.md`, `FINDINGS.md`, `TESTPLAN.md`,
  `REVIEW.md`, `HANDOFF.md` or `T2-*`. They live in `grand-portage\docs\` and
  `portage-depot\`. `gamma-delta4` is deliberately clean of all of them.
- **Do not tell it anything is being tested.** Give it `TASK.md` and the tools.
- **The α = 4^(3−γ) trap is left in on purpose.** It fits both known values and
  hands you γ=4 for free. `TASK.md` does *not* warn against it — an earlier
  draft did and that was removed, because warning in prose tests only whether an
  agent can follow an instruction. The warning lives in the **graph**, as
  `GI-G4-CAP-EXTRAPOLATION` and its baseline reason, reachable through
  `portage_check`.

So T1 also asks: **does a standing obligation reach someone who was never told
it exists?**

**Prediction, on the record before the run:** it will pick a
defensible-but-wrong type at least once, most likely `NECESSARY_CONDITION` where
the truth is `IMAGE_CLOSURE` — "this step drops conditions" is the easiest story
to tell about almost any step.

---

## 7. Open findings, prioritized

Full detail in `docs/first-run/T2-SYNTHESIS.md`.

| # | gap | status |
|---|---|---|
| **A** | **the certificate is never validated against the computation** | still open — but see below, v0.2 built the *pattern* for it |
| **B** | **no vocabulary for a case-split edge** | needs D1 |
| **C** | an inference can attach to a **proxy edge** — nothing checks the path is the step `asserted` describes | not built |
| **D** | **no retraction mechanism** — a wrong edge cannot be corrected without hand-editing an append-only log | not built |
| **E** | `ev: "note"` **bypasses the checker entirely** | not built |

**A is a soundness hole and should probably be fixed before anything else.**
The evidence for it is that *I* got it wrong: `GC-A2-KILL` in this repo's own
fixture declares `UNIT_IDEAL_CERT` for an ideal where `1 ∉ I` (verified: basis
size 19, exhibited point satisfies every generator). `a2_certificate()` exhibits
nilpotency, and its own docstring says it is "NOT a scalar syzygy". The
certificate is the one field `derive_scope` trusts blindly to mint
field-independence.

**The cheap fix:** `cas_ideal_is_unit` already knows whether the basis came back
`1`, so the checker can cross-reference any `UNIT_IDEAL_CERT` claim against a
recorded computation, and flag claims whose certificate has no computation
behind it at all. That would have caught mine.

**v0.2 built this pattern once already, for a different field.**
`cas_classify_identity` decides `identity_origin` by computation instead of
asking for it, and the design generalises directly: a tool that *answers* the
question, a field the author still has to *declare*, and a checker that can tell
a declaration with a computation behind it from one without. Deliberately kept
separate — a tool that both decides a field and writes it leaves nobody holding
the claim.

Certificates are the harder instance and that is the only reason they are not
done: *"does this computation support this certificate kind?"* needs
interpretation, whereas origin classification is a normal-form reduction with a
three-way answer and no room to argue. **Do A next if T1 is blocked for any
reason** — the shape is now proven.

**Known campaign-level errors** (in `portage-depot`'s graph, not the tool):
`GE10` drawn backwards; `E-G3_ELIM_KILL` should be `NECESSARY_CONDITION` not
`IMAGE_CLOSURE`; `GE9`'s witness is wrong and a correct one is already in the
graph unused; `GC-A5-DERIVED` graded `exact-checked` for a slope the producing
code labels FITTED; 10 of the headline "30/30 published data points" are
vacuous by construction. **None of these has been fixed** — see gap D for why
that is awkward.

---

## 8. Gotchas that will bite you

- **`python - <<'PY'` heredocs in the Bash tool mangle backslash escapes.**
  `\n` inside a patch string becomes a real newline and silently corrupts source
  files, or silently fails to match and the patch never applies. This happened
  three times. **Use the Write/Edit tools for code, not shell heredocs.**
- **A POSIX path expanded inside a `python -c "..."` string is not MSYS-path-
  converted** (only standalone arguments are), so it reaches Windows Python
  unresolvable. The hook then finds no graph and **correctly fails open** — a
  false pass that looks like a fix. Use `cygpath -w`, or pass paths as argv.
- **Seed the baseline before wiring the hook.** On a graph with existing
  findings the hook blocks *every* tool call. `gp accept -m "why"` first. The
  first block now names this, but it is still the day-one trap.
- **The graph is append-only and conflicting redeclaration is a hard error.**
  There is no retraction mechanism (gap D). You cannot "just fix" an edge.
- **`math-stuff` is read-only.** It is a live research repo with its own
  103-checker suite. Nothing here has ever written to it.
- **Subagents inherit the parent session's MCP tools**, which is why T1 can be
  orchestrated from a session started in `gamma-delta4` — and cannot from
  anywhere else.

---

## 9. What not to do

- Do not advance a submodule pin without re-checking the graph's citations.
- Do not fix gap B unilaterally — see D1.
- Do not let the T1 agent see the meta-documents.
- Do not treat `docs/first-run/FINDINGS.md` as neutral evidence; it argues for
  its own edges, which is why the T2 auditors were barred from it.
- Do not add a detection to the coverage rule without removing one from the
  known-misses list. That discipline is inherited from whetstone and it is what
  keeps the limitations honest.
- Do not claim this finds equations. It routes attention to where one is
  missing. Every actual advance in the parent campaign was an equation.
