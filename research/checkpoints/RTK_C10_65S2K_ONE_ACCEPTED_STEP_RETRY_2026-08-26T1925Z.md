# RTK C10.65s2k one-accepted-step retry checkpoint

Classification: `C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED`. Original C10.65s2 remains `C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED`.

Prospectively frozen retry width: `3.53993611477497021e-10` Mpc. Integrator tolerance and completed-U1 equations were unchanged. BEFORE observer rows were required to exactly reproduce the immutable original s2 boundary/RHS record; OFF numeric perturbation files were required SHA-identical to control. AFTER required exactly seven RHS calls on every anchor, corresponding to one accepted Cash-Karp trial with no rejection.

Constraint residual changes are retained as measurement-only diagnostics; this gate is not a finite-time stability claim.

Next gate if PASS: freeze a separate finite-short-interval/multi-step stability target with its interval and drift tolerance fixed before execution.
