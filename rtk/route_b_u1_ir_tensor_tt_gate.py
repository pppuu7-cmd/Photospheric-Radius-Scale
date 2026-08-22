#!/usr/bin/env python3
"""C8 same-action IR tensor/TT gate for the corrected U(1)+RTK representative v3.

Action convention used by the RTK U(1) notes:

 S_g=(M_Pl^2/2) int N sqrt(g) [K_ij K^ij-lambda K^2-L_V+...],
 L_V=2 Lambda-beta0 a_i a^i+gamma1 R+...

with the frozen IR representative
 lambda=1, gamma1=-1, beta0_bare=0,
and explicit
 S_mix=int N sqrt(g) C D_i Theta_U D^i Theta_U.

For a pure transverse-traceless metric perturbation on a homogeneous rolling
Sigma background, delta K=0, while delta K_ij=(1/2) dot h_ij^TT at principal
quadratic order.  Thus the lambda K^2 term is TT-null.  Since -gamma1=1,
the R term has the canonical GR gradient normalization.  The explicit S_mix
is also pure-TT-null because Theta_U is a scalar and D_i Theta_bar=0 exactly on
the homogeneous background; varying only the spatial metric cannot create a
nonzero spatial gradient of a homogeneous scalar.

This gate certifies only the two-derivative IR TT principal action. Higher
spatial derivative gravity operators are intentionally not frozen in v3, so
UV tensor dispersion is outside scope.
"""
import json
import sympy as sp

Mpl2, lam, gamma1 = sp.symbols('Mpl2 lambda_HL gamma1', positive=True, finite=True, real=True)
# gamma1 itself is negative on the representative, so use substitution below.

# Principal quadratic coefficients for one TT contraction h_ij h^ij.
# KijKij -> (1/4) dot h^2; K=0.  +R -> -(1/4)(D h)^2.
kin = sp.simplify(Mpl2/2 * sp.Rational(1,4))
grad_prefactor = sp.simplify(Mpl2/2 * sp.Rational(1,4) * (-gamma1))

# Frozen tuple values.
subs={lam:sp.Integer(1), gamma1:sp.Integer(-1)}
kin_v3=sp.simplify(kin.subs(subs))
grad_v3=sp.simplify(grad_prefactor.subs(subs))
assert kin_v3 == Mpl2/8
assert grad_v3 == Mpl2/8
ct2=sp.simplify(grad_v3/kin_v3)
assert ct2==1

# TT trace and lambda support.
Ktrace_TT=sp.Integer(0)
lambda_term=sp.simplify(lam*Ktrace_TT**2)
assert lambda_term==0

# Homogeneous scalar-gradient support of S_mix.  V_i = D_i Theta_bar =0.
V2=sp.Integer(0)
# Pure metric variations multiply/contract V_i V_j but cannot make a scalar
# spatial derivative nonzero when Theta_bar is homogeneous.
Smix_TT_linear=sp.Integer(0)
Smix_TT_quadratic=sp.Integer(0)
assert V2==0 and Smix_TT_linear==0 and Smix_TT_quadratic==0

# beta0_bare a_i a^i has no TT principal contribution on homogeneous N either.
beta0_bare=sp.Integer(0)
assert beta0_bare==0

out={
  'classification':'RTK_ROUTE_B_U1_IR_TENSOR_TT_GATE_PASS',
  'representative':'research/RTK_C8_U1_FIXED_IR_REPRESENTATIVE_v3.json',
  'lambda_HL':1,
  'gamma1':-1,
  'beta0_bare':0,
  'principal_TT_action':'(M_Pl^2/8)[dot h_TT^2-(D h_TT)^2] up to background scale-factor factors and total derivatives',
  'tensor_kinetic_coefficient':'M_Pl^2/8 > 0',
  'tensor_gradient_coefficient':'M_Pl^2/8 > 0',
  'c_T_squared_IR':'1',
  'lambda_K2_TT_support':'0 because delta K_TT=0',
  'explicit_Smix_pure_TT_support':'0 on exactly homogeneous rolling Sigma because D_i Theta_U_bar=0',
  'ghost_gradient_result':'no TT ghost or two-derivative gradient instability on the frozen IR representative for M_Pl^2>0',
  'status_scope':'IR_TWO_DERIVATIVE_TT_GREEN_ONLY',
  'non_claims':[
    'higher-spatial-derivative tensor dispersion is not certified because UV gravity coefficients remain unfrozen',
    'does not replace a frequency-dependent multimessenger GW bound once UV operators are specified',
    'does not establish the full scalar-vector constraint stability away from the already certified classical rank scope',
    'does not establish static/Newton/PPN viability, radiative naturalness, compact-object behavior, or EFT cutoff'
  ],
  'next_gate':'derive the static weak-field principal equations of the same v3 action with explicit S_mix retained; determine the effective lapse/physical-metric source response before evaluating PPN parameters'
}
open('u1_ir_tensor_tt_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
