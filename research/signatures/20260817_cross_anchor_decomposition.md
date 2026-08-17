# RTK vs LCDM cross-anchored observable decomposition

Status: **validated theory-output diagnostic; not model selection**.

## Provenance

- GitHub Actions run: `32054061956`, success.
- Job: `95460035790`.
- RTK source checkout: `f1f3dd7c0261ac83fb7ebb51a06ca2ae64e18062`.
- CLASS nonlocal upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`.
- Artifact: `9295856434`.
- Artifact ZIP SHA256: `939cf617b1a1c0b42c0beefddc7a169bbfa4a1c106b522ca5c44cac8cda9f397`.
- Standalone CLASS inputs use legacy-compatible `A_s` / `n_s`.
- Exact requested P(k,z) and drag-epoch extraction are fail-closed.

## Method

Within each anchor, RTK and LCDM are forced to use identical shared cosmological parameters
`As, Ob, Om, h, ns, zre`. RTK alone uses the current accepted `lambda_D = 217644.75828347108`.
Two anchors were used:

1. RTK-center anchor: shared parameters fixed to the current RTK accepted center.
2. LCDM-center anchor: shared parameters fixed to the current LCDM accepted center.

Therefore these residuals isolate the **model-sector switch** much more directly than the matched-current-centers comparison, which mixes model physics with parameter retuning.

All fractional values are `RTK/LCDM - 1`.

## Geometry

| anchor | z | H/c | D_M |
|---|---:|---:|---:|
| RTK center | 0.38 | -0.9954% | +0.5861% |
| RTK center | 0.51 | -1.1057% | +0.6963% |
| RTK center | 0.61 | -1.1417% | +0.7589% |
| RTK center | 1.00 | -1.0628% | +0.8809% |
| LCDM center | 0.38 | -0.9743% | +0.5759% |
| LCDM center | 0.51 | -1.0782% | +0.6824% |
| LCDM center | 0.61 | -1.1106% | +0.7426% |
| LCDM center | 1.00 | -1.0265% | +0.8579% |

At z=0 the H residual is numerically consistent with zero because h is held identical. The intrinsic drag-ruler change is only about `-1.1e-6`, i.e. negligible at this anchor precision.

## CMB selected multipoles

### RTK-center anchor

| ell | TT | EE |
|---:|---:|---:|
| 30 | -0.405% | -1.429% |
| 100 | -0.504% | -0.797% |
| 500 | -0.661% | +2.660% |
| 1000 | +0.778% | +0.543% |
| 2000 | -0.065% | +5.127% |

### LCDM-center anchor

| ell | TT | EE |
|---:|---:|---:|
| 30 | -0.338% | -1.385% |
| 100 | -0.493% | -0.780% |
| 500 | -0.670% | +2.666% |
| 1000 | +0.946% | +0.308% |
| 2000 | -0.081% | +4.578% |

The qualitative pattern is stable under changing the anchor. This is important: at fixed shared parameters the RTK sector produces percent-level CMB changes, especially in EE, whereas at separately retuned matched centers the sampled CMB residuals are mostly below 0.2%. The fit therefore uses parameter shifts to cancel a substantial intrinsic CMB signature.

## Linear matter power

### RTK-center anchor

| z | k=0.01 | 0.05 | 0.10 | 0.20 | 0.50 h/Mpc |
|---:|---:|---:|---:|---:|---:|
| 0.00 | +2.391% | +2.402% | +2.399% | +2.383% | +2.271% |
| 0.38 | +2.074% | +2.082% | +2.082% | +2.079% | +2.062% |
| 0.61 | +1.774% | +1.780% | +1.781% | +1.780% | +1.773% |
| 1.00 | +1.303% | +1.307% | +1.308% | +1.307% | +1.306% |

### LCDM-center anchor

| z | k=0.01 | 0.05 | 0.10 | 0.20 | 0.50 h/Mpc |
|---:|---:|---:|---:|---:|---:|
| 0.00 | +2.321% | +2.332% | +2.330% | +2.315% | +2.214% |
| 0.38 | +2.006% | +2.014% | +2.015% | +2.012% | +1.996% |
| 0.61 | +1.711% | +1.717% | +1.718% | +1.717% | +1.711% |
| 1.00 | +1.252% | +1.256% | +1.257% | +1.256% | +1.255% |

This signal is extremely stable between the two anchors. At fixed shared parameters, the model-sector switch alone generates an approximately scale-flat ~1.3--2.4% enhancement over k=0.01--0.5 h/Mpc, with the amplitude growing toward low redshift.

The previously validated matched-current-centers comparison showed a much more scale-dependent +2--6% enhancement. Therefore parameter retuning supplies a large fraction of the extra low-k tilt, while the ~2% late-time power enhancement itself is intrinsic to the current RTK sector.

## Growth

| anchor | z | fσ8 eff | fσ8 k01 | σ8 |
|---|---:|---:|---:|---:|
| RTK center | 0.38 | +2.233% | +2.247% | +1.034% |
| RTK center | 0.51 | +2.262% | +2.270% | +0.951% |
| RTK center | 0.61 | +2.226% | +2.232% | +0.886% |
| LCDM center | 0.38 | +2.173% | +2.186% | +1.001% |
| LCDM center | 0.51 | +2.195% | +2.202% | +0.919% |
| LCDM center | 0.61 | +2.157% | +2.161% | +0.855% |

The growth residual is also stable under anchor choice. Thus the current ~2% `fσ8` shift is predominantly a model-sector effect rather than an artifact of best-fit parameter displacement.

## Main scientific result

The present RTK/LCDM degeneracy has a clear structure:

- **Primary/linear CMB:** intrinsic percent-level differences can be largely cancelled by retuning standard cosmological parameters.
- **Drag ruler:** essentially unchanged at fixed shared parameters.
- **Late-time geometry:** intrinsic ~0.6--1.1% differences remain.
- **Linear power and growth:** intrinsic late-time enhancement remains at ~1--2.4%, robust to the choice of shared-parameter anchor.
- **Matched-center low-k power:** parameter retuning adds a further scale-dependent tilt, raising the total difference to as much as ~6%.

This points to joint late-time geometry + scale-resolved LSS/growth as the most promising falsification channel. These residuals are not evidence, significance, preference, or a substitute for a survey-window RSD likelihood.
