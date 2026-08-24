#!/usr/bin/env python3
"""C10 exact A-source normalization bridge for the elliptic U(1) completion.

Preregistered target:
  research/theory_targets/RTK_C10_U1_A_SOURCE_NORMALIZATION_TARGET_v1.json

Primary conventions:
- Zhu-Shu-Wu-Wang arXiv:1110.5106: J_A=2 d(N L_M)/dA and
  R-2 Lambda_g = 8 pi G J_A.
- Lin-Mukohyama-Wang-Zhu arXiv:1310.6666: on the family-I
  a1=1,a2=0,Omega=1 slice, J_A=2 rho_H.

The existing compensator workbench was Hamiltonian.  This gate fixes the
sign/factor translation before those sources are inserted into metric equations.
"""
import json
import sympy as sp

A,Acal,H0,Q,Lam,ell=sp.symbols('A Acal H0 Q Lambda ell', real=True, finite=True)
k,a,Mc,G,dH0,psi=sp.symbols('k a M_c G delta_H0 psi', positive=True, finite=True, real=True)

Hm=-(A-Acal)*H0
Haux=(A-Acal)*Q + Lam*(ell*Q-H0)
H=sp.expand(Hm+Haux)
internal_A_coeff=sp.simplify(sp.diff(H,A))
assert internal_A_coeff == Q-H0

# For nondynamical A, L = p*qdot-H has no A in the kinetic term, so
# dL/dA=-dH/dA.  Primary U1 convention is J_A=2 d(N L_M)/dA;
# on background N=1 this gives the following projected source.
dL_dA=sp.simplify(-internal_A_coeff)
JA=sp.simplify(2*dL_dA)
assert JA == 2*(H0-Q)
# Old universal-matter limit Q=0 must reproduce family-I J_A=2 rho_H.
assert sp.simplify(JA.subs(Q,0)-2*H0)==0

# Elliptic constraint Q=H0/ell.
JA_filter=sp.factor(JA.subs(Q,H0/ell))
aeff=sp.simplify(1-1/ell)
assert sp.simplify(JA_filter-2*aeff*H0)==0

# On homogeneous FLRW, the separate linear-resolvent theorem gives
# delta Q = delta H0/ell for each k>0 perturbation mode.  Therefore
# delta J_A = 2 a_eff delta H0.
ell_fourier=1+k**2/(a**2*Mc**2)
aeff_fourier=sp.factor((1-1/ell_fourier))
assert sp.simplify(aeff_fourier-k**2/(k**2+a**2*Mc**2))==0
dJA=sp.factor(2*aeff_fourier*dH0)

# Primary flat-FLRW A constraint (sigma1=sigma2=Lambda_g=0):
# partial^2 psi = 2 pi G a^2 delta J_A.
# Fourier partial^2=-k^2.  For k>0, cancellation yields Helmholtz/Yukawa form.
psi_solution=sp.factor(-(2*sp.pi*G*a**2*dJA)/k**2)
psi_expected=-4*sp.pi*G*a**2*dH0/(k**2+a**2*Mc**2)
assert sp.simplify(psi_solution-psi_expected)==0
psi_GR=-4*sp.pi*G*a**2*dH0/k**2
ratio=sp.factor(psi_solution/psi_GR)
assert sp.simplify(ratio-aeff_fourier)==0
assert sp.limit(ratio,k,sp.oo)==1
assert sp.limit(ratio,k,0,dir='+')==0

out={
  'classification':'C10_U1_A_SOURCE_NORMALIZATION_AND_HELMHOLTZ_CONSTRAINT_PASS_SCOPED',
  'status_scope':'GREEN_EXACT_A_SECTOR_NORMALIZATION_FOR_K_GT_0_FULL_REDUCED_SCALAR_SYSTEM_STILL_OPEN',
  'internal_hamiltonian_A_coefficient':'Q-H0 = -a1_eff H0 after the elliptic constraint',
  'literature_J_A':'2(H0-Q) = +2 a1_eff H0 on the frozen family-I normalization',
  'linear_literature_delta_J_A':'2 a1_eff delta H0',
  'a1_eff':'k^2/(k^2+a^2 M_c^2) = k_phys^2/(k_phys^2+M_c^2)',
  'A_constraint_fourier_k_gt_0':'psi = -4 pi G a^2 delta H0/(k^2+a^2 M_c^2)',
  'equivalent_helmholtz_form':'(k^2+a^2 M_c^2) psi = -4 pi G a^2 delta H0',
  'GR_transfer_ratio_k_gt_0':'psi/psi_GR = a1_eff',
  'high_k_limit':'psi/psi_GR -> 1',
  'low_k_limit_k_to_0_plus':'psi/psi_GR -> 0; exact k=0 remains the separately certified homogeneous constraint and is not obtained by dividing by k^2',
  'critical_correction':'Prior internal files that write delta_J_A_total=-a1_eff delta H0 use the Hamiltonian/projected A-coefficient convention. They must not be inserted as the primary-literature J_A without the sign and factor-of-two translation certified here.',
  'prepotential_boundary':'The canonical p_nu/projected-prepotential source is not yet identified with the primary-literature J_varphi. That normalization/derivative map remains mandatory before the full scalar reduction.',
  'non_claims':[
    'does not close the prepotential constraint normalization',
    'does not close Hamiltonian/momentum/trace/traceless equations',
    'does not implement CLASS or produce a likelihood score',
    'does not assert the exact homogeneous k=0 mode is fixed by the divided Helmholtz equation'
  ],
  'target':'research/theory_targets/RTK_C10_U1_A_SOURCE_NORMALIZATION_TARGET_v1.json'
}
open('u1_A_source_normalization_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
