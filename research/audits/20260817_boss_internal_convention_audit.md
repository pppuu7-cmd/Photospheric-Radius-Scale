# BOSS DR12 internal convention audit

Status: **internal pipeline convention consistent; external publication-level cross-check remains separate**.

## Stored 9-vector order

The repository file `rtk/data/boss_DR12Consensus_final.dat` stores, for z = 0.38, 0.51, 0.61 in that order:

1. geometry entry historically labeled `DM_over_rs`,
2. geometry entry labeled `bao_Hz_rs`,
3. `f_sigma8`.

Numerical values are:

- z=0.38: 1518.36, 81.5095, 0.49749
- z=0.51: 1977.44, 90.4474, 0.457523
- z=0.61: 2283.18, 97.2556, 0.436148

The covariance file is 9x9 in the same ordering.

## Runner convention

`rtk/joint_profile_runner.py` defines `R_FID = 147.78` Mpc and predicts:

- first geometry component: `D_M(z) * R_FID / r_d`,
- second geometry component: `H(z) * r_d / R_FID`,
- third component: either `fσ8_eff` or the separately tracked `fσ8_k01` mapping.

Thus the dimensions are:

- first component: Mpc,
- second component: km s^-1 Mpc^-1,
- third component: dimensionless.

The legacy label `DM_over_rs` is therefore potentially misleading if read literally: in this pipeline it denotes the fiducially rescaled distance `D_M r_d,fid / r_d`, not the dimensionless ratio `D_M/r_d`.

## Covariance scale sanity

The covariance diagonal is numerically compatible with those dimensions: the first distance variances are O(500--1000) Mpc^2, the H variances O(3--4) (km s^-1 Mpc^-1)^2, and the growth variances O(10^-3).

## Internal conclusion

No internal unit mismatch is visible between the stored vector, covariance ordering and the implemented prediction formulas. The same `R_FID` is used inversely for D_M and H as required by the chosen fiducial-rescaling convention.

## Remaining independent gate

This document is not an external provenance proof. Before a publication-strength claim, independently verify against the original BOSS DR12 consensus release/paper that:

- `r_d,fid = 147.78 Mpc` is the intended fiducial ruler for this exact vector/covariance,
- the vector convention is exactly `D_M r_d,fid/r_d`, `H r_d/r_d,fid`, `fσ8`,
- the 9x9 covariance corresponds to precisely this ordering and normalization.

Until that external check is recorded, classify this item as **internally consistent, externally pending**.
