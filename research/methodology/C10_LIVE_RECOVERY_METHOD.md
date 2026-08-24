# C10 live recovery method — completed U(1) cosmology bridge

Last manual theory advance: **2026-08-24T23:40Z**.  
Canonical branch: `rtk-class-build`.  
This file is a recovery/checkpoint document. It is not a replacement for frozen target/result JSON artifacts.

## 1. Purpose

C10 asks whether the phenomenological RTK cosmology can be embedded into the same fixed local U(1)-completed Hořava action strongly enough to build an **independent completed-gravity shadow solver**, without silently treating the historical phenomenological CLASS fit as though it were already a fit of the completed action.

The production path is therefore immutable during C10. Every completed-action implementation must be opt-in and must first reproduce zero/near-deformation controls.

## 2. Read these files first after chat loss

1. `research/state/C10_current.json`
2. `research/theory_results/RTK_C10_U1_A_SOURCE_NORMALIZATION_RESULT_v1.json`
3. `research/theory_results/RTK_C10_U1_PREPOTENTIAL_WARD_NORMALIZATION_RESULT_v1.json`
4. `research/theory_results/RTK_C10_U1_LINEAR_WARD_CONSTRAINT_REDUCTION_RESULT_v1.json`
5. `research/theory_results/RTK_C10_U1_MINIMAL_LINEAR_METRIC_REDUCTION_RESULT_v1.json`
6. `research/theory_results/RTK_C10_U1_TRACE_MOMENTUM_CONSERVATION_CLOSURE_RESULT_v1.json`
7. `research/theory_results/RTK_C10_U1_TOTAL_MOMENTUM_SOURCE_SCOPE_RESULT_v1.json`
8. `research/theory_results/RTK_C10_U1_PHYSICAL_METRIC_CLASS_GAUGE_BRIDGE_RESULT_v1.json`
9. `research/theory_results/RTK_C10_U1_NEWTONIAN_STUECKELBERG_METRIC_BRIDGE_RESULT_v1.json`
10. `research/theory_results/RTK_C10_U1_NEWTONIAN_SOURCE_TRANSFORM_POLE_AUDIT_RESULT_v1.json`

Primary literature anchors used for conventions: Zhu–Shu–Wu–Wang, Phys. Rev. D 85, 044053 (2012), arXiv:1110.5106; and standard first-order scalar gauge transformations as reviewed by Malik & Wands, Phys. Rept. 475 (2009), arXiv:0809.4944.

## 3. Frozen action/source architecture

On the production-matching U(1) branch:

- `a1=1`, `a2=0`, `Ahat=0` is the admissible matching branch used by the C10 metric map.
- The elliptic compensator filters the **ordinary** universal source `H0` only.
- Baseline ordinary `H0` means baryons + photons + massless relativistic species.
- The fitted RTK/Khronon component is **not** ordinary CDM in this source split.
- RTK/Khronon is U(1)-neutral in the A-current: `J_A^RTK=0`.
- Neutrality in `J_A` does **not** mean neutral momentum can be omitted from metric or Ward equations.

The exact filtered transfer for a Fourier mode is

\[
a_{1,\mathrm{eff}}(k,a)=\frac{k^2}{k^2+a^2 M_c^2}.
\]

With `P=H0-Q`, the literature-normalized A-current is

\[
J_A=2P,
\qquad
\delta P=a_{1,\mathrm{eff}}\,\delta H_0.
\]

The A constraint for every nonzero mode is

\[
L\psi=4\pi G a^2\delta P,
\qquad L\equiv\partial^2=-k^2,
\]

or equivalently

\[
(k^2+a^2M_c^2)\psi=-4\pi G a^2\delta H_0.
\]

Exact `k=0` is not obtained by cancelling `L`; it is handled by the separately certified homogeneous bridge.

## 4. Ward/prepotential normalization

The U(1) Ward identity fixes the prepotential source once `J_A` and the **total** momentum current are known:

\[
J_\varphi=
\frac{D_t J_A-\nabla_i(J_A N^i)}{2N}
-\frac{\nabla_i(NJ^i_{\rm total})}{N}.
\]

For flat FLRW scalar perturbations, with

\[
\delta J^i_{\rm total}=a^{-2}\partial^i q_{\rm total},
\]

this becomes

\[
\delta J_\varphi
=a^{-1}\left[(\delta P)'+3\mathcal H\delta P-a^{-1}Lq_{\rm total}\right].
\]

The momentum constraint is

\[
8\pi G a q_{\rm total}
=(3\lambda-1)(\psi'+\mathcal H\phi)
+(\lambda-1)LB.
\]

Adding an arbitrary U(1)-neutral momentum `q_neutral` changes the Ward and momentum sides by the same amount; the previously derived prepotential-redundancy residual remains exactly zero. Therefore `q` in the C10 linear Ward theorem is always **total metric momentum**.

## 5. Minimal preferred-coordinate metric system

Define

\[
D=3\lambda-1,
\qquad r=\lambda-1,
\qquad M_q=8\pi G a q_{\rm total}.
\]

After the A constraint fixes `psi`, the preferred-coordinate scalar constraints are

\[
LB=\frac{M_q-D(\psi'+\mathcal H\phi)}{r},
\]

and

\[
\left[rE_{\rm th}L-2D\mathcal H^2\right]\phi
=-8\pi G a^2r\,\delta\mu_{\rm total}
-D\mathcal H M_q
+2D\mathcal H\psi'
+2r\mathcal P L\psi.
\]

On the scoped branch `lambda>1`, `E_th>0`, and `k>0`, the preferred lapse denominator is

\[
-\left[rE_{\rm th}k^2+2D\mathcal H^2\right]<0,
\]

so there is no preferred-coordinate lapse pole.

The remaining trace compatibility equation is exactly total momentum conservation once the background equations are used; it is not a new propagating gravitational scalar equation in this scoped linear system.

## 6. Physical metric and Newtonian/Stueckelberg bridge

In quasilongitudinal preferred coordinates (`E=0`, `delta varphi=0`) the matter metric has

\[
\Phi_{\rm matter}=\phi-\delta A/a,
\qquad
\Psi_{\rm matter}=\psi,
\qquad
\sigma_{\rm phys}=B.
\]

A standard Newtonian-coordinate representation is constructed with the coordinate change `T=-B`, while a separate Stückelberg field retains the preferred-foliation information:

\[
\chi_N=B.
\]

This `chi` is neither the RTK/DBI scalar `Sigma` nor the U(1) prepotential `varphi`.

The physical Newtonian potentials are

\[
\Psi_N=\psi-\mathcal H B,
\]

\[
\Phi_N=(1-\mathcal P)\phi+\psi+\alpha_1L\psi
-\mathcal H B-8\pi G a^2\Pi_{\rm total}.
\]

The `B'` dependence cancels exactly after the certified traceless constraint is substituted.

## 7. Newtonian source transformation

For each covariant species, and therefore for the total stress tensor, the pure time change `T=-B` gives

\[
\delta\mu_N=\delta\mu_{\rm pref}+\rho'\chi,
\]

\[
\delta p_N=\delta p_{\rm pref}+p'\chi,
\]

\[
q_N=q_{\rm pref}+a(\rho+p)\chi,
\]

\[
\Pi_N=\Pi_{\rm pref}.
\]

The momentum rule follows from the already certified convention

\[
q=-a(\rho+p)(v+B).
\]

Hence the inverse map used inside a completed-gravity Newtonian shadow interface is

\[
\delta\mu_{\rm pref}=\delta\mu_N-\rho'\chi,
\quad
\delta p_{\rm pref}=\delta p_N-p'\chi,
\]

\[
q_{\rm pref}=q_N-a(\rho+p)\chi,
\quad
\Pi_{\rm pref}=\Pi_N.
\]

For the **ordinary-only A source**, do not gauge-transform `deltaP` as if it were a covariant density. Reconstruct the preferred-slice ordinary density first:

\[
\delta H_{0,\rm pref}=\delta H_{0,N}-H_0'\chi,
\]

then apply the elliptic filter:

\[
\delta P_{\rm pref}
=a_{1,\rm eff}\left(\delta H_{0,N}-H_0'\chi\right).
\]

This distinction is mandatory.

## 8. Coupled transformed solve and pole audit

Define

\[
C=4\pi G a^2,
\qquad
K=\frac{C a_{1,\rm eff}}{L}
=-\frac{4\pi G a^2}{k^2+a^2M_c^2},
\]

\[
W=\rho_{\rm total}+p_{\rm total},
\quad
Q_N=8\pi G a q_{{\rm total},N},
\]

\[
\Delta_\phi=rE_{\rm th}L-2D\mathcal H^2.
\]

The A constraint becomes

\[
\psi=K\left(\delta H_{0,N}-H_0'\chi\right).
\]

Write its derivative as

\[
\psi'=S_\psi-KH_0'\chi',
\]

where `S_psi` contains no `phi` or `chi'`.

After substituting the inverse source map into momentum and Hamiltonian constraints, the unknown pair `(phi,chi')` obeys a 2x2 system with coefficient matrix

\[
M=
\begin{pmatrix}
D\mathcal H & -DKH_0'\\
\Delta_\phi & 2D\mathcal H K H_0'
\end{pmatrix}.
\]

Its exact determinant is

\[
\det M
=D K H_0'\left(2D\mathcal H^2+\Delta_\phi\right)
=CDrE_{\rm th}H_0'a_{1,\rm eff}.
\]

Using ordinary-background conservation,

\[
H_0'=-3\mathcal H W_{0,\rm ordinary},
\]

so

\[
\boxed{
\det M
=-12\pi G a^2D r E_{\rm th}\mathcal H
W_{0,\rm ordinary}
\frac{k^2}{k^2+a^2M_c^2}
}.
\]

Therefore, on the certified expanding branch

- `lambda>1` => `D>0`, `r>0`;
- `E_th>0`;
- `H>0`;
- `W0_ordinary>0` at every finite cosmological time represented by the ordinary baryon/radiation sector;
- `M_c^2>0`;
- `k>0`;

we have `det M < 0`, so **no new finite-k pole exists**.

The cancellation of the apparent `Delta_phi` factor is important: the Newtonian/Stueckelberg representation does not inherit a new lapse singularity from a bad solve ordering.

## 9. k -> 0 conditioning guard

Although there is no finite-`k` pole,

\[
\det M\propto a_{1,\rm eff}\sim k^2
\qquad (k\to0).
\]

This is expected because the exact homogeneous mode belongs to the separate `k=0` bridge. A future numerical solver must not infer a physical instability from a large condition number at very small `k`. It should monitor conditioning and, if useful, evolve a rescaled shear/Stueckelberg variable rather than raw `chi`.

## 10. Current next gate

The next gate is **not** a likelihood or a production CLASS change.

Freeze and implement a standalone completed-gravity shadow metric API with these requirements:

1. Inputs: background, Newtonian ordinary density source, Newtonian total `delta_mu/q/delta_p/Pi`, frozen action parameters.
2. Internal state: `chi` (or a numerically safer equivalent) plus preferred-coordinate constraint variables.
3. Reconstruction: convert Newtonian sources to preferred sources exactly as above.
4. Solve: A constraint + coupled `(phi,chi')` system + certified traceless metric map.
5. Outputs: `Phi_N`, `Psi_N`, `chi`, determinant/conditioning diagnostics, constraint residuals.
6. Controls before any Boltzmann use: exact source-map round trip, `k=0` routing, finite-`k` determinant sign, zero/near-deformation limits, and fixed prescribed source histories.
7. Production CLASS remains untouched.

Only after those metric-source controls pass may an opt-in completed-U1 Boltzmann shadow be attempted. Only after fixed-parameter spectra pass may a completed-action likelihood/refit be discussed.

## 11. Do not conflate with parallel numerical gates

A5 recenter/cross-basin certification, B4 half-eigenmode rays, and B5 linear scale-dependence are separate numerical frontiers. Their pending status is not a C10 failure and C10 theory progress does not close them.

## 12. Non-claims still open

C10 does not yet provide:

- a completed-U1 metric-solver likelihood score;
- a completed-action refit;
- full nonlinear perturbation closure;
- the B4 massive-neutrino completion-source extension;
- C9 radiative protection/naturalness;
- compact-object/strong-field closure.
