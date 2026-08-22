# Final Family-F2 publication audit

This experimental adapter checks whether the final `(75,125)` public export's
dossier, release manifest, Gate-B custody matrix, replay inventory, and release
gates describe the same observation.  It is a derived audit with graph effect
`NONE`; it does not promote any theorem or custody grade.

```text
python -m experiments.f2_75_125_publication.adapter \
  fixtures/dossier/f2_75_125_publication/dossier.json \
  --source-root ../math-stuff \
  --export-root ../plane-jacobian-75-125
```

`--source-root` names the canonical campaign checkout used by the dossier and
custody archaeology. `--export-root` names the independently published tree.
Keeping them separate prevents a stale `_public_export_75_125` staging copy
from manufacturing missing-payload or replay failures after publication. For
backward compatibility, omitting `--export-root` still audits the historical
in-tree staging export; a source root that itself contains
`artifacts/release-manifest.json` is treated as the public repository.

Use `--require-clear` in a publication gate.  It returns nonzero while any
`BLOCKER` finding remains.  `OPPORTUNITY` findings deliberately do not change a
grade: they identify evidence worth curator review. The audit checks the
standalone Lean declaration binding and manifest-reported kernel, comparator,
and nanoda layers separately; a broad `Mathlib.Tactic` import is reported as
replay-cost debt even when all proof layers pass.
