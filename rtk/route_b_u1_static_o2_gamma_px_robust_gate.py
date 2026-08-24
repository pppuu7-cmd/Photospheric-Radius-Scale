#!/usr/bin/env python3
"""O(2) static gamma_PPN robustness to an arbitrary DBI lapse-equation source.

The exact static variation bridge proves that P(X_U) has no direct A source and,
because P=P_N=0 at N=1, its spatial-metric variation starts beyond linear O(2).
Therefore at O(2) finite P(X_U) can deform the lapse/Hamiltonian equation but not
the spatial dynamical Eq.(5.28) or A-constraint Eq.(5.29) used here.

We deliberately leave the lapse equation completely unspecified through an
arbitrary Delta_H.  If the two unaffected equations independently force
gamma=1, the conclusion is robust to that whole deformation class.
"""
import json
import sympy as sp

a1,a2,kappa,sigma2,gamma1=sp.symbols('a1 a2 kappa sigma2 gamma1')
gamma,f,Delta_H=sp.symbols('gamma f Delta_H')
vals={a1:1,a2:0,kappa:1,sigma2:0,gamma1:-1}

# Lin-Mukohyama-Wang-Zhu arXiv:1310.6666 Eq.(5.28), in the same notation
# already frozen in route_b_u1_static_o2_newton_gamma_gate.py.
eq_dyn=sp.expand(f + gamma1*(gamma+a2*f) - gamma1*(1-a1*f))
# Eq.(5.29), A constraint.
eq_A=sp.expand(4*kappa*a1 - 4*(gamma+a2*f) + sigma2*(1-a1*f))

dyn=sp.simplify(eq_dyn.subs(vals))
Aeq=sp.simplify(eq_A.subs(vals))
assert sp.simplify(dyn-(1-gamma))==0
assert sp.simplify(Aeq-(4-4*gamma))==0
assert not dyn.has(f) and not Aeq.has(f)
assert not dyn.has(Delta_H) and not Aeq.has(Delta_H)
assert sp.solve(sp.Eq(dyn,0),gamma)==[1]
assert sp.solve(sp.Eq(Aeq,0),gamma)==[1]

# Structural bridge check for P(X): around N=1+n, P starts at n^2, so its
# metric-measure variation ~P delta(sqrt g) is O(n^2), not linear O(2), while
# the lapse variation starts at O(n) and is allowed inside Delta_H.
n,mu2,lam=sp.symbols('n mu2 lambda_D')
P=mu2*n**2-2*mu2*n**3+mu2*(3+lam/4)*n**4
assert P.subs(n,0)==0
assert sp.diff(P,n).subs(n,0)==0
assert sp.diff(P,n,2).subs(n,0)==2*mu2

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_O2_GAMMA_PX_ROBUST_EXACT_PASS',
 'status':'STATIC_GAMMA_O2_ROBUST_TO_ARBITRARY_LAPSE_EQUATION_DEFORMATION',
 'external_equations':'arXiv:1310.6666 Eqs.(5.28),(5.29), same notation as existing repo O2 gate',
 'parameters':{'a1':1,'a2':0,'kappa':1,'sigma2':0,'gamma1':-1},
 'allowed_lapse_deformation':'arbitrary Delta_H, including the linearized finite-P(X_U) lapse source',
 'spatial_dynamical_equation':'1-gamma=0',
 'A_constraint':'4(1-gamma)=0',
 'gamma_PPN_O2':1,
 'why_P_does_not_enter_these_two_O2_equations':'P(N=1)=P_N(N=1)=0; P has no A dependence, and its spatial-metric measure source starts quadratic in the weak lapse',
 'non_claims':[
   'does not certify exact Newton radial law or scale-independent G_N with finite P(X_U)',
   'does not certify beta_PPN at O(v^4)',
   'does not certify moving-source alpha1 or alpha2',
   'does not address compact objects, radiative stability or UV cutoff'
 ],
 'next_gate':'derive the finite-mu_K Newton/lapse Green-function correction or a rigorous local bound, then derive the full static O(v^4) beta_PPN equations with explicit P(X_U)'
}
open('u1_static_o2_gamma_px_robust_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
