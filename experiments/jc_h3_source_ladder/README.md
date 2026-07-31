# JC actual-source ordered-chain adapter

This isolated adapter reads the frozen native
`f2_h3_q_receipt_probe.json`, translates its exact five top-face polynomials,
and asks GP to replay the landed `(2, 5, 1, 4, 3)` substitution order.

```console
python experiments/jc_h3_source_ladder/adapter.py
```

The default run checks that the generated envelope is byte-identical to the
frozen GP fixture. `--write-fixture` is an explicit maintainer operation for a
reviewed native receipt update. The envelope binds the native file's SHA-256.

The adapter does not import the native Python producer, write `math-stuff`, or
promote any JC ledger. Native extraction and replay stay in JC; GP checks the
composition boundary and preserves its outstanding model-binding authority.

`second_face_adapter.py` is the first normalization-bearing consumer. Literal
v1 replay correctly refuses all five second-face solves: every discrepancy is
a multiple of the landed scalar-gauge equation `15*t^3+1=0`. The v2 envelope
retains that equation as a persistent normalization generator and supplies an
exact cofactor at every step. No generically nonzero expression is inverted.
