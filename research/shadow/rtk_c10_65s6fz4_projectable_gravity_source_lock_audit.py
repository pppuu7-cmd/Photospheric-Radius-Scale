#!/usr/bin/env python3
import json, sys
from pathlib import Path

T=Path('research/theory_targets/RTK_C10_65S6FZ4_PROJECTABLE_GRAVITY_SOURCE_LOCK_AUDIT_TARGET_v1.json')
P=Path('research/theory_results/RTK_C10_65S6FZ3_FULL_COUPLED_CONSTRAINT_IDENTIFIABILITY_PREFLIGHT_RESULT_v1.json')
C9=Path('research/checkpoints/RTK_PROJECTABLE_U1_C9_ARCHITECTURE_CHECKPOINT_2026-08-23T2007Z.md')
S6FT=Path('research/checkpoints/RTK_C10_65S6FT_ADM_EMBEDDING_SOURCE_LOCK_2026-08-27T1224Z.md')
Z1=Path('research/checkpoints/RTK_C10_65S6FZ1_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_AUDIT_2026-08-27.md')
OUT=Path('research/theory_results/RTK_C10_65S6FZ4_PROJECTABLE_GRAVITY_SOURCE_LOCK_AUDIT_RESULT_v1.json')
for p in (T,P,C9,S6FT,Z1):
    if not p.exists():
        print(f'missing {p}', file=sys.stderr); sys.exit(3)
t=json.loads(T.read_text()); parent=json.loads(P.read_text())
c9=C9.read_text(); s6ft=S6FT.read_text(); z1=Z1.read_text()
checks={
 'target_exact': t.get('gate')=='C10.65s6fZ4',
 'parent_exact': parent.get('classification')=='C10_65S6FZ3_FULL_COUPLED_CONSTRAINT_NON_IDENTIFIABLE_PASS_SCOPED',
 'historical_projectable_parent_exists': 'PROJECTABLE BRANCH STRUCTURALLY GREEN IN SCOPED C8/C9 GATES' in c9,
 'projectability_explicit': 'For `N=N(t)`' in c9 and '`a_i=D_i ln N=0`' in c9,
 'historical_projectable_dof_certificate_exists': 'RTK_C9_PROJECTABLE_U1_COUPLED_DOF_ALLQ_PASS' in c9,
 'historical_parent_has_open_full_program': 'FULL FINITE-Mc PPN, PRODUCTION COSMOLOGY, STRONG COUPLING AND STRONG FIELD REMAIN OPEN' in c9,
 's6ft_says_no_single_full_embedding': 'no single projectable ADM action currently fixes' in s6ft,
 'z1_says_no_ready_s6fz_symmetry_realization': 'NO_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_FOUND_PASS_SCOPED' in z1,
 'no_soft_s_retest': t['guards']['no_soft_s_retest'] is True,
 'no_k003_production': t['guards']['no_k003_production'] is True,
 'no_parameter_fit': t['guards']['no_parameter_fit'] is True,
 'threshold_changed_false': t['guards']['threshold_changed'] is False,
}
core=all(checks.values())
if not (checks['target_exact'] and checks['parent_exact']):
    cls='C10_65S6FZ4_FAIL_SCOPED'
elif core:
    cls='C10_65S6FZ4_PROJECTABLE_GRAVITY_PARTIAL_PARENT_PASS_SCOPED'
else:
    cls='C10_65S6FZ4_FAIL_SCOPED'
result={
 'schema':'RTK_C10_65S6FZ4_PROJECTABLE_GRAVITY_SOURCE_LOCK_AUDIT_RESULT_v1',
 'gate':'C10.65s6fZ4','classification':cls,'checks':checks,
 'finding':'A genuine independently motivated projectable-U(1) gravitational architecture predates the present soft-s problem and has scoped C9 projectability/DOF certificates. However the audited archive does not provide a single full nonlinear projectable ADM embedding that simultaneously realizes the new s6fZ2 field-space gauge template and fixes the same-action lapse/shift/source/constraint interface. It is therefore a partial parent, not an embedding-ready combined action.',
 'historical_parent':'RTK projectable-U(1) C9 architecture checkpoint 2026-08-23',
 's6ft_embedding_ready':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,
 'next_gate':'C10.65s6fZ5: freeze the exact interface requirements for combining the independently motivated projectable-U(1) gravitational parent with the s6fZ2 gauge-invariant scalar template, without choosing new coefficients; derive whether the symmetries commute/close and what lapse/shift couplings are forced before a full coupled Dirac count.',
 'threshold_changed':False,
 'provenance':{'workflow':'rtk-c10-65s6fz4-projectable-gravity-source-lock-audit.yml','frozen_target_commit':'f2fd6ddb55058d3ab768d0dc948c693e4e736737','threshold_changed':False}
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if core else 2)
