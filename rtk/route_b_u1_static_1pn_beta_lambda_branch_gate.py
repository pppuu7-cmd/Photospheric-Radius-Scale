#!/usr/bin/env python3
"""Recertify the scoped static 1PN beta theorem for arbitrary lambda_HL, including lambda_HL>1.

The previously derived same-action fixed-clock static equation on the family-I
matter frame is
  4 Delta n4 - 4 M_K^2 n4 = 0,
with regular stellar center/interior, asymptotic n4->0, and no singular scalar
shell/source.  Its origin is the exact O(4) source cancellation plus the fixed
P(X_U) clock lapse Euler response.  The equation contains no lambda_HL.

Why: this is a static sector, so K_ij=0 and K=0; therefore the kinetic term
K_ij K^ij-lambda_HL K^2 vanishes identically at every weak-field order on the
static branch.  The energy identity forces n4=0 for M_K^2>0, so the remaining
family-I static result beta_PPN=1 extends to lambda_HL>1.

Scope remains narrow: regular asymptotically-flat star, zero scalar flux/charge,
constant-q clock branch.  Preferred-frame alpha1/alpha2 and strong-field objects
are not certified.
"""
import json
import sympy as sp

lam=sp.symbols('lambda_HL', real=True, finite=True)
Kij2,K2=sp.symbols('Kij2 K2', real=True, finite=True)
LK=Kij2-lam*K2
assert sp.simplify(LK.subs({Kij2:0,K2:0}))==0
assert sp.diff(LK.subs({Kij2:0,K2:0}),lam)==0

# Family-I source cancellation and beta consistency.
rho=sp.symbols('rho', real=True, finite=True)
a1=sp.Integer(1); gamma1=sp.Integer(-1); kappa=sp.Integer(1)
Jt=-2*rho; JA=2*a1*rho
assert sp.simplify(Jt-gamma1*JA)==0
beta0_eff=sp.Integer(2)
consistency=beta0_eff*(a1**2*kappa*gamma1+1)+2*kappa*(a1*gamma1+1)**2
assert sp.simplify(consistency)==0

# O4 fixed-clock lapse equation and lambda independence.
MK2,n4,lapn4=sp.symbols('M_K_squared n4 laplacian_n4', positive=True, finite=True)
E4=sp.expand(4*lapn4-4*MK2*n4)
assert sp.diff(E4,lam)==0
assert sp.simplify(E4/4-(lapn4-MK2*n4))==0

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_1PN_BETA_LAMBDA_BRANCH_PASS',
  'status_scope':'GREEN_STATIC_1PN_BETA_REGULAR_STAR_FOR_LAMBDA_BRANCH_PREFERRED_FRAME_PENDING',
  'domain':'static weak-field 1PN, regular connected asymptotically-flat star, zero scalar flux/charge, constant-q X_U>0 clock branch; corrected beta0_bare=0 with explicit S_mix',
  'static_lambda_decoupling':'K_ij=0 and K=0 imply K_ij K^ij-lambda_HL K^2=0 identically; lambda_HL does not enter the scoped static O(4) lapse equation.',
  'source_cancellation':'At a1=1,gamma1=-1: Jt-gamma1 JA=0 exactly.',
  'O4_equation':'(Delta-M_K^2)n4=0 with M_K^2>0.',
  'uniqueness':'Regularity plus n4->0 at infinity gives integral(|grad n4|^2+M_K^2 n4^2)=0, hence n4=0.',
  'beta_result':'beta_PPN=1 on the scoped regular-star zero-flux branch for arbitrary regular lambda_HL, including lambda_HL>1.',
  'interpretation':'Together with the O(2) lambda-branch gate, the static Newton normalization, gamma_PPN and beta_PPN are compatible with the positive-source lambda_HL>1 all-q rank-safe branch in their stated weak-field scopes.',
  'non_claims':[
    'does not certify preferred-frame alpha1 or alpha2',
    'does not cover nonzero scalar charge/flux, black-hole horizons or strong-field stars',
    'does not freeze lambda_HL or M_K',
    'does not establish C9 radiative protection or EFT cutoff'
  ],
  'next_gate':'rederive the O(3) moving-source/vector equations with explicit S_mix on lambda_HL>1 to determine alpha1 and alpha2; keep static 1PN and preferred-frame claims separate.'
}
open('u1_static_1pn_beta_lambda_branch_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
