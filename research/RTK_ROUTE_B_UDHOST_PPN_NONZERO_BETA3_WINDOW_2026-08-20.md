# RTK Route-B U-DHOST PPN nonzero-beta3 window — 2026-08-20

## Source-of-truth context

- Repository: `pppuu7-cmd/Photospheric-Radius-Scale`
- Branch: `rtk-class-build`
- State observed before this step: iteration 147 (`research/iterations/000147_20260820T055806Z.json`).
- Frozen matched local comparison remains unchanged: `S_RTK=1050.249912429787`, `S_LCDM=1049.966118347761`, `Delta S=+0.2837940820259064`; this remains a local matched-objective result only.

## New source-level result

Primary source: Saito, Yao, Kobayashi, arXiv:2402.10459 / JCAP 06 (2024) 040, especially Eqs. (82)-(90) and Table 1.

For `c_GW=1`,

- `gamma_PPN = 1 + alpha_H`,
- `alpha1_PPN = 4[2 gamma_PPN^2 - gamma_PPN - 1 - beta3]`,
- U-DHOST degeneracy requires `beta2=-6 beta1^2/(1+alpha_L)`.

### Exact-GR boundary

If one imposes exactly `gamma_PPN=1` and `alpha1_PPN=0`, then necessarily `alpha_H=0` and `beta3=0`. Therefore the exact GR-indistinguishable PPN subclass constructed in the source cannot carry the nonzero `beta3` lapse-gradient / normal-acceleration operator required by the RTK mixed spatial-kinetic mechanism.

This closes only the **exact-GR PPN subclass** as a direct RTK carrier. It is not a no-go for experimentally allowed U-DHOST.

### Constructive experimentally allowed nonzero-beta3 point

The new symbolic gate `rtk/route_b_udhost_ppn_nonzero_beta3_window.py` exhibits

- `alpha_H=0`,
- `beta3=1e-6 != 0`,
- `alpha_L=1`,
- `delta1=delta2=0`,
- `beta1 = 3e-6 ± sqrt(12000282)/6000000` (approximately `-5.74357053015434e-4` or `+5.80357053015434e-4`).

At either root,

- `gamma_PPN=1`,
- `beta_PPN=1`,
- `alpha2_PPN=0`,
- `alpha1_PPN=-4e-6`, which lies inside the Table-1 quoted interval,
- the U-DHOST `beta2` degeneracy relation holds exactly.

Hence **PPN + luminal GW + unitary degeneracy do not force beta3 to zero observationally**. They restrict the acceleration channel to a small weak-field window.

## Scientific interpretation

This is a constructive rescue result, but only at the local PPN/EFT level. The decisive next question is quantitative: after canonical normalization, what dimensionless `beta3` is required by the replay-certified RTK `C(a), M_K(a)`? If the local/current required value is `O(1e-5)` or smaller, the U-DHOST route remains directly viable. If it is larger, a fixed-action `X`-dependent environmental/background separation must be demonstrated rather than assumed.

## Non-claims / guards

- no claim that `beta3=1e-6` equals the RTK-required value;
- no claim of one-fixed-action FLRW completion;
- no scalar-radiation/binary-pulsar closure;
- no compact-object/universal-horizon closure;
- no nonlinear hyperbolicity, radiative stability, or matter-loop closure;
- no change to the frozen cosmological fit/model-selection status.

## Next gate

Derive the canonical normalization of the RTK scalar in the U-DHOST EFT basis and compute the required dimensionless `beta3(a)=K(a)/(M^2 M_K(a)^2)` using replay-certified `C(a),M_K(a)` data. Compare the present/weak-field value against the sourced `O(1e-5)` PPN window before invoking any background-dependent escape mechanism.
