#!/usr/bin/env python3
"""C8 exact reduction of the coupled U(1) four-constraint rank problem.

Once the selected coupling preserves {pi_N,J_A}=0, the second-class candidate
basis C=(pi_N,J_A,H_perp,phi_A) has an antisymmetric Poisson matrix

    [ 0  0  a  b ]
    [ 0  0  c  d ]
    [-a -c  0  e ]
    [-b -d -e  0 ]

where a={pi_N,H_perp}, b={pi_N,phi_A}, c={J_A,H_perp},
d={J_A,phi_A}; e={H_perp,phi_A}. Exact algebra gives
 det M=(a*d-b*c)^2, independent of e.

Thus the full rank-4 question reduces to the nonsingularity of one 2x2 cross
block B=[[a,b],[c,d]]. If this survives coupling, adding exactly one Sigma
canonical pair to the exceptional U(1) gravity phase space gives 3 physical
DOF in d=3: two tensors plus the intended RTK scalar.
"""
import json
import sympy as sp

a,b,c,d,e=sp.symbols('a b c d e', finite=True)
M=sp.Matrix([
    [0,0,a,b],
    [0,0,c,d],
    [-a,-c,0,e],
    [-b,-d,-e,0],
])
B=sp.Matrix([[a,b],[c,d]])
detM=sp.factor(M.det())
detB=sp.factor(B.det())
assert sp.simplify(detM-detB**2)==0
assert e not in detM.free_symbols

# Conditional phase-space count: paper's gravity phase space plus one Sigma pair.
dsp=sp.symbols('dsp', integer=True, positive=True)
dimP_gravity=dsp**2+3*dsp+6
dimP_coupled=dimP_gravity+2
C1=2*dsp+2
C2=4
Ndof=sp.simplify((dimP_coupled-2*C1-C2)/2)
assert sp.simplify(Ndof-dsp*(dsp-1)/2)==0
assert Ndof.subs(dsp,3)==3

out={
  'classification':'RTK_ROUTE_B_U1_SECOND_CLASS_BLOCK_REDUCTION_PASS',
  'constraint_basis':['pi_N','J_A','H_perp','phi_A'],
  'matrix':str(M),
  'cross_block_B':str(B),
  'det_M':str(detM),
  'det_B':str(detB),
  'rank4_condition':'a*d-b*c != 0 weakly on the generic coupled phase space',
  'Hperp_phiA_bracket_relevance':'drops out of determinant exactly when {pi_N,J_A}=0',
  'conditional_DOF_count':{'dimension_d_formula':str(Ndof),'d3':3,'interpretation':'2 tensor + 1 intended RTK scalar if the four second-class constraints remain independent'},
  'non_claims':[
    'does not prove det(B) is nonzero after RTK coupling',
    'does not allow a symmetric-background rank drop to be mistaken for a nonlinear extra mode or its absence',
    'does not fix lambda_HL'
  ],
  'next_gate':'compute only the four coupled cross brackets a,b,c,d (or directly det B) with RTK Sigma sources and lambda_HL symbolic; no calculation of {H_perp,phi_A} is needed for the rank decision'
}
open('u1_second_class_block_reduction_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_SECOND_CLASS_BLOCK_REDUCTION_PASS',json.dumps(out,sort_keys=True))
