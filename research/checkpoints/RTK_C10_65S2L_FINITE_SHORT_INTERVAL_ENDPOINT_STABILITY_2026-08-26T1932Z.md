# RTK C10.65s2l finite-short-interval endpoint stability checkpoint

Classification: `C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_FAIL_SCOPED`. Original C10.65s2 remains `C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED`; C10.65s2k remains `C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED`.

The interval and terminal normalized constraint bound were frozen before execution: interval `3.53993611477497e-08` Mpc (100 x s2k width), endpoint |A|,|H|,|M| <= `1e-8`. Equations, state ownership, approximation criteria and perturbation tolerance were unchanged.

Adaptive trace:
- k=0.0001: accepted=4, rejected=3, min_hdid=1.102604172766757e-09
- k=0.00029999999999999997: accepted=4, rejected=2, min_hdid=2.5074906403787403e-09
- k=1.0000000000000001e-05: accepted=4, rejected=2, min_hdid=3.343168236363952e-09
- k=3.0000000000000001e-05: accepted=5, rejected=4, min_hdid=9.017227388293345e-10

Terminal normalized constraints:
- k=0.0001: A=0.000e+00, H=0.000e+00, M=0.000e+00
- k=0.00029999999999999997: A=0.000e+00, H=0.000e+00, M=2.999e-16
- k=1.0000000000000001e-05: A=0.000e+00, H=0.000e+00, M=0.000e+00
- k=3.0000000000000001e-05: A=0.000e+00, H=0.000e+00, M=0.000e+00

This gate does not bound intra-step or accepted-step peak constraints and is not a long-time stability claim.
