#!/usr/bin/env python3
"""C8 constructive Dirac-degenerate one-DOF gate.

Motivation
----------
Regular algebraic auxiliaries cannot hide the H^-2 coefficient of the minimal
grad-K representation without losing constraint rank. Ordinary dynamical
auxiliaries introduce extra frequency poles, and a positive two-auxiliary
kinetic block cannot cancel all of them. The remaining local possibility is a
genuinely degenerate kinetic system whose primary/secondary constraints remove
the would-be extra degree of freedom.

Toy quadratic action
--------------------
For q=(X,y), take

    L = k/2 (dot X + a dot y)^2 - V(X,y),

    V = 1/2 Omega^2 X^2 + g X y + 1/2 m^2 y^2,

with k>0 and a real. The velocity Hessian is

    K_vel = k v v^T,   v=(1,a),

which has rank one. Momenta obey

    p_X = k(dot X + a dot y),
    p_y = a p_X,

so there is a primary constraint

    phi1 = p_y - a p_X = 0.

The canonical Hamiltonian is

    H_c = p_X^2/(2k) + V.

Preserving phi1 gives the secondary constraint

    phi2 = a V_X - V_y
         = (a Omega^2-g) X + (a g-m^2) y.

Their Poisson bracket is

    {phi1,phi2} = m^2 + a^2 Omega^2 - 2 a g.

For a positive-definite potential matrix

    Vmat=[[Omega^2,g],[g,m^2]],

the bracket equals w^T Vmat w with w=(a,-1), hence is strictly positive.
Thus phi1 and phi2 form one second-class pair. Starting with four-dimensional
phase space, two second-class constraints leave

    (4-2)/2 = 1

physical configuration-space degree of freedom.

Exact frequency/source response
-------------------------------
At fixed spatial momentum the Fourier quadratic matrix is

    M(omega^2)=Vmat-k omega^2 v v^T.

Let a physical source couple along the same kinetic direction v. Define

    Q = v^T Vmat^{-1} v > 0.

Sherman-Morrison/determinant lemma gives exactly

    v^T M^{-1} v = Q/(1-k Q omega^2),

    det M = det(Vmat) (1-k Q omega^2).

Therefore the degenerate two-field system has exactly one finite frequency pole
in this source channel, not the two poles of a nondegenerate two-field kinetic
matrix. Its pole is

    omega_*^2 = 1/(k Q) > 0.

The response may be rewritten as

    (1/k)/(omega_*^2-omega^2).

Hence any positive stable one-pole target response R/(Omega_T^2-omega^2) can be
matched pointwise by k=1/R and Q=R/Omega_T^2. This is a structural constructive
escape, not yet an RTK completion: the required k,Q and source direction must
be derived from one local fixed action across all p and FLRW epochs, and the
full gravity constraints/PPN/GW/cutoff must still pass.
"""

import json
import sympy as sp

k,a,Om2,g,m2,w2 = sp.symbols(
    'k a Om2 g m2 w2', nonzero=True, finite=True, real=True
)
X,y,pX,py = sp.symbols('X y pX py', finite=True, real=True)

v = sp.Matrix([1,a])
Vmat = sp.Matrix([[Om2,g],[g,m2]])
Kvel = sp.factor(k) * (v*v.T)
assert Kvel.rank() == 1
assert sp.factor(Kvel.det()) == 0

# Primary and secondary constraints.
phi1 = py-a*pX
Vpot = sp.Rational(1,2)*Om2*X**2 + g*X*y + sp.Rational(1,2)*m2*y**2
Vx = sp.diff(Vpot,X)
Vy = sp.diff(Vpot,y)
phi2 = sp.expand(a*Vx - Vy)
assert sp.simplify(phi2 - ((a*Om2-g)*X + (a*g-m2)*y)) == 0

# Poisson bracket for canonical pairs (X,pX),(y,py).
def PB(f,h):
    return sp.expand(
        sp.diff(f,X)*sp.diff(h,pX)-sp.diff(f,pX)*sp.diff(h,X)
        + sp.diff(f,y)*sp.diff(h,py)-sp.diff(f,py)*sp.diff(h,y)
    )

bracket = sp.factor(PB(phi1,phi2))
expected_bracket = sp.factor(m2+a**2*Om2-2*a*g)
assert sp.simplify(bracket-expected_bracket) == 0

w = sp.Matrix([a,-1])
assert sp.simplify((w.T*Vmat*w)[0]-expected_bracket) == 0

# Constructive Cholesky parameterization proves strict positivity of the
# constraint bracket for positive-definite Vmat.
l11,l21,l22 = sp.symbols('l11 l21 l22', positive=True, finite=True, real=True)
L = sp.Matrix([[l11,0],[l21,l22]])
Vpd = L*L.T
quad_pd = sp.factor((w.T*Vpd*w)[0])
assert sp.simplify(quad_pd - ((a*l11-l21)**2+l22**2)) == 0

# 2 coordinates -> phase dimension 4; two second-class constraints -> 1 DOF.
phase_dim = 4
second_class = 2
physical_dof = (phase_dim-second_class)//2
assert physical_dof == 1

# Exact source response along v.
M = Vmat-k*w2*(v*v.T)
Q = sp.factor((v.T*Vmat.inv()*v)[0])
response = sp.factor((v.T*M.inv()*v)[0])
target_response = sp.factor(Q/(1-k*Q*w2))
assert sp.simplify(response-target_response) == 0

det_identity = sp.factor(M.det() - Vmat.det()*(1-k*Q*w2))
assert sp.simplify(det_identity) == 0

pole = sp.solve(sp.Eq(1-k*Q*w2,0),w2)
assert pole == [sp.simplify(1/(k*Q))]

# Exact pointwise map to a generic positive one-pole response.
R,OmT2 = sp.symbols('R OmT2', positive=True, finite=True, real=True)
k_map = 1/R
Q_map = R/OmT2
mapped = sp.simplify(target_response.subs({k:k_map,Q:Q_map}) - R/(OmT2-w2))
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
  'positive_potential_result':'For V>0 the bracket is strictly positive, so phi1,phi2 are a second-class pair.',
  'physical_dof':1,
  'source_response':{
    'Q':'v^T V^{-1}v',
    'response':'Q/(1-k Q omega^2)',
    'pole':'omega_*^2=1/(k Q)',
    'rewritten':'(1/k)/(omega_*^2-omega^2)'
  },
  'constructive_map':'Any positive stable one-pole response R/(Omega_T^2-omega^2) is matched pointwise by k=1/R and Q=R/Omega_T^2.',
  'interpretation':'A genuinely rank-one Dirac-degenerate two-field kinetic system can contain only one physical scalar DOF and one source-channel frequency pole. This evades the ordinary positive two-dynamical-auxiliary pole-count obstruction at quadratic level.',
  'non_claims':[
    'not yet a fixed RTK action across momentum and FLRW epochs',
    'source alignment with v must be derived from the action, not imposed by hand',
    'not yet a full gravitational Dirac constraint count including lapse and shift',
    'not a nonlinear/compact-object or radiative-stability theorem',
    'PPN/Newton/GW and EFT cutoff remain untested for this candidate class'
  ],
  'next_step':'Embed this rank-one kinetic block into the FLRW lapse/shift constraint system and solve for fixed invariant-dependent coefficients that reproduce the RTK p- and epoch-dependence while keeping the full Dirac rank, positive residue and a regular H->0 representation.'
}

print('RTK_ROUTE_B_DIRAC_DEGENERATE_ONE_DOF_GATE_PASS',json.dumps(out,sort_keys=True))
