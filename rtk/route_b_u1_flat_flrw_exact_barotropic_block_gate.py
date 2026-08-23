#!/usr/bin/env python3
"""Exact flat-FLRW reduced U(1) cross-block for barotropic ordinary matter.

Scope and external inputs:
- special eta1=eta2=0 U(1) branch of Mukohyama et al. (arXiv:1504.07357),
  Eqs. (55)-(58). On flat homogeneous isotropic pi^ij=P g^ij, Eqs. (56),(57)
  give exactly b_g=-b2 q, c_g=+b2 q; the paper states only Eq. (55) depends
  on L_V, so no UV-potential terms enter b,c,d.
- corrected current full action has beta0_bare=0 and neutral RTK direct
  canonical lapse Hessian zero on the homogeneous phase-space background.
- Zhu et al. (arXiv:1108.1237) soft-detailed-balance flat pure-lapse operator
  is parameterized by beta24=beta2+beta4 and beta8.
- projected ordinary matter has exact filtered c_m and b_m=-c_m on the stated
  flat homogeneous support.
- homogeneous barotropic/commuting stress response {H0,tau_H}_m=0, so d is
  exhausted by the kinetic DeWitt square.

Then, in d=3 and background lapse N=1,
  B(q)=[[a(q),-F(q)],[F(q),d(q)]]
with every displayed q dependence exact within this background/operator scope.
"""
import json
import sympy as sp

q,M2,Mpl,eta,P,lam,sqrtg=sp.symbols('q M_c_squared M_Pl eta0 P lambda sqrtg', positive=True, finite=True)
rho,tau,b24=sp.symbols('rho tau_rho beta24', real=True, finite=True)
b8=sp.symbols('beta8', real=True, finite=True)
d=sp.Integer(3)
# Exact pure-gravity off-diagonal coefficient from Eqs.56-57.
b2=sp.factor(2*eta*P*(d-1)/(d*lam-1))
# Isotropic gravity canonical velocity and exact filtered c_m.
V=sp.factor(-4*P/(Mpl**2*sqrtg*(d*lam-1)))
H0=sqrtg*rho; tauH=sqrtg*tau
cm=sp.factor(V*(M2*q*H0/(M2+q)**2-q*tauH/(M2+q)))
F=sp.factor(b2*q+cm)
# Exact pure-lapse a(q) on beta0_bare=0 with zeta^2=Mpl^2/2.
aentry=sp.factor(-2*b24*q**2-4*b8*q**3/Mpl**2)
# Exact metric derivative of total J divided by q sqrt(g): X=A nn+B g.
A0=sp.factor(Mpl**2*eta/2)
Ann=sp.factor(A0+M2*rho/(M2+q)**2)
Bg=sp.factor(-A0-tau/(d*(M2+q)))
X2=sp.expand(Ann**2+2*Ann*Bg+d*Bg**2)
trX=sp.expand(Ann+d*Bg)
XGX=sp.factor(X2-lam/(d*lam-1)*trX**2)
dentry=sp.factor(4*sqrtg/Mpl**2*q**2*XGX)
B=sp.Matrix([[aentry,-F],[F,dentry]])
detB=sp.factor(B.det())
assert sp.simplify(detB-(F**2+aentry*dentry))==0
# Leading coefficient must reproduce the exact antisymmetric leading theorem.
leadF=sp.simplify(sp.limit(F/q,q,0,dir='+'))
x_over=sp.factor(V*sqrtg*(rho-tau)/M2)
assert sp.simplify(leadF-(b2+x_over))==0
lead_det=sp.simplify(sp.limit(detB/q**2,q,0,dir='+'))
assert sp.simplify(lead_det-leadF**2)==0
# At any off-diagonal zero, determinant reduces exactly to a*d.
Fsym=sp.symbols('Fsym', real=True)
asym,dsym=sp.symbols('asym dsym', real=True)
assert sp.det(sp.Matrix([[asym,-Fsym],[Fsym,dsym]])).subs(Fsym,0)==asym*dsym

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_EXACT_BAROTROPIC_BLOCK_PASS',
  'status_scope':'GREEN_EXACT_FLAT_BAROTROPIC_BLOCK_SYMBOL_UV_WILSON_VALUES_AND_ROOT_SCAN_PENDING',
  'domain':'d=3 flat homogeneous isotropic canonical background, N=1 time gauge, barotropic/commuting ordinary-matter stress response, beta0_bare=0, Zhu soft-detailed-balance pure-lapse UV basis, eta1=eta2=0',
  'matrix':'B(q)=[[a(q),-F(q)],[F(q),d(q)]]',
  'b2':str(b2),
  'V':str(V),
  'a_exact':'-2(beta2+beta4)q^2-4 beta8 q^3/M_Pl^2',
  'F_exact':str(F),
  'd_exact':'(4 sqrt(g)/M_Pl^2) q^2 X(q) G X(q), with X_nn=A0+M_c^2 rho/(M_c^2+q)^2 and X_g=-A0-tau_rho/[3(M_c^2+q)]',
  'det_exact':'det B(q)=F(q)^2+a(q)d(q)',
  'leading_det_over_q2':str(sp.factor(lead_det)),
  'offdiagonal_zero_rule':'At F(q*)=0 the full determinant is a(q*)d(q*), so an off-diagonal zero is only a candidate rank-loss point.',
  'literature_support_note':'Mukohyama et al. explicitly state after Eqs.(55)-(58) that only Eq.(55) depends on L_V; thus the UV lapse Wilson coefficients enter a(q) but not b,c,d on this special branch.',
  'interpretation':'Within the stated flat barotropic candidate-UV scope, the low/intermediate-q classical rank problem is reduced to roots of one explicit rational-plus-polynomial determinant rather than an unspecified remainder matrix.',
  'non_claims':[
    'does not freeze beta2+beta4 or beta8',
    'does not cover generic non-barotropic matter Poisson response or anisotropic stress',
    'does not prove the determinant has no positive-q roots for every Wilson tuple',
    'does not choose M_c or certify curved/inhomogeneous backgrounds'
  ],
  'next_gate':'classify det B at the exact off-diagonal root and derive sign/sufficient no-root conditions in terms of beta2+beta4,beta8,lambda and the matter background; then perform a dimensionless symbolic/numerical root scan only after a UV Wilson domain is frozen.'
}
open('u1_flat_flrw_exact_barotropic_block_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
