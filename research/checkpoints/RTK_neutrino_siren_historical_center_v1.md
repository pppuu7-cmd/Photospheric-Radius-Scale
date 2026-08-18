# RTK neutrino + standard-siren historical-center checkpoint v1

Status: reproducible diagnostic evidence, **not a final-center prediction**.

## Provenance / center freshness

Both diagnostics below were evaluated from `research/state/current.json` at **state iteration 52**, with the then-axis-certified RTK center

```text
As   = 2.0872356834621613e-09
Ob   = 0.046795335641066506
Om   = 0.2523064029808687
h    = 0.6910694838209896
lam  = 219968.33239135708
ns   = 0.9646445048182237
zre  = 7.319677519287684
```

The matched RTK search subsequently recentered. Therefore these artifacts are retained as historical-center robustness/signature evidence and **must be replayed at the finally certified RTK center before any final numerical claim**.

Frozen scalar objective remained `matched-ultra-linstep2+dense-BOSS`; these diagnostics do not replace or modify it.

## Minimal-neutrino fixed-center robustness

GitHub Actions run: `32083374097` — success.

Artifact: `rtk-neutrino-mass-robustness`, artifact id `9306029433`, digest
`sha256:4e42969a70a4e0438a546d525e347deefebcb5eccdb3e8c175a7e5c77d467582`.

Research-source SHA recorded by artifact: `1a7dc0c1ac545859d8d461496fe75226b88f6cf3`.

Pinned environment in workflow includes CLASS `36cf283628c4a3330ec9fd3d84239bf775f77317`, Pantheon `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`, Planck archive SHA256 `0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6`, NumPy `2.5.2`, SciPy `1.18.0`.

The massless baseline was exactly reproduced within the workflow tolerance. Fixed-center `S_RTK-S_LCDM` values were:

| mode | eff delta S | k01 delta S |
|---|---:|---:|
| massless | +0.3088895888447496 | +0.30912973621661877 |
| mnu=0.06 eV, additive density | -0.8011517660384015 | -0.8001301343090290 |
| mnu=0.06 eV, fixed total non-baryonic density | -1.4661434588947486 | -1.4653224821468030 |

Interpretation boundary: this demonstrates substantial **fixed-center sensitivity** of the RTK-vs-LCDM raw-score difference to the standard neutrino-sector assumption. It is not a reoptimized massive-neutrino comparison and is not model-selection evidence. A matched reoptimization would be needed for a massive-neutrino model comparison.

## Standard-siren / tensor-friction diagnostic

GitHub Actions run: `32083365308` — success.

Artifact: `rtk-current-standard-siren`, artifact id `9305829506`, digest
`sha256:5a6580a4b1ccb027b4f2e928acb46fa6020fc126055998a10b565700c369d374`.

Research-source SHA recorded by artifact: `1a7dc0c1ac545859d8d461496fe75226b88f6cf3`.

For the implemented prediction prescription the artifact records

```text
c_gw / c = 1
gamma = 0.05170298355873
h'' + [2 a H - 3 H0^2 gamma V] h' + k^2 h = source
```

and defines

```text
delta = 3 H0^2 gamma V / (2 a H)
dL_GW/dL_EM = exp[- integral_0^z delta(z)/(1+z) dz]
```

Historical-center values:

| z | dL_GW/dL_EM | fractional difference |
|---:|---:|---:|
| 0.10 | 0.9866962832 | -1.3304% |
| 0.38 | 0.9636162417 | -3.6384% |
| 0.51 | 0.9571954009 | -4.2805% |
| 0.61 | 0.9533862641 | -4.6614% |
| 1.00 | 0.9442313568 | -5.5769% |
| 2.00 | 0.9366123295 | -6.3388% |
| 5.00 | 0.9337078309 | -6.6292% |

This is a potentially distinctive amplitude-distance signature of the implemented tensor-friction prescription while maintaining luminal tensor propagation. It is **prediction-only**: not a GW likelihood, not a new fit, and not a claim that the primordial/nonlinear tensor sector is complete.

## Closure status

- ✅ Neutrino diagnostic workflow repaired and successful.
- ✅ Massless baseline reproduced in the robustness workflow.
- ✅ Two explicit 0.06 eV fixed-center neutrino conventions evaluated.
- ✅ Standard-siren tensor-friction diagnostic successfully evaluated with `c_gw/c=1`.
- ✅ Artifact IDs/digests and research-source SHA retained here.
- 🟡 Numerical values correspond to historical state iteration 52, not the later recentered RTK state.
- 🔴 Replay both diagnostics at the finally Stage-4D3-certified RTK center.
- 🔴 Massive-neutrino matched reoptimization is not performed and must not be inferred from this fixed-center test.
- 🔴 No standard-siren likelihood / observational constraint has been applied.
- 🔴 No all-order or complete primordial tensor-sector claim follows from this diagnostic.
