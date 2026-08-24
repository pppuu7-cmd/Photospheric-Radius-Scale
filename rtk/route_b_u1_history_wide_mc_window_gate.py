#!/usr/bin/env python3
"""Exact history-wide sufficient M_c compatibility window for the elliptic U(1) completion.

Frozen parents establish, in their common controlled domain,

  M_c^2 >= rho_filtered/(32 eta0 M_Pl^2)                  (radiation-conservative all-q bound)
  rho_eff = (3/2)(3 lambda_HL-1) M_Pl^2 H^2             (flat same-action normalization)
  M_c^2 >= 99 k_cos_phys^2                               (>=99% cosmological compensation)
  M_c^2 <= k_local_phys^2/99                             (<=1% local compensation)

This v1 theorem assumes rho_filtered <= rho_eff throughout a declared EFT history interval
and H(a) <= H_EFT there. It derives a sufficient history-wide lower bound and its exact
compatibility with the scale-separation upper bound. It does not select any parameter.
"""
import json
import sympy as sp

# Positive-domain symbols. lambda_HL=1+epsilon guarantees the certified lambda_HL>1 branch.
eps, eta0, H, HEFT, kcos, klocal, Mpl2 = sp.symbols(
    'epsilon eta0 H H_EFT k_cos_phys k_local_phys M_Pl_squared', positive=True, finite=True
)
lam = 1 + eps
rho_f, rho_eff = sp.symbols('rho_filtered rho_eff', nonnegative=True, finite=True)

# Same-action flat-FLRW normalization and radiation-conservative all-q source bound.
rho_eff_expr = sp.Rational(3, 2) * (3*lam - 1) * Mpl2 * H**2
Lrho_eff = sp.factor(rho_eff_expr / (32*eta0*Mpl2))
Lhist_at_H = sp.factor(3*(3*lam - 1)*H**2/(64*eta0))
assert sp.simplify(Lrho_eff - Lhist_at_H) == 0

# If rho_filtered<=rho_eff, replacing rho_filtered by rho_eff is conservative.
Lhist = sp.factor(3*(3*lam - 1)*HEFT**2/(64*eta0))
assert sp.simplify(Lhist.subs(HEFT, H) - Lhist_at_H) == 0

# Frozen 1%/1% scale-separation interval.
Lcos = 99*kcos**2
Ulocal = klocal**2/99
scale_margin = sp.factor(Ulocal - Lcos)
scale_factored = sp.factor((klocal-99*kcos)*(klocal+99*kcos)/99)
assert sp.simplify(scale_margin - scale_factored) == 0

# History lower bound versus local upper bound.
C = sp.factor(3*(3*lam-1)/(64*eta0))
Hceil2 = sp.factor(64*eta0*klocal**2/(297*(3*lam-1)))
history_margin = sp.factor(Ulocal - Lhist)
assert sp.simplify(history_margin - C*(Hceil2-HEFT**2)) == 0

# Positive square-root form of the exact history ceiling.
Hceil = 8*sp.sqrt(eta0/(297*(3*lam-1)))*klocal
assert sp.simplify(Hceil**2 - Hceil2) == 0

# Near-GR homogeneous normalization remains continuously available for eps>0.
R_H2 = sp.factor(2/(3*lam-1))
frac_dev = sp.factor(1-R_H2)
assert sp.simplify(R_H2 - 2/(2+3*eps)) == 0
assert sp.simplify(frac_dev - 3*eps/(2+3*eps)) == 0

out = {
  'classification': 'RTK_ROUTE_B_U1_HISTORY_WIDE_MC_WINDOW_PASS',
  'status_scope': 'GREEN_EXACT_HISTORY_WINDOW_ALGEBRA_SOURCE_COMPOSITION_AND_PRODUCTION_IMPLEMENTATION_PENDING',
  'target': 'research/theory_targets/RTK_ROUTE_B_U1_HISTORY_WIDE_MC_WINDOW_TARGET_v1.json',
  'domain': {
    'lambda_HL': 'lambda_HL=1+epsilon with epsilon>0',
    'eta0': 'eta0>0',
    'history': 'declared a_EFT with H(a)<=H_EFT for every audited a>=a_EFT',
    'source_assumption': '0<=rho_filtered(a)<=rho_eff(a)',
    'matter_scope': 'nonnegative-pressure barotropic all-q theorem; massive-neutrino anisotropic stress excluded',
    'units': 'c=1, so H and physical wavenumbers carry the same inverse-length units'
  },
  'history_bound_derivation': {
    'parent_source_bound': 'M_c^2 >= rho_filtered/(32 eta0 M_Pl^2)',
    'same_action_rho_eff': 'rho_eff=(3/2)(3 lambda_HL-1) M_Pl^2 H^2',
    'conservative_instantaneous_bound': 'M_c^2 >= 3(3 lambda_HL-1) H^2/(64 eta0)',
    'history_wide_bound': 'M_c^2 >= L_history := 3(3 lambda_HL-1) H_EFT^2/(64 eta0)'
  },
  'joint_pre_root_exclusion_window': 'max(99 k_cos_phys^2, L_history) <= M_c^2 <= k_local_phys^2/99',
  'nonempty_conditions': [
    'k_local_phys/k_cos_phys >= 99',
    'L_history <= k_local_phys^2/99',
    'equivalently H_EFT <= 8 sqrt[eta0/(297(3 lambda_HL-1))] k_local_phys'
  ],
  'exact_margins': {
    'scale_margin': 'k_local_phys^2/99-99 k_cos_phys^2 = (k_local_phys-99 k_cos_phys)(k_local_phys+99 k_cos_phys)/99',
    'history_margin': '[3(3 lambda_HL-1)/(64 eta0)](H_ceiling^2-H_EFT^2)',
    'H_ceiling_squared': '64 eta0 k_local_phys^2/[297(3 lambda_HL-1)]'
  },
  'near_GR_background': {
    'ratio': 'H^2(lambda_HL)/H^2(1)=2/(3 lambda_HL-1)',
    'lambda_HL_1_plus_epsilon_deviation': '1-R=3 epsilon/(2+3 epsilon)'
  },
  'root_exclusion': 'The isolated leading rank-loss root M_c^2=-x/b2, when positive, remains a separate point/buffer exclusion inside any otherwise allowed interval; this theorem does not replace it by a one-sided bound.',
  'interpretation': 'A fixed M_c can satisfy both the constructive all-q rank requirement and the 1% cosmology/local filter separation over a declared finite EFT history if the two displayed interval conditions hold. Because the sufficient source lower bound grows with H, extending the same fixed-M_c theorem arbitrarily toward an H->infinity early-time limit is not certified; an EFT onset or a different UV regime is mandatory.',
  'parameter_freeze': 'No numerical M_c, lambda_HL, epsilon, eta0, a_EFT, k_cos_phys, k_local_phys or H_EFT is selected.',
  'non_claims': [
    'does not prove rho_filtered<=rho_eff for the production source composition',
    'does not include massive-neutrino anisotropic stress',
    'does not implement lambda_HL or the elliptic filtered source in CLASS',
    'does not provide a likelihood score',
    'does not prove generic inhomogeneous rank',
    'does not cure the local-rest C8 rank collapse or C9 radiative-naturalness obstruction'
  ],
  'next_gate': 'freeze a production-completion implementation protocol that exposes lambda_HL separately from lambda_D, evaluates k_phys=k_com/a, implements the projected filtered source/constraint equations, and audits the source-history assumptions before any new likelihood score.'
}
with open('u1_history_wide_mc_window_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'], json.dumps(out,sort_keys=True))
