# RTK C10.65s4d moderate-k one-step production canary checkpoint

UTC checkpoint: 2026-08-26T21:30Z
Branch: `rtk-class-build`
Pinned CLASS upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`
Scientific workflow run: `33014408144` (successful final rerun job)
Classification: `C10_65S4D_MODERATE_K_ONE_ACCEPTED_STEP_PRODUCTION_CANARY_PASS_SCOPED`

## Recovered frontier

The parent chain used by the frozen s4d target is preserved:
- C10.65s4b moderate-k completed onset seed: PASS_SCOPED.
- C10.65s4c moderate-k current-state first-RHS parity: PASS_SCOPED.
- C10.65s2k low-k one-accepted-step retry: PASS_SCOPED.
- Historical C10.65s2e remains FAIL_SCOPED and is not reclassified.

The frozen s4d domain is exactly the first completion point and two moderate-k modes:
`k = 1e-3, 3e-3 Mpc^-1`.
The retry step width is inherited prospectively from s2k; integrator/kernel tolerances and completed-U1 equations are unchanged.

## Harness failures before scientific execution

The first attempts of run 33014408144 died before any OFF rollback or canary execution. They are infrastructure/software failures, not scientific s4d failures.

1. The domain patch searched for the Python f-string source spelling `S[4]={{...}}` instead of the rendered C initializer `S[4]={...}`. The patch was changed to a structural generated-C regex bounded by the following `DT` declaration.
2. A whole-file postcondition searched for the bare substring `0.0001` and falsely matched unrelated constants. It was replaced by parsing only the first field of the actual `S[2]` seed rows and checking the domain numerically.
3. The frozen workflow snapshot accepted two textual serializations of the same binary64 retry width, while `.17g` emitted another equivalent round-tripping representation. The domain adapter now writes the same binary64 `DT` using a canonical `.16g` representation and explicitly asserts that reparsing it gives exactly the frozen target float. No numerical width changed.

No scientific threshold, equation, mode, completion parameter, tolerance, or pass criterion was relaxed in these fixes.

## Final frozen result

Persisted result:
`research/theory_results/RTK_C10_65S4D_MODERATE_K_ONE_ACCEPTED_STEP_PRODUCTION_CANARY_RESULT_v1.json`

All frozen checks pass, including:
- exact dormant OFF identity;
- exact onset/domain ownership;
- moderate-k seed only / no low-k seed lookup;
- no legacy nlde physical role and no double gauge transform;
- first-RHS parity against s4c;
- same production kernel and integrator tolerance;
- exactly one accepted no-rejection Cash-Karp step;
- finite post-step state and finite A/H/M/traceless constraint capture;
- `threshold_changed=false`.

Numerical worst cases:
- max first-RHS relative difference vs s4c: `4.262129182962879e-11`;
- max kernel-metric relative difference vs s4c: `1.2128517215502012e-13`;
- boundary carrier relative error: `0`;
- higher-UR boundary relative error: `0`;
- largest measured post-step normalized momentum-constraint residual/change: `3.0083646253800744e-16` at `k=3e-3 Mpc^-1`;
- A and Hamiltonian residual changes are zero at the serialized precision for both modes.

Observed accepted widths were `3.539923909556819e-10 Mpc` for both modes, consistent with the frozen retry-width machinery. The target width itself was not changed.

## Interpretation

This is a scoped production-entry certificate only. It establishes that the s4b moderate-k completed onset carrier can enter the unchanged completed-U1 production kernel, reproduce the s4c first RHS, and survive one accepted Cash-Karp step at both moderate-k anchors while preserving exact OFF rollback.

It is NOT a finite-time moderate-k stability result, not broad-k stability, not validation of k=0.01 or 0.03 Mpc^-1, not a UV derivation of higher UR multipoles, not same-full-action primordial/background closure, not massive-neutrino completion, and not spectra/likelihood evidence.

## Next gate

Per the frozen s4d result, the next scientific gate is C10.65s4e: freeze a moderate-k finite-short-trajectory target on exactly these two modes, with every sample-time/accepted-state policy and any trajectory constraint-residual bound fixed before execution. Do not widen k or the completion-parameter domain before that gate passes.

Fundamental open gates remain independent: C9 radiative naturalness, same-full-action primordial/background closure, microscopic UV matching/higher-UR derivation, and massive-neutrino completion.
