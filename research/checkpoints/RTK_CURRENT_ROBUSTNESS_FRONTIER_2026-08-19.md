# RTK current robustness frontier — 2026-08-19

Status: **CURRENT OVERRIDE FOR B4/B6/B9/B10 ROWS OF THE OLDER MASTER CLOSURE MATRIX.**

`research/state/current.json` remains authoritative for the frozen massless A1–A5 production objective. Live Actions monitoring is isolated on `rtk-runtime-state:research/runtime/active_runs_snapshot.json`. Detailed code/provenance findings are in `research/audits/RTK_CODE_LOGIC_AUDIT_2026-08-19.md`; current constructive theory is in `research/theory/ROUTE_B_THEORY_FRONTIER_2026-08-19.md`.

| Package | Current status | Evidence | Next earned gate |
|---|---|---|---|
| A1–A5 massless matched local chain | ✅ CLOSED local/reproducible | fresh-tree replay `32148894768`; LCDM `1049.966118347761`, RTK `1050.249912429787`, raw local delta `+0.2837940820259064` | no reinterpretation as global/model-selection evidence |
| B10 lambda-tail identifiability v1 | ✅ CLOSED | T1 `32240381293`, T2 `32244330691`, T3 `32252288173`; primary-artifact audit passed | none unless separately scoped protocol |
| B6 H(T)+AlterBBN v1 | ✅ CLOSED | extended H(T) `32284769820`; abundance continuation `32290608424`, artifact `9380003379`; primary-artifact audit passed | none for B6-v1 |
| B4 minimal neutrino — LCDM | ✅ CLOSED local multiscale subgate | base `32251647845`; half `32284521400`; both recenter-clear+PD; all exact points re-audited | paired replay only after RTK side earns accepted point |
| B4 minimal neutrino — RTK | 🟡 ACTIVE | negative-ray winner `S_eff=1050.5880475140204`; recentered base run `32290108210` still active | after completion parse **all** `points.jsonl`, including k01 Newton; only true improvement<=0.005 + PD earns half-scale |
| B9 fixed-center adapter/interface | ✅ PASS | run `32285180694`, artifact `9377441941`; provenance corrected; lensed-Cl and `phiphi` unit guards passed | paired reoptimization |
| B9 reoptimization — RTK | ✅ INTERIOR CANDIDATE, not minimum | run `32289834876`, artifact `9384705087`; true all-point min `S_B9=1059.2759492715309`; improvement `0.013230490875912437`; `boundary_axes=[]` | wait paired LCDM candidate; then freeze recenter targets before stationarity |
| B9 reoptimization — LCDM | 🟡 ACTIVE | paired run `32289834876`, LCDM job still active | exact trace/boundary audit after artifact |
| B9 calibration contract | ✅ AUDIT PASS | run `32302366002`, artifact `9383486257`; all four Planck products declare `A_planck` with split defaults `1.000442/1.0` | shared-`A_planck` variant preregistered; heavy run waits for certified B9-v1 centers |
| B9 nonlinear-lensing sensitivity | 🟡 PREREGISTERED ONLY | B9-v1 uses linear CLASS lensing; pinned solver supports Halofit while BOSS `pk.dat` remains linear | Halofit variant waits for certified B9-v1 centers |
| Route-B healthy-BPS completion route | 🟡 CONSTRUCTIVE, C7 not closed | exact rational pole family, pole/residue guard, z=3 two-crossover family, C8 design-window chain all machine-checked | off-shell/source mapping, tuned-family nonlinear constraints, FLRW/generic stability |
| C8 strong-coupling | 🟡 PARAMETRIC DESIGN CHAIN, not numerical closure | quadratic nonidentifiability + exact BPS cutoffs + `p_UV` accuracy window | map phenomenological `M_*,c_s,p_max,epsilon`; specialize full tuned cubic/higher-spatial interactions |

## Current B9 RTK candidate

`research/robustness/B9_RTK_REOPTIMIZATION_CANDIDATE_v1.json` records the all-points-audited candidate:

- `S_B9 = 1059.2759492715309`;
- baseline part `S_base_eff = 1050.253210640323`;
- standalone lensing `-2 log L = 9.022738631207893`;
- `lambda_D = 801437.5006766783`;
- `h = 0.6911020893447606`, `Ob = 0.04679736391039825`, `Om = 0.25226571239744694`;
- `As = 2.087516612980563e-9`, `ns = 0.9645408625912186`, `zre = 7.329114544599571`;
- maximum normalized coordinate `0.6476240339149215 < 0.97`, so the preregistered boundary guard passes.

This is an interior reoptimization candidate only. It is not a stationarity-certified B9 minimum and cannot yet define a paired `Delta S_B9`.

## Mandatory guard corrections

- B9 fixed-center persisted metadata was corrected against primary artifact `9377441941`; cosmological fixed-center scores were unchanged.
- `B9_BOUNDARY_INTERPRETATION_GUARD_v1.md` forbids treating boundary optimizer endpoints as interior stationarity candidates.
- `B9_LENSED_CL_INTERFACE_GUARD_v1.md` confirms ordinary non-marginalized Planck lensing uses lensed CMB `Cl`, and the pinned CLASS `phiphi` class-format conversion is exactly inverted by the adapter.
- `B9_PLANCK_CALIBRATION_INTERPRETATION_GUARD_v1.md` records that A5/B9-v1 are conditional on each product's distributed `A_planck` default; `B9_SHARED_APLANCK_PROFILE_PROTOCOL_v1.md` separately preregisters a shared-calibration profile test.
- `B9_HALOFIT_LENSING_ROBUSTNESS_PROTOCOL_v1.md` separately preregisters nonlinear-lensing sensitivity; it must not overwrite B9-v1 post hoc.
- Historical B4 Hessian worker selected `eff.best_exact` before the later k01-Newton point existed. Commit `4d2416c02979650e48e8f53cf67da4ae07079992` fixes future runs; the active RTK run predates it, so all points must be rescanned manually before gating.
- The sparse Stage4D3 AI agent is retired/read-only; it cannot override dense production state.
- Runtime snapshots use dedicated branch `rtk-runtime-state`, preventing ephemeral monitoring from racing scientific commits.

## Interpretation boundaries

- B4 absolute scores belong to `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1` and are incomparable to massless A1–A5 absolute scores.
- B9-v1 belongs to `matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`; it is conditional on distributed Planck calibration defaults and linear CLASS lensing.
- No local optimizer, Hessian, raw score delta, abundance check or tail check establishes global optimality, significance, AIC/BIC preference, posterior preference or Bayes factor.
- C7 remains open on full coupled nonlinear DOF/constraint closure and observable mapping. C8 remains open on an actual selected-family numerical cutoff. C9 radiative/quantum stability remains open.
