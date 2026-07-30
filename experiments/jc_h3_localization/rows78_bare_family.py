#!/usr/bin/env python3
"""Replay the two rows 7--8 bare-family unit-ideal certificates."""

from __future__ import annotations

import copy
import json

from grandportage import groebner as G
from grandportage import localization as L


def family_spec(chart):
    if chart == "q":
        # Row 8, y^-43: -5*q^3*t^2.  Since q and t are units, its
        # vanishing puts 1 in the localized ideal.
        guards = ["q", "t"]
        generator = "-5*q^3*t^2"
        powers = [3, 2]
        target = "q^3*t^2"
        cofactor = "-1/5"
        receipt = "row 8 coefficient y^-43"
    elif chart == "p":
        # Row 7, y^-38: 5*p^4*t^2.
        guards = ["p", "t"]
        generator = "5*p^4*t^2"
        powers = [4, 2]
        target = "p^4*t^2"
        cofactor = "1/5"
        receipt = "row 7 coefficient y^-38"
    else:
        raise ValueError("chart must be q or p")
    return receipt, {
        "schema": L.SCHEMA,
        "characteristic": 0,
        "ring_vars": ["p", "q", "t"],
        "generators": [generator],
        "guards": guards,
        "expression": {
            "numerator": "1",
            "denominator_powers": [0, 0],
        },
        "certificate": {
            "localization_powers": powers,
            "membership_target": target,
            "cofactors": [cofactor],
        },
    }


def replay(chart):
    receipt, spec = family_spec(chart)
    report = L.verify(spec)
    return {
        "chart": chart,
        "source_receipt": receipt,
        "verdict": report["verdict"],
        "checked_target": report["checked"]["target"],
        "spec_fingerprint": report["spec_fingerprint"],
        "runtime_authority": report["licenses"],
        "certified_coordinate_statement":
            "1 = 0 in the declared localized quotient",
        "lean_bridge": "localized_unit_ideal_has_no_point",
        "point_emptiness_is_not_graph_bound": True,
        "source_membership_authority": False,
        "h3_authority": False,
    }


def mutation_controls():
    _receipt, base = family_spec("q")
    mutations = []
    cases = []

    changed = copy.deepcopy(base)
    changed["certificate"]["localization_powers"] = [2, 2]
    cases.append(("wrong localization power", changed))

    changed = copy.deepcopy(base)
    changed["certificate"]["cofactors"] = ["1/5"]
    cases.append(("wrong cofactor sign", changed))

    changed = copy.deepcopy(base)
    changed["guards"] = ["p", "t"]
    cases.append(("cross-chart guards", changed))

    changed = copy.deepcopy(base)
    changed["generators"] = ["-5*q^2*t^2"]
    cases.append(("changed source receipt", changed))

    for label, spec in cases:
        try:
            L.verify(spec)
        except (L.LocalizationError, G.CertificateError):
            mutations.append(label)
    if len(mutations) != len(cases):
        raise AssertionError("a rows 7--8 mutation survived: %r" % mutations)
    return mutations


def main():
    print(json.dumps({
        "schema": "jc_h3_rows78_bare_family_replay_v1",
        "reports": [replay("q"), replay("p")],
        "refused_mutations": mutation_controls(),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
