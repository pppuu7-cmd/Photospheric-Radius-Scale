# RTK Formula Bible — current pointer

Updated: 2026-08-22 22:46 UTC
Status: current recovery pointer; use this before the older index when reconstructing C8/U(1)

## Canonical reading order for the active U(1) completion

1. `research/methods/RTK_FORMULA_BIBLE.md` — base notation and production identities.
2. `research/methods/RTK_FORMULA_BIBLE_C8_U1_COMPLETION_APPENDIX.md` — historical local-U(1) construction ladder and published family context.
3. `research/methods/RTK_FORMULA_BIBLE_C8_U1_COMPLETION_ADDENDUM_2026-08-22T2220Z.md` — **mandatory correction**: actual primary mixing, genuine `(p_Q,C_Lambda)` pair, exact Dirac projection, reduced constraint chain, zero-mode caveat and punctured-low-k strategy.
4. `research/methods/RTK_FORMULA_BIBLE_C8_U1_LOWK_RANK_ADDENDUM_2026-08-22T2245Z.md` — **current low-k frontier**: neutral-RTK determinant immunity, filtered-matter one-coefficient reduction, exact leading determinant, matter-density rank scale and finite-epsilon remainder bridge.
5. `research/checkpoints/RTK_MODEL_DEVELOPMENT_ADDENDUM_2026-08-22T2245Z.md` — current run/artifact/digest provenance and heavy-B9 status.

## Supersession rules

- Do **not** use the old assumed `old-four + auxiliary-four` 8x8 constraint basis as the physical coupled DOF proof. Its Schur determinant identity remains a conditional algebraic lemma only.
- Eliminate the genuine auxiliary pair `(p_Q,C_Lambda)` first, then use the reduced physical chain `(pi_N,Jhat,Hperp_hat,phi_hat)`.
- Do **not** use exact flat-FLRW `k=0` as a local propagating-rank certificate. It is a background/source-cancellation mode. The physical local target is a punctured interval `0<|k|<epsilon`.
- Keep `M_c>0` symbolic until classical rank and scale-window existence gates close. Numerical fitting is not a substitute for these gates.
- On the currently certified flat-FLRW/homogeneous-lapse/analytic-kernel scope, the leading filtered-matter matrix is `K=[[0,-x],[x,0]]`, with `x=V(H0-tau_H)`. Do not export this to curved/anisotropic/inhomogeneous-lapse backgrounds without new gates.
- The frozen elliptic candidate filters the **ordinary universally coupled matter** `H0`; the neutral RTK scalar is a separate sector and must not be double-counted into the filtered-matter density bound.
- C9 remains open: `eta1=eta2=0` is not technically natural merely because the classical low-k rank is controlled.

## Current leading formulas

`a_eff=q/(M_c^2+q)`, `q=|k|^2`.

`B_RTK/q=[[A,-b],[b,0]]`, `A=a2+r2`, `b=2 eta0 P(d-1)/(d lambda-1)`.

Filtered matter on the controlled flat branch:

`Delta B_m/q=(1/M_c^2)[[0,-x],[x,0]]`,

`x=V(H0-tau_H)`.

Exact leading determinant:

`det L=(b+x/M_c^2)^2`.

Published Hamiltonian normalization gives

`x/b=-2(H0-tau_H)/[eta0(d-1)M_Pl^2 sqrt(g)]`.

For isotropic perfect-fluid ordinary matter,

`tau_H/sqrt(g)=-(d/2)p`,

so a conservative leading no-cancellation condition is

`M_c^2 > 2|sum_s(rho_s+d p_s/2)|/[|eta0|(d-1)M_Pl^2]`.

To turn the leading theorem into an explicit finite interval, derive `C` such that

`B(q)=q L+q^2R(q)`, `||R(q)||_2<=C`.

Then

`0<|k|<sqrt(min(q0,sigma_min(L)/C))`

is sufficient.

## Immediate order

1. finish ordinary-matter source/species dictionary;
2. derive subleading remainder bound `C`;
3. intersect the rank lower edge with the frozen 1% `M_c` window without choosing `M_c`;
4. analyze intermediate/high-k roots with the full elliptic symbol;
5. only then perform same-action PPN/GW/cutoff/compact-object/C9 gates.

For B9 statistical work, follow the separately frozen B9 decision tree; do not mix B9 parameter recentering with C8 `M_c` selection.
