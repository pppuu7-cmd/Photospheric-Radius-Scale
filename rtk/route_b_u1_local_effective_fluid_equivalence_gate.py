#!/usr/bin/env python3
"""C10 local/frozen-background effective-fluid equivalence theorem.

This theorem asks whether the full-action lapse-source density definition and
mixed-inertia scalar EOM reproduce the same principal perfect-fluid closure as
the phenomenological RTK fluid.  It deliberately excludes expanding-FLRW
coefficient derivatives and metric forcing.
"""
import json
from pathlib import Path
import sympy as sp

K,ca2,k2,F,pi,pid,pidd=sp.symbols(
    'K_pi c_a_sq k_phys_sq F pi pi_dot pi_double_dot',
    positive=True, finite=True, real=True
)
# Frozen rational inertia factor.
cs2=sp.factor(ca2/F)
dmu=sp.factor(F*K*pid)
rhop=sp.factor(ca2*K)
qmom=sp.factor(rhop*pi)
dp=sp.factor(ca2*K*pid)
assert sp.simplify(dp-cs2*dmu)==0

# Scalar EOM in the metric-free locally frozen background.
eom=sp.Eq(F*K*pidd + ca2*K*k2*pi,0)
pidd_sol=sp.factor(-ca2*k2*pi/F)

# Time derivatives on frozen coefficients.
dmu_dot=sp.factor(F*K*pidd_sol)
q_dot=sp.factor(rhop*pid)
continuity=sp.simplify(dmu_dot+k2*qmom)
euler=sp.simplify(q_dot-dp)
assert continuity==0
assert euler==0

omega2=sp.factor(ca2*k2/F)
assert sp.simplify(omega2-cs2*k2)==0

out={
  'classification':'C10_LOCAL_FULL_ACTION_EFFECTIVE_FLUID_EQUIVALENCE_PASS_SCOPED',
  'status_scope':'GREEN_LOCALLY_FROZEN_PRINCIPAL_FLUID_EQUIVALENCE_FULL_FLRW_LOWER_DERIVATIVE_TERMS_OPEN',
  'F':'1+k_phys^2/M_K^2',
  'delta_mu_eff':'F K_pi pi_dot',
  'rho_plus_p':'c_a^2 K_pi',
  'q_momentum':'(rho+p) pi',
  'delta_p':'c_a^2 K_pi pi_dot = c_s^2 delta_mu_eff',
  'c_s_squared':'c_a^2/F',
  'continuity_principal':'dot(delta_mu_eff)+k_phys^2 q_momentum=0',
  'euler_principal':'dot(q_momentum)=delta_p',
  'dispersion':'omega^2=c_s^2 k_phys^2',
  'interpretation':'Once the perturbation density is defined by the lapse variation of the full P(X)+S_mix action, the same rational inertia factor that enhances the lapse source converts the bare DBI pressure response into the production scale-dependent sound speed. On a locally frozen background, the full-action scalar exactly admits the standard perfect-fluid principal continuity/Euler form. The earlier source-ratio warning therefore does not by itself imply a production-source mismatch.',
  'next_gate':'derive the expanding-FLRW lower-derivative terms, including time derivatives of F, K_pi, q and metric forcing, and compare them term-by-term with rtk/khronon_perturbations.c',
  'non_claims':[
    'not a proof of the exact Hubble/friction/entropy terms in khronon_perturbations.c',
    'not a CLASS likelihood validation',
    'not a nonlinear stress tensor theorem',
    'not a B4 massive-neutrino extension'
  ],
  'target':'research/theory_targets/RTK_C10_LOCAL_EFFECTIVE_FLUID_EQUIVALENCE_TARGET_v1.json'
}
Path('u1_local_effective_fluid_equivalence_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
