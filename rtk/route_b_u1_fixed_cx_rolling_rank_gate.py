#!/usr/bin/env python3
"""Exact homogeneous rolling rank support for fixed C(X_U)=M_Pl^2/(2X_U).

For homogeneous Sigma with D_iSigma=0 and static/spatial lapse perturbations,
Theta=q/N and X=Theta^2/2. Therefore C=M_Pl^2/Theta^2 and
D_iTheta=-Theta a_i. The mixed operator is exactly

  C(DTheta)^2=M_Pl^2 a_i a^i

before any weak-field expansion. Multiplying by N gives exactly the same
lapse-gradient action as beta0_eff=2 in the Hořava convention. Hence the
rolling fixed-C action modifies the exceptional-U1 second-class cross block
only through the same L_V[g,a] operator class for which the external
Hamiltonian theorem states det B is weakly nonzero for arbitrary coefficients.
"""
import json
import sympy as sp

M,Theta,a2,N=sp.symbols('M_Pl Theta a2 N', positive=True, finite=True, real=True)
X=Theta**2/2
C=M**2/(2*X)
Lmix=sp.simplify(N*C*Theta**2*a2)
Leff=sp.simplify(N*M**2*a2)
assert sp.simplify(Lmix-Leff)==0
beta_eff=sp.simplify(2*Lmix/(N*M**2*a2))
assert beta_eff==2

# Cross block structural update remains only a->a+delta_a.
a,b,c,d,da=sp.symbols('a b c d delta_a', finite=True)
det_g=sp.expand(a*d-b*c)
det_c=sp.expand((a+da)*d-b*c)
assert sp.simplify(det_c-det_g-da*d)==0

out={
  'classification':'RTK_ROUTE_B_U1_FIXED_CX_ROLLING_RANK_PASS',
  'fixed_C':'M_Pl^2/(2X_U)',
  'rolling_conditions':['D_i Sigma=0','X_U=Theta_U^2/2>0','homogeneous rolling clock'],
  'exact_identity':'N C(X_U)(D_iTheta_U)^2 = N M_Pl^2 a_i a^i',
  'beta0_eff_static_spatial_lapse':2,
  'cross_block_update':'only {pi_N,H_perp}: a->a+delta_a; b,c,d unchanged by neutral invariant-shift scalar sector',
  'external_rank_input':'exceptional eta1=eta2=0 U1 Hamiltonian theorem: det B weakly nonzero for arbitrary L_V[g,a] coefficients',
  'result':'The fixed C(X_U) rolling branch lies exactly in the already-covered acceleration-operator class and does not force loss of the four second-class constraints on the homogeneous X_U>0 branch.',
  'scope':'homogeneous rolling / spatial-lapse rank support',
  'non_claims':[
    'does not exclude specially inhomogeneous rank-changing scalar configurations',
    'does not cover X_U=0',
    'does not establish radiative stability, PPN or cutoff'
  ],
  'next_gate':'reissue the classical coupled DOF certificate for the fixed scalar action using the regular X>0 slice and fixed-C velocity/Noether support'
}
open('u1_fixed_cx_rolling_rank_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
