#!/usr/bin/env python3
"""Exact Dirac-projection theorem for the frozen elliptic U(1) compensator.

The coupled primary-mixing audit shows that G=p_nu+J_A_total has a nonzero
Poisson bracket with p_Q.  The correct next step is not to assume four isolated
auxiliary second-class constraints.  Instead use the genuine secondary

    C_L = ell Q-H0 = 0,

which together with p_Q forms an everywhere-invertible second-class pair for
ell>0.  Project the U(1) source and gauge-pair constraint along this pair:

    Jhat = J - C_L/ell,
    Ghat = G - C_L/ell = p_nu+Jhat.

For J=Jg-H0+Q this gives

    Jhat = Jg-(1-1/ell) H0 = Jg-a1_eff H0.

Jhat and Ghat have zero p_Q bracket exactly.  After Dirac elimination of
(p_Q,C_L), Q=H0/ell and the reduced Hamiltonian is precisely the previously
certified scale-transfer Hamiltonian.  The remaining Lambda coordinate drops
out on C_L=0; p_Lambda is then a trivial first-class multiplier constraint.
Thus Q,Lambda add zero physical DOF in the correctly coupled reduction.

This theorem restores the correct reduced constraint architecture but does NOT
prove the remaining four U(1) scalar constraints have nonzero rank.  That rank
must be recomputed for Jhat,Hperp_hat,phi_hat with the metric-dependent elliptic
operator retained.
"""
import json
import sympy as sp

# Canonical auxiliary pair and symbolic old-sector functions.
Q,pQ,Lam,pLam=sp.symbols('Q p_Q Lambda p_Lambda', finite=True)
ell=sp.symbols('ell', positive=True, finite=True)
H0,Jg,pnu,N,A,Acal=sp.symbols('H0 Jg p_nu N A Acal', finite=True)

# Auxiliary canonical PB suffices for the projection theorem; all old-sector
# variables are spectators here.
def PBaux(f,g):
    return sp.simplify(
        sp.diff(f,Q)*sp.diff(g,pQ)-sp.diff(f,pQ)*sp.diff(g,Q)
        + sp.diff(f,Lam)*sp.diff(g,pLam)-sp.diff(f,pLam)*sp.diff(g,Lam)
    )

CL=ell*Q-H0
J=Jg-H0+Q
G=pnu+J
assert PBaux(pQ,CL)==-ell
assert PBaux(CL,pQ)==ell
assert sp.simplify(ell)>0

Jhat=sp.simplify(J-CL/ell)
Ghat=sp.simplify(G-CL/ell)
aeff=sp.simplify(1-1/ell)
assert sp.simplify(Jhat-(Jg-aeff*H0))==0
assert sp.simplify(Ghat-(pnu+Jhat))==0
assert PBaux(Jhat,pQ)==0
assert PBaux(Ghat,pQ)==0
assert PBaux(Jhat,CL)==0
assert PBaux(Ghat,CL)==0

# Dirac bracket for chi=(pQ,CL).  Its matrix determinant is ell^2 > 0.
C=sp.Matrix([[0,-ell],[ell,0]])
Cinv=sp.simplify(C.inv())
assert sp.simplify(C.det()-ell**2)==0

# For any projected old-sector functions F,G that are independent of Q,pQ,
# their brackets with pQ vanish, so the auxiliary-pair Dirac correction is zero.
f1,f2=sp.symbols('f1 f2', finite=True)
# Encode the structural statement directly: vectors have only possible CL
# component and no pQ component, hence v^T C^-1 w=0.
v2,w2=sp.symbols('v2 w2', finite=True)
v=sp.Matrix([0,v2])
w=sp.Matrix([0,w2])
assert sp.simplify((v.T*Cinv*w)[0])==0

# Exact reduced Hamiltonian in the matter+auxiliary A sector.
Hm=N*H0-(A-Acal)*H0
Haux=(A-Acal)*Q+Lam*CL
Qsol=H0/ell
Hred=sp.factor((Hm+Haux).subs(Q,Qsol).subs(CL,0))
expected_Hred=sp.factor(N*H0-aeff*(A-Acal)*H0)
assert sp.simplify(Hred-expected_Hred)==0
assert sp.diff(expected_Hred,Lam)==0

# The leftover pLambda commutes with the reduced Hamiltonian and projected
# constraints in this auxiliary support algebra: Lambda is a pure multiplier
# coordinate after C_L is imposed.
assert PBaux(pLam,expected_Hred)==0
assert PBaux(pLam,Jhat)==0
assert PBaux(pLam,Ghat)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_DIRAC_PROJECTION_PASS',
  'status_scope':'GREEN_EXACT_AUXILIARY_DIRAC_REDUCTION_REMAINING_U1_RANK_PENDING',
  'frozen_parent':'research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json',
  'genuine_second_class_pair':{
    'constraints':['p_Q','C_Lambda=ell Q-H0'],
    'poisson_matrix':'[[0,-ell],[ell,0]]',
    'determinant':'ell^2 > 0 for every physical k and M_c>0',
    'solution':'Q=H0/ell, p_Q=0'
  },
  'projected_constraints':{
    'Jhat':'J_A_total-C_Lambda/ell = J_A^(g)-a1_eff H0',
    'Ghat':'G-C_Lambda/ell = p_nu+Jhat',
    'a1_eff':'1-1/ell = k_phys^2/(M_c^2+k_phys^2)',
    'brackets_with_pQ':'{Jhat,p_Q}={Ghat,p_Q}=0 exactly',
    'brackets_with_CLambda':'zero in the auxiliary canonical support algebra'
  },
  'dirac_bracket_result':'For projected functions independent of Q,p_Q, the (p_Q,C_Lambda) Dirac-bracket correction vanishes because both p_Q components of the constraint-bracket vectors are zero.',
  'reduced_hamiltonian':'H_red=N H0-a1_eff(A-Acal)H0 + old gravity/RTK/shift terms',
  'lambda_sector':'After C_Lambda=0 the reduced Hamiltonian is Lambda-independent; p_Lambda is a trivial first-class multiplier constraint, removing the Lambda canonical pair.',
  'auxiliary_physical_dof_count':'0: one second-class pair (p_Q,C_Lambda) removes one configuration DOF and one first-class p_Lambda removes the other.',
  'interpretation':'The primary mixing is resolved by an exact change to the genuine coupled Dirac basis, not by postulating C_Q. The reduced U(1) problem is the original exceptional-surface constraint problem with the matter A-source replaced by the exact filtered coupling a1_eff(k).',
  'impact_on_conditional_schur_gate':'The earlier 8x8 Schur identity remains algebraically true for its assumed basis but is not the preferred coupled Dirac basis. The physical rank gate should now be run on the reduced four-constraint U(1) sector built from Jhat.',
  'non_claims':[
    'does not yet prove the reduced four-constraint U(1) scalar block is rank four',
    'does not establish finite-k absence of rank zeros caused by metric dependence of ell^{-1}',
    'does not choose M_c or lambda_HL',
    'does not address radiative regeneration of the exceptional eta1,eta2 operators'
  ],
  'next_gate':'derive H_perp_hat and phi_hat from preservation of pi_N and Ghat in the reduced Hamiltonian, then compute the exact 4x4 Poisson/Pfaffian rank with ell^{-1} treated as the spatial elliptic operator rather than a constant fit parameter.'
}
with open('u1_elliptic_compensator_dirac_projection_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
