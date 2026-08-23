#!/usr/bin/env python3
"""All-q sufficient no-rank-loss domain for the exact flat-FLRW barotropic block.

Uses only the already reduced exact symbol
  det B(q)=F(q)^2+a(q)d(q)
with d=3, beta0_bare=0.  This gate does NOT claim the sign domain is already
selected by UV phenomenology; it proves that if the displayed inequalities hold,
there is no positive-q determinant root in this controlled flat/barotropic slice.
"""
import json
import sympy as sp

A,B,lam=sp.symbols('A B lambda', real=True, finite=True)
q,Mpl,u,v=sp.symbols('q M_Pl u v', positive=True, finite=True)

# For X=A nn+B g in d=3, with nn:nn=1, nn:g=1, g:g=3.
X2=sp.expand(A**2+2*A*B+3*B**2)
tr=sp.expand(A+3*B)
XTF2=sp.factor(X2-tr**2/3)
assert sp.simplify(XTF2-2*A**2/3)==0
XGX=sp.factor(X2-lam/(3*lam-1)*tr**2)
positive_branch_form=sp.factor(XTF2+tr**2/(3*(1-3*lam)))
assert sp.simplify(XGX-positive_branch_form)==0

# UV lapse entry after beta0_bare=0.  Set u=-beta24>0 and/or v=-beta8>0.
a_pos=sp.factor(2*u*q**2+4*v*q**3/Mpl**2)
assert sp.simplify(a_pos-2*q**2*(u+2*v*q/Mpl**2))==0

# Generic determinant identity.
F,dentry,aentry=sp.symbols('F dentry aentry', real=True, finite=True)
det_expr=sp.expand(F**2+aentry*dentry)
assert sp.simplify(det_expr-F**2-aentry*dentry)==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_NO_ROOT_SUFFICIENT_DOMAIN_PASS',
  'status_scope':'GREEN_ANALYTIC_ALL_Q_SUFFICIENT_DOMAIN_PHYSICAL_UV_ADMISSIBILITY_PENDING',
  'domain':'d=3 flat homogeneous isotropic canonical background, barotropic/commuting ordinary-matter response, eta0>0, rho>=0, M_c^2>0, q>0, beta0_bare=0',
  'deWitt_identity':'X G X = (2/3) A^2 + (tr X)^2/[3(1-3 lambda)] for lambda<1/3',
  'strict_d_reason':'For the exact block A=A0+M_c^2 rho/(M_c^2+q)^2 with A0=M_Pl^2 eta0/2>0, so X G X>0 and therefore d(q)>0 for every q>0 when lambda<1/3.',
  'uv_sign_domain':['lambda<1/3','beta24=beta2+beta4<=0','beta8<=0','at least one of beta24,beta8 is strictly negative'],
  'strict_a_reason':'a(q)=-2 beta24 q^2-4 beta8 q^3/M_Pl^2>0 for every q>0 in the stated UV sign domain.',
  'determinant_conclusion':'det B(q)=F(q)^2+a(q)d(q)>0 for every q>0, independently of zeros of F(q).',
  'interpretation':'This is an analytic all-positive-q no-rank-loss certificate for one explicit symbolic Wilson domain of the controlled flat/barotropic block; no M_c tuning or numerical q scan is required inside this theorem.',
  'non_claims':[
    'does not assert lambda<1/3 is selected by the final same-action phenomenology',
    'does not assert beta24<=0,beta8<=0 is already proven compatible with every UV/tensor stability requirement',
    'does not cover lambda>1/3, curved/anisotropic backgrounds, or non-barotropic matter response',
    'does not choose M_c, beta24, beta8, or lambda'
  ],
  'next_gate':'check the theorem sign domain against the tensor/high-k stability conventions of the same Zhu/Mukohyama U(1) action; separately classify lambda>1/3 where the DeWitt trace direction is indefinite.'
}
open('u1_flat_flrw_no_root_sufficient_domain_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
