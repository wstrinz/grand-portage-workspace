# JC H3 `b=0` transported depth-eight block

This assay composes the previously verified `c9_7` affine pivot with the
landed coefficient-only depth-eight receipt. It independently checks:

- all nine raw `c7_4`, `c8_5`, and `c9_7` coefficient commitments;
- the forced sign and exact native commitment for the transported derivative
  `D7=d/dc7_4-(3/2)c2_3*d/dc9_7`;
- the exact anti-diagonal `3x2` block on `X_b`;
- its three minors, constant rank two, and left syzygy `(c2_3,0,2)`;
- the symbolic identity
  `det[M8|r8]=-(25/16)c2_3^5*c3_5*t*(c2_3*r8_1+2*r8_3)`.

The native derivative-table chain-rule assembly includes earlier solved-
coordinate sensitivities and is recorded as consumed frozen semantics. GP does
not pretend the six raw direct coefficients alone reconstruct `M8`.

The result is standalone `affine_fiber_block_v1` evidence with graph effect
`NONE`. It says that the two transported coordinates are determined in the
named **necessary** extension block and that one residual compatibility remains.
It does not supply the residual vector `r8`, materialize the boundary bodies,
or prove sufficiency for actual-source extension.

The next exact object is therefore `r8`: the three boundary residuals after all
earlier legal solves on `X_b`. Until it lands, `Psi8` is a symbolic pairing and
not an explicit coordinate-ring polynomial.

```powershell
python experiments\jc_h3_b0_free_plane\depth8_adapter.py
python experiments\jc_h3_b0_free_plane\depth8_adapter.py --check-native-bindings
python experiments\jc_h3_b0_free_plane\depth8_adapter.py --native-replay
```

Fixture construction is the only path that executes the native checker:

```powershell
python experiments\jc_h3_b0_free_plane\depth8_adapter.py --write-fixture --force
```
