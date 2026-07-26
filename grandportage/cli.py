"""`gp` -- the command line.

Deterministic, read-only by default, exits nonzero when the graph licenses a
conclusion it should not.  No model in the loop: everything here is a fold and
a table lookup.
"""

import argparse
import json
import os
import sys

from . import check as C
from . import kernel as K
from . import store as S
from .discharge import KNOWN_CONSERVATISM


def _graphs(args):
    if args.graph:
        return list(args.graph)
    default = S.graph_path(args.root)
    if not os.path.exists(default):
        sys.stderr.write(
            "no graph at %s.  Pass --graph, or start one with `gp init`.\n"
            % default)
        raise SystemExit(2)
    return [default]


def _load(args):
    try:
        return S.load(*_graphs(args))
    except S.GraphError as exc:
        sys.stderr.write("GRAPH ERROR\n  %s\n" % exc)
        raise SystemExit(2)
    except K.ScopeError as exc:
        sys.stderr.write("SCOPE ERROR\n  %s\n" % exc)
        raise SystemExit(2)


def cmd_check(args):
    g = _load(args)
    findings = C.run(g)
    if args.json:
        print(json.dumps({
            "findings": [f.as_dict() for f in findings],
            "clean": C.clean_inferences(g, findings),
            "counts": {"models": len(g.models), "edges": len(g.edges),
                       "claims": len(g.claims),
                       "inferences": len(g.inference_order)},
        }, indent=2))
        return C.exit_code(findings, args.floor)

    if not args.quiet:
        print("graph: %d models, %d edges, %d claims, %d inferences"
              % (len(g.models), len(g.edges), len(g.claims),
                 len(g.inference_order)))
        print()
    for f in findings:
        if args.quiet:
            print("%-18s %-20s %s" % (f.severity, f.rule, f.subject))
            continue
        print("%s  %s" % (f.severity, f.fid))
        for line in f.detail.splitlines():
            print("    " + line)
        if f.overridden:
            print("    severity OVERRIDDEN from %s -- %s"
                  % (f.derived_severity, f.severity_why))
        for eid, direction, ok, reason in f.trace:
            print("    %-6s %-7s %-3s %s"
                  % (eid, direction, "ok" if ok else "NO", reason))
        print("    -> DISCHARGE: %s" % f.discharge)
        print()

    if not args.quiet:
        clean = C.clean_inferences(g, findings)
        print("clean inferences (%d): %s" % (len(clean), ", ".join(clean)))
        print()
        n = sum(1 for f in findings
                if C.SEVERITY_RANK[f.severity] >= C.SEVERITY_RANK[args.floor])
        print("%d finding(s) at or above %s" % (n, args.floor))
    return C.exit_code(findings, args.floor)


def cmd_table(args):
    """Print the transport table from the kernel itself, so a document quoting
    it and the code applying it cannot drift apart."""
    width = max(len(t) for t in K.DECLARABLE_TYPES)
    hdr = "| %-*s | %-7s | %s |" % (width, "edge type", "dir",
                                    " | ".join("%-9s" % k
                                               for k in K.CLAIM_KINDS))
    print(hdr)
    print("|" + "-" * (len(hdr) - 2) + "|")
    for t in K.DECLARABLE_TYPES:
        for d in K.DIRECTIONS:
            cells = []
            for k in K.CLAIM_KINDS:
                v = K.TRANSPORT[t][d][k]
                cells.append("%-9s" % ("yes" if v is True else
                                       "NO" if v is False else v))
            print("| %-*s | %-7s | %s |" % (width, t, d, " | ".join(cells)))
    print()
    print("Conditional cells resolve against edge/claim attributes:")
    print("  scheme_scope     EMPTY base-changes only if its certificate does")
    print("  map_polynomial   IDENTITY rewriting needs a denominator-free map")
    print("  closed_condition only Zariski-closed predicates reach a closure")
    print()
    print("Certificates that base-change (an emptiness proved this way is")
    print("field-independent):")
    for c, bc in sorted(K.BUILTIN_CERTIFICATES.items()):
        print("  %-28s %s" % (c, "yes" if bc else "NO -- field-relative"))
    print()
    print("Known conservatism -- cells refused more strictly than the")
    print("mathematics requires, kept deliberately:")
    for kc in KNOWN_CONSERVATISM:
        print("  %s/%s/%s: %s" % (kc["cell"] + (kc["truth"],)))
    return 0


def cmd_show(args):
    g = _load(args)
    for mid in sorted(g.models):
        m = g.models[mid]
        bits = [b for b in (m.get("chart"), m.get("field")) if b]
        print("MODEL %-14s %s" % (mid, " ".join(bits)))
        print("    %s" % m.get("desc", ""))
    print()
    for eid in sorted(g.edges):
        e = g.edges[eid]
        print("EDGE  %-6s %-14s -> %-14s %s" % (eid, e["src"], e["dst"],
                                                e["type"]))
    print()
    for cid in sorted(g.claims):
        c = g.claims[cid]
        print("CLAIM %-20s %-9s @%-14s scope=%s"
              % (cid, c["kind"], c["model"], c.get("scope")))
    return 0


def cmd_accept(args):
    """Record the findings this campaign is knowingly carrying.

    Accepting a finding is a decision with a cost, so it lands in a file a
    reviewer can read -- and one that belongs in version control -- rather than
    in someone's memory of which warnings are the normal ones.
    """
    from . import hook as H
    g = _load(args)
    findings = C.run(g)
    if args.only:
        findings = [f for f in findings if f.fid in set(args.only)]
    payload = H.save_baseline(args.root, findings, note=args.message)
    print("accepted %d finding(s) into %s"
          % (len(payload["accepted"]), H.baseline_path(args.root)))
    for fid in payload["accepted"]:
        print("  " + fid)
    if not args.message:
        print("\n(no -m given.  A baseline without a reason is a list of "
              "warnings someone decided to stop reading.)")
    return 0


def cmd_init(args):
    path = S.graph_path(args.root)
    if os.path.exists(path):
        sys.stderr.write("%s already exists\n" % path)
        return 1
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# Grand Portage graph.  Append-only; merge by concatenation.\n")
    print("initialised %s" % path)
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="gp", description=__doc__)
    p.add_argument("--root", default=".", help="project root (default: .)")
    p.add_argument("--graph", action="append",
                   help="graph log to read; repeat to MERGE several")
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("check", help="type-check the graph")
    c.add_argument("--json", action="store_true")
    c.add_argument("--quiet", action="store_true")
    c.add_argument("--floor", default=C.UNSOUND_PREMISE,
                   choices=C.SEVERITY_ORDER,
                   help="lowest severity that fails the run")
    c.set_defaults(func=cmd_check)

    t = sub.add_parser("table", help="print the transport table")
    t.set_defaults(func=cmd_table)

    s = sub.add_parser("show", help="print the graph")
    s.set_defaults(func=cmd_show)

    a = sub.add_parser("accept",
                       help="record findings this campaign knowingly carries")
    a.add_argument("-m", "--message", default="",
                   help="why these are being carried")
    a.add_argument("--only", action="append",
                   help="accept only this finding id; repeat for several")
    a.set_defaults(func=cmd_accept)

    i = sub.add_parser("init", help="create an empty graph")
    i.set_defaults(func=cmd_init)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not getattr(args, "func", None):
        build_parser().print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
