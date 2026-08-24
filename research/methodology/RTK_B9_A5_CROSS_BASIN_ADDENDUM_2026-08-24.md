# RTK B9 / A5 cross-basin live methodology addendum — 2026-08-24

Status: **CURRENT LIVE ADDENDUM**  
Canonical B9 state: `research/state/B9_current.json`  
Baseline global state: `research/state/current.json`  
B9 base methodology: `research/methodology/B9_LIVE_RECOVERY_METHOD.md`

## 1. Why this addendum exists

During continuation of the B9 Planck-lensing robustness chain, the exact center rows from already validated B9 stationarity artifacts were inspected component-by-component. This exposed a new issue that is logically distinct from B9 itself: the final B9 LCDM-v7 center appears to have a substantially lower value of the **unchanged baseline A5 objective** than the historical A5 LCDM accepted local minimum.

This is not yet allowed to supersede A5 because the observation came from B9 artifacts. An independent fresh-tree baseline-only four-point replay has therefore been preregistered and launched before any baseline recentering conclusion is accepted.

## 2. Exact B9 decomposition at the current local centers

The frozen B9 score is

`S_B9(theta) = S_A5(theta) - 2 log L_lensing(theta)`.

At the RTK recentered B9 point, run `32518496348`, artifact `9464480301` gives the exact center row:

- `S_A5,RTK(B9-center) = 1050.2560245726381`
- `log L_lensing,RTK = -4.507965372437646`
- `-2 log L_lensing,RTK = 9.015930744875291`
- `S_B9,RTK = 1059.2719553175134`
- baseline components: `logL_planck=-501.5166012679034`, `chi2_SN=39.60219024877595`, `chi2_BOSS_eff=7.620631788055366`, `rd=146.990401`.

At the LCDM-v7 point, run `32657629806`, artifact `9499099343` gives:

- `S_A5,LCDM(B9-center) = 1049.400976604194`
- `log L_lensing,LCDM = -4.408182903642276`
- `-2 log L_lensing,LCDM = 8.816365807284551`
- `S_B9,LCDM = 1058.2173424114785`
- baseline components: `logL_planck=-501.7107533611436`, `chi2_SN=39.6159823431352`, `chi2_BOSS_eff=6.363487538771697`, `rd=147.129323`.

Therefore the provisional current B9 difference decomposes exactly as

`Delta S_B9 = Delta S_A5(at B9 centers) + Delta[-2 log L_lensing]`

with

- `Delta S_A5(at B9 centers) = 1050.2560245726381 - 1049.400976604194 = +0.8550479684441`;
- `Delta[-2 log L_lensing] = 9.015930744875291 - 8.816365807284551 = +0.199564937590740`;
- total `Delta S_B9 = +1.0546129060349`.

Thus the direct standalone-lensing term accounts for only about `0.199565` of the current local B9 gap; most of the gap is already present in the baseline objective evaluated at the B9-reoptimized centers.

## 3. Comparison with the historical frozen A5 local pair

Historical fresh-tree replay-certified A5 scores:

- `S_A5,RTK(old) = 1050.249912429787`;
- `S_A5,LCDM(old) = 1049.966118347761`;
- historical local `Delta S_A5 = +0.2837940820259064`.

At the B9 centers the baseline difference becomes `+0.8550479684441`, a change of

`+0.5712538864181`.

The individual baseline movements are strongly asymmetric:

### LCDM

`S_A5,LCDM(B9-center) - S_A5,LCDM(old) = -0.565141743567`.

Component changes, B9-center minus historical A5 center:

- Planck contribution `-2 logL_planck`: `-0.06105919676108`;
- Pantheon `chi2_SN`: `-0.1399564911825`;
- BOSS `chi2_BOSS_eff`: `-0.364126055623454`;
- total: `-0.565141743567034`.

All three baseline data components improve simultaneously at this new LCDM point. That makes a simple lensing-versus-baseline trade-off an inadequate explanation.

### RTK

`S_A5,RTK(B9-center) - S_A5,RTK(old) = +0.0061121428511`.

Component changes:

- Planck contribution `+0.008776102471`;
- Pantheon `+0.00319628073072`;
- BOSS `-0.005860240350449`;
- total `+0.006112142851271`.

The RTK B9 center is therefore almost baseline-neutral relative to the historical RTK A5 local point, whereas the LCDM B9 center is much better on the baseline objective.

## 4. Scientific interpretation and guard

The observation above is **not yet a replacement A5 result**. It establishes a concrete cross-basin hypothesis:

> The B9 reoptimization may have discovered a deeper LCDM basin of the already-frozen `matched-ultra-linstep2+dense-BOSS` objective that the original local A5 stationarity chain did not search.

This does not invalidate the historical A5 local Hessian/stationarity theorem at its own center. It would, if independently reproduced, mean that the historical A5 pair should be described as an older local-basin comparison rather than the best currently known local pair.

No global-minimum claim is authorized in either case.

## 5. Independent A5/B9 cross-basin replay gate

Frozen target:

`research/robustness/A5_B9_CROSS_BASIN_REPLAY_TARGET_v1.json`

Target commit:

`e77c71d594772518611e1c1196d8777dc16fa1b4`

Worker:

`rtk/a5_b9_cross_basin_replay.py`

Worker commit:

`f9788b991a43985a1623828c2b29db96bc665da8`

Main workflow:

`.github/workflows/rtk-a5-b9-cross-basin-replay.yml`

Workflow commit:

`d759a2fbf7497c87cc4ada026e7f7b0b9f95a3e6`

Trigger commit:

`7fa310f17719827681e44cd2608db056aa64a244`

The audit evaluates exactly four points in one freshly rebuilt pinned environment:

1. historical A5 LCDM center;
2. historical A5 RTK center;
3. B9-v7 LCDM center with the standalone lensing term removed;
4. B9 RTK recentered point with the standalone lensing term removed.

All four expected baseline scores must replay within `2e-6`, and the objective fingerprint must remain

`754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`.

Only if the independent replay confirms

`S_A5,LCDM(old) - S_A5,LCDM(B9-seed) > 0.005`

may the new LCDM point advance to a baseline stationarity/reoptimization chain.

## 6. Conditional LCDM baseline stationarity gate already frozen

Before seeing the independent cross-basin replay result, the response to a confirmed lower LCDM basin was frozen in

`research/robustness/A5_LCDM_B9_SEED_STATIONARITY_TARGET_v1.json`

commit

`e3cfab8793a816bbd3026d62ce0b5b33aa133ade`.

Its center is exactly the B9 LCDM-v7 point, but the objective is the original baseline objective with no standalone lensing term.

Base steps are the same six-dimensional local geometry used for the controlled LCDM stationarity audits:

- `delta h = 0.00035`;
- `delta Omega_b = 0.00007`;
- `delta Omega_m = 0.0007`;
- `delta A_s = 4e-12`;
- `delta n_s = 0.00035`;
- `delta z_re = 0.07`.

Frozen rules:

- exact improvement `>0.005` -> mandatory recenter;
- recenter-clear + PD base Hessian -> independent half-scale Hessian at the unchanged center;
- recenter-clear + non-PD -> preregister exact eigenmode rays before any fallback;
- half-scale recenter-clear + PD -> fresh-tree replay before superseding historical A5.

Worker:

`rtk/a5_lcdm_b9_seed_stationarity.py`, commit `6b55f5fe36a2c03508d337394dded35a82fd29d8`.

Main workflow:

`.github/workflows/rtk-a5-lcdm-b9-seed-stationarity.yml`.

The workflow scale-directory guard was corrected before any scientific run; corrected workflow commit:

`86659b167d2a12039a0384421b381d853957129e`.

A workflow-run router committed at `799f62e02378219f7fa4fb3ccbe88787241c90cf` dispatches scale `1.0` only after the independent cross-basin result is persisted with classification `A5_B9_CROSS_BASIN_REPLAY_PASS_NEW_LCDM_SEED_CONFIRMED`.

## 7. B9 computation chain now armed

The B9 RTK fresh-tree gate is triggered from `main`, where the historical trigger route is known to exist, while the compute step explicitly checks out `rtk-class-build`.

Main trigger commit:

`58d6e9943bc753eda2ebbcc58fe7a5bbe88aa482`.

A `workflow_run` router on `main` persists the result into `rtk-class-build`. On scientific PASS only, it dispatches the already-preregistered final paired B9 exact replay. On a non-success workflow conclusion it records infrastructure/run state without manufacturing a scientific FAIL.

Router commit:

`db13e0e5a3a938240adbe0946642b31d6f91305a`.

Final paired worker:

`rtk/b9_final_paired_replay.py`, commit `3edcd6fed40e599ed785138af40a0154b8d0957d`.

Final paired workflow:

`.github/workflows/rtk-b9-final-paired-replay.yml`, commit `412565dbfbed84f8f2a441476bff7b00315c3184`.

Its target was frozen before the RTK fresh-tree result:

`research/robustness/B9_FINAL_PAIRED_REPLAY_TARGET_v1.json`.

Final B9 `Delta S` remains provisional until that paired replay passes.

## 8. Recovery order after chat loss

1. Read `research/state/B9_current.json`.
2. Read this addendum.
3. Read `research/methodology/B9_LIVE_RECOVERY_METHOD.md` for the full B9 equations and stationarity rules.
4. Check whether `research/robustness/B9_RTK_FRESH_TREE_CERTIFICATION_RESULT_v1.json` exists.
5. Check whether `research/robustness/B9_FINAL_PAIRED_REPLAY_RESULT_v1.json` exists.
6. Independently check whether `research/robustness/A5_B9_CROSS_BASIN_REPLAY_RESULT_v1.json` exists.
7. If the cross-basin classification confirms the new LCDM seed, inspect `research/state/A5_LCDM_cross_basin_stationarity_current.json` and follow the frozen base/half/ray/recenter decision tree.
8. Never use a launch/trigger commit as evidence that a scientific gate passed.

## 9. Current non-claims

- no global minimum is established for either model;
- the historical A5 local certificate is not erased by a different basin;
- the provisional B9 `Delta S=+1.0546129060349` is not final until independent paired replay;
- none of these raw score differences is a sigma significance or Bayes factor;
- the phenomenological `lambda_D` coordinate remains distinct from later fixed-action `lambda_HL` parameters.
