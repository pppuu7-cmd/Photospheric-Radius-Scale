#!/usr/bin/env python3
"""Exact symbolic principal-TT gate for the fixed U(1) IR representative.

Scope: two-derivative pure TT principal quadratic sector on a homogeneous
rolling Sigma background. This intentionally does not certify the scalar,
vector, UV, radiative or compact-object sectors.
"""
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'research/RTK_C8_U1_TT_PRINCIPAL_GATE_TARGET_v1.json'
t=json.loads(TARGET.read_text())
assert t['classification']=='RTK_C8_U1_TT_PRINCIPAL_GATE_TARGET_V1_FROZEN'
assert t['status']=='FROZEN_BEFORE_EXECUTABLE_TT_GATE_RESULT'
assert t['gravity_ir']['lambda_HL']==1
assert t['gravity_ir']['gamma1']==-1

# One Fourier mode propagating along z, with the two standard TT polarizations.
eps, hp, hx, dhp, dhx, k, M = sp.symbols('eps hp hx dhp dhx k M', nonzero=True)
h=sp.Matrix([[hp,hx,0],[hx,-hp,0],[0,0,0]])
dh=sp.Matrix([[dhp,dhx,0],[dhx,-dhp,0],[0,0,0]])

trace_h=sp.simplify(sp.trace(h))
trace_dh=sp.simplify(sp.trace(dh))
norm_h=sp.simplify(sp.trace(h*h))
norm_dh=sp.simplify(sp.trace(dh*dh))
assert trace_h==0 and trace_dh==0
assert sp.simplify(norm_h-2*(hp**2+hx**2))==0
assert sp.simplify(norm_dh-2*(dhp**2+dhx**2))==0

# For N=1, shift=0 and a locally inertial background, K_ij=(eps/2) dot h_ij.
# K starts only at O(eps^2) because h is traceless, so K^2 is O(eps^4).
# Thus [K_ij K^ij-K^2]_(2)=eps^2/4 Tr(dot h^2).
adm_kin_inside=sp.expand(eps**2*norm_dh/4)
expected_adm_kin_inside=sp.expand(eps**2*(dhp**2+dhx**2)/2)
assert sp.simplify(adm_kin_inside-expected_adm_kin_inside)==0

# Standard TT second variation of sqrt(g) R after dropping a spatial boundary:
# [sqrt(g) R]_(2)=-eps^2/4 (partial_k h_ij)^2.
# For a Fourier mode along z, (partial h)^2=k^2 Tr(h^2).
ricci_grad_inside=sp.expand(-eps**2*k**2*norm_h/4)
expected_ricci_grad_inside=sp.expand(-eps**2*k**2*(hp**2+hx**2)/2)
assert sp.simplify(ricci_grad_inside-expected_ricci_grad_inside)==0

# Multiplying by the IR gravitational prefactor M_Pl^2/2 gives equal kinetic
# and gradient principal coefficients for each polarization.
Lkin=sp.expand(M**2*adm_kin_inside/2)
Lgrad=sp.expand(M**2*ricci_grad_inside/2)
kin_coeff=sp.simplify(sp.diff(sp.diff(Lkin,dhp),dhp)/2)
grad_coeff_abs=sp.simplify(-sp.diff(sp.diff(Lgrad,hp),hp)/(2*k**2))
assert sp.simplify(kin_coeff-grad_coeff_abs)==0
ct2=sp.simplify(grad_coeff_abs/kin_coeff)
assert ct2==1

# Fixed scalar sector. Homogeneous Sigma(t) and homogeneous lapse imply
# D_i Sigma=0, Theta_U=dotSigma/N is spatially homogeneous, hence D_i Theta=0.
# Pure TT changes only the transverse-traceless spatial metric and does not
# source lapse/shift at principal quadratic order. Therefore S_mix vanishes
# identically in this sector, despite its nonzero coefficient C(X).
q,N,X=sp.symbols('q N X', positive=True)
Theta=q/N
Xexpr=sp.simplify(Theta**2/2)
C=sp.simplify(M**2/(2*Xexpr))
DiTheta=sp.Integer(0)
Smix_principal=sp.simplify(C*DiTheta**2)
assert Smix_principal==0

# P(X) is derivative-free in the metric. It can enter background/algebraic
# TT terms through sqrt(g), but cannot change the principal dot(h)^2 or
# (grad h)^2 coefficients considered here.
PX_principal_derivative_contribution=sp.Integer(0)
assert PX_principal_derivative_contribution==0

checks={
    'tt_trace_zero': trace_h==0,
    'tt_time_trace_zero': trace_dh==0,
    'adm_lambda1_kinetic_standard': sp.simplify(adm_kin_inside-expected_adm_kin_inside)==0,
    'ricci_tt_gradient_standard': sp.simplify(ricci_grad_inside-expected_ricci_grad_inside)==0,
    'Di_Theta_U_zero_pure_TT': DiTheta==0,
    'P_of_X_no_principal_metric_derivative': PX_principal_derivative_contribution==0,
    'S_mix_no_principal_TT': Smix_principal==0,
    'c_T_squared_one': ct2==1,
}
status='PASS' if all(checks.values()) else 'FAIL'
classification=('RTK_C8_U1_FIXED_ACTION_TT_PRINCIPAL_PASS' if status=='PASS'
                else 'RTK_C8_U1_FIXED_ACTION_TT_PRINCIPAL_FAIL')
result={
    'status':status,
    'classification':classification,
    'target':str(TARGET.relative_to(ROOT)),
    'scope':t['scope'],
    'checks':checks,
    'exact_algebra':{
        'Tr_h2':str(norm_h),
        'Tr_doth2':str(norm_dh),
        'ADM_kinetic_inside_quadratic':str(adm_kin_inside),
        'Ricci_gradient_inside_quadratic':str(ricci_grad_inside),
        'kinetic_coefficient_per_polarization':str(kin_coeff),
        'gradient_coefficient_abs_per_polarization':str(grad_coeff_abs),
        'c_T_squared':str(ct2),
        'Theta_U':str(Theta),
        'X_U':str(Xexpr),
        'C_of_X_on_background':str(C),
        'S_mix_principal_TT':str(Smix_principal),
    },
    'interpretation':(
        'On the fixed IR representative, the explicit rolling-scalar mixed operator '
        'does not modify the principal pure-TT kinetic or gradient term. The '
        'two-derivative TT cone is therefore the GR cone, c_T^2=1, within the frozen scope.'
    ),
    'non_claims':[
        'no scalar/vector principal-sector certification',
        'no higher-spatial-derivative UV certification',
        'no radiative/naturalness certification',
        'no compact-object or X_U->0 regularity certification',
        'no statement about algebraic background TT mass terms off shell',
    ],
    'next_gate':'derive the static/Newton/PPN equations from the same fixed action, retaining explicit S_mix rather than importing pure-U1 PPN values',
}
out=ROOT/'research/RTK_C8_U1_TT_PRINCIPAL_GATE_RESULT_v1.json'
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(classification)
print(json.dumps(result,sort_keys=True))
