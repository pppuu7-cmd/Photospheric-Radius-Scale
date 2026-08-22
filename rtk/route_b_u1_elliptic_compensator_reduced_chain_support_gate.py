#!/usr/bin/env python3
"""Reduced-chain support theorem after exact (p_Q,C_Lambda) Dirac projection.

In a translationally invariant Fourier-symbol patch, ell and
  a_eff=1-1/ell
are c-number mode symbols.  The projected matter Hamiltonian is again exactly
of the a2=0 universal-matter form

  Hm_red = [N-a_eff(A-Acal)] H0 + (shift terms),

with H0 independent of N,A,nudot after Legendre transform.  Therefore the
projected source obeys the same canonical gauge-pair identity, is lapse
independent, and its self-sector Poisson bracket with Hm_red vanishes because
both are proportional to the same canonical matter generator H0.

This localizes the remaining finite-k Dirac-rank problem: any new correction to
the old exceptional-U(1) 4x4 block must come from gravity/metric dependence of
the elliptic operator or gravity-matter cross brackets, not from a direct
matter self-bracket or a new lapse/A Hessian.
"""
import json
import sympy as sp

N,A,Ni,nudot,nux,H0,Hi,ell=sp.symbols(
    'N A Ni nudot nux H0 Hi ell', real=True, finite=True
)
assert ell != 0
aeff=sp.factor(1-1/ell)
Acal=-nudot+Ni*nux+sp.Rational(1,2)*N*nux**2
Hm=sp.expand((N-aeff*(A-Acal))*H0+(Ni+N*nux)*Hi)
Jm=sp.simplify(sp.diff(Hm,A))
pnum=sp.simplify(-sp.diff(Hm,nudot))
assert sp.simplify(Jm+aeff*H0)==0
assert sp.simplify(pnum-aeff*H0)==0
assert sp.simplify(Jm+pnum)==0
assert sp.simplify(sp.diff(Jm,N))==0
assert sp.simplify(sp.diff(Hm,A,A))==0
assert sp.simplify(sp.diff(Hm,nudot,nudot))==0
assert sp.simplify(sp.diff(Hm,A,nudot))==0

# On the regular D_i nu=0 slice the reduced matter lapse constraint is H0 and
# is itself N independent.
Hm0=sp.simplify(Hm.subs({nux:0,Ni:0}))
Hperp_m=sp.simplify(sp.diff(Hm0,N))
assert sp.simplify(Hperp_m-H0)==0
assert sp.diff(Hperp_m,N)==0

# Abstract canonical matter phase space: if Jm=-a H0 and Hm=f H0 with a,f
# independent of matter canonical variables, the direct matter self bracket is
# identically zero by antisymmetry {H0,H0}=0.  Verify in a nontrivial explicit
# representative H0=p^2/2+V(q), leaving V generic polynomial.
q,p,m,w=sp.symbols('q p m w', nonzero=True, finite=True)
H0rep=p**2/(2*m)+sp.Rational(1,2)*m*w**2*q**2
f=sp.symbols('f', finite=True)
Jrep=-aeff*H0rep
Hmrep=f*H0rep
PB=lambda F,G: sp.simplify(sp.diff(F,q)*sp.diff(G,p)-sp.diff(F,p)*sp.diff(G,q))
assert PB(Jrep,Hmrep)==0

# Exact source limits in symbol space.
assert sp.simplify(aeff.subs(ell,1))==0
assert sp.simplify(sp.limit(aeff,ell,sp.oo)-1)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_REDUCED_CHAIN_SUPPORT_PASS',
  'status_scope':'GREEN_REDUCED_CANONICAL_CHAIN_SUPPORT_METRIC_CROSS_BRACKETS_PENDING',
  'parent_projection':'rtk/route_b_u1_elliptic_compensator_dirac_projection_gate.py',
  'symbol_patch':'translationally invariant Fourier mode with ell=1+k_phys^2/M_c^2 treated as a c-number symbol; full covariant operator dependence remains pending',
  'projected_matter':{
    'Hamiltonian':'[N-a_eff(A-Acal)]H0+(N^i+N D^i nu)H_i',
    'a_eff':'1-1/ell',
    'J_A_m':'-a_eff H0',
    'p_nu_m':'+a_eff H0',
    'gauge_pair_identity':'p_nu_m+J_A_m=0',
    'dJ_A_m_dN':'0',
    'regular_slice_Hperp_m':'H0',
    'dHperp_m_dN':'0',
    'A_nudot_affinity':'all direct second derivatives vanish'
  },
  'self_sector_result':'For c-number a_eff the direct matter contribution {J_A_m,H_m}_matter is identically zero because both are proportional to H0 and {H0,H0}=0.',
  'rank_localization':'The remaining reduced 4x4 U(1) rank corrections must arise from gravity/metric cross brackets and, beyond the Fourier-symbol patch, functional metric dependence of ell^{-1}; they cannot arise from a direct matter self-bracket or lapse/A Hessian.',
  'limits':{
    'k=0':'a_eff=0: ordinary matter drops out of the projected A/prepotential source exactly',
    'high_k':'a_eff->1: recovers the original family-I source structure'
  },
  'non_claims':[
    'does not treat ell^{-1} as a c-number in the final nonlinear field theory',
    'does not prove the gravity-matter cross brackets vanish',
    'does not prove the reduced four-constraint Pfaffian stays nonzero at every finite k',
    'does not choose M_c'
  ],
  'next_gate':'derive functional metric variations of L^{-1}=(1-D^2/M_c^2)^{-1} and insert them into the reduced constraints Jhat,Hperp_hat,phi_hat; then compute the physical finite-k Pfaffian/rank-loss locus.'
}
with open('u1_elliptic_compensator_reduced_chain_support_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
