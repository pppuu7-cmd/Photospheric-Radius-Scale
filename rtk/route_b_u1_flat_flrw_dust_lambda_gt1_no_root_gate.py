#!/usr/bin/env python3
"""Exact all-q no-rank-loss domain on the positive-source dust FLRW branch.

Controlled scope: d=3 flat homogeneous isotropic canonical background,
pressureless ordinary matter (tau_rho=0), eta0>0, M_c^2>0, q>0,
beta0_bare=0, Zhu UV sign convention.

For the exact projected J metric derivative write
  A0=M_Pl^2 eta0/2 >0,
  m(q)=M_c^2 rho/(M_c^2+q)^2 >=0,
  X=A nn+B g,
  A=A0+m,
  tr X=-2 A0+m   (dust tau_rho=0).
For lambda>1/3,
  X G X=(2/3)A^2-(tr X)^2/[3(3 lambda-1)].
For lambda>1 its positivity is exact for all m>=0 because
 (3 lambda-1)*3 XGX
 =6(lambda-1)A0^2+12 lambda A0 m+3(2 lambda-1)m^2 >0.
Thus d(q)>0.  If beta24<=0 and beta8<0 in Zhu convention, a(q)>0,
so det B=F^2+a d>0 for every q>0 independently of F zeros and M_c.
"""
import json
import sympy as sp

A0,m,lam=sp.symbols('A0 m lambda', positive=True, finite=True)
A=A0+m
T=-2*A0+m
XGX=sp.factor(sp.Rational(2,3)*A**2-T**2/(3*(3*lam-1)))
poly=sp.factor(3*(3*lam-1)*XGX)
expected=sp.expand(6*(lam-1)*A0**2+12*lam*A0*m+3*(2*lam-1)*m**2)
assert sp.simplify(poly-expected)==0

q,Mpl,u,v=sp.symbols('q M_Pl u v', positive=True, finite=True)
aentry=sp.factor(2*u*q**2+4*v*q**3/Mpl**2) # u=-beta24>0, v=-beta8>0
assert sp.simplify(aentry-2*q**2*(u+2*v*q/Mpl**2))==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_DUST_LAMBDA_GT1_NO_ROOT_PASS',
  'status_scope':'GREEN_EXACT_ALL_Q_DUST_FLRW_RANK_SAFE_DOMAIN_GENERIC_MATTER_AND_PPN_PENDING',
  'domain':'d=3 flat homogeneous isotropic dust ordinary-matter background, eta0>0, rho>=0, M_c^2>0, q>0, lambda>1, beta0_bare=0, Zhu beta8 convention',
  'dust_metric_response':'tau_rho=0; A=A0+m, trX=-2A0+m, A0=M_Pl^2 eta0/2, m=M_c^2 rho/(M_c^2+q)^2>=0',
  'deWitt_positive_polynomial':'3(3 lambda-1) XGX = 6(lambda-1)A0^2 + 12 lambda A0 m + 3(2 lambda-1)m^2 >0 for lambda>1',
  'd_conclusion':'d(q)>0 for every finite q>0, every rho>=0 and every M_c^2>0 in the stated dust scope.',
  'uv_sign_domain':['beta24=beta2+beta4<=0','beta8<0 in Zhu convention'],
  'a_conclusion':'a(q)=-2 beta24 q^2-4 beta8 q^3/M_Pl^2>0 for every q>0.',
  'determinant_conclusion':'det B(q)=F(q)^2+a(q)d(q)>0 for every q>0; no M_c tuning and no numerical q-root scan are required inside this theorem.',
  'cosmology_compatibility':'Unlike the earlier simple lambda<1/3 positivity branch, lambda>1 is compatible with the positive-source sign required by the flat-FLRW lapse constraint.',
  'interpretation':'This is a nonempty all-positive-q classical rank-safe domain on a positive-source dust FLRW branch of the corrected same-action candidate.',
  'non_claims':[
    'does not yet include radiation, massive-neutrino pressure, anisotropic stress or generic canonical matter Poisson response',
    'does not freeze lambda, beta24, beta8 or M_c',
    'does not constitute a same-action PPN or GW observational pass',
    'does not extend to curved/inhomogeneous or nonlinear backgrounds'
  ],
  'next_gate':'extend the XGX positivity inequality to a barotropic p=w rho source and derive an explicit pressure/density/M_c bound for radiation and massive-neutrino eras; then intersect with tensor and same-action PPN conditions.'
}
open('u1_flat_flrw_dust_lambda_gt1_no_root_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
