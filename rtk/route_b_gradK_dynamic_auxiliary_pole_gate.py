#!/usr/bin/env python3
"""C8 pole-count gate for a genuinely dynamical auxiliary field.

Context
-------
The minimal EH+clock grad-K exact carrier requires a reduced coefficient
U~H^-2 as H->0. A regular algebraic auxiliary cannot generate this while its
constraint Hessian stays finite and nonsingular. The next natural proposal is
to give an auxiliary field y its own kinetic operator.

At fixed spatial momentum, consider the minimal quadratic block

  L = 1/2 K0(w^2,H) X^2
      + b(H) X y
      + 1/2 [A(H)-Z(H) w^2] y^2.

Eliminating y gives

  K_eff = K0 - b^2/[A-Z w^2].

For finite nonzero Z and b this contains an additional frequency-plane pole at

  w_aux^2 = A/Z.

The controlled RTK quadratic scalar target is polynomial/linear in w^2 at fixed
p^2; it does not contain this extra finite auxiliary pole. Therefore this
minimal single-dynamical-auxiliary completion cannot be exactly off-shell
equivalent to the RTK target unless the pole is removed by a special mechanism:

  * b=0 (the auxiliary decouples),
  * Z=0 (returns to the algebraic-auxiliary case),
  * A/Z is sent outside the exact domain/infinite-mass limit, or
  * a larger degenerate system supplies an exact numerator/denominator
    cancellation and must then be checked by a full DOF/constraint analysis.

There is also a zero-H regularity consequence. If b and Z remain finite and
nonzero while one tries to obtain an H^-2 enhancement from b^2/A, then A->0;
consequently w_aux^2=A/Z->0. The attempt to regularize the Wilson coefficient
turns the extra auxiliary excitation into a light/zero-frequency mode rather
than removing the singular behavior. This is precisely where a strong-coupling
or branch-change analysis becomes mandatory.

Scope
-----
This is a minimal one-dynamical-auxiliary quadratic theorem. It is NOT a no-go
for deliberately degenerate multi-field theories, gauge constraints, exact
pole-zero cancellations derived from a larger local action, or controlled
retarded/nonlocal completions.
"""

import json
import sympy as sp

w2, H = sp.symbols('w2 H', finite=True, real=True)
K0, A, Z, b = sp.symbols('K0 A Z b', nonzero=True, finite=True, real=True)

Keff = sp.factor(K0 - b**2/(A-Z*w2))
num, den = sp.fraction(sp.together(Keff))
assert sp.factor(den) == A-Z*w2

pole = sp.solve(sp.Eq(den,0), w2)
assert pole == [A/Z]

# A finite nonzero mixing leaves a nonzero residue at the auxiliary pole.
res = sp.simplify(sp.limit((w2-A/Z)*Keff, w2, A/Z))
assert sp.simplify(res - b**2/Z) == 0

# Decoupling removes the pole from the reduced X kernel.
assert sp.simplify(Keff.subs(b,0)-K0) == 0

# Z->0 reproduces the algebraic Schur complement.
assert sp.simplify(Keff.subs(Z,0) - (K0-b**2/A)) == 0

# Zero-H scaling example: finite b,Z, A~H^2 gives the desired H^-2 static
# enhancement but simultaneously sends the extra pole to zero frequency.
a2,b0,z0 = sp.symbols('a2 b0 z0', positive=True, finite=True, real=True)
A_H = a2*H**2
static_enhancement = sp.simplify(b0**2/A_H)
pole_H = sp.simplify(A_H/z0)
assert sp.simplify(H**2*static_enhancement - b0**2/a2) == 0
assert sp.limit(pole_H,H,0,dir='+') == 0

out = {
  'classification':'RTK_ROUTE_B_GRADK_DYNAMIC_AUXILIARY_POLE_GATE_PASS',
  'minimal_block':{
    'action':'1/2 K0 X^2 + b X y + 1/2(A-Z omega^2)y^2',
    'reduced':'K_eff=K0-b^2/(A-Z omega^2)',
    'auxiliary_pole':'omega_aux^2=A/Z',
    'pole_residue_in_Keff':'b^2/Z'
  },
  'exact_target_gate':'For finite nonzero b and Z, a new finite omega^2 pole is unavoidable in the minimal reduced kernel. The controlled RTK target has no such extra finite auxiliary pole.',
  'escape_conditions':[
    'b=0: decoupling',
    'Z=0: algebraic auxiliary, already covered by the rank gate',
    'A/Z outside the exact validity domain or an infinite-mass limit',
    'a larger explicitly degenerate system with an action-derived exact pole-zero cancellation'
  ],
  'zero_H_connection':'If finite b,Z and A~H^2 are used so b^2/A~H^-2, then omega_aux^2=A/Z~H^2 -> 0: the extra mode becomes light at the static boundary.',
  'scope':'minimal single dynamical auxiliary at quadratic level; not a no-go for degenerate/gauge multi-field systems, larger exact cancellations, branch-changing theories, or controlled retarded/nonlocal completions',
  'next_step':'If this gate passes CI, formulate the smallest degenerate two-field constraint matrix whose determinant removes the extra omega pole while keeping the H->0 rank and kinetic residues finite, then perform an explicit DOF count.'
}

print('RTK_ROUTE_B_GRADK_DYNAMIC_AUXILIARY_POLE_GATE_PASS', json.dumps(out, sort_keys=True))
