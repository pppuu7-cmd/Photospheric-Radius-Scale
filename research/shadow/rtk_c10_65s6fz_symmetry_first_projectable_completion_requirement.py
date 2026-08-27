#!/usr/bin/env python3
import json, sys
from pathlib import Path
import sympy as sp

TARGET=Path('research/theory_targets/RTK_C10_65S6FZ_SYMMETRY_FIRST_PROJECTABLE_COMPLETION_REQUIREMENT_TARGET_v1.json')
PARENT=Path('research/theory_results/RTK_C10_65S6FY_SYMMETRY_FIRST_CANDIDATE_SPACE_AUDIT_RESULT_v1.json')
OUT=Path('research/theory_results/RTK_C10_65S6FZ_SYMMETRY_FIRST_PROJECTABLE_COMPLETION_REQUIREMENT_RESULT_v1.json')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())

u1,u2,kappa,m,sigma,z,x=sp.symbols('u1 u2 kappa m sigma z x', nonzero=True)
m11,m12,m22,s1,s2=sp.symbols('m11 m12 m22 s1 s2')
u=sp.Matrix([u1,u2])
n=sp.Matrix([-u2,u1])
K=kappa*(u*u.T)
M=sp.Matrix([[m11,m12],[m12,m22]])
s=sp.Matrix([s1,s2])

checks={}
checks['target_exact_gate']=t.get('gate')=='C10.65s6fZ'
checks['parent_exact']=p.get('classification')=='C10_65S6FY_NO_SOURCE_LOCKED_PROJECTABLE_CANDIDATE_FOUND_PASS_SCOPED'
checks['kinetic_null_identity']=all(sp.simplify(v)==0 for v in K*n)

# Necessity of M proportional to u u^T, checked on both nonzero coordinate patches.
eqs=list(M*n)
sol_u1=sp.solve(eqs,[m12,m22],dict=True)
sol_u2=sp.solve(eqs,[m11,m12],dict=True)
checks['Mn_zero_patch_u1_solved']=bool(sol_u1) and sp.simplify(sol_u1[0][m12]-m11*u2/u1)==0 and sp.simplify(sol_u1[0][m22]-m11*u2**2/u1**2)==0
checks['Mn_zero_patch_u2_solved']=bool(sol_u2) and sp.simplify(sol_u2[0][m12]-m22*u1/u2)==0 and sp.simplify(sol_u2[0][m11]-m22*u1**2/u2**2)==0
Mclass=m*(u*u.T)
checks['Mclass_null_identity']=all(sp.simplify(v)==0 for v in Mclass*n)
checks['Mclass_rank_one']=sp.simplify(Mclass.det())==0

# Necessity/sufficiency of source alignment.
source_null=sp.expand((s.T*n)[0])
sol_s1=sp.solve(sp.Eq(source_null,0),s1)
sol_s2=sp.solve(sp.Eq(source_null,0),s2)
checks['source_alignment_patch_u1']=bool(sol_s1) and sp.simplify(sol_s1[0]-s2*u1/u2)==0
checks['source_alignment_patch_u2']=bool(sol_s2) and sp.simplify(sol_s2[0]-s1*u2/u1)==0
sclass=sigma*u
checks['source_class_null_identity']=sp.simplify((sclass.T*n)[0])==0

# Gauge quotient q=u*x has a scalar inverse response affine in z.
q=u*x
kin_coeff=sp.expand((q.T*K*q)[0]/x**2)
pot_coeff=sp.expand((q.T*Mclass*q)[0]/x**2)
src_coeff=sp.expand((sclass.T*q)[0]/x)
quotient_inverse=sp.factor(pot_coeff-z*kin_coeff)
expected=(u1**2+u2**2)**2*(m-kappa*z)
checks['quotient_inverse_affine']=sp.simplify(quotient_inverse-expected)==0
checks['quotient_source_aligned']=sp.simplify(src_coeff-sigma*(u1**2+u2**2))==0
checks['one_finite_pole_max']=sp.Poly(quotient_inverse,z).degree()==1

all_required=all(checks.values())
classification='C10_65S6FZ_SYMMETRY_PROTECTED_PROJECTABLE_RANK_ONE_CLASS_PASS_SCOPED' if all_required else 'C10_65S6FZ_THEOREM_FAIL_SCOPED'
result={
  'schema':'RTK_C10_65S6FZ_SYMMETRY_FIRST_PROJECTABLE_COMPLETION_REQUIREMENT_RESULT_v1',
  'gate':'C10.65s6fZ',
  'classification':classification,
  'checks':checks,
  'exact_theorem':{
    'kinetic_class':'K = kappa u u^T',
    'null_direction':'n = (-u2,u1)^T',
    'gauge_invariance_conditions':['M n = 0','s.n = 0'],
    'symmetric_M_solution':'M = m u u^T (patchwise for nonzero u)',
    'source_solution':'s = sigma u',
    'quotient_inverse_response':str(quotient_inverse),
    'pole_statement':'After quotienting the local null direction, the inverse response is affine in z=omega^2 and has at most one finite pole.'
  },
  'finding':'A nonempty local symmetry-protected projectable rank-one quadratic class exists. Local redundancy along the kinetic null direction forces both the symmetric algebraic matrix and the linear source to align with the kinetic direction. This protects the one-pole structure, but it does not identify a unique nonlinear ADM/clock action or its background functions.',
  's6ft_embedding_ready':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  'next_gate':'C10.65s6fZ1: source-lock whether the RTK archive contains an independently motivated nonlinear symmetry realization whose projectable ADM reduction implements this null-direction redundancy. If absent, retain the action-selection blocker rather than inventing coefficients.',
  'threshold_changed':False,
  'provenance':{'workflow':'rtk-c10-65s6fz-symmetry-first-projectable-completion-requirement.yml','threshold_changed':False}
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if all_required else 2)
