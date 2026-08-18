# RTK final matched local result — Stage-4D3 + clean-room replay

**Status:** final frozen **local** matched result for the preregistered production objective.  This is not a global-minimum theorem and not by itself an observational-preference/significance/Bayes claim.

## Frozen objective

- objective: `matched-ultra-linstep2+dense-BOSS`
- production mapping: `eff`
- recenter tolerance: `0.005`
- objective fingerprint: `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`

## Final RTK accepted point

- As `2.0877827951474356e-09`
- Ob `0.046800730927437424`
- Om `0.2522864064078236`
- h `0.691103719964454`
- lambda_D `219457.5727136581`
- ns `0.9645577770978523`
- zre `7.328459220286924`
- center fingerprint `9b3b0a7f44e48ed0eb80b8907382a87ae40c079b125d14422f0e040e9dd78d41`
- accepted local score `S_RTK = 1050.249912429787`

## Stage-4D3 numerical proof

### Base stencil scale 1

- workflow run `32117012431`
- artifact `9322103180`, `rtk-autonomous-dense-rtk-stationarity`
- digest `sha256:13baded38c6cbcc0e19a58b9f680e1d906dee3d41cff8da09daa6c38a02a80e0`
- best improvement `0.0`
- eff Hessian positive definite
- minimum eff eigenvalue `2.539372582019114e-4`

### Half stencil scale 1/2

- workflow run `32133215190`
- artifact `9328770791`, `rtk-autonomous-dense-rtk-half-stencil`
- digest `sha256:9329f217bf58947708e3643c1982e8369375fb2c4b55094fc490b1b299f8998d`
- exact center and objective fingerprints match the final RTK candidate
- `S_center = S_best_exact = 1050.249912429787`
- best improvement `0.0`
- eff Hessian positive definite, eigenvalues:
  `[0.0002755537750933801, 0.022109338548007403, 0.0488778149942228, 0.08489396919468396, 0.11750099452408003, 0.8139167341773023, 1.8754372309459193]`
- k01 Hessian positive definite; minimum k01 eigenvalue `0.0002757135581862385`
- runtime checked against the live lock: Python `3.12.3`, NumPy `2.5.2`, SciPy `1.18.0`, clipy-like `0.15`, pinned CLASS/Pantheon and exact Planck archive SHA256.

Therefore the official state certification is:

`N5_BASE_AND_HALF_STENCIL_PASS`

and the current candidate satisfies the preregistered two-adjacent-scale local interior-minimum proof gate.

## ΛCDM matched local reference

Accepted score point:

- As `2.1054040998203598e-09`
- Ob `0.04858764689799632`
- Om `0.2611722579449536`
- h `0.6782837587382693`
- lambda `0`
- ns `0.9653185632254442`
- zre `7.788312934950947`
- `S_LCDM = 1049.966118347761`

## Independent fresh-tree paired replay

- workflow run `32148894768`
- artifact `9329042339`, `rtk-clean-room-matched-minima-reproduction`
- digest `sha256:79fe90fedda3d914cada442f620ac63d6f6caa1d27eb271191f7517e9c9963b2`
- target fingerprint `91ff4471a86ba9ac0d84cea7ad945cdf54b96b52dac111b6b5db47d106af618c`
- classification `INDEPENDENT_FRESH_TREE_MATCHED_MINIMA_REPLAY`
- status `PASS`
- exact replay tolerance `2e-6`
- RTK replayed score `1050.249912429787`, error `0.0`
- ΛCDM replayed score `1049.966118347761`, error `0.0`
- replayed delta error `0.0`
- pinned CLASS `36cf283628c4a3330ec9fd3d84239bf775f77317`
- pinned Pantheon `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`
- Python `3.12.3`, NumPy `2.5.2`, SciPy `1.18.0`
- Planck archive SHA expected by the live lock: `0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6`
- exact-float cache version `clean-room-exact-float-v2`

Official final replay certification:

`INDEPENDENT_FRESH_TREE_REPLAY_PASS`

## Final frozen raw local comparison

`Delta S = S_RTK - S_LCDM = +0.2837940820259064`

Thus ΛCDM has the lower **raw local objective** by `0.2837940820259064` on the frozen matched objective.  This number is exactly reproduced by the independent fresh-tree replay.

This does **not** imply a statistically significant preference.  RTK has an additional physical coordinate `lambda_D`, and any information criterion or Bayesian evidence requires its own explicit parameter-count/prior/effective-sample protocol.  No global-minimum claim follows from the local Stage-4D3 Hessian proof.
