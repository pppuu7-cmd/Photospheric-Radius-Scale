# RTK Research Ledger

Version: 2026-08-21 14:25 UTC
Purpose: canonical current-frontier record independent of chat history.

Historical development belongs in `research/RTK_MODEL_CHRONOLOGY.md`; detailed formulas belong in the Formula Bible/index and named appendices. This ledger records the current scientific gates, evidence, exact run provenance and next action.

## Current frontier

| ID | Question | Current evidence | Status | Next mandatory gate |
|---|---|---|---|---|
| A1-A5 | Frozen matched dense cosmology | exact replay-certified local scores | GREEN local baseline | do not reinterpret as global evidence |
| B4 | Minimal-neutrino local robustness | target-v2 ray-recenter replay run `32482490823` is in exact base-Hessian step | YELLOW / running | inspect artifact; recenter/rays/half-scale per frozen tree |
| B6 | Primordial abundances | paired AlterBBN run `32285359564` attempt 2 | GREEN differential robustness | separate absolute BBN likelihood only if later preregistered |
| B9 | Planck lensing | fixed-center diagnostic passed; paired reoptimization run `32490152072` is executing RTK and LCDM | YELLOW / running | inspect both reoptimized artifacts, then stationarity/paired interpretation |
| B10 | lambda_D identifiability | base T3 passed at factors 64 and 16384; half-scale run `32482153752` executing both anchors | YELLOW / running | inspect both half-scale artifacts before tail/identifiability claim |
| C8 | UV/IR off-shell carrier | Schur/rank/q-residue algebra CI-verified; source-redefinition locality gate launched | YELLOW overall | derive M,J,K0 from one explicit fixed FLRW action and match source response |
| INFRA-HOME3 | Additional compute | 10-core/12-logical i5-1235U self-hosted node connected; v2.1 bootstrap queued as run `32487473962` | YELLOW / queued | let stale legacy jobs drain, then require 12-worker saturation/checkpoint PASS |

## Frozen production baseline

Objective:

`matched-ultra-linstep2+dense-BOSS`

Production mapping:

`eff`

Frozen exact local scores:

- LCDM: `S_eff = 1049.966118347761`
- RTK: `S_eff = 1050.249912429787`
- local raw-objective difference: `Delta S_eff = +0.2837940820259064`

Latest production iteration inspected:

- `rtk-class-build:research/iterations/000194_20260821T135112Z.json`
- iteration `194`
- action: `compute_matched_dense_raw_delta_S`

Iteration 194 only recomputed the already frozen local difference. It does not advance the physical frontier.

Guardrail: this is a local matched raw-objective comparison only, not a global optimum, posterior preference, significance, AIC/BIC or Bayes factor.

## B4 minimal-neutrino stationarity chain

Separate objective:

`matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`.

Never compare its absolute scores numerically with the massless A1-A5 objective.

First recentered RTK base Hessian run `32252398625` had three negative eigenvalues:

- `-0.0324084135524679`
- `-0.0015792056227914312`
- `-1.9922876135075676e-05`

Exact negative-mode ray run `32284932113` then confirmed real objective improvements. Strongest:

- mode `0`
- alpha `+2.0`
- parent `S_eff = 1050.6979573843187`
- ray winner `S_eff = 1050.5880475140204`
- improvement `0.10990987029822463 > 0.005`.

Frozen target-v2 parameters:

- `As=2.0920212896820786e-9`
- `Ob=0.04722200104991654`
- `Om=0.2528393318824633`
- `h=0.6885660022475836`
- `lambda_D=3043326.1774413693`
- `ns=0.9657332769496741`
- `zre=7.506210209218662`.

Canonical proof chain:

`research/robustness/RTK_B4_NEUTRINO_STATIONARITY_CHAIN_2026-08-21.md`.

Fresh target-v2 replay:

- run `32482490823`
- job `ray-recentered-base-hessian`
- setup, frozen target checks, hardened CLASS build and Planck verification passed
- exact RTK ray-recenter base Hessian step is/was the active scientific step at the last direct job check.

Decision rule remains mechanical: exact improvement >0.005 -> recenter; indefinite Hessian -> exact negative/near-zero-mode rays; positive-definite base -> half-scale; adjacent base+half -> fresh-tree replay; only then pair with the LCDM side.

Status: OPEN.

## B6 paired AlterBBN abundance gate — CLOSED DIFFERENTIAL ROBUSTNESS

Canonical result:

`research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.

Provenance:

- run `32285359564`, attempt 2
- artifact `9447623417`
- digest `sha256:d8cae8fbd36b886219b611603ef90852dff18251f93e020b0ab87c393e012287`.

Expansion perturbation:

`max |R_H-1| = 2.422446243599552e-09`.

Primary shifts:

- `delta Yp = +1.4314660568004456e-12`, resolved; conservative bound `1.5052958879380185e-12`
- `delta(D/H) = +1.6226982865047423e-15`, below preregistered numerical resolution; conservative bound `4.560750648668899e-15`.

Frozen standardized residual changes induced by RTK are only about `1.10e-9 sigma` for Yp and `6.76e-9 sigma` for D/H.

Scope boundary: the reference AlterBBN calculation itself is about `-4.706 sigma` from the frozen D/H central value if only the quoted observational sigma is used. Therefore B6 closes only the *differential RTK effect*. It is not an absolute BBN likelihood, lithium solution or model-evidence result.

## B9 Planck lensing

Fixed-center standalone diagnostic run `32285180694`:

- LCDM `-2 ln L = 9.054925581629908`
- RTK `-2 ln L = 9.039267332621456`
- RTK-LCDM fixed-center difference `-0.015658249008452`.

This fixed-center number is not a matched reoptimized result.

A frozen paired reoptimization has now been launched:

- run `32490152072`
- LCDM job `reoptimize (LCDM)`
- RTK job `reoptimize (RTK)`
- both jobs passed preregistered-target checks, hardened CLASS preparation/build and Planck R3 baseline verification
- at the last direct job check both were inside `Run exact B9 paired reoptimization`.

Status: OPEN/RUNNING. Do not use the fixed-center number for model-selection claims while the paired reoptimization is unresolved.

## B10 lambda_D tail / identifiability

Base T3 run `32252288173`:

Factor 64:

- `lambda_D = 14045284.653674118`
- `S_eff(center) = 1050.249062546245`
- exact stencil improvement `0`
- Hessian positive definite
- minimum eigenvalue approximately `0.046675`.

Factor 16384:

- `lambda_D = 3595592871.3405743`
- `S_eff(center) = 1050.2490169939647`
- exact stencil improvement `0`
- Hessian positive definite
- minimum eigenvalue approximately `0.046707`.

Base scale alone does not close B10.

Half-scale validation:

- run `32482153752`
- jobs `half-stationarity (64)` and `half-stationarity (16384)`
- both passed target checks, hardened CLASS setup/build and Planck verification
- at the last direct job check both were inside the exact fixed-lambda 6D half-scale stationarity step.

Acceptance requires center replay consistency, no exact improvement above `0.005`, positive-definite Hessian and qualitative base/half consistency. Only after both artifacts pass may a conservative tail-flatness/identifiability statement be made.

Status: OPEN/RUNNING.

## C8 fixed-action FLRW / off-shell carrier

### Established moving-pole theorem

`rtk-class-build:rtk/route_b_flrw_constraint_kernel.py` shows that a fixed healthy-Horava-style action can have an FLRW constraint kernel

`D_phi = 3(3 lambda-1)H^2 - eta p^2 - eta2 p^4/M_Pl^2 + eta4 p^6/M_Pl^4`,

so a constraint root can move with `H(a)` even when Wilson coefficients are fixed. Hence a fixed-Minkowski globalization obstruction does not by itself extend to FLRW.

This is structural only; it is not a full propagating/source map.

### Exact Schur/rank/q-residue algebra — CI VERIFIED

For two nondynamical variables,

`M=[[A,C],[C,B]]`, `J=(P,R)`,

exact elimination gives

`K_eff = K0 - (B P^2 - 2 C P R + A R^2)/(A B-C^2)`.

For `M(q)=M0+q M1`, strict nonconstant linear denominator requires

`det(M1)=0` and `M1 != 0`, hence for the real symmetric 2x2 case

`rank(M1)=1`.

The strengthened self-test is now independently artifact-verified:

- run `32490690248`
- artifact `9449602889`
- digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`
- artifact markers `C8_FLRW_SCHUR_SELFTEST_PASS` and `C8_FLRW_SCHUR_RANK_RESIDUE_SELFTEST_PASS`
- exact diagnostic example: `D0=2`, `D1=6`, `D2=0`, rank `1`, `q_pole=-1/3`, `Res_q[N/D]=+1/9`, Schur contribution residue `-1/9`.

Canonical CI result:

`research/RTK_C8_SCHUR_CI_RESULT_2026-08-21.md`.

These are q-plane reduced-coefficient residues, not physical `omega^2` propagator residues.

### Exact BPS pole embedding remains stronger than a no-go

`rtk-class-build:rtk/route_b_bps_target_inversion.py` constructs, for every positive target

`omega^2 = C p^2/(1+p^2/Mdisp^2)`,

an exact healthy-BPS quadratic dispersion/pole embedding with a continuous `h in (0,1)` family and explicit low-energy cutoff optimization. This result remains valid.

It explicitly does not establish the off-shell source/residue map.

### New residue/source redefinition locality gate

Prior theorem:

`K_RTK=(1+r q^2) K_BPS`.

A scalar-only multiplicative redefinition `phi_BPS=T phi_RTK` that exactly maps the kernels forces

`T(q)=sqrt(1+r q^2)`

on the positive branch. The source must transform as

`J_RTK=T(q) J_BPS`.

Crucial invariant:

`J_RTK^2/K_RTK = J_BPS^2/K_BPS`.

Therefore fixed-source residue mismatch alone is not a physical inequivalence theorem; a consistent field+source change leaves the quadratic source response invariant.

The actual scoped locality gate is that `sqrt(1+r q^2)` is not a finite polynomial in `q^2` for `r>0`. Hence an exact scalar-only finite-derivative local normalization cannot implement this map while also leaving the original q-independent fixed source unchanged.

This is not a no-go for constraint mixing, auxiliary fields, disformal/derived source maps or other local carriers.

Executable theorem:

- `rtk-class-build:rtk/route_b_residue_source_redefinition_gate.py`
- refined commit `7f5fda897938e24170b8a0228ce8a392e4110e8a`
- CI retrigger commit `2fcc9fb34fdffcd65a7fd487d6a1aff300ab4e85`.

Formula derivation appendix:

`research/methods/RTK_FORMULA_BIBLE_C8_SOURCE_REDEFINITION_APPENDIX.md`.

Status of this newest sub-gate: YELLOW pending its GitHub artifact inspection. Core symbolic identities were separately re-evaluated exactly before entry.

### Current C8 next step

Do not fit `A,B,C,P,R` independently at each epoch.

Derive `M0,M1,J,K0` from **one explicit fixed FLRW action**, keep one Wilson-coefficient tuple across epochs, then require:

1. correct constraint/DOF identification;
2. rank-one linear-gradient gate if a strict linear q denominator is claimed;
3. matched q-plane pole across epochs;
4. matched normalized q-plane residue and polynomial remainder;
5. source response generated by the action rather than an inserted `sqrt(1+r q^2)` factor;
6. physical `omega^2` propagator/source response;
7. no-ghost/no-gradient/hyperbolicity;
8. EFT/strong-coupling cutoff;
9. same-tuple PPN/Newton/GW constraints;
10. observational/nonlinear tests.

## Home compute architecture state

Observed node:

- runner `RTK-HOME-PC`
- Linux/X64 WSL
- custom label `rtk-home3`
- Intel i5-1235U
- **10 physical cores / 12 logical processors**
- about 7.7 GiB Windows RAM, about 5.9 GiB visible to WSL during measurement.

Engine v2.1 removes the old eight-worker cap, supports `RTK_WORKERS=auto`, adaptive task batching, persistent atomic checkpoint/resume, progress/rate/ETA and Ubuntu-visible event logging.

Fresh saturation/bootstrap run:

- run `32487473962`
- status at the latest runtime-index snapshot: pending behind previously queued self-hosted jobs.

Legacy `parallel`/`benchmark` CPU measurements are infrastructure history only, not performance evidence for v2.1 and not scientific model evidence.

Canonical architecture/history:

- `docs/RTK_COMPUTE_ARCHITECTURE.md`
- `docs/COMPUTE_LOG.md`.

## Immediate research order

1. Inspect B4 run `32482490823` artifact when complete and mechanically follow the frozen recenter/ray/half-scale decision tree.
2. Inspect both B10 half-scale jobs in `32482153752`; close/advance tail identifiability only if both pass.
3. Inspect paired B9 reoptimization run `32490152072`; retire fixed-center-only interpretation once matched results are available.
4. Inspect the new C8 residue/source-redefinition CI artifact; promote only the scoped locality statement if PASS.
5. Build the explicit fixed-action FLRW `M,J,K0` derivation rather than another abstract pole fit.
6. When home bootstrap `32487473962` reaches the runner, validate 12-worker saturation/checkpoint behavior, then route a suitable nonduplicated heavy scientific workload to it.

## Interpretation discipline

A workflow success means the encoded computation executed and its explicit assertions passed. It is not automatically a scientific gate closure. Every closure must satisfy the frozen acceptance rule and preserve its exact scope.
