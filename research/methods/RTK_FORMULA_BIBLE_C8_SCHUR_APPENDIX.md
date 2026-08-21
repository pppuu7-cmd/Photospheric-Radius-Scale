# RTK Formula Bible — C8 FLRW Schur Appendix

Date: 2026-08-21
Status: canonical detailed derivation appendix

## Scope

This appendix reconstructs the exact algebra used by the current C8 FLRW constraint-kernel program. It is deliberately narrower than a covariant-completion theorem.

It distinguishes three objects that must never be conflated:

1. the determinant/rational structure of the nondynamical lapse+shift constraint matrix as a function of a spatial Fourier variable `q`;
2. the off-shell reduced scalar kernel after those constraints are eliminated;
3. the physical propagator pole/residue with respect to `omega^2` after all dynamical fields and source normalizations are fixed.

The formulas in sections 1–7 concern levels (1) and (2). Physical `omega^2` residue is a separate gate, already motivated by `rtk/route_b_pole_residue_distinction.py` on `rtk-class-build`.

---

## 1. Starting quadratic form

Let the nondynamical scalar variables be

`x = (delta N, chi)^T`

and let `zeta` denote the remaining scalar variable at this algebraic stage. Write

`L = 1/2 x^T M(q,H) x + x^T J(q,H) zeta + 1/2 K0(q,H) zeta^2`,

where

`M = [[A,C],[C,B]]`,

`J = (P,R)^T`.

No assumption about a final covariant carrier is made here. `A,B,C,P,R,K0` must eventually be derived from one fixed action; they are not independent epoch-by-epoch fit parameters.

Assumptions for the Schur elimination:

- the two variables in `x` are nondynamical at this stage;
- `M` is invertible away from isolated coefficient poles;
- all quantities use one fixed Fourier/sign convention.

Status: GREEN algebra.

---

## 2. Exact lapse/shift elimination

The constraint equations are

`dL/dx = M x + J zeta = 0`,

hence

`x = -M^{-1} J zeta`.

Substituting gives

`L_eff = 1/2 K_eff zeta^2`,

with

`K_eff = K0 - J^T M^{-1} J`.

For a symmetric 2x2 matrix,

`M^{-1} = adj(M)/det(M)`

and

`adj(M) = [[B,-C],[-C,A]]`.

Therefore

`J^T adj(M) J = B P^2 - 2 C P R + A R^2`.

Define

`D(q,H) = A B - C^2`,

`N(q,H) = B P^2 - 2 C P R + A R^2`.

Then

`K_eff(q,H) = K0(q,H) - N(q,H)/D(q,H)`.

This is the exact two-constraint Schur complement.

Status: GREEN exact identity.

Provenance:

- base exact-arithmetic implementation: `rtk/route_b_flrw_schur_kernel.py` on `rtk-class-build`;
- original implementation commit: `175adcc14bdfcdfc83218055dcbe4b0096545980`.

---

## 3. Linear-in-q determinant and the rank-one theorem

Take the diagnostic truncation

`A=a0+a1 q`,

`B=b0+b1 q`,

`C=c0+c1 q`.

Equivalently,

`M(q)=M0+q M1`,

where

`M1=[[a1,c1],[c1,b1]]`.

Direct expansion gives

`D(q)=D0+D1 q+D2 q^2`,

with

`D0=a0 b0-c0^2`,

`D1=a0 b1+a1 b0-2 c0 c1`,

`D2=a1 b1-c1^2`.

But

`D2 = det(M1)`.

Suppose the intended reduced coefficient has a **strict nonconstant linear denominator**. Then its determinant must satisfy

`D2=0`

and

`D1 != 0`.

The first condition makes `M1` singular. The second condition excludes `M1=0`, because if `a1=b1=c1=0` then automatically `D1=0`.

For a 2x2 matrix the only remaining possibility is therefore

`rank(M1)=1`.

So the stronger necessary gate is

**strict nonconstant linear denominator => rank(M1)=1**.

Interpretation: at this truncation order only one independent linear combination of the two nondynamical constraints can carry the leading q-gradient structure.

Non-claim: this is not automatically a DHOST degeneracy condition. DHOST degeneracy is a statement about the Hessian/constraint structure of a specified covariant action and must be derived from that action.

Status: GREEN exact reduced-matrix theorem; RED for action-level identification.

Provenance:

- theorem implementation: `rtk/route_b_flrw_schur_rank_residue.py` on `rtk-class-build`;
- first rank/residue commit: `5029f5dd9bc62665063a926bc260a871bb9bb6f9`;
- terminology/sign refinement: `524849364e0911f0afc35059c4dd3ac7d63c2b3e`.

---

## 4. Correctly normalized q-plane residue

For a strict linear denominator

`D(q)=D0+D1 q`,

with `D1 != 0`, the simple q-plane pole is

`q_p = -D0/D1`.

Let `N(q)` be any polynomial regular at `q_p`. Near the pole,

`D(q) = D1 (q-q_p)`.

Therefore

`N(q)/D(q) ~ [N(q_p)/D1] / (q-q_p)`.

Thus

`Res_q[N/D] = N(q_p)/D1`.

Because the Schur term enters with a minus sign,

`K_eff = K0 - N/D`,

its q-plane residue is

`Res_q[Schur in K_eff] = -N(q_p)/D1`.

This corrects a common shortcut: `N(q_p)` is the polynomial-division remainder, but it is not by itself the normalized residue if denominator normalization can change.

Under a common nonzero scaling

`N -> s N`, `D -> s D`,

we have

`N(q_p)/D1 -> s N(q_p)/(s D1)`,

so the normalized q-plane residue is invariant.

Status: GREEN exact simple-pole algebra.

---

## 5. Rank-one factorization and closed pole formula

For a real symmetric rank-one matrix `M1`, write

`M1 = sigma v v^T`,

where `sigma = +1` or `-1` is the sign of its unique nonzero eigenvalue; the magnitude is absorbed into the real vector `v`.

Assume now that `M0` is invertible and define

`a = v^T M0^{-1} v`.

The matrix determinant lemma states

`det(M0 + u w^T) = det(M0) [1 + w^T M0^{-1} u]`.

Choose

`u = q sigma v`, `w=v`.

Then

`det(M0 + q sigma v v^T)`
`= det(M0) [1 + q sigma v^T M0^{-1} v]`
`= det(M0) [1 + q sigma a]`.

Therefore, when `a != 0`,

`q_p = -1/(sigma a)`.

This gives the coefficient-pole location without expanding the determinant coefficient by coefficient.

Status: GREEN conditional exact theorem (`M0` invertible, rank-one real symmetric `M1`).

---

## 6. Sherman–Morrison and the conditional q-residue sign theorem

For the same assumptions, Sherman–Morrison gives

`(M0 + q sigma v v^T)^(-1)`
`= M0^(-1)`
` - [q sigma M0^(-1) v v^T M0^(-1)]/[1+q sigma a]`.

Define

`b(q) = v^T M0^(-1) J(q)`.

Then

`J^T M^{-1} J`
`= J^T M0^{-1} J - q sigma b(q)^2/[1+q sigma a]`.

Hence

`K_eff`
`= K0 - J^T M0^{-1} J`
`  + q sigma b(q)^2/[1+q sigma a]`.

The first two terms are regular at `q_p` if `K0` and `J` are regular there. The singular part has residue

`Res_q[Schur in K_eff]`
`= [q_p sigma b(q_p)^2]/[sigma a]`
`= q_p b(q_p)^2/a`.

Using

`q_p=-1/(sigma a)`,

we obtain

`Res_q[Schur in K_eff]`
`= - b(q_p)^2/[sigma a^2]`.

Since `b(q_p)^2 >= 0` and `a^2>0`, a nonzero q-plane residue has sign

`sign Res_q = -sigma`.

Therefore:

- positive unique eigenvalue of `M1` => nonzero q-plane Schur residue is negative;
- negative unique eigenvalue of `M1` => nonzero q-plane Schur residue is positive;
- if `b(q_p)=0`, the determinant zero is canceled from that mixing/source channel and the channel has no simple q-plane pole.

This creates a new early rejection test for candidate action maps once the sign of their target q-plane coefficient residue is fixed.

Non-claims:

- not a ghost/no-ghost criterion;
- not the physical `omega^2` propagator residue;
- not a source-normalization proof;
- not valid when `M0` is singular without a separate derivation;
- not a general statement for higher-rank or higher-degree q kernels.

Status: GREEN conditional reduced-kernel sign theorem; YELLOW until applied to one explicit RTK carrier action.

---

## 7. Why q-plane and omega^2 residues are separate

The existing Route-B exact test compares

`K_BPS = A omega^2 - G q^2/(1+r q^2)`

and

`K_RTK = A(1+r q^2) omega^2 - G q^2`.

They satisfy

`K_RTK=(1+r q^2) K_BPS`

and have the same on-shell dispersion

`omega^2=(G/A) q^2/(1+r q^2)`,

but for the same fixed source normalization their propagators and `omega^2` residues differ by the momentum factor.

Therefore:

**matching a q-plane coefficient pole is weaker than matching the off-shell kernel, and matching the on-shell omega^2 pole is also weaker than matching the physical source-coupled propagator residue.**

C8 must eventually pass all of these levels with one fixed action and one consistent field/source normalization.

Canonical prior theorem: `rtk/route_b_pole_residue_distinction.py` on `rtk-class-build`.

Status: GREEN distinction theorem; full action/source map remains RED.

---

## 8. Current C8 gate sequence

A candidate is not accepted by satisfying one algebraic identity. The current required sequence is:

1. derive `M0,M1,J,K0` from one explicit fixed action;
2. check intended nondynamical variables and DOF count;
3. if a strict linear q denominator is claimed, require `rank(M1)=1`;
4. match the q-plane pole at multiple FLRW epochs with the same Wilson coefficients;
5. match the normalized q-plane residue and its sign;
6. verify the pole does not disappear through `b(q_p)=0` when a nonzero target residue is required;
7. match the polynomial/local part after division;
8. independently match the physical omega^2 propagator/source response;
9. verify kinetic sign, gradient stability and hyperbolicity;
10. derive EFT/strong-coupling cutoff;
11. apply the same parameter tuple to PPN/Newton/GW constraints;
12. only then compare to observational transfer functions/nonlinear limits.

Current status: YELLOW/RED overall. The exact reduced-matrix algebra is GREEN; a fixed healthy carrier that passes the whole chain is not yet established.

---

## 9. Verification and provenance

Primary files:

- `rtk-class-build:rtk/route_b_flrw_schur_kernel.py`
- `rtk-class-build:rtk/route_b_flrw_schur_rank_residue.py`
- `rtk-class-build:research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md`
- `rtk-class-build:rtk/route_b_pole_residue_distinction.py`

GitHub-hosted self-test workflow:

- `main:.github/workflows/rtk-c8-flrw-schur-selftest.yml`
- final q-residue theorem retrigger commit: `b6fb32f79b1bc951ea7ae50b8bdda5947c526229`.

A workflow success proves only that the encoded algebraic self-tests passed under the recorded runtime. It does not promote C8 to a completed physical theory.
