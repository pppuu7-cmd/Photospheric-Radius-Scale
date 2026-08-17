# BOSS DR12 residual decomposition at current matched points

Status: **validated correlated residual diagnostic; RTK stationarity still pending**.

## Provenance

- Workflow run: `32055604273`, success.
- Job: `95464914446`.
- RTK source checkout: `9854d8b3874ab2d3cc9eb138b0e392f910ea2c7b`.
- CLASS upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`.
- Artifact ID: `9296355450`.
- Artifact ZIP SHA256: `dccb0f729ccb3b971157265d4bd9588123b16111e1b9f12c68857a0714e114ab`.
- Frozen objective: `matched-ultra-linstep2+dense-BOSS`.

The diagnostic reproduced the independent component-control values:
- RTK BOSS eff chi2 = `7.612172203430674`;
- LCDM BOSS eff chi2 = `6.727613594395151`;
- provisional delta chi2_BOSS = `+0.884558609035523` (RTK minus LCDM).

## Raw 9-vector residuals

Raw standardized residual means `(prediction-data)/sqrt(C_ii)`. These are useful pointwise diagnostics but do not include covariance coupling.

| z | observable | RTK | LCDM | qualitative change |
|---:|---|---:|---:|---|
| 0.38 | D_M rfid/rd | +0.029 | +0.629 | RTK much better |
| 0.38 | H rd/rfid | +0.759 | +0.677 | RTK slightly worse |
| 0.38 | f sigma8 | -0.175 | -0.329 | RTK better |
| 0.51 | D_M rfid/rd | -0.215 | +0.300 | RTK better |
| 0.51 | H rd/rfid | -0.536 | -0.498 | RTK slightly worse |
| 0.51 | f sigma8 | +0.852 | +0.632 | RTK worse |
| 0.61 | D_M rfid/rd | +0.445 | +0.856 | RTK better |
| 0.61 | H rd/rfid | -1.147 | -1.045 | RTK worse |
| 0.61 | f sigma8 | +1.426 | +1.168 | RTK worse |

The RTK current point improves the transverse-distance residual in all three redshift bins. The worsening occurs mainly in radial expansion and growth, especially at z=0.51--0.61.

## Correlated leave-one-block-out influence

For a block B, define the diagnostic `I_B = chi2_full - chi2_using_the_complement_subcovariance`. Because the published covariance couples observables and bins, these `I_B` values are **not additive unique chi2 contributions**; they only measure how strongly the full correlated fit changes when a block is omitted.

### Observable-type blocks

| omitted block | I_B RTK | I_B LCDM | delta influence RTK-LCDM |
|---|---:|---:|---:|
| D_M | 0.5541 | 1.0796 | **-0.5254** |
| H | 4.6088 | 3.8812 | **+0.7276** |
| f sigma8 | 4.1919 | 3.1533 | **+1.0386** |

This is the clearest decomposition: transverse BAO distances favor the current RTK point relative to the current LCDM point, while the H and compressed-growth sectors generate additional pressure on RTK.

### Redshift blocks

| omitted z block | I_z RTK | I_z LCDM | delta influence RTK-LCDM |
|---|---:|---:|---:|
| z=0.38 | 2.5445 | 2.8758 | **-0.3313** |
| z=0.51 | 0.9576 | 0.6981 | **+0.2595** |
| z=0.61 | 3.0603 | 2.6249 | **+0.4354** |

Thus z=0.38 is actually relatively improved by RTK; the extra BOSS pressure is concentrated toward z=0.51 and especially z=0.61.

## Exact predictions (eff mapping)

### RTK
- z=0.38: D_M-rescaled `1519.00294`, H-rescaled `82.95503`, fσ8 `0.4895961`.
- z=0.51: `1971.74991`, `89.40657`, `0.4896503`.
- z=0.61: `2297.37627`, `94.85418`, `0.4852402`.

### LCDM
- z=0.38: `1532.43153`, `82.80005`, `0.4826548`.
- z=0.51: `1985.38287`, `89.48041`, `0.4813480`.
- z=0.61: `2310.49572`, `95.06941`, `0.4763659`.

BOSS data are respectively:
- z=0.38: `1518.36`, `81.5095`, `0.49749`;
- z=0.51: `1977.44`, `90.4474`, `0.457523`;
- z=0.61: `2283.18`, `97.2556`, `0.436148`.

## eff versus k01

The k01 mapping changes the full RTK BOSS chi2 only from `7.6121722` to `7.6124370`; the analogous LCDM change is negligible. Therefore the current +0.885 BOSS gap is not primarily an eff-vs-k01 bookkeeping issue. The compressed-RSD model-dependence caveat nevertheless remains mandatory.

## Scientific consequence

The current RTK problem is more specific than “BOSS is worse”:

1. transverse BAO distance D_M is already improved relative to LCDM at all three bins;
2. radial H(z) is slightly more discrepant, with the largest raw mismatch at z=0.61;
3. growth is too high at z=0.51 and z=0.61 relative to the compressed BOSS fσ8 values;
4. the most promising observational/theoretical improvement target is therefore the coupled late-time `H(z) + growth` evolution, not the standard ruler or transverse distance.

No parameter should be manually tuned to these three bins before the repeated RTK stationarity gate is closed; this document is a diagnostic for the next physics stage, not an instruction to data-tune the current minimum.
