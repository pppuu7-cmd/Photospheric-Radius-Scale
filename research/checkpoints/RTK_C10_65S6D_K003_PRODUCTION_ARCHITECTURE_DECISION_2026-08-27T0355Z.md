# RTK C10.65s6d k=0.03 production architecture decision

Classification: `C10_65S6D_K003_PRODUCTION_ARCHITECTURE_DECISION_PASS_SCOPED`.

Decision: `REQUIRE_STRONGER_UV_PRE_EFT_MATCHING_BEFORE_K003_PRODUCTION`.

Maximum key metric/carrier response: `1.47481443935257972e+00`. Responses at or above the frozen order-unity boundary: `{'delta_b': 1.4748144393525797}`.

No k=0.03 production output was consumed. If production is blocked, return to the UV/pre-EFT matching interface rather than tuning production branches.
