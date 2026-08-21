# RTK Research Ledger

Version: 2026-08-21 23:58 UTC
Purpose: canonical current-frontier record independent of chat history. Detailed derivations/results remain in named robustness notes, Formula Bible appendices, model chronology and iteration chronology.

## Current frontier

| ID | Question | Current evidence | Status | Next mandatory gate |
|---|---|---|---|---|
| A1-A5 | Frozen matched dense cosmology | exact fresh-tree local replay | ✅ GREEN local baseline | preserve local/global distinction |
| B4 | Minimal-neutrino robustness | target-v2 half-scale run `32514077002`, artifact `9463331303`: zero exact improvement but non-PD Hessian, lambda_min `-0.00715417294` | 🟡 OPEN / RAYS LAUNCHED | exact frozen negative/soft eigenmode rays; recenter if improvement >0.005, else quarter-scale resolution audit |
| B6 | Primordial abundances | paired AlterBBN differential result | ✅ CLOSED differential | absolute BBN likelihood is separate |
| B9-RTK | Planck lensing RTK center | recenter base run `32518496348`, artifact `9464480301`: improvement 0, PD Hessian, lambda_min `5.825694e-4` | 🟡 BASE PASS / HALF LAUNCHED | independent half-scale, then fresh-tree if recenter-clear + PD |
| B9-LCDM | Planck lensing LCDM center | run `32522002655`, artifact `9463358870`: exact improvement `0.03518806935 > 0.005` from interrupted-seed center | 🟡 RECENTER-V2 LAUNCHED | fresh exact base Hessian at frozen v2 center |
| B10 | finite `lambda_D` vs dust tail | T1/T2/T3 + independent half-scale at factors 64,16384; prior-chat audit complete | ✅ CLOSED protocol v1 | do not reopen; posterior/Bayes/global questions require separate A6 protocol |
| C8-Schur | constraint pole/rank/q-residue/source algebra | CI/artifact verified | ✅ GREEN scoped algebra | use only action-derived source maps |
| C8-direct | direct local FLRW scalar kernel | exact quadratic scalar construction exists | ✅ GREEN quadratic scalar theorem | physical completion remains open |
| C8-standard matter | standard universally coupled low-energy Hořava direct embedding | BBN/PPN/GW incompatibility on frozen direct slice | ❌ BLACK scoped | use different constraint/matter architecture |
| C8-gradK | minimal/regular grad-K and ordinary auxiliary escapes | several exact scoped obstructions; corrected TT-safe basis pointwise escape exists | 🟡 MIXED | no broad no-go; retain scope boundaries |
| C8-Dirac | rank-one degenerate one-scalar mechanism | one-DOF theorem and lapse/shift Schur bridge artifact-verified | ✅ GREEN quadratic/constraint toy scope | embed same rank-one direction in a complete fixed action |
| C8-mixed kinetic | fixed-state local mixed-kinetic scalar EFT | corrected run `32528572862`, artifact `9463080405`; exact production RTK dispersion, one scalar in isolated rank-one sector | ✅ GREEN quadratic scalar EFT | avoid additive second kinetic direction; full gravitational embedding |
| C8-U1 | local U(1) gauge/constraint completion | one explicit GR-PPN family conflicts with RTK direct beta0=2; another published GR-PPN family leaves beta0 algebraically free | 🟡 ACTIVE | CI both family gates, then freeze one beta0=2 family-I tuple and solve static/constraint equations |
| C9 | EFT cutoff / radiative/strong-coupling stability | no final surviving full action yet | ❌ OPEN | apply to same action that survives C8 |
| INFRA-HOME3 | Additional compute | i5-1235U, 10 physical / 12 logical; new engine exists, legacy self-hosted queue previously blocked clean bootstrap | 🟡 INFRA OPEN | require clean 12-worker saturation/checkpoint artifact before unique science |

## Frozen production baseline

Objective: `matched-ultra-linstep2+dense-BOSS`; mapping `eff`; objective fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`.

- LCDM `S_eff = 1049.966118347761`.
- RTK `S_eff = 1050.249912429787`.
- `Delta S_eff = +0.2837940820259064`.

Scope: reproducible local raw-objective comparison only; not global optimality, significance, AIC/BIC, posterior preference or Bayes evidence.

## B4 minimal-neutrino robustness

Objective: `matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`. Never compare its absolute scores directly with the massless A1-A5 objective.

Target-v2 base run `32482490823`, artifact `9452581043`:

- center `1050.5880475140204`;
- best improvement `4.12100232551893e-05 < 0.005`;
- Hessian PD but extremely soft, minimum eigenvalue `1.1738932605478353e-05`.

Independent half-scale run `32514077002`, artifact `9463331303`, digest `sha256:e96fcb3ab64286dadacd61d0b619889ac1b366d06d36a049effba67987edc614`:

- center replay `1050.5880475140204`;
- exact coordinate/stencil improvement `0`;
- Hessian **not** positive definite;
- first two eigenvalues `-0.007154172940511002`, `+0.00013489280964015747`.

The frozen decision tree therefore forbids fresh-tree closure at this point. A target was frozen before ray scores at

`rtk-class-build:research/robustness/b4_neutrino_rtk_target_v2_half_eigenmode_rays_target_v1.json`, commit `b0f17ffddb943c73c48f769de1407456e4aefd82`.

It selects the negative mode plus a conservatively preselected very soft positive mode, amplitudes `[-2,-1,-0.5,+0.5,+1,+2]`, with no clipping. Worker commit `55c993894e9b2c8595e8fffb1a21ecf41ac68dd5`; workflow commit `99781cb503862d6812cef90634764eafb7f9dfab`; trigger `69f07b8956ead1611f0add45ad8474ab859018a7`.

Decision: any exact ray improvement > `0.005` => new recenter; otherwise preregister quarter-scale Hessian resolution audit because half-scale curvature remains non-PD.

## B6 AlterBBN

Run `32285359564` attempt 2, artifact `9447623417`. `max |R_H-1| = 2.422446243599552e-09`; RTK-induced paired abundance shifts are observationally negligible in the frozen differential protocol. Absolute BBN goodness-of-fit remains a separate question.

## B9 Planck lensing

Objective: `matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`.

### RTK

Parent paired reoptimization found

- fixed center `1059.2891797624084`;
- best exact `1059.2719553175134`;
- improvement `0.017224444894964108 > 0.005`.

Recenter base run `32518496348`, artifact `9464480301`, digest `sha256:021e393bdadee9d70d20de0d901247e347db3b2c677e13ce6d830fcd3a8b448d`:

- center/best exact `1059.2719553175134`;
- improvement `0`;
- Hessian PD;
- minimum eigenvalue `0.0005825694006286208`.

Base decision frozen at `rtk-class-build:research/robustness/B9_RTK_RECENTER_BASE_DECISION_v1.json`, commit `bb4f9d988c87e96572d4d3fd603dbc2186f0fa54`.

Independent half-scale workflow commit `33738438c4a1d617a2046ea1233c5dcb59573794`, trigger `3f8f9fe18530bec31e7a9bfc69c03b780b4df721`. Do not claim B9 RTK local certification until half-scale and then fresh-tree gates pass.

### LCDM

The original paired optimizer timed out after 293 exact points; its best exact point `1058.6304210952487` became an interrupted-recenter seed.

Base-Hessian run `32522002655`, artifact `9463358870`, digest `sha256:282ac56a04ba2f9dfb29851a208084d44c86d0e6f295cfb450cb1af282a6c0d6` completed the exact calculation. The workflow red status came from a post-computation generated-worker summary-model assertion bug, not from a lost scientific calculation.

Scientific result:

- parent center `1058.6304210952487`;
- best exact `1058.595233025902`;
- improvement `0.03518806934675922 > 0.005`;
- parent Hessian PD, but recenter is mandatory because the exact improvement exceeds tolerance.

New frozen center:

- `As=2.1005029109474964e-09`
- `Ob=0.04847523676526571`
- `Om=0.25950316605972396`
- `h=0.6794495137400001`
- `ns=0.965527972117784`
- `zre=7.719806125603674`
- `lambda_D=0`.

Target `rtk-class-build:research/robustness/B9_LCDM_RECENTER_TARGET_v2.json`, commit `0ae9f85c652aacfc75e5edc5b00774225496d732`; fresh base workflow `9f74c2ca56b593814f381c2824fb48f044e8204d`; trigger `5f034d51b0b71ed335819ff11c03126f137adb52`.

## B10 lambda-tail identifiability — CLOSED

Canonical result: `research/robustness/RTK_B10_FINAL_TAIL_IDENTIFIABILITY_RESULT_2026-08-21.md`.

- finite score `1050.249912429787`;
- factor-64 stationarity-certified tail `1050.249062546245`;
- factor-16384 tail `1050.2490169939647`;
- best tail-finite delta `-0.0008954358222581504`;
- `|Delta| < 0.005`.

Classification:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

A direct prior-chat audit is now canonical at `research/robustness/RTK_B10_CHAT_AUDIT_2026-08-22.md`, commit `22515a46f6f908e022026ea2156ca547fabd4723`. It found **no missing mandatory B10-v1 gate**. T1 reconnaissance, T2 profiling, T3 base stationarity and independent half-scale validation are all represented. No farther-tail extension is required by protocol v1.

Posterior/profile-likelihood confidence intervals, prior sensitivity, evidence/Bayes factors and global optimization are possible future A6/post-freeze studies only. They require new frozen protocols and must not retroactively reopen or reinterpret B10-v1.

## C8 physical-completion ladder

### Exact scalar/mixed-kinetic results that survive

The production DBI background defines fixed state-functions and the exact rational scalar law

`omega^2 = c_a^2(r) p^2/[1+p^2/M_K(r)^2]`.

A fixed-state local quadratic scalar EFT

`L2 = K(r)/2 [dot S^2 + (D_i dot S)^2/M_K(r)^2] - G(r)/2 (D_i S)^2`

reproduces this exactly. Corrected run `32528572862`, artifact `9463080405`, digest `sha256:30af13757eb4b78553f97d1b887c11f6eb690a7f7bb02550bb03c11096211113`.

The rank-one Dirac mechanism and invertible lapse/shift Schur bridge show that an isolated aligned two-field kinetic sector can retain one physical scalar and one source-channel pole. Bridge run `32525916760`, artifact `9462166939`, digest `sha256:1b23375d2dbd6af5076c3bb9b1404bc4cd84cec5702fc0831ff93e3d3a35dc77`.

### Important alignment/embedding restrictions

For rank-one IR and mixed kinetic directions `v,w`,

`det(A vv^T + s B ww^T) = A B s (v1 w2-v2 w1)^2`.

Thus exact one-scalar rank preservation requires `w || v`. Run `32528978511`, artifact `9463185301`.

Simply adding a healthy independent companion to the already propagating DBI scalar opens a second kinetic direction; run `32529167558`, artifact `9463249160`.

If the same aligned combination carries the rolling DBI background, it cannot simultaneously be background-silent. Run `32529238991`, artifact `9463273507`.

For a separately normalized rolling scalar, the exact mixed coefficient fixes the invariant product `C q^2 = M_Pl^2`, so making the background speed `q` small does not remove the direct acceleration-strength problem. Run `32529333288`, artifact `9463302781`.

These are scoped restrictions, not a no-go for gauge/constraint cancellations or nonminimal matter frames.

### U(1) gauge/constraint frontier

The extra-local-U(1) Hořava literature provides explicit parameter families where all PPN parameters take GR values. Publicly stated examples include:

1. `a1 = kappa = 1`, `sigma2 = 0`;
2. `sigma2 = 4(1-a1)`, `beta0 = -2(gamma1+1)`.

For the direct rolling RTK acceleration normalization, the action convention maps to `beta0_RTK=2`. Under canonical IR curvature normalization `gamma1=-1`, explicit family 2 gives `beta0=0`, so that family does not contain the direct RTK slice. Executable source commit `bb04a706a7742005569dfa5feeb27bc59e42ef8c`; workflow `343943c6d35404c72bf7dbd830ed846a2bce3065`; trigger `1ad8f32ce6d857016cc1717d135ac06081df4164`.

Family 1 does not itself fix `beta0`; therefore its displayed algebraic GR-PPN conditions do not exclude `beta0=2`. This is **not** a PPN certification. Executable source commit `21fff2f9911350bd4fe4d701559acaf71821705d`; workflow `fbab5cb514d7babee97cfc68c12bcd2eae1d84cb`; trigger `4247ed53d5d9f4d7850318c6ea34a03c6a467fd9`.

Next C8 gate: after CI artifacts, freeze one concrete family-1 `beta0=2` parameter/matter tuple and derive/solve its IR static equations and full constraint/DOF structure. Radiative stability/C9 must be applied early because exceptional U(1) scalar-removal surfaces are not automatically technically natural.

## Iteration timing provenance

Current user-driven iteration started `2026-08-22 02:46:00 UTC+03:00` / `2026-08-21 23:46:00 UTC`.

Append-only fragment: `research/iteration_chronology/2026-08-22T024600+0300.md`, commit `08733e532645b572e9d61609189704347e8bd034`.

## Immediate research order

1. Inspect B4 target-v2 half-scale eigenmode-ray run; recenter if any exact descent exceeds `0.005`, otherwise quarter-scale Hessian audit.
2. Inspect B9 RTK half-scale; if recenter-clear + PD, launch fresh-tree replay.
3. Inspect B9 LCDM recenter-v2 base; recenter/rays/half mechanically.
4. Inspect the U(1) family-II and family-I CI artifacts; never interpret family-I algebraic openness as a PPN pass.
5. Freeze and test one complete U(1) family-I `beta0=2` static/matter tuple if the algebraic gates pass.
6. Apply DOF, ghost/gradient/hyperbolicity, Newton/PPN, GW, compact-object, radiative-stability and EFT-cutoff gates to the **same fixed action/tuple**.
7. Validate home-runner 12-worker bootstrap before routing unique scientific work there.

## Interpretation discipline

Workflow success means only that encoded assertions executed. Scientific closure requires the frozen acceptance rule and exact stated scope. A scoped no-go must never be promoted to a no-go for RTK or all completions. A diagnostic algebraic opening must never be promoted to viability before the full same-tuple physical gates are passed.
