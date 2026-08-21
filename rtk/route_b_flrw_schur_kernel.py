#!/usr/bin/env python3
"""Algebraic C8 diagnostic for a two-constraint FLRW scalar kernel.

This module does *not* claim a covariant completion.  It isolates the algebra that
any proposed lapse+shift carrier must satisfy after the nondynamical constraints
are eliminated.

Let q denote the Fourier variable (for example k^2/a^2) and

    M(q) = [[A(q), C(q)],
            [C(q), B(q)]]

be the quadratic constraint matrix for x=(delta N, chi).  If the propagating
scalar zeta couples through J=(P,R),

    L = 1/2 x^T M x + x^T J zeta + 1/2 K0 zeta^2,

then exact elimination gives

    K_eff = K0 - (B P^2 - 2 C P R + A R^2)/(A B - C^2).

For coefficients linear in q, det(M) is generically quadratic.  A strict
single-linear-pole target therefore requires the q^2 coefficient of det(M) to
vanish.  Matching the pole is only the first gate: the rational residue must
also match.  The functions below expose both denominator and numerator
coefficients exactly using fractions.Fraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import argparse
import json
from typing import Iterable, Sequence

Q = Fraction


def _q(x: int | float | str | Fraction) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, float):
        return Fraction(str(x))
    return Fraction(x)


def _poly_add(a: Sequence[Fraction], b: Sequence[Fraction]) -> tuple[Fraction, ...]:
    n = max(len(a), len(b))
    out = [Q(0) for _ in range(n)]
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def _poly_scale(a: Sequence[Fraction], s: Fraction) -> tuple[Fraction, ...]:
    return tuple(s * x for x in a)


def _poly_mul(a: Sequence[Fraction], b: Sequence[Fraction]) -> tuple[Fraction, ...]:
    out = [Q(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def _poly_eval(a: Sequence[Fraction], q: Fraction) -> Fraction:
    acc = Q(0)
    for x in reversed(a):
        acc = acc * q + x
    return acc


@dataclass(frozen=True)
class Linear:
    c0: Fraction
    c1: Fraction

    @classmethod
    def make(cls, c0=0, c1=0) -> "Linear":
        return cls(_q(c0), _q(c1))

    def poly(self) -> tuple[Fraction, Fraction]:
        return (self.c0, self.c1)


@dataclass(frozen=True)
class ConstraintKernel:
    A: Linear
    B: Linear
    C: Linear
    P: Linear
    R: Linear

    def determinant_coeffs(self) -> tuple[Fraction, Fraction, Fraction]:
        """Return D0,D1,D2 for det M = D0 + D1 q + D2 q^2."""
        a0, a1 = self.A.c0, self.A.c1
        b0, b1 = self.B.c0, self.B.c1
        c0, c1 = self.C.c0, self.C.c1
        return (
            a0 * b0 - c0 * c0,
            a0 * b1 + a1 * b0 - 2 * c0 * c1,
            a1 * b1 - c1 * c1,
        )

    def numerator_coeffs(self) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        """Return N0..N3 for N=B P^2 - 2 C P R + A R^2."""
        bp2 = _poly_mul(self.B.poly(), _poly_mul(self.P.poly(), self.P.poly()))
        cpr = _poly_mul(self.C.poly(), _poly_mul(self.P.poly(), self.R.poly()))
        ar2 = _poly_mul(self.A.poly(), _poly_mul(self.R.poly(), self.R.poly()))
        n = _poly_add(_poly_add(bp2, _poly_scale(cpr, Q(-2))), ar2)
        return tuple(list(n) + [Q(0)] * (4 - len(n)))[:4]

    def single_pole_gate(self) -> bool:
        """Necessary condition for det M to be at most linear in q."""
        return self.determinant_coeffs()[2] == 0

    def evaluate_rational_subtraction(self, q) -> Fraction:
        q = _q(q)
        d = _poly_eval(self.determinant_coeffs(), q)
        if d == 0:
            raise ZeroDivisionError("constraint determinant vanishes at requested q")
        return _poly_eval(self.numerator_coeffs(), q) / d


def proportional_linear_denominator(
    actual: Sequence[Fraction], target: Sequence[Fraction]
) -> tuple[bool, Fraction | None]:
    """Check D(q)=s*T(q) for a linear target, returning (pass, scale)."""
    if len(actual) < 3:
        actual = tuple(actual) + (Q(0),) * (3 - len(actual))
    d0, d1, d2 = actual[:3]
    t0, t1 = target[:2]
    if d2 != 0:
        return False, None
    candidates: list[Fraction] = []
    if t0 != 0:
        candidates.append(d0 / t0)
    elif d0 != 0:
        return False, None
    if t1 != 0:
        candidates.append(d1 / t1)
    elif d1 != 0:
        return False, None
    if not candidates:
        return False, None
    s = candidates[0]
    if s == 0 or any(x != s for x in candidates[1:]):
        return False, None
    return True, s


def linear_remainder(poly: Sequence[Fraction], den: Sequence[Fraction]) -> tuple[Fraction]:
    """Return the constant remainder of poly(q) modulo d0+d1*q.

    This is the invariant rational residue numerator after polynomial pieces are
    separated, provided d1 != 0.  It equals poly(q_pole) with q_pole=-d0/d1.
    """
    d0, d1 = den[:2]
    if d1 == 0:
        raise ValueError("linear denominator requires nonzero q coefficient")
    q_pole = -d0 / d1
    return (_poly_eval(poly, q_pole),)


def diagnostic(kernel: ConstraintKernel, target_den: Sequence[Fraction] | None = None) -> dict:
    d = kernel.determinant_coeffs()
    n = kernel.numerator_coeffs()
    out = {
        "classification": "C8_FLRW_SCHUR_ALGEBRAIC_DIAGNOSTIC",
        "determinant": [str(x) for x in d],
        "numerator": [str(x) for x in n],
        "single_linear_pole_gate": d[2] == 0,
        "warning": (
            "Algebraic constraint-kernel diagnostic only. Passing it neither proves "
            "DHOST degeneracy nor supplies a covariant UV completion."
        ),
    }
    if target_den is not None:
        td = tuple(_q(x) for x in target_den)
        ok, scale = proportional_linear_denominator(d, td)
        out["target_denominator"] = [str(x) for x in td]
        out["target_pole_match"] = ok
        out["target_denominator_scale"] = None if scale is None else str(scale)
        if ok and td[1] != 0:
            out["rational_residue_remainder"] = str(linear_remainder(n, d[:2])[0])
    return out


def _self_test() -> None:
    # Diagonal M: subtraction = P^2/A + R^2/B.
    k = ConstraintKernel(
        A=Linear.make(2, 0), B=Linear.make(3, 0), C=Linear.make(0, 0),
        P=Linear.make(5, 0), R=Linear.make(7, 0),
    )
    assert k.evaluate_rational_subtraction(11) == Q(25, 2) + Q(49, 3)

    # Symmetry A<->B, P<->R leaves det and numerator invariant.
    k1 = ConstraintKernel(
        A=Linear.make(2, 3), B=Linear.make(5, 7), C=Linear.make(11, 13),
        P=Linear.make(17, 19), R=Linear.make(23, 29),
    )
    k2 = ConstraintKernel(A=k1.B, B=k1.A, C=k1.C, P=k1.R, R=k1.P)
    assert k1.determinant_coeffs() == k2.determinant_coeffs()
    assert k1.numerator_coeffs() == k2.numerator_coeffs()

    # Necessary one-pole condition D2=a1*b1-c1^2=0.
    one = ConstraintKernel(
        A=Linear.make(1, 1), B=Linear.make(2, 4), C=Linear.make(0, 2),
        P=Linear.make(1, 0), R=Linear.make(0, 0),
    )
    assert one.determinant_coeffs()[2] == 0
    assert one.single_pole_gate()
    assert proportional_linear_denominator(one.determinant_coeffs(), one.determinant_coeffs()[:2])[0]

    # Generic coefficients need not satisfy the one-pole condition.
    generic = ConstraintKernel(
        A=Linear.make(1, 2), B=Linear.make(3, 5), C=Linear.make(7, 11),
        P=Linear.make(13, 17), R=Linear.make(19, 23),
    )
    assert generic.determinant_coeffs()[2] != 0
    assert not generic.single_pole_gate()

    # Polynomial remainder agrees with evaluation at the pole.
    p = (Q(3), Q(4), Q(5), Q(6))
    d = (Q(2), Q(3))
    rem = linear_remainder(p, d)[0]
    assert rem == _poly_eval(p, Q(-2, 3))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    _self_test()
    if args.self_test:
        print("C8_FLRW_SCHUR_SELFTEST_PASS")
        return

    # A transparent exact-arithmetic example satisfying the necessary D2=0 gate.
    example = ConstraintKernel(
        A=Linear.make(1, 1), B=Linear.make(2, 4), C=Linear.make(0, 2),
        P=Linear.make(1, 1), R=Linear.make(1, 0),
    )
    print(json.dumps(diagnostic(example), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
