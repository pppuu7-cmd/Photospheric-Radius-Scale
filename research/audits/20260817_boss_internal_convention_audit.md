# BOSS DR12 convention audit

Status: **closed for vector convention, units and fiducial ruler**.

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

The legacy label `DM_over_rs` is misleading if read literally: in this pipeline it denotes the fiducially rescaled distance `D_M r_d,fid / r_d`, not the dimensionless ratio `D_M/r_d`.

## External primary-source cross-check

The original BOSS DR12 final cosmological analysis (Alam et al., *The clustering of galaxies in the completed SDSS-III Baryon Oscillation Spectroscopic Survey: cosmological analysis of the DR12 galaxy sample*, arXiv:1607.03155; published MNRAS) reports in its final-consensus table exactly the observables

- `D_M (r_d,fid / r_d)` in Mpc,
- `H (r_d / r_d,fid)` in km s^-1 Mpc^-1,
- `f sigma_8`,

at effective redshifts 0.38, 0.51 and 0.61, and states `r_d,fid = 147.78 Mpc` for the fiducial cosmology. The published BAO+FS central values (1518, 81.5, 0.497), (1977, 90.5, 0.458), (2283, 97.3, 0.436) match the repository vector to its stored extra precision/rounding.

## Covariance scale sanity

The covariance diagonal is numerically compatible with those dimensions: the first distance variances are O(500--1000) Mpc^2, the H variances O(3--4) (km s^-1 Mpc^-1)^2, and the growth variances O(10^-3).

## Conclusion

The BOSS DR12 vector convention, units, fiducial sound horizon and runner rescaling are mutually consistent and agree with the original consensus analysis. This closes the previously open unit/convention concern.

A separate caveat remains: compressed `fσ8` is not fully model-independent for RTK's scale-dependent growth. That is a likelihood-modeling limitation, not a units/convention error, and the project continues to keep `eff` and `k01` mappings separate.
