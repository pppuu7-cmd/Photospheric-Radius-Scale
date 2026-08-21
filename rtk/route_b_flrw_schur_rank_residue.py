#!/usr/bin/env python3
"""Exact C8 diagnostics for strict-linear FLRW Schur denominators.

This module concerns the rational dependence on the spatial Fourier variable q
after lapse/shift elimination.  Its `q-plane residue` is *not* the physical
propagator residue with respect to omega^2.  The latter is a separate dynamical
question covered by route_b_pole_residue_distinction.py and future action-level
stability/source-coupling analyses.

For a real symmetric two-constraint matrix

    M(q) = M0 + q M1
         = [[A0+A1 q, C0+C1 q],
            [C0+C1 q, B0+B1 q]],

we have

    det M(q) = D0 + D1 q + D2 q^2,
    D2 = det M1 = A1 B1 - C1^2.

If det M is strictly linear and nonconstant, D2=0 and D1!=0.  Hence M1 is
nonzero and singular, so for a 2x2 matrix rank(M1)=1 exactly.

For

    K_eff(q) = K0(q) - N(q)/D(q),

and the simple q-plane pole q*= -D0/D1,

    Res_q[N/D]              =  N(q*)/D1,
    Res_q[Schur in K_eff]   = -N(q*)/D1.

The unnormalised polynomial remainder N(q*) is therefore insufficient when
comparing representations with differently normalised denominators.

Conditional sign theorem.  If in addition M0 is invertible, write the real
rank-one symmetric gradient block as

    M1 = sigma v v^T,  sigma in {+1,-1}.

Let

    a = v^T M0^{-1} v,
    b(q) = v^T M0^{-1} J(q).

Matrix determinant lemma and Sherman-Morrison give

    q* = -1/(sigma a),

and, provided K0 and J are regular at q*,

    Res_q[Schur in K_eff]
      = - b(q*)^2 / (sigma a^2).

Thus a nonzero q-plane Schur residue has sign opposite to the sole nonzero
eigenvalue of M1.  If b(q*)=0 the pole cancels from that source/mixing channel.
This is an exact reduced-kernel statement only; it is not a DHOST degeneracy,
physical omega^2 residue, ghost, or UV-completion theorem.
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


def rankone_gradient_sign(kernel: ConstraintKernel) -> int:
    """Sign (+1/-1) of the unique nonzero eigenvalue of rank-one symmetric M1.

    For a rank-one 2x2 symmetric matrix the nonzero eigenvalue equals trace(M1).
    """
    if gradient_block_rank(kernel) != 1:
        raise ValueError("rank-one gradient block required")
    trace = kernel.A.c1 + kernel.B.c1
    if trace == 0:
        raise AssertionError("nonzero rank-one symmetric matrix cannot have zero trace")
    return 1 if trace > 0 else -1


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


def qplane_residues(kernel: ConstraintKernel) -> tuple[Fraction, Fraction]:
    """Return (Res_q[N/D], Res_q[-N/D]) at the simple spatial-q pole."""
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
        "classification": "C8_FLRW_STRICT_LINEAR_QPLANE_THEOREM_DIAGNOSTIC",
        "D0": str(d0),
        "D1": str(d1),
        "D2": str(d2),
        "gradient_block_rank": rank,
        "strict_linear_denominator_gate": strict,
        "rank_one_necessary_gate": strict and rank == 1,
        "residue_variable": "q (spatial Fourier variable), not omega^2",
        "warning": (
            "Exact reduced-constraint algebra only. q-plane residue is not the "
            "physical propagator residue; passing this is neither DHOST degeneracy "
            "nor a stability/UV-completion proof."
        ),
    }
    if rank == 1:
        out["rankone_gradient_eigenvalue_sign"] = rankone_gradient_sign(kernel)
    if strict:
        qstar = pole_location(kernel)
        r_plus, r_eff = qplane_residues(kernel)
        out.update(
            {
                "q_pole": str(qstar),
                "qplane_residue_N_over_D": str(r_plus),
                "qplane_residue_Keff_Schur_term": str(r_eff),
            }
        )
        if rank == 1 and r_eff != 0 and d0 != 0:
            sigma = rankone_gradient_sign(kernel)
            observed_sign = 1 if r_eff > 0 else -1
            out["conditional_rankone_residue_sign_gate"] = observed_sign == -sigma
    return out


def _self_test() -> None:
    # Positive rank-one q-gradient block and strict linear determinant.
    one = ConstraintKernel(
        A=Linear.make(1, 1),
        B=Linear.make(2, 4),
        C=Linear.make(0, 2),
        P=Linear.make(1, 0),
        R=Linear.make(0, 0),
    )
    assert one.determinant_coeffs() == (Q(2), Q(6), Q(0))
    assert gradient_block_rank(one) == 1
    assert rankone_gradient_sign(one) == 1
    assert strict_linear_denominator_gate(one)
    assert pole_location(one) == Q(-1, 3)
    # N=B=2+4q. At q*=-1/3, N*=2/3 and D'=6.
    assert qplane_residues(one) == (Q(1, 9), Q(-1, 9))
    assert theorem_report(one)["conditional_rankone_residue_sign_gate"]

    # Flip M1 -> -M1.  The unique gradient eigenvalue and q-plane Schur
    # residue both flip sign relative to the previous example.
    neg = ConstraintKernel(
        A=Linear.make(1, -1),
        B=Linear.make(2, -4),
        C=Linear.make(0, -2),
        P=Linear.make(1, 0),
        R=Linear.make(0, 0),
    )
    assert neg.determinant_coeffs() == (Q(2), Q(-6), Q(0))
    assert gradient_block_rank(neg) == 1
    assert rankone_gradient_sign(neg) == -1
    assert pole_location(neg) == Q(1, 3)
    assert qplane_residues(neg) == (Q(-1, 9), Q(1, 9))
    assert theorem_report(neg)["conditional_rankone_residue_sign_gate"]

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

    # Rank-zero gradient block cannot give a nonconstant linear denominator.
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

    # Common scaling of numerator and denominator leaves the q-plane residue.
    d1 = Q(6)
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
