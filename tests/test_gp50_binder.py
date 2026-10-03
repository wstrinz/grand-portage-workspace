"""G1 decision 2 / Addendum A4: generated theorem warrants, the binder's records, and their use."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile"
RUNNER = PROFILE / ".lake/build/bin/gp_corpus_run.exe"
RECORDS = ROOT / "reports/PHASE-3A-BINDER.json"
GENERATED = ROOT / "binding/GPBinding/Warrants/Generated.lean"
STANDARD = {"propext", "Quot.sound", "Classical.choice"}
TOOLCHAIN = Path.home() / ".elan/toolchains" / (PROFILE / "lean-toolchain").read_text(
    encoding="utf-8").strip().replace("/", "--").replace(":", "---")


def run(*args):
    return json.loads(subprocess.run([str(RUNNER), str(ROOT), *map(str, args)], check=True,
                                     capture_output=True, text=True, encoding="utf-8").stdout)


class BinderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env = dict(os.environ, PATH=str(TOOLCHAIN / "bin") + os.pathsep + os.environ["PATH"])
        subprocess.run([str(TOOLCHAIN / "bin/lake.exe"), "build", "gp_corpus_run"], cwd=PROFILE,
                       env=env, check=True, capture_output=True)

    def test_generated_warrants_are_current(self):
        cands = run(PROFILE / "slice/manifest.json", "--candidates") + \
            run(PROFILE / "slice/corpus-3a.json", "--candidates")
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "cands.json"
            src.write_text(json.dumps(cands, ensure_ascii=False), encoding="utf-8")
            out = Path(d) / "Generated.lean"
            subprocess.run([sys.executable, str(ROOT / "tools/gen-warrants.py"), str(src), "--out", str(out)],
                           check=True, capture_output=True)
            self.assertEqual(out.read_text(encoding="utf-8"), GENERATED.read_text(encoding="utf-8"))

    def test_records_are_bound_with_standard_axioms(self):
        records = json.loads(RECORDS.read_text(encoding="utf-8"))["records"]
        self.assertTrue(records)
        for r in records:
            with self.subTest(declaration=r["declaration"]):
                self.assertTrue(r["bound"])
                self.assertLessEqual(set(r["axioms"]), STANDARD)

    def test_minted_theorem_warrants_support_their_claims(self):
        out = run(PROFILE / "slice/manifest.json", "--binder", RECORDS)
        minted = [t for c in out["cases"] for t in c.get("theorem_warrants", [])]
        self.assertTrue(minted)
        self.assertTrue(all(t["supported"] for t in minted))
        self.assertEqual(out["agree"], out["case_count"])

    def test_tampered_record_mints_nothing(self):
        records = json.loads(RECORDS.read_text(encoding="utf-8"))
        for r in records["records"]:
            r["scopeHash"] = r["scopeHash"].replace("true", "false")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "tampered.json"
            path.write_text(json.dumps(records), encoding="utf-8")
            out = run(PROFILE / "slice/manifest.json", "--binder", path)
        self.assertFalse([t for c in out["cases"] for t in c.get("theorem_warrants", [])])


if __name__ == "__main__":
    unittest.main()
