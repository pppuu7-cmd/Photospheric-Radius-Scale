# RTK Formula Bible — C8 Residue/Source Redefinition Appendix

Date: 2026-08-21
Status: YELLOW — exact algebra independently checked; GitHub CI rerun pending at time of entry

## Purpose

This appendix connects three already established C8 facts:

1. the constructive BPS family can reproduce the target scalar dispersion pole exactly;
2. equal poles do not imply equal fixed-source off-shell kernels/residues;
3. a complete C8 carrier must derive both the constraint kernel and source map from one fixed local action.

It asks whether the known BPS/RTK kernel mismatch can be repaired by a scalar-only field normalization without changing a standard q-independent source coupling.

## 1. Starting kernels

The prior exact pole/residue distinction theorem uses

`K_BPS = A omega^2 - G q^2/(1+r q^2)`

and

`K_RTK = A(1+r q^2) omega^2 - G q^2`.

Define

`F(q)=1+r q^2`, with `r>0`.

Then exactly

`K_RTK = F(q) K_BPS`.

Thus the two kernels have the same zero in `omega^2`, but if one holds the source normalization fixed their propagator residues differ by `F(q)`.

Provenance: `rtk-class-build:rtk/route_b_pole_residue_distinction.py`.

## 2. General scalar-only multiplicative field map

Start from

`L_BPS = 1/2 K_BPS phi_B^2 + J_B phi_B`.

Let

`phi_B = T(q) phi_R`.

Then

`L = 1/2 [T(q)^2 K_BPS] phi_R^2 + [T(q) J_B] phi_R`.

Therefore

`K_new = T^2 K_BPS`,

`J_new = T J_B`.

Exact off-shell kernel matching `K_new=K_RTK` forces

`T(q)^2 = F(q)`.

On the positive branch,

`T(q)=sqrt(1+r q^2)`.

So the exact scalar normalization required to convert the BPS kernel to the RTK kernel also transforms an initially q-independent source into

`J_R = sqrt(1+r q^2) J_B`.

Status: GREEN exact algebra; physical interpretation remains conditional on the underlying action/source definition.

## 3. Source-response invariant

A crucial guard against a false no-go is that a legitimate field redefinition must transform the source consistently.

After integrating out a Gaussian scalar, the source-source response is proportional to

`J^2/K`.

Under the transformation above,

`J_new^2/K_new`
`= [T^2 J_B^2]/[T^2 K_BPS]`
`= J_B^2/K_BPS`.

Thus

`J_R^2/K_RTK = J_B^2/K_BPS`

exactly.

Therefore the fixed-source residue mismatch is **not by itself a physical inequivalence theorem**. If field and source are transformed together, the quadratic source response is invariant.

This sharpens the C8 question: can the necessary source/field normalization arise from the intended local fixed action and matter coupling, rather than being inserted as an arbitrary momentum-space transformation?

## 4. Finite-derivative locality gate

For a scalar-only local finite-spatial-derivative redefinition, `T` would be a finite polynomial in `x=q^2`.

Suppose a polynomial `P(x)` obeyed

`P(x)^2 = 1+r x`, `r>0`.

If `deg P=n>=1`, then

`deg(P^2)=2n`,

which is even and at least two, while the target right-hand side has degree one. Contradiction.

If `deg P=0`, then `P^2` is constant and cannot reproduce the nonzero `r x` term.

Hence there is no finite polynomial `P(q^2)` whose square is exactly `1+r q^2` for `r>0`.

So the scalar-only exact map

`T=sqrt(1+r q^2)`

is pseudodifferential/infinite-derivative when viewed as a direct single-field spatial operator.

Status: GREEN scoped mathematical statement.

## 5. Correct interpretation

The result is **not** a no-go for RTK and not a no-go for local completion.

It excludes only the shortcut:

> take the BPS pole-equivalent scalar kernel, apply a scalar-only finite-derivative local normalization, and simultaneously demand that an initially q-independent fixed source coupling remain unchanged.

Allowed escape routes remain:

- lapse/shift mixing whose Schur complement dynamically generates the same normalization/source factor;
- extra auxiliary local fields whose elimination realizes the effective pseudodifferential factor;
- a derived matter/disformal source map consistent with equivalence-principle, PPN and GW constraints;
- a different local carrier whose off-shell scalar kernel already has the target RTK normalization.

## 6. Consequence for the C8 program

The previously proved exact BPS dispersion embedding remains valid. The new result tells us precisely what it still does not provide.

The next nonredundant action-level gate is:

1. choose one explicit fixed FLRW action;
2. derive its nondynamical lapse/shift matrix `M` and source vector `J=(P,R)`;
3. perform exact Schur elimination;
4. match the RTK q-plane denominator;
5. match the normalized q-plane residue;
6. verify the source-source response without inserting `sqrt(1+r q^2)` by hand;
7. then apply DOF, stability, cutoff, PPN/Newton/GW and observational gates to that same fixed parameter tuple.

This is now the preferred C8 bridge between the exact BPS pole theorem and a genuine off-shell/local carrier.

## 7. Verification/provenance

Executable theorem:

- `rtk-class-build:rtk/route_b_residue_source_redefinition_gate.py`
- refined source-response commit: `7f5fda897938e24170b8a0228ce8a392e4110e8a`

CI workflow:

- `main:.github/workflows/rtk-route-b-residue-source-redefinition.yml`
- refined retrigger commit: `2fcc9fb34fdffcd65a7fd487d6a1aff300ab4e85`

The key symbolic identities were independently re-evaluated before this appendix was written. CI status must still be inspected before promoting this appendix from YELLOW to GREEN in the central status table.
