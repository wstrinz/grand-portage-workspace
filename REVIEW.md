# REVIEW.md — what to attack, and where I am least confident

A brief for an independent reviewer. It is deliberately not a tour: the parts
that work are visible from the tests. What follows is where I think the risk
actually is, ordered by how much damage a mistake would do.

Everything here is four days old, has had exactly one live user session, and
is v0.1.

---

## The claim, stated so it can be falsified

> A computation produces an artifact. The artifact does not carry its own
> license to conclude. Grand Portage records what each modelling step *loses*
> and refuses the conclusions that loss does not support.

Three failure modes would each sink it, and they are not equally likely:

1. **A wrong cell in the transport table.** The system would then refuse sound
   steps or license unsound ones *with confidence*, which is worse than not
   having it. This is the highest-stakes surface and it is 60 lines.
2. **It induces plausible mislabelling.** If the required `edge` argument makes
   people pick the type easiest to justify rather than the true one, it
   launders guesses into typed facts. A tool that does this is worse than no
   tool.
3. **Nobody uses it.** Ergonomics. Partially measured, see §5.

---

## 1. THE TRANSPORT TABLE — attack this first

`grandportage/kernel.py`, the `TRANSPORT` dict. Five edge types × 2 directions
× 4 claim kinds. Everything else in the project is data or plumbing.

Semantics: edges point **tighter → looser**, so `V(src) ⊆ V(dst)`. `ALONG` is
src → dst. `AGAINST` is dst → src, which is the direction emptiness travels.

**Specific things I want checked:**

- **`BASE_EXTENSION` reverses the asymmetry.** `NONEMPTY` travels `ALONG`
  freely; `EMPTY` only with a certificate that base-changes. Is the reversal
  stated correctly in both directions?
- **`IMAGE_CLOSURE / AGAINST / NONEMPTY = NO`** is meant to be Chevalley: a
  point of the Zariski closure need not lift to the constructible image. Is
  `AGAINST` the right direction for that refusal given `src` = image and
  `dst` = closure?
- **`SPECIALIZATION` carries nothing** in either direction for `EMPTY`,
  `NONEMPTY` and `PREDICATE`, and `IDENTITY` only when the map is
  denominator-free. Justified by Fano (empty over `Q`, nonempty over `F₂`) and
  non-Fano (the reverse). Is `IDENTITY` under a denominator-free map actually
  safe here? An integral identity reduces mod p, but I have not checked
  whether every `IDENTITY` claim this system admits is integral.
- **`NECESSARY_CONDITION / IDENTITY`** is licensed in *both* directions when
  the map is denominator-free. Is bidirectionality right, or should rewriting
  only travel one way?

**A known conservatism, deliberately kept** — `discharge.KNOWN_CONSERVATISM`:
`IMAGE_CLOSURE / ALONG / EMPTY` is refused although `cl(∅) = ∅` makes it
sound. Kept because the cell derives from the generic inclusion and the case is
unreachable in practice (asserting the image is empty requires computing the
constructible image). **Is that reasoning right, or is this a latent false
positive that will bite someone?**

## 2. SCOPE DERIVATION

`kernel.derive_scope`. An emptiness claim's scope comes from its *certificate
kind*, never from the author's label. `BUILTIN_CERTIFICATES` says which kinds
base-change.

- `UNIT_IDEAL_CERT`, `NONZERO_RESULTANT`, `EXACT_VALUATION_COLLISION`,
  `DEGREE_COUNT` → `SCHEME`. **Is `DEGREE_COUNT` really field-independent in
  every use, or only when the degrees are computed over a field where the
  leading coefficients do not vanish?** This is the entry I trust least.
- Declaring a field-relative certificate at `SCHEME` scope raises at fold time
  rather than producing a finding. Is refusing to *state* it the right call, or
  should the graph be able to record a wrong claim and flag it?

## 3. DERIVED SEVERITY

`check.contradicting_claims`. A refused transport is `UNSOUND_CONCLUSION` iff
the graph holds a claim at the conclusion's model asserting the opposite
existence statement; otherwise `UNSOUND_PREMISE`.

This reproduced two prototypes' hand grading on 9 of 10 findings. But it turns
entirely on **model identity** and ignores scope — `NONEMPTY over R` at model
`M` contradicts `EMPTY` at model `M`, with no reasoning about whether `R` is in
scope. I argued the field lives in the model so no scope lattice is needed.
**Is that sound, or does it break the moment someone models two fields with
one model id?**

## 4. THE GRAPH THE FIRST RUN PRODUCED — the best available test

`docs/first-run/campaign-graph.jsonl`, plus `docs/first-run/FINDINGS.md` (the
user's own report) and `docs/first-run/STEP2_GAMMA_CHART.md` (the mathematics).

**This is the most valuable review target after the table**, because it is the
only evidence about failure mode 2. Ten edges were declared by an agent doing
real work. For each one:

- Is the edge type correct, or merely defensible?
- Is the **direction** right? (`src` must be the more informative model.)
- Does `drops` actually name what is lost, or is it a restatement of `why`?
- Where `UNTYPED` was chosen, was that honest, or was it avoidance?

Edges to look at hardest: `GE7`/`GE8`/`GE9` (the γ-chart family — `GE9` is the
one the user called pure transcription) and `GE10` (`UNTYPED`, the cap-slope
obligation). The user's own account of `map_kind` on `GE7` leading to a
determinant of −2, and thence to a congruence structure GGV3 leaves
unexplained, is in `FINDINGS.md` §"Is it useful".

**Note the observer effect:** that agent had read `docs/first-run/BRIEF.md`,
which explicitly names mislabelling as the worst failure mode. It then avoided
it. That is weak evidence and I know it — see `TESTPLAN.md` T1.

## 5. ERGONOMICS

Measured once. The user's split was ~2/3 genuine modelling, 1/3 transcription,
and they localised the transcription precisely: *"say again what you said for
the neighbouring edge, with one field changed."*

Open question: is the right fix a sibling-edge **diff** (their proposal, and
mine), or does any autofill defeat the purpose by removing the moment of
thought that produced the determinant finding?

## 6. Things I already know are weak

Stated so review effort is not spent rediscovering them:

- **Coverage detects absent structure, never weak structure.** A declared but
  too-weak component is invisible. Inherited limitation of the whole coverage
  tradition.
- **One incident per axis.** `place` and `order` each fire, and each is
  necessary — but neither shows discrimination *within* an axis, and the source
  repo does not contain a second incident on either.
- **Merge safety is unit-tested only.** Idempotent redeclaration and loud
  conflict are asserted in `tests/test_store.py`; no two real agents have ever
  merged branches.
- **Resumability is claimed, not demonstrated.** "The graph is the state" has
  never been tested by handing a fresh session only the graph.
- **`ladder` is unvalidated free text.** Nothing checks that
  `independently-audited` means what the source campaign means by it.
- **No timestamps anywhere.** Deliberate — the files stay diffable and git
  carries the when — but it means a baseline entry cannot say *when* a debt was
  accepted.

## 7. Where the bodies are buried

Three defects have already been found and fixed. All three are the same family
— **quiet damage between a computation and its consumer** — and that family is
the reason this project exists, so a fourth is likely:

1. `poly g0 = ...` shadowing a ring variable, producing false `UNIT` verdicts
   at every prime (inherited; guarded in `cas.py`).
2. An illegal `_ASSAY_` identifier prefix: Singular reported an error, kept
   going, printed empty markers, and **exited 0** (inherited; guarded).
3. `_parse_outputs` capturing one line of a multi-generator Groebner basis, so
   `GP_G[1]=f6` read as "the ideal is (f6)" (mine, found by `cas_health` on its
   first run).

And one that is not that family but is worse in kind:

4. `gp accept --only` **replaced** the baseline instead of merging, silently
   destroying a version-controlled record of knowingly-carried obligations. The
   broken path was the one the docs recommended. Caught by luck. Fixed, with
   six regression tests, and the fix makes deletion an explicit act.

**If you find a fifth, that is the most useful thing this review can produce.**
