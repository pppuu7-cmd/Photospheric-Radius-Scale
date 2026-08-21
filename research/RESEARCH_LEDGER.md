# RTK Research Ledger

Version: 2026-08-21 18:58 UTC
Purpose: canonical current-frontier record independent of chat history.

Historical evolution belongs in `research/RTK_MODEL_CHRONOLOGY.md`. Detailed derivations belong in `research/methods/RTK_FORMULA_BIBLE.md`, its index and appendices. This file records the current gates, evidence, exact run/artifact provenance and mandatory next actions.

## Current frontier

| ID | Question | Current evidence | Status | Next mandatory gate |
|---|---|---|---|---|
| A1-A5 | Frozen matched dense cosmology | replay-certified local scores | ✅ GREEN local baseline | keep local/global distinction |
| B4 | Minimal-neutrino local robustness | target-v2 base PASS; half-scale run `32514077002` executing exact Hessian | 🟡 RUNNING | inspect half artifact; then fresh-tree if PASS |
| B6 | Primordial abundances | paired AlterBBN differential run complete | ✅ CLOSED differential robustness | absolute BBN likelihood is separate if later frozen |
| B9 | Planck lensing robustness | RTK paired reoptimization complete; LCDM side of run `32490152072` still executing | 🟡 RUNNING | inspect LCDM artifact, then freeze matched stationarity targets |
| B10 | `lambda_D` finite-vs-dust-tail identifiability | base+half stationarity pass at factors 64 and 16384 | ✅ CLOSED protocol v1 | no further B10 work unless a broader posterior/global question is separately frozen |
| C8a | Schur/rank/q-residue algebra | run `32490690248`, artifact `9449602889` | ✅ GREEN reduced-kernel theorem | apply only to mechanisms that claim a strict constraint-determinant pole |
| C8b | BPS residue/source normalization | run `32491666126`, artifact `9449986685` | ✅ GREEN scoped locality theorem | use action-derived source map, not hand-inserted `sqrt(1+r q^2)` |
| C8c | Direct spatial-covariant FLRW scalar carrier | run `32514697064`, artifact `9458330218` | ✅ GREEN quadratic FLRW exact match / 🟡 completion | Newton/PPN/GW/compact-object/cutoff audit |
| C8d | Minimal Newton normalization of direct carrier | exact map requires `alpha=2`; theorem CI launched | 🟡 scoped boundary under CI | test smallest nonminimal/companion escape if confirmed |
| INFRA-HOME3 | Additional home compute | 10-core/12-logical self-hosted node; saturation bootstrap `32487473962` pending | 🟡 QUEUED | validate 12-worker saturation/checkpoint artifact before scientific dispatch |

## Frozen production baseline

Objective:

`matched-ultra-linstep2+dense-BOSS`

Production mapping: `eff`.

Frozen exact local scores:

- LCDM `S_eff = 1049.966118347761`
- RTK `S_eff = 1050.249912429787`
- `Delta S_eff = +0.2837940820259064`.

These are local raw-objective values only. They are not a global optimum theorem, significance, AIC/BIC, posterior preference or Bayes factor.

The latest autonomous production iterations, including iteration 201, have merely replayed this frozen comparison and do not by themselves advance the physics frontier.

## B4 minimal-neutrino stationarity

Objective:

`matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`.

Its absolute scores must never be mixed with the massless A1-A5 objective.

The first recentered RTK Hessian had three negative modes. Exact negative-mode rays in run `32284932113` confirmed real improvements, strongest at mode 0, alpha `+2`:

- parent `S_eff = 1050.6979573843187`
- winner `S_eff = 1050.5880475140204`
- improvement `0.10990987029822463 > 0.005`.

That winner became frozen target-v2.

### Target-v2 base replay

Run `32482490823` completed successfully.

Artifact:

- id `9452581043`
- digest `sha256:c5bb88ef4d182104d8e5b5ed578b749dd4e0f9b5b4857f047633782540d7223d`.

Results:

- center `1050.5880475140204`
- best exact `1050.5880063039972`
- improvement `4.12100232551893e-05 << 0.005`
- Hessian positive definite
- minimum eigenvalue `1.1738932605478353e-05`.

The soft minimum eigenvalue is still above the frozen positive-definite threshold `1e-8`, so the preregistered decision is **base PASS, half-scale mandatory**, not immediate local certification.

Frozen decision:

`rtk-class-build:research/robustness/b4_neutrino_rtk_ray_recenter_base_decision_v2.json`, commit `9202e84e9e0f98c35a4b6fc3be0caaea40d63a32`.

Half-scale validation:

- workflow `RTK B4 neutrino RTK target-v2 half stationarity`
- run `32514077002`
- last direct job check: setup/locks/build/Planck PASS, exact half-Hessian step in progress.

Decision after artifact:

- improvement `>0.005` -> recenter;
- non-PD without large coordinate improvement -> exact negative/near-zero-mode rays;
- recenter-clear + PD -> fresh-tree target-v2 replay;
- only after fresh-tree can the RTK side be locally certified, and paired robustness still requires equivalent LCDM certification.

Status: OPEN/RUNNING.

## B6 paired AlterBBN — CLOSED DIFFERENTIAL ROBUSTNESS

Canonical result:

`research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.

Run `32285359564` attempt 2, artifact `9447623417`.

Key result:

`max |R_H-1| = 2.422446243599552e-09`.

RTK-induced abundance shifts are observationally negligible under the frozen paired protocol. The reference D/H residual itself is about `-4.706 sigma` if only the quoted observational sigma is used, so this is not an absolute BBN goodness-of-fit claim.

Status: CLOSED within differential B6 scope.

## B9 Planck lensing

Fixed-center diagnostic:

- LCDM lensing `-2 ln L = 9.054925581629908`
- RTK lensing `-2 ln L = 9.039267332621456`
- fixed-center RTK-LCDM contribution `-0.015658249008452`.

This fixed-center number is diagnostic only.

Paired reoptimization run `32490152072`:

### RTK side — completed candidate

Artifact:

- id `9456206708`
- digest `sha256:3067fa908eb27cd90aa90b1898ea70ce0d4aa3b2e4e2b7a07bbfc8b9b9e945ea`.

Candidate summary:

- `best_S_B9 = 1059.2719553175134`
- `best_S_base_eff = 1050.2560245726381`
- lensing `-2 ln L = 9.015930744875291`
- improvement over RTK fixed-center B9 value `0.017224444894964108`
- no reported boundary axis
- classification `INTERIOR_LOCAL_REOPTIMIZATION_CANDIDATE`.

Best RTK candidate parameters:

- `As=2.0874265764520984e-9`
- `Ob=0.04679404670223316`
- `Om=0.2522369962493503`
- `h=0.6911169559022905`
- `lambda_D=792605.2167661682`
- `ns=0.9645439945136476`
- `zre=7.329291125785135`.

This is not yet a stationarity-certified B9 minimum.

### LCDM side

At the last direct check, the LCDM job remained inside `Run exact B9 paired reoptimization`; no LCDM artifact existed yet.

Therefore no paired B9 model comparison is allowed yet. Once both sides exist, freeze their exact candidates and run matched base+half stationarity/fresh-tree validation before using the paired score difference.

Status: OPEN/RUNNING.

## B10 lambda-tail identifiability — CLOSED

Canonical final result:

`research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`.

Protocol:

`rtk-class-build:research/robustness/B10_LAMBDA_TAIL_IDENTIFIABILITY_PROTOCOL_v1.md`.

Frozen finite local RTK score:

`S_finite = 1050.249912429787`.

Stationarity-certified tail anchors:

- factor 64: `S_tail=1050.249062546245`
- factor 16384: `S_tail=1050.2490169939647`.

Base T3 at both anchors had zero exact improvement and positive-definite Hessians. Independent half-scale run `32482153752` also had zero exact improvement and positive-definite Hessians at both anchors, with corresponding base↔half eigenvectors remaining strongly aligned.

Artifacts:

- factor64 `9450288661`, digest `sha256:f7f2d67b4770ab611e77f523b2ac2715f1b0c58c1aec685e9f745b454f520ef5`
- factor16384 `9450372881`, digest `sha256:1f5e57fc7b60d9d6f87535561b1c45403632933ca674e189a5be6ee220517d08`.

Best preregistered tail difference:

`Delta_tail = 1050.2490169939647 - 1050.249912429787 = -0.0008954358222581504`.

Because

`|Delta_tail| < 0.005`,

the frozen protocol mechanically gives

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

The slightly lower tail score is too small to trigger the separate recenter/global-search branch. This is a numerical-identifiability statement under the preregistered local/tail protocol, not a confidence interval, posterior, Bayes factor, global-minimum theorem or proof that lambda is mathematically redundant.

Status: CLOSED protocol v1.

## C8 — off-shell/local carrier program

### C8a Schur/rank/q-residue theorem

Run `32490690248`, artifact `9449602889`, digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`.

For mechanisms that claim a strict nonconstant linear denominator in the two-constraint determinant, the leading gradient block must be rank one. Normalized q-plane residues are fixed by the Schur algebra. These are not automatically physical `omega^2` propagator residues.

Status: GREEN scoped algebra.

### C8b BPS residue/source redefinition theorem

Refined run `32491666126` completed successfully.

Artifact:

- id `9449986685`
- digest `sha256:006d396c0bd686a76c1b76da2aaf3dd2c462b5ef696227b9ce5bf456134661d9`.

For

`K_RTK=(1+r q^2)K_BPS`,

an exact scalar-only field normalization requires

`T=sqrt(1+r q^2)`

and transforms the source with the same factor. The source-source response `J^2/K` is invariant under a consistent field+source transformation. Therefore residue mismatch alone is not a physical no-go.

The scoped locality result is that `sqrt(1+r q^2)` is not a finite polynomial in `q^2`; the exact scalar-only finite-derivative shortcut cannot both implement this normalization and leave the original q-independent source untouched.

Status: GREEN scoped theorem.

### C8c Direct spatial-covariant FLRW exact scalar match

Existing local benchmark action class:

`N sqrt(gamma)[Mpl^2/2(R3+KijKij-K^2)+F(t,N)+C_acc a_i a^i]`.

New executable theorem:

`rtk-class-build:rtk/route_b_spatial_covariant_flrw_exact_match.py`, commit `36c30a9b94ad120bfe461d93057daf57db8d14dc`.

CI:

- run `32514697064` — success
- artifact `9458330218`
- digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`.

Production DBI identities give exactly

`K_8piG = (rho_8piG+p_8piG)/c_a^2 = 2 M_K^2`.

Hence

`K_phys=2 Mpl^2 M_K^2`

and the acceleration coefficient required by the exact direct match is simply

`C_acc=Mpl^2`, constant across epochs.

After exact lapse/shift elimination on flat FLRW:

`S2 = 1/2 int a^3/H^2 [K_phys(1+p^2/M_K^2) dot(zeta)^2 - G_phys p^2 zeta^2]`,

so

`omega^2=c_a^2 p^2/(1+p^2/M_K^2)`

exactly for the production scalar target.

This mechanism does not rely on a linear pole in the constraint determinant; the earlier Schur single-pole filter is therefore inapplicable rather than violated.

Interpretation: the question “can a fixed local spatially covariant action reproduce the exact quadratic scalar FLRW RTK kernel?” now has a constructive YES within this benchmark class.

This is not yet a final covariant/phenomenologically viable completion.

Status: GREEN exact quadratic scalar theorem; completion remains OPEN.

### C8d Immediate Newton boundary of the direct carrier

In the standard low-energy healthy-Hořava/BPS normalization, the coefficient of `a_i a^i` is `(M_P^2/2) alpha`. The exact direct carrier has `C_acc=M_P^2`, hence its direct identification gives

`alpha=2`.

For the minimal/universal `xi=1,beta=0` matter branch,

`G_N=1/[8 pi M_P^2(1-alpha/2)]`.

Therefore the direct exact match lands at a singular Newton-normalization boundary for finite bare `M_P`.

A new exact scoped theorem was committed as

`rtk-class-build:rtk/route_b_spatial_covariant_newton_boundary.py`, commit `c9579ef48d508f0864b11914f399d9d517ed72de`, and its CI was launched by main commit `8c251c92e05683d76b1b29abcb386336138bc709`.

This does **not** reject the spatially covariant scalar EFT. It rejects, if CI confirms, only the simplest direct identification with `xi=1,beta=0` universal/minimal matter normalization. Candidate escape routes include `xi!=1`, a derived nonminimal/disformal matter metric, fixed companion operators, auxiliary fields or a broader covariant completion.

Status: YELLOW pending artifact inspection.

## Home compute architecture

Observed node:

- `RTK-HOME-PC`
- WSL Linux/X64
- label `rtk-home3`
- Intel i5-1235U
- 10 physical cores / 12 logical processors.

Engine v2.1 includes all-logical-CPU auto mode, adaptive batching, persistent atomic checkpoint/resume, progress/rate/ETA and Ubuntu-visible lifecycle logging.

Fresh saturation bootstrap run `32487473962` remained pending in the latest live Actions index because older self-hosted queue items had not fully drained.

Do not treat legacy one-thread/eight-worker benchmark utilization as evidence about v2.1.

## Immediate research order

1. Inspect B4 half run `32514077002`; mechanically follow the frozen decision tree.
2. Inspect the C8 minimal Newton-boundary CI artifact; if PASS, freeze the scoped negative result and search the smallest fixed escape deformation.
3. Wait for the LCDM side of B9 run `32490152072`; then freeze matched RTK/LCDM stationarity targets and do not compare uncertified optimizer candidates as minima.
4. Move C8 from scalar-kernel construction to the same-action matter/Newton/PPN/GW/compact-object/strong-coupling gates.
5. When home bootstrap `32487473962` finally executes, inspect its artifact and then dispatch only a nonduplicated suitable heavy scientific workload.

## Interpretation discipline

Workflow success is execution evidence, not automatically scientific closure. Every conclusion above uses the frozen acceptance rule and explicitly stated scope.
