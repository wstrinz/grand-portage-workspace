# Grand Portage packet for the lead JC agent

## The assignment

Use Grand Portage (GP) as the official sidecar and promotion gate for
load-bearing exact-affine JC work. Keep exploratory algebra in the existing
research environment. Move a result into GP when it changes models or supports
a conclusion: specialization, restriction, elimination, coordinate change,
base extension, case partition, or coefficient expansion.

GP is not being asked to discover the mathematics or to contain every scratch
calculation. Its job is to preserve the meaning of successful computations as
they are composed.

## Start here

Tool repository:

```text
C:\Users\wstri\dev\grand-portage
```

Current reviewed milestone:

```text
85c39e3  Validate bounded polynomial coefficient lowering
version 0.14.0; graph format 3; kernel epoch 9
```

Read, in order:

1. `QUICKSTART.md` -- installation, graph direction, and the basic loop.
2. `OPERATION-CONTRACTS.md` -- what checked operations actually license.
3. `REVIEW.md` -- the surfaces that deserve suspicion.
4. `..\portage-depot\campaigns\v14-jc-coefficient-lowering\RESULT.md` -- the
   newest JC-shaped example.

Install and check:

```powershell
cd C:\Users\wstri\dev\grand-portage
pip install -e .
python -m pytest -q -m "not live" --basetemp .portage\pytest-agent-onboarding
cd lean
lake build
```

In PowerShell use `gport`; `gp` is a PowerShell alias. From bash/cmd, `gp` is
fine.

## Operating model

For each research lane, give the campaign its own directory and initialize it:

```powershell
mkdir <campaign>
cd <campaign>
gport init
```

The durable state is `.portage/graph.jsonl`, plus content-addressed artifacts
under `.portage/artifacts/`. Notes and transcripts are useful context but are
not authority.

Use this loop:

1. Explore freely in `math-stuff` or disposable scripts.
2. Before consuming a model-changing result, declare the source, target,
   operation, intended claim, and scope.
3. Prefer operation constructors and verifiers for load-bearing steps.
4. Run `gport check` after each semantic milestone.
5. Treat a refusal as a typed obligation, not something to word around.
6. Commit the campaign graph, evidence, and a short `RESULT.md`.

Useful commands:

```powershell
gport declare --file events.json
gport verify
gport check
gport history
gport artifacts check
gport why <EDGE_TYPE> <DIRECTION> <CLAIM_KIND>
```

The CLI is currently the best-tested authoring path. MCP is appropriate for
agent orchestration, but pass an explicit campaign `root` to every
`portage_*` tool.

## Enforcement must be tested, not assumed

GP without an active hook is still a checker, but it is not an execution gate.
For Codex, copy/adapt `examples/settings.json`, trust the project hook, enable
it in `/hooks`, and deliberately provoke one harmless refusal before relying
on enforcement. For Claude, copy/adapt the example MCP and hook files and
confirm that the agent receives the exit-2 refusal.

Do not begin from a graph with unaccepted existing findings: the hook will
correctly block every subsequent tool call. Establish or explicitly accept the
baseline first.

## What JC work is already covered

GP has already:

- reproduced the historical JC(2) semantic defects with clean controls;
- caught a bad inference during a live agent run;
- replayed W7-W10 eliminations with checked Groebner certificates;
- refused a proposed three-generator exact `dm4` target because the actual
  contraction has seventeen retained generators;
- materialized that exact contraction from a 21-element basis with 210
  critical-pair checks;
- separately certified a finite point-lift cover, because exact contraction
  alone does not imply that target points lift;
- translation-validated bounded-polynomial coefficient models and exhibited a
  scalar target point whose only lift violates the declared `dm4` degree cap.

The last result is the current mathematical front: polynomial liftability over
`Q[y]` and bounded polynomial liftability are distinct claims.

## First real integration exercise

Do not start by encoding the whole JC program. Select one live sub2 state with
fixed degree bounds and:

1. Record the original polynomial templates and caps.
2. Use `gport verify-coefficient-expansion` to validate every required
   coefficient row.
3. Record positive witnesses or scoped unit certificates in the scalar
   coefficient model.
4. Keep the source-to-coefficient lowering report distinct from any later
   elimination certificate.
5. End with `gport check`, `gport artifacts check`, and a short result stating
   exactly what is and is not licensed.

Acceptance criterion: the GP record should help a cold agent resume the
mathematical state without reading the originating conversation, and should
refuse at least the known control where a scalar lift requires
`dm4 = -y/2` but the declared cap is zero.

## Boundaries and sharp edges

- The supported semantic regime is exact affine algebra. Do not encode
  inequalities, numerical residuals, optimization, or finite census claims as
  if they shared this transport calculus.
- Exact elimination/contraction does not imply point-surjectivity.
- A complete coefficient expansion licenses polynomial-identity equivalence;
  selected rows are necessary conditions only.
- The coefficient-expansion verdict is translation evidence, not yet a
  first-class graph edge or elimination verdict.
- Generic pure-lex elimination can be prohibitively expensive on expanded
  coefficient systems. A killed or timed-out backend run earns no authority.
- Mapped equivalence requires checked `forward` and `inverse` substitutions; it
  is not literal same-coordinate containment.
- Keep `math-stuff` read-only unless the research repository owner explicitly
  changes that rule.
- The IR is evolving. Prefer small campaign adapters over broad framework
  rewrites, and bring repeated friction back as evidence for the next GP
  operation contract.

## Escalation rule

If GP refuses a mathematically sound move, first determine whether it exposed:

1. a missing hypothesis or certificate;
2. an unsupported semantic regime;
3. a conservative but intentional kernel boundary; or
4. a GP defect.

Do not weaken the claim or relabel the edge merely to make the graph green.
Preserve the refusal and the smallest counterexample or positive control, then
raise it for kernel/Lean review.

## Suggested kickoff prompt

> Read `JC-LEAD-AGENT-PACKET.md`, then the four documents it names. Confirm the
> Grand Portage Python suite and Lean build. Inspect the current live JC front
> without modifying `math-stuff`. Propose one bounded sub2 state as the first
> official GP sidecar campaign, including the source templates, degree caps,
> coefficient-expansion plan, intended conclusions, and explicit pass/fail
> criteria. Keep exploratory computation disposable; persist only checked,
> scoped evidence and the semantic relationships needed to consume it.
