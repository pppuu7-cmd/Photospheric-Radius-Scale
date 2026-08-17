# RTK vs LCDM observable fingerprint — matched current centers

Status: **validated theory-output diagnostic; not model selection**.

Provenance:
- GitHub Actions run: `32052144053`, attempt 3, success.
- Job: `95458439154`.
- RTK source checkout: `6787b3fb5ade2f16da0bedf020949127e712908f`.
- CLASS nonlocal upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`.
- Artifact: `9295645643`.
- Artifact ZIP SHA256: `7208e5eeab81feb744b0c5010b6795cd9ac677d789e60cd7c054a24c64ab7f12`.
- Primordial inputs use legacy-compatible `A_s` / `n_s` (not `A_s_ad` / `n_s_ad`).
- Exact requested P(k,z) outputs and drag-epoch parser are fail-closed.

Comparison semantics: each model is evaluated at its own current accepted center with the same frozen ultra precision and dense-z grid. Therefore residuals combine **model-sector physics + parameter retuning**. A separate cross-anchored diagnostic is required to isolate the model-sector contribution.

All values below are `RTK/LCDM - 1`, except the z=0 comoving-distance entry where both are zero and the stored diagnostic is absolute delta = 0.

## Geometry / standard ruler

| z | H/c fractional | D_M fractional |
|---:|---:|---:|
| 0.00 | +0.0182154 | 0 absolute |
| 0.38 | +0.00250490 | -0.00940784 |
| 0.51 | -0.000204580 | -0.00750727 |
| 0.61 | -0.00165146 | -0.00631566 |
| 1.00 | -0.00401159 | -0.00327807 |

`r_d` fractional difference: **-0.000426247** (-0.0426%).

## Lensed CMB selected multipoles

| ell | TT fractional | EE fractional |
|---:|---:|---:|
| 30 | -0.000530074 | +0.00154864 |
| 100 | -0.000727397 | +0.00161996 |
| 500 | -0.000140650 | -0.000448525 |
| 1000 | -0.000145565 | -0.0000676416 |
| 2000 | -0.000868638 | -0.00145862 |

The sampled CMB fingerprint is sub-percent and mostly sub-0.2%, while LSS differences are much larger.

## Linear matter power P(k,z)

| z | k=0.01 | 0.05 | 0.10 | 0.20 | 0.50 h/Mpc |
|---:|---:|---:|---:|---:|---:|
| 0.00 | +5.997% | +4.181% | +2.764% | +2.125% | +1.856% |
| 0.38 | +6.321% | +4.496% | +3.077% | +2.451% | +2.275% |
| 0.61 | +6.274% | +4.448% | +3.031% | +2.406% | +2.241% |
| 1.00 | +6.069% | +4.245% | +2.830% | +2.207% | +2.048% |

## Growth

| z | fσ8 eff | fσ8 k01 | σ8 |
|---:|---:|---:|---:|
| 0.38 | +1.458% | +1.473% | +1.520% |
| 0.51 | +1.747% | +1.755% | +1.514% |
| 0.61 | +1.886% | +1.891% | +1.498% |

## Scientific interpretation boundary

The strongest provisional discriminant is currently linear LSS/growth, not primary CMB or the drag ruler. These values are **not** evidence, significance, preference, or a statement that RTK predicts more clustering at fixed primordial/shared parameters; matched-center retuning is mixed into the result. The cross-anchored calculation must be consulted for that decomposition.
