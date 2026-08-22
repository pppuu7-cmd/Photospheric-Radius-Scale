#!/usr/bin/env python3
"""C8 fixed-action static spherical zero-flux scalar-branch theorem.

Take zero invariant shift and a static spherical geometry.  Let

    Sigma = q t + psi(r),
    Theta_U = q/N(r),
    X = 1/2 [Theta_U^2 - g^{rr} psi'^2],
    Y = D_i Theta_U D^i Theta_U.

For the fixed shift-symmetric scalar Lagrangian

    L_s = N sqrt(g) [P(X) + C(X) Y],
    C(X)=M_Pl^2/(2X),

the radial scalar equation integrates once to a conserved flux

    F_r = -N sqrt(g) g^{rr} psi' [P_X + C_X Y].

For a regular stellar center with no scalar charge/flux, F_r=0.  Therefore a
regular zero-flux solution is pointwise on one of two branches:

  (A) psi'=0, the already studied constant-q clock branch;
  (B) P_X + C_X Y = 0.

On branch B, using C_X=-M_Pl^2/(2X^2) and P_phys=M_Pl^2 P_8,

    2X P_{8,X} = Y/X.

But 2X P_{8,X}=rho_8+p_8.  Hence the exact branch condition is

    (rho+p)_8piG = Y/X.

The numerical section does NOT substitute the physical Newtonian lapse for the
ADM lapse.  It only translates the condition into a threshold for an assumed
local PN ansatz n_4=C4 U^2, because the same-action family-I gate already proved
n_2=0.
"""
import json, math
import sympy as sp

# Exact symbolic branch derivation.
N,sqrtg,grr,psip,PX,CX,Y,X,Mpl2,rhop8=sp.symbols(
    'N sqrtg grr psip P_X C_X Y X Mpl2 rhop8',
    positive=True, finite=True, real=True)
# psip may have either sign; replace its positivity assumption locally.
ps=sp.symbols('psi_prime', finite=True, real=True)
flux=-N*sqrtg*grr*ps*(PX+CX*Y)
CX_fixed=-Mpl2/(2*X**2)
# Branch B condition PX+CX Y=0 with PX=Mpl2*P8X.
P8X=sp.symbols('P8_X', finite=True, real=True)
branchB=sp.simplify((Mpl2*P8X+CX_fixed*Y)*2*X/Mpl2)
assert sp.simplify(branchB-(2*X*P8X-Y/X))==0

# z=0 production enthalpy from the pinned scale dictionary.
mu=1.572550669049847e-4 # Mpc^-1
x0=0.8115162588884343
r0=0.0021346329644460586
enthalpy8=2*mu**2*x0*(1+r0)
threshold_a=math.sqrt(enthalpy8/2.0) # for psi'=0-like X~Theta^2/2,N~1: Y/X~2 a_N^2
assert enthalpy8>0 and threshold_a>0

# Conditional PN translation.  If n4=C4 U^2 around a point-mass exterior,
# |D n4| = 2 |C4| U |D U|.  This is ADM-lapse power counting, not physical
# matter-lapse substitution.
MPC_M=3.085677581491367e22
GM_sun_c2_m=1476.6250385
R_sun_m=6.957e8
AU_m=1.495978707e11
rows={}
for name,Rm in [('solar_surface',R_sun_m),('1_AU',AU_m)]:
    U=GM_sun_c2_m/Rm
    gradU=(GM_sun_c2_m/Rm**2)*MPC_M # Mpc^-1
    gradn_per_absC4=2*U*gradU
    C4_for_threshold=threshold_a/gradn_per_absC4
    rows[name]={
      'U':U,'gradU_Mpc_inv':gradU,
      'ADM_grad_n4_Mpc_inv_per_absC4_if_n4_eq_C4_U2':gradn_per_absC4,
      'absC4_for_ADM_grad_n4_equal_background_branchB_threshold':C4_for_threshold
    }
    assert C4_for_threshold>0

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_SPHERICAL_ZERO_FLUX_SCALAR_BRANCH_PASS',
 'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
 'assumptions':['static spherical geometry','zero invariant shift','Sigma=q t+psi(r)','regular stellar center / zero conserved radial scalar flux','X_U>0'],
 'conserved_flux':'F_r=-N sqrt(g) g^rr psi_prime [P_X+C_X Y] with Y=D_iTheta D^iTheta',
 'zero_flux_branches':[
   'A: psi_prime=0 (constant-q static clock branch)',
   'B: P_X+C_X Y=0'
 ],
 'fixed_C_derivative':'C_X=-M_Pl^2/(2 X^2)',
 'branch_B_exact_condition':'(rho+p)_8piG = Y/X',
 'z0_production':{'rho_plus_p_8piG_Mpc_inv2':enthalpy8,'sqrt_half_enthalpy_Mpc_inv':threshold_a},
 'conditional_PN_rows':rows,
 'interpretation':'A nontrivial regular zero-flux scalar profile is not freely adjustable: it must satisfy the exact algebraic branch-B condition in addition to the remaining gravity/U1 equations. Because the ADM lapse has n2=0, local relevance must be assessed from its O4 gradient, not from the physical Newtonian lapse gradient.',
 'non_claims':[
   'does not prove that branch B has a global regular solution',
   'does not exclude nonzero scalar flux/charge, relevant especially to black-hole boundary conditions',
   'does not solve the O4 ADM-lapse coefficient C4',
   'does not use the physical Newtonian gradient as the ADM-lapse gradient',
   'does not establish compact-object viability or failure'
 ],
 'next_gate':'combine the branch-B condition with the exact DBI P_X(u) and the solved/ bounded O4 ADM-lapse response; determine whether a regular stellar profile can remain inside the DBI domain without exponentially approaching its square-root edge, then extend to nonzero-flux black-hole boundary conditions'
}
open('u1_static_spherical_zero_flux_scalar_branch_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
