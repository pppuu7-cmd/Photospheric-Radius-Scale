# RTK C10.65s5d multibranch one-step production-entry checkpoint

UTC checkpoint: 2026-08-26T23:35Z
Branch: `rtk-class-build`
Classification: `C10_65S5D_NEXT_K_MULTIBRANCH_ONE_STEP_PRODUCTION_CANARY_PASS_SCOPED`.

## Recovered parent frontier

- C10.65s5a: near-horizon onset-state preflight PASS scoped at k=0.01 Mpc^-1.
- C10.65s5b: completed onset seed/domain audit PASS scoped.
- C10.65s5c: preregistered 27-point omitted-order sensitivity map PASS scoped, but with non-negligible response; it is not a UV uncertainty probability distribution.
- Historical C10.65s2e remains FAIL scoped and is not reclassified.

## Frozen s5d design

Before production execution, s5d fixed three branches from the already-executed s5c response envelope:

1. `baseline`: eta_D=0, eta_C=0, eta_S=0.
2. `joint_extremum`: eta_D=-1, eta_C=-1, eta_S=-1.
3. `phi_extremum`: eta_D=-1, eta_C=-1, eta_S=+1.

The test kept the existing completed-U1 production kernel, RK integrator/tolerance and inherited C10.65s2k one-step width. It required exact dormant OFF rollback, current-state first-RHS parity, finite state/constraint diagnostics and exactly one accepted no-rejection step. Constraint drift was measurement-only.

## Harness history

Run 33023567159 stopped before physics because `mpmath` was absent from the fresh Python environment. Pinned `mpmath==1.3.0` was added; no target or threshold changed.

Run 33023699457 stopped before physics because the branch adapter placed its `s=s.replace(...)` statement inside a one-line Python `if` suite. The adapter control flow was split onto separate lines; no target, equation, branch or threshold changed.

Run 33023782012 executed the full frozen gate and passed.

## Final s5d measurements

- exact dormant OFF identity: PASS for all three branches;
- boundary carrier reproduction: max relative error 0;
- higher-UR historical-control reproduction: max relative error 0;
- independent first-RHS parity: max relative error `4.441607914714873e-12` against frozen `5e-9`;
- current-state kernel metric parity: max relative error `1.556334652245679e-13` against frozen `5e-9`;
- approximation state preserved: TCA/RSA/UFA=(0,0,0), l_max_ur=17;
- measured one-step width for all branches: `3.539923909556819e-10 Mpc`, within the frozen absolute width tolerance;
- all post-step states and constraint diagnostics finite;
- largest measured normalized constraint change was the baseline momentum constraint, `3.1096286799641316e-16`; phi-extremum momentum change was `2.9987067315926926e-16`; joint-extremum A/H/M/T changes serialized as zero.

The scientific result is therefore a multibranch production-entry certificate at k=0.01 Mpc^-1 only. It does not establish finite-time stability, does not prove that the true omitted O(k^4) terms are contained by the s5c envelope, and does not justify widening to k=0.03 Mpc^-1.

## Next gate

Freeze C10.65s5e before implementation: finite-short-trajectory sampling on these same three prospectively fixed branches at k=0.01 Mpc^-1. Reuse the already certified endpoint-restart sampling architecture, freeze elapsed times and normalized A/H/M/T residual bounds before execution, preserve exact OFF identity and unchanged production kernel/tolerance, and keep the s5c envelope explicitly non-probabilistic. Do not widen k before s5e.

Still open outside this scoped bridge: C9 radiative naturalness, same-full-action primordial/background closure, microscopic UV/pre-EFT matching of the omitted-order coefficients/higher-UR hierarchy, and massive-neutrino completion.
