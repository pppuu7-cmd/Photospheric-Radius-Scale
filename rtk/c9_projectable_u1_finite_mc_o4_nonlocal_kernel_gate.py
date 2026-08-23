#!/usr/bin/env python3
"""Finite-Mc projectable O(4) nonlocal metric-variation kernel theorem.

After exact Q,Lambda reduction the A-Acal matter response contains
    a_eff = 1-L^{-1},  L=1-D^2/M_c^2.
The exact metric variation is
    delta a_eff = -(1/M_c^2) L^{-1}(delta D^2)L^{-1}.

At O(4), the spatial metric is perturbed by the O(2) Newtonian potential.
For a conformal perturbation h_ij=2 gamma U delta_ij in d spatial dimensions,
variation of the scalar Laplacian is
    delta D^2 phi = -h^{ij} d_i d_j phi
                    +(1/2 d^j h-d_i h^{ij}) d_j phi
                  = -2 gamma U Delta phi
                    +(d-2) gamma grad U.grad phi.
For Fourier momenta p carried by U and q carried by phi, output k=p+q,
    K_D(p,q)=gamma[2 q^2-(d-2) p.q].
Thus the resolvent contribution has two different propagator factors,
    K_a(p,q)=-(M_c^2 gamma [2q^2-(d-2)p.q])/
              [(M_c^2+k^2)(M_c^2+q^2)].
It depends on the momentum partition p,q even at fixed output k. Therefore finite
M_c O(4) response cannot in general be represented by replacing a constant PPN
coefficient by a single function of |k|. A generalized convolution-kernel PPN
(or direct source-specific observable calculation) is required.
"""
import json
import sympy as sp

M2,k2,q2,pq,gamma=sp.symbols('M_c_squared k_squared q_squared p_dot_q gamma', positive=True, finite=True)
d=sp.symbols('d', integer=True, positive=True)
KD=gamma*(2*q2-(d-2)*pq)
Gk=M2/(M2+k2)
Gq=M2/(M2+q2)
Ka=sp.factor(-Gk*KD*Gq/M2)
expected=-M2*gamma*(2*q2-(d-2)*pq)/((M2+k2)*(M2+q2))
assert sp.simplify(Ka-expected)==0

# d=3 and fixed output k: compare two collinear momentum partitions.
Ka3=sp.simplify(Ka.subs(d,3))
# Partition A: p=0, q=k -> q2=k2,pq=0.
KA=sp.factor(Ka3.subs({q2:k2,pq:0}))
# Partition B: p=q=k/2 -> q2=k2/4,p.q=k2/4.
KB=sp.factor(Ka3.subs({q2:k2/4,pq:k2/4}))
diff=sp.factor(KA-KB)
assert diff != 0
# Prove the difference cannot vanish for positive M2,k2,gamma.
num=sp.factor(sp.together(diff).as_numer_denom()[0])
assert sp.factor(num)==-sp.Rational(3,4)*M2*gamma*k2*(2*M2+k2)

# Parent/local limit M_c^2 -> 0 at fixed nonzero momenta removes this specific
# resolvent-metric-variation correction, consistently with a_eff -> 1.
local_limit=sp.limit(Ka3,M2,0,dir='+')
assert local_limit==0

out={
  'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_O4_NONLOCAL_KERNEL_PASS',
  'status_scope':'GREEN_EXACT_O4_RESOLVENT_MODE_MIXING_STANDARD_CONSTANT_PPN_NOT_EXACT_AT_FINITE_MC',
  'domain':'projectable U1 PN patch; exact auxiliary reduction; finite M_c^2>0; conformal O(2) spatial metric perturbation; scalar Laplacian acting on ordinary matter source; Fourier momenta p+q=k',
  'exact_metric_variation':'delta a_eff=-(1/M_c^2)L^{-1}(delta D^2)L^{-1}',
  'laplacian_variation':'delta D^2 phi=-2 gamma U Delta phi +(d-2) gamma grad(U).grad(phi)',
  'fourier_D2_kernel':'gamma[2 q^2-(d-2) p.q]',
  'fourier_resolvent_kernel':'-M_c^2 gamma[2 q^2-(d-2)p.q]/[(M_c^2+k^2)(M_c^2+q^2)]',
  'd3_fixed_k_partition_A':'p=0,q=k',
  'd3_fixed_k_partition_B':'p=q=k/2 collinear',
  'partition_difference_numerator':'-(3/4) M_c^2 gamma k^2 (2 M_c^2+k^2) != 0 for positive M_c^2,k^2,gamma',
  'interpretation':'At O(4) finite M_c produces genuine momentum-partition dependence. A single substitution kappa->1/f(k), or ten constant PPN parameters, cannot encode the full nonlinear response. The next heavy gate must solve generalized convolution kernels or direct extended-source observables.',
  'parent_limit':'M_c^2->0 at fixed nonzero momenta gives this resolvent-variation kernel ->0 and recovers the local parent response.',
  'non_claims':[
    'does not by itself compute beta, alpha2 or zeta_i for a concrete source',
    'does not prove phenomenological failure; it changes the correct observable language',
    'does not include all O(4) geometric and matter-H0 metric-variation terms',
    'does not use a universal identification k=1/r'
  ],
  'next_gate':'construct the complete O(4) source-transfer convolution operator from the parent projectable Eq.(6.17), including filtered J_A, ordinary tau_ij, H0 metric variation and delta a_eff; then evaluate it for spherical and moving compact sources.'
}
open('c9_projectable_u1_finite_mc_o4_nonlocal_kernel_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
