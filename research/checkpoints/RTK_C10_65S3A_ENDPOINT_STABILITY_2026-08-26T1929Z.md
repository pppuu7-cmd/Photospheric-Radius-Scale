# RTK C10.65s3a endpoint stability checkpoint

Classification: `C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_PASS_SCOPED`. Original s2 remains `C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED`; s2k remains `C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED`.

Frozen interval: `9.99999999999999955e-07` Mpc, unchanged production kernel/tolerance.

- k=1e-05: accepted=6, rejected=4, min_hdid=1.94154616823396927e-09, max_hdid=4.86313467717991443e-07
- k=3e-05: accepted=6, rejected=6, min_hdid=1.30026907430720316e-09, max_hdid=7.11517529339289467e-07
- k=0.0001: accepted=6, rejected=4, min_hdid=1.69138817290330697e-09, max_hdid=7.06347847767574422e-07
- k=0.0003: accepted=7, rejected=5, min_hdid=1.11352665520857552e-09, max_hdid=7.96203550765069866e-07

Maximum endpoint normalized A/H/M residual: `2.99880304840224160e-16`; maximum normalized change: `2.99880304840224160e-16`; frozen bound: `1.00000000000000004e-10`.

This is endpoint-only scoped stability, not a full-trajectory or cosmological stability theorem.
