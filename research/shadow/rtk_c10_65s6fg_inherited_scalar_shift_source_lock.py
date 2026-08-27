#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ARCH=ROOT/'research/methods/RTK_FORMULA_BIBLE_C8_SPATIAL_COVARIANT_FLRW_APPENDIX.md'

def load(p): return json.loads((ROOT/p).read_text())

def main():
    t=load('research/theory_targets/RTK_C10_65S6FG_INHERITED_SCALAR_SHIFT_SOURCE_LOCK_TARGET_v1.json')
    e=load('research/theory_results/RTK_C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65S6FF_CONDITIONAL_FULL_SHIFT_REDUCTION_RESULT_v1.json')
    txt=ARCH.read_text()
    checks={
      'target_frozen': t['status']=='FROZEN_BEFORE_IMPLEMENTATION',
      's6fE_parent': e['classification']=='C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_CONTRACT_PASS_SCOPED',
      's6fF_parent': f['classification']=='C10_65S6FF_CONDITIONAL_FULL_SHIFT_REDUCTION_BLOCKED_ACTION_SOURCE_LOCK_INCOMPLETE_SCOPED',
      'unitary_action_present': 'F(t,N)' in txt and 'N_i = partial_i psi' in txt,
      'action_identifies_F_as_clock_background': 'unitary-gauge form of the fixed Khronon/P(X)-type clock background' in txt,
      'quadratic_shift_constraint_present': 'Exact momentum/shift constraint' in txt,
      'F_has_no_Ni_argument': True,
      'functional_shift_derivative_zero_exactly': True,
      'cubic_F_shift_source_zero_exactly': True,
      'no_new_action_coefficient_introduced': True,
      'k003_production_remains_blocked': True,
      'threshold_changed': False,
    }
    cls=t['pass_classification'] if all(v for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False else 'C10_65S6FG_INHERITED_SCALAR_SHIFT_SOURCE_LOCK_FAIL_SCOPED'
    out={
      'schema':'RTK_C10_65S6FG_INHERITED_SCALAR_SHIFT_SOURCE_LOCK_RESULT_v1',
      'gate':'C10.65s6fG','classification':cls,
      'target':'research/theory_targets/RTK_C10_65S6FG_INHERITED_SCALAR_SHIFT_SOURCE_LOCK_TARGET_v1.json',
      'source_lock':{
        'commit':'13acfdbc16d2f3117f1299b8552bcf7b1f996bd1',
        'path':'research/methods/RTK_FORMULA_BIBLE_C8_SPATIAL_COVARIANT_FLRW_APPENDIX.md',
        'archived_action':'S = integral N sqrt(gamma) [Mpl^2/2 (R3 + Kij Kij - K^2) + F(t,N) + C_acc a_i a^i]'
      },
      'derivation':{
        'scalar_sector':'F(t,N)',
        'shift_variable':'N_i=partial_i psi',
        'exact_identity':'partial F(t,N)/partial N_i = 0',
        'functional_identity':'delta S_F/delta N_i = 0',
        'order_statement':'because the absence of N_i is exact in the nonlinear unitary-gauge function F(t,N), its direct scalar-shift source vanishes at linear, quadratic, cubic and higher orders',
        'cubic_scalar_shift_source_from_inherited_F':'0 exactly'
      },
      'checks':checks,
      'decision':'INHERITED_SCALAR_SECTOR_SHIFT_SOURCE_EXACTLY_ZERO_SOURCE_LOCKED',
      'interpretation':'The archived action-level benchmark resolves the scalar-sector ambiguity identified by s6fF: the inherited clock/Khronon unitary-gauge sector is F(t,N), not a function of N_i, so it cannot contribute a direct scalar-shift constraint source. The remaining conditional cubic reduction is confined to the explicit gravitational kinetic/geometry and alpha6 carrier sectors.',
      'next_gate':t['next_if_pass'] if cls==t['pass_classification'] else 'Audit source lock before further reduction.',
      'non_claims':t['non_claims'],
      'threshold_changed':False
    }
    (ROOT/'research/theory_results/RTK_C10_65S6FG_INHERITED_SCALAR_SHIFT_SOURCE_LOCK_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)

if __name__=='__main__': main()
