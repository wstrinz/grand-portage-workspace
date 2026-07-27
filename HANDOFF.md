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
      → kernel (5 edge types × 2 directions × 4 claim kinds)
      → checker → findings → discharge moves
      → hook (runs after each tool call, exit 2 = refuse)
```

Drop the hook and it is telemetry. Drop the MCP server and it is a linter
nobody runs.

**Age: about four days. One real user session. Version 0.1.** Treat every claim
in the docs as provisional.

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
| work on the tool | `cd C:\Users\wstri\dev\grand-portage && python -m pytest` (171 checks, ~8 s) |

---

## 3. Where things live

```
C:\Users\wstri\dev\
  grand-portage\    THE TOOL.  git@github.com:wstrinz/grand-portage.git (PRIVATE)
                    HEAD 0d24d35, clean, pushed.  171 checks green.
                    Installed editable (`pip install -e .`), so `gp` is on PATH
                    and edits take effect everywhere immediately.

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
server, enforcement hook. 171 checks, live against Singular 4.2.1 via WSL.
Two domains of retrodiction (JC(2) and matroid realizability) against answer
keys pinned before this code existed, reproducing 4+6 flags with zero false
positives and 15 clean positive controls.

**Tested in anger once.** `docs/first-run/` — a real agent doing real
open research (the γ-window compiler for a Jacobian Conjecture counterexample
search). It produced genuine mathematics and a very good bug report.

**Audited once.** `docs/first-run/T2-SYNTHESIS.md` — four independent auditors,
four lenses. **The audit FAILED its declared pass condition on edge type.**

---

## 5. THE OPEN DECISIONS — these need a human

### D1. Gap B — how to express a case-split edge *(design change, unresolved)*

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

### D2. Should T1 run before or after fixing B?

Argument for **before**: if a blind agent hits the same wall independently, that
confirms the gap is systematic rather than one agent's slip.
Argument for **after**: T1 then tests a tool that can express the truth.

My recommendation was *before*. Not decided.

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
| **A** | **the certificate is never validated against the computation** | has a cheap fix, not built |
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
