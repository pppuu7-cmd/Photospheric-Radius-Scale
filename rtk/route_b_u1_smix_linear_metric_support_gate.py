#!/usr/bin/env python3
"""C10 principal quadratic metric support of the frozen U1-invariant S_mix.

This is a local-rest/two-derivative principal theorem, not a full cosmological
source map.  It freezes the exact lapse-kernel bookkeeping needed before CLASS.
"""
import json
from pathlib import Path
import sympy as sp

C,q,u,phi,k2,Mpl,zeta2=sp.symbols('C q u phi k2 M_Pl zeta2', positive=True, finite=True, real=True)
lam,H=sp.symbols('lambda H', positive=True, finite=True, real=True)

# Homogeneous rolling background: D_i Sigma_bar=0.  To first principal order
# the invariant normal velocity perturbation is deltaTheta=u-q*phi.
dTheta=u-q*phi
L2=sp.expand(C*k2*dTheta**2)  # positive homogeneous measure suppressed

# Quadratic coefficients/support.
phi2_coeff=sp.expand(L2).coeff(phi,2)
cross_coeff=sp.expand(L2).coeff(phi,1).coeff(u,1)
u2_coeff=sp.expand(L2).coeff(u,2)
assert phi2_coeff==C*k2*q**2
assert cross_coeff==-2*C*k2*q
assert u2_coeff==C*k2

# No principal B, psi, A, nu variables occur in this reduced homogeneous-background expression.
B,psi,A,nu=sp.symbols('B psi A nu')
for v in (B,psi,A,nu):
    assert not L2.has(v)

# Exact RTK matching C q^2=M_Pl^2.
phi2_matched=sp.simplify(phi2_coeff.subs(C,Mpl**2/q**2))
assert phi2_matched==Mpl**2*k2

# Pure U1 gravity quadratic lapse term is zeta^2 beta0 k^2 phi^2,
# with zeta^2=M_Pl^2/2.  Thus S_mix corresponds to beta0_eff=2.
beta_eff=sp.simplify(phi2_matched/(Mpl**2*sp.Rational(1,2)*k2))
assert beta_eff==2

# Corrected full-action bookkeeping has beta0_bare=0, so two-derivative IR
# full principal lapse kernel is Eth_IR_full=2.
EthIR=sp.Integer(2)
D=3*lam-1
r=lam-1
k=sp.symbols('k', positive=True, finite=True, real=True)
# C10 minimal metric-reduction Fourier lapse denominator:
den=sp.expand(-(r*EthIR*k**2+2*D*H**2))
expected=-2*r*k**2-2*D*H**2
assert sp.simplify(den-expected)==0
# Under lambda>1,H>=0,k>0 every term in -den is positive. Symbolically expose it.
positive_core=sp.expand(-den/2)
assert sp.simplify(positive_core-(r*k**2+D*H**2))==0

out={
  'classification':'C10_SMIX_LINEAR_METRIC_SUPPORT_AND_IR_LAPSE_KERNEL_PASS_SCOPED',
  'status_scope':'GREEN_LOCAL_REST_TWO_DERIVATIVE_PRINCIPAL_SMIX_SUPPORT_FULL_FLRW_SOURCE_MAP_OPEN',
  'principal_delta_Theta':'u-q phi on D_i Sigma_bar=0; lower-derivative qdot*pi pieces are outside this principal gate',
  'principal_quadratic_kernel':'C k_phys^2 (u-q phi)^2',
  'metric_support':'At this quadratic principal order the homogeneous-background S_mix has direct lapse support through phi, while direct B, psi, A and nu dependence is absent.',
  'lapse_phi2_coefficient_before_matching':'C q^2 k_phys^2',
  'exact_RTK_match':'C q^2=M_Pl^2',
  'lapse_phi2_coefficient_after_matching':'M_Pl^2 k_phys^2',
  'gravity_comparison':'zeta^2 beta0_eff k_phys^2 phi^2 with zeta^2=M_Pl^2/2 gives beta0_eff_from_Smix=2',
  'corrected_bare_plus_mixed':'beta0_bare=0 plus explicit S_mix gives Eth_IR_full=2 in the two-derivative local-rest principal truncation',
  'IR_lapse_denominator':'for lambda_HL>1 and k>0: -[2(lambda-1)k^2+2(3lambda-1)H^2] < 0, hence no lapse-solve pole in this scoped IR principal truncation',
  'unresolved_cross_source':'The cross term is -2 C q k_phys^2 u phi; its mapping to the completed-action scalar/lapse source variables is mandatory before a CLASS implementation.',
  'non_claims':[
    'not a full FLRW lower-derivative expansion when q varies with time',
    'not a theorem for higher-spatial-derivative Eth(k)',
    'not a completed-action delta_mu/source dictionary',
    'not a CLASS or likelihood result',
    'not nonlinear perturbation closure'
  ],
  'target':'research/theory_targets/RTK_C10_SMIX_LINEAR_METRIC_SUPPORT_TARGET_v1.json'
}
Path('u1_smix_linear_metric_support_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
