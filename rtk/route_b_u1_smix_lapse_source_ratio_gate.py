#!/usr/bin/env python3
"""C10 exact rolling-background S_mix lapse-source / inertia ratio theorem.

Preregistered target:
  research/theory_targets/RTK_C10_SMIX_LAPSE_SOURCE_RATIO_TARGET_v1.json

This gate is deliberately convention-narrow.  It proves a ratio inside the
quadratic scalar action before any final mapping to the normalized U1
Hamiltonian or CLASS source convention.
"""
import json
from pathlib import Path
import sympy as sp

q,PX,PXX,C,k2,y,phi,pidot=sp.symbols(
    'q P_X P_XX C k_phys_sq y phi pi_dot',
    positive=True, finite=True, real=True
)
# y is introduced as pi_dot-phi; keep a replacement form for differentiation.
y_expr=pidot-phi
K=sp.factor(q**2*(PX+q**2*PXX))
MK2=sp.factor(K/(2*C*q**2))
assert sp.simplify(MK2-(PX+q**2*PXX)/(2*C))==0

# Pure P(X) density response: rho=2 X P_X-P, X=q^2/2, deltaTheta=q*y.
# d rho / d Theta = q(P_X+q^2 P_XX), hence delta rho = K*y.
delta_rho=sp.factor(K*y_expr)
L2_dbi=sp.Rational(1,2)*K*y_expr**2
L2_mix=C*q**2*k2*y_expr**2
L2=sp.expand(L2_dbi+L2_mix)

# Lapse functional derivative at fixed pi_dot.  Since dy/dphi=-1, the
# positive source-like coefficient is -dL/dphi.
lapse_fd=sp.factor(-sp.diff(L2,phi))
expected=sp.factor(K*y_expr*(1+k2/MK2))
assert sp.simplify(lapse_fd-expected)==0
ratio=sp.factor(lapse_fd/delta_rho)
assert sp.simplify(ratio-(1+k2/MK2))==0

# The y^2 inertia is enhanced by the identical factor.
K_eff=sp.factor(sp.diff(L2,pidot,2))
assert sp.simplify(K_eff-K*(1+k2/MK2))==0

# If the unmixed spatial gradient is -(K*c_a^2*k^2/2) pi^2, the isolated
# scalar dispersion is omega^2=c_a^2 k^2/(1+k^2/MK^2).
ca2,omega2=sp.symbols('c_a_sq omega_sq', positive=True, finite=True, real=True)
omega_expected=sp.factor(ca2*k2/(1+k2/MK2))
assert sp.simplify(K_eff*omega_expected-K*ca2*k2)==0

out={
  'classification':'C10_SMIX_LAPSE_SOURCE_RATIO_AND_RATIONAL_INERTIA_PASS_SCOPED',
  'status_scope':'GREEN_EXACT_QUADRATIC_ACTION_RATIO_FINAL_U1_CLASS_SOURCE_NORMALIZATION_OPEN',
  'K_pi':'q^2(P_X+q^2 P_XX)',
  'M_K_squared':'K_pi/(2 C q^2)',
  'delta_rho_DBI':'K_pi (pi_dot-phi)',
  'scalar_lapse_functional_derivative':'-dL2_scalar/dphi = delta_rho_DBI [1+k_phys^2/M_K^2]',
  'lapse_ratio_to_pure_DBI_density':'1+k_phys^2/M_K^2',
  'effective_quadratic_inertia':'K_pi [1+k_phys^2/M_K^2]',
  'isolated_scalar_dispersion':'omega^2=c_a^2 k_phys^2/[1+k_phys^2/M_K^2]',
  'interpretation':'The same mixed operator responsible for the rational scalar inertia also changes the scalar-sector lapse functional derivative at fixed field perturbation by the identical rational-inertia factor. Therefore changing only c_s^2(k) in a phenomenological fluid implementation is not, by itself, a proof of equivalence to the completed action metric sourcing.',
  'non_claims':[
    'does not prescribe multiplying an existing CLASS delta_rho source by this factor without the full reduced U1 normalization',
    'does not include lower-derivative FLRW q-dot terms',
    'does not derive nonlinear stress or anisotropic stress',
    'does not include the separate B4 massive-neutrino extension'
  ],
  'target':'research/theory_targets/RTK_C10_SMIX_LAPSE_SOURCE_RATIO_TARGET_v1.json'
}
Path('u1_smix_lapse_source_ratio_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
