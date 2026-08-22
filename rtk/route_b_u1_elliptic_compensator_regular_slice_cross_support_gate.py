#!/usr/bin/env python3
"""Exact regular-slice cross-support theorem for the frozen elliptic U(1) compensator.

Frozen canonical candidate:
  H_m   = [N-(A-Acal)] H0 + (N^i+N D^i nu) H_i
  H_aux = (A-Acal) Q + Lambda [ell Q-H0]
  ell   = 1+k_phys^2/M_c^2 > 0.

On the regular homogeneous-prepotential slice D_i nu=0,
  Acal=-nudot,
so neither C_Q=A-Acal+ell Lambda nor C_Lambda=ell Q-H0 has explicit lapse
support (H0 and ell are independent of N in canonical variables). Likewise the
lapse constraint H_perp has no Q/Lambda dependence on this slice. Therefore the
pi_N row of the old-vs-auxiliary cross matrix X vanishes exactly, while the
frozen source identity J_A=J_A(rest)-H0+Q forces {J_A,p_Q}=+1 and
{J_A,p_Lambda}=0 (orientation convention fixed below).

The still-undetermined brackets with C_Q,C_Lambda and phi_A are retained as
independent symbols. The gate then computes the exact Schur correction
X E^{-1} X^T and the Pfaffian of the deformed 4x4 old-U(1) block.

This is a support/rank-reduction theorem only. It does not assume the remaining
cross brackets vanish and does not claim full coupled rank before they are
derived from the frozen action.
"""
import json
import sympy as sp

ell=sp.symbols('ell', positive=True, finite=True)
N,A,nudot,H0,Q,Lam=sp.symbols('N A nudot H0 Q Lambda', finite=True)

# Regular D_i nu=0 slice.
Acal=-nudot
CQ=sp.expand(A-Acal+ell*Lam)
CL=sp.expand(ell*Q-H0)
assert sp.diff(CQ,N)==0
assert sp.diff(CL,N)==0

# On this slice the matter+auxiliary Hamiltonian has lapse derivative H0 and
# no Q/Lambda dependence in H_perp. Gravity+neutral RTK pieces contain neither
# Q nor Lambda by construction.
Hm=sp.expand((N-(A-Acal))*H0)
Haux=sp.expand((A-Acal)*Q+Lam*(ell*Q-H0))
Hperp_maux=sp.simplify(sp.diff(Hm+Haux,N))
assert sp.simplify(Hperp_maux-H0)==0
assert sp.diff(Hperp_maux,Q)==0
assert sp.diff(Hperp_maux,Lam)==0

# Auxiliary second-class block in basis (pQ,pLambda,CQ,CLambda).
E=sp.Matrix([
    [0,0,0,-ell],
    [0,0,-ell,0],
    [0,ell,0,0],
    [ell,0,0,0],
])
Einv=sp.simplify(E.inv())
assert sp.simplify(E.det()-ell**4)==0

# Old basis: (pi_N, J_A, H_perp, phi_A).
# Proven structural entries:
#   row(pi_N)=0;
#   {J_A,pQ}=+1, {J_A,pLambda}=0;
#   {H_perp,pQ}={H_perp,pLambda}=0 on the regular slice.
# The unresolved entries are kept symbolic, not set to zero.
a,b,c,d,g,h,i,j=sp.symbols('a b c d g h i j', finite=True)
X=sp.Matrix([
    [0,0,0,0],
    [1,0,a,b],
    [0,0,c,d],
    [g,h,i,j],
])
Delta=sp.simplify(X*Einv*X.T)
assert Delta + Delta.T == sp.zeros(4)
assert Delta[0,:] == sp.zeros(1,4)
assert Delta[:,0] == sp.zeros(4,1)
assert sp.simplify(Delta[1,2]-d/ell)==0
assert sp.simplify(Delta[1,3]-(-a*h-b*g+j)/ell)==0
assert sp.simplify(Delta[2,3]-(-c*h-d*g)/ell)==0

# Generic old antisymmetric block and its Schur-deformed Pfaffian.
o12,o13,o14,o23,o24,o34=sp.symbols('o12 o13 o14 o23 o24 o34', finite=True)
O=sp.Matrix([
    [0,o12,o13,o14],
    [-o12,0,o23,o24],
    [-o13,-o23,0,o34],
    [-o14,-o24,-o34,0],
])
S=sp.simplify(O+Delta)
pf_O=sp.expand(o12*o34-o13*o24+o14*o23)
pf_S=sp.factor(S[0,1]*S[2,3]-S[0,2]*S[1,3]+S[0,3]*S[1,2])
expected=sp.factor(
    pf_O
    + (o12*(-c*h-d*g)
       - o13*(-a*h-b*g+j)
       + o14*d)/ell
)
assert sp.simplify(pf_S-expected)==0
assert sp.simplify(S.det()-pf_S**2)==0

# Algebraic genericity only: the Pfaffian is not the zero polynomial in the
# unresolved physical brackets. This does NOT prove that the actual frozen
# action cannot land on its zero locus.
assert sp.simplify(sp.diff(pf_S,o34)-o12)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_REGULAR_SLICE_CROSS_SUPPORT_PASS',
  'status_scope':'GREEN_EXACT_REGULAR_SLICE_SUPPORT_AND_PFAFFIAN_REDUCTION_PHYSICAL_CROSS_BRACKETS_PENDING',
  'frozen_parent':'research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json',
  'regular_slice':'D_i nu=0 with rolling X_U>0 allowed; ell and H0 canonical-lapse independent',
  'proven_cross_support':{
    'X_piN_row':'[0,0,0,0]',
    'bracket_JA_pQ':'+1',
    'bracket_JA_pLambda':'0',
    'bracket_Hperp_pQ':'0',
    'bracket_Hperp_pLambda':'0'
  },
  'unresolved_symbol_map':{
    'a':'{J_A,C_Q}', 'b':'{J_A,C_Lambda}',
    'c':'{H_perp,C_Q}', 'd':'{H_perp,C_Lambda}',
    'g':'{phi_A,p_Q}', 'h':'{phi_A,p_Lambda}',
    'i':'{phi_A,C_Q}', 'j':'{phi_A,C_Lambda}'
  },
  'schur_correction_nonzero_entries':{
    'Delta_23':'d/ell',
    'Delta_24':'(-a h-b g+j)/ell',
    'Delta_34':'(-c h-d g)/ell',
    'entries_touching_pi_N':'0'
  },
  'pfaffian_old':'o12 o34-o13 o24+o14 o23',
  'pfaffian_schur':'pf_old + [o12(-c h-d g)-o13(-a h-b g+j)+o14 d]/ell',
  'full_rank_on_regular_slice_iff':'pfaffian_schur != 0',
  'rank_loss_locus':'one exact Pfaffian equation after the eight unresolved physical brackets are derived; no X=0 assumption is permitted',
  'interpretation':'The auxiliary sector cannot modify any Schur entry touching pi_N on the regular D_i nu=0 slice. All possible rank change is compressed into the lower 3x3 antisymmetric sector and one explicit Pfaffian correction. The frozen candidate is therefore not algebraically forced to lose rank, but physical nonvanishing still depends on the remaining brackets.',
  'non_claims':[
    'does not prove the actual physical cross brackets a,b,c,d,g,h,i,j take generic independent values',
    'does not prove Pfaffian nonzero for all finite k',
    'does not choose M_c or lambda_HL',
    'does not replace the full coupled Dirac calculation off the D_i nu=0 regular slice'
  ],
  'next_gate':'derive a,b,c,d,g,h,i,j from the frozen canonical action, substitute them into this exact Pfaffian, and classify all finite-k zeros before any M_c fit.'
}
with open('u1_elliptic_compensator_regular_slice_cross_support_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
