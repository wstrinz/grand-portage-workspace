"""THE GATE.

The generic checker, reading each domain's DAG as DATA, must reproduce the
verdicts the hardcoded prototypes produced with that domain's DAG compiled into
the checker itself.  Both answer keys were pinned before Grand Portage existed:
one against three errors that actually shipped, one against externally
published matroid theory.

A framework that flags a sound step is a false-positive generator and unusable,
so the clean sets are asserted exactly, not merely as supersets.
"""

import pytest

from grandportage import check as C

import helpers as H


@pytest.mark.parametrize("domain", H.DOMAINS)
def test_findings_are_exactly_the_pinned_set(domain):
    """No missing flags AND no extra ones.  The second half is the load-bearing
    one: the prototype earned its credibility on zero false positives."""
    got = set(H.findings_by_id(H.load(domain)))
    want = set(H.expected(domain)["findings"])
    assert got == want, ("missing: %s\nextra: %s"
                         % (sorted(want - got), sorted(got - want)))


@pytest.mark.parametrize("domain", H.DOMAINS)
def test_severities_match(domain):
    found = H.findings_by_id(H.load(domain))
    for fid, want in H.expected(domain)["findings"].items():
        assert found[fid].severity == want["severity"], fid


@pytest.mark.parametrize("domain", H.DOMAINS)
def test_derived_severities_match(domain):
    """The sharper assertion.  The prototypes ASSIGNED severity by hand and
    said so; Grand Portage DERIVES it from contradictions present in the graph.
    Agreement here is evidence the derivation is real and not a relabelling."""
    found = H.findings_by_id(H.load(domain))
    for fid, want in H.expected(domain)["findings"].items():
        assert found[fid].derived_severity == want["derived_severity"], fid


def test_only_one_severity_is_overridden_in_total():
    """Judgement that is not a fact about the graph must be visible AS
    judgement, and there must be very little of it.  Ten findings across two
    domains; exactly one carries a declared override, with a reason."""
    overridden = [(d, f.fid) for d in H.DOMAINS
                  for f in H.findings_by_id(H.load(d)).values() if f.overridden]
    assert overridden == [("jc2", "TRANSPORT:INF-A10-SURV")]
    f = H.findings_by_id(H.load("jc2"))["TRANSPORT:INF-A10-SURV"]
    assert f.derived_severity == C.UNSOUND_PREMISE
    assert f.severity == C.TRIAGE
    assert f.severity_why


@pytest.mark.parametrize("domain", H.DOMAINS)
def test_clean_inferences_are_exactly_the_positive_controls(domain):
    g = H.load(domain)
    got = C.clean_inferences(g, C.run(g))
    assert sorted(got) == sorted(H.expected(domain)["clean_inferences"])


def test_the_contrast_pairs_differ_only_in_the_certificate():
    """The discriminating test in BOTH domains, asserted structurally.

    Two emptiness claims, same edge type, same direction, same claim kind, both
    computed over a small field -- opposite verdicts, because one certificate
    base-changes and the other does not.  A rule tuned to fire on "computed
    over Q" would flag both, and this is what proves it is not.
    """
    pairs = [
        ("jc2", "INF-C08-HIST", "INF-POSSLICE"),
        ("matroid", "IM-ML8-BASE-EXT", "IM-FANO-CONTRAST"),
    ]
    for domain, refused, licensed in pairs:
        g = H.load(domain)
        flagged = H.flagged(g)
        assert refused in flagged and licensed not in flagged, domain
        cr = g.claims[g.inferences[refused]["claim"]]
        cl = g.claims[g.inferences[licensed]["claim"]]
        assert cr["kind"] == cl["kind"] == "EMPTY"
        assert cr["certificate"] != cl["certificate"]
        assert g.certificates[cr["certificate"]] is False
        assert g.certificates[cl["certificate"]] is True


def test_the_reversed_asymmetry_is_exercised_in_both_directions():
    """On the SAME edge type, EMPTY is refused ALONG and NONEMPTY passes.
    Both halves, on one matroid, against published ground truth."""
    flagged = H.flagged(H.load("matroid"))
    assert "IM-ML8-Q-BASE-EXT" in flagged     # EMPTY along a BASE_EXTENSION
    assert "IM-ML8-ASCEND" not in flagged     # NONEMPTY along the same type


def test_place_coverage_fires_at_exactly_t():
    """Error 2.  Must fire at t and at NEITHER y NOR inf, both of which have
    declared components -- otherwise it is a blanket refusal, not a detection."""
    g = H.load("jc2")
    gaps = C.coverage_gaps(g, g.models["WINDOW"])
    assert gaps == {"place": ["t"]}


def test_taint_is_separate_from_transport():
    """A licensed conclusion drawn in an illegitimately-constructed model is
    still unsound.  INF-SLICEPHI-KILL's own transport IS licensed; it appears
    in the clean set and separately under TAINT."""
    g = H.load("jc2")
    findings = C.run(g)
    assert "INF-SLICEPHI-KILL" in C.clean_inferences(g, findings)
    taints = [f for f in findings if f.rule == C.R_TAINT]
    assert [f.subject for f in taints] == ["SLICEPHI"]
    assert "CL-ATLE9-PHI" in taints[0].detail


def test_refinement_edges_all_reuse_one_existing_type():
    """Monotonicity is not a fourth type: 'a closed branch can never reopen
    under refinement' is a theorem about NECESSARY_CONDITION read AGAINST."""
    g = H.load("jc2")
    refinements = [e for e in g.edges.values() if e["refinement"]]
    assert len(refinements) == 3
    assert all(e["type"] == "NECESSARY_CONDITION" for e in refinements)
    assert not [f for f in C.run(g) if f.rule == C.R_REFINEMENT]


@pytest.mark.parametrize("domain", H.DOMAINS)
def test_every_finding_carries_a_discharge_move(domain):
    """A flag with no next move is telemetry.  The whole point of typing the
    failure is that the type names the repair."""
    for f in C.run(H.load(domain)):
        assert f.discharge and len(f.discharge) > 40, f.fid


@pytest.mark.parametrize("domain", H.DOMAINS)
def test_exit_code_is_nonzero_while_the_historical_errors_stand(domain):
    assert C.exit_code(C.run(H.load(domain))) == 1


def test_the_repaired_inference_is_not_flagged():
    """If this were flagged the framework could not tell a defect from its fix,
    which would make it useless for exactly the moment it is needed."""
    assert "INF-C08-CURRENT" not in H.flagged(H.load("jc2"))
