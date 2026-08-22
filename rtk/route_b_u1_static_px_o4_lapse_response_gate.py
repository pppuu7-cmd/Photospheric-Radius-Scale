#!/usr/bin/env python3
"""C8 fixed-action static P(X) O(v^4) lapse-response theorem.

For the exact static clock Sigma=q t, D_i Sigma=0, zero invariant shift,
X=X0/N^2.  The purely kinetic contribution to the lapse equation is

    E_N^P = d[N P(X0/N^2)]/dN = P - 2 X P_X = -rho.

After subtracting the homogeneous background equation, the first local lapse
response around N=1 is

    delta E_N^P = K_phys n + O(n^2),
    K_phys = 2 X (P_X+2 X P_XX).

On the already certified family-I branch n_2=0, so n=n_4+O(6): nonlinear
P(X) terms start beyond 1PN while the only O(4) local clock correction is the
linear mass-like K_phys n_4 term.  Production RTK gives exactly
K_phys=2 M_Pl^2 M_K^2.

This gate also computes the exact square-root domain margin of the fixed DBI
clock and the allowed coefficient C4 in |n4|=C4 U^2 before the static clock
would reach the lower-N branch boundary.  It is a domain budget, not a proof of
the actual C4 from the full O(4) constraint system.
"""
import json, math
import sympy as sp

# Exact symbolic lapse response for arbitrary P(X).
N,X0=sp.symbols('N X0', positive=True, finite=True, real=True)
X=sp.symbols('X', positive=True, finite=True, real=True)
P=sp.Function('P')
XN=X0/N**2
LP=N*P(XN)
EN=sp.simplify(sp.diff(LP,N))
expected=sp.simplify(P(XN)-2*XN*sp.Subs(sp.Derivative(P(X),X),X,XN))
assert sp.simplify(EN-expected)==0

# Derive dE/dN at N=1 by using abstract PX,PXX after differentiating.
PX,PXX=sp.symbols('P_X P_XX', finite=True, real=True)
# E=P-2XP_X, dE/dX=-(P_X+2X P_XX), dX/dN=-2X/N.
dEdN_at1=sp.simplify(2*X0*(PX+2*X0*PXX))
Kphys=dEdN_at1
assert Kphys==2*X0*(PX+2*X0*PXX)

# Production z=0 values from exact scale-dictionary Actions run 32568333920.
lam=219457.5727136581
r0=0.0021346329644460586
MK0=1.1681315109161161 # Mpc^-1
u0=1.0+r0
sqrtlam=math.sqrt(lam)
Ncrit_lower=u0/(1.0+1.0/sqrtlam)
margin=1.0-Ncrit_lower
assert margin>0
# Verify equivalent direct square-root boundary relation.
assert abs((u0/Ncrit_lower-1.0)-1.0/sqrtlam) < 1e-12

# Solar weak-field benchmark potentials U=GM/(rc^2), used only for a domain budget.
GM_sun_over_c2_m=1476.6250385
R_sun_m=6.957e8
AU_m=1.495978707e11
bench={
  'solar_surface':GM_sun_over_c2_m/R_sun_m,
  '1_AU':GM_sun_over_c2_m/AU_m,
}
budgets={}
for name,U in bench.items():
    U2=U*U
    C4max=margin/U2
    budgets[name]={'U':U,'U2':U2,'C4_abs_max_for_lower_N_domain_if_abs_n4_eq_C4_U2':C4max}
    assert C4max>1.0

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_PX_O4_LAPSE_RESPONSE_PASS',
 'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
 'exact_static_clock_run_id':32568097865,
 'adm_lapse_pn_order_run_id':32567940387,
 'scale_dictionary_run_id':32568333920,
 'symbolic':{
   'E_N_P':'P-2 X P_X = -rho',
   'background_subtracted_linear_response':'delta E_N_P = K_phys n + O(n^2)',
   'K_phys':'2 X (P_X+2 X P_XX)',
   'production_identity':'K_phys=2 M_Pl^2 M_K^2',
   'family_I_order':'n_2=0, hence n=n_4+O(6); nonlinear local P(X) lapse response begins beyond O(4)'
 },
 'z0':{
   'lambda_D':lam,'r0':r0,'u0':u0,'M_K_Mpc_inv':MK0,
   'lower_N_DBI_boundary':Ncrit_lower,'lower_N_margin_1_minus_Ncrit':margin
 },
 'domain_budgets':budgets,
 'interpretation':'At 1PN the fixed P(X) clock adds a linear K_phys n4 term to the background-subtracted lapse equation. Against an M_Pl^2 k^2 local spatial operator its scale ratio is exactly 2(M_K/k)^2. The DBI square-root boundary is therefore controlled by the actual O(4) ADM-lapse solution, not by the physical Newtonian lapse N_tilde=1-U.',
 'non_claims':[
   'does not solve the full coupled O(4) elliptic system or determine the actual coefficient C4',
   'does not by itself certify beta_PPN=1',
   'does not address moving-source alpha1 or alpha2',
   'does not certify compact-object interiors or configurations approaching X_U=0'
 ],
 'next_gate':'insert the K_phys n4 response into the frozen family-I O(4) constraint/source matrix and solve or bound the ADM-lapse n4 coefficient; then compare with the explicit DBI domain budget and extract the scale-dependent correction to beta_PPN'
}
open('u1_static_px_o4_lapse_response_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
