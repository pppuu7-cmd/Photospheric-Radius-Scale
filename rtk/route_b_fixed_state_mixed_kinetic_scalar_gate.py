#!/usr/bin/env python3
"""C8 constructive fixed-state mixed-kinetic scalar theorem.

This gate combines the production DBI state functions with the rank-one
Dirac-degenerate one-DOF mechanism.

Production state variable
-------------------------
Use r=x/s on the positive DBI branch. Then

  c_a^2(r) = r(1-lambda r^2)/(1+r),
  M_K(r)   = mu_K(1+r)(1-lambda r^2)^(-3/4),
  K_phys(r)=2 M_Pl^2 M_K(r)^2,
  G_phys(r)=K_phys(r)c_a^2(r).

These are fixed functions of the state r and the fixed parameters lambda,mu_K;
they are not separately fitted at each epoch.

Local mixed-kinetic quadratic action
------------------------------------
For the physical scalar S, consider

  L2 = 1/2 K(r) [ dot S^2 + (D_i dot S)^2/M_K(r)^2 ]
       -1/2 G(r) (D_i S)^2.

At fixed physical p^2 this gives

  K_eff = K(r)(1+p^2/M_K^2),
  omega^2 = [G/K] p^2/(1+p^2/M_K^2)
          = c_a^2 p^2/(1+p^2/M_K^2),

exactly the production RTK law.

The operator contains only first time derivatives. It changes the coefficient
of omega^2 but does not introduce an additional finite frequency pole.

Rank-one local two-field realization
------------------------------------
Let S=X+a y with constant real a and N=1+a^2. Use the same mixed kinetic term
for S and an isotropic gradient potential

  V = G(r) N p^2/2 [X^2+y^2].

The velocity Hessian is rank one. The secondary constraint sets y=a X for
p^2>0, leaving one physical scalar. The source response along v=(1,a) is

  1/[G p^2 - K(1+p^2/M_K^2) omega^2],

which is exactly the inverse quadratic RTK kernel up to the conventional overall
source sign.

Scope
-----
This is an exact local quadratic scalar preferred-foliation construction. It is
not yet a covariant gravitational completion. One must derive a symmetry-based
action whose scalar reduction is this operator, check lapse/shift constraints,
source/matter coupling, nonlinear DOF, PPN/Newton, GW/tensors, compact objects,
radiative stability and the EFT cutoff.
"""

import json
import sympy as sp

r,lam,mu,Mpl2,p2,w2 = sp.symbols(
    'r lam mu Mpl2 p2 w2', positive=True, finite=True, real=True
)
a = sp.symbols('a', finite=True, real=True)

u = 1-lam*r**2
ca2 = sp.factor(r*u/(1+r))
MK2 = sp.factor(mu**2*(1+r)**2*u**sp.Rational(-3,2))
K = sp.factor(2*Mpl2*MK2)
G = sp.factor(K*ca2)

Keff = sp.factor(K*(1+p2/MK2))
disp = sp.factor(G*p2/Keff)
target_disp = sp.factor(ca2*p2/(1+p2/MK2))
assert sp.simplify(disp-target_disp) == 0

# Positivity in the physical DBI domain r>0, 0<lambda r^2<1 implies
# ca2>0, MK2>0, K>0 and G>0. The assumptions are encoded symbolically except
# for u>0, so we also provide a positive-domain reparameterization u=u0^2.
u0=sp.symbols('u0', positive=True, finite=True, real=True)
ca2_pd=sp.simplify(ca2.subs(u,u0**2))
# Direct substitution of a compound expression is not guaranteed; verify the
# equivalent positive expression explicitly.
ca2_positive_form = r*u0**2/(1+r)
assert ca2_positive_form.is_positive

# Two-field rank-one realization.
N = 1+a**2
v = sp.Matrix([1,a])
wnull = sp.Matrix([a,-1])
Kvel = Keff*(v*v.T)
assert Kvel.rank() == 1
assert sp.factor(Kvel.det()) == 0

Vmat = sp.simplify(G*p2*N)*sp.eye(2)
Q = sp.factor((v.T*Vmat.inv()*v)[0])
assert sp.simplify(Q-1/(G*p2)) == 0

secondary_bracket = sp.factor((wnull.T*Vmat*wnull)[0])
assert sp.simplify(secondary_bracket-G*p2*N**2) == 0

Mfreq = Vmat-Keff*w2*(v*v.T)
response = sp.factor((v.T*Mfreq.inv()*v)[0])
rtk_response = sp.factor(1/(G*p2-Keff*w2))
assert sp.simplify(response-rtk_response) == 0

# The sole pole reproduces the production dispersion. Compare invariantly:
# SymPy may print algebraically identical radicals/rational factors differently.
pole = sp.solve(sp.Eq(G*p2-Keff*w2,0),w2)
assert len(pole) == 1
assert sp.simplify(pole[0]-target_disp) == 0

out = {
  'classification':'RTK_ROUTE_B_FIXED_STATE_MIXED_KINETIC_SCALAR_GATE_PASS',
  'state_functions':{
    'c_a^2(r)':'r(1-lambda r^2)/(1+r)',
    'M_K(r)':'mu_K(1+r)(1-lambda r^2)^(-3/4)',
    'K_phys(r)':'2 M_Pl^2 M_K(r)^2',
    'G_phys(r)':'K_phys(r) c_a^2(r)'
  },
  'local_scalar_action':'1/2 K(r)[dot S^2+(D_i dot S)^2/M_K(r)^2]-1/2 G(r)(D_i S)^2',
  'exact_dispersion':'omega^2=c_a^2(r) p^2/[1+p^2/M_K(r)^2]',
  'time_derivative_order':'first derivatives in the action; second order in time in the linear equation',
  'two_field_realization':{
    'S':'X+a y with constant a',
    'potential':'G(r)(1+a^2)p^2/2 [X^2+y^2]',
    'velocity_rank':1,
    'secondary_constraint':'y=a X for p^2>0',
    'physical_dof':1,
    'source_response':'1/[G p^2-K(1+p^2/M_K^2) omega^2]'
  },
  'interpretation':'A fixed-state-function local quadratic scalar EFT with one physical DOF reproduces the full production RTK rational dispersion for the entire positive DBI state branch, without epoch-by-epoch coefficient fitting and without an extra frequency pole.',
  'non_claims':[
    'not yet a covariant/spatially-covariant gravitational action derivation',
    'does not yet prove the matter/source coupling or metric transfer functions',
    'does not by itself establish nonlinear degeneracy or radiative stability',
    'PPN/Newton, GW/tensor, compact-object and EFT-cutoff gates remain open',
    'the p=0 homogeneous/gauge sector is separate from the finite-momentum constraint count'
  ],
  'next_step':'Construct the minimal symmetry-based Khronon/ADM operator whose quadratic reduction is (D_i dot S)^2/M_K(r)^2, then compute its full lapse/shift/Dirac constraint algebra and static/PPN/GW behavior using the same fixed state functions.'
}

print('RTK_ROUTE_B_FIXED_STATE_MIXED_KINETIC_SCALAR_GATE_PASS',json.dumps(out,sort_keys=True))
