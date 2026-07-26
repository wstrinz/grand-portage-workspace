# Wiring Grand Portage into an agent session

Copy `.mcp.json` and `settings.json` into the project's `.claude/` (or merge
them into what is already there).

Two halves, and they do different jobs:

**`.mcp.json` — the forcing function.** Registers the server whose CAS tools
require a transport declaration. `edge` is `required` in the schema, so the
model is told; the handler validates, so a model that ignores its own schema is
still refused; and `run_cas` takes it as a keyword-only argument with no
default, so no future refactor can introduce a path that skips both.

**`settings.json` — the teeth.** Runs the checker after every tool call and
returns exit 2 when the graph licenses a conclusion it should not. Claude Code
feeds the hook's stderr back to the model as blocking feedback, so the refusal
and its discharge move arrive where the work is happening.

## The baseline

A campaign mid-flight legitimately carries unrepaired historical inferences. If
the hook blocked on those it would fail every tool call forever, which trains
the operator to disable it — and a disabled hook enforces nothing. So record
what is knowingly carried:

```python
from grandportage import check as C, hook as HK, store as S
HK.save_baseline(".", C.run(S.load(S.graph_path("."))),
                 note="the recorded errata, tracked in ERRATA.md")
```

That writes `.portage/baseline.json`. Only findings **not** in it block, so a
new unsound step still stops the session. Commit the file: accepting a finding
is a decision with a cost, and it belongs somewhere a reviewer can see it
rather than in someone's memory of which warnings are the normal ones.

`gp check` always reports the full picture, baseline or no baseline.

## Environment

`GP_ROOT` sets the project root the server reads and writes (default `.`).
`GP_SINGULAR_ARGV` overrides how Singular is invoked — on Windows the default
is `wsl.exe -- Singular -q`, elsewhere `Singular -q`.
