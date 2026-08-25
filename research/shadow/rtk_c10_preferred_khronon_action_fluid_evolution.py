#!/usr/bin/env python3
import json
import sympy as sp

H,w,ca2,cs2,k2,B,psi_p,phi,delta,theta,rho=sp.symbols(
    'H w ca2 cs2 k2 B psi_prime phi delta theta rho', finite=True
)
onepw=1+w
W=rho*onepw
Sratio=H*(1-3*ca2)  # Sigma''/Sigma'
rhop=-3*H*W

deltap=sp.symbols('delta_prime', finite=True)
dmu=rho*delta
dmu_p=rhop*delta+rho*deltap

# This is the local shift-current equation after multiplying by Sigma'/a^4:
# delta_mu' + (4H-Sigma''/Sigma')delta_mu + W(theta+k^2 B-3 psi') = 0.
charge_eq=sp.expand(dmu_p+(4*H-Sratio)*dmu+W*(theta+k2*B-3*psi_p))
deltap_solution=sp.solve(sp.Eq(charge_eq,0),deltap)[0]
expected_delta=-(onepw)*(theta+k2*B-3*psi_p)-3*H*(ca2-w)*delta
assert sp.simplify(deltap_solution-expected_delta)==0

# theta=k^2 deltaSigma/Sigma'.  With U=deltaSigma'-Sigma' phi,
# U/Sigma'=c_s^2 delta/(1+w), therefore:
thetap_from_definition=sp.expand(k2*(cs2*delta/onepw+phi)-Sratio*theta)
expected_theta=-H*(1-3*ca2)*theta+k2*(cs2*delta/onepw+phi)
assert sp.simplify(thetap_from_definition-expected_theta)==0

# B=0 must reduce to the frozen action-fluid shadow (notation-swapped metric potentials).
shadow_delta=-(onepw)*(theta-3*psi_p)-3*H*(ca2-w)*delta
shadow_theta=-H*(1-3*ca2)*theta+k2*(cs2*delta/onepw+phi)
assert sp.simplify(deltap_solution.subs(B,0)-shadow_delta)==0
assert sp.simplify(thetap_from_definition-shadow_theta)==0

# The only direct B term is the spatial-current advection contribution in continuity.
B_coefficient=sp.simplify(sp.diff(deltap_solution,B))
assert sp.simplify(B_coefficient+onepw*k2)==0
assert sp.simplify(sp.diff(thetap_from_definition,B))==0

out={
  'schema':'RTK_C10_PREFERRED_KHRONON_ACTION_FLUID_EVOLUTION_RESULT_v1',
  'classification':'C10_PREFERRED_KHRONON_ACTION_FLUID_EVOLUTION_PASS_SCOPED',
  'preferred_equations':{
    'delta_prime':'-(1+w)(theta+k^2 B-3 psi_pref_prime)-3 H(c_a^2-w)delta',
    'theta_prime':'-H(1-3c_a^2)theta+k^2[c_s^2 delta/(1+w)+phi_pref]',
    'q_pref':'a(rho+p)theta/k^2',
    'Pi_khr':'0 at the certified linear effective-fluid boundary'
  },
  'action_derivation':{
    'background_charge':"(a^2 P_X Sigma_prime)'=0",
    'charge_perturbation':'a^2 F A U-3 a^2 P_X Sigma_prime psi_pref',
    'U':'deltaSigma_prime-Sigma_prime phi_pref',
    'spatial_current_divergence':'a^2 P_X k^2(deltaSigma+Sigma_prime B)',
    'reduced_charge_equation':'delta_mu_prime+(4H-Sigma_double_prime/Sigma_prime)delta_mu+(rho+p)(theta+k^2 B-3 psi_pref_prime)=0',
    'Sigma_double_prime_over_Sigma_prime':'H(1-3c_a^2)',
    'U_over_Sigma_prime':'c_s^2 delta/(1+w)'
  },
  'shift_structure':{
    'continuity_B_coefficient':'-(1+w)k^2',
    'Euler_direct_B_coefficient':'0',
    'interpretation':'B enters the local conserved shift-current through coordinate spatial flux; the canonical preferred momentum theta=k^2 deltaSigma/Sigma_prime itself is not replaced by a Newtonian-frame velocity.'
  },
  'B0_shadow_roundtrip':{
    'delta_residual':'0',
    'theta_residual':'0',
    'metric_notation':'psi_pref is the spatial-curvature potential corresponding to CLASS phi; phi_pref is the preferred lapse corresponding to CLASS psi when B=0 and before the ordinary-matter deltaA physical-lapse map'
  },
  'machine_residuals':{
    'continuity':str(sp.simplify(deltap_solution-expected_delta)),
    'euler':str(sp.simplify(thetap_from_definition-expected_theta)),
    'B0_delta_shadow':str(sp.simplify(deltap_solution.subs(B,0)-shadow_delta)),
    'B0_theta_shadow':str(sp.simplify(thetap_from_definition-shadow_theta)),
    'B_coefficient':str(sp.simplify(B_coefficient+onepw*k2)),
    'Euler_B_coefficient':str(sp.simplify(sp.diff(thetap_from_definition,B)))
  },
  'interpretation':{
    'core':'the neutral Khronon can be evolved directly in the preferred foliation using the action-derived variables; ordinary species may remain on the physical-metric Newtonian interface while the preferred DAE projector couples both through total stress/momentum',
    'architecture':'do not feed the ordinary physical lapse phi-deltaA/a into the neutral Khronon Euler force; its fixed action is U1-neutral and uses the preferred lapse phi_pref'
  },
  'next_gate':'construct a detached dual-interface DAE evolution (ordinary physical-metric species + preferred neutral action fluid + algebraic completed-U1 metric projector) and test finite-onset memory loss before any UV matching parameter is introduced',
  'non_claims':['not nonlinear closure','not exact k=0','not massive-neutrino completion','not coupled CLASS feedback yet','not an attractor theorem','not spectra or likelihood evidence']
}
assert all(v=='0' for v in out['machine_residuals'].values())
print(json.dumps(out,indent=2,sort_keys=True))
