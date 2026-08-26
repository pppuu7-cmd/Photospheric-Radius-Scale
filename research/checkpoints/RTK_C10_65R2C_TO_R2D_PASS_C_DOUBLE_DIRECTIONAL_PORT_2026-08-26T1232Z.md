# RTK C10.65r2c -> r2d C-double directional port checkpoint — 2026-08-26T12:32Z

## Scope

This checkpoint records the validated numerical C-port frontier before the actual C10.65r2 in-CLASS first-RHS diagnostic parity gate. It does **not** change the frozen C10.65r2 target, thresholds, physical assumptions, or the no-feedback/no-`dy`-write contract. Pinned CLASS upstream remains `36cf283628c4a3330ec9fd3d84239bf775f77317`.

## Confirmed parent frontier

- C10.65r1: `PASS_SCOPED` — conditioned in-CLASS onset projector parity, diagnostic only.
- C10.65r2b: `INCONCLUSIVE_FAIL` — the historical fixed-C2 onset relation is not certified tangent along the first-RHS direction; therefore fixed-C2 may not be differentiated to obtain Bprime.
- C10.65r2c: `PASS_SCOPED` — the general off-manifold cancellation-reduced projector and its directional derivative are equivalent to the original q projector on all 36 records.

## C10.65r2d — frozen C double directional implementation preflight

A new target was frozen before execution: `research/theory_targets/RTK_C10_65R2D_C_DOUBLE_GENERAL_PROJECTOR_DIRECTIONAL_PORT_TARGET_v1.json`.

The C source `rtk/c10_65r2d_general_projector_dual.c` implements forward dual propagation in IEEE-754 double from primitive background/state values and the source-locked zero-slip first-RHS direction through the validated general off-manifold projector

`B = [E L (Q-D s) + 3 D H^2 Q + 3 D H a^2 delta_mu_pref - 2 D H P L psi_pref] / [r E L^2 - 2 D H^2 L + E L X0 + 3 D H^2 X0]`.

It contains no fixed-C2 dependence in executable directional code and introduces no boundary datum.

### First run and diagnosis

The first Action run (`32968847389`) returned the fail classification only because the static guard searched comments for the literal text `C2`; the numerical results themselves were already far inside the frozen bounds:

- max C-double vs high-precision stable B relative = `3.596963958165162e-16`;
- max C-double vs high-precision stable Bprime relative = `1.8232422754359036e-15`;
- max C-double vs persisted q Bprime relative = `1.8375675471050986e-15`;
- all outputs finite.

The guard was corrected to strip C comments and search executable text for an identifier-level fixed-C2 token. No threshold, equation, parent, or scientific criterion was changed.

### Corrected run

Corrected Action run `32968987214` completed successfully and persisted
`research/theory_results/RTK_C10_65R2D_C_DOUBLE_GENERAL_PROJECTOR_DIRECTIONAL_PORT_RESULT_v1.json` with classification
`C10_65R2D_C_DOUBLE_GENERAL_PROJECTOR_DIRECTIONAL_PORT_PASS_SCOPED`.

Frozen checks on all 36 records:

- max C-double vs high-precision stable B relative = `3.596963958165162e-16` <= `5e-11`;
- max C-double vs high-precision stable Bprime relative = `1.8232422754359036e-15` <= `5e-9`;
- max C-double vs persisted q Bprime relative = `1.8375675471050986e-15` <= `5e-9`;
- all outputs finite = true;
- fixed-C2 absent from executable C directional source = true;
- `threshold_changed=false`.

## Implementation consequence

The dangerous numerical part of the actual C10.65r2 port is now independently validated in C double. The next admissible step is to inject this exact forward-directional general projector into the existing dormant r1 diagnostic insertion point in pinned CLASS, then construct

`Psi_N_prime = psi_pref_prime - H_prime*B - H*B_prime`,

`metric_continuity_shadow = -3*Psi_N_prime`,

`metric_euler_shadow = k^2*Phi_N`,

followed by the source-locked TCA slip and first RHS for baryon/photon/UR/Khronon. The unchanged frozen C10.65r2 gate must then compare the C outputs against independent local and detached q/n/o parents over the exact 9x4 grid.

Production `dy`, metric sources, RHS, switching, state handoff and feedback remain forbidden until a later separately frozen gate.

## Still-open physical gates

- C9 radiative naturalness remains open.
- same-full-action primordial/background closure remains open.
- no claim of completed-U1 time integration, spectra/likelihood validation, or microscopic UV matching is made.
