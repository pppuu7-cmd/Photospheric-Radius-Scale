# RTK Research Ledger

Version: 2026-08-21 19:47 UTC
Purpose: canonical current-frontier record independent of chat history.

Historical evolution belongs in `research/RTK_MODEL_CHRONOLOGY.md`. Long derivations belong in the Formula Bible/index/appendices. This ledger records only the current scientific gates, exact run/artifact provenance, interpretation boundaries, and mandatory next actions.

## Current frontier

| ID | Question | Current evidence | Status | Next mandatory gate |
|---|---|---|---|---|
| A1-A5 | Frozen matched dense cosmology | exact fresh-tree replay | ✅ GREEN local baseline | preserve local/global distinction |
| B4 | Minimal-neutrino robustness | target-v2 base PASS; half-scale run `32514077002` in exact Hessian | 🟡 RUNNING | inspect half artifact; fresh-tree if PASS |
| B6 | Primordial abundances | paired AlterBBN differential result | ✅ CLOSED differential | absolute BBN likelihood is separate |
| B9 | Planck lensing robustness | RTK reoptimization recentered; RTK base Hessian `32518496348` running; LCDM reoptimization still running | 🟡 RUNNING | certify each side base+half+fresh-tree before paired score |
| B10 | finite `lambda_D` vs dust tail | base+half tail stationarity | ✅ CLOSED protocol v1 | broader posterior/global question only if separately frozen |
| C8a | Schur/rank/q-residue algebra | run `32490690248`, artifact `9449602889` | ✅ GREEN scoped algebra | apply only to claimed determinant-pole mechanisms |
| C8b | BPS residue/source normalization | run `32491666126`, artifact `9449986685` | ✅ GREEN scoped locality | source map must be action-derived |
| C8c | Direct local FLRW scalar carrier | run `32514697064`, artifact `9458330218` | ✅ GREEN quadratic scalar theorem | physical completion still open |
| C8d | Correct cosmological/Newton normalization, beta=0 | run `32518243787`, artifact `9459582368` | ✅ BLACK scoped no-go | beta!=0 / nonminimal / companion route |
| C8e | Standard universal matter frame, general beta | run `32518936616`, artifact `9459822043` | ✅ BLACK scoped no-go | leave standard universal matter frame |
| C8f | Minimal static-safe mixed-gradient escape | theorem launched from source `7aa3f26e...` | 🟡 CI PENDING | inspect artifact; if PASS move beyond `{a_i,D_iK}` quadratic basis |
| C9 | EFT cutoff / strong coupling for viable completion | no final carrier yet | ❌ OPEN | evaluate after an escape carrier survives C8 matter/PPN/GW gates |
| INFRA-HOME3 | Additional compute | 10-core/12-logical WSL node; bootstrap `32487473962` has no executed job record | 🟡 QUEUED | require 12-worker saturation/checkpoint PASS before science dispatch |

## Frozen production baseline

Objective: `matched-ultra-linstep2+dense-BOSS`.

Production mapping: `eff`.

Frozen exact local scores:

- LCDM `S_eff = 1049.966118347761`;
- RTK `S_eff = 1050.249912429787`;
- `Delta S_eff = +0.2837940820259064`.

This remains a reproducible **local raw-objective** comparison only. It is not a global optimum theorem, significance, AIC/BIC, posterior preference, or Bayes factor.

Latest autonomous production iterations have mainly replayed this number and do not themselves advance the physical frontier.

## B4 minimal-neutrino gate

Separate objective:

`matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`.

Never mix its absolute scores with the massless A1-A5 objective.

Earlier exact negative-mode rays forced target-v2 recentering. The frozen target-v2 center is:

- `As=2.0920212896820786e-9`
- `Ob=0.04722200104991654`
- `Om=0.2528393318824633`
- `h=0.6885660022475836`
- `lambda_D=3043326.1774413693`
- `ns=0.9657332769496741`
- `zre=7.506210209218662`.

Target-v2 base run `32482490823`, artifact `9452581043`, digest `sha256:c5bb88ef4d182104d8e5b5ed578b749dd4e0f9b5b4857f047633782540d7223d`:

- center `1050.5880475140204`;
- best exact `1050.5880063039972`;
- improvement `4.12100232551893e-05 << 0.005`;
- Hessian positive definite;
- minimum eigenvalue `1.1738932605478353e-05` > frozen `1e-8` threshold.

Frozen decision: base PASS, independent half-scale mandatory.

Half-scale:

- run `32514077002`;
- job `target-v2-half-hessian`;
- latest direct check: locks/build/Planck PASS, exact half-Hessian still `in_progress`.

Decision tree remains mechanical: improvement `>0.005` -> recenter; non-PD -> exact eigenmode rays; recenter-clear + PD -> independent fresh-tree replay; paired B4 still requires equivalent LCDM certification.

Canonical proof chain: `research/robustness/RTK_B4_NEUTRINO_STATIONARITY_CHAIN_2026-08-21.md`.

## B6 AlterBBN — CLOSED DIFFERENTIAL ROBUSTNESS

Run `32285359564` attempt 2, artifact `9447623417`.

`max |R_H-1| = 2.422446243599552e-09`.

RTK-induced Yp and D/H changes are observationally negligible under the frozen paired differential protocol. This does not establish absolute BBN goodness-of-fit; the frozen reference D/H residual itself is about `-4.706 sigma` if only the quoted observational sigma is used.

Canonical result: `research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.

## B9 Planck lensing

Objective:

`matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`.

The old fixed-center difference remains diagnostic only.

### RTK reoptimization candidate

Parent run `32490152072`, RTK artifact `9456206708`, digest `sha256:3067fa908eb27cd90aa90b1898ea70ce0d4aa3b2e4e2b7a07bbfc8b9b9e945ea`:

- fixed-center `S_B9 = 1059.2891797624084`;
- best exact `S_B9 = 1059.2719553175134`;
- improvement `0.017224444894964108 > 0.005`;
- status `INTERIOR_LOCAL_REOPTIMIZATION_CANDIDATE`;
- no boundary axis.

Best parameters:

- `As=2.0874265764520984e-9`
- `Ob=0.04679404670223316`
- `Om=0.2522369962493503`
- `h=0.6911169559022905`
- `lambda_D=792605.2167661682`
- `ns=0.9645439945136476`
- `zre=7.329291125785135`.

Because the improvement exceeds the frozen `0.005` threshold, the original fixed RTK center is not B9-stationary.

The RTK recenter target was frozen **before the final LCDM artifact existed**:

`rtk-class-build:research/robustness/B9_RTK_RECENTER_TARGET_v1.json`, commit `c89b8eac3e70f0fa40bc41963695de803e2e5487`.

RTK base stationarity:

- worker `rtk/b9_rtk_stationarity_hessian.py`, source commit `b3d146658a16d2407a659638179a8a75e92720ee`;
- run `32518496348`;
- latest direct check: exact B9 RTK recenter base Hessian `in_progress`, all prerequisite locks passed.

### LCDM reoptimization

Original paired run `32490152072` LCDM job remains inside exact B9 reoptimization at the latest direct check. No final LCDM artifact has been used in any RTK target decision.

No matched B9 RTK-vs-LCDM score may be interpreted until both candidates separately pass base, independent half-scale, and fresh-tree certification.

## B10 lambda-tail identifiability — CLOSED

Canonical result: `research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`.

Stationarity-certified tail scores:

- factor 64: `1050.249062546245`;
- factor 16384: `1050.2490169939647`.

Both base and independent half-scale stencils had zero exact improvement and positive-definite Hessians. Best tail difference from the finite local score:

`Delta_tail = -0.0008954358222581504`.

Since `|Delta_tail|<0.005`, the preregistered classification is

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

Scope: numerical identifiability under protocol v1 only; not posterior/global evidence.

## C8 — constructive carrier and scoped exclusions

### C8a — Schur/rank/q-residue

Run `32490690248`, artifact `9449602889`, digest `sha256:1f2bfda3959e8b6c57866bd35e7279e7cb398460c1a6cd296d4b2d146e092dce`.

For a two-constraint mechanism claiming a strict nonconstant linear determinant denominator, the leading gradient block must be rank one. q-plane residues are not automatically physical `omega^2` propagator residues.

### C8b — BPS residue/source normalization

Run `32491666126`, artifact `9449986685`, digest `sha256:006d396c0bd686a76c1b76da2aaf3dd2c462b5ef696227b9ce5bf456134661d9`.

`K_RTK=(1+r q^2)K_BPS` can be related by `T=sqrt(1+r q^2)` only if the source transforms with the same factor; `J^2/K` stays invariant. The exact scalar-only finite-derivative shortcut is unavailable because that square root is not a finite polynomial in `q^2`.

### C8c — direct local FLRW scalar match: constructive YES

Run `32514697064`, artifact `9458330218`, digest `sha256:72fe15a918873ee0d7bf6af27f6eab51ef47dea48d4a4c3d7db9d65de9aeeb74`.

Production DBI identity:

`K_8piG=(rho_8piG+p_8piG)/c_a^2=2 M_K^2`.

Exact lapse/shift elimination in the spatial-covariant benchmark gives

`S2 = 1/2 int a^3/H^2 [K_phys(1+p^2/M_K^2) dot(zeta)^2-G_phys p^2 zeta^2]`,

hence

`omega^2=c_a^2 p^2/(1+p^2/M_K^2)`.

Thus a fixed local spatially covariant action can reproduce the exact controlled quadratic FLRW RTK scalar kernel. This is not yet a viable covariant/matter completion.

### C8d — beta=0 correct gravitational-normalization no-go

Production `8 pi G` must be mapped to the candidate's cosmological/Friedmann coupling, not automatically to the bare action coefficient.

For the standard beta=0 universal matter branch, exact matching forces

`alpha=2+3 lambda_prime`.

Run `32518243787`, artifact `9459582368`, digest `sha256:1250056abd3426d1b78a32d4c97272dd6fa7d609f954adcd2cdb2e8cb14235d9` proves no healthy positive-finite-Newton solution on this branch.

### C8e — standard universal matter frame excluded for general beta

Modern standard low-energy relations give on the exact-match hypersurface

`alpha=2+3 gamma+beta`,

`G_cosm/G_N=(2-alpha)/alpha`.

The cited BBN bound reduces to

`16/17 < alpha < 16/15`.

With the post-GW170817 `|beta|<=~1e-15` benchmark, the first PPN expression is at least `3.7647058823529296`, versus the `1e-4` benchmark — a minimum exclusion factor `37647.058823529296`.

CI:

- run `32518936616`;
- artifact `9459822043`;
- digest `sha256:07f9e3bb7e64139a5f35df9e7aa2d77a7bfe2b06b4578a545e14354c046aca02`.

Canonical result: `research/RTK_C8_STANDARD_MATTER_NO_GO_RESULT_2026-08-21.md`.

This excludes only the direct acceleration-only carrier mapped to the cited standard **universal** low-energy Hořava matter frame. Nonminimal/disformal matter, auxiliary fields, other fixed companion operators and broader completions remain open.

### C8f — minimal mixed-gradient static-safe escape

The operator basis

`C a_i a^i + 2D a_i D^i K + B D_iK D^iK`

was tested because the `D_iK` terms vanish in a strictly static `K_ij=0` sector.

Exact FLRW polynomial matching has two analytic candidate branches in the committed theorem. The nontrivial mixed branch requires

`C/C_direct=[(6H^2M_*^2+K)/(6H^2M_*^2-K)]^2 > 1`.

Therefore, if CI confirms, this minimal mixed-gradient basis cannot lower the static acceleration coefficient; `C=0` has no exact RTK solution.

Source:

- `rtk-class-build:rtk/route_b_mixed_gradient_static_safe_gate.py`;
- commit `7aa3f26e3896baf69deb2c45d915f7b38ec50ba0`;
- workflow/trigger launched from main; artifact inspection pending.

## Formula/provenance map

Important new normalization appendix:

`research/methods/RTK_FORMULA_BIBLE_C8_GRAVITY_NORMALIZATION_APPENDIX.md`.

It explicitly separates bare `M_*`, cosmological `G_cosm`, and local `G_N`. Never revert to a single unspecified `Mpl` when mapping the exact scalar EFT to a physical matter frame.

Chronology: `research/RTK_MODEL_CHRONOLOGY.md`.

## Home compute state

Home node:

- `RTK-HOME-PC`, WSL Linux/X64, label `rtk-home3`;
- Intel i5-1235U;
- 10 physical cores / 12 logical processors.

Engine v2.1 provides all-logical-CPU mode, adaptive batching, persistent atomic checkpoint/resume, progress/rate/ETA and Ubuntu-visible lifecycle logs.

Bootstrap run `32487473962` still returns no executed job record. Do not dispatch unique heavy science to the home node until the saturation/checkpoint bootstrap produces an inspected PASS artifact.

## Immediate research order

1. Inspect B4 half-scale `32514077002`; if recenter-clear + PD, launch independent fresh-tree target-v2 replay.
2. Inspect B9 RTK base Hessian `32518496348`; follow recenter/ray/half decision mechanically.
3. Inspect B9 LCDM reoptimization from `32490152072` when complete; freeze its center without changing the already-frozen RTK target.
4. Inspect C8 mixed-gradient artifact; if PASS, move the escape search beyond the minimal `{a_i,D_iK}` quadratic gradient basis.
5. Prioritize nonminimal/auxiliary/constraint companion constructions that preserve the exact FLRW scalar kernel while changing static PPN/Newton response; apply GW, DOF, stability and compact-object gates to the same fixed tuple.
6. Validate the 12-worker home bootstrap before routing nonduplicated science to the local node.

## Interpretation discipline

A GitHub workflow success means the encoded computation ran and its assertions passed. A scientific closure requires the frozen acceptance rule and the exact scope above. Scoped no-go results must never be promoted to a no-go for RTK or for all covariant completions.
