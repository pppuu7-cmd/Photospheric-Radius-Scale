#!/usr/bin/env python3
"""Extend the same-action O(2) static Newton/gamma result to arbitrary regular lambda.

Inputs already established in separate gates:
- corrected full action beta0_bare=0 plus explicit rolling S_mix;
- in the static pure-lapse quadratic action S_mix is exactly equivalent to
  beta0_eff=2, while the mismatch starts at cubic action order;
- a1=1,a2=0,kappa=1,sigma1=sigma2=0,gamma1=-1.

Static O(2) has K_ij=0, hence K=0 and the Hořava kinetic combination
K_ij K^ij-lambda K^2 vanishes identically for every lambda.  The Lin et al.
O(2) static equations used previously therefore contain no lambda.  Re-solving
them yields f=1, gamma_PPN=1 and G_N=G for arbitrary regular lambda, including
the newly identified lambda>1 rank-safe branch.

This is NOT a full PPN pass: beta_PPN and preferred-frame alpha1/alpha2 require
cubic/static and time-dependent O(3/O4) rederivations with explicit S_mix.
"""
import json
import sympy as sp

lam=sp.symbols('lambda_HL', real=True, finite=True)
# Static extrinsic-curvature support: algebraic placeholders vanish.
K2,Ksq=sp.symbols('KijKij Ksq', real=True, finite=True)
LK=K2-lam*Ksq
assert sp.simplify(LK.subs({K2:0,Ksq:0}))==0
assert sp.diff(LK.subs({K2:0,Ksq:0}),lam)==0

# Lin et al. O(2) algebra, with beta_eff=2 only in the proven quadratic lapse bridge.
a1,a2,kappa,sigma2,gamma1,beta_eff=sp.symbols('a1 a2 kappa sigma2 gamma1 beta_eff', real=True, finite=True)
gamma,f=sp.symbols('gamma f', real=True, finite=True)
vals={a1:1,a2:0,kappa:1,sigma2:0,gamma1:-1,beta_eff:2}
den=2*beta_eff*a1-4*gamma1*a2-sigma2
num=2*beta_eff+4*gamma1*gamma+4*kappa
f_expr=sp.factor(num/den)
f_branch=sp.simplify(f_expr.subs(vals))
assert sp.simplify(f_branch-(2-gamma))==0

eq_dyn=sp.expand(f + gamma1*(gamma+a2*f) - gamma1*(1-a1*f))
eq_A=sp.expand(4*kappa*a1-4*(gamma+a2*f)+sigma2*(1-a1*f))
eq_dyn_b=sp.simplify(eq_dyn.subs(vals).subs(f,f_branch))
eq_A_b=sp.simplify(eq_A.subs(vals).subs(f,f_branch))
assert sp.simplify(eq_dyn_b-(1-gamma))==0
assert sp.simplify(eq_A_b-(4-4*gamma))==0
assert sp.solve(sp.Eq(eq_dyn_b,0),gamma)==[1]
assert sp.solve(sp.Eq(eq_A_b,0),gamma)==[1]
gamma_sol=sp.Integer(1)
f_sol=sp.simplify(f_branch.subs(gamma,gamma_sol))
assert f_sol==1
# No lambda entered any O2 equation.
for expr in (f_expr,eq_dyn,eq_A):
    assert sp.diff(expr,lam)==0

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_O2_NEWTON_GAMMA_LAMBDA_BRANCH_PASS',
  'status_scope':'GREEN_SAME_ACTION_STATIC_O2_NEWTON_GAMMA_FOR_LAMBDA_BRANCH_FULL_PPN_PENDING',
  'domain':'static weak field O(2), corrected beta0_bare=0 action with explicit S_mix quadratic bridge, a1=kappa=1,a2=0,sigma1=sigma2=0,gamma1=-1; arbitrary regular lambda_HL including lambda_HL>1',
  'static_lambda_decoupling':'K_ij=0 => K=0 => K_ij K^ij-lambda_HL K^2=0 identically, so lambda_HL does not enter the O(2) static equations.',
  'solutions':['f=1','A_2=U','gamma_PPN=1','kappa=G/G_N=1 -> G_N=G in this O(2) normalization'],
  'lambda_result':'The O(2) Newton/gamma result extends unchanged from the old lambda_HL=1 representative to the entire lambda_HL>1 rank-safe branch.',
  'same_action_scope':'S_mix is retained explicitly; beta0_eff=2 is used only as the separately proved quadratic pure-lapse bridge, not as a replacement for S_mix beyond O(2).',
  'non_claims':[
    'does not certify beta_PPN because S_mix differs from beta0_eff=2 at cubic weak-field action order',
    'does not certify alpha1 or alpha2 because time-dependent/vector O(3) equations remain to be rederived',
    'does not prove strong-field, compact-object, radiative or cutoff viability',
    'does not freeze lambda_HL or choose its observational value'
  ],
  'next_gate':'derive the explicit S_mix cubic static mismatch contribution to the O(4) field equations and solve beta_PPN on the lambda_HL>1 branch; separately rederive O(3) vector equations for alpha1/alpha2.'
}
open('u1_static_o2_newton_gamma_lambda_branch_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
