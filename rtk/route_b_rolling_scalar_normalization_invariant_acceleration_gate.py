#!/usr/bin/env python3
"""C8 normalization-invariant rolling-scalar acceleration gate.

Question
--------
Can one avoid the direct acceleration/lapse-gradient coefficient by letting the
mixed-derivative field be an independent rolling scalar with a small background
normal velocity q, rather than the foliation clock itself?

Let

    q = nabla_perp S_bar != 0,
    delta S = q pi

at leading Goldstone order.  For

    L_mix = C D_i(nabla_perp S) D^i(nabla_perp S),

one obtains both

    C q^2 (D_i dot pi)^2

and the lapse-gradient term

    C q^2 (D_i n)^2

(up to lower-derivative/background-rate terms).

Exact RTK matching fixes the Goldstone mixed-kinetic coefficient to

    K_pi/(2 M_K^2).

The production DBI identity is

    K_pi = 2 M_Pl^2 M_K^2,

so exact matching requires

    C q^2 = M_Pl^2.

Therefore decreasing q merely increases C; the physical product multiplying
both the desired mixed kinetic and the direct lapse-gradient term is invariant.
A separately normalized rolling scalar does not evade the acceleration-sector
problem by field rescaling alone.
"""

import json
import sympy as sp

C,q,Mpl2,MK2 = sp.symbols('C q Mpl2 MK2', positive=True, finite=True, real=True)
Kpi = 2*Mpl2*MK2
required = sp.simplify(Kpi/(2*MK2))
assert required == Mpl2

# Matching C q^2 to the RTK mixed coefficient fixes the invariant product.
C_solution = sp.solve(sp.Eq(C*q**2,required),C)
assert len(C_solution) == 1
assert sp.simplify(C_solution[0]-Mpl2/q**2) == 0
assert sp.simplify(C_solution[0]*q**2-Mpl2) == 0

# Field rescaling S -> z S implies q -> z q and C -> C/z^2 if the same
# physical quadratic operator is kept.  The product C q^2 is invariant.
z = sp.symbols('z', positive=True, finite=True, real=True)
C_rescaled = C/z**2
q_rescaled = z*q
assert sp.simplify(C_rescaled*q_rescaled**2-C*q**2) == 0

out = {
  'classification':'RTK_ROUTE_B_ROLLING_SCALAR_NORMALIZATION_INVARIANT_ACCELERATION_GATE_PASS',
  'operator':'C D_i(nabla_perp S) D^i(nabla_perp S)',
  'rolling_background':'q=nabla_perp S_bar != 0, delta S=q pi',
  'mixed_kinetic_coefficient':'C q^2',
  'lapse_gradient_coefficient':'C q^2',
  'production_identity':'K_pi=2 M_Pl^2 M_K^2',
  'exact_match':'C q^2=K_pi/(2M_K^2)=M_Pl^2',
  'rescaling_invariance':'S->zS, q->zq, C->C/z^2 leaves Cq^2 invariant',
  'consequence':'An independently normalized rolling scalar cannot suppress the direct acceleration coefficient while still exactly generating the RTK mixed kinetic term. Small q is compensated by large C.',
  'escapes':[
    'background-silent mixed combination q=0 with the RTK kinetic supplied through a broader degenerate architecture',
    'same-action auxiliary/gauge cancellation of the static lapse-gradient response',
    'nonminimal/disformal matter/source frame'
  ],
  'non_claims':[
    'does not exclude U(1) or other gauge-extended cancellations',
    'does not exclude background-silent constrained sectors',
    'does not by itself compute PPN parameters of a broader action'
  ],
  'next_step':'Prioritize explicit constraint/gauge cancellation architectures for the rolling branch, while independently testing whether a nondynamical background carrier can support a background-silent physical mixed mode.'
}

print('RTK_ROUTE_B_ROLLING_SCALAR_NORMALIZATION_INVARIANT_ACCELERATION_GATE_PASS',json.dumps(out,sort_keys=True))
