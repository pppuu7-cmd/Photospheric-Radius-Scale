#!/usr/bin/env python3
"""Linear-perturbation obstruction for the minimal coordinate-only U1 compensator.

Parent candidate:
    Delta L = - sigma F_Sigma(Sigma)
with F_Sigma(Sigma_bar(a)) = rho_bar_m(a)+rho_bar_r(a).

This exactly cancels the homogeneous family-I ordinary-matter A source while
preserving the exceptional primary velocity degeneracy.  The question here is
strictly stronger: can the same *coordinate-only* fixed function cancel the
ordinary A source for arbitrary independent linear matter perturbations?

At linear order
    delta F_Sigma = F'_Sigma(Sigma_bar) delta Sigma.
For the frozen a1=1,a2=0 universal matter frame, already the density part of
the ordinary A source contains an independent delta rho_H direction.  Choose
a legitimate tangent direction with delta Sigma=0 and delta rho_H != 0.  Then
the coordinate compensator has delta F_Sigma=0 while the ordinary source is
nonzero.  Therefore no single F_Sigma(Sigma) can provide an off-shell identity
that cancels arbitrary independent matter perturbations.

This is a scoped no-go only for *full perturbative A-source cancellation by a
coordinate-only clock function*. It does not invalidate the exact FLRW
background cancellation, and it does not exclude a dynamical constraint that
locks matter perturbations to Sigma, a matter-dependent compensator, or a new
matter/A-source architecture. Those are new actions and require fresh DOF/PPN
checks.
"""
import json
import sympy as sp

Fp, dSigma, drho = sp.symbols('Fprime deltaSigma delta_rho', finite=True, real=True)

# Linear source pieces in the normalization used by the preceding family-I gates.
dF = Fp*dSigma
dJA_ord_density = 2*drho
dJA_comp = -2*dF
residual = sp.expand(dJA_ord_density + dJA_comp)
assert residual == 2*drho - 2*Fp*dSigma

# Independent matter-density tangent direction: clock coordinate held fixed.
residual_independent_matter = sp.simplify(residual.subs(dSigma, 0))
assert residual_independent_matter == 2*drho
assert residual_independent_matter != 0

# Exact cancellation is possible only on a restricted locked subspace.
locked_solution = sp.solve(sp.Eq(residual, 0), drho)
assert locked_solution == [Fp*dSigma]

# Two-variable Jacobian makes the structural mismatch explicit: a function of
# Sigma alone has no derivative with respect to the independent matter density.
Sigma, rho = sp.symbols('Sigma rho', finite=True, real=True)
F = sp.Function('F')(Sigma)
comp_grad = sp.Matrix([sp.diff(F, Sigma), sp.diff(F, rho)])
target_grad = sp.Matrix([sp.Integer(0), sp.Integer(1)])
assert comp_grad[1] == 0
assert target_grad[1] == 1

out = {
  'classification': 'RTK_ROUTE_B_U1_COORDINATE_COMPENSATOR_PERTURBATION_OBSTRUCTION',
  'status_scope': 'BLACK_SCOPED_COORDINATE_ONLY_FULL_PERTURBATIVE_A_SOURCE_CANCELLATION',
  'parent_candidate': 'Delta L=-sigma F_Sigma(Sigma)',
  'background_result_retained': 'F_Sigma(Sigma_bar(a))=rho_bar_H(a) can exactly cancel the homogeneous family-I A source and preserve primary velocity degeneracy.',
  'linear_identity': 'delta J_A^tot = 2 delta rho_H - 2 F_Sigma_prime delta Sigma, before additional stress/velocity source pieces.',
  'counterdirection': 'delta Sigma=0 with independent delta rho_H!=0 gives delta J_A^tot=2 delta rho_H!=0.',
  'restricted_cancellation_subspace': 'delta rho_H = F_Sigma_prime delta Sigma',
  'result': 'A fixed function of the RTK clock coordinate alone cannot identically cancel arbitrary independent ordinary-matter perturbations. Full perturbative cancellation would require a new relation that locks matter to the clock or a compensator/source architecture with explicit matter-state dependence.',
  'why_this_precedes_finite_k_rank': 'A finite-k rank test of the coordinate-only source can still classify that action, but passing rank would not make it reproduce the intended cosmological perturbation sector. The source-content mismatch must therefore remain an explicit model-completion obstruction.',
  'non_claims': [
    'does not invalidate the exact homogeneous FLRW cancellation',
    'does not prove that every finite-k mode is inconsistent; the A constraint may instead impose a new matter-clock relation',
    'does not exclude an auxiliary constrained compensator, matter-current construction, non-universal matter frame, or other degenerate source architecture',
    'does not by itself change the already-certified B9 numerical robustness results of the phenomenological RTK implementation'
  ],
  'next_gate': 'search for the minimal velocity-degenerate compensator whose A source depends on an independent matter state variable (or a protected auxiliary variable constrained to it), while retaining the exceptional primary constraint. Freeze that action before recomputing full finite-k Dirac rank, cosmological perturbations, PPN/equivalence principle, and radiative stability.'
}
with open('u1_coordinate_compensator_perturbation_obstruction_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'], json.dumps(out,sort_keys=True))
