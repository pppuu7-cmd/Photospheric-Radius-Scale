#!/usr/bin/env python3
"""Exact canonical-affinity gate for the elliptic U1 matter compensator.

Use the already-certified a2=0 universal-matter Hamiltonian convention:

  Nbar = N-a1(A-Acal),
  Acal = -nudot + Ni*nux + N*nux^2/2,
  H_m = Nbar H0 + (Ni+N*nux) Hi,

with H0,Hi independent of N,A,nudot after matter Legendre transform.
For the family-I value a1=1, J_A^m=dH_m/dA=-H0.

Introduce neutral nondynamical Q,Lambda and the canonical compensator

  H_aux = (A-Acal) Q + Lambda [ ell Q - H0 ],
  ell(k)=1+k_phys^2/M_c^2 > 0.

The first term supplies J_A^aux=+Q while preserving the same U1 gauge-pair
identity p_nu^aux+J_A^aux=0.  The Lambda constraint filters the matter source.
At k=0 ell=1, Q=H0 and the ordinary A source cancels exactly. At high k the
fraction Q/H0=1/ell tends to zero.

This gate proves canonical affinity and the isolated auxiliary constraint rank;
it does not yet prove the full gravity+RTK+matter Dirac matrix rank.
"""
import json
import sympy as sp

N,A,Ni,nudot,nux,H0,Hi,Q,Lam,ell=sp.symbols(
    'N A Ni nudot nux H0 Hi Q Lambda ell', real=True, finite=True
)
a1=sp.Integer(1)
Acal=-nudot+Ni*nux+sp.Rational(1,2)*N*nux**2
Nbar=sp.expand(N-a1*(A-Acal))
Nibar=Ni+N*nux
Hm=sp.expand(Nbar*H0+Nibar*Hi)
Haux=sp.expand((A-Acal)*Q + Lam*(ell*Q-H0))
Htot=sp.expand(Hm+Haux)

# Canonical prepotential/A gauge-pair identities.
pnu_m=sp.simplify(-sp.diff(Hm,nudot))
JA_m=sp.simplify(sp.diff(Hm,A))
pnu_aux=sp.simplify(-sp.diff(Haux,nudot))
JA_aux=sp.simplify(sp.diff(Haux,A))
pnu_tot=sp.simplify(-sp.diff(Htot,nudot))
JA_tot=sp.simplify(sp.diff(Htot,A))
assert sp.simplify(JA_m+H0)==0 and sp.simplify(pnu_m-H0)==0
assert sp.simplify(JA_aux-Q)==0 and sp.simplify(pnu_aux+Q)==0
assert sp.simplify(pnu_tot+JA_tot)==0
assert sp.simplify(sp.diff(JA_tot,N))==0

# The new Hamiltonian remains affine in A and nudot; no new A/nudot Hessian.
assert sp.simplify(sp.diff(Htot,A,A))==0
assert sp.simplify(sp.diff(Htot,nudot,nudot))==0
assert sp.simplify(sp.diff(Htot,A,nudot))==0

# Auxiliary primary constraints p_Q=p_Lambda=0 generate the two secondaries.
# C_Q=dH/dQ=(A-Acal)+ell Lambda; C_L=dH/dLambda=ell Q-H0.
CQ=sp.simplify(sp.diff(Haux,Q))
CL=sp.simplify(sp.diff(Haux,Lam))
assert sp.simplify(CQ-(A-Acal+Lam*ell))==0
assert sp.simplify(CL-(Q*ell-H0))==0

# Poisson matrix on (pQ,pLambda,CQ,CL); canonical signs only affect orientation.
M=sp.Matrix([
    [0,0,0,-ell],
    [0,0,-ell,0],
    [0,ell,0,0],
    [ell,0,0,0],
])
assert sp.simplify(sp.factor(M.det())-ell**4)==0

# Solve the auxiliary branch algebraically.
solQ=sp.solve(sp.Eq(CL,0),Q)[0]
solLam=sp.solve(sp.Eq(CQ,0),Lam)[0]
assert sp.simplify(solQ-H0/ell)==0
assert sp.simplify(solLam-(-A+Acal)/ell)==0
JA_on_aux=sp.simplify(JA_tot.subs(Q,solQ))
assert sp.simplify(JA_on_aux-H0*(1/ell-1))==0
assert sp.simplify(JA_on_aux.subs(ell,1))==0
assert sp.simplify(sp.limit(JA_on_aux,ell,sp.oo)+H0)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_CANONICAL_AFFINITY_PASS',
  'status_scope':'YELLOW_CANONICAL_GAUGE_PAIR_AND_AUXILIARY_RANK_PASS_FULL_COUPLED_DIRAC_PENDING',
  'frozen_family_I_input':{'a1':1,'a2':0},
  'canonical_candidate':{
    'ordinary_matter':'H_m=[N-(A-Acal)] H0 + (N^i+N D^i nu) H_i',
    'auxiliary':'H_aux=(A-Acal) Q + Lambda[(1-D^2/M_c^2)Q-H0]',
    'fourier_ell':'ell=1+k_phys^2/M_c^2 > 0'
  },
  'exact_primary_results':{
    'J_A_m':'-H0',
    'p_nu_m':'+H0',
    'J_A_aux':'+Q',
    'p_nu_aux':'-Q',
    'p_nu_total_plus_J_A_total':'0',
    'dJ_A_total_dN':'0',
    'A_nudot_affinity':'all A-A, nudot-nudot and A-nudot second derivatives vanish'
  },
  'auxiliary_constraints':{
    'C_Q':'A-Acal+ell Lambda=0',
    'C_Lambda':'ell Q-H0=0',
    'solution_Q':'H0/ell',
    'solution_Lambda':'-(A-Acal)/ell',
    'four_constraint_det':'ell^4',
    'isolated_auxiliary_dof':0
  },
  'source_transfer':{
    'J_A_total_on_auxiliary_branch':'H0(1/ell-1)',
    'k0':'ell=1 -> J_A_total=0',
    'high_k':'ell->infinity -> J_A_total=-H0, recovering the original local family-I source'
  },
  'interpretation':'The scale-separated compensator can be written in the same canonical a2=0 convention without destroying the p_nu+J_A primary identity or introducing an isolated propagating Q/Lambda mode. It interpolates from exact FLRW A-source cancellation to the original local family-I source.',
  'non_claims':[
    'does not yet prove the enlarged full second-class matrix factorizes or stays rank-complete after gravity/RTK/matter cross brackets are included',
    'does not establish finite-k cosmological perturbation agreement',
    'does not establish PPN/equivalence-principle bounds, radiative stability, cutoff or compact-object behavior'
  ],
  'next_gate':'freeze this canonical functional form with M_c>0 symbolic, derive the enlarged full Dirac matrix including the Q,Lambda cross brackets with H_perp and phi_A, and determine whether the original four U1 second-class constraints plus the four auxiliary constraints remain independent for all physical k>0. Only then scan an observational M_c window.'
}
with open('u1_elliptic_compensator_canonical_affinity_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
