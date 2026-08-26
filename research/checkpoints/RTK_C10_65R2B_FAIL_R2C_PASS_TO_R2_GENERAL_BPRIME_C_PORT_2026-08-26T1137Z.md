# RTK C10.65r2b/r2c frontier checkpoint — 2026-08-26T11:37Z

## Scope

This checkpoint records the implementation frontier after C10.65r2a and before the actual C10.65r2 in-CLASS first-RHS diagnostic parity gate. It does **not** change the frozen C10.65r2 target, thresholds, physical assumptions, or the no-feedback/no-`dy`-write contract.

Pinned CLASS upstream SHA remains `36cf283628c4a3330ec9fd3d84239bf775f77317`.

## Confirmed parents

- C10.65r1: `PASS_SCOPED` — conditioned in-CLASS algebraic projector parity, diagnostic only.
- C10.65r2 source-lock preflight: `PASS_SCOPED`; full r2 remained `OPEN_NOT_EXECUTED`.
- C10.65r2a: `PASS_SCOPED` — audited bridge `Psi_N' = psi_pref' - H' B - H B'`, `metric_continuity_shadow=-3 Psi_N'`, pinned `metric_euler_shadow=k^2 Phi_N`.

## C10.65r2b — frozen tangent audit: INCONCLUSIVE_FAIL

The onset matching condition used by the conditioned r1 value projector was tested as

`C = 3 H Q_pref + 3 a^2 delta_mu_pref - C2 k^2`, with `C2=-1.314425482950032`.

The condition itself is reproduced at onset extremely accurately:

- max onset constraint relative residual = `8.717179345786061e-21` (frozen bound `5e-11`).

However, along the exact C10.65q zero-slip aggregate first-RHS direction its derivative is not certified tangent:

- min normalized `|C'|` = `2.6503963655747855e-07`;
- max normalized `|C'|` = `2.406923043462018e-04`;
- frozen tangent requirement was max `<=5e-9`;
- preregistered strong resolved-non-tangent requirement was min `>=1e-6`.

Therefore the only admissible frozen classification is `C10_65R2B_INCONCLUSIVE_FAIL`. The data show an approximately `k^2` scaling of the normalized derivative, so differentiating the fixed-C2 onset specialization as though it were a dynamical constraint is not certified. No threshold was weakened and the negative result is persisted with provenance.

## C10.65r2c — general off-manifold projector directional equivalence: PASS_SCOPED

To avoid assuming tangent propagation of the onset matching relation, the same **general mixed-interface projector used by C10.65q** was algebraically reduced without imposing fixed C2. With

- `r=lambda_HL-1`,
- `D=3 lambda_HL-1`,
- `L=-k^2`,
- `E=2`, `P=1`,
- `X0=3 a^2 W0`,
- `Q=Qbase`,
- `s=psi_pref_prime`,

and identity `D(D-2)=3 r D`, the cancellation-reduced general expression is

`B = [E L (Q-D s) + 3 D H^2 Q + 3 D H a^2 delta_mu_pref - 2 D H P L psi_pref] / [r E L^2 - 2 D H^2 L + E L X0 + 3 D H^2 X0]`.

This expression is valid off the fixed-C2 onset manifold. On the complete 9x4 = 36 record grid, the frozen C10.65r2c audit returned `C10_65R2C_GENERAL_PROJECTOR_DIRECTIONAL_EQUIVALENCE_PASS_SCOPED` with:

- max stable-general B vs original q B relative = `3.973216746925637e-99` (bound `1e-40`);
- max stable-general Bprime vs original q directional Bprime relative = `0.0` (bound `1e-35`);
- max 70 vs 100 dps stable Bprime relative = `5.940328119194908e-72` (bound `1e-30`);
- max stable Bprime vs persisted q Bprime record relative = `1.0539163191290829e-16` (bound `5e-15`).

No r2 threshold or parent result was changed.

## Implementation consequence

For the actual C10.65r2 C port:

1. Keep the already-certified conditioned r1 fixed-C2 expression for the **algebraic onset value/regression path**.
2. Compute `B'` by differentiating the validated **general off-manifold cancellation-reduced mixed-interface projector** above along the source-locked C10.65q local direction. Do not differentiate the fixed-C2 onset specialization.
3. Construct `Psi_N' = psi_pref' - H' B - H B'`.
4. Construct read-only shadow sources `metric_continuity=-3 Psi_N'` and `metric_euler=k^2 Phi_N` in the pinned CLASS convention.
5. Evaluate the source-locked TCA slip and first RHS for baryon/photon/UR/Khronon.
6. Run the unchanged frozen C10.65r2 36-record parity checks.
7. Continue to forbid writes into `dy`, production metric sources, production species RHS, approximation switches, or integration state.

A C10.65r2 PASS, if obtained, is only an in-CLASS first-RHS software/algebra parity result. It does not authorize state handoff or production feedback; those require a separately frozen later gate.

## Still open physical gates

- C9 radiative naturalness remains open.
- same-full-action primordial/background closure remains open.
- no claim of full completed-U1 cosmological integration, spectra/likelihood validation, or microscopic UV matching is made here.
