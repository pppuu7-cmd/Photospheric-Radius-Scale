# RTK Research Ledger

Version: 2026-08-21 20:31 UTC
Purpose: canonical current-frontier record independent of chat history. Historical evolution belongs in `research/RTK_MODEL_CHRONOLOGY.md`; long derivations belong in Formula Bible appendices and dated result notes.

## Current frontier

| ID | Question | Current evidence | Status | Next mandatory gate |
|---|---|---|---|---|
| A1-A5 | Frozen matched dense cosmology | exact fresh-tree replay | ✅ GREEN local baseline | preserve local/global distinction |
| B4 | Minimal-neutrino robustness | target-v2 base PASS; half-scale run `32514077002` computing exact Hessian | 🟡 RUNNING | inspect half; fresh-tree if recenter-clear + PD |
| B6 | Primordial abundances | paired AlterBBN differential result | ✅ CLOSED differential | absolute BBN likelihood separate |
| B9-RTK | Planck lensing RTK center | recentered candidate; base Hessian `32518496348` running | 🟡 RUNNING | recenter/rays/half mechanically |
| B9-LCDM | Planck lensing LCDM center | original optimizer interrupted after 293 exact points; best exact point frozen; base Hessian `32522002655` running | 🟡 RUNNING | recenter/rays/half mechanically |
| B10 | finite `lambda_D` vs dust tail | base+half tail stationarity | ✅ CLOSED protocol v1 | broader posterior/global question only if separately frozen |
| C8a-b | Schur/rank/residue/source algebra | runs `32490690248`, `32491666126` | ✅ GREEN scoped algebra | preserve action-derived source discipline |
| C8c | Direct local FLRW scalar carrier | run `32514697064`, artifact `9458330218` | ✅ GREEN quadratic scalar theorem | physical completion open |
| C8d-e | Standard universal low-energy matter frame | beta=0 and general-beta BBN+PPN+GW tests | ❌ BLACK scoped no-go | leave standard universal matter frame |
| C8f | Minimal `{a_i,D_iK}` mixed-gradient escape | run `32519335082`, artifact `9459962141` | ❌ BLACK scoped no-go | use broader extrinsic-curvature basis |
| C8g | Full scalar grad-K pointwise carrier | exact rank-one solution exists; constant-Wilson all-epoch gate run `32521251025` PASS | 🟡 MIXED | state/invariant-dependent fixed action required |
| C8h | Tensor safety of grad-K carrier | prior restricted-basis `R=2` theorem superseded broadly after discovering `D_iK D_jK^{ij}`; corrected TT-safe basis CI launched | 🟡 CORRECTION IN CI | inspect correction artifact; never quote old `R=2` as full-basis obstruction |
| C8i | Static/Minkowski regularity of minimal grad-K carrier | exact `U~H^-2` theorem launched | 🟡 CI PENDING | if PASS move to auxiliary/modified-constraint carrier |
| C9 | EFT cutoff / strong coupling | no final regular carrier yet | ❌ OPEN | evaluate same surviving action/tuple |
| INFRA-HOME3 | Additional compute | 10-core/12-logical WSL node; legacy queued benchmark flood blocks clean bootstrap | 🟡 QUEUED | require 12-worker saturation/checkpoint PASS before unique science |

## Frozen production baseline

Objective: `matched-ultra-linstep2+dense-BOSS`; mapping `eff`; objective fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`.

- LCDM `S_eff = 1049.966118347761`.
- RTK `S_eff = 1050.249912429787`.
- `Delta S_eff = +0.2837940820259064`.

This is a reproducible **local raw-objective** comparison only: not global optimality, significance, AIC/BIC, posterior preference, or Bayes evidence.

## B4 minimal-neutrino robustness

Separate objective `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`; never mix absolute scores with A1-A5.

Target-v2 base run `32482490823`, artifact `9452581043`:

- center `1050.5880475140204`;
- best exact `1050.5880063039972`;
- improvement `4.12100232551893e-05 < 0.005`;
- positive-definite Hessian; minimum eigenvalue `1.1738932605478353e-05`.

Independent half-scale run `32514077002` remains inside exact Hessian. Decision rule: `>0.005` improvement -> recenter; non-PD -> exact eigenmode rays; recenter-clear + PD -> fresh-tree replay.

## B6 AlterBBN

Run `32285359564` attempt 2, artifact `9447623417`. `max |R_H-1| = 2.422446243599552e-09`; RTK-induced paired Yp/D/H changes are negligible under this differential protocol. Absolute BBN goodness-of-fit is a separate question.

## B9 Planck lensing

Objective `matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`.

### RTK

Parent paired run `32490152072`, RTK artifact `9456206708`:

- fixed center `1059.2891797624084`;
- best exact `1059.2719553175134`;
- improvement `0.017224444894964108 > 0.005`.

Frozen RTK recenter center: `As=2.0874265764520984e-9`, `Ob=0.04679404670223316`, `Om=0.2522369962493503`, `h=0.6911169559022905`, `lambda_D=792605.2167661682`, `ns=0.9645439945136476`, `zre=7.329291125785135`.

Base stationarity run `32518496348` is computing exact Hessian.

### LCDM interrupted optimizer recovery

The LCDM job in paired run `32490152072` was cancelled during the numerical step by the 360-minute job limit. Upload succeeded: artifact `9460759915`, digest `sha256:6551f10c5896ef98d042aa578ade61c2922b002941dcc241e13b322d2cdc94c0`.

The uploaded log contains **293 exact B9 evaluations**. Exact scan of the complete log gives:

- eval 1 frozen center: `S_B9=1059.021043929391`;
- best exact eval 291: `S_B9=1058.6304210952487`;
- improvement `0.3906228341422775 >> 0.005`;
- base part `1049.7048540841683`;
- lensing contribution `8.925567011080329`.

Best exact params:

- `As=2.1043404211660074e-09`
- `Ob=0.04854523676526571`
- `Om=0.26020316605972393`
- `h=0.6790995137400001`
- `ns=0.965177972117784`
- `zre=7.785420802640161`
- `lambda_D=0`.

This is **not** a converged COBYQA result. It is frozen only as an interrupted-optimizer recenter seed in `rtk-class-build:research/robustness/B9_LCDM_INTERRUPTED_RECENTER_TARGET_v1.json`. Base Hessian run `32522002655` was launched directly at this exact seed to avoid repeating the 293 expensive points. Matched B9 interpretation still requires both models to pass base + independent half-scale + fresh-tree replay.

## B10 lambda-tail identifiability

Closed under protocol v1. Stationarity-certified tail scores: factor 64 `1050.249062546245`; factor 16384 `1050.2490169939647`; best tail-vs-finite delta `-0.0008954358222581504`, below the `0.005` numerical identifiability threshold. This is not posterior/global evidence.

## C8 exact scalar carrier and physical completion ladder

### Direct scalar construction

Run `32514697064`, artifact `9458330218`. Production identity `K_8piG=(rho_8piG+p_8piG)/c_a^2=2M_K^2`. Exact constraint elimination yields the controlled RTK scalar dispersion `omega^2=c_a^2 p^2/(1+p^2/M_K^2)`.

### Standard universal matter route excluded in scope

Correctly distinguish bare `M_*`, Friedmann `G_cosm`, and local `G_N`. Beta=0 run `32518243787` and general-beta run `32518936616` exclude the direct acceleration carrier in the cited standard universal low-energy Hořava matter frame. Nonminimal/disformal matter and other constraint completions remain open.

### Minimal mixed-gradient basis excluded

Run `32519335082`, artifact `9459962141`, digest `sha256:2bde114d4aafb9f5758ff7107c8479c3112036ccf507755960ff5bad676d1809`.

For `C a_i a^i + 2D a_iD^iK + B D_iK D^iK`, exact mixed branch obeys

`C/C_direct=[(6H^2M_*^2+K)/(6H^2M_*^2-K)]^2>1`.

Thus `C=0` cannot reproduce the exact RTK scalar kernel in this basis.

### Full scalar grad-K pointwise carrier

For the general scalar form

`p^2[U A^2+2V A q+W q^2]`, `A=dot(zeta)-Hn`, `q=p^2 psi`, exact matching requires

- `UW=V^2`;
- `V/W=(6H^2M_*^2-K_clock)/(4H^2M_*^2)`;
- `W=2H^2M_*^4/(K_clock M_K^2)`.

The pointwise solution exists. But one constant `(U,V,W)` tuple would force `K_clock/(H^2M_*^2)` constant and then `M_K` constant. Production `M_K(a)` is not constant. Constant-Wilson theorem: run `32521251025`, artifact `9460618747`, digest `sha256:3e7fdd10e8847483ce212472779ff06f518c7190be82150ded3e282701159f99`.

### Important tensor-basis correction

Run `32521548678`, artifact `9460716295` correctly proved an `R=2` tensor-null condition **only inside the restricted basis `{O_T,O_K,O_D}`**. Its earlier broad interpretation as a full one-grad-K obstruction is superseded.

The missing allowed contraction is

`O_X=D_iK D_jK^{ij}`.

At scalar quadratic flat-FLRW order the TT-safe basis maps as

- `O_K=D_iK D^iK -> (U,V,W)=(9,3,1)`;
- `O_D=D_iK^i_j D_kK^{kj} -> (1,1,1)`;
- `O_X=D_iK D_jK^{ij} -> (3,2,1)`.

Its determinant is `-4`: TT-safe operators alone span arbitrary scalar `(U,V,W)`. On the rank-one RTK branch `r=V/W`, the whole pointwise correction can be written

`W[((r-1)/2) D_iK + ((3-r)/2) D_jK^j_i]^2`.

This vanishes for strictly static `K_ij=0` and for TT tensors (`delta K=0`, `D_j delta K^j_i=0`). Corrected exact theorem is in `rtk/route_b_gradK_full_ttsafe_basis_gate.py`; CI launched. **Do not quote `R=2` as a full-basis tensor obstruction.**

The normalization-independent dictionary run `32521709199`, artifact `9460770879`, found `Q_cosm=2M_K^2/H^2` changes by a factor `169.01086404510914` between z=0 and z=1 on the frozen grid. This rules out staying on `R=2` with a constant normalization in the old restricted representation, but no longer excludes the corrected TT-safe full basis.

### Minimal grad-K regularity issue

Basis-independently, the exact pointwise scalar form has

`U=(6H^2M_*^2-K_clock)^2/(8 K_clock M_K^2 H^2)`.

Thus for finite positive `K_clock/M_K^2`, `U~H^-2`. With the production identity `K_clock=2M_cosm^2 M_K^2`, `lim(H^2 U)=M_cosm^2/4`. A CI theorem has been launched to test/freeze this scoped zero-H regularity obstruction. If confirmed, the next viable route is auxiliary fields or a modified base lapse/shift constraint structure rather than merely dressing the same minimal grad-K carrier.

## Infrastructure

Home node is WSL Linux/X64, Intel i5-1235U, 10 physical / 12 logical processors. A legacy flood of queued `RTK Home Scientific Benchmark v3 Progress` runs blocks the clean bootstrap. Do not route unique science there until a 12-worker saturation/checkpoint artifact is inspected.

## Immediate research order

1. Inspect B4 half-scale `32514077002`; follow fresh-tree/recenter/ray decision mechanically.
2. Inspect B9 RTK base `32518496348` and LCDM base `32522002655`; advance each independently to half-scale only after base pass.
3. Inspect corrected full TT-safe basis CI; mark old `R=2` result restricted/superseded in all formula docs.
4. Inspect grad-K zero-H regularity CI. If PASS, prioritize auxiliary/modified-constraint carriers that avoid `U~H^-2`.
5. Apply DOF/ghost/gradient/hyperbolicity, PPN/Newton, GW, compact-object and EFT-cutoff gates to the **same fixed action**, not to separate tuned sectors.
6. Validate the 12-worker home bootstrap before dispatching nonduplicated science.

## Interpretation discipline

Workflow success means the encoded assertions ran. A scientific closure requires the frozen acceptance rule and exact stated scope. Any scoped no-go or superseded restricted-basis result must never be promoted to a no-go for RTK or for all covariant completions.
