# JC source depth-6 fixtures

- boundary_v1.json is GP's exact portable projection of the native boundary
  receipt: the 3,262-term R2B, 6,124-term beta, and 33 rung digests.
- chain_v1.json.gz is byte-identical to the certificate landed by JC commit
  cb3136c. Its compressed SHA-256 is
  7d0ab133e5e0bd3f9f82d6cdac66302c8e3078321113820b56ca2ef04d4a5871;
  its canonical uncompressed SHA-256 is
  d5ed44977e1f39312fbd2d30a286f686a0cd26d55dba237420a7a3d2bf513f15.
- graded_face_extraction_v1.json freezes the five reduced E-system rows,
  finite root supports, coordinate-series manifest, and 25 expected face
  commitments. Its SHA-256 is
  6c8887034321884b6bb0aa7cd8cf04d90e472a36f4a6ba4035a53e7eda1aa8a1.

Run the chain consumer with:

    python experiments/jc_h3_source_depth6/chain_adapter.py

Add --full-replay to recompute all exact chain substitutions. The chain
certificate itself has no graph effect.

Run the independent graded extraction with:

    python experiments/jc_h3_source_depth6/face_extraction_adapter.py
    python experiments/jc_h3_source_depth6/face_extraction_adapter.py --full-source-replay

The stronger mode rederives the five reduced rows from the defining E-system
formula before extraction. This closes raw E-system-to-face translation
validation but retains graph effect NONE and supplies no reverse point lift.
