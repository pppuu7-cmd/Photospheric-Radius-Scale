#!/usr/bin/env python3
"""C8 bridge: rank-one Dirac kinetic pair plus algebraic lapse/shift block.

Let q=(X,y) carry a rank-one kinetic matrix k v v^T, and let z=(n,s) be two
nondynamical variables (standing for a generic lapse/shift scalar block) with no
velocities. Write the potential quadratic form as

  Vtot = 1/2 q^T V q + q^T C z + 1/2 z^T A z.

If A is invertible, z=-A^{-1} C^T q and

  Veff = V - C A^{-1} C^T.

Because z has no velocities, this Schur elimination does not change the
rank-one velocity Hessian. The primary constraint of the degenerate kinetic
pair therefore survives. Its secondary-constraint bracket is obtained by
replacing V by Veff. If Veff is positive definite, the primary/secondary pair
remains second class and the physical scalar count remains one.

The source response along the kinetic direction v is then exactly

  Qeff/(1-k Qeff omega^2),  Qeff=v^T Veff^{-1}v,

so an invertible algebraic lapse/shift Schur block is structurally compatible
with the one-DOF/one-pole Dirac mechanism.

This theorem does not identify the actual RTK A,C,V matrices; deriving them from
one fixed gravitational action is the next gate. It also excludes H=0 points
where the chosen algebraic block A itself loses rank; those require a separate
full-constraint analysis.
"""

import json
import sympy as sp

# q-sector potential, algebraic z-sector, and mixing.
v11,v12,v22 = sp.symbols('v11 v12 v22', finite=True, real=True)
a11,a12,a22 = sp.symbols('a11 a12 a22', finite=True, real=True)
c11,c12,c21,c22 = sp.symbols('c11 c12 c21 c22', finite=True, real=True)
X,y,n,s = sp.symbols('X y n s', finite=True, real=True)
k,alpha,w2 = sp.symbols('k alpha w2', nonzero=True, finite=True, real=True)

V = sp.Matrix([[v11,v12],[v12,v22]])
Az = sp.Matrix([[a11,a12],[a12,a22]])
C = sp.Matrix([[c11,c12],[c21,c22]])
q = sp.Matrix([X,y])
z = sp.Matrix([n,s])

assert sp.factor(Az.det()) == a11*a22-a12**2
Az_inv = Az.inv()
Veff = sp.simplify(V-C*Az_inv*C.T)

Vtot = sp.Rational(1,2)*(q.T*V*q)[0] + (q.T*C*z)[0] + sp.Rational(1,2)*(z.T*Az*z)[0]
zsol = -Az_inv*C.T*q
Vreduced = sp.expand(Vtot.subs({n:zsol[0],s:zsol[1]}))
Veff_form = sp.expand(sp.Rational(1,2)*(q.T*Veff*q)[0])
assert sp.simplify(Vreduced-Veff_form) == 0

# Rank-one kinetic direction v=(1,alpha) is untouched by algebraic elimination.
v = sp.Matrix([1,alpha])
Kvel = k*(v*v.T)
assert Kvel.rank() == 1
assert sp.factor(Kvel.det()) == 0

# Primary constraint null direction w=(alpha,-1).  The secondary bracket is the
# projected effective potential.  We verify the exact expression.
w = sp.Matrix([alpha,-1])
secondary_bracket = sp.factor((w.T*Veff*w)[0])

# Frequency matrix and exact one-pole response.
M = Veff-k*w2*(v*v.T)
Qeff = sp.factor((v.T*Veff.inv()*v)[0])
response = sp.factor((v.T*M.inv()*v)[0])
assert sp.simplify(response-Qeff/(1-k*Qeff*w2)) == 0
assert sp.simplify(M.det()-Veff.det()*(1-k*Qeff*w2)) == 0

# Constructive PD example after Schur reduction: choose Veff=lambda I.  This is
# sufficient to verify that the bridge has a nonempty healthy algebraic region.
lam = sp.symbols('lam', positive=True, finite=True, real=True)
Veff_pd = lam*sp.eye(2)
bracket_pd = sp.simplify((w.T*Veff_pd*w)[0])
Q_pd = sp.simplify((v.T*Veff_pd.inv()*v)[0])
assert bracket_pd == lam*(alpha**2+1)
assert Q_pd == (alpha**2+1)/lam

out = {
  'classification':'RTK_ROUTE_B_DIRAC_LAPSE_SHIFT_SCHUR_BRIDGE_PASS',
  'schur_map':'V_eff=V-C A_z^{-1} C^T',
  'kinetic_rank':'rank(k v v^T)=1 is unchanged because the z=(lapse,shift) block has no velocities',
  'primary_constraint':'same rank-one kinetic primary constraint as before',
  'secondary_bracket':'w^T V_eff w, w=(alpha,-1)',
  'healthy_condition':'If V_eff>0 then the secondary bracket is positive and the primary/secondary pair remains second class, leaving one scalar DOF.',
  'source_response':'Q_eff/(1-k Q_eff omega^2), Q_eff=v^T V_eff^{-1}v',
  'constructive_nonempty_region':'V_eff=lambda I with lambda>0 gives bracket=lambda(1+alpha^2)>0 and Q_eff=(1+alpha^2)/lambda>0.',
  'interpretation':'An invertible nondynamical lapse/shift Schur block does not by itself spoil the one-DOF/one-pole Dirac escape. The remaining hard problem is the action-derived RTK coefficient map and the behavior where the lapse/shift block changes rank.',
  'non_claims':[
    'not yet the explicit RTK lapse/shift matrix',
    'does not cover points where A_z is singular, including a possible static-boundary rank change',
    'not a full gravitational Hamiltonian analysis',
    'not a PPN/GW/cutoff or nonlinear theorem'
  ],
  'next_step':'Derive A_z,C,V,k,alpha from one explicit spatially-covariant/degenerate Khronon action and solve the multi-epoch RTK pole+residue matching conditions without fitting coefficients independently by epoch.'
}

print('RTK_ROUTE_B_DIRAC_LAPSE_SHIFT_SCHUR_BRIDGE_PASS',json.dumps(out,sort_keys=True))
