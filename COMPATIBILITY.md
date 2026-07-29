# Compatibility epochs

Grand Portage separates **file readability** from **mathematical authority**.
An old graph may remain valuable history without retaining every licence that an
older kernel inferred from it.

## The year-zero boundary

Version 0.5.0 establishes:

- `graph_format: 1` — the syntax and ownership of persisted fields;
- `kernel_epoch: 1` — the semantics that decide which transports are licensed;
- `created_with` — the Grand Portage version that wrote the graph.

Every native graph begins with one `meta` event carrying those fields. Native
events have closed schemas: an unknown field is rejected, licensing flags are
JSON booleans, and every edge declares `map_kind` explicitly.

Within one kernel epoch, no field will silently acquire a more permissive
interpretation. A future syntax-only extension can bump `graph_format`; a
change to transport meaning or verifier trust bumps `kernel_epoch`.

The exact pre-epoch implementation is tagged `pre-epoch-0.4.2`.

## Epoch-0 graphs

Unversioned graphs are epoch 0. Version 0.5 reads them through a conservative,
read-only importer. It will not append new events to them and will not blend
them with epoch-1 graphs.

The importer can preserve or reduce authority, never increase it:

- malformed truthy licensing values become `false`;
- a missing `map_kind` becomes the non-licensing `RATIONAL` kind, except that a
  `RESTRICTION` remains the same-coordinate `IDENTITY_MAP` inclusion its type
  already asserts;
- legacy `witness` is read as `strictness_witness`;
- retired `zariski_dense` is dropped;
- old verifier verdicts remain history but are inactive;
- cited, no-map `ring_iso` declarations do not license identities;
- fingerprintless baseline acceptances are stale until deliberately accepted
  again.

## Migration

Migration never rewrites the append-only source:

```console
gp --graph path/to/graph.jsonl migrate --to-epoch1
```

This writes `graph.epoch1.jsonl` and `graph.epoch1.jsonl.audit.json` beside the
source. The audit records the source SHA-256 and every normalization or dropped
field. The new graph is strict-loaded before either artifact is written.

To activate a migrated graph in a new campaign root, choose its destination
explicitly:

```console
gp --graph old/.portage/graph.jsonl migrate --to-epoch1 \
  --epoch1-output new/.portage/graph.jsonl
```

Existing output is never overwritten. Epoch-0 and epoch-1 logs cannot be merged
until the epoch-0 side has been migrated.

## Verifier verdicts

A computed verdict is executable trust. Epoch 1 records:

- verifier identity and verifier-specific version;
- kernel epoch;
- backend;
- a SHA-256 fingerprint of the complete semantic input.

A legacy verdict, a verdict from another implementation epoch, or a verdict
whose target input changed remains visible in history but is `STALE` and does
not populate any effective evidence field. Rerun the verifier to mint a current
answer.

Algebraic verifiers also require an explicit model characteristic. Omission is
unknown, not characteristic zero.

## Next milestone: narrow backend seam and M2

The next architectural step after the epoch-1/L3 hardening cut is a narrow CAS
backend seam, not a promise of broad multi-CAS support. `SingularBackend` remains
the reference implementation and must preserve the exact program, backend
identity, input fingerprint, and verdict provenance that were actually run.

M2 then differential-tests only the load-bearing primitives already used by the
kernel: ideal membership and certificates, saturation, elimination, mapped ideal
pullback, partition coverage, and factorizing decomposition. Backend disagreement
is recorded as an artifact and blocks promotion; it is not resolved by silently
choosing one answer. New backends are added only after this seam and differential
corpus are stable.

This follows the release order: close known semantic defects, cut epoch 1, finish
the L3 gate, then use M2 to widen independent computational crosschecks.

## Sealed campaigns

A sealed epoch-0 experiment should continue with the executable pinned when it
was sealed. Do not migrate or reinterpret it mid-experiment. Migration is for a
new artifact after the seal opens, or for a new campaign root.