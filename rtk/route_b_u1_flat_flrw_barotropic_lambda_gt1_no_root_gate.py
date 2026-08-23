#!/usr/bin/env python3
"""All-q rank-safe domain for lambda>1 with nonnegative-pressure barotropic ordinary matter.

Scope: d=3 flat homogeneous isotropic canonical background, ordinary source with
p=w rho, 0<=w<=4/3, eta0>0, rho>=0, M_c^2>0, beta0_bare=0, Zhu UV convention.
The neutral RTK scalar is not part of the elliptic H0 source.

Set
 A0=M_Pl^2 eta0/2,
 r=M_c^2/(M_c^2+q) in (0,1],
 z=rho/(A0 M_c^2)=2 rho/(eta0 M_Pl^2 M_c^2),
 c=3w/2.
Then the exact metric-response tensor entering d(q) obeys
 A/A0=1+z r^2,
 T/A0=trX/A0=-2+z r^2+c z r.
For c>=0, T>=-2A. Also T<=2A follows if z r(c-r)<=4.
For 0<=c<=2, max_{0<=r<=1} r(c-r)=c^2/4, so z<=16/c^2
(or vacuously w=0) implies |T|<=2A for every q.
For lambda>1, 3 lambda-1>2, hence
 XGX=(2/3)A^2-T^2/[3(3lambda-1)]>0.
With beta24<=0,beta8<0, a(q)>0 and det B=F^2+a d>0 for all q>0.
"""
import json
import sympy as sp

r,z,c=sp.symbols('r z c', nonnegative=True, finite=True)
A=1+z*r**2
T=-2+z*r**2+c*z*r
lower=sp.factor(T+2*A)
upper=sp.factor(2*A-T)
assert sp.simplify(lower-z*r*(3*r+c))==0
assert sp.simplify(upper-(4-z*r*(c-r)))==0
quad=sp.expand(r*(c-r))
complete=sp.expand(c**2/sp.Integer(4)-(r-c/sp.Integer(2))**2)
assert sp.simplify(quad-complete)==0

w,eta,Mpl,M2,rho=sp.symbols('w eta0 M_Pl M_c_squared rho', positive=True, finite=True)
zdef=sp.factor(2*rho/(eta*Mpl**2*M2))
bound_M2=sp.factor(sp.Rational(9,32)*w**2*rho/(eta*Mpl**2))
# Exact factorization proving z<=64/(9w^2) iff M2>=bound_M2 for positive variables.
margin_z=sp.factor(sp.Rational(64,9)/w**2-zdef)
margin_M=sp.factor(32*eta*Mpl**2*M2-9*w**2*rho)
pref=sp.factor(sp.Rational(2,9)/(w**2*eta*Mpl**2*M2))
assert sp.simplify(margin_z-pref*margin_M)==0
assert sp.simplify(bound_M2-sp.Rational(9,32)*w**2*rho/(eta*Mpl**2))==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_BAROTROPIC_LAMBDA_GT1_NO_ROOT_PASS',
  'status_scope':'GREEN_EXACT_ALL_Q_BAROTROPIC_FLRW_SUFFICIENT_DOMAIN_TIME_HISTORY_BOUND_PENDING',
  'domain':'d=3 flat homogeneous isotropic ordinary barotropic source, eta0>0, rho>=0, 0<=w<=4/3, lambda>1, q>0, beta0_bare=0, Zhu beta8 convention',
  'dimensionless_variables':['r=M_c^2/(M_c^2+q) in (0,1]','z=2 rho/(eta0 M_Pl^2 M_c^2)','c=3w/2'],
  'exact_response':['A/A0=1+z r^2','trX/A0=-2+z r^2+c z r'],
  'absolute_trace_bound':'For w=0, |trX|<=2A automatically. For w>0 with 0<w<=4/3, z<=64/(9w^2) implies |trX|<=2A for every q>0.',
  'Mc_bound':'M_c^2 >= (9 w^2/32) rho/(eta0 M_Pl^2)',
  'radiation_specialization':'w=1/3 -> M_c^2 >= rho/(32 eta0 M_Pl^2)',
  'standard_multifluid_note':'For an isotropic sum of ordinary nonnegative-pressure species, use instantaneous rho=sum rho_s, p=sum p_s and w_eff=p/rho. If 0<=w_eff<=1/3, the radiation specialization is a conservative sufficient bound at that epoch.',
  'deWitt_conclusion':'lambda>1 and |trX|<=2A imply XGX>0, hence d(q)>0 for every q>0.',
  'uv_sign_domain':['beta24=beta2+beta4<=0','beta8<0 in Zhu convention'],
  'determinant_conclusion':'With the Mc/source bound and UV sign domain, det B(q)=F(q)^2+a(q)d(q)>0 for every q>0.',
  'interpretation':'The positive-source lambda>1 all-q rank-safe theorem extends beyond dust to radiation and standard isotropic ordinary multifluids, with an explicit source-density lower bound on M_c rather than a q scan or tuned point.',
  'non_claims':[
    'does not prove the M_c bound over all cosmic times; rho and w are epoch-dependent',
    'does not include negative-pressure ordinary components, anisotropic stress, or generic matter Poisson response beyond the barotropic commuting sector',
    'does not freeze M_c, lambda, beta24 or beta8',
    'does not close same-action PPN, GW observational dispersion, technical naturalness or strong-field gates'
  ],
  'next_gate':'combine the epochwise radiation bound with the same-action Friedmann equation and a declared EFT starting epoch to obtain a history-wide sufficient M_c floor; separately handle massive-neutrino anisotropic stress.'
}
open('u1_flat_flrw_barotropic_lambda_gt1_no_root_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
