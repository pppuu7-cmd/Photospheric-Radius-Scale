#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(p):
    return json.loads((ROOT/p).read_text())

def main():
    target=load('research/theory_targets/RTK_C10_65S6FF_CONDITIONAL_FULL_SHIFT_REDUCTION_TARGET_v1.json')
    b=load('research/theory_results/RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_RESULT_v1.json')
    e=load('research/theory_results/RTK_C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_RESULT_v1.json')
    assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert b['classification']=='C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_BLOCKED_INCOMPLETE_FIXED_ACTION_SCOPED'
    assert e['classification']=='C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_CONTRACT_PASS_SCOPED'
    c=e['candidate_branch']

    # The gravitational shift sector is explicit enough to expose the universal
    # quadratic scalar-shift kernel.  In flat scalar ADM perturbations with
    # N_i=partial_i beta, the kinetic term gives
    #   L2_beta ~ (Mstar^2/2)(1-lambda_HL)(Delta beta)^2
    # so K_beta(q) is proportional to (1-lambda_HL) q^4.  This is not yet the
    # full cubic source: every nonlinear matter/scalar term that depends on N_i
    # must also be fixed before beta can be eliminated consistently.
    quadratic_shift_kernel = '(Mstar^2/2)*(1-lambda_HL)*q^4 (overall Fourier/sign convention aside)'

    scalar_decl=c.get('matter_and_existing_scalar_sector','')
    explicit_scalar_action = (
        ('P(X)=' in scalar_decl) or
        ('action=' in scalar_decl.lower()) or
        ('source:' in scalar_decl.lower()) or
        ('sha' in scalar_decl.lower())
    )
    explicit_scalar_cubic_shift_source = False
    explicit_gravity = 'K_ij K^ij - lambda_HL K^2' in c.get('gravitational_kinetic_sector','')
    explicit_alpha = c.get('alpha6_rule')=='alpha6(X)=alpha6_0*(X/X0)^(1/2)'
    extra_closed = c.get('extra_shift_dependent_operator_basis')==[] and c.get('nu_Sigma2_rule')=='nu(X) identically zero by candidate-branch definition'

    checks={
        'candidate_branch_frozen_before_reduction': c.get('name')==target['candidate_branch'],
        'projectable_lapse_no_local_finite_k_mode': c.get('projectability')=='N=N(t)',
        'gravitational_shift_sector_explicit': explicit_gravity,
        'alpha6_full_state_rule_explicit': explicit_alpha,
        'additional_shift_operator_basis_closed': extra_closed,
        'quadratic_shift_kernel_explicit': True,
        'all_scalar_shift_sources_explicit_or_immutably_referenced': explicit_scalar_action,
        'cubic_shift_source_explicit': explicit_scalar_cubic_shift_source,
        'q_s_zero_taken_after_constraint_reduction': True,
        'no_soft_s_driven_coefficient_fit': e.get('checks',{}).get('s6e_bare_vertex_not_used_to_choose_branch') is True,
        'k003_production_remains_blocked': e.get('checks',{}).get('k003_production_remains_blocked') is True,
        'threshold_changed': False,
    }

    complete = explicit_gravity and explicit_alpha and extra_closed and explicit_scalar_action and explicit_scalar_cubic_shift_source
    if complete:
        raise SystemExit('Unexpected complete action: extend analyzer to perform exact ZERO/NONZERO reduction before classifying')

    classification=target['blocked_if_incomplete']
    out={
        'schema':'RTK_C10_65S6FF_CONDITIONAL_FULL_SHIFT_REDUCTION_RESULT_v1',
        'gate':'C10.65s6fF',
        'classification':classification,
        'target':'research/theory_targets/RTK_C10_65S6FF_CONDITIONAL_FULL_SHIFT_REDUCTION_TARGET_v1.json',
        'candidate_branch':c['name'],
        'checks':checks,
        'derived':{
            'quadratic_scalar_shift_kernel':quadratic_shift_kernel,
            'kernel_soft_scaling':'K_beta(q) proportional to q^4; exact q=0 is degenerate and must only be approached after the full source is reduced',
            'gravitational_kinetic_sector_source_locked':explicit_gravity,
            'additional_shift_operator_basis_closed':extra_closed,
            'alpha6_state_function_source_locked':explicit_alpha,
            'inherited_scalar_sector_declaration':scalar_decl,
            'inherited_scalar_nonlinear_action_explicit_or_immutable_reference':explicit_scalar_action,
            'inherited_scalar_cubic_shift_source_explicit':explicit_scalar_cubic_shift_source,
        },
        'shift_reduction':{
            'quadratic_kernel':'EXPOSED_FOR_GRAVITATIONAL_KINETIC_SECTOR',
            'cubic_source':'NOT_FULLY_DEFINED_FROM_SOURCE_LOCKED_CANDIDATE',
            'exchange_contribution':'NOT_CLASSIFIED',
            'total_reduced_vertex':'NOT_CLASSIFIED',
            'exact_cancellation_residual':'NOT_DEFINED'
        },
        'decision':'SOURCE_LOCK_INHERITED_NONLINEAR_SCALAR_SECTOR_BEFORE_ZERO_NONZERO_CLASSIFICATION',
        'interpretation':'s6fE closes the new gravitational/extra-shift operator choices, but its inherited scalar sector is specified only by a lower-order inheritance statement, with no explicit nonlinear action or immutable source reference for its cubic N_i dependence. Because the scalar shift is a constraint variable, silently setting that missing cubic source to zero would change the fixed action. The candidate reduction therefore remains scientifically blocked at a narrower, now explicit source-lock boundary.',
        'next_gate':'C10.65s6fG: source-lock the exact inherited nonlinear scalar/P(X) action and derive/prove its cubic scalar-shift source; then rerun the unchanged s6fF ZERO/NONZERO target.',
        'non_claims':[
            'not an exact cancellation result',
            'not a surviving-vertex result',
            'not a no-go for MINIMAL_PROJECTABLE_N2_S1HALF_v1 after complete scalar-sector source lock',
            'not permission for k=0.03 production',
            'not radiative-naturalness closure'
        ],
        'threshold_changed':False,
    }
    p=ROOT/'research/theory_results/RTK_C10_65S6FF_CONDITIONAL_FULL_SHIFT_REDUCTION_RESULT_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)

if __name__=='__main__': main()
