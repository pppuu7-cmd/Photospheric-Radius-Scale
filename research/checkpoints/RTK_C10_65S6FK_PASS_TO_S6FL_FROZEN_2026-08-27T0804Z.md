# RTK C10.65s6fK PASS → s6fL frozen frontier

UTC checkpoint: 2026-08-27T08:04Z
Branch: `rtk-class-build`

## Closed in this research pass

- C10.65s6fG: inherited `F(t,N)` clock/Khronon direct scalar-shift source is exactly zero at all orders.
- C10.65s6fH: finite-q projectable shift reduction has `K_beta=O(q^4)`, `J1=O(q^2)`, `J2=O(q^2)`, so the reduced cross contribution can have a finite `q->0` limit. Exact q=0 may not be substituted before reduction.
- C10.65s6fI: after including both beta-linear and beta^2*zeta ADM kinetic terms, the punctured soft limit is direction dependent. Its shift-dependent coefficient contains
  `9(1-lambda_HL) omega + 4 mu^2(k v_g-3 omega)`.
  For the n=2 completed dispersion, `3-n_g=2 M_U^4/(M_U^4+k^4)+k^2/(M_K^2+k^2)>0`, so the mu^2 term cannot vanish for finite positive scales.
- C10.65s6fJ: exact spatial q=0 is a separate homogeneous/global projectable sector, not a punctured finite-q shift constraint limit.
- C10.65s6fK: exact homogeneous quadratic/global-lapse block source-locked from the fixed C8 P(X_U) action:
  `A=(3/2)Mstar^2(1-3lambda_HL)`, `D=K_phys/2=Mstar^2 M_K^2`,
  `Delta_N=A H^2+D`,
  `L2_hom/a^3=A dot(zeta_0)^2-2AH n_0 dot(zeta_0)+Delta_N n_0^2`,
  `n_0=AH dot(zeta_0)/Delta_N`,
  `Q_hom=A D/Delta_N` when `Delta_N != 0`.
  This differs exactly from the punctured finite-q coefficient `D/H^2`.

## Active frontier

C10.65s6fL target is frozen before implementation:
`research/theory_targets/RTK_C10_65S6FL_HARD_HARD_HOMOGENEOUS_CUBIC_SOURCE_TARGET_v1.json`.

It must derive the hard-hard → homogeneous cubic source vector `(S_zeta0,S_n0)` from one fixed action, including gravitational kinetic/R3, fixed P(X_U), `C(X_U)(DTheta_U)^2`, and `alpha6(X_U) D_iR3D^iR3`. The finite-k hard shift must be reduced first, while the homogeneous leg must use the s6fK global block, never a punctured beta limit.

Outcome is preregistered as PROJECTED, FINITE, SINGULAR-SURFACE, or BLOCKED-INCOMPLETE. No parameter may be tuned to obtain cancellation.

## Guards

- Do not rerun s6fF ZERO/NONZERO until s6fL is complete and bare + alpha6 + exact homogeneous exchange are summed.
- Do not choose a punctured direction `mu` or angular average as the exact q=0 channel.
- `k=0.03 Mpc^-1` production remains blocked.
- No spectra/likelihood claim follows from this UV/cubic analysis.
- C9 technical naturalness and same-full-action primordial/background closure remain open.
