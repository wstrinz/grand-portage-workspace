"""Conservative Phase 2 source/documentation budget checks; no build or writes."""
import json
from pathlib import Path
import re
import subprocess
ROOT = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")
def has_executable_declaration(source):
    pattern = re.compile(r"^\s*(?:(?:private|protected|noncomputable|partial)\s+)*(def|abbrev|structure|inductive|instance|opaque)\b", re.M)
    for match in pattern.finditer(source):
        if match.group(1) in {"def", "abbrev"}:
            header = source[match.end():].split(":=", 1)[0].strip()
            if header.endswith(": Prop"):
                continue  # Erased proposition; no production executable helper.
        if match.group(1) == "structure":
            header = source[match.end():].split("where", 1)[0].strip()
            if header.endswith(": Prop"):
                continue  # Proof records are erased as well as proposition defs.
        return True
    return False

def measure():
    baseline = json.loads((ROOT / "reports/PHASE-2-BASELINE.json").read_text(encoding="utf-8"))
    change = git("diff", "--unified=0", baseline["base_commit"], "--", "*.md")
    words = sum(len(line[1:].split()) for line in change.splitlines()
                if line.startswith("+") and not line.startswith("+++"))
    words += sum(len((ROOT / p).read_text(encoding="utf-8").split())
                 for p in git("ls-files", "--others", "--exclude-standard").splitlines()
                 if p.endswith(".md"))
    counts = {"logic": 0, "decoder": 0, "statement": 0, "proof": 0}
    modules = []
    for path in sorted((ROOT / "phase2/lean/GP50").rglob("*.lean")):
        source = path.read_text(encoding="utf-8")
        if "Proof" in path.stem or "Completeness" in path.stem:
            # A mixed proof/executable-helper file gets charged entirely to logic.
            category = "logic" if has_executable_declaration(source) else "proof"
        elif "Decod" in path.stem:
            category = "decoder"
        elif path.stem in {"Statement", "Semantics"}:
            category = "statement"
        else:
            category = "logic"
        size = len(source.splitlines())
        counts[category] += size
        modules.append({"path": str(path.relative_to(ROOT)), "category": category, "lines": size})
    limits = {"logic": (500, 750), "decoder": (400, 600), "statement": (80, 120)}
    failures = [f"{name} tripwire: {counts[name]} > {stop}"
                for name, (_, stop) in limits.items() if counts[name] >= stop]
    if words >= 15000:
        failures.append(f"Markdown tripwire: {words} > 15000")
    status_words = len((ROOT / "STATUS.md").read_text(encoding="utf-8").split())
    if status_words > 300:
        failures.append(f"STATUS cap: {status_words} > 300")
    for path in (ROOT / "reports").glob("PHASE-2*.md"):
        cap = 500 if path.stem == "PHASE-2-SLICE" else 800
        size = len(path.read_text(encoding="utf-8").split())
        if size > cap:
            failures.append(f"{path.name}: {size} > {cap}")
    return {"baseline": baseline["base_commit"], "counts": counts, "modules": modules,
            "markdown_added_words": words, "markdown_target": 10000,
            "markdown_tripwire": 15000, "status_words": status_words,
            "targets_exceeded": [name for name, (target, _) in limits.items()
                                 if counts[name] > target],
            "failures": failures}
if __name__ == "__main__":
    result = measure()
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result["failures"] else 0)
