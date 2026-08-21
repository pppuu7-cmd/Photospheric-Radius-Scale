# RTK Formula Bible Index

Updated: 2026-08-21

## Canonical formula sections

1. Fundamental action / candidate carrier
2. Background equations
3. Khronon/DBI reduction
4. Perturbation equations
5. Stability / DOF / hyperbolicity conditions
6. Weak-field limit
7. Transition-radius derivation and environmental scaling
8. Cosmological observables and frozen objective
9. Numerical implementation mapping and cache semantics
10. Route-B / U-DHOST scoped PPN algebra
11. FLRW constraint-kernel / Schur-complement matching
12. Primordial-abundance differential robustness
13. Provenance and derivation discipline

## Detailed derivation appendices

The main Formula Bible stores project-level formulas/status. Long derivations live in named appendices and must be linked here so the project remains reconstructible without chat history.

### C8 FLRW Schur appendix

Canonical detailed derivation:

- `research/methods/RTK_FORMULA_BIBLE_C8_SCHUR_APPENDIX.md` on `main`.

Supporting source/protocol:

- `research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md` on `rtk-class-build`;
- `rtk/route_b_flrw_schur_kernel.py` on `rtk-class-build`;
- `rtk/route_b_flrw_schur_rank_residue.py` on `rtk-class-build`;
- `rtk/route_b_pole_residue_distinction.py` on `rtk-class-build`.

### B4 numerical proof chain

Canonical audit/provenance chain:

- `research/robustness/RTK_B4_NEUTRINO_STATIONARITY_CHAIN_2026-08-21.md` on `main`.

It reconstructs the first recentered B4 Hessian, its three negative modes, exact negative-mode rays, the winning recenter point, target-v2 provenance and the mandatory base/half/fresh-tree closure sequence.

## Current exact C8 reduced-kernel theorem

For

`M(q)=M0+q M1`,

with symmetric two-constraint gradient block

`M1=[[a1,c1],[c1,b1]]`,

`det M(q)=D0+D1 q+D2 q^2`,

and

`D2=det(M1)=a1 b1-c1^2`.

If the desired reduced-kernel denominator is strictly linear and nonconstant, then `D2=0` and `D1!=0`. Hence `M1` is nonzero and singular, so

`rank(M1)=1`.

For the simple **q-plane coefficient pole**

`q*=-D0/D1`,

the normalized q-plane residues are

`Res_q[N/D]=N(q*)/D1`,

and for

`K_eff=K0-N/D`,

`Res_q[Schur in K_eff]=-N(q*)/D1`.

The unnormalised remainder `N(q*)` alone is not a valid cross-representation residue comparison when denominator normalization differs.

### Conditional rank-one sign theorem

For real symmetric rank-one

`M1=sigma v v^T`, `sigma=+1 or -1`,

with invertible `M0`, define

`a=v^T M0^{-1}v`,

`b(q)=v^T M0^{-1}J(q)`.

Matrix determinant lemma gives

`q*=-1/(sigma a)`.

Sherman-Morrison gives the q-plane Schur residue

`Res_q[Schur in K_eff] = - b(q*)^2/(sigma a^2)`.

Therefore, when `b(q*) != 0`, its sign is opposite to the unique nonzero eigenvalue of `M1`. If `b(q*)=0`, the determinant pole cancels from that mixing/source channel.

### Critical residue distinction

The C8 residue above is a residue with respect to the **spatial variable q** in a reduced coefficient. It is **not** automatically the physical propagator residue with respect to `omega^2`.

The existing `route_b_pole_residue_distinction.py` theorem separately shows that two kernels can share the same on-shell scalar dispersion/pole while differing in fixed-source propagator normalization and `omega^2` residue. A complete carrier must therefore pass both the q-plane off-shell coefficient mapping and the dynamical/source-coupled propagator mapping.

Scope: these are exact algebraic statements for the stated reduced two-constraint kernel. They are not by themselves DHOST degeneracy conditions, DOF/stability proofs, ghost criteria, or UV-completion theorems.

## Recovery principle

Every formula admitted to the research record must contain or link to:

- starting action/equations;
- definitions and conventions;
- algebraic derivation steps;
- assumptions and limits;
- dimensional checks where applicable;
- symbolic/numerical verification;
- implementation location;
- commit/workflow/run provenance;
- explicit scope and non-claims;
- validation status.

Status markers:

- GREEN = derived/validated within stated assumptions
- YELLOW = partial/pending independent audit
- RED = open
- BLACK = scoped ruled-out construction
