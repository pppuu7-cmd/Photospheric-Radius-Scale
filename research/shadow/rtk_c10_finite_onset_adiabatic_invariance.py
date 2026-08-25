#!/usr/bin/env python3
import json
import sympy as sp

H,B,a=sp.symbols('H B a', nonzero=True)
rhoi,rhoj,wi,wj=sp.symbols('rho_i rho_j w_i w_j', nonzero=True)
driN,drjN,qiN,qjN=sp.symbols('dr_i_N dr_j_N q_i_N q_j_N')

rhip_i=-3*H*rhoi*(1+wi)
rhip_j=-3*H*rhoj*(1+wj)
Wi=rhoi*(1+wi); Wj=rhoj*(1+wj)

driP=driN-rhip_i*B
drjP=drjN-rhip_j*B
qiP=qiN-a*Wi*B
qjP=qjN-a*Wj*B

entropy_res=sp.simplify((driP/rhip_i-drjP/rhip_j)-(driN/rhip_i-drjN/rhip_j))
baro_i_res=sp.simplify((driP/rhoi)/(1+wi)-((driN/rhoi)/(1+wi)+3*H*B))
baro_j_res=sp.simplify((drjP/rhoj)/(1+wj)-((drjN/rhoj)/(1+wj)+3*H*B))
vel_res=sp.simplify((qiP/(a*Wi)-qjP/(a*Wj))-(qiN/(a*Wi)-qjN/(a*Wj)))
common_i_res=sp.simplify(qiP/(a*Wi)-(qiN/(a*Wi)-B))
common_j_res=sp.simplify(qjP/(a*Wj)-(qjN/(a*Wj)-B))

assert entropy_res==0
assert baro_i_res==0 and baro_j_res==0
assert vel_res==0 and common_i_res==0 and common_j_res==0

out={
  'schema':'RTK_C10_FINITE_ONSET_ADIABATIC_INVARIANCE_RESULT_v1',
  'classification':'C10_FINITE_ONSET_ADIABATIC_INVARIANCE_PASS_UV_OR_GROWING_MODE_MATCH_REQUIRED_SCOPED',
  'machine_residuals':{
    'relative_entropy':str(entropy_res),
    'barotropic_i':str(baro_i_res),
    'barotropic_j':str(baro_j_res),
    'relative_velocity':str(vel_res),
    'velocity_shift_i':str(common_i_res),
    'velocity_shift_j':str(common_j_res)
  },
  'identities':{
    'density_time_shift':'delta_rho_pref/rho_prime=delta_rho_N/rho_prime-B',
    'barotropic':'delta_pref/(1+w)=delta_N/(1+w)+3 H B',
    'velocity':'v_pref=v_N-B, v=q/[a(rho+p)]'
  },
  'combined_with_prior':{
    'C10_53':'leading finite-B constraint is total comoving regularity and does not determine B0',
    'C10_54':'B0=[C2+2 Pcal psi0-Eth phi0]/(2H); C2 is source-coordinate invariant'
  },
  'interpretation':{
    'core':'instantaneous finite-onset adiabatic relative-density and common-velocity conditions are exactly blind to the common preferred-foliation time shift B',
    'boundary_data':'adiabaticity plus leading regularity cannot manufacture C2 or B0; one needs temporal growing-mode/attractor selection or pre-EFT/UV matching',
    'dof_guard':'this is a finite-onset boundary-data statement, not evidence for an extra propagating scalar or physical isocurvature mode'
  },
  'next_gate':'test in-EFT attractor/memory loss before introducing any arbitrary UV matching parameter',
  'non_claims':['no numerical C2 or B0','no UV completion selected','no completed-U1 CLASS feedback','not exact k=0','no spectra or likelihood result']
}
print(json.dumps(out,indent=2,sort_keys=True))
