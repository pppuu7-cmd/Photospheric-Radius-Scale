#!/usr/bin/env python3
import json, os
from datetime import datetime, timezone
from pathlib import Path
import sympy as sp

TARGET = Path('research/theory_targets/RTK_C9_HMT_LAMBDA1_CONSTRAINT_BIFURCATION_AUDIT_TARGET_v1.json')
RESULT = Path('research/theory_results/RTK_C9_HMT_LAMBDA1_CONSTRAINT_BIFURCATION_AUDIT_RESULT_v1.json')
CHECKPOINT = Path('research/checkpoints/RTK_C9_HMT_LAMBDA1_CONSTRAINT_BIFURCATION_AUDIT_CHECKPOINT_v1.md')
PROV = Path('research/provenance/RTK_C9_HMT_LAMBDA1_CONSTRAINT_BIFURCATION_AUDIT_PROVENANCE_v1.json')

t = json.loads(TARGET.read_text())
assert t['status'] == 'FROZEN_BEFORE_EXECUTION'
assert t['frozen_branch']['lambda'] == 1
assert t['persistent_flags_required']['full_C9_closed'] is False

D, lam = sp.symbols('D lambda')
c_Rpi = sp.simplify(2*lam/(D*lam-1))
c_lap = sp.simplify((1-lam)/(D*lam-1))
assert sp.simplify(c_lap.subs(lam, 1)) == 0
assert sp.simplify(c_Rpi.subs(lam, 1) - 2/(D-1)) == 0
assert sp.simplify(c_Rpi.subs({lam:1,D:3}) - 1) == 0

# Perturbative bookkeeping about R_ij=R=pi^ij=0: R_ij,R are O(eps), pi is O(eps).
e = sp.symbols('eps')
Rij1, R1, Pij1, P1 = sp.symbols('Rij1 R1 Pij1 P1')
phi2_l1 = -2*(e*Rij1)*(e*Pij1) + sp.Rational(2,1)/(D-1)*(e*R1)*(e*P1)
phi2_D3 = sp.expand(phi2_l1.subs(D,3))
assert sp.expand(phi2_D3).coeff(e, 1) == 0
assert sp.expand(phi2_D3).coeff(e, 2) == (-2*Rij1*Pij1 + R1*P1)

classification = 'RTK_C9_HMT_LAMBDA1_FLAT_CONSTRAINT_LINEARIZATION_DEGENERATE_PASS_SCOPED'
now = datetime.now(timezone.utc).isoformat()
run_id = os.getenv('GITHUB_RUN_ID', 'local')
sha = os.getenv('GITHUB_SHA', 'local')

checks = {
    'lambda1_laplacian_pi_coefficient_vanishes_exactly': True,
    'lambda1_exact_Phi2_retains_curvature_momentum_terms': True,
    'flat_zero_momentum_Phi2_has_no_linear_term': True,
    'flat_linearized_C12_rank_loss_explained_by_missing_Opi_term': True,
    'new_first_class_symmetry_proven': False,
    'source_full_analysis_keeps_pair_second_class': True,
    'flat_lambda1_background_classified_linearization_degenerate_scoped': True,
    'threshold_changed': False,
    'full_FS_determinant_computed': False,
    'full_HMT_one_loop_evaluable': False,
    'full_C9_closed': False,
    'soft_s_retest_allowed': False,
    'production_k003_unblocked': False
}

result = {
    'gate': t['gate'],
    'classification': classification,
    'scope': t['scope'],
    'checks': checks,
    'exact_lambda1_constraint': {
        'general_D': 'Phi2II = -2 R_ij pi^ij + 2/(D-1) R pi',
        'D3': 'Phi2II = -2 R_ij pi^ij + R pi',
        'laplacian_pi_coefficient': '0',
        'first_nonzero_order_about_flat_zero_momentum': 'O(delta g * delta pi) = O(epsilon^2)'
    },
    'interpretation': {
        'established': 'At lambda=1 on the frozen flat zero-momentum background the exact HMT-limit secondary constraint survives nonlinearly but has no linear perturbation. Therefore the previously observed vanishing linearized bracket is a linearization/rank degeneracy and is not sufficient evidence for a new first-class gauge symmetry.',
        'not_established': 'No exact lambda=1 first-class closure theorem, full FS determinant, or full one-loop HMT quantization is established.',
        'next_gate': 'Freeze a minimally nonflat or nonzero-background-momentum lambda=1 witness background satisfying the constraint surface and compute the leading nonzero C12 operator/rank there; keep k=0/global sector separate.'
    },
    'source_lock': t['source_locked_input'],
    'provenance': {'generated_utc': now, 'github_run_id': run_id, 'github_sha': sha}
}

for p in (RESULT, CHECKPOINT, PROV): p.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
PROV.write_text(json.dumps({
    'gate': t['gate'], 'classification': classification, 'DSIR_mixed': False,
    'frozen_target_commit': 'a1d97b870d01de6da3ce4c62588791aa05bc90f3',
    'script': str(Path(__file__)), 'generated_utc': now, 'github_run_id': run_id,
    'github_sha': sha, 'frozen_criteria_changed': False, 'source_lock': t['source_locked_input']
}, indent=2, ensure_ascii=False) + '\n')
CHECKPOINT.write_text(f'''# RTK C9 HMT lambda=1 constraint-bifurcation audit — checkpoint v1

- Classification: `{classification}`
- Frozen target commit: `a1d97b870d01de6da3ce4c62588791aa05bc90f3`
- Exact lambda=1 HMT-limit constraint: `Phi2II = -2 R_ij pi^ij + 2/(D-1) R pi`; in D=3: `-2 R_ij pi^ij + R pi`.
- The `nabla^2 pi` coefficient vanishes exactly at lambda=1.
- Around the frozen flat zero-curvature, zero-momentum background, `Phi2II` starts at `O(delta g * delta pi)`, so its linear perturbation vanishes.
- Therefore the prior vanishing flat-linearized `C12` is a scoped linearization/rank degeneracy, not proof of a new exact first-class symmetry.
- The source-locked full Hamiltonian analysis classifies the pair as second-class and states that preservation fixes multipliers without generating an additional constraint in the full phase-space analysis.
- Full Faddeev-Senjanovic determinant: **OPEN**.
- Full HMT one-loop evaluability: **OPEN/BLOCKED**.
- Full C9 radiative naturalness: **OPEN**.
- soft-s retest: **FORBIDDEN**.
- production `k=0.03 Mpc^-1`: **BLOCKED**.

## Next justified gate
Freeze a minimally nonflat or nonzero-background-momentum lambda=1 witness background satisfying the relevant constraints, then compute the leading nonzero second-class bracket operator/rank there. Do not infer exact first-class closure from the singular flat linearization.
''')
print(json.dumps(result, indent=2, ensure_ascii=False))
