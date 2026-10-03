"""post-G2 §3.7: 3a-owned expressible cases through the shared frontend reproduce the receipt."""
import json
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile"
RECEIPT = ROOT / "reports/PHASE-3A-CORPUS.json"
TOOLCHAIN = Path.home() / ".elan/toolchains" / (PROFILE / "lean-toolchain").read_text(
    encoding="utf-8").strip().replace("/", "--").replace(":", "---")


class Corpus3aTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env = dict(os.environ, PATH=str(TOOLCHAIN / "bin") + os.pathsep + os.environ["PATH"])
        subprocess.run([str(TOOLCHAIN / "bin/lake.exe"), "build", "gp_corpus_run"], cwd=PROFILE,
                       env=env, check=True, capture_output=True)
        out = subprocess.run([str(PROFILE / ".lake/build/bin/gp_corpus_run.exe"), str(ROOT),
                              str(PROFILE / "slice/corpus-3a.json")], check=True, capture_output=True, text=True)
        cls.fresh = json.loads(out.stdout)

    def test_matches_committed_receipt(self):
        self.assertEqual(self.fresh, json.loads(RECEIPT.read_text(encoding="utf-8")))

    def test_every_case_agrees_without_loss(self):
        self.assertEqual(self.fresh["losses"], 0)
        for case in self.fresh["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["observed"], case["expected"])


if __name__ == "__main__":
    unittest.main()
