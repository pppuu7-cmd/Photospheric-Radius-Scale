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

## C8 exact-algebra appendices

The main Formula Bible gives the project-level statement. Reconstructible detailed C8 derivations are additionally pinned in:

- `research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md` on `rtk-class-build` — full lapse+shift Schur setup, pole and normalized-residue gates;
- `rtk/route_b_flrw_schur_kernel.py` on `rtk-class-build` — exact Fraction arithmetic for D(q) and N(q);
- `rtk/route_b_flrw_schur_rank_residue.py` on `rtk-class-build` — strict-linear theorem: `rank(M1)=1`, exact pole location, and normalized residues `N(q*)/D1` and `-N(q*)/D1` for the effective-kernel Schur term.

### Current exact C8 theorem

For

`M(q)=M0+q M1`,

with symmetric two-constraint gradient block

`M1=[[a1,c1],[c1,b1]]`,

`det M(q)=D0+D1 q+D2 q^2`,

and

`D2=det(M1)=a1 b1-c1^2`.

If the desired denominator is strictly linear and nonconstant, then `D2=0` and `D1!=0`. The latter excludes `M1=0`; therefore the 2x2 matrix `M1` is nonzero and singular and hence

`rank(M1)=1`.

For the simple pole

`q*=-D0/D1`,

the residue of `N/D` is

`Res[N/D]=N(q*)/D1`,

while the pole residue contributed to

`K_eff=K0-N/D`

is

`Res[K_eff pole]=-N(q*)/D1`.

The unnormalised remainder `N(q*)` alone is not a valid cross-representation residue comparison if denominator normalization differs.

Scope: exact algebraic necessary condition for the reduced two-constraint linear-in-q kernel only. It is **not** by itself a DHOST degeneracy condition, a DOF proof, stability proof, or UV-completion theorem.

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
