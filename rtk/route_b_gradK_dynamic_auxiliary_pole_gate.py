#!/usr/bin/env python3
"""C8 pole-count gate for a genuinely dynamical auxiliary field.

The minimal EH+clock grad-K exact carrier requires a reduced coefficient U~H^-2
as H->0. A regular algebraic auxiliary cannot generate this while preserving a
finite nonsingular constraint Hessian. Here the auxiliary y is given its own
kinetic operator.

At fixed spatial momentum,

  L = 1/2 K0 X^2 + b X y + 1/2 [A-Z omega^2] y^2.

Eliminating y gives

  K_eff = K0 - b^2/(A-Z omega^2).

For finite nonzero Z and b this contains an additional frequency-plane pole at
omega_aux^2=A/Z. The controlled RTK target is polynomial/linear in omega^2 at
fixed p^2 and has no such additional finite auxiliary pole.

If finite b,Z are kept while A~H^2 is used to generate b^2/A~H^-2, then
omega_aux^2=A/Z~H^2 -> 0: the additional excitation becomes light at the
static boundary. Thus this minimal dynamical auxiliary does not hide the
regularity problem; it converts it into an extra low-frequency mode.

Scope: minimal single dynamical auxiliary at quadratic level. Explicitly
degenerate/gauge multi-field systems, action-derived pole-zero cancellations,
branch-changing theories and retarded/nonlocal completions remain open.
"""

import json
import sympy as sp

w2, H = sp.symbols('w2 H', finite=True, real=True)
K0, A, Z, b = sp.symbols('K0 A Z b', nonzero=True, finite=True, real=True)

Keff = sp.factor(K0 - b**2/(A-Z*w2))
num, den = sp.fraction(sp.together(Keff))
# SymPy is free to normalize numerator and denominator by a common -1.
ratio = sp.simplify(den/(A-Z*w2))
assert ratio in (sp.Integer(1), sp.Integer(-1))

pole = sp.solve(sp.Eq(den,0), w2)
assert pole == [A/Z]

res = sp.simplify(sp.limit((w2-A/Z)*Keff, w2, A/Z))
assert sp.simplify(res - b**2/Z) == 0

assert sp.simplify(Keff.subs(b,0)-K0) == 0
assert sp.simplify(Keff.subs(Z,0) - (K0-b**2/A)) == 0

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
  'exact_target_gate':'For finite nonzero b and Z, a new finite omega^2 pole is unavoidable in this minimal reduced kernel.',
  'zero_H_connection':'If finite b,Z and A~H^2 are used so b^2/A~H^-2, then omega_aux^2=A/Z~H^2 -> 0: the extra mode becomes light at the static boundary.',
  'ci_debug_note':'The first CI attempt compared the denominator to one fixed overall sign. SymPy returned the algebraically identical -A+Z omega^2. The revised guard accepts only a common overall +/-1; pole and residue formulas are unchanged.',
  'escape_conditions':[
    'b=0: decoupling',
    'Z=0: algebraic auxiliary',
    'A/Z outside the exact validity domain or infinite-mass limit',
    'larger explicitly degenerate system with action-derived exact pole-zero cancellation'
  ],
  'scope':'minimal single dynamical auxiliary at quadratic level; not a no-go for degenerate/gauge multi-field systems, larger exact cancellations, branch changes, or controlled retarded/nonlocal completions',
  'next_step':'Test whether a positive two-auxiliary block can cancel the frequency denominator; if not, move to an explicit Dirac-degenerate constraint action and DOF count.'
}

print('RTK_ROUTE_B_GRADK_DYNAMIC_AUXILIARY_POLE_GATE_PASS', json.dumps(out, sort_keys=True))
