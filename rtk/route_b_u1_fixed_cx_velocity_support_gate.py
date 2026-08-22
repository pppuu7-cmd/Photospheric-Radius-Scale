#!/usr/bin/env python3
"""Re-audit velocity support after fixing C(X_U)=M_Pl^2/(2X_U).

The earlier U(1) mixed-velocity gate treated C as an external neutral state
coefficient.  The reconstructed scalar action now fixes C as a function of the
same scalar kinetic invariant X_U, so this dependence must be included before
carrying the classical DOF certification forward.

For one local Cartesian direction,
  Theta=(Sdot-(Ni-N*nux)Sx)/N,
  X=1/2(Theta^2-Sx^2),
  C=M^2/(2X),
  Lmix=C(Dx Theta)^2.

X contains the intended scalar velocity but no time velocity of N, Ni, A, nu,
or g_ij. Therefore the fixed C(X) cannot create a new gravity/gauge kinetic
direction.  The coefficient of (Dx Sdot)^2 remains C/N^2 and is nonzero on the
frozen timelike X>0 branch.
"""
import json
import sympy as sp

N,Ni,nux,Sx,Sdot=sp.symbols('N Ni nux Sx Sdot', nonzero=True, finite=True, real=True)
Nx,Nix,nuxx,Sxx,Sdotx=sp.symbols('Nx Nix nuxx Sxx Sdotx', finite=True, real=True)
M=sp.symbols('Mpl', positive=True, finite=True, real=True)
Ndot,Nidot,Adot,nudot,gdot=sp.symbols('Ndot Nidot Adot nudot gdot', finite=True, real=True)

V=Ni-N*nux
Vx=Nix-Nx*nux-N*nuxx
Theta=sp.simplify((Sdot-V*Sx)/N)
X=sp.simplify((Theta**2-Sx**2)/2)
C=sp.simplify(M**2/(2*X))
DxTheta=sp.expand((Sdotx-Vx*Sx-V*Sxx)/N-(Sdot-V*Sx)*Nx/N**2)
Lmix=sp.simplify(C*DxTheta**2)

gravity_velocities=[Ndot,Nidot,Adot,nudot,gdot]
for gv in gravity_velocities:
    assert sp.simplify(sp.diff(Lmix,gv))==0
    assert sp.simplify(sp.diff(Lmix,gv,gv))==0
    assert sp.simplify(sp.diff(Lmix,Sdot,gv))==0
    assert sp.simplify(sp.diff(Lmix,Sdotx,gv))==0

# C depends on Sdot but not Sdotx.  Hence the highest scalar velocity-jet
# coefficient is especially simple and cannot disappear for finite X>0.
coeff_Sdotx2=sp.simplify(sp.diff(Lmix,Sdotx,Sdotx)/2)
assert sp.simplify(coeff_Sdotx2-C/N**2)==0

# A and dot(nu) remain absent exactly; nu enters only through invariant shift.
assert not Lmix.has(Adot) and not Lmix.has(nudot)

out={
  'classification':'RTK_ROUTE_B_U1_FIXED_CX_VELOCITY_SUPPORT_PASS',
  'fixed_C':'C(X_U)=M_Pl^2/(2X_U)',
  'kinetic_invariant':'X_U=1/2[Theta_U^2-D_iSigma D^iSigma]',
  'domain':'timelike rolling branch X_U>0',
  'gravity_gauge_time_velocity_support':'none for N, shift, A, nu or spatial metric',
  'scalar_highest_velocity_jet_coefficient':'C/N^2 = M_Pl^2/(2 X_U N^2), nonzero and positive for X_U>0',
  'interpretation':'Making C a function of X_U changes the scalar momentum nonlinearly but does not add a gravity/gauge kinetic direction or a second independent scalar field velocity.',
  'status_scope':'PRIMARY_VELOCITY_SUPPORT_GREEN_FOR_FIXED_CX',
  'non_claims':[
    'does not by itself recompute the full secondary Poisson matrix after the nonlinear scalar Legendre transform',
    'does not cover the singular X_U=0 boundary',
    'does not establish radiative stability, PPN or cutoff'
  ],
  'next_gate':'recheck A-independence, invariant-shift Noether identity and second-class cross-block source support with fixed P(X_U) and C(X_U), then reissue the scoped classical DOF certificate only if those identities remain exact'
}
open('u1_fixed_cx_velocity_support_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
