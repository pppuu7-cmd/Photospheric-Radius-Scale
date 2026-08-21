#!/usr/bin/env python3
"""Exact C8 theorem diagnostic for strict linear FLRW Schur poles.

This file strengthens the algebraic filter in route_b_flrw_schur_kernel.py.
It does not claim a DHOST degeneracy condition or a covariant UV completion.

For a two-constraint matrix

    M(q) = M0 + q M1
         = [[A0+A1 q, C0+C1 q],
            [C0+C1 q, B0+B1 q]],

we have

    det M(q) = D0 + D1 q + D2 q^2,
    D2 = det M1 = A1 B1 - C1^2.

If det M is required to be strictly linear and nonconstant, then D2=0 and
D1!=0.  D1!=0 excludes M1=0, so M1 must be nonzero and singular.  For a 2x2
matrix this means rank(M1)=1 exactly.

For

    K_eff = K0 - N(q)/D(q),

and a simple pole q*= -D0/D1, the representation-independent pole residue is

    Res[N/D] = N(q*) / D'(q*) = N(q*) / D1,

while the pole residue of the Schur subtraction appearing in K_eff is

    Res[K_eff pole] = -N(q*) / D1.

The unnormalised remainder N(q*) alone is not sufficient for comparing two
denominator normalisations.
"""

from __future__ import annotations

from fractions import Fraction
import argparse
import json

from route_b_flrw_schur_kernel import ConstraintKernel, Linear, Q


def gradient_block_rank(kernel: ConstraintKernel) -> int:
    """Exact rank of M1=[[a1,c1],[c1,b1]] for the linear-in-q kernel."""
    a1 = kernel.A.c1
    b1 = kernel.B.c1
    c1 = kernel.C.c1
    if a1 == 0 and b1 == 0 and c1 == 0:
        return 0
    if a1 * b1 - c1 * c1 == 0:
        return 1
    return 2


def strict_linear_denominator_gate(kernel: ConstraintKernel) -> bool:
    """True iff det M is exactly degree one in q."""
    _d0, d1, d2 = kernel.determinant_coeffs()
    return d2 == 0 and d1 != 0


def pole_location(kernel: ConstraintKernel) -> Fraction:
    d0, d1, d2 = kernel.determinant_coeffs()
    if d2 != 0 or d1 == 0:
        raise ValueError("strict linear denominator required")
    return -d0 / d1


def _poly_eval(coeffs: tuple[Fraction, ...], q: Fraction) -> Fraction:
    out = Q(0)
    for c in reversed(coeffs):
        out = out * q + c
    return out


def normalized_residues(kernel: ConstraintKernel) -> tuple[Fraction, Fraction]:
    """Return (Res[N/D], Res[-N/D]) at the unique simple linear pole."""
    _d0, d1, _d2 = kernel.determinant_coeffs()
    qstar = pole_location(kernel)
    nstar = _poly_eval(kernel.numerator_coeffs(), qstar)
    res_n_over_d = nstar / d1
    return res_n_over_d, -res_n_over_d


def theorem_report(kernel: ConstraintKernel) -> dict:
    d0, d1, d2 = kernel.determinant_coeffs()
    rank = gradient_block_rank(kernel)
    strict = strict_linear_denominator_gate(kernel)
    out = {
        "classification": "C8_FLRW_STRICT_LINEAR_POLE_THEOREM_DIAGNOSTIC",
        "D0": str(d0),
        "D1": str(d1),
        "D2": str(d2),
        "gradient_block_rank": rank,
        "strict_linear_denominator_gate": strict,
        "rank_one_necessary_gate": strict and rank == 1,
        "warning": (
            "Exact algebraic necessary conditions only; this is not a DHOST "
            "degeneracy theorem and not a covariant-completion claim."
        ),
    }
    if strict:
        qstar = pole_location(kernel)
        r_plus, r_eff = normalized_residues(kernel)
        out.update(
            {
                "q_pole": str(qstar),
                "residue_N_over_D": str(r_plus),
                "residue_Keff_Schur_term": str(r_eff),
            }
        )
    return out


def _self_test() -> None:
    # Rank-one q-gradient block and strict linear determinant:
    # M1=[[1,2],[2,4]], det(M1)=0, rank=1.
    one = ConstraintKernel(
        A=Linear.make(1, 1),
        B=Linear.make(2, 4),
        C=Linear.make(0, 2),
        P=Linear.make(1, 0),
        R=Linear.make(0, 0),
    )
    assert one.determinant_coeffs() == (Q(2), Q(6), Q(0))
    assert gradient_block_rank(one) == 1
    assert strict_linear_denominator_gate(one)
    assert pole_location(one) == Q(-1, 3)
    # N=B=2+4q.  At q*=-1/3, N*=2/3; D'=6.
    assert normalized_residues(one) == (Q(1, 9), Q(-1, 9))

    # Full-rank gradient block cannot yield a strict linear determinant.
    full = ConstraintKernel(
        A=Linear.make(1, 1),
        B=Linear.make(1, 1),
        C=Linear.make(0, 0),
        P=Linear.make(1, 0),
        R=Linear.make(0, 0),
    )
    assert gradient_block_rank(full) == 2
    assert full.determinant_coeffs()[2] == 1
    assert not strict_linear_denominator_gate(full)

    # Rank-zero gradient block also cannot give a nonconstant linear denominator.
    zero = ConstraintKernel(
        A=Linear.make(1, 0),
        B=Linear.make(2, 0),
        C=Linear.make(0, 0),
        P=Linear.make(1, 0),
        R=Linear.make(0, 0),
    )
    assert gradient_block_rank(zero) == 0
    assert zero.determinant_coeffs()[1:] == (Q(0), Q(0))
    assert not strict_linear_denominator_gate(zero)

    # Scaling both N and D by the same nonzero factor leaves the normalized
    # residue unchanged.  Test algebraically on a generic simple pole.
    d0, d1 = Q(2), Q(6)
    nstar = Q(2, 3)
    scale = Q(7)
    assert nstar / d1 == (scale * nstar) / (scale * d1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    _self_test()
    if args.self_test:
        print("C8_FLRW_SCHUR_RANK_RESIDUE_SELFTEST_PASS")
        return

    example = ConstraintKernel(
        A=Linear.make(1, 1),
        B=Linear.make(2, 4),
        C=Linear.make(0, 2),
        P=Linear.make(1, 0),
        R=Linear.make(0, 0),
    )
    print(json.dumps(theorem_report(example), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
