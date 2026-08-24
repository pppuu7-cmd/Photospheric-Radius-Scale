#!/usr/bin/env python3
"""C10 source-scope theorem: ordinary-only A filter, total metric/Ward momentum.

Preregistered target:
  research/theory_targets/RTK_C10_U1_TOTAL_MOMENTUM_SOURCE_SCOPE_TARGET_v1.json
"""
import json
from pathlib import Path
import sympy as sp

# Repository-level production guard: Khronon is a real momentum source.
src=Path('rtk/khronon_perturbations.c').read_text()
assert 's->momentum_class=(s->rho_class+s->p_class)*y->theta' in src
source_audit=Path('research/theory_results/RTK_C10_PRODUCTION_SOURCE_COMPOSITION_AUDIT_2026-08-24.md').read_text()
assert 'RTK/Khronon completion sector is neutral/unfiltered' in source_audit
assert 'baryons' in source_audit and 'photons' in source_audit and 'massless relativistic species' in source_audit

# Algebraic total-current audit.  P is ordinary-only projected A coefficient.
H,lam,G,a=sp.symbols('H lambda G a', nonzero=True, finite=True, real=True)
psi,phi,psip,lapB=sp.symbols('psi phi psi_prime lapB', finite=True, real=True)
q_ord,q_neutral=sp.symbols('q_ord q_neutral', finite=True, real=True)
qtot=sp.expand(q_ord+q_neutral)
lap=sp.symbols('lap', nonzero=True, finite=True, real=True)

# From A+Ward, before momentum substitution, the prepotential bracket is
# 2(psi'+H psi)-8 pi G a q_total.  The A-density part remains ordinary-only.
ward_bracket=sp.expand(2*(psip+H*psi)-8*sp.pi*G*a*qtot)
# Momentum equation sees exactly the same q_total.
momentum_total=sp.expand((3*lam-1)*(psip+H*phi)+(lam-1)*lapB)
reduced=sp.expand(ward_bracket.subs(8*sp.pi*G*a*qtot,momentum_total))
target=sp.expand(2*H*(psi-phi)+(1-lam)*(lapB+3*psip+3*H*phi))
assert sp.simplify(reduced-target)==0

# Neutral momentum cannot be dropped unless it is actually zero: doing so leaves
# a nonzero residual proportional to q_neutral.
wrong_bracket=sp.expand(2*(psip+H*psi)-8*sp.pi*G*a*q_ord)
# Replace q_ord using qtot-qneutral and then the total momentum equation.
wrong_rewritten=sp.expand(wrong_bracket.subs(q_ord,qtot-q_neutral))
wrong_after=sp.expand(wrong_rewritten.subs(8*sp.pi*G*a*qtot,momentum_total))
wrong_residual=sp.factor(wrong_after-target)
assert sp.simplify(wrong_residual-8*sp.pi*G*a*q_neutral)==0

out={
  'classification':'C10_U1_TOTAL_MOMENTUM_SOURCE_SCOPE_PASS_SCOPED',
  'status_scope':'GREEN_SOURCE_SPLIT_ORDINARY_A_FILTER_TOTAL_METRIC_AND_WARD_MOMENTUM',
  'A_source_density_scope':'P=H0_ordinary-Q; delta J_A=2 delta P. Baseline H0_ordinary is baryons+photons+massless relativistic species. Neutral Khronon is not inserted into P.',
  'metric_momentum_scope':'q_total=q_ordinary+q_Khronon at baseline; add physical massive-neutrino momentum only in the separate B4 same-action extension.',
  'production_guard':'rtk/khronon_perturbations.c has momentum_class=(rho_class+p_class)*theta, so a generic Khronon perturbation carries metric momentum.',
  'Ward_identity_total':'J_varphi=[Dt(J_A)-div(J_A N^i)]/(2N)-div(N J^i_total)/N',
  'linear_flat_FLRW':'delta J_varphi=a^-1[(delta P)\u0027+3H delta P-a^-1 partial^2 q_total]',
  'redundancy_scope_correction':'In RTK_C10_U1_LINEAR_WARD_CONSTRAINT_REDUCTION_RESULT_v1.json, q must be interpreted as total metric momentum q_total, exactly as in primary Eq.(7.12). With that interpretation the symbolic residual remains zero for arbitrary neutral-sector q_Khronon.',
  'dropped_neutral_momentum_residual':'If q_Khronon is omitted from the Ward source while Eq.(7.12) uses q_total, the prepotential identity acquires residual +8 pi G a q_Khronon and is generically false.',
  'stress_scope_for_next_gate':'Hamiltonian/momentum/trace/traceless equations use total gravitating density, momentum, pressure and anisotropic stress. Only the A-source density filter P is ordinary-only under the frozen baseline contract.',
  'non_claims':[
    'does not add massive-neutrino B4 sources',
    'does not close Hamiltonian or dynamical metric equations',
    'does not prove a new nonlinear RTK stress tensor beyond the frozen action/production architecture',
    'does not implement CLASS or change likelihood results'
  ],
  'target':'research/theory_targets/RTK_C10_U1_TOTAL_MOMENTUM_SOURCE_SCOPE_TARGET_v1.json'
}
Path('u1_total_momentum_source_scope_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
