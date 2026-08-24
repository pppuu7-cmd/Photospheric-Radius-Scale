# A5/B9 cross-basin RTK strip-lensing diagnostic — 2026-08-24

Status: **DIAGNOSTIC ONLY — NOT AN A5 CERTIFICATE**

Purpose: test the symmetric hypothesis that the B9 RTK reoptimization may also have exposed a better point of the unchanged A5 objective `matched-ultra-linstep2+dense-BOSS`.

Historical fresh-tree A5 RTK score:

`S_A5,RTK(old) = 1050.249912429787`.

B9 recentered RTK center, after removing the standalone lensing term:

`S_A5,RTK(B9-center) = 1050.2560245726381`,

so the B9 RTK center is worse than the historical A5 RTK point by

`+0.006112142851179669`.

## Exact inherited base-scale stencil

Source B9 run: `32518496348`.
Source artifact: `9464480301`.

The artifact contains 101 exact B9 stationarity points with both `S_B9_eff` and `S_base_eff` stored point-by-point. Searching all 101 `S_base_eff` values gives:

- best label: `center`;
- best baseline-only score: `1050.2560245726381`;
- improvement relative to the B9 RTK center: `0.0`;
- difference relative to the historical A5 RTK score: `+0.006112142851179669`.

Thus no exact point in the inherited base-scale B9 stencil improves the historical RTK A5 point.

## Exact inherited half-scale stencil

Source B9 run: `32538458738`.
Source artifact: `9468954931`.
Artifact digest: `sha256:e4193abe049f6035fb50e9933fafff47c276ef4c567fcb7c15050f994d4d3409`.

Again 101 exact points were inspected using only their stored `S_base_eff` values. Result:

- best label: `center`;
- best baseline-only score: `1050.2560245726381`;
- improvement relative to the B9 RTK center: `0.0`;
- difference relative to the historical A5 RTK score: `+0.006112142851179669`.

Therefore neither inherited B9 stencil contains evidence for a deeper RTK basin of the original A5 objective.

## Best-known-pair implication

The independently confirmed new LCDM cross-basin seed has

`S_A5,LCDM(new seed) = 1049.400976604194`.

Because the historical RTK A5 point remains better than the B9 RTK seed, the provisional best-known mixed pair is

`Delta S_A5,best-known provisional = 1050.249912429787 - 1049.400976604194 = +0.8489358255928892`.

This is **not frozen**: the new LCDM seed must first complete its independently preregistered baseline stationarity and fresh-tree replay chain. It is only a navigation quantity.

## Interpretation

The cross-basin discovery is presently strongly asymmetric. B9 exposed a substantially deeper known LCDM point of the baseline objective, while the corresponding RTK reoptimized neighborhood does not beat the already certified historical RTK point.

This diagnostic does not prove that no deeper RTK basin exists elsewhere. It only rules out the already-computed B9 RTK base/half neighborhoods as evidence for one.
