#!/usr/bin/env python3
"""Dirac-Bergmann primary-mixing audit for the frozen elliptic U(1) compensator.

The earlier isolated auxiliary audit treated p_Q and p_Lambda as if their
preservation independently generated C_Q and C_Lambda.  In the fully coupled
system, however, the U(1) primary gauge-pair constraint is

    G = p_nu + J_A_total,
    J_A_total = J0 + Q,

where J0 contains the gravity+ordinary-matter contribution but is independent
of Q,p_Q.  Hence {G,p_Q}=+1 exactly.  The primary p_Q consistency equation is
therefore mixed with the multiplier of G, while preservation of G is mixed with
the p_Q multiplier.

On the regular D_i nu=0 slice the canonical Hamiltonian support is

    H_c = H_rest + A (J0+Q) + Lambda (ell Q-H0),

up to sign/orientation conventions that do not affect the nonzero primary
bracket.  This gate proves the multiplier mixing and therefore forbids treating
C_Q and the old would-be phi_A as independent first-generation secondaries
without completing the full Dirac chain.

It is not a no-go theorem: after J_A_total=0 one may replace G by p_nu=G-J_A,
so the U(1) gauge direction can reorganize.  The actual tertiary chain and final
first/second-class count remain to be derived.
"""
import json
import sympy as sp

nu,pnu,Q,pQ,Lam,pLam,A,pA,N,pN=sp.symbols(
    'nu p_nu Q p_Q Lambda p_Lambda A p_A N p_N', finite=True
)
J0,H0,ell=sp.symbols('J0 H0 ell', finite=True, nonzero=True)
uG,uQ,uLam,uA,uN=sp.symbols('u_G u_Q u_Lambda u_A u_N', finite=True)
Phi,Hperp=sp.symbols('Phi H_perp', finite=True)

coords=[nu,Q,Lam,A,N]
moms=[pnu,pQ,pLam,pA,pN]

def PB(f,g):
    return sp.simplify(sum(sp.diff(f,q)*sp.diff(g,p)-sp.diff(f,p)*sp.diff(g,q)
                           for q,p in zip(coords,moms)))

J=J0+Q
G=pnu+J
CL=ell*Q-H0
CQ=A+ell*Lam
Hc_support=A*J+Lam*CL

# Exact primary mixing.
assert PB(G,pQ)==1
assert PB(pQ,G)==-1
assert PB(G,pLam)==0
assert PB(G,pA)==0
assert PB(G,pN)==0

# The support part of the total Hamiltonian. H_rest contributes the abstract
# would-be old G-preservation source Phi and full lapse source Hperp, but has no
# Q/Lambda primary-momentum multipliers.
HT_support=Hc_support+uG*G+uQ*pQ+uLam*pLam+uA*pA+uN*pN

dotG_support=sp.expand(PB(G,HT_support))
dotpQ=sp.expand(PB(pQ,HT_support))
dotpLam=sp.expand(PB(pLam,HT_support))
dotpA=sp.expand(PB(pA,HT_support))

assert sp.simplify(dotG_support-uQ)==0
assert sp.simplify(dotpQ+CQ+uG)==0
assert sp.simplify(dotpLam+CL)==0
assert sp.simplify(dotpA+J)==0

# Including H_rest, preservation equations have the exact multiplier structure
#   dot G = Phi + u_Q = 0  -> u_Q=-Phi, not Phi=0;
#   dot pQ = -C_Q-u_G = 0 -> u_G=-C_Q, not C_Q=0.
sol_uQ=sp.solve(sp.Eq(Phi+uQ,0),uQ)[0]
sol_uG=sp.solve(sp.Eq(-CQ-uG,0),uG)[0]
assert sp.simplify(sol_uQ+Phi)==0
assert sp.simplify(sol_uG+CQ)==0

# By contrast pLambda and pA are not primary-mixed with G and do generate the
# first-generation secondaries C_Lambda and J_A_total.
assert PB(pLam,G)==0 and PB(pA,G)==0

# Once J_A_total is imposed, the old primary gauge combination reorganizes to
# p_nu exactly: G-J=p_nu. This prevents overinterpreting primary mixing as a
# proof of U(1) gauge-symmetry loss.
assert sp.simplify(G-J-pnu)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_PRIMARY_MIXING_DIRAC_AUDIT_PASS',
  'status_scope':'YELLOW_PRIMARY_MIXING_PROVED_NAIVE_EIGHT_CONSTRAINT_BASIS_NOT_YET_JUSTIFIED_FULL_CHAIN_PENDING',
  'frozen_parent':'research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json',
  'primary_constraints_relevant':['G=p_nu+J_A_total','p_Q','p_Lambda','p_A','p_N'],
  'exact_nonzero_primary_bracket':'{G,p_Q}=+1 (orientation convention)',
  'regular_slice_support':{
    'J_A_total':'J0+Q',
    'C_Q':'A+ell Lambda',
    'C_Lambda':'ell Q-H0'
  },
  'first_consistency_generation':{
    'G':'dot G=Phi+u_Q=0 -> fixes u_Q=-Phi; does not by itself impose old phi_A=0',
    'p_Q':'dot p_Q=-C_Q-u_G=0 -> fixes u_G=-C_Q; does not by itself impose C_Q=0',
    'p_Lambda':'dot p_Lambda=-C_Lambda=0 -> C_Lambda is a genuine secondary',
    'p_A':'dot p_A=-J_A_total=0 -> J_A_total is a genuine secondary',
    'p_N':'still generates the full H_perp because {p_N,G}=0 on the frozen a2=0 regular slice'
  },
  'basis_correction':'The conditional 8x8 Schur basis (p_N,J_A,H_perp,phi_A,p_Q,p_Lambda,C_Q,C_Lambda) must not be called the actual Dirac constraint basis until the consistency chain of J_A,C_Lambda,H_perp is completed and any tertiary replacements for phi_A/C_Q are derived.',
  'gauge_reorganization':'After J_A_total=0, G-J_A_total=p_nu exactly, so the primary mixing alone does not prove loss of the U(1) gauge direction.',
  'impact_on_previous_results':{
    'canonical_affinity':'still valid',
    'source_transfer':'still valid as an algebraic source relation',
    'isolated_auxiliary_det_ell4':'valid only for the isolated four-constraint assumption, not yet the coupled Dirac chain',
    'schur_reduction':'valid as a conditional matrix identity if that eight-constraint basis is actually generated, but not yet a full DOF proof'
  },
  'non_claims':[
    'does not prove the elliptic compensator has the wrong final DOF count',
    'does not prove U(1) gauge symmetry is broken',
    'does not determine the tertiary constraints generated by J_A,C_Lambda,H_perp consistency',
    'does not choose M_c or lambda_HL'
  ],
  'next_gate':'perform the full Dirac-Bergmann chain with the mixed primary pair (G,p_Q): derive consistency of J_A_total, C_Lambda and H_perp after substituting u_Q=-Phi and u_G=-C_Q, identify all tertiary constraints, then classify the final first/second-class rank and physical DOF count.'
}
with open('u1_elliptic_compensator_primary_mixing_dirac_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
