#!/usr/bin/env python3
"""Scoped moving-source O(3) clock-source cancellation on the fixed U1 family-I action.

We linearize the fixed shift-symmetric P(X_U)+C(X_U)(D Theta_U)^2 sector about
Sigma=q t, D_i Sigma=0, N=1+O(4), g_ij=(1+2U)delta_ij, and the family-I O(3)
shift.  To first order the scalar perturbation pi has equation

 (P_X+q^2 P_XX) ddot(pi) - 2 C Delta ddot(pi) - P_X Delta pi
 + q P_X [3 dot(U)-partial_i N^i] = 0.

The metric source is the perturbation of sqrt(g) times the background clock
charge, together with the shift advection term.  Exact production identities
give 2C/(P_X+q^2P_XX)=1/M_K^2 and P_X/(P_X+q^2P_XX)=c_a^2.

For the nonprojectable U1 family I with a1=kappa=1, a2=0, sigma1=sigma2=0,
the published O(3) momentum solution has c=-4 and, for regular lambda != 1,
d=1/2. Since chi_,0i=V_i-W_i,
  N_i = -4 V_i + (1/2)(V_i-W_i)
      = -(7/2)V_i-(1/2)W_i.
Using div V=-dot U and div(V-W)=-2 dot U gives div W=+dot U and hence
  div N = 3 dot U.
Therefore the fixed RTK clock has zero O(3) moving-matter source. With zero
incoming scalar perturbation / retarded homogeneous initial data, pi_O3=0, so
this scalar sector does not change the published family-I O(3) alpha1=alpha2=0
result in the regular lambda !=1 domain.

At exact lambda=1 the published O(3) equation loses the condition fixing d;
this gate deliberately does not certify that singular parameter point.
"""
import json
import sympy as sp

# Published family-I O3 momentum equation specialized to a1=kappa=1,a2=0,
# gamma=1: (1-lambda)(2d-1)=0.
lam,d=sp.symbols('lambda_HL d', finite=True, real=True)
momentum=sp.factor((1-lam)*(2*d-1))
assert sp.simplify(momentum-(1-lam)*(2*d-1))==0
d_regular=sp.Rational(1,2)

# Shift coefficients c=-4*kappa=-4 and d=1/2.
c=sp.Integer(-4)
# chi_,0i = V_i-W_i => N_i=(c+d)V_i-d W_i.
coefV=sp.simplify(c+d_regular)
coefW=sp.simplify(-d_regular)
assert coefV==-sp.Rational(7,2) and coefW==-sp.Rational(1,2)

# PPN divergence identities: div V=-Udot; div(V-W)=-2Udot -> div W=+Udot.
Udot=sp.symbols('Udot', finite=True, real=True)
divV=-Udot
divW=Udot
divN=sp.simplify(coefV*divV+coefW*divW)
source=sp.simplify(3*Udot-divN)
assert divN==3*Udot and source==0

# Fixed scalar kinetic ratios.
PX,PXX,q2,C,Mpl2,MK2=sp.symbols('P_X P_XX q2 C Mpl2 MK2', positive=True, finite=True, real=True)
Akin=PX+q2*PXX
# q2=2X, C=Mpl2/q2, q2*Akin=Kphys=2 Mpl2 MK2.
ratio_mix=sp.simplify((2*(Mpl2/q2))/(2*Mpl2*MK2/q2))
assert ratio_mix==1/MK2
ca2=sp.symbols('c_a2', positive=True, finite=True, real=True)

out={
  'classification':'RTK_ROUTE_B_U1_MOVING_O3_CLOCK_SOURCE_CANCELLATION_PASS',
  'scope':'linear moving-source O(3), regular nonprojectable family-I lambda_HL != 1, X_U>0, retarded/no-incoming scalar perturbation',
  'frozen_family_I':{'a1':1,'a2':0,'kappa':1,'gamma1':-1,'sigma1':0,'sigma2':0,'beta0_eff_static':2},
  'published_O3':{
    'momentum_constraint_specialization':'(1-lambda_HL)(2d-1)=0',
    'regular_domain':'lambda_HL != 1 gives d=1/2; c=-4',
    'shift':'N_i=-(7/2)V_i-(1/2)W_i',
    'pure_family_I_preferred_frame':'alpha1=alpha2=0'
  },
  'clock_linear_equation':'(P_X+q^2 P_XX) ddot(pi)-2 C Delta ddot(pi)-P_X Delta pi + q P_X(3 dotU-divN)=0',
  'fixed_action_ratios':{
    '2C_over_Akin':'1/M_K^2',
    'P_X_over_Akin':'c_a^2',
    'reduced_operator':'(1-Delta/M_K^2)ddot(pi)-c_a^2 Delta pi + q c_a^2(3 dotU-divN)=0'
  },
  'PPN_divergence_identities':['div V=-dot U','div(V-W)=-2 dot U','therefore div W=+dot U'],
  'div_shift':str(divN),
  'clock_source_residual':str(source),
  'result':'The homogeneous fixed RTK clock is not sourced at O(3) by moving ordinary matter on the regular family-I solution. With retarded/no-incoming scalar data, pi_O3=0 and the fixed scalar sector does not shift the published alpha1=alpha2=0 at this PN order.',
  'status_scope':'MOVING_O3_PREFERRED_FRAME_GREEN_FOR_REGULAR_LAMBDA_NOT_1',
  'non_claims':[
    'does not certify exact lambda_HL=1, where the published O3 equation does not fix d',
    'does not prove higher-PN preferred-frame terms vanish',
    'does not cover strong-field systems, nonzero scalar charge/flux, or incoming scalar waves',
    'does not establish radiative stability or the C9 cutoff'
  ],
  'next_gate':'either freeze a concrete regular lambda_HL !=1 after the strong-coupling/cutoff analysis, or derive the exact lambda_HL=1 O3 constrained solution directly; then extend the scalar-current audit to O4/O5 and binary/strong-field preferred-frame response'
}
open('u1_moving_o3_clock_source_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
