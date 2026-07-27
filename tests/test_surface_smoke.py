"""GATE 2 -- every construct, driven through every surface a user touches.

THREE CRASHES IN ONE DAY, all the same shape:

    construct            built for                              how it failed
    ------------------   ------------------------------------   -------------
    open premise slot    "the artifact requires a claim that     gp check
                          does not exist"                        crashed
    partition            "this case analysis leaves one case     gp check
                          open"                                  crashed
    family               "4 of 1567 classes are 2-to-1"          gp check
                                                                 crashed

Each was built for the hardest thing a campaign has to say.  Each was CORRECT
IN ITSELF -- the kernel cell was right, the fold was right, the rule was right.
Each broke on the path a user takes, and each was found by a live run rather
than by a suite that was over 300 checks at the time.

THE REASON IS SPECIFIC AND THIS FILE IS THE REPAIR.  Nothing exercised a
construct END TO END.  `test_cell_ledger` tests the kernel.  `test_adversarial`
tests functions -- its open-slot regression called `audit_inference` and never
`run`, so the construct was correct in every respect except being reachable.
`contradicting_claims` subscripted `c["model"]` on a claim that had a `family`
instead.  `_first_refusal` looked up a sentinel in `graph.edges`.

So: one fixture per construct, every surface driven over every fixture, and a
completeness gate that fails when an event kind has no fixture.  A new
construct cannot be added without being walked through the whole surface, and a
new surface cannot be added without being walked over every construct.

The assertion is deliberately weak -- DOES IT COMPLETE.  Not what it says; the
other files own that.  All three crashes would have been caught by "does it
return at all", and that is the whole point: the bar was never height, it was
existence.
"""

import io
import json
import os
import sys

import pytest

from grandportage import check as C
from grandportage import cli
from grandportage import hook as HK
from grandportage import kernel as K
from grandportage import mcp
from grandportage import store as S


# ===========================================================================
# ONE FIXTURE PER CONSTRUCT.  Each is a COMPLETE graph, not a fragment: it
# carries whatever else the surfaces need to actually do work on it.  A family
# fixture with no inference would never have reached `contradicting_claims`,
# which is exactly how that crash survived.
# ===========================================================================
_MODELS = [
    {"ev": "model", "id": "TIGHT", "desc": "with equations"},
    {"ev": "model", "id": "LOOSE", "desc": "equations dropped"},
]
_NC = {"ev": "edge", "id": "E", "src": "TIGHT", "dst": "LOOSE",
       "type": K.NECESSARY_CONDITION, "why": "drops equations"}


def _claim(cid, model="TIGHT", kind=K.PREDICATE, **kw):
    c = {"ev": "claim", "id": cid, "model": model, "kind": kind,
         "statement": "a statement for %s" % cid}
    c.update(kw)
    return c


def _inf(iid, claim, path, kind=K.PREDICATE, **kw):
    i = {"ev": "inference", "id": iid, "claim": claim, "path": path,
         "concludes_kind": kind, "asserted": "an assertion for %s" % iid}
    i.update(kw)
    return i


FIXTURES = {}


def construct(name, event_kinds):
    """Register a fixture and the event kinds it is the coverage for."""
    def deco(fn):
        FIXTURES[name] = (fn(), set(event_kinds))
        return fn
    return deco


@construct("plain_transport", ["model", "edge", "claim", "inference"])
def _plain():
    return _MODELS + [_NC, _claim("C"),
                      _inf("I", "C", [["E", K.ALONG]])]


@construct("open_premise_slot", [])
def _slot():
    """The construct that crashed `_first_refusal` on its sentinel."""
    return _MODELS + [_NC, _claim("HAVE", model="LOOSE"),
                      {"ev": "inference", "id": "I", "premises": [
                          {"claim": "HAVE", "path": [["E", K.AGAINST]]},
                          {"required_kind": K.EMPTY, "at": "LOOSE",
                           "missing_why": "nothing kills every case"}],
                       "concludes_kind": K.PREDICATE,
                       "asserted": "the artifact establishes X"}]


@construct("open_slot_leading", [])
def _slot_first():
    """Slot FIRST, so the fold leaves the legacy `claim` field None -- which
    broke two further lines that used it as a dict key."""
    return _MODELS + [_NC, _claim("HAVE", model="LOOSE"),
                      {"ev": "inference", "id": "I", "premises": [
                          {"required_kind": K.EMPTY, "at": "LOOSE",
                           "missing_why": "unsettled"},
                          {"claim": "HAVE", "path": [["E", K.AGAINST]]}],
                       "concludes_kind": K.PREDICATE,
                       "asserted": "the artifact establishes X"}]


@construct("partition_covered", ["partition"])
def _part_ok():
    return [{"ev": "model", "id": "P", "desc": "parent"},
            {"ev": "model", "id": "B1", "desc": "branch one"},
            {"ev": "model", "id": "B2", "desc": "branch two"},
            {"ev": "edge", "id": "EB1", "src": "B1", "dst": "P",
             "type": K.NECESSARY_CONDITION, "why": "a branch"},
            {"ev": "edge", "id": "EB2", "src": "B2", "dst": "P",
             "type": K.NECESSARY_CONDITION, "why": "a branch"},
            _claim("X", model="B1", kind=K.EMPTY,
                   certificate="UNIT_IDEAL_CERT"),
            _claim("Y", model="B2", kind=K.EMPTY,
                   certificate="UNIT_IDEAL_CERT"),
            _claim("EXH", model="P"),
            {"ev": "partition", "id": "PG", "parent": "P",
             "branches": ["B1", "B2"], "exhaustive": "EXH",
             "why": "the split is by gamma"},
            {"ev": "inference", "id": "IP", "via_partition": "PG",
             "premises": [{"claim": "X", "path": []},
                          {"claim": "Y", "path": []},
                          {"claim": "EXH", "path": []}],
             "concludes_kind": K.EMPTY, "asserted": "the parent is empty"}]


@construct("partition_uncovered", [])
def _part_bad():
    """The case the mechanism EXISTS for, and the one that crashed: a split
    that does not cover its parent."""
    evs = [e for e in _part_ok() if e.get("id") != "Y"]
    for e in evs:
        if e.get("id") == "IP":
            e["premises"] = [p for p in e["premises"]
                             if p.get("claim") != "Y"]
    return evs


@construct("partition_with_open_slot", [])
def _part_slot():
    """Both at once -- `graph.claims[pr["claim"]]` with claim=None."""
    evs = _part_bad()
    for e in evs:
        if e.get("id") == "IP":
            e["premises"] = e["premises"] + [
                {"required_kind": K.EMPTY, "at": "B2",
                 "missing_why": "the second branch is not settled"}]
    return evs


@construct("family_and_dispositions", ["family"])
def _family():
    """A family claim has no `model`, and five rules subscripted it. The
    inference is not decoration: without one, `contradicting_claims` never runs
    and the crash stays hidden."""
    return _MODELS + [_NC, _claim("C", model="LOOSE", kind=K.EMPTY,
                                  certificate="UNIT_IDEAL_CERT"),
                      _inf("I", "C", [["E", K.AGAINST]], kind=K.EMPTY),
                      {"ev": "family", "id": "F", "count": 4,
                       "desc": "the four cases",
                       "members": ["m1", "m2", "m3", "m4"],
                       "enumeration": "CF-ENUM"},
                      {"ev": "claim", "id": "CF-ENUM", "family": "F",
                       "kind": K.PREDICATE,
                       "statement": "there are exactly four",
                       "established_by": "RAN", "ladder": "exact-checked"},
                      {"ev": "claim", "id": "D", "family": "F", "kind": K.COUNT,
                       "statement": "three of four are settled",
                       "splits": "F",
                       "groups": [{"id": "G-OK", "settles": 3,
                                   "verdict": "settled",
                                   "exhibited": ["m1", "m2", "m3"]},
                                  {"id": "G-NO", "settles": 1,
                                   "verdict": "open", "exhibited": ["m4"]}],
                       "method": "a cheap screen",
                       "proves": ["G-OK"],
                       "why": "the screen proves the kill and not the survival",
                       "established_by": "RAN", "ladder": "exact-checked"}]


@construct("family_crosscut", [])
def _crosscut():
    evs = _family()
    return evs + [
        {"ev": "claim", "id": "D2", "family": "F", "kind": K.COUNT,
         "statement": "a second decomposition", "splits": "F",
         "groups": [{"id": "H-A", "settles": 2, "verdict": "type A",
                     "exhibited": ["m1", "m4"]},
                    {"id": "H-B", "settles": 2, "verdict": "type B",
                     "exhibited": ["m2", "m3"]}],
         "method": "an invariant", "proves": ["H-A", "H-B"],
         "why": "computed, not inferred",
         "established_by": "RAN", "ladder": "exact-checked"},
        {"ev": "claim", "id": "X", "family": "F", "kind": K.COUNT,
         "statement": "the result buys two", "rests_on": "H-A",
         "counts_against": "G-OK", "asserts_count": 2,
         "established_by": "RAN", "ladder": "exact-checked"}]


@construct("supersession_all_three", [])
def _supersede():
    return _MODELS + [
        {"ev": "edge", "id": "E1", "src": "TIGHT", "dst": "LOOSE",
         "type": K.UNTYPED, "why": "?", "debt_why": "not worked out"},
        {"ev": "edge", "id": "E2", "src": "TIGHT", "dst": "LOOSE",
         "type": K.NECESSARY_CONDITION, "why": "drops equations",
         "supersedes": "E1", "discharge_kind": "RETYPE"},
        _claim("C", model="LOOSE"),
        {"ev": "claim", "id": "C2", "model": "LOOSE",
         "kind": K.PREDICATE, "statement": "a statement for C",
         "cite": "a better citation", "supersedes": "C",
         "discharge_kind": K.AMEND},
        _inf("I1", "C2", [["E2", K.AGAINST]]),
        _inf("I2", "C2", [["E2", K.AGAINST]], supersedes="I1",
             discharge_kind=K.RESTATE),
    ]


@construct("certificates_and_scope", ["certificate"])
def _certs():
    return _MODELS + [
        {"ev": "certificate", "id": "MY_CERT", "base_changes": False,
         "why": "field-relative by construction"},
        {"ev": "edge", "id": "EB", "src": "TIGHT", "dst": "LOOSE",
         "type": K.BASE_EXTENSION, "why": "the coefficient field grows"},
        _claim("C", kind=K.EMPTY, certificate="MY_CERT",
               scope="Q(sqrt 17)"),
        _inf("I", "C", [["EB", K.ALONG]], kind=K.EMPTY)]


@construct("aliases_and_provenance", ["same_as", "built_by", "note"])
def _misc():
    return _MODELS + [_NC, _claim("C"),
                      _inf("I", "C", [["E", K.ALONG]]),
                      {"ev": "same_as", "id": "A", "models": ["TIGHT", "LOOSE"],
                       "why": "two names for one object, recorded to be checked"},
                      {"ev": "built_by", "model": "LOOSE", "inference": "I"},
                      {"ev": "note", "text": "carried and never typed"}]


@construct("every_edge_type", [])
def _all_types():
    evs = list(_MODELS)
    for i, t in enumerate(K.ALL_TYPES):
        e = {"ev": "edge", "id": "E%d" % i, "src": "TIGHT", "dst": "LOOSE",
             "type": t, "why": "a step of type %s" % t}
        if t == K.EQUIVALENCE:
            e["converse_witness"] = "the inverse construction"
            e["ring_iso"] = True
        if t == K.RESTRICTION:
            e["zariski_dense"] = True
        evs.append(e)
    evs.append(_claim("C"))
    evs.append(_inf("I", "C", [["E0", K.ALONG]]))
    return evs


# ===========================================================================
# EVERY SURFACE A USER TOUCHES.  Each takes (root, graph) and must COMPLETE.
# ===========================================================================
def _s_fold(root, g):
    S.load(S.graph_path(root))


def _s_check(root, g):
    C.run(g)


def _s_render(root, g):
    C.render(C.run(g), {}, full=False)
    C.render(C.run(g), {}, full=True)


def _s_clean(root, g):
    C.clean_inferences(g, C.run(g))


def _s_cli_check(root, g):
    cli.main(["--root", root, "check"])


def _s_cli_check_json(root, g):
    cli.main(["--root", root, "check", "--json"])


def _s_cli_check_quiet(root, g):
    cli.main(["--root", root, "check", "--quiet"])


def _s_cli_show(root, g):
    cli.main(["--root", root, "show"])


def _s_cli_history(root, g):
    cli.main(["--root", root, "history"])


def _s_cli_accept(root, g):
    cli.main(["--root", root, "accept", "-m", "smoke"])


def _s_cli_migrate(root, g):
    cli.main(["--root", root, "migrate", "--dry-run"])


def _s_hook(root, g):
    HK.evaluate(root)


def _s_mcp_check(root, g):
    mcp.h_portage_check({"full": True}, root)


def _s_mcp_show(root, g):
    mcp.h_portage_show({}, root)


def _s_fingerprints(root, g):
    for f in C.run(g):
        f.fingerprint
        f.as_dict()
        repr(f)


SURFACES = {
    "fold": _s_fold,
    "check.run": _s_check,
    "check.render": _s_render,
    "check.clean_inferences": _s_clean,
    "finding.fingerprint": _s_fingerprints,
    "gp check": _s_cli_check,
    "gp check --json": _s_cli_check_json,
    "gp check --quiet": _s_cli_check_quiet,
    "gp show": _s_cli_show,
    "gp history": _s_cli_history,
    "gp accept": _s_cli_accept,
    "gp migrate --dry-run": _s_cli_migrate,
    "hook.evaluate": _s_hook,
    "mcp portage_check": _s_mcp_check,
    "mcp portage_show": _s_mcp_show,
}


def _write(root, events):
    p = S.graph_path(root)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8") as fh:
        for e in events:
            fh.write(json.dumps(e) + "\n")
    return S.load(p)


@pytest.mark.parametrize("surface", sorted(SURFACES))
@pytest.mark.parametrize("fixture", sorted(FIXTURES))
def test_every_construct_survives_every_surface(fixture, surface, tmp_path,
                                                capsys):
    """DOES IT COMPLETE.  Deliberately not what it says.

    All three of this week's crashes would have been caught by exactly this
    question, which is the point: the bar was never height, it was existence.
    A checker that raises is indistinguishable from a checker nobody ran, and
    it takes the hook and `gp accept` down with it -- so a campaign that hits
    one cannot even record what it knowingly carries.
    """
    events, _kinds = FIXTURES[fixture]
    root = str(tmp_path)
    graph = _write(root, events)
    SURFACES[surface](root, graph)
    capsys.readouterr()


def test_every_event_kind_has_a_fixture():
    """The gate on the gate, same discipline as the cell ledger's.

    A new event kind cannot be added without being walked through every
    surface. `family` was added yesterday, was exercised by the kernel and by
    its own rules, and crashed on first contact with a real graph because no
    fixture drove it through the CLI.
    """
    covered = set()
    for _events, kinds in FIXTURES.values():
        covered |= kinds
    missing = sorted(set(S.EVENT_KINDS) - covered)
    assert not missing, (
        "these event kinds have no smoke fixture, so nothing walks them "
        "through the user-facing surfaces: %s" % ", ".join(missing))


def test_the_surface_list_covers_what_a_campaign_actually_calls():
    """A surface absent from this list is a surface no construct is driven
    through. The three crashes were all in `gp check`; `gp accept` shares its
    path and went down with it, which is why the affected campaign could not
    record its own deliberate findings."""
    for required in ("gp check", "gp accept", "hook.evaluate",
                     "mcp portage_check", "gp show"):
        assert required in SURFACES
