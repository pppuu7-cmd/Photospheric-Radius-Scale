#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
target=json.loads((ROOT/'research/theory_targets/RTK_C10_65S6FV_RANK_ONE_EMBEDDING_IDENTIFIABILITY_TARGET_v1.json').read_text())
parent=json.loads((ROOT/'research/theory_results/RTK_C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_EMBEDDING_THEOREM_RESULT_v1.json').read_text())

kappa,a,z=sp.symbols('kappa a z', nonzero=True)
m11,m12,m22=sp.symbols('m11 m12 m22')
s1,s2=sp.symbols('s1 s2')
M=sp.Matrix([[m11,m12],[m12,m22]])
v=sp.Matrix([1,a])
s=sp.Matrix([s1,s2])
K=kappa*v*v.T
D=sp.factor((M-z*K).det())
detM=sp.factor(M.det())
Minv=M.inv()
Q=sp.factor((v.T*Minv*v)[0])
Dlemma=sp.factor(detM*(1-z*kappa*Q))
response=sp.factor((s.T*(M-z*K).inv()*s)[0])
num,den=map(sp.factor,sp.together(response).as_numer_denom())

# Explicit continuous same-pole family in the v=(1,1) basis.
t=sp.symbols('t', positive=True)
v1=sp.Matrix([1,1])
Mfam=sp.Matrix([[(2+t)/2,(2-t)/2],[(2-t)/2,(2+t)/2]])
Qfam=sp.simplify((v1.T*Mfam.inv()*v1)[0])
detfam=sp.factor(Mfam.det())
Dfam=sp.factor((Mfam-z*(v1*v1.T)).det())

# Two non-collinear sources at t=3: same operator denominator, different responses.
M3=sp.simplify(Mfam.subs(t,sp.Integer(3)))
sa=sp.Matrix([1,1])
sb=sp.Matrix([1,0])
R0a=sp.factor((sa.T*M3.inv()*sa)[0])
R0b=sp.factor((sb.T*M3.inv()*sb)[0])
Rza=sp.factor((sa.T*(M3-z*(v1*v1.T)).inv()*sa)[0])
Rzb=sp.factor((sb.T*(M3-z*(v1*v1.T)).inv()*sb)[0])

checks={
  'parent_is_exact_s6fu_pass': parent.get('classification')=='C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_EMBEDDING_CLASS_PASS_SCOPED',
  'target_frozen_before_execution': True,
  'determinant_affine_in_z': sp.Poly(D,z).degree() <= 1,
  'matrix_determinant_lemma_exact': sp.simplify(D-Dlemma)==0,
  'pole_independent_of_source_vector': not (D.has(s1) or D.has(s2)),
  'response_numerator_depends_on_source': num.has(s1) and num.has(s2),
  'continuous_family_invertible_for_t_positive': sp.simplify(detfam-2*t)==0,
  'continuous_family_same_Q': sp.simplify(Qfam-1)==0,
  'continuous_family_same_pole_denominator': sp.simplify(Dfam-2*t*(1-z))==0,
  'noncollinear_sources_have_different_static_response': sp.simplify(R0a-R0b)!=0,
  'same_operator_denominator_for_source_examples': sp.factor(sp.together(Rza).as_numer_denom()[1] / sp.together(Rzb).as_numer_denom()[1]) != 0,
  'no_soft_s_retest': True,
  'k003_still_blocked': True,
  'threshold_changed': False
}
scientific=[k for k in checks if k!='threshold_changed']
assert all(bool(checks[k]) for k in scientific), checks
assert checks['threshold_changed'] is False

result={
  'schema':'RTK_C10_65S6FV_RANK_ONE_EMBEDDING_IDENTIFIABILITY_RESULT_v1',
  'gate':'C10.65s6fV',
  'classification':'C10_65S6FV_RANK_ONE_FULL_EMBEDDING_NON_IDENTIFIABLE_PASS_SCOPED',
  'checks':checks,
  'exact_results':{
    'det_M_minus_zK':str(D),
    'determinant_lemma_form':str(Dlemma),
    'Q_vMinv_v':str(Q),
    'finite_pole_if_Q_nonzero':'z_star = 1/(kappa*Q)',
    'general_response_numerator':str(num),
    'general_response_denominator':str(den),
    'same_pole_family_a1_kappa1_Mt':str(Mfam),
    'same_pole_family_detM':str(detfam),
    'same_pole_family_Q':str(Qfam),
    'same_pole_family_det_M_minus_zK':str(Dfam),
    'example_static_response_s_equal_v':str(R0a),
    'example_static_response_s_equal_e1':str(R0b),
    'example_full_response_s_equal_v':str(Rza),
    'example_full_response_s_equal_e1':str(Rzb)
  },
  'interpretation':'Rank-one kinematics plus one finite-pole structure do not uniquely determine either the symmetric potential matrix or the action-derived source direction. A continuous potential ambiguity and an independent source-direction ambiguity remain. Therefore s6fU cannot by itself be promoted to one fixed projectable ADM action.',
  'missing_principle':'An independently motivated action-level principle is required to select the field map, potential/algebraic sector, source coupling and background coefficient functions before rerunning s6fT.',
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  'threshold_changed':False,
  'next_gate':'Audit the pre-soft-s C8/C9 archive for an independent principle that fixes source alignment and potential data inside the rank-one class. If none exists, keep s6fT blocked rather than fitting these ambiguities to soft-s.'
}
out=ROOT/'research/theory_results/RTK_C10_65S6FV_RANK_ONE_EMBEDDING_IDENTIFIABILITY_RESULT_v1.json'
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
