#!/usr/bin/env python3
"""Exact static bare-lapse uniqueness gate for the frozen U(1)+RTK action.

Scope: time-independent, zero invariant shift, Sigma=q t, D_i Sigma=0,
N>0, interior of the real DBI branch, regular asymptotically-flat boundary.

This script verifies the algebraic part of the uniqueness theorem.  The final
sign/IBP step is encoded explicitly in the result and follows from the frozen
domain inequalities, not from a numerical scan.
"""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_TARGET_V1_FROZEN'

# Require all preceding same-action results.
required={
 'research/theory_results/RTK_ROUTE_B_U1_STATIC_CLOCK_SCALAR_EOM_RESULT_v1.json':'RTK_ROUTE_B_U1_STATIC_CLOCK_SCALAR_EOM_EXACT_PASS',
 'research/theory_results/RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_RESULT_v1.json':'RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_EXACT_PASS',
 'research/theory_results/RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_RESULT_v1.json':'RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_PASS',
}
for path,classification in required.items():
    r=json.load(open(path)); assert r['classification']==classification,(path,r.get('classification'))

# Fixed DBI algebra.
N,lam,mu=sp.symbols('N lam mu', positive=True, finite=True)
r=sp.simplify(1/N-1)
s=sp.sqrt(1-lam*r**2)
p=2*mu**2/lam*(1-s)
F_N=sp.simplify(p+N*sp.diff(p,N))
F_target=sp.simplify(-2*mu**2*r*(1+s+r)/(s*(1+s)))
assert sp.simplify(F_N-F_target)==0

# Smooth lambda_D -> 0 limit.
F_lam0=sp.simplify(sp.limit(F_N,lam,0,dir='+'))
F_lam0_target=sp.simplify(-mu**2*r*(2+r))
assert sp.simplify(F_lam0-F_lam0_target)==0

# The u=sqrt(N) elliptic identity.
u,gu2,lapu=sp.symbols('u gu2 lapu', positive=True, finite=True)
Delta_lnN=2*(lapu/u-gu2/u**2)
grad_lnN_sq=4*gu2/u**2
assert sp.simplify(2*Delta_lnN+grad_lnN_sq-4*lapu/u)==0

# Exact sign bridge. For N=u^2, -r=(u^2-1)/u^2.
r_u=sp.simplify(1/u**2-1)
sign_core=sp.factor((u-1)*(-r_u))
assert sp.simplify(sign_core-(u-1)**2*(u+1)/u**2)==0

# On the frozen domain: u>0, s>0, r>-1. Therefore
# Q=(1+s+r)/(s(1+s))>0 and F_N=(-r)*2 mu^2 Q.
# Hence u(u-1)F_N >=0, with equality only at u=1 (mu>0).

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_EXACT_PASS',
 'status':'EXACT_STATIC_ZERO_SHIFT_UNIQUENESS_ON_REAL_DBI_INTERIOR',
 'target':TARGET,
 'fixed_sector':t['sector'],
 'ordinary_matter_cancellation':{
   'source':'arXiv:1310.6666v4 Eqs.(4.15),(5.5),(5.14)',
   'a2_0_Omega_1':'Jt_m=-2 rho_H; JA_m=2 a1 rho_H',
   'a1_1_gamma1_minus1':'Jt_m-gamma1*JA_m=Jt_m+JA_m=0 exactly',
 },
 'exact_static_equation':'2 D_i a^i + a_i a^i = F_N, with F_N=d[N p_8piG]/dN',
 'dbi':{
   'r':'1/N-1',
   's':'sqrt(1-lambda_D r^2)',
   'p_8piG':'2 mu_K^2/lambda_D (1-s)',
   'F_N_factorized':'-2 mu_K^2 r (1+s+r)/[s(1+s)]',
   'lambda_D_zero_limit':'-mu_K^2 r(2+r)',
   'sign_statement':'for N>0 and s>0, sign(F_N)=sign(N-1)',
 },
 'elliptic_transform':{
   'u':'sqrt(N)',
   'identity':'2 Delta ln N + |grad ln N|^2 = 4 Delta u/u',
   'equation':'4 Delta u = u F_N',
   'sign_core':'(u-1)(-r)=(u-1)^2(u+1)/u^2 >= 0',
 },
 'uniqueness_integral':{
   'after_multiply_by_u_minus_1':'-4 integral |grad u|^2 = integral u(u-1)F_N',
   'lhs':'non-positive',
   'rhs':'non-negative on the frozen domain',
   'conclusion':'both sides vanish; u=1, hence N=1 uniquely under the frozen regular/asymptotically-flat boundary conditions',
 },
 'static_scalar_consequence':{
   'N':'1',
   'a_i':'0',
   'r':'0',
   'P':'0',
   'P_N':'0',
   'interpretation':'the fixed RTK scalar is exactly background-silent in the certified static zero-invariant-shift branch; no forced spatial Sigma profile is needed',
 },
 'non_claims':t['non_claims'],
 'next_gate':'static beta_PPN inheritance on the identical action; moving-source alpha1/alpha2 remain separate',
}
open('u1_static_bare_lapse_nonlinear_uniqueness_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
