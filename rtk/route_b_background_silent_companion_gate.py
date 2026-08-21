#!/usr/bin/env python3
"""C8 design gate for a background-silent mixed-derivative companion.

Goal
----
Identify when the natural preferred-foliation operator

    O_Sigma = D_i(nabla_perp Sigma) D^i(nabla_perp Sigma)

produces the desired mixed kinetic term (D_i dot sigma)^2 without simply
reducing to the already-tested direct acceleration/lapse-gradient carrier.

On flat FLRW write

    N = 1+n,
    Sigma = Sigma_bar(t)+sigma,
    q = dot(Sigma_bar),
    nabla_perp Sigma = (q+dot sigma)/(1+n)

at zero background shift.  To linear order

    delta(nabla_perp Sigma) = dot sigma - q n.

Since the background is homogeneous,

    O_Sigma^(2) = p^2 (dot sigma-q n)^2.

Consequences
------------
* q=0 (background-silent companion): O^(2)=p^2 dot sigma^2.  No direct
  p^2 n^2 / a_i a^i term is generated at quadratic order.
* q!=0: O^(2) contains q^2 p^2 n^2 and therefore directly excites the
  lapse-gradient/acceleration sector.
* If Sigma is the same normalized foliation clock, unitary gauge removes
  sigma and the operator is proportional to a_i a^i (up to the clock-speed
  normalization).  Thus it is not a new escape from the direct acceleration
  branch.

This is a design theorem, not a full completion.  The remaining constructive
route is a companion or degenerate scalar combination whose background normal
derivative vanishes, while its perturbation is tied by constraints to the RTK
physical scalar so that no extra propagating scalar remains.
"""

import json
import sympy as sp

eps = sp.symbols('eps')
q,n,d = sp.symbols('q n d', finite=True, real=True)
p2 = sp.symbols('p2', positive=True, finite=True, real=True)

# Exact first-order expansion of the normal derivative at zero background shift.
normal = (q + eps*d)/(1 + eps*n)
series = sp.series(normal, eps, 0, 2).removeO().expand()
delta_normal = sp.simplify(series.coeff(eps,1))
assert sp.simplify(delta_normal - (d-q*n)) == 0

# The quadratic spatial-gradient operator at one Fourier momentum p^2.
O2 = sp.expand(p2*delta_normal**2)
assert sp.simplify(O2 - p2*(d-q*n)**2) == 0

# Background-silent branch: pure mixed kinetic, no lapse-gradient term.
O_silent = sp.expand(O2.subs(q,0))
assert sp.simplify(O_silent - p2*d**2) == 0
assert sp.expand(O_silent).coeff(n,2) == 0
assert sp.expand(O_silent).coeff(n*d) == 0

# Generic rolling background: direct lapse-gradient and cross terms are present.
assert sp.expand(O2).coeff(n,2) == p2*q**2
assert sp.expand(O2).coeff(n*d) == -2*p2*q

# Unitary-gauge clock limit sigma=0 (d=0): exactly a lapse-gradient quadratic
# carrier, proportional to p^2 n^2.
O_clock_unitary = sp.expand(O2.subs(d,0))
assert sp.simplify(O_clock_unitary-p2*q**2*n**2) == 0

out = {
  'classification':'RTK_ROUTE_B_BACKGROUND_SILENT_COMPANION_GATE_PASS',
  'operator':'D_i(nabla_perp Sigma) D^i(nabla_perp Sigma)',
  'linear_identity':'delta(nabla_perp Sigma)=dot sigma-q n, q=dot(Sigma_bar)',
  'quadratic_FLRW':'p^2(dot sigma-q n)^2',
  'background_silent_branch':'q=0 -> p^2 dot sigma^2 with no direct p^2 n^2 term',
  'rolling_branch':'q!=0 -> includes q^2 p^2 n^2 and -2q p^2 n dot sigma',
  'clock_limit':'If Sigma is the rolling foliation clock, unitary gauge reduces the operator to the direct lapse-gradient/acceleration carrier rather than a new class.',
  'design_consequence':'To evade the direct acceleration/PPN branch through this mixed-derivative mechanism, use a background-silent companion or degenerate combination and prove that the full constraint system still has only one physical scalar.',
  'non_claims':[
    'not yet a nonlinear covariant completion',
    'does not yet construct the degeneracy tying the companion to the Khronon/metric scalar',
    'does not establish PPN cancellation beyond the absence of the direct quadratic lapse-gradient term on q=0',
    'radiative stability and EFT cutoff remain open'
  ],
  'next_step':'Construct a fixed two-field/Khronon degenerate action in which the mixed-kinetic combination has q=0 on the production background, then derive the full lapse/shift/Dirac rank and the exact RTK source response.'
}

print('RTK_ROUTE_B_BACKGROUND_SILENT_COMPANION_GATE_PASS',json.dumps(out,sort_keys=True))
