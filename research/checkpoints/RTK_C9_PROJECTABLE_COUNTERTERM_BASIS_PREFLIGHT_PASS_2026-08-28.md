# RTK C9 projectable counterterm-basis preflight

- Classification: `RTK_C9_PROJECTABLE_SYMMETRY_ALLOWS_NONVANISHING_FINITE_K_COUNTERTERM_DIRECTIONS_PASS_SCOPED`
- Status: `PASS_SCOPED`
- GitHub Actions run: `33136913046`
- Execution SHA: `1e2018843f8724e67ed6a592bab70c4adde76013`
- threshold_changed: `false`

## Exact scoped result

Projectability still gives `a_i=0`, but invariant carrier gradients need not vanish. For a finite Fourier mode, the symmetry-allowed representatives are `O2 = k^2 deltaPhi^2/a^2` and `O4 = k^4 deltaPhi^2/a^4`; independent coefficients multiplying them survive.

## Scope boundary

This is a counterterm-basis/symmetry preflight only. It does not assert that either operator is generated with a nonzero beta function and does not compute loop coefficients. Full C9 remains open. Soft-s and `k=0.03 Mpc^-1` production remain blocked.

## Next gate

Perform a same-action radiative-evaluability/source-lock audit: determine whether the frozen HMT+carrier action and matter interface are sufficiently specified for a one-loop counterterm or beta-function calculation without post-hoc choices of unresolved interface parameters.
