#!/usr/bin/env python3
"""C8 canonical-affinity theorem for the published U(1) universal matter frame.

Conventions follow arXiv:1310.6666, Eqs. (2.5), (4.2)-(4.3), in one local
spatial direction. For a2=0 the physical spatial metric equals gij, while

  Nbar = (1-a1*sigma) N = N-a1*(A-Acal),
  Acal = -nudot + Ni*nux + N*nux**2/2,
  Nbar^i = Ni + N*nux.

Take any matter sector already Legendre transformed with respect to its own
velocities, with ADM generators H0 and Hi independent of N,A,nudot. Its
canonical Hamiltonian contribution is Hm=Nbar*H0+Nbar_i*Hi.

This gate proves exactly that Hm is affine in N,A,nudot and that the matter
contributions satisfy p_nu^m + J_A^m = 0 and d J_A^m/dN = 0. Therefore the
universal a2=0 matter frame does not by itself destroy the two algebraic
identities behind the exceptional U(1) primary/secondary-constraint chain.
A full coupled Poisson-matrix calculation is still mandatory.
"""
import json
import sympy as sp

N,A,Ni,nudot,nux,a1=sp.symbols('N A Ni nudot nux a1', real=True, finite=True)
H0,Hi=sp.symbols('H0 Hi', real=True, finite=True)

Acal=-nudot+Ni*nux+sp.Rational(1,2)*N*nux**2
sigma=(A-Acal)/N
Nbar=sp.expand((1-a1*sigma)*N)
Nibar=Ni+N*nux
Hm=sp.expand(Nbar*H0+Nibar*Hi)

# Matter contribution to canonical p_nu comes from L_m^can = p qdot - Hm.
pnu_m=sp.simplify(-sp.diff(Hm,nudot))
JA_m=sp.simplify(sp.diff(Hm,A))
piN_JA_bracket_proxy=sp.simplify(sp.diff(JA_m,N))

assert sp.simplify(Nbar-(N-a1*(A-Acal)))==0
assert sp.simplify(pnu_m+JA_m)==0
assert piN_JA_bracket_proxy==0

# Affinity in the variables whose nonlinear dependence would alter the primary
# multiplier structure. All pure second derivatives vanish identically.
affine_vars=(N,A,Ni,nudot)
second={}
for x in affine_vars:
    val=sp.simplify(sp.diff(Hm,x,x))
    second[str(x)]=val
    assert val==0

# A-N mixed derivative also vanishes, equivalent here to dJA/dN=0.
assert sp.simplify(sp.diff(Hm,A,N))==0

out={
  'classification':'RTK_ROUTE_B_U1_A2ZERO_CANONICAL_AFFINITY_GATE_PASS',
  'matter_frame':{'a2':0,'Nbar':str(Nbar),'Nbar_i':str(Nibar)},
  'generic_matter_generators':{'H0':'independent of N,A,nudot after matter Legendre transform','Hi':'same assumption'},
  'matter_primary_identity':{'pnu_m':str(pnu_m),'JA_m':str(JA_m),'pnu_plus_JA':str(sp.simplify(pnu_m+JA_m))},
  'piN_JA_bracket_proxy_dJA_dN':str(piN_JA_bracket_proxy),
  'pure_second_derivatives_of_Hm':{k:str(v) for k,v in second.items()},
  'interpretation':'At a2=0, the published universal matter frame is canonically affine in lapse/gauge/prepotential variables and preserves p_nu^m+J_A^m=0 plus dJ_A^m/dN=0 for a generic ADM matter Hamiltonian generator.',
  'why_a2_zero_is_now_structurally_motivated':'a2=0 removes sigma dependence from the physical spatial metric, so the matter Hamiltonian generators do not acquire hidden A/N/nudot dependence through gbar_ij.',
  'non_claims':[
    'does not prove the full coupled secondary-constraint Poisson matrix has the pure-gravity rank',
    'does not prove a2 nonzero is impossible for every matter sector',
    'does not include the RTK mixed higher-spatial-derivative scalar term in the secondary-constraint algebra',
    'does not pass PPN, radiative, GW, or cutoff gates'
  ],
  'next_gate':'add the RTK Sigma Hamiltonian and mixed operator to the exceptional eta1=eta2=0 constraint chain, derive modified H_perp and phi_A, then compute their Poisson rank with lambda_HL symbolic'
}
open('u1_a2zero_canonical_affinity_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_A2ZERO_CANONICAL_AFFINITY_GATE_PASS',json.dumps(out,sort_keys=True))
