#!/usr/bin/env python3
import json, math, pathlib, datetime

ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C9_HMT_LAMBDA1_CONSTANT_CURVATURE_WITNESS_RANK_TARGET_v1.json'
RESULT=ROOT/'research/theory_results/RTK_C9_HMT_LAMBDA1_CONSTANT_CURVATURE_WITNESS_RANK_RESULT_v1.json'
CHECKPOINT=ROOT/'research/checkpoints/RTK_C9_HMT_LAMBDA1_CONSTANT_CURVATURE_WITNESS_RANK_2026-08-28.md'
PROV=ROOT/'research/provenance/RTK_C9_HMT_LAMBDA1_CONSTANT_CURVATURE_WITNESS_RANK_PROVENANCE_v1.json'

t=json.loads(TARGET.read_text())
assert t['frozen_before_execution'] is True
assert t['background']['spatial_dimension']==3 and t['background']['lambda']==1
assert t['frozen_status']['threshold_changed'] is False

# Exact algebra in units a=1; restore dimensions by R=6/a^2 and q_l=l(l+2)/a^2.
R=6.0
A=R/3.0
rows=[]
for ell in range(0,7):
    q=ell*(ell+2)
    eigen=A*(2*q-R)  # (R/3)[2 q - R], since nabla^2 Y=-qY.
    rows.append({'ell':ell,'minus_laplacian_eigenvalue_times_a2':q,'C12_eigenvalue_times_a4':eigen,'zero':abs(eigen)<1e-12})

assert abs(rows[0]['C12_eigenvalue_times_a4'] + 12.0)<1e-12
assert rows[1]['zero'] is True
assert all(not r['zero'] for r in rows[2:])

classification='RTK_C9_HMT_LAMBDA1_CONSTANT_CURVATURE_WITNESS_RANK_RESTORED_WITH_L1_ZERO_MODES_PASS_SCOPED'
result={
 'classification':classification,
 'frozen_target_parent_head':t['parent_head'],
 'target_frozen_commit':'77ca3bec42e48be2df0888f65f9c725ef4ae5903',
 'derivation':{
   'Phi2_linearized_on_constant_curvature':'(R/3) delta pi',
   'conformal_delta_R_D3':'-R f - 2 nabla^2 f',
   'C12_operator':'(R/3)(-R - 2 nabla^2) delta(x,y)',
   'S3_spectrum':'C12_l=(R/3)[2 l(l+2)/a^2 - R] with R=6/a^2',
   'dimensionless_a4_spectrum':'4[l(l+2)-3]'
 },
 'mode_audit':rows,
 'findings':{
   'nonflat_lambda1_witness_restores_nonzero_rank_for_nonempty_modes':True,
   'ell1_zero_modes_present':True,
   'ell0_nonzero':True,
   'ell_ge2_nonzero_checked_through_6_and_exact_formula_implies_all_ge2':True,
   'flat_zero_momentum_linearization_degeneracy_is_not_generic_across_backgrounds':True,
   'global_exact_constraint_classification_proven':False,
   'full_FS_determinant_computed':False,
   'full_HMT_one_loop_evaluable':False,
   'full_C9_closed':False,
   'soft_s_retest_allowed':False,
   'production_k003_unblocked':False,
   'threshold_changed':False
 },
 'interpretation':'At lambda=1 the flat zero-momentum rank loss is background-dependent: a constant-positive-curvature witness gives a nonzero second-class bracket on ell=0 and all ell>=2 scalar harmonics, while ell=1 remains an exact kernel zero-mode of this linearized block. This is scoped rank restoration, not a full determinant or global constraint proof.',
 'next_gate':'Classify the ell=1 zero modes against the full HMT gauge/constraint algebra (gauge, global/conformal, or genuine residual degeneracy) before forming a reduced determinant.'
}
RESULT.parent.mkdir(parents=True,exist_ok=True); RESULT.write_text(json.dumps(result,indent=2)+'\n')
CHECKPOINT.parent.mkdir(parents=True,exist_ok=True); CHECKPOINT.write_text(f'''# RTK C9 HMT lambda=1 constant-curvature witness rank checkpoint\n\nClassification: `{classification}`\n\nFrozen target commit: `77ca3bec42e48be2df0888f65f9c725ef4ae5903`.\n\nOn S^3 with R=6/a^2, lambda=1 and background momentum zero, the linearized second-class block is\n\nC12 = (R/3)(-R-2 nabla^2),\n\nso on scalar harmonics\n\nC12_l a^4 = 4[l(l+2)-3].\n\nThus ell=0 and every ell>=2 are nonzero, while ell=1 is an exact zero-mode sector. The prior flat-background degeneracy is therefore not generic across backgrounds, but the ell=1 residual kernel prevents claiming a full determinant.\n\nStrict status: full FS determinant OPEN; full HMT one-loop BLOCKED; full C9 OPEN; soft-s retest forbidden; k=0.03 production blocked.\n\nNext gate: classify ell=1 zero modes using the full HMT gauge/constraint algebra before any reduced determinant.\n''')
PROV.parent.mkdir(parents=True,exist_ok=True); PROV.write_text(json.dumps({
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'target':str(TARGET.relative_to(ROOT)),
 'script':str(pathlib.Path(__file__).relative_to(ROOT)),
 'result':str(RESULT.relative_to(ROOT)),
 'checkpoint':str(CHECKPOINT.relative_to(ROOT)),
 'method':'exact symbolic background specialization plus S3 scalar-harmonic eigenvalue audit',
 'no_DSIR':True,
 'no_threshold_change':True
},indent=2)+'\n')
print(json.dumps(result,indent=2))
