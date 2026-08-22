#!/usr/bin/env python3
"""Exact algebra gate for the nonprojectable U(1) family-I RTK slice.

Literature anchor: Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666.
For sigma1=sigma2=0 their Eq. (5.43) is

  beta0*(a1**2*kappa*gamma1 + 1) + 2*kappa*(a1*gamma1 + 1)**2 = 0.

The paper separately states that a1=kappa=1 makes the PPN parameters reduce to
GR values.  This executable gate proves the exact factorization of Eq. (5.43)
and distinguishes the gamma1=-1 branch from the beta0=-2(gamma1+1) branch.
It is a literature-consistency/algebra gate only, not an independent static
solution or a coupled Hamiltonian DOF proof.
"""
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
target=json.loads((ROOT/'research/RTK_C8_U1_FAMILY1_FIXED_IR_SLICE_v1.json').read_text())
assert target['classification']=='RTK_C8_U1_FAMILY1_PARTIAL_IR_SLICE_V1_FROZEN'
p=target['gravity_and_matter_frame']
assert p['a1']==1 and p['a2']==0 and p['kappa']==1
assert p['sigma1']==0 and p['sigma2']==0
assert p['beta0']==2 and p['gamma1']==-1 and p['lambda_HL'] is None

a1,kappa,gamma1,beta0=sp.symbols('a1 kappa gamma1 beta0', real=True, finite=True)
E=beta0*(a1**2*kappa*gamma1+1)+2*kappa*(a1*gamma1+1)**2
E_family1=sp.factor(E.subs({a1:1,kappa:1}))
expected=(gamma1+1)*(beta0+2*(gamma1+1))
assert sp.expand(E_family1-expected)==0

E_rtk=sp.simplify(E.subs({a1:1,kappa:1,gamma1:-1,beta0:2}))
assert E_rtk==0
beta_other=sp.simplify(-2*(gamma1+1))
assert beta_other.subs(gamma1,-1)==0
assert beta_other.subs(gamma1,-1)!=2

out={
  'classification':'RTK_ROUTE_B_U1_FAMILY1_EQ543_FIXED_SLICE_PASS',
  'eq543_original':str(E),
  'eq543_family1_factorized':str(E_family1),
  'rtk_partial_slice':p,
  'rtk_eq543_residual':str(E_rtk),
  'branch_A':'gamma1=-1; beta0 remains algebraically free in Eq. (5.43), including beta0=2',
  'branch_B':'beta0=-2*(gamma1+1); at gamma1=-1 gives beta0=0 and excludes beta0=2',
  'matter_frame_note':'a2=0 is an explicit representative choice, not an RTK derivation; it does not enter Eq. (5.43)',
  'non_claims':[
    'not an independent derivation of the published PPN solution',
    'not a coupled gravity+RTK scalar Hamiltonian DOF count',
    'not a Newton/static spherical solution',
    'not a radiative-stability or strong-coupling result'
  ],
  'next_gate':'keep lambda_HL symbolic in the coupled constraint/DOF calculation; only after an admissible domain is derived freeze a complete same-action tuple'
}
(ROOT/'u1_family1_eq543_fixed_slice_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_FAMILY1_EQ543_FIXED_SLICE_PASS',json.dumps(out,sort_keys=True))
