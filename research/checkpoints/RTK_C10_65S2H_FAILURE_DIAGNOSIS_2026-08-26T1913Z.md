# RTK C10.65s2h failure diagnosis checkpoint

Classification: `C10_65S2H_FAILURE_DIAGNOSIS_PASS_SCOPED`.

Original C10.65s2 remains `C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED` and is not reclassified. The physical/onset/OFF/RHS/finite/constraint checks passed; the genuine failed scientific execution requirement was exactly one accepted post-handoff step.

Pinned Cash-Karp accounting on the immutable s2 observer gives: k=1e-05: >= 4 accepted, k=3e-05: >= 5 accepted, k=0.0001: >= 5 accepted, k=0.0003: >= 4 accepted. Thus the frozen 1e-4 Mpc interval was adaptively split into multiple accepted substeps; this is not explained by rejected trials alone.

The second original failure, `thermo_signature_fix_only`, is diagnosed as an analyzer literal-string false negative. The executed v3 patch explicitly describes the change as `No physics or frozen criteria change` and `compile-only thermo/prototype fixes`; all other static guards passed, OFF numeric identity was exact, and first production RHS parity remained far inside the frozen 5e-9 bound.

No threshold or retry width was changed or selected in s2h. Next gate: freeze C10.65s2i diagnostic instrumentation at the same 1e-4 Mpc interval and unchanged tolerance, record accepted `hdid`/`hnext` and rejection counts in the actual pinned production integrator, then only prospectively freeze a retry width in a later gate.
