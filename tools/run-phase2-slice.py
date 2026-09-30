"""Execute selected unchanged kernel fixtures through the native bound-span runner."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "phase2/lean/.lake/build/bin/gp_span_runner.exe"
SCRATCH = ROOT / "tmp/phase2-slice"
POLYNOMIALS = {
    "x": [{"exp": 1, "num": 1, "den": 1}],
    "x^2": [{"exp": 2, "num": 1, "den": 1}],
}
ONE = [{"exp": 0, "num": 1, "den": 1}]

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()

def binding(generators, target):
    return {
        "statementHash": digest({"kind": "formal-span", "generators": generators, "target": target}),
        "scopeHash": digest({"coefficient_field": "Q", "reach": "formal-univariate-span"}),
        "modelHash": digest({"ring": "Q[x]", "encoding": "sparse-rational-terms/v1"}),
        "inputHashes": [digest(generators), digest(target)],
        "authority": "gp50-rat-span-test-stub",
        "authorityVersion": 1,
        "kernelVersion": 1,
    }

def prepared(generators, target, version=1):
    b = binding(generators, target)
    clause = {"key": 1, "version": version, "binding": b,
              "generators": generators, "target": target}
    receipt = {"name": "receipt-1", "claim": 1, "version": version,
               "binding": copy.deepcopy(b), "cofactors": [copy.deepcopy(ONE)]}
    registry = {"schema_version": 1, "clauses": [clause], "receipts": [receipt]}
    current = {"kind": "current", "value": {"claim": 1, "version": version, "binding": b}}
    warrant = {"kind": "warrant", "value": {
        "id": 10, "claim": 1, "version": version, "binding": copy.deepcopy(b),
        "evidence": {"kind": "receipt", "data": receipt["name"]}}}
    return registry, {"schema_version": 1, "events": [current, warrant]}

def translate(case):
    inputs = case["inputs"]
    if case["id"] == "GP-A18":
        if set(inputs) != {"old_ideal", "new_ideal", "identity"} or inputs["identity"] != "x=0":
            raise ValueError("A18 requires the literal declared x=0 identity contract")
        old = [copy.deepcopy(POLYNOMIALS[name]) for name in inputs["old_ideal"]]
        new = [copy.deepcopy(POLYNOMIALS[name]) for name in inputs["new_ideal"]]
        if old != [POLYNOMIALS["x"]] or new != [POLYNOMIALS["x^2"]]:
            raise ValueError("A18 bridge supports only this unchanged recorded ideal mutation")
        registry, events = prepared(old, copy.deepcopy(POLYNOMIALS["x"]))
        baseline = (copy.deepcopy(registry), copy.deepcopy(events))
        changed_registry, changed_events = prepared(new, copy.deepcopy(POLYNOMIALS["x"]), 2)
        changed_registry["receipts"] = registry["receipts"]
        changed_events["events"][1] = events["events"][1]
        return changed_registry, changed_events, baseline, (
            "Actual x=1*x replay accepts before the input mutation. "
            "The unchanged receipt keeps its old version/input binding after (x) becomes (x^2). "
            "The query is whether that receipt remains current, not geometric emptiness."), 1
    if case["id"] == "GP-A17":
        if set(inputs) != {"attempt_status", "earlier_current_warrant"} or inputs["earlier_current_warrant"] is not False:
            raise ValueError("A17 bridge requires no earlier current warrant")
        statuses = {"UNVERIFIED": "absent", "TIMEOUT": "timeout", "FAILED": "failed"}
        status = statuses[inputs["attempt_status"]]
        registry, events = prepared([copy.deepcopy(POLYNOMIALS["x"])], copy.deepcopy(POLYNOMIALS["x"]))
        baseline = (copy.deepcopy(registry), copy.deepcopy(events))
        registry["receipts"] = []
        events["events"][1]["value"]["evidence"] = {"kind": "attempt", "status": status}
        return registry, events, baseline, (
            "Explicit UNVERIFIED-to-absent vocabulary translation; no earlier warrant is supplied. "
            "A successful exact-replay contrast uses the same statement and current binding."), 1
    if case["id"] == "GP-A25b":
        if set(inputs) != {"identifiers", "alias_evidence"} or inputs["alias_evidence"] is not None:
            raise ValueError("A25b requires the unchanged absent-alias contract")
        names = inputs["identifiers"]
        if len(names) != 2 or names[0] == names[1]:
            raise ValueError("A25b requires two distinct selected object identities")
        first, first_events = prepared([copy.deepcopy(POLYNOMIALS["x"])], copy.deepcopy(POLYNOMIALS["x"]))
        second, second_events = prepared([copy.deepcopy(POLYNOMIALS["x"])], copy.deepcopy(POLYNOMIALS["x"]))
        for registry, events, key, name in ((first, first_events, 1, names[0]),
                                          (second, second_events, 2, names[1])):
            b = copy.deepcopy(registry["clauses"][0]["binding"])
            b["modelHash"] = digest({"ring": "Q[x]", "selected_object": name})
            b["inputHashes"].append(digest({"selected_object": name}))
            registry["clauses"][0].update(key=key, binding=copy.deepcopy(b))
            registry["receipts"][0].update(claim=key, binding=copy.deepcopy(b))
            events["events"][0]["value"].update(claim=key, binding=copy.deepcopy(b))
            events["events"][1]["value"].update(claim=key, binding=copy.deepcopy(b))
        baseline = (copy.deepcopy(second), copy.deepcopy(second_events))
        second["clauses"].insert(0, first["clauses"][0])
        second["receipts"] = first["receipts"]
        return second, second_events, baseline, (
            "Both selected identities are preserved in registry keys and model/input bindings. "
            "The B warrant asks for the A-owned receipt; no alias rule is registered. "
            "A fresh independently bound B receipt is a separate positive control."), 2
    raise ValueError("Uncommissioned fixture: " + case["id"])

def execute(label, registry, events):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    config_path = SCRATCH / (label + ".registry.json")
    event_path = SCRATCH / (label + ".events.json")
    config_path.write_bytes((encoded(registry) + "\n").encode("utf-8"))
    event_path.write_bytes((encoded(events) + "\n").encode("utf-8"))
    result = subprocess.run([str(EXE), str(config_path), str(event_path)], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8", check=True)
    observed = json.loads(result.stdout)
    if observed["status"] != "OK":
        raise ValueError(label + ": malformed native input: " + observed.get("error", ""))
    return observed, {
        "registry_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "events_sha256": hashlib.sha256(event_path.read_bytes()).hexdigest(),
    }

def run(output):
    results = []
    tags = json.loads((ROOT / "corpus/LAYER-TAGS.json").read_text(encoding="utf-8"))
    for case_id in ("GP-A17", "GP-A18", "GP-A25b"):
        path = ROOT / "corpus/must" / (case_id + ".json")
        raw = path.read_bytes()
        case = json.loads(raw)
        row = next(row for row in tags["cases"] if row["id"] == case_id)
        assert row["primary_layer"] == "kernel"
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
        registry, events, baseline, fidelity, query = translate(case)
        positive, positive_inputs = execute(case_id + "-positive-control", *baseline)
        assert query in positive["held"], case_id + ": positive replay control failed"
        observed, receipts = execute(case_id, registry, events)
        verdict = "ACCEPT" if query in observed["held"] else "REFUSE"
        assert verdict == case["expected"]["verdict"], case_id + ": unexpected native verdict"
        assert path.read_bytes() == raw, case_id + ": fixture modified"
        results.append({"id": case_id, "source_sha256": hashlib.sha256(raw).hexdigest(),
                        "expected": case["expected"], "observed": verdict, "native_query": query,
                        "native_result": observed, "positive_control": positive,
                        "native_inputs": receipts, "positive_inputs": positive_inputs, "full_fixture_contract": True,
                        "translation_fidelity": fidelity})
    record = {"schema": "gp-phase2-native-slice/v1", "case_count": len(results),
              "complete_ten_case_slice": False, "g2_pass": False,
              "runner_sha256": hashlib.sha256(EXE.read_bytes()).hexdigest(),
              "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "cases": results,
              "remaining_slice_behaviors": [
                  "non-exhaustive cover", "independent checked support and targeted retraction",
                  "failed retry", "real supersession branch-order fixture", "K2 narrowing",
                  "earned consequence", "proved-overlap conflict", "corpus positive control"]}
    output.write_bytes((json.dumps(record, indent=2) + "\n").encode("utf-8"))
    print("Native slice: 3 unchanged fixtures passed; 3 exact-replay positive controls passed.")
    return record

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/PHASE-2-SLICE.json")
    args = parser.parse_args()
    run(args.output)
