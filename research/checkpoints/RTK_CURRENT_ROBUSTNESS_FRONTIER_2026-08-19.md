# RTK current robustness frontier — 2026-08-19

Status: **CURRENT OVERRIDE FOR B4/B6/B9/B10 ROWS OF THE OLDER MASTER CLOSURE MATRIX.**

The older `research/RTK_MASTER_RESEARCH_CLOSURE_MATRIX.md` is historically useful but its B4/B6/B9/B10 rows lag the completed artifacts below. For these packages, this checkpoint plus the package-specific result/protocol files is the current human-readable frontier. `research/state/current.json` remains authoritative for the frozen massless A1–A5 production objective. Live Actions monitoring is isolated on `rtk-runtime-state:research/runtime/active_runs_snapshot.json` so ephemeral runtime writes cannot race durable research commits.

| Package | Current status | Evidence | Next earned gate |
|---|---|---|---|
| A1–A5 massless matched local chain | ✅ CLOSED local/reproducible | fresh-tree replay `32148894768`; LCDM `1049.966118347761`, RTK `1050.249912429787`, raw local delta `+0.2837940820259064` | no reinterpretation as global/model-selection evidence |
| B10 lambda-tail identifiability v1 | ✅ CLOSED | T1 `32240381293`, T2 `32244330691`, T3 `32252288173`; both tail anchors stationarity-certified and within `0.005` of finite RTK; primary-artifact audit passed | none unless a separately scoped protocol is introduced |
| B6 BBN H(T) mapping | ✅ CLOSED | extended mapping `32284769820`, artifact `9377196879`; max `|R_H-1|=2.422446243599552e-09` | abundance gate completed below |
| B6 AlterBBN abundances | ✅ CLOSED | continuation `32290608424`, artifact `9380003379`, digest `sha256:3961ff52803574d3389111dc93fc5dcf843c463a54968f4d75c7e0c909ac6dca`; all six networks complete; primary-artifact audit passed | none for B6-v1 |
| B4 minimal neutrino — LCDM | ✅ CLOSED local multiscale subgate | base `32251647845`; half `32284521400`; both recenter-clear and PD; all 75 exact points at each scale re-audited after worker order-dependence discovery | paired replay only after RTK side earns an accepted point |
| B4 minimal neutrino — RTK | 🟡 ACTIVE | first recenter `32252398625` non-PD; negative rays `32284932113` found real descent; exact ray winner `S_eff=1050.5880475140204`; base recenter run `32290108210` active | parse **all** points including k01 Newton; only true recenter-clear + PD may earn half-scale |
| B9 Planck standalone lensing adapter | ✅ STEP-1 PASS | fixed-center run `32285180694`, artifact `9377441941`; provenance corrected against primary artifact; lensed-Cl and phiphi-unit interface guards passed | paired reoptimization active |
| B9 paired reoptimization v1 | 🟡 ACTIVE | run `32289834876`, independent LCDM 6D and RTK 7D jobs | consume exact candidates; boundary guard before Hessian; then base+half stationarity and fresh-tree replay |
| B9 Planck calibration contract | ✅ AUDIT PASS | run `32302366002`, artifact `9383486257`; all four project Planck products declare `A_planck`, with distributed defaults split between `1.000442` and `1.0` | shared-`A_planck` profile variant preregistered, heavy run waits for B9-v1 certified centers |
| Route-B reduced scalar kinematics | ✅ NARROW LEMMA | run `32302480967`, artifact `9383521326`; exact omega/phase/group-velocity relations verified | full coupled C7 characteristic/constraint theorem remains open |

## Current guard corrections

- `research/robustness/B9_FIXED_CENTER_LENSING_RESULT_v1.json` was corrected against primary artifact `9377441941`: the previous hand-persisted artifact digest, run timestamps and default-vector selfcheck were wrong. The cosmological LCDM/RTK fixed-center scores and raw diagnostic delta were unchanged at the precision relevant to B9 progression.
- `research/robustness/B9_BOUNDARY_INTERPRETATION_GUARD_v1.md` fail-closes optimizer boundary candidates: no boundary endpoint may be treated as an interior stationarity candidate. Shared-parameter boundaries require same-width translated reoptimization; an RTK-only `loglambda` boundary requires a B9-specific tail/profile protocol rather than importing B10 from a different objective.
- `research/robustness/B9_LENSED_CL_INTERFACE_GUARD_v1.md` confirms from official Cobaya+CLASS semantics that the ordinary non-CMB-marginalized lensing clik consumes the standard lensed `Cl` theory product; the pinned CLASS source also proves class-format `phiphi = l(l+1) C_l^{phiphi}/(2pi)`, so the adapter's division recovers raw `C_l^{phiphi}` exactly.
- `research/robustness/B9_PLANCK_CALIBRATION_INTERPRETATION_GUARD_v1.md` records that A5/B9-v1 are **conditional on each product's distributed `A_planck` default**, not a single shared nuisance profile. `B9_SHARED_APLANCK_PROFILE_PROTOCOL_v1.md` preregisters the separate shared-calibration profile test with one Gaussian prior contribution.
- B9-v1 enables CLASS lensing but no nonlinear method. The pinned RT-CLASS supports `halofit`, while its `pk.dat` writer explicitly requests the linear spectrum for BOSS growth. `B9_HALOFIT_LENSING_ROBUSTNESS_PROTOCOL_v1.md` preregisters a separate nonlinear-lensing sensitivity test without changing B9-v1 post hoc.
- Historical B4 `neutrino_stationarity_hessian.py` selected the production best before the later k01-Newton point existed. Worker commit `4d2416c02979650e48e8f53cf67da4ae07079992` makes selection order-independent. Historical LCDM base/half artifacts were rescanned across all exact points and closure survives; active RTK run predates the fix and must be rescanned manually from `points.jsonl`.
- The historical `main:rtk/agent/frontier_state.json` contains the sparse Stage4D3 score `1050.0338294787366` and is explicitly stale. Its automatic AI-agent workflow has been retired from schedule/workflow-run triggers and reduced to read-only manual fail-closed behavior. It cannot override the dense production state.
- Production-branch CLASS smoke failures seen on result/provenance commits were a CI harness defect (`output/` absent before stock parser smoke), not a source regression. The smoke now creates the directory and automatic builds are path-scoped to actual Khronon C/H changes.
- Runtime snapshots no longer write `rtk-class-build`; dedicated branch `rtk-runtime-state` isolates ephemeral Actions state from durable scientific commits.
- Detailed defect/provenance history is checkpointed in `research/audits/RTK_CODE_LOGIC_AUDIT_2026-08-19.md`.

## Interpretation boundaries

- B4 absolute scores belong to `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1` and must not be numerically compared to the massless A1–A5 objective.
- B9-v1 belongs to `matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`; its fixed-center diagnostic is not a reoptimized comparison. B9-v1 is conditional on distributed calibration defaults and on linear CLASS lensing.
- The separately preregistered shared-`A_planck` and Halofit variants are robustness extensions, not repairs that overwrite B9-v1. A later combined variant, if earned, must be preregistered separately rather than inferred by adding score shifts.
- No local optimizer, Hessian, raw score delta, B6 abundance check or B10 tail check establishes a global optimum, significance, AIC/BIC preference, posterior preference or Bayes factor.
- Fundamental C7/C8/C9 questions remain open: full coupled nonlinear DOF/constraint theorem, strong-coupling cutoff, and radiative/quantum stability.
