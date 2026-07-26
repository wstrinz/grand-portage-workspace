"""MCP server: the CAS, wrapped so that every call emits a typed edge.

Zero dependencies -- JSON-RPC 2.0 over stdio, written out rather than pulled in.
That is a deliberate choice and not stubbornness: the MCP specification is
moving toward statelessness at the transport layer, and a transport GRAPH is
stateful.  Owning the ~150 lines that speak the protocol means the state can
live where it belongs -- `.portage/graph.jsonl` -- instead of in a session that
the protocol may stop guaranteeing.  Nothing in this server holds state between
calls; restart it mid-campaign and the next call folds the same graph.

THE FORCING FUNCTION.  `edge` is `required` in the JSON Schema of every tool
that produces a model, AND the handler validates it, AND `run_cas` takes it as
a keyword-only argument with no default.  Three layers saying the same thing,
because each protects against a different failure: the schema tells the model
what to send, the handler catches a malformed send, and the signature makes it
impossible for a future refactor to introduce a path that skips both.

Register in `.mcp.json`:

    {"mcpServers": {"grand-portage": {
        "command": "python", "args": ["-m", "grandportage.mcp"]}}}
"""

import json
import os
import sys
import traceback

from . import cas
from . import check as C
from . import kernel as K
from . import store as S

PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_PROTOCOLS = ("2024-11-05", "2025-03-26", "2025-06-18")

ROOT = os.environ.get("GP_ROOT", ".")


# ---------------------------------------------------------------------------
# The transport declaration, as a schema fragment.
#
# The description text matters more than usual here.  This is the one place a
# model is asked to make a modelling judgement, and the enum alone does not
# tell it how to choose.  So the description is a decision procedure, phrased
# as "what does this step LOSE?" rather than "what kind of step is this?" --
# the second question invites a guess, the first has an answer the caller knows.
# ---------------------------------------------------------------------------
EDGE_SCHEMA = {
    "type": "object",
    "description": (
        "REQUIRED. How the model this computation produces relates to the one "
        "it came from. There is no default and no inference: a step whose "
        "relaxation type is not named is exactly where unsound conclusions "
        "come from."),
    "properties": {
        "src": {"type": "string",
                "description": "id of the model this computation starts from"},
        "type": {
            "type": "string",
            "enum": list(K.DECLARABLE_TYPES),
            "description": (
                "Ask what the step LOSES.\n"
                "  EQUIVALENCE - nothing, and you can exhibit the converse. "
                "Do not use this because a step 'should be' reversible.\n"
                "  NECESSARY_CONDITION - equations. The target is a strict "
                "relaxation: every point of the source is a point of the "
                "target, not conversely.\n"
                "  BASE_EXTENSION - the coefficient field grows. Note the "
                "reversed asymmetry: witnesses travel along the arrow freely, "
                "emptiness only with a certificate that base-changes.\n"
                "  IMAGE_CLOSURE - an elimination or a projection. What you "
                "get back is the Zariski CLOSURE of the image, and a point of "
                "the closure need not lift.\n"
                "  SPECIALIZATION - the characteristic changes. Carries no "
                "existence statement in either direction.\n"
                "  UNTYPED - not yet known. Legal, but requires debt_why, and "
                "no conclusion will cross this edge until it is typed.")},
        "why": {"type": "string",
                "description": "REQUIRED. What information does this step lose?"},
        "map_kind": {"type": "string", "enum": list(K.MAP_KINDS),
                     "description": (
                         "POLYNOMIAL / IDENTITY_MAP if the coordinate change "
                         "is denominator-free, RATIONAL otherwise. This single "
                         "attribute decides whether a dictionary may be "
                         "rewritten across the edge.")},
        "drops": {"type": "array", "items": {"type": "string"},
                  "description": "the specific conditions this step discards"},
        "witness": {"type": "string",
                    "description": (
                        "explicit evidence that the step is NOT an equivalence "
                        "-- e.g. a point of the target that is not in the "
                        "source")},
        "debt_why": {"type": "string",
                     "description": "required when type is UNTYPED"},
        "cite": {"type": "string"},
    },
    "required": ["src", "type", "why"],
}


def _tool(name, description, properties, required):
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": properties,
                            "required": required}}


TOOLS = [
    _tool(
        "cas_ideal_is_unit",
        "Run a Groebner basis computation to see whether an ideal reduces to "
        "(1), and record the typed edge to the model it produces. Returns "
        "EVIDENCE, not a verdict: std(I)==1 becomes a kill only once you "
        "attach a certificate kind and the scope that certificate derives. "
        "Requires `edge` -- no CAS process is spawned without it.",
        {"ring_vars": {"type": "array", "items": {"type": "string"},
                       "description": "ring variables, in order"},
         "generators": {"type": "array", "items": {"type": "string"},
                        "description": "ideal generators as CAS expressions"},
         "characteristic": {"type": "integer", "default": 0,
                            "description": (
                                "0 for char 0. A nonzero value is "
                                "RECONNAISSANCE: a mod-p result may direct "
                                "effort and may never close a case, and the "
                                "step to char 0 is a SPECIALIZATION edge that "
                                "carries nothing.")},
         "produces": {"type": "string",
                      "description": "id for the model this run produces"},
         "describes": {"type": "string",
                       "description": "one line: what that model IS"},
         "edge": EDGE_SCHEMA},
        ["ring_vars", "generators", "produces", "describes", "edge"]),

    _tool(
        "portage_declare",
        "Append events to the graph without running a CAS: models, claims, "
        "inferences, certificate kinds, provenance. This is how a conclusion "
        "gets recorded, and recording it is what submits it to the checker. "
        "The write is transactional against the fold -- if the events do not "
        "produce a well-formed graph, nothing is written.",
        {"events": {"type": "array", "items": {"type": "object"},
                    "description": (
                        "graph events. Each needs `ev`: one of certificate, "
                        "model, edge, claim, inference, built_by, note. An "
                        "EMPTY claim must carry a `certificate` kind, and its "
                        "scope is DERIVED from that certificate rather than "
                        "from what you declare.")}},
        ["events"]),

    _tool(
        "portage_check",
        "Type-check the accumulated graph. Returns findings with their "
        "discharge moves, and the list of inferences that came back clean.",
        {"floor": {"type": "string", "enum": list(C.SEVERITY_ORDER),
                   "description": "lowest severity to report as failing"}},
        []),

    _tool(
        "portage_show",
        "Print the current graph: models, edges, claims, inferences. Read this "
        "before adding to a campaign you did not start -- the graph is the "
        "state, so it is the handoff.",
        {}, []),

    _tool(
        "portage_transport_table",
        "The transport table and the certificate registry, printed from the "
        "kernel. Read this when deciding an edge type or a certificate kind.",
        {}, []),
]


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------
def _text(s):
    return {"content": [{"type": "text", "text": s}]}


def _err(s):
    return {"content": [{"type": "text", "text": s}], "isError": True}


def h_cas_ideal_is_unit(args, root):
    edge = args.get("edge")
    if edge is None:
        # Belt and braces: the schema says required, but a client that ignores
        # its own schema must not reach the solver either.
        return _err(str(cas.TransportNotDeclared(
            "no transport declared. A computation that produces a new model "
            "must say how that model relates to its source. Pass edge with "
            "src, type and why; see portage_transport_table for the types.")))
    result = cas.ideal_is_unit(
        args["ring_vars"], args["generators"],
        characteristic=args.get("characteristic", 0),
        edge=edge, produces=args["produces"], describes=args["describes"],
        root=root, dst_field=args.get("field"), cite=args.get("cite", ""))
    lines = ["run: %s" % result["verdict"],
             "recorded: model %s, edge %s (%s from %s)"
             % (args["produces"], "E-" + args["produces"],
                edge.get("type"), edge.get("src"))]
    if result["values"]:
        for k, v in sorted(result["values"].items()):
            lines.append("%s = %s" % (k, v))
        if result["values"].get("GP_G", "").replace(" ", "").endswith("=1"):
            lines.append("")
            lines.append(
                "The ideal reduced to (1). That is EVIDENCE of emptiness and "
                "not yet a kill: record it as an EMPTY claim with a "
                "`certificate` kind, and the scope will be derived. If the "
                "certificate is field-relative the emptiness will NOT "
                "base-change, and reading it as geometric is the exact error "
                "this system exists to refuse.")
    if result["verdict"] == "ABORTED":
        lines.append("An unfinished run is not evidence of anything.")
    return _text("\n".join(lines))


def h_portage_declare(args, root):
    events = args.get("events") or []
    if not isinstance(events, list):
        return _err("`events` must be a list of graph events")
    S.append(events, root=root)
    kinds = {}
    for e in events:
        kinds[e.get("ev")] = kinds.get(e.get("ev"), 0) + 1
    summary = ", ".join("%d %s" % (v, k) for k, v in sorted(kinds.items()))
    findings = C.run(S.load(S.graph_path(root)))
    return _text("recorded %s\n\n%s" % (summary, _render(findings)))


def h_portage_check(args, root):
    path = S.graph_path(root)
    if not os.path.exists(path):
        return _text("no graph yet at %s" % path)
    graph = S.load(path)
    findings = C.run(graph)
    clean = C.clean_inferences(graph, findings)
    return _text("%s\nclean inferences (%d): %s"
                 % (_render(findings), len(clean), ", ".join(clean) or "-"))


def _render(findings):
    if not findings:
        return "no findings: every recorded conclusion is licensed by the "\
               "transport it rests on."
    out = []
    for f in findings:
        out.append("%s  %s" % (f.severity, f.fid))
        out.extend("    " + l for l in f.detail.splitlines())
        out.append("    -> DISCHARGE: %s" % f.discharge)
        out.append("")
    return "\n".join(out)


def h_portage_show(args, root):
    path = S.graph_path(root)
    if not os.path.exists(path):
        return _text("no graph yet at %s" % path)
    g = S.load(path)
    out = []
    for mid in sorted(g.models):
        m = g.models[mid]
        tag = " ".join(x for x in (m.get("chart"), m.get("field")) if x)
        out.append("MODEL %-16s %-14s %s" % (mid, tag, m.get("desc", "")[:70]))
    for eid in sorted(g.edges):
        e = g.edges[eid]
        out.append("EDGE  %-16s %s -> %s  %s"
                   % (eid, e["src"], e["dst"], e["type"]))
    for cid in sorted(g.claims):
        c = g.claims[cid]
        out.append("CLAIM %-16s %-9s @%-14s scope=%s cert=%s"
                   % (cid, c["kind"], c["model"], c.get("scope"),
                      c.get("certificate")))
    for iid in g.inference_order:
        i = g.inferences[iid]
        out.append("INFER %-16s %s via %s -> %s"
                   % (iid, i["claim"],
                      " ".join("%s/%s" % s for s in i["path"]) or "(no path)",
                      i["concludes_at"]))
    return _text("\n".join(out) or "(empty graph)")


def h_portage_transport_table(args, root):
    rows = ["%-20s %-8s %s" % ("edge type", "dir",
                               " ".join("%-16s" % k for k in K.CLAIM_KINDS))]
    for t in K.DECLARABLE_TYPES:
        for d in K.DIRECTIONS:
            cells = []
            for k in K.CLAIM_KINDS:
                v = K.TRANSPORT[t][d][k]
                cells.append("%-16s" % ("yes" if v is True else
                                        "NO" if v is False else v))
            rows.append("%-20s %-8s %s" % (t, d, " ".join(cells)))
    rows.append("")
    rows.append("Certificate kinds. An EMPTY claim's SCOPE is derived from "
                "this, not from what you declare:")
    for c, bc in sorted(K.BUILTIN_CERTIFICATES.items()):
        rows.append("  %-28s %s" % (c, "base-changes (scope SCHEME)" if bc
                                    else "FIELD-RELATIVE -- name the field"))
    return _text("\n".join(rows))


HANDLERS = {
    "cas_ideal_is_unit": h_cas_ideal_is_unit,
    "portage_declare": h_portage_declare,
    "portage_check": h_portage_check,
    "portage_show": h_portage_show,
    "portage_transport_table": h_portage_transport_table,
}


# ---------------------------------------------------------------------------
# JSON-RPC 2.0
# ---------------------------------------------------------------------------
def dispatch(request, root=ROOT):
    """Return a response dict, or None for a notification."""
    method = request.get("method")
    rid = request.get("id")
    params = request.get("params") or {}

    if method == "initialize":
        asked = params.get("protocolVersion")
        version = asked if asked in SUPPORTED_PROTOCOLS else PROTOCOL_VERSION
        return _ok(rid, {
            "protocolVersion": version,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "grand-portage", "version": "0.1.0"},
            "instructions": (
                "Every computation that produces a model must declare how that "
                "model relates to its source. Call portage_transport_table if "
                "you are unsure which type applies. Record conclusions with "
                "portage_declare so they are checked; an unrecorded conclusion "
                "is an unchecked one."),
        })
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return _ok(rid, {})
    if method == "tools/list":
        return _ok(rid, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            return _fail(rid, -32602, "unknown tool %r" % (name,))
        try:
            return _ok(rid, handler(params.get("arguments") or {}, root))
        except (cas.TransportNotDeclared, cas.IdentifierCollision,
                cas.CASError, S.GraphError, K.ScopeError) as exc:
            # Expected refusals.  These are the product, not a crash: the
            # message tells the caller what to do differently.
            return _ok(rid, _err("%s: %s" % (type(exc).__name__, exc)))
        except Exception:
            return _ok(rid, _err("unhandled error:\n%s"
                                 % traceback.format_exc()))
    if rid is None:
        return None
    return _fail(rid, -32601, "method not found: %r" % (method,))


def _ok(rid, result):
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _fail(rid, code, message):
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": code, "message": message}}


def serve(stdin=None, stdout=None, root=None):
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    root = root or ROOT
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except ValueError:
            stdout.write(json.dumps(_fail(None, -32700, "parse error")) + "\n")
            stdout.flush()
            continue
        response = dispatch(request, root=root)
        if response is not None:
            stdout.write(json.dumps(response) + "\n")
            stdout.flush()


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    root = ROOT
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    serve(root=root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
