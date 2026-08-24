# RTK iteration chronology — A5 recenter1 + same-action static/PPN continuation

Timestamp: **2026-08-24T17:35:00Z**

This checkpoint is chat-independent. It records only persisted scientific results and frozen/active gates. Workflow absence or success is not itself a scientific classification.

## 1. A5 cross-basin LCDM frontier

The t=1.1 LCDM navigation point was tested by the preregistered half-scale Hessian and did **not** pass the recenter gate despite positive-definite curvature.

Persisted result:

- `research/robustness/A5_LCDM_T1P1_HALF_RESULT_v1.json`
- scale: `0.5`
- center score: `1049.3633203461363`
- center replay abs error: `2.2737367544323206e-13`
- positive definite: `true`
- minimum Hessian eigenvalue: `0.019510024973060546`
- best exact score: `1049.3550570964142`
- best exact label: `newton_trust_eff`
- exact improvement: `0.008263249722176624 > 0.005`

Therefore the frozen decision rule requires a mandatory recenter. No fresh-tree replay or paired A5 refreeze is admissible yet.

New exact recenter1 center:

- `As = 2.098490857524975e-09`
- `Ob = 0.048382880062392684`
- `Om = 0.25847022980776346`
- `h = 0.6804976358942407`
- `lam = 0`
- `ns = 0.9664964612260075`
- `zre = 7.67518361771309`
- expected `S_eff = 1049.3550570964142`

Frozen before recenter1 scores:

- base target `research/robustness/A5_LCDM_T1P1_RECENTER1_STATIONARITY_TARGET_v1.json`, commit `5c7e296944e9a5f65e33f96e8d29aeb71caf812b`;
- conditional half target `research/robustness/A5_LCDM_T1P1_RECENTER1_HALF_STATIONARITY_TARGET_v1.json`, commit `c79930063dc4d552e140cebcb8a832b1a1526a66`;
- base workflow `main:.github/workflows/rtk-a5-lcdm-t1p1-recenter1-stationarity-base.yml`, commit `71179e7a5f775a32cfdeeab20e0da23fb24b96a7`;
- half workflow `main:.github/workflows/rtk-a5-lcdm-t1p1-recenter1-stationarity-half.yml`, commit `98778af5961965fa076113d373e3aa7908cea26d`;
- launch commit `a8592af220aa1313d43301560de5ba2987a98052`.

The base workflow dispatches half only if the persisted base result has improvement `<=0.005` and is positive definite. Otherwise it stops on the appropriate frozen branch.

At this checkpoint `A5_LCDM_T1P1_RECENTER1_BASE_RESULT_v1.json` has not yet persisted. Status: **PENDING, not FAIL**.

## 2. B4 / B5 parallel compute

B4 remains at the recovered v4 half non-PD center with exact half-eigenmode rays active. The expected persisted ray result

`research/robustness/B4_NEUTRINO_RTK_RECENTER_V4_HALF_EIGENMODE_RAYS_RESULT_v1.json`

has not yet appeared. Do not route to quarter scale unless the persisted result explicitly classifies the ray gate as no exact descent above `0.005`.

B5-LIN remains active under the frozen BOSS interval `k=0.02..0.24 h/Mpc`, `z={0.38,0.51,0.61}`. The result

`research/robustness/B5_BOSS_LINEAR_SCALE_DEPENDENCE_RESULT_v1.json`

has not yet appeared. Even a B5-LIN pass cannot close the separate B5-SURVEY window/AP/nonlinear-template/bias scope.

## 3. Same-action static RTK scalar theorems now persisted

### 3.1 Exact scalar EOM

`research/theory_results/RTK_ROUTE_B_U1_STATIC_CLOCK_SCALAR_EOM_RESULT_v1.json`

Classification: `RTK_ROUTE_B_U1_STATIC_CLOCK_SCALAR_EOM_EXACT_PASS`.

For time-independent `N,g_ij`, zero invariant shift and `Sigma=q t`, the first scalar variation reduces after integration by parts to the time derivative of static coefficients; the scalar EOM vanishes exactly.

### 3.2 Exact static variation bridge

`research/theory_results/RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_RESULT_v1.json`

Classification: `RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_EXACT_PASS`.

For `C(X_U)=M_Pl^2/(2X_U)` the full first variation of the mixed operator on the static rolling branch is exactly that of `M_Pl^2 a_i a^i`; no direct `A` source and no linear invariant-shift source appear. The old fixed-C cubic-mismatch interpretation is superseded.

### 3.3 DBI real-domain bound

`research/theory_results/RTK_ROUTE_B_U1_STATIC_DBI_REALITY_DOMAIN_RESULT_v1.json`

Classification: `RTK_ROUTE_B_U1_STATIC_DBI_REALITY_DOMAIN_SCOPED_PASS_WITH_NONUNIFORM_TAIL_BOUND`.

At the nominal solar-photospheric weak-field reference, the fixed finite lambda and both preregistered B10 tail anchors are inside the DBI-real static-clock domain. The formal fixed-nonzero-lapse `lambda_D -> infinity` limit is not uniform. This does not reopen B10 cosmological protocol-v1.

### 3.4 Exact O(2) Newton/gamma

`research/theory_results/RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_RESULT_v1.json`

Classification: `RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_PASS`.

With the universal matter frame `a1=1,a2=0` in the PPN gauge, `tilde N=N-A`. At O(2), `n=N-1=A2-U`, and the full DBI-corrected equation is

`4 [Delta n - mu_K^2 n] = 0`.

Regular asymptotic-flatness gives uniquely `n=0`, hence `A2=U`, `f=1`, `gamma_PPN=1`, and `G_N=G` for the frozen branch.

## 4. New exact nonlinear bare-lapse uniqueness theorem

Frozen target:

`research/theory_targets/RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_TARGET_v1.json`

Persisted result:

`research/theory_results/RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_RESULT_v1.json`

Classification: `RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_EXACT_PASS`.

On the regular asymptotically-flat, static, zero-invariant-shift, real-DBI-interior branch:

`2 D_i a^i + a_i a^i = F_N`,

with

`r=1/N-1`, `s=sqrt(1-lambda_D r^2)`,

`F_N = -2 mu_K^2 r(1+s+r)/[s(1+s)]`.

For `N>0,s>0`, `sign(F_N)=sign(N-1)`. With `u=sqrt(N)`, the exact identity

`2 Delta ln N + |grad ln N|^2 = 4 Delta u/u`

gives `4 Delta u=u F_N`. Multiplying by `u-1`, integrating and using the frozen boundary condition yields

`-4 integral |grad u|^2 = integral u(u-1)F_N`.

The left side is non-positive and the right side non-negative, so both vanish and

**`N=1` uniquely**.

Consequently on this certified static branch:

- `a_i=0`;
- `r=0`;
- `P=0`;
- `P_N=0`.

Thus the fixed RTK scalar is exactly background-silent there, rather than merely parametrically small.

Non-claims: this does not cover nonzero invariant shift/rotation, spatial Sigma gradients, DBI boundary `s=0`, `X_U->0` compact objects, radiative stability or the EFT cutoff.

## 5. Static beta_PPN now closed on the certified branch

Frozen-before-result target:

`research/theory_targets/RTK_ROUTE_B_U1_STATIC_BETA_PPN_INHERITANCE_TARGET_v1.json`

Persisted result:

`research/theory_results/RTK_ROUTE_B_U1_STATIC_BETA_PPN_RESULT_v1.json`

Classification: `RTK_ROUTE_B_U1_STATIC_BETA_PPN_EXACT_PASS`.

Using the nonlinear `N=1` theorem, the RTK DBI source has `P=P_N=0`, while the exact mixed static variation is already accounted for by the acceleration structure. The remaining static equations reduce to the corresponding nonprojectable U(1) family-I system. The `sigma1=sigma2=0` PPN expression must be simplified at `a1=kappa=1` before the apparent `gamma1=-1` singular form is evaluated; after cancellation it gives exactly

- `beta_PPN = 1`;
- `gamma_PPN = 1`.

This is a scoped weak-field static result, not a moving-source preferred-frame result.

## 6. O(v^3) moving-source / preferred-frame chain frozen and launched

To avoid improperly importing pure-U1 preferred-frame formulae, a separate vector-sector decoupling target was frozen first:

`research/theory_targets/RTK_ROUTE_B_U1_PPN_O3_SCALAR_SILENCE_VECTOR_TARGET_v1.json`

commit `341a12d6ee7c35bccd6f5b6d9506707302132afa`.

It requires standard PPN ordering, the already-certified O(2) `n2=0`, `D_i Sigma=0`, and the no-independent-homogeneous/incoming-scalar PPN boundary condition. The target checks that through O(3):

- `Theta_U=q+O(4)`;
- `X_U=X_star+O(4)`;
- `P(X_star)=P_X(X_star)=0`;
- `D_iTheta_U=O(4)`;
- the invariant shift enters `Theta_U` multiplied by `D_iSigma=0`;
- first variations of the RTK scalar action supply no O(3) vector/shift source.

Worker commit: `304da64d978f28a61177922727f2824fcf427071`.
Workflow commit: `eaee797512f9ddeb1f74ae98cf87bc8060e618ad`.
Launch commit: `3377bdbe7995b8575d1488d5788718abfcb2c3fa`.

The conditional preferred-frame target was also preregistered before the O(3) result:

`research/theory_targets/RTK_ROUTE_B_U1_PREFERRED_FRAME_INHERITANCE_TARGET_v1.json`

commit `ac38c95939c06bbf714eba2aaa7ecacf565cce06`.

It will execute only after a persisted O(3) scalar-silence PASS. It simplifies the `sigma1=sigma2=0` U(1) PPN formulae at `a1=kappa=1,a2=0` before taking the apparent `gamma1=-1` and `lambda_HL=1` limits. The preregistered expected cancellations are `alpha1=0` and continuous `alpha2=0`; these are **not yet authoritative RTK results at this checkpoint**.

At this checkpoint the O(3) result has not yet persisted. Status: **PENDING, not PASS/FAIL**.

## 7. Strict next actions

1. Inspect `A5_LCDM_T1P1_RECENTER1_BASE_RESULT_v1.json` when it persists and follow its frozen decision exactly.
2. Inspect the O(3) scalar-silence result. Only PASS permits the already-preregistered preferred-frame workflow.
3. Inspect B4 v4-half rays; route to quarter only on persisted no-descent classification.
4. Inspect B5-LIN; keep B5-SURVEY independent.
5. If preferred-frame PASS persists, update the fixed-action PPN checkpoint to the scoped weak-field tuple `beta=gamma=1, alpha1=alpha2=0`, while retaining compact-object, radiative, strong-coupling and UV gates as open.
6. Do not modify canonical `research/state/current.json` A5 pair until the recenter chain, fresh-tree and common paired replay pass.
