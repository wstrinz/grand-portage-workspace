# JC source depth-6 fixtures

- `boundary_v1.json` is GP's exact portable projection of the native boundary
  receipt: the 3,262-term `R2B`, 6,124-term `beta`, and 33 rung digests.
- `chain_v1.json.gz` is byte-identical to the certificate landed by JC commit
  `cb3136c`. Its compressed SHA-256 is
  `7d0ab133e5e0bd3f9f82d6cdac66302c8e3078321113820b56ca2ef04d4a5871`;
  its canonical uncompressed SHA-256 is
  `d5ed44977e1f39312fbd2d30a286f686a0cd26d55dba237420a7a3d2bf513f15`.

Run the routine consumer gate with:

```powershell
python experiments/jc_h3_source_depth6/chain_adapter.py
```

Add `--full-replay` to recompute all exact face substitutions. The certificate
does not prove raw E-system-to-face extraction and has no graph effect.
