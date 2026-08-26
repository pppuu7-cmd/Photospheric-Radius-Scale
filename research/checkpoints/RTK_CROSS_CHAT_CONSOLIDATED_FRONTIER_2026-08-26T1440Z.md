# RTK cross-chat consolidated frontier — 2026-08-26T14:40Z

Authoritative repo/branch: `pppuu7-cmd/Photospheric-Radius-Scale` / `rtk-class-build`.
Pinned CLASS upstream: `dirian/class_public`, branch `nonlocal`, SHA `36cf283628c4a3330ec9fd3d84239bf775f77317`.

This checkpoint consolidates the current repository frontier with material recovered from earlier RTK 1/2/3/4, Research Loop, Auto-Continue/Auto-Advance, Stage 4D1, B9 and related chats. It is a recovery document, not a new physics claim.

## Current C10.65 completed-U1 / initial-condition frontier

Closed chain through C10.65r2:
- corrected generic adiabatic condition is `Delta I_iso = I_khr - J_ad = 0`; absolute `I_khr=0` is a special zero-charge sector, not generic cosmological adiabaticity;
- pinned ordinary control gives `J_ad -> -3` at low k;
- exact onset `a_on = 0.0002203229136467` and low-k anchors `1e-5,3e-5,1e-4,3e-4 Mpc^-1`;
- TCA domain boundary `k_TCA ~= 0.086419535657 Mpc^-1`;
- finite-onset snapshot rank and any finite local time jet cannot select the primordial growing branch;
- no certified pre-onset coupled low-k support interval exists in the persisted production branch, so primordial selection remains explicitly pre-EFT/UV matched unless a new earlier completed-U1 background is independently constructed;
- normalized UV/pre-EFT matching basis has nine coordinates `(A2,E_gb2,E_urb2,E_khr2,R_gb0,R_urb0,R_khrb0,S_ur0,C2)`, where `R_khrb0=V_khr,pref0+B0-V_b,N0`;
- historical phenomenological control only: `A2=-1120.906563855608`, `S_ur0=298.90841588141416`, `C2=-1.314425482950032`, other relative entropy/velocity coordinates zero;
- detached completed-U1 onset chain n/o/p/q closes metric, radiation shear, B', Psi_N' and source-locked compromise_CLASS slip without extra metric/shift temporal data;
- C10.65r2g isolates the read-only first-RHS observer in a separate noinline/noclone translation unit, restoring exact dormant OFF-path identity;
- original frozen C10.65r2 has now passed on the full 3x3 completion grid x four exact low-k onset anchors, with its original frozen analyzer and thresholds unchanged.

C10.65r2 full-grid worst checks:
- exact dormant OFF SHA identity: PASS on all four anchors;
- grid points: 9; records per point: 4;
- max r1 projector regression relative: `0`;
- max C vs independent local RHS relative: `2.0625432202795618e-10`;
- max C vs detached parent RHS relative: `2.0625432202795618e-10`;
- max Bprime actual-slip invariance relative: `0`;
- max weighted photon+baryon slip cancellation normalized residual: `2.134955834845e-16`;
- no-dy-write and no-production-metric/RHS-write static guards: PASS.

Interpretation: this is first-RHS diagnostic parity inside real pinned CLASS only. It is not yet state handoff or production feedback.

## Next C10.65 architecture

The next gate must be a controlled state-handoff / one-or-short-step completed-U1 integration test. Do not mutate integrator state from inside an ordinary adaptive RHS callback.

Pinned CLASS source audit: `perturb_solve()` explicitly divides evolution into intervals of uniform approximation scheme. At interval starts it calls `perturb_vector_init()`: with `pa_old==NULL` it initializes a new k mode, and at an approximation-switch boundary it redistributes the old integrated vector into the new one. Constraint quantities are not stored as independent integrated components. This interval/vector-init mechanism is therefore the preferred integration-safe handoff architecture.

Next gate requirements should include:
1. opt-in switch default OFF;
2. exact rollback: OFF reproduces the prior production path exactly;
3. explicit deterministic boundary at `a_on`/corresponding tau, not a hidden one-time RHS side effect;
4. conditional historical matching vector clearly labeled as phenomenological control only;
5. controlled write only to genuine integrated state variables; completed metric/shift remain algebraic projected quantities;
6. first post-handoff RHS parity against C10.65r2;
7. one/short-step finite evolution with constraint-drift diagnostics;
8. TCA/approximation state at handoff certified and no collision/switch coefficients changed;
9. rollback/disable path tested before expansion in k or spectra.

## Recovered global RTK constraints from older chats

### B9 / likelihood candidate
An older authoritative matched-cosmology result preserved:
- `S_RTK = 1050.249912429787`
- `S_LCDM = 1049.966118347761`
- local `Delta S = +0.2837940820259064`.
This is a local matched comparison, not global optimality, Bayes evidence or statistical significance.

A separate B9 candidate with `S_B9 = 1059.2759492715309` and 140 exact points/boundary guard existed in older work, but stationarity/Hessian and paired-LCDM certification were not completed; an LCDM job had been cancelled after partial evaluations. Therefore B9 is NOT globally/fully certified and must not be reported as closed until those gates are replayed/verified from repository evidence.

### C7 / U-DHOST
Two levels must not be conflated:
- algebraically, class-I DHOST with `c_GW=1` can admit nonzero `beta3`; existence of an algebraic benchmark is not a general no-go;
- however the direct minimal U-DHOST carrier on the same asymptotic background has the PPN conflict `beta3=gamma^2`, `G_GW/G_N=gamma^2/2`, giving approximately `G_GW/G_N~0.5` and `alpha1~-4` for `gamma~1`, incompatible with weak-field bounds. Allowing fixed `M^2(X)` on that same asymptotic background does not remove this algebraic conflict.

Thus direct minimal same-background carrier is disfavored/closed under those assumptions, but the broader C7 program remains OPEN for environmental `X_local != X_FLRW`, nontrivial matter/disformal frame map, additional operators/fields, and full positivity/matter-coupling/exact-mapping checks.

## Global open lines not closed by C10.65
- C9 radiative protection/naturalness of the exceptional parameter surface;
- same-full-action primordial/background/gravity normalization;
- massive-neutrino completion;
- B9 stationarity/Hessian + paired-LCDM certification;
- broader C7 PPN/positivity/matter coupling/exact mapping beyond the direct minimal same-background carrier;
- microscopic derivation of the UV/pre-EFT matching vector.

No C10.65 diagnostic pass should be promoted to a claim that the full RTK theory is proven or globally preferred by data.
