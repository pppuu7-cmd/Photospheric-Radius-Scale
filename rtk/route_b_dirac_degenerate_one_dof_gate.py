#!/usr/bin/env python3
"""C8 constructive Dirac-degenerate one-DOF gate.

For q=(X,y), consider

    L = k/2 (dot X + a dot y)^2 - V(X,y),
    V = 1/2 Omega^2 X^2 + g X y + 1/2 m^2 y^2.

The rank-one velocity Hessian produces a primary constraint. For a positive-
definite potential matrix its preservation produces an independent secondary
constraint, leaving exactly one physical scalar DOF. The source response along
the kinetic direction also contains exactly one finite omega^2 pole.

This is a structural constructive escape from ordinary nondegenerate auxiliary
pole-count obstructions. It is not yet a fixed RTK gravitational action across
momentum and FLRW epochs.
"""

import json
import sympy as sp

k,a,Om2,g,m2,w2 = sp.symbols(
    'k a Om2 g m2 w2', nonzero=True, finite=True, real=True
)
X,y,pX,py = sp.symbols('X y pX py', finite=True, real=True)

v = sp.Matrix([1,a])
Vmat = sp.Matrix([[Om2,g],[g,m2]])
Kvel = k*(v*v.T)
assert Kvel.rank() == 1
assert sp.factor(Kvel.det()) == 0

phi1 = py-a*pX
Vpot = sp.Rational(1,2)*Om2*X**2 + g*X*y + sp.Rational(1,2)*m2*y**2
phi2 = sp.expand(a*sp.diff(Vpot,X)-sp.diff(Vpot,y))
assert sp.simplify(phi2-((a*Om2-g)*X+(a*g-m2)*y)) == 0

def PB(f,h):
    return sp.expand(
        sp.diff(f,X)*sp.diff(h,pX)-sp.diff(f,pX)*sp.diff(h,X)
        + sp.diff(f,y)*sp.diff(h,py)-sp.diff(f,py)*sp.diff(h,y)
    )

bracket = sp.factor(PB(phi1,phi2))
expected = sp.factor(m2+a**2*Om2-2*a*g)
assert sp.simplify(bracket-expected) == 0

w = sp.Matrix([a,-1])
assert sp.simplify((w.T*Vmat*w)[0]-expected) == 0

# Explicit positive-definite parameterization of V proves the bracket is >0.
l11,l21,l22 = sp.symbols('l11 l21 l22', positive=True, finite=True, real=True)
L = sp.Matrix([[l11,0],[l21,l22]])
Vpd = L*L.T
quad_pd = sp.factor((w.T*Vpd*w)[0])
assert sp.simplify(quad_pd-((a*l11-l21)**2+l22**2)) == 0

phase_dim=4
second_class=2
physical_dof=(phase_dim-second_class)//2
assert physical_dof == 1

M = Vmat-k*w2*(v*v.T)
Q = sp.factor((v.T*Vmat.inv()*v)[0])
response = sp.factor((v.T*M.inv()*v)[0])
response_expected = sp.factor(Q/(1-k*Q*w2))
assert sp.simplify(response-response_expected) == 0
assert sp.simplify(M.det()-Vmat.det()*(1-k*Q*w2)) == 0

pole = sp.solve(sp.Eq(1-k*Q*w2,0),w2)
assert pole == [sp.simplify(1/(k*Q))]

# Generic one-pole map: use an independent symbol Q0 instead of trying to
# substitute the composite expression Q=v^T V^{-1}v as an atomic symbol.
R,OmT2,Q0 = sp.symbols('R OmT2 Q0', positive=True, finite=True, real=True)
generic_response = Q0/(1-k*Q0*w2)
mapped = sp.simplify(
    generic_response.subs({k:1/R,Q0:R/OmT2}) - R/(OmT2-w2)
)
assert mapped == 0

out = {
  'classification':'RTK_ROUTE_B_DIRAC_DEGENERATE_ONE_DOF_GATE_PASS',
  'kinetic_structure':{
    'L_kin':'k/2 (dot X + a dot y)^2',
    'velocity_hessian':'k v v^T, v=(1,a)',
    'rank':1,
    'primary_constraint':'phi1=p_y-a p_X=0'
  },
  'secondary_constraint':'phi2=(a Omega^2-g)X+(a g-m^2)y=0',
  'constraint_bracket':'m^2+a^2 Omega^2-2 a g = (a,-1)^T V (a,-1)',
  'positive_potential_result':'For V>0 the bracket is strictly positive, so phi1 and phi2 are a second-class pair.',
  'physical_dof':1,
  'source_response':{
    'Q':'v^T V^{-1}v',
    'response':'Q/(1-k Q omega^2)',
    'pole':'omega_*^2=1/(k Q)',
    'rewritten':'(1/k)/(omega_*^2-omega^2)'
  },
  'constructive_map':'Any positive stable one-pole response R/(Omega_T^2-omega^2) is matched pointwise by k=1/R and Q=R/Omega_T^2.',
  'interpretation':'A rank-one Dirac-degenerate two-field kinetic system can have exactly one physical scalar DOF and one source-channel frequency pole, evading the ordinary positive nondegenerate auxiliary pole-count obstruction at quadratic level.',
  'ci_debug_note':'The first draft generic-map guard attempted to replace the already-expanded composite Q expression as an atomic symbol. The theorem identities themselves passed; the guard now uses an independent Q0 symbol.',
  'non_claims':[
    'not yet a fixed RTK action across momentum and FLRW epochs',
    'source alignment with v must be derived from the action, not imposed by hand',
    'not yet a full gravitational Dirac constraint count including lapse and shift',
    'not a nonlinear/compact-object or radiative-stability theorem',
    'PPN/Newton/GW and EFT cutoff remain untested for this candidate class'
  ],
  'next_step':'Embed the rank-one kinetic block into the FLRW lapse/shift constraint system and solve for fixed invariant-dependent coefficients reproducing the RTK momentum/epoch dependence while keeping full Dirac rank, positive residue and a regular H->0 representation.'
}
print('RTK_ROUTE_B_DIRAC_DEGENERATE_ONE_DOF_GATE_PASS',json.dumps(out,sort_keys=True))
