# RTK C10.65n–C10.65q detached completed-U1 onset checkpoint

UTC checkpoint: 2026-08-26T01:46Z
Branch: `rtk-class-build`
Status: conditional/scoped. Historical control matching data remain external phenomenological pre-EFT data, not a UV derivation.

## C10.65n — conditional completed-U1 onset seed

Classification: `C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED`.

Input matching control from C10.65m:
- `J_ad0=-3`
- `A2=-1120.906563855608`
- `S_ur0=298.90841588141416`
- `C2=-1.314425482950032`
- all three relative entropy-gradient coordinates zero
- all three relative-velocity coordinates zero.

The seed is reconstructed without historical CLASS metric potentials. For each exact low-k anchor:
`D_b=J_ad0+A2*k^2`, `D_g=D_ur=(4/3)D_b`, `J_khr=D_b`.

Dressed ordinary A constraint:
`K=-(3/2)a^2/(k^2+a^2 M_c^2)`, `D_A=1-3KW0`, `D_A psi_pref=K h_hat`.

The invariant matching scalar fixes preferred momentum:
`Q_pref=[C2*k^2-3a^2 delta_mu_pref]/(3H)`.

The differentiated A equation makes `psi_pref_prime` affine in B; Hamiltonian makes `phi_pref` affine in B; momentum closes one scalar linear equation for B. All nine diagnostic `(lambda_HL,M_c)` points pass high-precision residual and low-k convergence tests.

Important example, first grid point leading k->0 control:
- `psi_pref0 = 1.569114230485656e-4`
- `psi_pref_prime0 = -7.969865716214555e-6`
- `phi_pref0 = 1.7812131739531292`
- `B0 = -188.0955106558435`
- `Psi_N0 = 2.438425915428145`
- `Q_pref0 = 0.04627924300526934`
- `V_pref0 = 77.13094659066762`
- `V_N0 = -110.96456406517586`.

The large difference from historical CLASS metric values is not treated as a failure: the historical metric is not imported into the completed-U1 solution.

## C10.65o — radiation shear / physical lapse closure

Classification: `C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED`.

Uses the pinned `compromise_CLASS` photon shear and the matched massless-UR shear. In flat Newtonian gauge:
`sigma_g,1=(16/45)tau_c theta_g` and the source-locked second-order compromise correction is retained.

The anisotropic-stress map is
`Pi=1.5*(W_gamma sigma_g+W_ur sigma_ur)/k^2`.
For the frozen diagnostic `Pcal=1, alpha1=0`, physical lapse satisfies
`Phi_N=Psi_N-3a^2 Pi`.
Because photon shear is affine in `Phi_N`, this is an algebraic one-dimensional closure:
`Phi_N=(Psi_N-3a^2 Pi_A)/(1+3a^2 Pi_Phi)`.
All 36 low-k/grid records pass; no B_prime or slip is assumed in this gate.

## C10.65p — triangular derivative/slip theorem

Classification: `C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_PASS_SCOPED`.

Pinned TCA baryon slip coefficient: `R/(1+R)`.
Pinned photon slip coefficient: `-1/(1+R)`.
With `W_gamma=R W_b`, their weighted contribution to photon+baryon aggregate momentum derivative cancels exactly.

Therefore Thomson slip does not source the aggregate `q0_N_prime` consumed by the differentiated completed-U1 projector. The roundtrip theorem also establishes that `B_prime` is the derivative of algebraic `B[z(t)]`, not a new chi/B initial datum.

At the zero-relative-velocity matching point, pinned compromise_CLASS slip is affine in physical curvature derivative:
`d slip/d Psi_N_prime = -(1-2HF) F k^2 (1-3 cb2)`.
At onset `1-2HF=0.9996101429394949`; the derivative coefficient is finite on all four anchors.

Correct execution order:
1. evaluate aggregate ordinary+neutral local RHS/background derivatives;
2. differentiate algebraic completed-U1 projector to get B_prime;
3. compute `Psi_N_prime=psi_pref_prime-H_prime B-H B_prime`;
4. evaluate pinned compromise_CLASS slip;
5. recover individual photon/baryon Euler derivatives. Slip cancels again in the aggregate channel.

## C10.65q — numeric B_prime / Psi_N_prime / full slip closure

Classification: `C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED`.

Final successful Actions run: `32921537406`.
A first run `32921303943` failed only the deliberately extreme `1e-30` B_prime/slip-invariance threshold: `~4.02e-24`. The cause was mixing two rounded numerical representations of the same exact identity `R=W_gamma/W_b`: the TCA-pack R and independently rounded `rho_b,rho_gamma` from the detached seed. The frozen threshold was not relaxed. v2 reconstructs `R=W_gamma/W_b` from the same numerical state used by the aggregate projector and keeps the pack R as an independent consistency check.

Final diagnostics:
- `Hc = 0.0129629303512`
- `Hc_prime = -0.0001319668127152`
- `R_pack = 6.6951521502165`
- `R_projector_state = 6.695152150216499`
- relative representation mismatch `1.0687887370642212e-16`
- max projector reproduction relative error `3.6906169099292e-16`
- max 70-vs-100-dps B_prime relative error `5.940328119194908e-72`
- max B_prime change after inserting actual pinned slip `9.564268782638503e-102`
- max weighted photon-baryon slip cancellation residual `0.0`.

Example first grid point low-k intercepts:
- `B_prime -> 3.0202978979176693`
- `Psi_N_prime -> -0.06398224618357957`
- `slip/k^2 -> -3.802808169320444e-7`.
Nested smallest-three/all-four intercept disagreements are far below the frozen `1e-3` threshold.

Thus the entire detached onset metric/TCA chain is now closed conditionally without adding an independent B, B_prime, chi, Psi_N_prime or slip initial datum.

## Architecture status after q

The next step is no longer another detached algebraic theorem. Freeze an opt-in in-CLASS bridge gate that:
- is disabled by default and leaves the historical production path unchanged when off;
- starts only on the four exact low-k anchors;
- initializes from the declared C10.65m matching control;
- reconstructs preferred A -> Hamiltonian -> momentum metrics and physical Psi_N/Phi_N inside the CLASS perturbation RHS;
- uses the source-locked TCA shear/slip formulas;
- exports first-RHS/short-step diagnostics and compares them with detached C10.65n/o/q before expanding to the full k grid;
- does not use historical CLASS phi/psi as the completed metric solution.

Still open outside this conditional bridge: microscopic UV matching derivation, same-full-action primordial/background normalization, C9 radiative protection, massive-neutrino completion, full spectra/likelihood.
