# RTK C10.65s2 implementation frontier — 2026-08-26T17:40Z

## Canonical branch
`rtk-class-build`

## Last closed gates
- C10.65r2 — `C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED`
- C10.65s0 — direct-onset/state-vector architecture pass, with legacy nlde perturbation auxiliaries excluded from completed mode
- C10.65s1 — `C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED`
- C10.65s2a — `C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_PASS_SCOPED`

## Current open gate
`C10.65s2` under the already frozen target:
`research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json`

Do not create a replacement target and do not change any frozen criterion.

## Frozen domain
- lambda_HL = 1.0016708437761068
- M_c = 9066.231026460177 Mpc^-1
- a_on = 0.0002203229136467
- k = [1e-5, 3e-5, 1e-4, 3e-4] Mpc^-1
- TCA ON, RSA=0, UFA=0, l_max_ur=17

## Source-locked handoff manifest
Use `research/theory_results/RTK_C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_RESULT_v1.json` as the implementation source manifest. It cross-locks the first persisted C10.65s1 finite state to the certified C10.65r2 first RHS and verifies the Newtonian Phi_N constraint via metric Euler at <=5e-9.

## Non-negotiable implementation architecture
1. Opt-in flag `c10_65s2_canary`, default 0.
2. OFF path must remain numeric-text SHA256 identical to the s1 control for all four anchors.
3. The completed canary starts directly at the certified tau_on corresponding to a_on; no uncertified pre-onset completed trajectory is imported.
4. Ordinary photon/baryon/UR/metric initial state must be filled through `perturb_initial_conditions` / initial `perturb_vector_init` ownership. Do not mutate those coordinates inside `perturb_derivs` or at a later adaptive callback.
5. The only post-vector integrated carrier writes allowed by the frozen architecture are:
   - `pv->y[index_pt_delta_cdm]`
   - `pv->y[index_pt_theta_cdm]`
   These are the certified Khronon carrier slots.
6. Do not allocate/use historical dU,dUprime,dV,dVprime,dZ,dZprime as completed-U1 perturbation state on the opt-in path.
7. Historical background contribution is not rederived or removed by this perturbation canary; same-full-action background closure remains separately open.
8. Newtonian metric/projector feedback on the s2 opt-in path must use completed-U1 Phi_N / Psi_N_prime and the certified completed projector algebra, not historical model=2 dZ/dV constraints.
9. Do not modify TCA/RSA/UFA switching criteria, collision coefficients, or approximation logic except the deterministic direct-onset start/split already certified by s0.
10. No independent extra temporal, metric, or shift datum may be introduced.

## Required runtime measurement
For each of the four anchors:
- capture the state exactly at onset before the accepted step;
- capture the first production RHS before the step;
- compare the production RHS to the certified C10.65r2 values with frozen max relative error 5e-9;
- advance exactly one accepted post-handoff integrator step;
- capture the post-step state and require all outputs finite;
- capture preferred A, Hamiltonian and momentum constraints before and after;
- report raw, signed, absolute and normalized changes only. s2 has no post-hoc numerical drift threshold.

## Static guards required by frozen target
- exact OFF rollback;
- legacy nlde completed-state exclusion;
- handoff write-site guard;
- ordinary-state initialization ownership guard;
- no switching/collision mutation;
- no unlisted state or metric boundary datum;
- unchanged r2 RHS tolerance.

## Next action
Implement a disposable pinned-CLASS s2 patch plus analyzer/workflow against the source map certified by s2a. The workflow must build an s1 control and s2 opt-in tree, prove exact OFF identity first, run the four frozen anchors, persist PASS or FAIL result with immutable provenance, and fail CI on `FAIL_SCOPED`. If the implementation hits an architectural requirement outside the frozen allowed writes/ownership contract, stop s2 implementation and freeze a separate architecture proof before changing production state handling.

## Global open items not to conflate with s2
- C9 radiative naturalness remains open.
- same-full-action primordial/background closure remains open.
- broader C7/PPN/positivity and B9 global certification remain separate.
- no spectra or likelihood claim is licensed by s2.
