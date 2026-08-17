# RT auxiliary background-IC A/B equivalence

Date: 2026-08-18

Status: **source defect fixed for future runs; historical score interpretation preserved by exact A/B control.**

## Defect

Pinned upstream `dirian/class_public` commit

`36cf283628c4a3330ec9fd3d84239bf775f77317`

contains the background nonlocal auxiliary initial-condition block

```
U = 0
U' = 0
V = 0
U' = 0
```

rather than explicitly assigning `V' = 0` in the fourth line. `background.c` later consumes `V_prime_ini_nlde`, so this is an initialization/reproducibility defect.

The research patch `rtk/upgrade_rtk_nonlocal_initial_conditions.py` changes only the duplicated fourth assignment to explicit `V_prime_ini_nlde = 0` and fails closed unless the exact audited upstream block is found.

## Exact A/B control

Workflow run: `32073306866` — success.

Job: `95521033176`.

Research checkout used by the run: `a216f0c6e8364e971c8f2f6042366178d022489b`.

Artifact: `rtk-nonlocal-ic-ab-control`.

Artifact ID: `9302567450`.

Artifact ZIP SHA256: `08d7f2f8dc6f5407c027bd0fccd23ff4c97277dd2e4aebf21939c7c11ceedc56`.

The two CLASS trees were identical except for the one-line explicit-zero `V_prime_ini_nlde` patch. Both used:

- CLASS upstream pinned SHA `36cf283628c4a3330ec9fd3d84239bf775f77317`;
- Pantheon SHA `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`;
- clipy-like `0.15`;
- NumPy `2.5.2`;
- SciPy `1.18.0`;
- Python `3.12.3`;
- verified Planck baseline SHA256 `0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6`;
- frozen `matched-ultra-linstep2+dense-BOSS` objective;
- the current RTK accepted center at the time of the control.

## Result

Old upstream-typo tree and explicit-zero tree both returned

`S_eff = 1050.302218098562`

and

`S_k01 = 1050.3024996184474`.

Reported fixed-minus-old deltas were exactly `0.0` for:

- `score_eff`;
- `score_k01`;
- Planck log likelihood;
- Pantheon chi-square;
- BOSS eff chi-square;
- BOSS k01 chi-square;
- drag sound horizon `r_d`.

`max_abs_component_delta = 0.0`.

## Interpretation

The source defect is real because the pinned C source leaves the field without the intended explicit assignment. However, on the audited runner/build and physical point, replacing it by the intended zero initial condition is **numerically identical in every reported observable/likelihood component**.

Therefore:

✅ historical matched scores need not be invalidated solely because of this source typo;

✅ the already-running Hessian that predates the source hardening remains numerically interpretable, subject to its ordinary stationarity/multiscale gates;

✅ all future RT production workers should nevertheless apply the explicit-zero patch, because depending on uninitialized storage is not an acceptable reproducibility contract.

The result does not prove that arbitrary nonzero `V'_ini` would be equivalent. It proves only equivalence of the historical runner behavior and the intended explicit-zero implementation at the audited frozen point.
