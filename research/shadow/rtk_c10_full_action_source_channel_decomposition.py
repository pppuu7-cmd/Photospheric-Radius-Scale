#!/usr/bin/env python3
import json
import sympy as sp

# --- Ordinary universal-matter + elliptic-compensator reduced channel ---
N,A,nudot,nux,Ni,H0,Hi,ell=sp.symbols('N A nudot nux Ni H0 Hi ell', nonzero=True, finite=True)
aeff=1-1/ell
Acal=-nudot+Ni*nux+sp.Rational(1,2)*N*nux**2
Hm=sp.expand((N-aeff*(A-Acal))*H0+(Ni+N*nux)*Hi)
Hm_reg=sp.simplify(Hm.subs({nux:0,Ni:0}))
Hperp=sp.simplify(sp.diff(Hm_reg,N))
JA=sp.simplify(sp.diff(Hm,A))
pnu=sp.simplify(-sp.diff(Hm,nudot))
assert sp.simplify(Hperp-H0)==0
assert sp.simplify(JA+aeff*H0)==0
assert sp.simplify(pnu-aeff*H0)==0
assert sp.simplify(JA+pnu)==0

# --- Neutral action-fluid versus historical production-GDM source/evolution ---
rho,w,cs2,ca2,H,k,delta,theta,phi_p,psi=sp.symbols(
    'rho w cs2 ca2 H k delta theta phi_p psi', nonzero=True, finite=True
)
onepw=1+w
p_action_over_rho=cs2*delta
p_prod_over_rho=cs2*delta+3*H*onepw*(cs2-ca2)*theta/k**2
pressure_difference=sp.factor(p_prod_over_rho-p_action_over_rho)
expected_pressure_difference=3*H*onepw*(cs2-ca2)*theta/k**2
assert sp.simplify(pressure_difference-expected_pressure_difference)==0

delta_action=-(onepw)*(theta-3*phi_p)-3*H*(ca2-w)*delta
theta_action=-H*(1-3*ca2)*theta+k**2*(cs2*delta/onepw+psi)
delta_prod=-(onepw)*(theta-3*phi_p)-3*H*(cs2-w)*delta-9*H**2*onepw*(cs2-ca2)*theta/k**2
theta_prod=-H*(1-3*cs2)*theta+k**2*(cs2*delta/onepw+psi)

delta_diff=sp.factor(delta_prod-delta_action)
theta_diff=sp.factor(theta_prod-theta_action)
expected_delta_diff=-3*H*(cs2-ca2)*(delta+3*H*onepw*theta/k**2)
expected_theta_diff=3*H*(cs2-ca2)*theta
assert sp.simplify(delta_diff-expected_delta_diff)==0
assert sp.simplify(theta_diff-expected_theta_diff)==0

# Exact common limit.
assert sp.simplify(pressure_difference.subs(cs2,ca2))==0
assert sp.simplify(delta_diff.subs(cs2,ca2))==0
assert sp.simplify(theta_diff.subs(cs2,ca2))==0

out={
  'schema':'RTK_C10_FULL_ACTION_SOURCE_CHANNEL_DECOMPOSITION_RESULT_v1',
  'classification':'C10_FULL_ACTION_SOURCE_CHANNEL_DECOMPOSITION_PASS_PROJECTOR_SOURCE_REWIRE_REQUIRED_SCOPED',
  'ordinary_elliptic_channel':{
    'reduced_Hamiltonian':'[N-a_eff(A-Acal)] H0 + (N^i+N D^i nu) H_i',
    'a_eff':'1-1/ell = k_phys^2/(M_c^2+k_phys^2)',
    'regular_slice_Hperp':'H0',
    'J_A':'-a_eff H0',
    'p_nu':'+a_eff H0',
    'gauge_pair_residual':str(sp.simplify(JA+pnu)),
    'metric_stress_rule':'do not multiply ordinary delta_mu, q, delta_p or Pi by a_eff; the elliptic filter belongs to the A/prepotential gauge-pair channel'
  },
  'neutral_khronon_action_channel':{
    'U1_A_source':'zero direct A-source; its momentum still belongs to total q/Ward channel',
    'delta_mu':'rho_khr * delta_action',
    'delta_p':'rho_khr * c_s^2 * delta_action',
    'momentum':'(rho_khr+p_khr) theta_action',
    'Pi':'0 at the certified linear effective-fluid boundary',
    'evolution_delta_prime':'-(1+w)(theta-3 phi_prime)-3 H(c_a^2-w)delta',
    'evolution_theta_prime':'-H(1-3 c_a^2)theta+k^2[c_s^2 delta/(1+w)+psi]',
    'metric_scope_guard':'the preferred-coordinate forcing/shift convention still requires a dedicated derivation before coupled feedback'
  },
  'historical_production_difference':{
    'pressure_prod_minus_action_over_rho':str(pressure_difference),
    'delta_prime_prod_minus_action':str(delta_diff),
    'theta_prime_prod_minus_action':str(theta_diff),
    'common_limit_cs2_equals_ca2':'all three residuals vanish exactly',
    'interpretation':'production-GDM source histories are excellent historical diagnostics but are not the final same-action neutral source provider'
  },
  'completed_projector_contract':{
    'ordinary_metric_stress':'physical ordinary species stress transformed to the preferred source representation',
    'ordinary_A_filter':'ordinary-only deltaH0 through a_eff',
    'neutral_metric_stress':'action-derived Khronon effective stress, not production-GDM stress',
    'Ward_momentum':'total q = q_ordinary + q_neutral',
    'projector':'retain C10.52 A->Hamiltonian->momentum algebra; rewire source/evolution provider before feedback'
  },
  'machine_residuals':{
    'regular_Hperp_minus_H0':str(sp.simplify(Hperp-H0)),
    'JA_plus_a_eff_H0':str(sp.simplify(JA+aeff*H0)),
    'pnu_minus_a_eff_H0':str(sp.simplify(pnu-aeff*H0)),
    'JA_plus_pnu':str(sp.simplify(JA+pnu)),
    'pressure_difference_formula':str(sp.simplify(pressure_difference-expected_pressure_difference)),
    'delta_evolution_difference_formula':str(sp.simplify(delta_diff-expected_delta_diff)),
    'theta_evolution_difference_formula':str(sp.simplify(theta_diff-expected_theta_diff))
  },
  'next_gate':'derive neutral P(X_U)+S_mix perturbation evolution directly in preferred quasilongitudinal variables, including the shift/momentum definition, and prove the B=0 reduction equals the certified action-fluid shadow',
  'non_claims':[
    'not a preferred-coordinate neutral evolution theorem',
    'not a completed-U1 CLASS implementation',
    'not nonlinear S_mix stress',
    'not a massive-neutrino extension',
    'not spectra or likelihood evidence'
  ]
}
assert all(v=='0' for v in out['machine_residuals'].values())
print(json.dumps(out,indent=2,sort_keys=True))
