# RTK C8 — FLRW Schur-Complement Matching Protocol

Date: 2026-08-21
Status: diagnostic protocol; not a covariant completion

## Question

Can a single fixed set of carrier coefficients reproduce the RTK scalar rational kernel on FLRW after the nondynamical lapse/shift constraints are eliminated, including the full rational structure rather than only an on-shell dispersion relation?

This protocol exists because the fixed-Minkowski obstruction cannot simply be promoted to FLRW: background quantities such as H can enter the constraint matrix and move a coefficient pole with epoch even when Wilson coefficients are fixed.

## Algebraic setup

Let q denote the spatial Fourier variable used in the reduced scalar kernel and x=(delta N, chi) the nondynamical scalar constraints. Write

L = 1/2 x^T M(q,H) x + x^T J(q,H) zeta + 1/2 K0(q,H) zeta^2,

with

M = [[A,C],[C,B]],   J=(P,R).

Exact elimination gives

K_eff(q,H) = K0(q,H) - N(q,H)/D(q,H),

where

D = det M = A B - C^2,

N = B P^2 - 2 C P R + A R^2.

The zeros of D control poles of the reduced rational coefficient in the complex q-plane unless the numerator cancels them. Matching D alone is insufficient; the complete rational remainder and its normalization must also match the intended RTK off-shell kernel.

## Critical terminology: q-plane coefficient pole versus physical propagator pole

The residue defined below is the residue of the reduced **spatial-q rational coefficient** after lapse/shift elimination. It is not automatically the physical propagator residue with respect to `omega^2`.

The earlier exact theorem in `rtk/route_b_pole_residue_distinction.py` established a separate point: two kernels can have the same physical scalar dispersion/pole in `omega^2` while differing in propagator normalization/residue for a fixed source coupling. Therefore C8 must keep two levels distinct:

1. **constraint-rational q-plane matching** — the subject of this protocol;
2. **dynamical propagator/source-response matching in omega^2** — a later action-level gate.

Passing the first never implies the second.

## Linear-in-q diagnostic

For

A=a0+a1 q, B=b0+b1 q, C=c0+c1 q,

write

M(q)=M0+q M1,

with

M1=[[a1,c1],[c1,b1]].

Then

D(q)=D0+D1 q+D2 q^2,

D0=a0 b0-c0^2,

D1=a0 b1+a1 b0-2 c0 c1,

D2=a1 b1-c1^2=det(M1).

A strict nonconstant linear denominator requires not merely D2=0 but also D1!=0. Therefore:

1. det(M1)=0;
2. M1 cannot be the zero matrix, because M1=0 would force D1=0;
3. for a 2x2 matrix, M1 must consequently have rank exactly one.

Thus the exact necessary structural gate is

rank(M1)=1.

This says that the q-gradient part of the two-constraint matrix contains only one independent constraint-gradient combination at this truncation order.

This rank-one statement is only an algebraic property of the reduced constraint matrix. It must not be called DHOST degeneracy unless an explicit covariant action has been mapped to these coefficients and its full degeneracy/constraint algebra has been derived.

## Correct q-plane residue normalization

For P=p0+p1 q and R=r0+r1 q, N is generically cubic. Let

D(q)=D0+D1 q,

with simple q-plane pole

q_p=-D0/D1.

Polynomial division gives a polynomial part plus a simple rational term. The unnormalised remainder is

N(q_p),

but the q-plane residue of N/D is

Res_q[N/D] = N(q_p)/D'(q_p) = N(q_p)/D1.

Since the Schur term enters the effective kernel with a minus sign,

K_eff = K0 - N/D,

the q-plane residue contributed by the Schur subtraction is

Res_q[Schur in K_eff] = -N(q_p)/D1.

This normalized q-plane residue, not N(q_p) by itself, is the object that is invariant under a common nonzero rescaling of numerator and denominator.

Again: this is not yet the propagator residue in `omega^2`.

## Conditional rank-one factorization and sign theorem

For a real symmetric rank-one M1, write

M1 = sigma v v^T,

where sigma=+1 or -1 is the sign of its unique nonzero eigenvalue. Assume additionally that M0 is invertible. Define

a = v^T M0^{-1} v.

The matrix determinant lemma gives

det(M0 + q sigma v v^T)
= det(M0) [1 + q sigma a].

Therefore, for a simple pole,

q_p = -1/(sigma a).

Now let

b(q)=v^T M0^{-1} J(q).

Sherman-Morrison gives

M^{-1}
= M0^{-1}
- [q sigma M0^{-1} v v^T M0^{-1}]/[1+q sigma a].

Substituting into

K_eff = K0 - J^T M^{-1} J

shows that the singular q-dependent piece is

q sigma b(q)^2/[1+q sigma a].

If K0 and J are regular at q_p, its q-plane residue is

Res_q[Schur in K_eff]
= - b(q_p)^2/[sigma a^2].

Consequences:

- if b(q_p) != 0, the q-plane Schur residue has sign opposite to the unique nonzero eigenvalue of M1;
- if b(q_p) = 0, the apparent determinant pole cancels from that mixing/source channel and cannot reproduce a nonzero target residue;
- this sign rule is conditional on real symmetric rank-one M1, invertible M0 and regular K0/J at the pole.

This is a stronger scoped algebraic filter, not a ghost criterion. A kinetic ghost is determined by the dynamical omega-dependent quadratic action after all constraints and field normalizations are handled, not by this q-plane sign alone.

## Required gates for an actual C8 candidate

1. **Action map** — derive A,B,C,P,R,K0 from one explicit fixed covariant/ADM action. No coefficient may be fitted independently at each epoch.
2. **Constraint-rank gate** — in the linear-in-q reduction, verify rank(M1)=1 whenever a strict nonconstant linear denominator is claimed; also verify no unintended singularity over the physical q-domain.
3. **q-pole gate** — match the RTK reduced-kernel q-plane pole structure over more than one FLRW epoch with one fixed underlying coefficient set.
4. **q-residue gate** — match `-N(q_p)/D1`, with normalization and sign convention stated, at the same epochs; matching D alone or N(q_p) alone is insufficient.
5. **Pole-coupling gate** — when using the rank-one representation, require the overlap `b(q_p)` appropriate to the target channel to be nonzero if the RTK target has a nonzero q-plane residue.
6. **Polynomial-part gate** — show that the polynomial quotient generated by N/D is correctly combined with K0 and does not introduce a mismatched local term.
7. **Physical propagator/source gate** — independently compare the omega^2 pole/residue and matter/source normalization; do not infer it from q-plane matching.
8. **Kinetic/gradient gate** — after full elimination and normalization, verify no ghost, gradient stability and hyperbolicity.
9. **DOF gate** — establish the degree-of-freedom count from the actual action/constraint algebra.
10. **IR/UV gate** — recover the tested RTK IR kernel in its validity domain and state the EFT cutoff above all used scales.
11. **PPN/GW gate** — check the same parameter set against the pinned Newton normalization, preferred-frame and GW constraints.

## Reproducible algebraic tools

Base Schur tool:

`rtk/route_b_flrw_schur_kernel.py`

Original commit: `175adcc14bdfcdfc83218055dcbe4b0096545980`.

Rank/q-residue theorem diagnostic:

`rtk/route_b_flrw_schur_rank_residue.py`

Original commit: `5029f5dd9bc62665063a926bc260a871bb9bb6f9`.
Terminology/sign-theorem refinement: `524849364e0911f0afc35059c4dd3ac7d63c2b3e`.

Separate physical pole/residue distinction theorem:

`rtk/route_b_pole_residue_distinction.py`.

The exact-arithmetic C8 tests now cover:

- exact Schur-complement elimination;
- A<->B, P<->R symmetry;
- D2=det(M1);
- the strict-linear implication rank(M1)=1;
- rejection of full-rank M1 and rank-zero M1 as strict nonconstant linear-denominator carriers;
- exact q-plane pole location;
- normalized q-plane residues;
- opposite sign of the Schur contribution in K_eff;
- invariance under common numerator/denominator scaling;
- positive and negative rank-one gradient examples confirming the conditional q-plane sign rule.

## Interpretation rule

Passing these algebraic tools is not evidence for a complete theory. Their purpose is to reject impossible coefficient patterns early and to prevent a future carrier proposal from matching only a denominator while silently failing its q-plane residue, local polynomial part, dynamical propagator normalization, or source coupling.

A C8 success claim requires one explicit fixed action to pass the rank, q-pole, q-residue, polynomial-part, physical propagator/source, stability, DOF, IR/UV and observational consistency gates together.
