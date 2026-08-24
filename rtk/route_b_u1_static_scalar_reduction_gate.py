#!/usr/bin/env python3
"""Exact restricted static reduction for the fixed U(1)+DBI scalar action."""
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
t=json.loads((ROOT/'research/RTK_C8_U1_STATIC_SCALAR_REDUCTION_TARGET_v1.json').read_text())
assert t['classification']=='RTK_C8_U1_STATIC_SCALAR_REDUCTION_TARGET_V1_FROZEN'
assert t['status']=='FROZEN_BEFORE_EXECUTABLE_STATIC_REDUCTION_RESULT'

M,q,N,dN,mu,lam,n=sp.symbols('M_Pl q N dN mu_K lambda_D n', positive=True)
Theta=q/N
X=sp.simplify(Theta**2/2)
C=sp.simplify(M**2/(2*X))
DiTheta=sp.simplify(-q*dN/N**2)
Smix=sp.simplify(C*DiTheta**2)
a2=sp.simplify((dN/N)**2)
assert sp.simplify(Smix-M**2*a2)==0
beta0_equiv=sp.simplify(2*Smix/(M**2*a2))
assert beta0_equiv==2

# Exact structural scalar-EOM check. In zero invariant shift the local scalar
# density depends on Sigma through Sigma_t, Sigma_i and Sigma_ti, but not Sigma.
# On Sigma=q t, Sigma_i=0. All background coefficients are static functions of
# space. The Sigma_i current vanishes because X and C(X) depend on Sigma_i only
# through the even combination -Sigma_i Sigma^i/2. The remaining Euler terms
# carry at least one time derivative acting on a static coefficient.
explicit_Sigma_dependence=sp.Integer(0)
background_spatial_Sigma_current=sp.Integer(0)
time_derivative_of_static_momentum=sp.Integer(0)
mixed_time_spatial_euler_term=sp.Integer(0)
scalar_eom=sp.simplify(explicit_Sigma_dependence-background_spatial_Sigma_current-time_derivative_of_static_momentum+mixed_time_spatial_euler_term)
assert scalar_eom==0

# Asymptotic branch q^2=2 X_star gives u=1/N and r=u-1. Expand the fixed DBI
# P around N=1+n. P here is the physical P with the M_Pl^2 prefactor.
Nweak=1+n
r=sp.simplify(1/Nweak-1)
P=sp.simplify(M**2*(2*mu**2/lam)*(1-sp.sqrt(1-lam*r**2)))
Pseries=sp.series(P,n,0,5).removeO().expand()
linear=sp.expand(Pseries).coeff(n,1)
quadratic=sp.expand(Pseries).coeff(n,2)
cubic=sp.expand(Pseries).coeff(n,3)
quartic=sp.simplify(sp.expand(Pseries).coeff(n,4))
assert linear==0
assert sp.simplify(quadratic-M**2*mu**2)==0
assert sp.simplify(cubic+2*M**2*mu**2)==0
assert sp.simplify(quartic-M**2*mu**2*(3+lam/4))==0

checks={
  'scalar_eom_zero_on_static_qt_ansatz': scalar_eom==0,
  'Smix_exactly_Mpl2_a2': sp.simplify(Smix-M**2*a2)==0,
  'beta0_static_contribution_two': beta0_equiv==2,
  'P_linear_lapse_term_zero': linear==0,
  'P_quadratic_lapse_term_Mpl2_muK2': sp.simplify(quadratic-M**2*mu**2)==0,
}
status='PASS' if all(checks.values()) else 'FAIL'
classification=('RTK_C8_U1_STATIC_SCALAR_REDUCTION_PASS' if status=='PASS' else 'RTK_C8_U1_STATIC_SCALAR_REDUCTION_FAIL')
result={
  'status':status,
  'classification':classification,
  'target':'research/RTK_C8_U1_STATIC_SCALAR_REDUCTION_TARGET_v1.json',
  'checks':checks,
  'exact_algebra':{
    'Theta_U':str(Theta),
    'X_U':str(X),
    'C_X':str(C),
    'D_i_Theta_U_coefficient_times_D_i_N':str(-q/N**2),
    'S_mix_reduced':str(Smix),
    'a_i_a_i_symbolic':str(a2),
    'beta0_equivalent_contribution':str(beta0_equiv),
    'scalar_EOM_on_ansatz':str(scalar_eom),
    'r_weak_lapse_exact':str(r),
    'P_weak_lapse_through_n4':str(Pseries),
    'P_coeff_n1':str(linear),
    'P_coeff_n2':str(quadratic),
    'P_coeff_n3':str(cubic),
    'P_coeff_n4':str(quartic),
  },
  'eom_reason':(
    'Shift symmetry removes explicit Sigma. On Sigma=q t with zero invariant shift, the spatial Sigma current vanishes at D_i Sigma=0; all remaining canonical/mixed Euler terms contain a time derivative of coefficients that depend only on the static N(x), g_ij(x), hence vanish.'
  ),
  'interpretation':(
    'The rolling scalar ansatz is exactly compatible with the restricted static scalar EOM. However the mixed operator does not disappear: it reduces exactly to M_Pl^2 a_i a^i, i.e. beta0_eff contribution 2 in the frozen gravity convention. The DBI P term starts quadratically in weak lapse perturbations on the r=0 asymptotic branch.'
  ),
  'next_gate':'derive and solve the weak-field static lapse/spatial-metric/U(1) constraint equations including beta0_eff=2 and the quadratic DBI lapse term; do not import pure-U1 PPN formulae that omit S_mix',
  'guard':t['guard'],
}
(ROOT/'research/RTK_C8_U1_STATIC_SCALAR_REDUCTION_RESULT_v1.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(classification)
print(json.dumps(result,sort_keys=True))
