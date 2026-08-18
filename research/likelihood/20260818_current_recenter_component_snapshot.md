# Current recentered RTK component snapshot

Date: 2026-08-18

Status: **provisional current-center diagnostic only; RTK stationarity is still running and this is not a frozen matched Delta S.**

## Current RTK center

From `research/state/current.json`, iteration 64:

- As = `2.0877827951474356e-09`
- Ob = `0.046800730927437424`
- Om = `0.2522864064078236`
- h = `0.691103719964454`
- lambda_D = `219457.5727136581`
- ns = `0.9645577770978523`
- zre = `7.328459220286924`

The exact dense axis replay at this center, workflow run `32113618318`, found the center itself to be best on all 14 axis directions:

- `S_RTK,center = 1050.249912429787`
- `chi2_BOSS_eff = 7.626492028405815`
- `chi2_SN = 39.59899396804523`
- `logL_planck = -501.5122132166679`
- therefore `-2 logL_planck = 1003.0244264333358`

The next 7D Hessian at this center is run `32117012431` and is still in progress at the time of this checkpoint.

## Frozen LCDM reference

From the validated matched component checkpoint `20260817_matched_component_decomposition.md`:

- `S_LCDM = 1049.966118347761`
- `-2 logL_planck = 1003.4825659190`
- `chi2_SN = 39.7559388343`
- `chi2_BOSS_eff = 6.7276135944`

## Provisional component deltas, RTK minus LCDM

| component | current RTK | frozen LCDM | delta RTK-LCDM |
|---|---:|---:|---:|
| -2 log L Planck | 1003.024426433336 | 1003.4825659190 | **-0.458139485664** |
| chi2 Pantheon | 39.598993968045 | 39.7559388343 | **-0.156944866255** |
| chi2 BOSS eff | 7.626492028406 | 6.7276135944 | **+0.898878434006** |
| total S eff | 1050.249912429787 | 1049.966118347761 | **+0.283794082026** |

The component arithmetic closes to rounding precision.

## Interpretation

The latest sequence of exact mixed-mode / half-stencil recentering has reduced the provisional total RTK-minus-LCDM gap while making the qualitative component tension sharper:

- Planck now favors the current RTK point more strongly than at the earlier provisional center;
- Pantheon still favors RTK modestly;
- BOSS remains the only positive contribution to the provisional RTK-minus-LCDM gap, and its penalty is slightly larger than in the earlier `+0.88456` snapshot.

Thus the optimization is continuing mainly along a CMB-driven correlated manifold rather than eliminating the late-time geometry/growth pressure.

## Claim boundary

This file does **not** freeze a matched Delta S. `research/state/current.json` correctly leaves `comparison.dense_raw_delta_S = null` until the current RTK stationarity / multiscale proof sequence terminates.
