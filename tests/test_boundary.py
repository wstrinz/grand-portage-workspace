"""The CAS boundary and the enforcement hook.

The layers that make this a gate rather than a linter.  Everything above them
can be ignored by not looking; these two cannot.
"""

import json
import os
import shutil
import subprocess

import pytest

from grandportage import cas
from grandportage import check as C
from grandportage import hook as HK
from grandportage import kernel as K
from grandportage import store as S

import helpers as H


GOOD = dict(dialect=cas.SINGULAR, ring="GP_R", ring_vars=["x", "y"],
            decls=[("GP_I", "ideal", "x*y-1,x+y-2")],
            body=[], outputs=["GP_I"])

EDGE = {"src": "SRC", "type": "IMAGE_CLOSURE",
        "why": "elimination returns the Zariski closure of the image",
        "map_kind": "POLYNOMIAL"}


def program(**kw):
    d = dict(GOOD)
    d.update(kw)
    return cas.CASProgram(**d)


def fake_runner(stdout="", stderr="", rc=0):
    def run(prog, timeout):
        return {"returncode": rc, "stdout": stdout, "stderr": stderr,
                "aborted": rc in cas.ABORT_CODES,
                "abort_reason": cas.ABORT_CODES.get(rc), "argv": ["fake"]}
    return run


@pytest.fixture
def project(tmp_path):
    root = str(tmp_path)
    S.append([{"ev": "model", "id": "SRC", "desc": "the source system",
               "field": "Q"}], root=root)
    return root


# ===========================================================================
# Guard 1 -- the forcing function
# ===========================================================================

def test_omitting_the_transport_is_a_TypeError_from_argument_binding():
    """Not a check inside the body -- a missing required keyword-only argument.

    The distinction is the point.  A check can be reordered or short-circuited
    by a later edit; Python's own argument binding cannot, so no code path
    reaches a subprocess without the declaration.
    """
    with pytest.raises(TypeError) as exc:
        cas.run_cas(program(), produces="M", describes="d")
    assert "edge" in str(exc.value)


def test_no_subprocess_is_spawned_when_the_declaration_is_missing():
    """The claim is 'no CAS process spawned', so assert it rather than assume."""
    calls = []

    def spy(prog, timeout):
        calls.append(prog)
        return fake_runner("@@GP_I:\n1\n")(prog, timeout)

    with pytest.raises(TypeError):
        cas.run_cas(program(), produces="M", describes="d", _runner=spy)
    assert calls == []


def test_untyped_is_a_legal_declaration_but_silence_is_not(project):
    """A recorded debt is allowed; an unrecorded one is not."""
    with pytest.raises(cas.TransportNotDeclared):
        cas.Transport.from_dict(None)
    with pytest.raises(cas.TransportNotDeclared):
        cas.Transport.from_dict({"src": "SRC", "type": "UNTYPED",
                                 "why": "exploratory"})
    t = cas.Transport.from_dict({"src": "SRC", "type": "UNTYPED",
                                 "why": "exploratory sweep",
                                 "debt_why": "relation to the germ unknown"})
    assert t.type == K.UNTYPED


def test_an_unknown_type_names_the_five_options():
    """The error message has to teach the distinction, because the person
    hitting it is being asked to make a modelling decision they were trying to
    skip."""
    with pytest.raises(cas.TransportNotDeclared) as exc:
        cas.Transport(src="A", type="PROBABLY_FINE", why="w")
    msg = str(exc.value)
    for t in (K.EQUIVALENCE, K.NECESSARY_CONDITION, K.BASE_EXTENSION,
              K.IMAGE_CLOSURE, K.SPECIALIZATION):
        assert t in msg


def test_a_transport_with_no_why_is_refused():
    with pytest.raises(cas.TransportNotDeclared):
        cas.Transport(src="A", type=K.NECESSARY_CONDITION, why="")


# ===========================================================================
# Guard 2 -- the non-bypassable identifier assert
# ===========================================================================

def test_the_historical_shadowing_defect_is_caught():
    """`poly g0 = ...` against ring variables (a0..a4, g0, g1, gamma).

    The emitted program redefined the ring variable, so `sat(I, nz)` saturated
    the ideal by an element of itself and collapsed it to (1) -- a confident
    false EMPTY in 0.3 s at every prime.
    """
    with pytest.raises(cas.IdentifierCollision) as exc:
        program(ring_vars=["a0", "a1", "a2", "a3", "a4", "g0", "g1", "gamma"],
                decls=[("g0", "poly", "7447*a4^5*gamma^23")], outputs=["g0"])
    assert "SHADOWS" in str(exc.value)


def test_the_illegal_identifier_defect_is_caught():
    """Singular identifiers must begin with a letter.  An `_ASSAY_` prefix
    produced `? error`, markers printed with no values, and EXIT 0."""
    with pytest.raises(cas.IdentifierCollision):
        program(decls=[("_GP_I", "ideal", "x*y-1")], outputs=["_GP_I"])


def test_reserved_words_and_duplicates_are_caught():
    with pytest.raises(cas.IdentifierCollision):
        program(decls=[("ideal", "ideal", "x")], outputs=["ideal"])
    with pytest.raises(cas.IdentifierCollision):
        program(decls=[("GP_I", "ideal", "x"), ("GP_I", "ideal", "y")])


def test_the_assert_DISCRIMINATES_rather_than_refusing_everything():
    """A check that rejects everything is worse than none.  A legal program
    with a variable deliberately named `g0` -- the exact name the historical
    defect shadowed -- must pass, because the collision is about the
    DECLARATION shadowing it, not about the name."""
    p = program(ring_vars=["x", "y", "g0"],
                decls=[("GP_I", "ideal", "x*y-1,g0-x")], outputs=["GP_I"])
    assert "g0" in p.text


def test_there_is_no_string_path_to_a_solver():
    with pytest.raises(TypeError) as exc:
        cas.run_cas("ideal I = 1;", edge=EDGE, produces="M", describes="d")
    assert "CASProgram" in str(exc.value)


def test_the_check_and_the_text_derive_from_the_same_pairs():
    """They cannot drift apart, because they read the same triples."""
    p = program()
    names = [n for n, _, _ in p.decls]
    for n in names:
        assert ("ideal %s =" % n) in p.text


# ===========================================================================
# Guard 3 -- an errored CAS is not a CAS that answered
# ===========================================================================

def test_an_error_line_refuses_a_verdict_even_at_exit_zero(project):
    """The recorded symptom exactly: `? error`, markers with nothing behind
    them, exit 0.  Exit status is not evidence."""
    out = "? error occurred in or before STDIN line 2: `ring ...`\n@@GP_I:\n\n"
    with pytest.raises(cas.CASError) as exc:
        cas.run_cas(program(), edge=EDGE, produces="M", describes="d",
                    root=project, _runner=fake_runner(out, rc=0))
    assert "exits 0" in str(exc.value)


def test_a_missing_or_doubled_marker_refuses_a_verdict(project):
    for out in ("no markers at all\n",
                "@@GP_I:\n1\n@@GP_I:\n2\n"):
        with pytest.raises(cas.CASError):
            cas.run_cas(program(), edge=EDGE, produces="M", describes="d",
                        root=project, _runner=fake_runner(out))


@pytest.mark.parametrize("rc", sorted(cas.ABORT_CODES))
def test_abort_codes_are_never_a_verdict(project, rc):
    r = cas.run_cas(program(), edge=EDGE, produces="M", describes="d",
                    root=project, _runner=fake_runner("@@GP_I:\n1\n", rc=rc))
    assert r["verdict"] == "ABORTED" and r["values"] is None


# ===========================================================================
# Recording
# ===========================================================================

def test_a_successful_run_records_a_typed_edge(project):
    r = cas.run_cas(program(), edge=EDGE, produces="ELIM",
                    describes="the eliminated ideal", root=project,
                    _runner=fake_runner("@@GP_I:\n1\n"))
    assert r["values"] == {"GP_I": "1"}
    g = S.load(S.graph_path(project))
    assert "ELIM" in g.models
    assert g.edges["E-ELIM"]["type"] == K.IMAGE_CLOSURE
    assert g.edges["E-ELIM"]["src"] == "SRC"


def test_recording_a_step_whose_source_does_not_exist_is_refused(project):
    """The write is transactional against the fold, so a bad edge cannot land."""
    bad = dict(EDGE, src="NO_SUCH_MODEL")
    with pytest.raises(S.GraphError):
        cas.run_cas(program(), edge=bad, produces="ELIM", describes="d",
                    root=project, _runner=fake_runner("@@GP_I:\n1\n"))
    assert "NO_SUCH_MODEL" not in open(S.graph_path(project),
                                       encoding="utf-8").read()


def test_ideal_is_unit_returns_evidence_not_a_verdict(project):
    """The convenience wrapper deliberately does NOT turn std(I)==1 into a kill.

    A Groebner basis reducing to 1 is EVIDENCE of emptiness; what makes it a
    kill is the certificate attached and the scope that certificate derives.
    Collapsing those is the shape of the error that shipped.
    """
    r = cas.ideal_is_unit(["x", "y"], ["x", "x-1"], edge=EDGE, produces="E",
                          describes="d", root=project,
                          _runner=fake_runner("@@GP_G:\nGP_G[1]=1\n"))
    assert "verdict" not in str(r["values"]).lower()
    assert r["verdict"] == "OK"          # the RUN succeeded
    assert "EMPTY" not in json.dumps(r["values"])


# ===========================================================================
# The hook
# ===========================================================================

def _conclude(root, from_claim, edge_id, direction, asserted):
    S.append([{"ev": "inference", "id": "I-CONCLUDE", "claim": from_claim,
               "path": [[edge_id, direction]], "asserted": asserted,
               "era": "live"}], root=root)


def test_the_full_loop_compute_record_conclude_refuse(project):
    """The shape of the error that shipped, replayed through the whole stack.

    An emptiness is established over a small field with a field-relative
    certificate; the agent then reads it across a base extension as if it were
    geometric.  Nothing in the graph is malformed and the CAS ran clean -- the
    step is simply not licensed, and the hook is what stops it.
    """
    S.append([
        {"ev": "model", "id": "RES_L", "desc": "the residue equation over L",
         "field": "Q(sqrt 17)"},
        {"ev": "model", "id": "RES_K", "desc": "the same over arbitrary char-0 K",
         "field": "K"},
        {"ev": "edge", "id": "E-EXT", "src": "RES_L", "dst": "RES_K",
         "type": K.BASE_EXTENSION,
         "why": "the coefficient field changes from Q(sqrt 17) to arbitrary K",
         "drops": ["every field-relative arithmetic fact, in particular "
                   "square classes"]},
        {"ev": "claim", "id": "CL-KILL", "model": "RES_L", "kind": K.EMPTY,
         "statement": "no solution with all leading coefficients nonzero",
         "scope": "Q(sqrt 17)", "certificate": "NONSQUARE_CLASS",
         "ladder": "exact-checked"},
    ], root=project)

    block, _ = HK.evaluate(project)
    assert not block, "nothing has been concluded yet"

    _conclude(project, "CL-KILL", "E-EXT", K.ALONG,
              "the branch does not exist over the theorem's arbitrary char-0 K")

    block, message = HK.evaluate(project)
    assert block
    assert "REFUSED" in message
    assert "does not base-change" in message
    assert "DISCHARGE" in message


def test_the_same_step_is_ALLOWED_with_a_base_changing_certificate(project):
    """The contrast, and it is what makes the refusal a discrimination rather
    than a blanket ban on ever crossing a base extension."""
    S.append([
        {"ev": "model", "id": "RES_L", "desc": "over L", "field": "Q"},
        {"ev": "model", "id": "RES_K", "desc": "over K", "field": "K"},
        {"ev": "edge", "id": "E-EXT", "src": "RES_L", "dst": "RES_K",
         "type": K.BASE_EXTENSION, "why": "the coefficient field changes"},
        {"ev": "claim", "id": "CL-KILL", "model": "RES_L", "kind": K.EMPTY,
         "statement": "1 lies in the ideal, exhibited over Q",
         "certificate": "UNIT_IDEAL_CERT", "ladder": "exact-checked"},
    ], root=project)
    _conclude(project, "CL-KILL", "E-EXT", K.ALONG,
              "hence empty over every char-0 K")
    block, message = HK.evaluate(project)
    assert not block, message


def test_a_missing_graph_does_not_block(tmp_path):
    """Most tool calls in most repos have nothing to do with a proof campaign.
    A hook that blocks every session without a .portage/ gets disabled, and a
    disabled hook enforces nothing."""
    block, _ = HK.evaluate(str(tmp_path))
    assert not block


def test_a_malformed_graph_DOES_block(project):
    """Fail closed on the things we own.  The agent just caused this."""
    with open(S.graph_path(project), "a", encoding="utf-8") as fh:
        fh.write('{"ev":"claim","id":"X","model":"GHOST","kind":"EMPTY",'
                 '"statement":"x","certificate":"UNIT_IDEAL_CERT"}\n')
    block, message = HK.evaluate(project)
    assert block and "does not fold" in message


def test_the_baseline_suppresses_known_findings_but_not_new_ones(project):
    """A campaign mid-flight carries unrepaired historical inferences by
    construction.  Blocking on those forever trains the operator to disable the
    hook, so the baseline records what is knowingly carried -- in a file a
    reviewer can read, not in someone's memory of the normal warnings."""
    findings = C.run(H.load("jc2"))
    shutil.copy(H.graph_file("jc2"), S.graph_path(project))
    block, _ = HK.evaluate(project)
    assert block, "the four historical errors are present"

    HK.save_baseline(project, findings, note="the recorded errata")
    block, _ = HK.evaluate(project)
    assert not block, "accepted findings no longer block"

    S.append([{"ev": "inference", "id": "I-NEW", "claim": "CL-C20",
               "path": [["E9", K.ALONG]], "asserted": "a fresh bad step",
               "era": "live"}], root=project)
    block, message = HK.evaluate(project)
    assert block and "I-NEW" in message


def test_the_hook_reads_cwd_from_its_stdin_payload(project, monkeypatch):
    payload = json.dumps({"tool_name": "Bash", "cwd": project})
    monkeypatch.setattr("sys.stdin", _Stdin(payload))
    assert HK.main([]) == 0


class _Stdin(object):
    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text


# ===========================================================================
# Live CAS -- skipped where Singular is unreachable
# ===========================================================================

def _singular_available():
    try:
        p = subprocess.run(cas._argv() + ["--version"], capture_output=True,
                           timeout=30)
        return p.returncode == 0 or b"Singular" in (p.stdout + p.stderr)
    except Exception:
        return False


live = pytest.mark.skipif(not _singular_available(),
                          reason="Singular not reachable")


@live
def test_live_singular_both_directions(project):
    """Two targets with known answers, on the real solver.

    Reviewing the emitter would never have caught the identifier defect; only
    running it did.  So the emitter gets run.
    """
    empty = cas.ideal_is_unit(["x", "y", "g0"], ["x", "x-1", "y-g0"],
                              edge=EDGE, produces="ELIM1", describes="d",
                              root=project)
    assert empty["values"]["GP_G"].endswith("=1")

    nonempty = cas.ideal_is_unit(["x", "y", "g0"], ["x*y-1", "x+y-2", "g0-x"],
                                 edge=dict(EDGE, why="a second target"),
                                 produces="ELIM2", describes="d", root=project)
    assert not nonempty["values"]["GP_G"].endswith("=1")


@live
def test_live_run_emits_a_program_using_the_defects_own_variable_name(project):
    """The target deliberately names a variable `g0`, the exact name the
    historical defect shadowed, and the emitted program must be clean."""
    r = cas.ideal_is_unit(["x", "g0"], ["x*g0-1"], edge=EDGE, produces="E",
                          describes="d", root=project)
    assert r["verdict"] == "OK"


def test_the_first_run_hint_appears_only_when_no_baseline_exists(project):
    """The operational trap, caught as a test.

    On a graph with existing history and no baseline, EVERY tool call blocks.
    That is correct behaviour and a terrible first experience: it looks like a
    broken install, and the rational response to a broken install is to delete
    the hook.  So the first block has to name the one-command fix.
    """
    shutil.copy(H.graph_file("gamma_window"), S.graph_path(project))
    block, message = HK.evaluate(project)
    assert block and "--- FIRST RUN?" in message
    assert "gp accept" in message

    HK.save_baseline(project, C.run(S.load(S.graph_path(project))),
                     note="knowingly carried")
    block, _ = HK.evaluate(project)
    assert not block


def test_a_baseline_that_exists_suppresses_the_hint(project):
    """Once a baseline exists, a NEW finding must read as a new finding -- not
    as a setup problem the operator already solved."""
    shutil.copy(H.graph_file("gamma_window"), S.graph_path(project))
    HK.save_baseline(project, C.run(S.load(S.graph_path(project))), note="x")
    S.append([{"ev": "inference", "id": "I-FRESH", "claim": "GC-A2-KILL",
               "path": [["GE4", K.ALONG]],
               "asserted": "and therefore (75,125) is dead too",
               "era": "live"}], root=project)
    block, message = HK.evaluate(project)
    assert block and "I-FRESH" in message
    assert "--- FIRST RUN?" not in message


def test_gp_accept_records_a_reviewable_decision(project):
    """The baseline is a file a reviewer reads, not a memory of which warnings
    are the normal ones -- so the reason travels with it."""
    from grandportage import cli
    shutil.copy(H.graph_file("gamma_window"), S.graph_path(project))
    assert cli.main(["--root", project, "accept", "-m", "the standing four"]) == 0
    with open(HK.baseline_path(project), encoding="utf-8") as fh:
        payload = json.load(fh)
    assert payload["note"] == "the standing four"
    assert "TRANSPORT:GI-BRIDGE" in payload["accepted"]


def test_gp_accept_can_take_one_finding_at_a_time(project):
    """Accepting everything is the blunt instrument.  Accepting one finding is
    the honest one, and it keeps the rest blocking."""
    from grandportage import cli
    shutil.copy(H.graph_file("gamma_window"), S.graph_path(project))
    cli.main(["--root", project, "accept", "-m", "just the bridge",
              "--only", "TRANSPORT:GI-BRIDGE"])
    block, message = HK.evaluate(project)
    assert block
    assert "GI-BRIDGE" not in message
    assert "GI-GAMMA-IMPORT" in message
