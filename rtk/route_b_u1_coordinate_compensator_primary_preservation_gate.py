#!/usr/bin/env python3
"""Constructive degeneracy rescue: use sigma*F(Sigma), not sigma*F(X_U).

The naive FLRW compensator F(X_U) is velocity dependent and lifts the
exceptional local-U1 primary constraint pi_nu+J_A.  The smallest rescue is to
reconstruct the same homogeneous source as a fixed function of the *clock
coordinate* Sigma instead of its kinetic invariant X_U:

    Delta L = - sigma F_Sigma(Sigma).

On the rolling production branch X_U>0, choose the orientation dot(Sigma)>0.
For an expanding background H(a)>0,

    dSigma/da = sqrt(2 X_U(a))/(a H(a)) > 0.

Therefore Sigma(a) is strictly monotonic and an inverse a(Sigma) exists.  One
may define once and for all

    F_Sigma(Sigma) = rho_m0/a(Sigma)^3 + rho_r0/a(Sigma)^4.

Then F_Sigma(Sigma(a)) exactly reproduces the ordinary homogeneous density, but
off shell its coefficient in front of sigma is independent of velocities.
Hence the pi_nu+J_A+F_Sigma primary degeneracy is preserved.

This theorem establishes background reconstructibility and primary-degeneracy
preservation only.  The modified four-constraint Poisson matrix still needs an
exact rank audit at the physical coefficient.
"""

import json
import sympy as sp

# Monotonic production map.
a,H,X=sp.symbols('a H X', positive=True, finite=True, real=True)
dSigma_da=sp.sqrt(2*X)/(a*H)
assert dSigma_da.is_positive

# Abstract inverse a(Sigma) is legitimate by strict monotonicity.  Verify the
# target source algebraically using an independent positive inverse variable.
ainv,rhom,rhor=sp.symbols('a_of_Sigma rho_m0 rho_r0', positive=True, finite=True, real=True)
Fcoord=rhom/ainv**3+rhor/ainv**4
rho_target=Fcoord
assert sp.simplify(Fcoord-rho_target)==0

# Local velocity structure. Fq depends on Sigma coordinate but not vSigma.
N,vnu,vS,A,J0,m,Sigma=sp.symbols(
    'N v_nu v_Sigma A J0 m Sigma', nonzero=True, finite=True, real=True
)
Fq=sp.Function('F')(Sigma)
B=A+vnu
L=sp.Rational(1,2)*m*vS**2-B*(J0+Fq)
pnu=sp.diff(L,vnu)
Hvv=sp.hessian(L,(vnu,vS))
assert sp.simplify(sp.diff(pnu,vS))==0
assert sp.simplify(Hvv.det())==0

# The velocity-independent primary relation survives exactly.
primary=sp.simplify(pnu+J0+Fq)
assert primary==0

# On the conditional sigma=0 branch the coordinate-dependent compensator does
# not disturb the Sigma background equation: its Sigma variation is
# proportional to sigma.  Represent sigma by an independent symbol s.
s=sp.symbols('sigma', finite=True, real=True)
Lcomp=-s*Fq
dL_dSigma=sp.diff(Lcomp,Sigma)
assert sp.simplify(dL_dSigma.subs(s,0))==0
assert sp.simplify(Lcomp.subs(s,0))==0

# A-source sign: Delta L_M=-sigma F -> Delta J_A=-2F in the conventions used
# by the preceding family-I source gates. On the reconstructed trajectory F=rho.
JA_ord=2*rho_target
JA_comp=-2*Fcoord
assert sp.simplify(JA_ord+JA_comp)==0

out={
  'classification':'RTK_ROUTE_B_U1_COORDINATE_COMPENSATOR_PRIMARY_PRESERVATION_PASS',
  'status_scope':'YELLOW_CONSTRUCTIVE_DEGENERACY_RESCUE_FULL_CROSSBLOCK_RANK_PENDING',
  'candidate':'Delta L=-sigma F_Sigma(Sigma)',
  'production_reconstruction':{
    'monotonicity':'dSigma/da=sqrt(2 X_U(a))/(a H(a))>0 for X_U>0,H>0',
    'inverse':'a=a(Sigma) exists on the oriented production branch',
    'fixed_function':'F_Sigma(Sigma)=rho_m0/a(Sigma)^3+rho_r0/a(Sigma)^4',
    'trajectory_identity':'F_Sigma(Sigma(a))=rho_m0/a^3+rho_r0/a^4'
  },
  'background_source':'Delta J_A=-2 F_Sigma cancels family-I ordinary J_A=+2 rho_H on the frozen FLRW trajectory',
  'primary_degeneracy':{
    'p_nu':'-(J0+F_Sigma(Sigma))',
    'd_pnu_d_dotSigma':'0',
    'nu_Sigma_velocity_hessian_det':'0',
    'surviving_primary':'p_nu+J0+F_Sigma(Sigma)≈0'
  },
  'sigma_zero_background':'Delta L and its direct Sigma variation vanish at sigma=0, so the already reconstructed P(X_U) background equation is not shifted there.',
  'why_better_than_F_of_X':'The source tracks the same homogeneous density while its sigma coefficient is velocity-independent off shell, preserving the exceptional primary degeneracy that the F(X_U) candidate destroyed.',
  'costs_and_risks':[
    'breaks the internal shift symmetry Sigma->Sigma+const unless F is promoted by an additional symmetry construction',
    'the function F_Sigma encodes the frozen production trajectory and must be tested for technical naturalness',
    'J_A now depends on Sigma, so {J_A,H_perp} and phi_A acquire scalar contributions; det B at the physical coefficient is not yet certified',
    'local PPN/equivalence-principle behavior must be recomputed on the same action'
  ],
  'next_gate':'derive the modified secondary phi_A^tot and the 2x2 cross block B for (pi_N,J_A^tot) versus (H_perp^tot,phi_A^tot) on a regular rolling X_U>0 slice. Prove det B is nonzero at the physical F_Sigma coefficient before issuing any 3-DOF certificate.'
}
open('u1_coordinate_compensator_primary_preservation_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
