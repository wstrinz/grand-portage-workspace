"""The CAS boundary: declare the transport, or no process is spawned.

This module is where the discipline becomes unavoidable.  Everything above it
can be ignored by an agent that simply does not run `gp check`; this cannot,
because it sits between the agent and the solver.

Three guards, each earned by a specific recorded defect rather than designed
from first principles:

1. THE TRANSPORT DECLARATION IS REQUIRED.  `run_cas` takes `edge` as a
   keyword-only argument with no default.  Omit it and you get a TypeError
   before any subprocess exists.  A computation that produces a new model
   without saying how that model relates to its source is exactly the untyped
   step the whole system exists to prevent, and the cheapest place to prevent
   it is the moment of spend.

   `{"type": "UNTYPED", "debt_why": "..."}` is a LEGAL declaration -- an
   explicitly recorded debt the checker reports.  What is not legal is silence.

2. THE IDENTIFIER ASSERT IS NON-BYPASSABLE.  `CASProgram` is the only object
   `run_cas` accepts, and its constructor validates emitted identifiers against
   the ring variables and the dialect's reserved words BEFORE the program text
   exists.  There is no string path to a solver.

   Earned by: `build_singular_program` emitting `poly g{i}` indexed by
   generator while the ansatz named its tail coefficients `g0..gz`.  The
   emitted program redefined the ring variable `g0`, so `nz` became a product
   of ideal members and `sat(I, nz)` collapsed the ideal to (1).  Result: a
   confident false EMPTY in 0.3 s at every prime, propagating to 17 rows across
   two documents and to the top-priority recommendation of one.  Contained only
   by a standing social rule that mod p is reconnaissance.

3. AN ERRORED CAS IS NOT A CAS THAT ANSWERED.  Singular reports an error, KEEPS
   GOING, prints the output markers with nothing behind them, and exits 0.  So
   exit status is not evidence, and neither is the presence of a marker.  A
   verdict is read only from a run with no `? error` line and exactly one
   parseable value per declared output.

   Earned by: an `_ASSAY_` identifier prefix that was illegal because Singular
   identifiers must begin with a letter.  Reviewing the emitter would never
   have caught it; only running it did.
"""

import json
import os
import re
import subprocess

from . import kernel as K
from . import store as S


class IdentifierCollision(ValueError):
    """An emitted identifier would shadow or duplicate something."""


class CASError(RuntimeError):
    """The CAS did not answer.  Never a verdict."""


class TransportNotDeclared(TypeError):
    """A computation tried to produce a model without typing the step."""


# ---------------------------------------------------------------------------
# Dialects
# ---------------------------------------------------------------------------
SINGULAR = "singular"

DIALECTS = {
    SINGULAR: {
        # Singular identifiers must BEGIN WITH A LETTER.  This one line is the
        # whole of guard 3's prevention half.
        "identifier": re.compile(r"^[A-Za-z][A-Za-z0-9_]*$"),
        "reserved": frozenset("""
            ideal poly ring matrix module vector int intvec intmat number
            list string map proc if else while for return def qring resolution
            std groebner sat quotient reduce lift syz res kbase dim vdim
            factorize gcd lcm resultant subst size nrows ncols leadcoef
            option short printlevel basering
        """.split()),
        "comment": "//",
    },
}


def assert_no_identifier_collision(dialect, ring_vars, decls):
    """Validate emitted identifiers BEFORE the program text exists.

    `decls` is a list of (identifier, type, expression) TRIPLES.  Keeping the
    identifier a separate field from the text is not tidiness: it is what makes
    the check and the emitted program derive from the same data, so they cannot
    drift.  A format where the identifier must be parsed back out of a
    declaration string would reintroduce exactly the gap this guards.

    Four failure modes, and the discrimination matters: a check that rejects
    everything is worse than none, so legal programs must pass.
    """
    spec = DIALECTS[dialect]
    ring_set = set(ring_vars)
    seen = set()
    for name, _type, _expr in decls:
        if not spec["identifier"].match(name):
            raise IdentifierCollision(
                "emitted identifier %r is not valid in %s (must match %s).  "
                "An illegal identifier does not stop the run: the CAS reports "
                "an error, keeps going, prints the output markers with nothing "
                "behind them, and exits 0."
                % (name, dialect, spec["identifier"].pattern))
        if name in ring_set:
            raise IdentifierCollision(
                "emitted identifier %r SHADOWS the ring variable %r.  The "
                "declaration would redefine the variable, and any ideal "
                "operation naming it afterwards silently means something else "
                "-- this is the `poly g0 = ...` defect that manufactured false "
                "UNIT verdicts at every prime." % (name, name))
        if name in spec["reserved"]:
            raise IdentifierCollision(
                "emitted identifier %r is a %s reserved word" % (name, dialect))
        if name in seen:
            raise IdentifierCollision("identifier %r declared twice" % name)
        seen.add(name)
    return True


class CASProgram(object):
    """The ONLY thing `run_cas` accepts.  There is no string path to a solver.

    The collision check and the program text are derived from the SAME
    (identifier, definition) pairs, so they cannot drift apart.
    """

    def __init__(self, dialect, ring, ring_vars, decls, body, outputs,
                 characteristic=0):
        if dialect not in DIALECTS:
            raise ValueError("unknown CAS dialect %r" % (dialect,))
        self.dialect = dialect
        self.ring = ring
        self.ring_vars = list(ring_vars)
        self.decls = [(str(n), str(t), str(e)) for n, t, e in decls]
        self.body = list(body)
        self.outputs = list(outputs)
        self.characteristic = characteristic
        assert_no_identifier_collision(dialect, self.ring_vars, self.decls)
        assert_no_identifier_collision(dialect, self.ring_vars,
                                       [(o, "", "") for o in self.outputs])

    @property
    def text(self):
        if self.dialect != SINGULAR:
            raise NotImplementedError(self.dialect)
        lines = ["ring %s = %d,(%s),dp;"
                 % (self.ring, self.characteristic, ",".join(self.ring_vars))]
        for name, typ, expr in self.decls:
            lines.append("%s %s = %s;" % (typ, name, expr))
        lines.extend(self.body)
        for out in self.outputs:
            lines.append('"@@%s:";' % out.upper())
            lines.append("%s;" % out)
        lines.append("quit;")
        return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# The transport declaration
# ---------------------------------------------------------------------------
class Transport(object):
    """How the model this computation produces relates to its source.

    Constructing one is the act the MCP tool signature makes mandatory.  It
    validates eagerly so that a malformed declaration fails before the solver
    runs rather than after, when the cost has already been paid.
    """

    def __init__(self, src, type, why, map_kind=K.IDENTITY_MAP, drops=(),
                 witness="", debt_why="", cite=""):
        if type not in K.DECLARABLE_TYPES:
            raise TransportNotDeclared(
                "transport type %r is not declarable.  Name what this step "
                "LOSES:\n"
                "  nothing (and you can exhibit the converse) -> EQUIVALENCE\n"
                "  equations                                  -> %s\n"
                "  a larger coefficient field                 -> %s\n"
                "  an elimination or a projection             -> %s\n"
                "  a change of characteristic                 -> %s\n"
                "  not yet known                              -> UNTYPED, with "
                "debt_why"
                % (type, K.NECESSARY_CONDITION, K.BASE_EXTENSION,
                   K.IMAGE_CLOSURE, K.SPECIALIZATION))
        if not why:
            raise TransportNotDeclared(
                "transport declaration needs `why`: what does this step lose?")
        if type == K.UNTYPED and not debt_why:
            raise TransportNotDeclared(
                "an UNTYPED edge is a recorded modelling debt and needs "
                "`debt_why`.  Say what is not yet known about this step.")
        if map_kind not in K.MAP_KINDS:
            raise TransportNotDeclared("unknown map_kind %r" % (map_kind,))
        self.src = src
        self.type = type
        self.why = why
        self.map_kind = map_kind
        self.drops = list(drops)
        self.witness = witness
        self.debt_why = debt_why
        self.cite = cite

    @classmethod
    def from_dict(cls, d):
        if d is None:
            raise TransportNotDeclared(
                "no transport declared.  A computation that produces a new "
                "model must say how that model relates to its source; an "
                "untyped step is where the errors live.  Pass "
                "edge={'src': ..., 'type': ..., 'why': ...}.")
        if not isinstance(d, dict):
            raise TransportNotDeclared("edge must be an object, got %r"
                                       % type(d).__name__)
        unknown = set(d) - {"src", "type", "why", "map_kind", "drops",
                            "witness", "debt_why", "cite"}
        if unknown:
            raise TransportNotDeclared("unknown edge fields: %s"
                                       % ", ".join(sorted(unknown)))
        return cls(**d)

    def events(self, eid, dst, dst_desc, dst_field=None, dst_chart=None):
        """The graph events this computation contributes."""
        model = {"ev": S.EV_MODEL, "id": dst, "desc": dst_desc,
                 "cite": self.cite}
        if dst_field:
            model["field"] = dst_field
        if dst_chart:
            model["chart"] = dst_chart
        edge = {"ev": S.EV_EDGE, "id": eid, "src": self.src, "dst": dst,
                "type": self.type, "why": self.why, "map_kind": self.map_kind,
                "cite": self.cite}
        if self.drops:
            edge["drops"] = self.drops
        if self.witness:
            edge["witness"] = self.witness
        if self.debt_why:
            edge["debt_why"] = self.debt_why
        return [model, edge]


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------
ABORT_CODES = {124: "timeout", 137: "SIGKILL", 139: "SIGSEGV"}

# Windows dev boxes reach Singular through WSL; ASSAY.md recorded the same
# arrangement.  Overridable so a Linux/Mac checkout needs no edit.
SINGULAR_ARGV = os.environ.get("GP_SINGULAR_ARGV")


def _argv():
    if SINGULAR_ARGV:
        return SINGULAR_ARGV.split()
    if os.name == "nt":
        return ["wsl.exe", "--", "Singular", "-q"]
    return ["Singular", "-q"]


def _parse_outputs(stdout, outputs):
    """Read exactly one value BLOCK per declared output, or refuse.

    Not a lenient regex, deliberately.  A laxer parser would have read a
    verdict out of a program that never ran.

    THE WHOLE BLOCK, NOT THE FIRST LINE.  Singular prints an ideal one
    generator per line as `NAME[i]=...`.  The first version captured a single
    line, so a two-generator basis was reported as `GP_G[1]=f6` -- which a
    reader can easily take for "the ideal is (f6)".  It is not; it is the first
    element of a basis whose length was never shown.  Silently under-reporting
    the size of a Groebner basis is exactly the kind of quiet mis-description
    between a computation and its consumer that this project exists to refuse,
    and it reached a user before it was caught.

    Returns a list when the block has several lines, a string when it has one,
    so single-value outputs stay ergonomic.
    """
    values = {}
    for out in outputs:
        marker = "@@%s:" % out.upper()
        starts = [m.end() for m in
                  re.finditer(r"^%s[ \t]*$" % re.escape(marker), stdout,
                              re.MULTILINE)]
        if len(starts) != 1:
            raise CASError(
                "expected exactly one value block for output %r, found %d.  A "
                "CAS that errored is not a CAS that answered."
                % (out, len(starts)))
        lines = []
        for line in stdout[starts[0]:].lstrip("\n").splitlines():
            if not line.strip() or line.startswith("@@"):
                break
            lines.append(line.rstrip())
        if not lines:
            raise CASError(
                "output marker %r was printed with nothing behind it.  "
                "Singular reports an error, keeps going, prints the markers "
                "empty, and exits 0 -- so this is a failed run, not an empty "
                "answer." % out)
        values[out] = lines if len(lines) > 1 else lines[0]
    return values


def run_cas(program, *, edge, produces, describes, root=".", timeout=300,
            record=True, dst_field=None, dst_chart=None, cite="",
            edge_id=None, _runner=None):
    """Run a CAS program and record the typed edge it produced.

    `edge` is KEYWORD-ONLY WITH NO DEFAULT.  Omitting it is a TypeError raised
    by Python's own argument binding, before this function body runs and
    therefore before any subprocess exists.  That is the forcing function, and
    it is deliberately not enforced by a check inside the body -- a check can
    be reordered or short-circuited by a later edit; a missing required
    argument cannot.
    """
    if not isinstance(program, CASProgram):
        raise TypeError(
            "run_cas accepts only a CASProgram, not %r.  There is no string "
            "path to a solver: the identifier collision assert runs in the "
            "CASProgram constructor, before the program text exists, and a raw "
            "string would bypass it." % type(program).__name__)
    transport = Transport.from_dict(edge) if isinstance(edge, dict) else edge
    if not isinstance(transport, Transport):
        raise TransportNotDeclared("edge must be a Transport or a dict")

    runner = _runner or _run_subprocess
    result = runner(program, timeout)

    if result["aborted"]:
        result["verdict"] = "ABORTED"
        result["values"] = None
    elif "? error" in result["stdout"] or "? error" in result["stderr"]:
        raise CASError(
            "the CAS reported an error and cannot be read for a verdict.  "
            "Note the exit code was %s: Singular reports an error, keeps "
            "going, prints the output markers with nothing behind them, and "
            "exits 0, so exit status is not evidence.\n%s"
            % (result["returncode"], result["stdout"][-2000:]))
    else:
        result["values"] = _parse_outputs(result["stdout"], program.outputs)
        result["verdict"] = "OK"

    result["transport"] = {"src": transport.src, "type": transport.type,
                           "dst": produces}
    if record:
        eid = edge_id or ("E-%s" % produces)
        events = transport.events(eid, produces, describes,
                                  dst_field=dst_field, dst_chart=dst_chart)
        events[0]["cite"] = events[1]["cite"] = cite or transport.cite
        result["events"] = events
        S.append(events, root=root)
    return result


def _run_subprocess(program, timeout):
    argv = _argv()
    try:
        proc = subprocess.run(argv, input=program.text, capture_output=True,
                              text=True, timeout=timeout)
        rc, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        rc, stdout, stderr = 124, "", "timeout after %ss" % timeout
    except FileNotFoundError as exc:
        raise CASError("cannot reach the CAS via %s: %s" % (argv, exc))
    return {"returncode": rc, "stdout": stdout, "stderr": stderr,
            "aborted": rc in ABORT_CODES,
            "abort_reason": ABORT_CODES.get(rc), "argv": argv}


def ideal_is_unit(ring_vars, generators, characteristic=0, name="GP_I",
                  **kw):
    """Convenience: does the ideal reduce to (1)?

    Returns the raw CAS result.  It deliberately does NOT return a verdict
    object, and the reason is the whole point of the surrounding system: a
    Groebner basis reducing to 1 is EVIDENCE of emptiness, and what makes it a
    KILL is the certificate you attach and the scope that certificate derives.
    Turning `std(I) == 1` straight into "this cell is dead" over an unstated
    field is the shape of the error that shipped.
    """
    prog = CASProgram(
        SINGULAR, ring="GP_R", ring_vars=ring_vars,
        decls=[(name, "ideal", ",".join(generators)),
               ("GP_G", "ideal", "std(%s)" % name)],
        body=[], outputs=["GP_G"], characteristic=characteristic)
    return run_cas(prog, **kw)
