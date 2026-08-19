# RTK current robustness frontier — 2026-08-19

Status: **CURRENT OVERRIDE FOR B4/B6/B9/B10 ROWS OF THE OLDER MASTER CLOSURE MATRIX.**

The older `research/RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` is historically useful but its B4/B6/B9/B10 rows lag the completed artifacts below. For these packages, this checkpoint plus the package-specific result/protocol files is the current human-readable frontier. `research/state/current.json` remains authoritative for the frozen massless A1–A5 production objective.

| Package | Current status | Evidence | Next earned gate |
|---|---|---|---|
| A1–A5 massless matched local chain | ✅ CLOSED local/reproducible | fresh-tree replay `32148894768`; LCDM `1049.966118347761`, RTK `1050.249912429787`, raw local delta `+0.2837940820259064` | no reinterpretation as global/model-selection evidence |
| B10 lambda-tail identifiability v1 | ✅ CLOSED | T1 `32240381293`, T2 `32244330691`, T3 `32252288173`; both tail anchors stationarity-certified and within `0.005` of finite RTK | none unless a separately scoped protocol is introduced |
| B6 BBN H(T) mapping | ✅ CLOSED | extended mapping `32284769820`, artifact `9377196879`; max `|R_H-1|=2.422446243599552e-09` | abundance gate completed below |
| B6 AlterBBN abundances | ✅ CLOSED | continuation `32290608424`, artifact `9380003379`, digest `sha256:3961ff52803574d3389111dc93fc5dcf843c463a54968f4d75c7e0c909ac6dca`; all six networks complete | none for B6-v1 |
| B4 minimal neutrino — LCDM | ✅ CLOSED local multiscale subgate | base `32251647845`; half `32284521400`, artifact `9380579980`; both recenter-clear and PD | paired replay only after RTK side earns an accepted point |
| B4 minimal neutrino — RTK | 🟡 ACTIVE | first recenter `32252398625` non-PD; negative rays `32284932113` found real descent; new exact winner `S_eff=1050.5880475140204`; base recenter run `32290108210` active | inspect base; only if recenter-clear + PD may half-scale run |
| B9 Planck standalone lensing adapter | ✅ STEP-1 PASS | fixed-center run `32285180694`, artifact `9377441941`; corrected primary digest `sha256:4917318ec0f20a4060e4d158dae4a3b861dcdf616f6f378d62ddf0e23de89917` | paired reoptimization active |
| B9 paired reoptimization | 🟡 ACTIVE | run `32289834876`, independent LCDM 6D and RTK 7D jobs | consume exact candidates; boundary guard before any Hessian; then base+half stationarity and fresh-tree replay |

## Current guard corrections

- `research/robustness/B9_FIXED_CENTER_LENSING_RESULT_v1.json` was corrected against primary artifact `9377441941`: the previous hand-persisted artifact digest, run timestamps and default-vector selfcheck were wrong. The cosmological LCDM/RTK fixed-center scores and raw diagnostic delta were unchanged at the precision relevant to B9 progression.
- `research/robustness/B9_BOUNDARY_INTERPRETATION_GUARD_v1.md` fail-closes optimizer boundary candidates: no boundary endpoint may be treated as an interior stationarity candidate. Shared-parameter boundaries require same-width translated reoptimization; an RTK-only `loglambda` boundary requires a B9-specific tail/profile protocol rather than importing B10 from a different objective.
- The historical `main:rtk/agent/frontier_state.json` contains the sparse Stage4D3 score `1050.0338294787366` and is explicitly stale. Its automatic AI-agent workflow has been retired from schedule/workflow-run triggers and reduced to read-only manual fail-closed behavior. It cannot override the dense production state.
- Production-branch CLASS smoke failures seen on result/provenance commits were a CI harness defect (`output/` absent before stock parser smoke), not a source regression. The smoke now creates the directory and automatic builds are path-scoped to actual Khronon C/H changes.

## Interpretation boundaries

- B4 absolute scores belong to `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1` and must not be numerically compared to the massless A1–A5 objective.
- B9 belongs to `matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1` and its fixed-center diagnostic is not a reoptimized comparison.
- No local optimizer, Hessian, raw score delta, B6 abundance check or B10 tail check establishes a global optimum, significance, AIC/BIC preference, posterior preference or Bayes factor.
- Fundamental C7/C8/C9 questions remain open: full coupled nonlinear DOF/constraint theorem, strong-coupling cutoff, and radiative/quantum stability.
