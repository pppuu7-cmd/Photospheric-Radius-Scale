#!/usr/bin/env python3
"""Exact q^2 coefficient of d={Jhat,phi_hat} from the DeWitt square on FLRW.

On the special U(1) branch the published pure-gravity Eq. (58) is the kinetic
DeWitt square of the metric derivative of J. After auxiliary projection,
Jhat=Jg-a_eff H0 remains independent of gravity momentum. On an isotropic
ordinary-matter background without anisotropic stress, at leading q=|k|^2,

 D_g Jg = q sqrt(g) A0 (-g^ij+n^i n^j), A0=M_Pl^2 eta0/2,
 D_g Jm = q sqrt(g)/M_c^2 [rho n^i n^j-(tau_rho/d)g^ij] + O(q^2),

where n^i is the unit k direction, rho=H0/sqrt(g), and
tau_rho=(g_ij delta H0/delta g_ij)/sqrt(g).

The q^2 coefficient of d is therefore
  d4 = 4 sqrt(g)/M_Pl^2 * X^{ij} G_ijkl X^{kl},
with X the sum of the two displayed q-normalized tensors. Filter remainders in
D_g Jm begin at q^2 and thus affect d only at q^3 or higher.
"""
import json
import sympy as sp

d,lam=sp.symbols('d lambda', finite=True)
eta,Mpl,sqrtg,M2=sp.symbols('eta0 M_Pl sqrtg M_c_squared', nonzero=True, finite=True)
rho,tau=sp.symbols('rho tau_rho', real=True, finite=True)
A0=sp.simplify(Mpl**2*eta/2)
# X = a nn + b delta, with nn:nn=1, nn:delta=1, delta:delta=d.
a=sp.simplify(A0+rho/M2)
b=sp.simplify(-A0-tau/(d*M2))
X2=sp.expand(a**2+2*a*b+d*b**2)
trX=sp.expand(a+d*b)
XGX=sp.factor(X2-lam/(d*lam-1)*trX**2)
d4=sp.factor(4*sqrtg/Mpl**2*XGX)

# Pure-gravity limit must reproduce the separate Eq.(58) theorem.
pure_expected=sp.factor(sqrtg*Mpl**2*eta**2*(d-1)*(lam-1)/(d*lam-1))
assert sp.simplify(d4.subs({rho:0,tau:0})-pure_expected)==0

# Extract expansion in u=1/Mc^2: pure + cross*u + self*u^2.
u=sp.symbols('u', real=True, finite=True)
d4u=sp.expand(d4.subs(M2,1/u))
pure=sp.factor(d4u.coeff(u,0))
cross=sp.factor(d4u.coeff(u,1))
selfterm=sp.factor(d4u.coeff(u,2))
assert sp.simplify(pure-pure_expected)==0
assert sp.simplify(d4u-(pure+cross*u+selfterm*u**2))==0
# Cross term independently expected from T G B contraction.
cross_expected=sp.factor(4*sqrtg*eta*(d-1)/(d*lam-1)*(lam*rho-tau/d))
assert sp.simplify(cross-cross_expected)==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_TOTAL_D4_DEWITT_SQUARE_PASS',
  'status_scope':'GREEN_EXACT_ISOTROPIC_TOTAL_D4_FILTER_REMAINDER_Q3_AND_UV_A_REMAINDER_PENDING',
  'domain':'flat FLRW, isotropic gravity momentum and ordinary-matter metric response, no background anisotropic stress, regular projected filter, d lambda != 1',
  'X_tensor':'X=A0(-g+nn)+(1/M_c^2)[rho nn-(tau_rho/d)g], A0=M_Pl^2 eta0/2',
  'exact_d4':'d4=(4 sqrt(g)/M_Pl^2) X G X',
  'pure_gravity_d4':str(pure),
  'gravity_matter_cross_coefficient_of_1_over_Mc2':str(cross),
  'matter_self_coefficient_of_1_over_Mc4':str(selfterm),
  'cross_closed_form':'4 sqrt(g) eta0 (d-1)/(d lambda-1) * (lambda rho-tau_rho/d)',
  'filter_remainder_order':'The O(q^2) remainder of D_g Jm contributes only O(q^3) or higher to d and cannot alter this q^2 coefficient.',
  'interpretation':'The full q^2 (2,2) cross-block coefficient is fixed on the isotropic FLRW projected background once rho,tau_rho,M_c and lambda are specified; it is not an independent unknown remainder coefficient.',
  'non_claims':[
    'does not cover anisotropic-stress backgrounds',
    'does not include q^3-and-higher filter or UV corrections',
    'does not determine the pure-lapse a(q) UV Wilson coefficients beta2+beta4,beta8',
    'does not choose M_c or lambda'
  ],
  'next_gate':'assemble the q^2 remainder matrix using a4=-2(beta2+beta4), exact filtered off-diagonal q^2 remainders, and this d4; derive a symbolic operator-norm C2 bound.'
}
open('u1_flat_flrw_total_d4_dewitt_square_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
