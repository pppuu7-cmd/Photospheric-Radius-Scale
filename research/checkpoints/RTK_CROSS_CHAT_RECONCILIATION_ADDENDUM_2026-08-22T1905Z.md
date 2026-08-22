# RTK cross-chat reconciliation addendum — 2026-08-22 19:05 UTC

This addendum updates `RTK_CROSS_CHAT_RECONCILIATION_2026-08-22.md` with results that completed during the audit.

1. Corrected moving-source O(3) clock theorem: run `32592515149` **SUCCESS**, artifact `9480692739`, digest `sha256:c512c1274832fe1c1c3b40428512da5d2116c92ffb5e6e23e9e747d3eee4ceac`. The previous red run was only a SymPy structural-equality assertion bug. Scoped result: on the regular family-I `lambda_HL != 1` branch the homogeneous fixed RTK clock has zero O(3) moving-matter source, so it does not shift the published family-I `alpha1=alpha2=0` at that PN order. Exact `lambda_HL=1`, higher PN and strong-field/binary response remain open.

2. Universal-matter FLRW/PPN/DOF trilemma: run `32592531836` **SUCCESS**, artifact `9480698523`, digest `sha256:da15f07ddd388f3129c7c3db98645a0e353b76dc5f97936d87d7f457510aca43`. Classification `BLACK_SCOPED_PUBLISHED_UNIVERSAL_MATTER_NO_COMPENSATOR_CLASS`: evolving flat-FLRW ordinary dust, the `sigma1=sigma2=0` no-extra-gravity-scalar surface, and the published universal-matter PPN branch cannot be combined in the unchanged no-compensator architecture. This is not an RTK/U1 general no-go.

3. B9 LCDM recenter-v5: run `32587768594` **SUCCESS**, artifact `9480669429`, digest `sha256:5c87e4aa2fb647c87b5a4a4423197d3d01d853cdb8f97e521130d02477b709f8`. Scientific result: Hessian positive definite but exact improvement `0.04857762431061019 > 0.005`; therefore v5 is not stationary and mandatory recenter-v6 was frozen at commit `adc1eba84521b35df509a93a98e4ecc7e72556b0`. V6 workflow commit `ef8564d69901c9aafaebdb46de88a2cb5c3a70ec`; launch commit `260da72f7dd81206b319daab9c1d722c3e673f5e`.

4. B4 v4 half-resolution run `32587822698` remains in progress at this timestamp.

These completions strengthen the main reconciliation conclusion: the high-value neighboring-chat content is now substantially durable; remaining work is mostly synchronization of older summary indices and two primary-source re-audits (recovered BPS small-coupling cutoff scaling and detailed slowly-moving compact-object regularity boundary).
