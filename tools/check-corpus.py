
"""Validate neutral cases, check pinned source pointers, and record actual legacy observations."""
import argparse, hashlib, json, os, subprocess, sys, traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "oracle/checkout"
PIN = json.loads((ROOT/"oracle/PIN.json").read_text(encoding="utf-8-sig"))["commit"]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path[:0] = [str(ORACLE), str(ORACLE/"tests")]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(["git","-C",str(ORACLE),*args],text=True).strip()

def validate():
    if git("rev-parse","HEAD") != PIN:
        raise ValueError("Wrong oracle revision")
    if git("status","--porcelain","--untracked-files=no"):
        raise ValueError("Pinned oracle tracked content is dirty")
    schema = json.loads((ROOT/"corpus/case.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    routes = json.loads((ROOT/"oracle/ROUTES.json").read_text(encoding="utf-8"))
    if routes["commit"] != PIN:
        raise ValueError("Oracle routes are for a different commit")
    cases, ids = [], set()
    for path in sorted((ROOT/"corpus/must").glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        validator.validate(case)
        if path.stem != case["id"] or case["id"] in ids:
            raise ValueError("Duplicate or mismatched case identifier")
        ids.add(case["id"])
        for source in case["sources"]:
            base = ORACLE if source["repository"] == "gp-v037" else ROOT
            if source["repository"] == "gp-v037" and source.get("commit") != PIN:
                raise ValueError("Unpinned source")
            source_path = (base/source["path"]).resolve()
            if not source_path.is_relative_to(base.resolve()):
                raise ValueError("Source path escapes its repository")
            lines = source_path.read_text(encoding="utf-8-sig").splitlines()
            if source["anchor"] not in lines[source["line"]-1]:
                raise ValueError("Stale source anchor: "+str(source))
        cases.append((case,path))
    if set(routes["routes"]) != ids:
        raise ValueError("Case and oracle-route identifiers differ")
    return cases, routes["routes"]

def decision(ok, reason, **extra):
    return {"observed_verdict":"ACCEPT" if ok else "REFUSE", "reason":str(reason), **extra}

def never_run(*args, **kwargs):
    raise RuntimeError("Corpus boundary probe unexpectedly attempted a CAS execution")

def probe(case, route):
    from grandportage import kernel as K, store as S, cas, ordered_sos as SOS, field as E, groebner as G
    kind = route["kind"]
    if kind == "pending":
        return {"observed_verdict":None,"status":"PENDING","reason":route["reason"]}
    if kind == "advice_audit":
        text = (ORACLE/route["path"]).read_text(encoding="utf-8")
        return {"observed_verdict":None,"status":"DIAGNOSTIC_OBSERVED",
                "needles_found":{needle:needle in text for needle in route["needles"]},
                "reason":"Diagnostic wording reproduced from pinned source; no false held claim asserted."}
    if kind in ("transport","partition"):
        control = {}
        if route.get("control") == "target_membership":
            d = case["inputs"]
            control["target_membership"] = G.check_membership_identity(
                d["identity_difference"],d["target_ideal"],d["target_cofactors"],d["variables"],0)
        if route.get("control") == "unit_mod_three":
            G.check_membership_identity("1",case["inputs"]["generators"],case["inputs"]["cofactors"],["x"],0)
            control["rational_identity_replayed"] = True
            control["mod_three_identity"] = G.check_membership_identity("1",case["inputs"]["generators"],case["inputs"]["cofactors"],["x"],3)
        if route.get("control") == "witness_mod_three":
            from fractions import Fraction
            control["rational_substitution"] = 2*Fraction("1/2")-1 == 0
            control["mod_three_substitution"] = (2*2-1)%3 == 0
            if not all(control.values()):
                raise ValueError("Invalid specialization positive control")
        result = (K.transport if kind == "transport" else K.transport_over_partition)(**route["arguments"])
        return decision(result.licensed,result.reason,rule=result.rule,independent_control=control)
    if kind == "sos":
        data = case["inputs"]
        model = {"id":"M","compute_in":"Q","coefficient_domain":"Q","characteristic":0,
                 "ring_vars":data["variables"],"generators":data.get("model_generators",data.get("generators"))}
        certificate = {"method":SOS.METHOD,"ring_vars":data["variables"],
                       "generators":data.get("certificate_generators",data.get("generators")),
                       "squares":data["squares"],"cofactors":data["cofactors"]}
        try:
            receipt = SOS.verify(model,certificate)
        except SOS.OrderedSOSError as exc:
            return decision(False,exc,receipt_checked=False)
        result = E.instantiate({"kind":"ORDERED"},route["target"])
        return decision(result.allowed,result.reason,receipt_checked=True,receipt=receipt)
    if kind == "identifier":
        data = case["inputs"]
        declaration = data["declaration"]
        try:
            program = cas.CASProgram(dialect=cas.SINGULAR,ring="GP_R",ring_vars=data["variables"],
                       decls=[(declaration["name"],"poly" if route["shadow"] else "ideal",declaration["expression"])],
                       body=[],outputs=[declaration["name"]])
        except cas.IdentifierCollision as exc:
            return decision(False,exc,executed=False)
        return decision(True,"Identifier validation accepted; program was not executed.",executed=False)
    if kind == "division":
        try:
            cas.classify_identity(case["inputs"]["variables"],case["inputs"]["lhs"],
                                  case["inputs"]["rhs"],_runner=never_run)
        except cas.CASError as exc:
            return decision(False,exc,executed=False)
        raise RuntimeError("Unsupported division unexpectedly passed")
    if kind == "exact_ambient":
        d = case["inputs"]
        receipt = G.check_membership_identity("("+d["lhs"]+")-("+d["rhs"]+")",[],[],d["variables"],0)
        return decision(True,"Exact polynomial equality replayed with scalar denominators.",receipt=receipt)
    if kind == "kind_composition":
        try:
            K.check_conclusion_kind(K.NONEMPTY,[K.PREDICATE])
        except K.KindCompositionError as exc:
            return decision(False,exc)
        return decision(True,"Legacy pure transport accepted changed quantifier kind")
    if kind == "unknown_certificate":
        try:
            K.derive_scope(K.EMPTY,case["inputs"]["certificate_name"],case["inputs"]["target_context"])
        except K.ScopeError as exc:
            return decision(False,exc)
        return decision(True,"Legacy scope derivation accepted")
    if kind == "redeclaration":
        graph = S.Graph()
        records = case["inputs"].get("declarations")
        if records is None:
            records = [{"id":"A","description":case["inputs"]["description"]}]*2
        try:
            for r in records:
                graph.apply({"ev":"model","id":r["id"],"desc":r["description"]})
            graph.validate()
        except S.GraphError as exc:
            return decision(False,exc)
        return decision(True,"Fold retained one object.",model_count=len(graph.models))
    if kind == "disconnected":
        data = case["inputs"]
        graph = S.Graph()
        events = [{"ev":"model","id":mid,"desc":mid} for mid in ("A","B","C")]
        events += [{"ev":"edge","id":"E","src":data["map_source"],"dst":data["map_target"],
                    "type":K.NECESSARY_CONDITION,"why":"drops equations"},
                   {"ev":"claim","id":"CL","model":data["claim_object"],"kind":K.NONEMPTY,
                    "witness_kind":K.EXHIBITED,"statement":"a point"},
                   {"ev":"inference","id":"I","claim":"CL","path":[["E","ALONG"]],"asserted":"point of B"}]
        try:
            for e in events:
                graph.apply(e)
            graph.validate()
        except S.GraphError as exc:
            return decision(False,exc)
        return decision(True,"The disconnected graph folded")
    if kind == "stale_input":
        # Pinned oracle test helpers fabricate a backend descriptor: this is a
        # binding probe, never evidence that the declared backend actually ran.
        from test_verdict_provenance import _identity_graph, _verdict
        original = _identity_graph(case["inputs"]["old_ideal"][0])
        event = _verdict(original)
        changed = _identity_graph(case["inputs"]["new_ideal"][0])
        changed.apply(event)
        raw = changed.verdicts[event["id"]]
        return decision(bool(raw["current"]),raw.get("stale_reason","current"),
                        receipt_current=raw["current"],
                        claim_has_active_identity="identity_verdict" in changed.claims["C"])
    if kind == "expressibility":
        from test_adversarial import _hyperbola
        from grandportage import check as C
        findings = [f for f in C.run(_hyperbola({"eliminated":["y"]})) if f.rule == C.R_INEXPRESSIBLE]
        refused = any(f.severity == C.UNSOUND_CONCLUSION for f in findings)
        return decision(not refused,"; ".join(f.detail for f in findings),
                        findings=[{"rule":f.rule,"severity":f.severity} for f in findings])

    if kind == "join_fixture":
        from grandportage import check as C
        graph = S.load(str(ORACLE/"fixtures/gamma_window/graph.jsonl"))
        findings = [f for f in C.run(graph) if f.subject == "GI-BRIDGE"]
        refused = any(f.rule == C.R_TRANSPORT for f in findings)
        return decision(not refused,"; ".join(f.detail for f in findings),
                        findings=[{"rule":f.rule,"severity":f.severity} for f in findings])
    if kind == "unverified_attempt":
        from test_verdict_provenance import _identity_graph, _verdict
        graph = _identity_graph()
        event = _verdict(graph,verdict="UNVERIFIED")
        graph.apply(event)
        verdicts = [r.evidence.verdict for r in graph.authority_receipts.values()]
        supported = any(v.startswith("VERIFIED") for v in verdicts)
        return decision(supported,"UNVERIFIED remains visible but provides no positive verification.",
                        projected_verdict=graph.claims["C"].get("identity_verdict"),
                        receipt_wrapper_verdicts=verdicts)
    if kind == "laurent_zero":
        from test_laurent_lowering import _rows78_spec
        from grandportage import laurent_lowering as LL
        spec = _rows78_spec()
        spec["equalities"][0]["right"] = "ZERO"
        try:
            report = LL.verify(spec)
        except LL.LaurentLoweringError as exc:
            return decision(False,exc)
        return decision(True,"Laurent checker accepted",report=report)


    if kind == "alias_binding":
        from grandportage import format as F
        from test_verdict_provenance import _verdict
        def graph_for(mid):
            graph = S.Graph()
            graph.apply(F.meta_event())
            for name in case["inputs"]["identifiers"]:
                graph.apply({"ev":"model","id":name,"what":"same displayed equations",
                             "characteristic":0,"ring_vars":["x"],"generators":["x"]})
            graph.apply({"ev":"claim","id":"C","model":mid,"kind":K.IDENTITY,
                         "statement":"x vanishes","lhs":"x","rhs":"0",
                         "ring_vars":["x"],"identity_origin":K.DERIVED})
            return graph
        a,b = case["inputs"]["identifiers"]
        original = graph_for(a)
        event = _verdict(original)
        original.apply(event)
        changed = graph_for(b)
        changed.apply(event)
        raw = changed.verdicts[event["id"]]
        return decision(bool(raw["current"]),raw.get("stale_reason","current"),
                        original_current=original.verdicts[event["id"]]["current"],
                        destination_has_active_identity="identity_verdict" in changed.claims["C"])
    if kind == "point_universe":
        from grandportage import format as F
        d = case["inputs"]
        graph = S.Graph()
        graph.apply(F.meta_event())
        try:
            for mid,key in (("A","source_universe"),("B","target_universe")):
                model = {"ev":"model","id":mid,"what":"same equations",
                         "characteristic":0,"ring_vars":d["variables"],"generators":d["generators"]}
                if d[key] is not None:
                    model.update(coefficient_domain=d["coefficient_domain"],point_universe=d[key])
                graph.apply(model)
            graph.apply({"ev":"edge","id":"E","src":"A","dst":"B",
                         "type":K.EQUIVALENCE,"map_kind":K.IDENTITY_MAP,
                         "forward":{"x":"x"},"inverse":{"x":"x"},"ring_iso":True,
                         "why":"identity on the coordinate ring"})
            graph.validate()
        except S.GraphError as exc:
            return decision(False,exc)
        return decision(True,"Relation declaration folded.")
    if kind == "empty_anchor":
        from grandportage import format as F, check as C
        from test_empty_scope_anchor import _certificate, _claim
        d = case["inputs"]
        graph = S.Graph()
        graph.apply(F.meta_event())
        model = {"ev":"model","id":"M","desc":"combinatorial objects"}
        if d["coefficient_domain"]:
            model.update(characteristic=0,coefficient_domain=d["coefficient_domain"])
        for event in (model,_certificate(False),_claim(d["claimed_field"])):
            graph.apply(event)
        findings = [f for f in C.run(graph) if f.rule == C.R_EMPTY_SCOPE]
        return decision(not any(f.severity == C.UNSOUND_PREMISE for f in findings),
                        "; ".join(f.detail for f in findings),
                        findings=[{"rule":f.rule,"severity":f.severity} for f in findings])
    if kind == "membership":
        d = case["inputs"]
        try:
            receipt = G.check_membership_identity(d["target"],d["generators"],d["cofactors"],
                                                   d["variables"],d["characteristic"])
        except G.CertificateError as exc:
            return decision(False,exc)
        return decision(True,"Exact membership identity replayed.",receipt=receipt)
    if kind == "localization":
        from grandportage import localization as L
        d = case["inputs"]
        spec = {"schema":L.SCHEMA,"characteristic":0,"ring_vars":d["variables"],
                "generators":d["generators"],"guards":d["guards"],
                "expression":{"numerator":d["numerator"],"denominator_powers":d["denominator_powers"]},
                "certificate":{key:d[key] for key in ("localization_powers","membership_target","cofactors")}}
        try:
            receipt = L.verify(spec)
        except L.LocalizationError as exc:
            return decision(False,exc)
        return decision(receipt["verdict"] == L.VERIFIED,"Localization checker replayed.",receipt=receipt)
    if kind == "ring_iso":
        from grandportage import verify as V, format as F
        d = case["inputs"]
        graph = S.Graph()
        graph.apply(F.meta_event())
        for mid in ("A","B"):
            graph.apply({"ev":"model","id":mid,"what":mid,"characteristic":0,
                         "ring_vars":d["variables"],"generators":d["generators"]})
        graph.apply({"ev":"edge","id":"E","src":"A","dst":"B","type":K.EQUIVALENCE,
                     "map_kind":K.POLYNOMIAL,"why":"displayed maps","ring_iso":True,
                     "forward":d["forward"],"inverse":d["inverse"],
                     "ring_iso_certificate":{"schema":"mapped_ring_iso_v1",
                         "forward_cofactors":d["forward_cofactors"],"inverse_cofactors":d["inverse_cofactors"]}})
        verdict,why = V.ring_iso(graph,"E",_runner=never_run)
        return decision(verdict == V.ISO_VERIFIED,why,raw_verdict=verdict)
    if kind == "extension_witness":
        from grandportage import verify as V
        from test_number_field_witness import _graph, _model, _claim, _field
        d = case["inputs"]
        model = _model(d["point_universe"],d["generators"][0])
        model.update(ring_vars=d["variables"],open_conditions=d["guards"])
        graph = _graph([model,_claim(d["coordinate"],_field(d["field_polynomial"]))])
        verdict,why,receipt = V.point_witness(graph,"C",_runner=never_run)
        return decision(verdict == V.WITNESS_VERIFIED,why,raw_verdict=verdict,receipt=receipt)

    if kind in ("jc_cap_obstruction", "bounded_source_point"):
        from grandportage import coefficient_expansion as CE
        d = case["inputs"]
        parameter = d["parameter"]
        ring = d["source_variables"] + [parameter]
        if kind == "jc_cap_obstruction":
            point = {**d["other_retained_values"], **d["selected"], **d["forced"]}
        else:
            point = d["point"]
        images = {**point, parameter:parameter}
        residuals = [G.substitute_polynomial(eq,ring,images,0) for eq in d["source_equations"]]
        if any(not G.parse_polynomial(value,ring,0).is_zero for value in residuals):
            return decision(False,"The supplied source point fails an equation.",residuals=residuals)
        if kind == "bounded_source_point":
            degrees = {}
            for name,value in point.items():
                poly = G.parse_polynomial(value,[parameter],0)
                degrees[name] = max((m[0] for m in poly.terms),default=-1)
            fits = all(degrees[name] <= cap for name,cap in d["caps"].items())
            return decision(fits,"Exact source substitution and polynomial degree caps checked.",
                            residuals=residuals,degrees=degrees,caps=d["caps"])
        if d["cap"] != {"dm4":0}:
            raise ValueError("This source projection is specifically the cap-zero obstruction")
        obstruction = d["coefficient_obstruction"]
        coordinate = obstruction["variable"]
        bounded_images = {**point,"dm4":coordinate}
        equations = []
        for i,expression in enumerate(d["source_equations"]):
            equations.append({"id":["G1","G2","G3","G5"][i],"expression":expression,"degree":1,
                              "coverage":CE.COMPLETE,
                              "coefficients":obstruction["rows"] if i == 1 else {"0":"0","1":"0"}})
        spec = {"schema":CE.SCHEMA,"characteristic":0,"parameter":parameter,
                "coefficient_variables":[coordinate],"source_variables":d["source_variables"],
                "images":bounded_images,"bounded_variables":{"dm4":{"cap":0,"coefficients":[coordinate]}},
                "equations":equations}
        expansion = CE.verify(spec)
        rows = list(expansion["equations"][1]["checked_coefficients"].values())
        unit = G.check_membership_identity("1",rows,obstruction["unit_cofactors"],[coordinate],0)
        return decision(False,"The unrestricted source point verifies, but the complete cap-zero coefficient fiber contains 1.",
                        unrestricted_residuals=residuals,coefficient_expansion=expansion,unit_receipt=unit)
    if kind == "coefficient_expansion":
        from grandportage import coefficient_expansion as CE
        d = case["inputs"]
        keys = ("parameter","source_variables","coefficient_variables","images","bounded_variables","equations")
        spec = {"schema":CE.SCHEMA,"characteristic":0,**{key:d[key] for key in keys}}
        try:
            report = CE.verify(spec)
        except CE.CoefficientExpansionError as exc:
            return decision(False,exc)
        control = None
        if "counterexample_coefficients" in d:
            names = d["coefficient_variables"]
            values = d["counterexample_coefficients"]
            selected = [G.substitute_polynomial(row,names,values,0)
                        for row in report["equations"][0]["checked_coefficients"].values()]
            omitted = G.substitute_polynomial("a1*b1",names,values,0)
            if any(v != "0" for v in selected) or omitted != "1":
                raise ValueError("Invalid selected-coefficients counterexample")
            control = {"selected_rows":selected,"omitted_quadratic_row":omitted}
        return decision(d["requested_license"] in report["licenses"],
                        "Requested implication compared with the replayed license.",
                        receipt=report,counterexample=control)

    raise ValueError("Unknown oracle route: "+kind)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-oracle",action="store_true")
    args = parser.parse_args()
    cases,routes = validate()
    print("Validated",len(cases),"cases, source anchors and pinned oracle identity.")
    if not args.run_oracle:
        return
    results = []
    for case,path in cases:
        route = routes[case["id"]]
        record = {"id":case["id"],"case_sha256":sha(path),"expected":case["expected"]["verdict"],
                  "layer":route["layer"],"route":route["kind"],"limitation":route.get("limitation")}
        try:
            record.update(probe(case,route))
            if record["observed_verdict"] is not None:
                same = record["observed_verdict"] == record["expected"]
                record["status"] = "AGREES" if same else (
                    "KNOWN_DIFFERENCE" if route.get("known_difference") else "REVIEW_REQUIRED")
                if not same:
                    record["difference_class"] = route.get("known_difference","untriaged")
        except Exception as exc:
            record.update(status="ERROR",observed_verdict=None,reason=str(exc),traceback=traceback.format_exc())
        results.append(record)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    report = {"schema_version":1,"timestamp_utc":stamp,"oracle_commit":PIN,
              "oracle_path":str(ORACLE),"runner_sha256":sha(Path(__file__)),
              "routes_sha256":sha(ROOT/"oracle/ROUTES.json"),
              "schema_sha256":sha(ROOT/"corpus/case.schema.json"),
              "python":sys.version,"summary":dict(Counter(r["status"] for r in results)),
              "scope":"Layer-specific legacy observations, not GP 0.50 held claims or a completed G0 gate.",
              "results":results}
    history = ROOT/"reports/oracle-runs"
    history.mkdir(exist_ok=True)
    payload = json.dumps(report,indent=2,ensure_ascii=False)+"\n"
    with (history/(stamp+".json")).open("x",encoding="utf-8") as f:
        f.write(payload)
    (ROOT/"reports/ORACLE-RESULTS.json").write_text(payload,encoding="utf-8")
    print(json.dumps(report["summary"]))
    for result in results:
        if result["status"] in ("ERROR","REVIEW_REQUIRED","KNOWN_DIFFERENCE"):
            print(result["id"],result["status"],result["reason"][:180])
    if any(r["status"] in ("ERROR","REVIEW_REQUIRED") for r in results):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
