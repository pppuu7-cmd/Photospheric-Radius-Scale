# RTK C9 projectability structural-protection checkpoint

- Classification: `RTK_C9_PROJECTABILITY_STRUCTURALLY_ELIMINATES_SIGMA12_OPERATOR_PAIR_PASS_SCOPED`
- Status: `PASS_SCOPED`
- Frozen target: `research/theory_targets/RTK_C9_PROJECTABLE_STRUCTURAL_PROTECTION_TARGET_v1.json`
- GitHub Actions run: `33136256703`
- Execution SHA: `f5ecc8e685a2b47e781ea029addce9aca4e886bf`
- threshold_changed: `false`

## Exact scoped result

For exact projectability `N=N(t)`, every spatial derivative `D_i N` vanishes. Hence `a_i=D_i ln N=0`, and both C9 obstruction operators `a_i a^i sigma` and `D_i a^i sigma` vanish identically for arbitrary coefficients. This is structural elimination of this operator pair on projectable field space, not coefficient tuning.

## Scope boundary

This does **not** close C9 for the original nonprojectable fixed U1+RTK action and does not establish full radiative naturalness of the projectable HMT candidate. Other radiatively dangerous gravitational/matter operators remain to be audited. It does not unblock soft-s or `k=0.03 Mpc^-1` production.

## Next gate

Audit whether the projectable HMT candidate introduces other radiatively dangerous scalar-sector operators or matter Lorentz-violating couplings that replace the eliminated sigma1/sigma2 problem; require a same-action counterterm/RG argument before any full C9 closure.
