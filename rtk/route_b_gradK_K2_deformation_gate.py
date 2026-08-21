#!/usr/bin/env python3
"""C8 exact gate for a K^2 deformation of the base scalar constraint.

We test whether the simplest modified-base-constraint idea can regularize the
minimal grad-K carrier: deform the ADM kinetic term

  M_*^2/2 [ K_ij K^ij - K^2 + eta K^2 ]

while retaining the same clock quadratic coefficient K_clock and allowing the
most general scalar grad-K correction

  p^2 [ U A^2 + 2 V A q + W q^2 ],
  A=dot(zeta)-H n, q=p^2 psi.

At quadratic flat-FLRW order

  delta K_ij delta K^ij - delta K^2 = -6 A^2 -4 A q,
  (delta K)^2 = 9 A^2 +6 A q +q^2.

We eliminate lapse n and shift q exactly and demand the production RTK kinetic
factor for all s=p^2:

  K_eff(s) = K_clock/H^2 * (1+s/M_K^2).

After clearing denominators, the exact identity is a cubic polynomial in s.
Its constant coefficient is

  -K_clock^2 M_*^2 M_K^2 eta.

For positive finite K_clock, M_*^2, M_K^2 exact matching therefore forces
eta=0, independently of U,V,W. The naive K^2/lambda deformation cannot be the
mechanism that removes the zero-H singular coefficient while preserving the
same exact RTK scalar kinetic target.

Scope: quadratic flat-FLRW; this one-parameter base kinetic deformation with the
same clock sector. Not a no-go for more general modified constraints,
auxiliaries, beyond-quadratic degeneracy, or retarded/nonlocal completions.
"""

import json
import sympy as sp

# eta must be allowed to vanish because eta=0 is precisely the theorem result.
H,M2,Kc,MK2,s,U,V,W,d = sp.symbols(
    'H M2 Kc MK2 s U V W d', nonzero=True, finite=True, real=True)
eta = sp.symbols('eta', finite=True, real=True)
n,q = sp.symbols('n q', finite=True, real=True)
A = d-H*n

L = (
    sp.Rational(1,2)*Kc*n**2
    + sp.Rational(1,2)*M2*((-6+9*eta)*A**2 + (-4+6*eta)*A*q + eta*q**2)
    + s*(U*A**2 + 2*V*A*q + W*q**2)
)

sol = sp.solve([sp.diff(L,n),sp.diff(L,q)],[n,q],simplify=False,dict=True)[0]
Keff = sp.factor(2*L.subs(sol)/d**2)
target = Kc/H**2*(1+s/MK2)
num = sp.factor(sp.fraction(sp.together(Keff-target))[0])
poly = sp.Poly(sp.expand(num),s)
assert poly.degree() == 3
coeff = [sp.factor(c) for c in poly.all_coeffs()]

# Coefficients ordered s^3,s^2,s^1,s^0.
assert sp.simplify(coeff[0] + 4*H**2*Kc*(U*W-V**2)) == 0
assert sp.simplify(coeff[-1] + Kc**2*M2*MK2*eta) == 0

# Exact matching requires the constant coefficient to vanish. Since the three
# physical prefactors are explicitly nonzero, the unique eta solution is zero.
eta_solution = sp.solve(sp.Eq(coeff[-1],0),eta)
assert eta_solution == [0]

# eta=0 recovers the previously derived rank-one requirement at highest order.
assert sp.factor(coeff[0].subs(eta,0)) == -4*H**2*Kc*(U*W-V**2)

out = {
  'classification':'RTK_ROUTE_B_GRADK_K2_DEFORMATION_GATE_PASS',
  'action_deformation':'M_*^2/2 [K_ij K^ij-K^2+eta K^2]',
  'target':'K_eff=K_clock/H^2 (1+p^2/M_K^2)',
  'polynomial_degree_in_p2':3,
  'constant_coefficient':'-K_clock^2 M_*^2 M_K^2 eta',
  'theorem':'For finite nonzero K_clock, M_*^2 and M_K^2, exact RTK matching for all p^2 forces eta=0 independently of U,V,W.',
  'consequence':'A simple Hořava-lambda/K^2 deformation cannot regularize the minimal grad-K zero-H problem while preserving the same exact RTK quadratic scalar target and clock sector.',
  'ci_debug_note':'The first CI attempt incorrectly declared eta nonzero while testing eta=0. This implementation-only contradiction was removed; the analytic coefficient identity itself was unchanged.',
  'scope':'quadratic flat-FLRW; one K^2 deformation; unchanged clock coefficient; more general modified constraints/auxiliaries/nonlocal completions remain open',
  'next_step':'Test genuinely new constraint structures rather than a pure K^2 coefficient deformation; prioritize branches with regular static limit and explicit DOF/strong-coupling control.'
}
print('RTK_ROUTE_B_GRADK_K2_DEFORMATION_GATE_PASS',json.dumps(out,sort_keys=True))
