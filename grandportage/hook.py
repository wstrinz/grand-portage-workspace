"""The enforcement hook: the only part of Grand Portage that can say no.

Everything else informs.  The MCP layer records, the checker decides, the
discharge table advises -- and an agent can ignore all three by not looking.
This runs after each tool call whether anyone wants it to or not, and returns a
blocking exit status when the graph licenses a conclusion it should not.

Wire it into `.claude/settings.json`:

    {"hooks": {"PostToolUse": [{"matcher": "*", "hooks": [
        {"type": "command",
         "command": "python -m grandportage.hook"}]}]}}

Design notes that are not obvious and cost something to get wrong:

FAIL CLOSED, BUT ONLY ON THE THINGS WE OWN.  A malformed graph blocks -- that
is a real defect and the agent just caused it.  A MISSING graph does not: most
tool calls in most repos have nothing to do with a proof campaign, and a hook
that blocks every session without a `.portage/` would be turned off within a
day.  A hook that is turned off enforces nothing.

BLOCK ON NEW FINDINGS, NOT ON ALL FINDINGS.  A campaign mid-flight legitimately
carries known-unsound historical inferences it has not finished repairing --
the JC(2) graph has four of them by construction.  Blocking on those would make
every single tool call fail forever, which trains the operator to disable the
hook, which is worse than no hook.  So the baseline is recorded and only
findings that were not there before block.  `gp check` remains the full picture.
"""

import json
import os
import sys

from . import check as C
from . import store as S

BASELINE = "baseline.json"

BLOCK_MESSAGE = """\
GRAND PORTAGE REFUSED THIS STEP.

%(body)s
This is not advice.  The transport recorded in the graph does not license the
conclusion drawn from it, so proceeding builds on an unsound premise.  Discharge
the finding above, or record explicitly why the type is wrong, before continuing.
"""

# Shown when the hook is live, the graph already has findings, and no baseline
# has ever been recorded.  Without this the operator's first experience is
# every tool call failing for reasons that look like a broken install, and the
# rational response to that is to delete the hook.
NO_BASELINE_HINT = """\

--- FIRST RUN? ---
No baseline has been recorded for this project, so every finding above is
blocking -- including any this campaign already knew about and is deliberately
carrying.  That is almost certainly not what you want on a graph with existing
history.

Record what is knowingly carried, once:

    gp accept -m "why these are being carried"

Only findings NOT in .portage/baseline.json block after that, so a NEW unsound
step still stops the session.  `gp check` always shows the full picture.
"""


def baseline_path(root="."):
    return os.path.join(root, S.GRAPH_DIR, BASELINE)


def load_baseline(root="."):
    p = baseline_path(root)
    if not os.path.exists(p):
        return set()
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return set(json.load(fh).get("accepted", []))
    except (ValueError, OSError):
        return set()


def save_baseline(root=".", findings=None, note=""):
    """Record the findings a campaign is knowingly carrying.

    Accepting a finding is a decision with a cost, so it is written down where
    a reviewer can see it, rather than living in someone's memory of which
    warnings are 'the normal ones'.
    """
    p = baseline_path(root)
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    payload = {"accepted": sorted(f.fid for f in (findings or [])),
               "note": note or "findings this campaign is knowingly carrying"}
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return payload


def evaluate(root=".", floor=C.UNSOUND_PREMISE):
    """Return (block: bool, message: str).  Pure -- no I/O beyond reading."""
    path = S.graph_path(root)
    if not os.path.exists(path):
        return False, ""
    try:
        graph = S.load(path)
    except Exception as exc:                     # malformed graph: fail CLOSED
        return True, ("the graph at %s does not fold:\n  %s\n\nA log that "
                      "cannot be folded is worse than a rejected write -- "
                      "nothing downstream of it can be trusted."
                      % (path, exc))
    findings = C.run(graph)
    accepted = load_baseline(root)
    rank = C.SEVERITY_RANK[floor]
    new = [f for f in findings
           if f.fid not in accepted and C.SEVERITY_RANK[f.severity] >= rank]
    if not new:
        return False, ""
    body = []
    for f in new:
        body.append("%s  %s" % (f.severity, f.fid))
        for line in f.detail.splitlines():
            body.append("    " + line)
        body.append("    -> DISCHARGE: %s" % f.discharge)
        body.append("")
    message = BLOCK_MESSAGE % {"body": "\n".join(body)}
    if not os.path.exists(baseline_path(root)):
        message += NO_BASELINE_HINT
    return True, message


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    # The hook payload arrives on stdin.  We read it so the stream is drained
    # and so `cwd` can be honoured, but nothing here depends on the tool that
    # was called: the graph is the state, and the graph is what gets checked.
    root = "."
    try:
        raw = sys.stdin.read()
        if raw.strip():
            root = json.loads(raw).get("cwd") or "."
    except (ValueError, OSError):
        pass
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]

    block, message = evaluate(root)
    if not block:
        return 0
    sys.stderr.write(message)
    return 2        # Claude Code feeds stderr back to the model as blocking


if __name__ == "__main__":
    sys.exit(main())
