#!/usr/bin/env python3
"""C8 exact velocity-support theorem for the U(1)-invariant RTK mixed operator.

For one local Cartesian spatial direction,
  Theta_U = (Sdot - (Ni-N*nux)*Sx)/N.
The spatial derivative D_x Theta_U contains Sdot and D_x Sdot but no time
velocity of lapse, shift, U(1) gauge field, Newtonian prepotential, or metric.
Thus C(D Theta_U)^2 cannot by itself give those multiplier/gauge variables new
canonical velocities. This is only a primary-Hessian support theorem; secondary
constraints and their Poisson matrix can still change after coupling.
"""
import json
import sympy as sp

# Fields / spatial jets.
N,Ni,nux,Sx,Sdot = sp.symbols('N Ni nux Sx Sdot', nonzero=True, real=True, finite=True)
Nx,Nix,nuxx,Sxx,Sdotx = sp.symbols('Nx Nix nuxx Sxx Sdotx', real=True, finite=True)
C=sp.symbols('C', nonzero=True, real=True, finite=True)

# Formal gravity/gauge time velocities, intentionally independent jet variables.
Ndot,Nidot,Adot,nudot,gdot = sp.symbols('Ndot Nidot Adot nudot gdot', real=True, finite=True)

V=Ni-N*nux
Vx=Nix-Nx*nux-N*nuxx
# Exact ordinary x derivative of Theta=(Sdot-V*Sx)/N.
DxTheta=sp.expand((Sdotx-Vx*Sx-V*Sxx)/N - (Sdot-V*Sx)*Nx/N**2)
Lmix=sp.expand(C*DxTheta**2)

# No gravity/gauge time velocity can occur in the mixed operator.
gravity_velocities=[Ndot,Nidot,Adot,nudot,gdot]
first={str(v):sp.simplify(sp.diff(Lmix,v)) for v in gravity_velocities}
second={str(v):sp.simplify(sp.diff(Lmix,v,v)) for v in gravity_velocities}
assert all(x==0 for x in first.values())
assert all(x==0 for x in second.values())

# The intended scalar velocity support is genuinely present.
scalar_Sdot=sp.simplify(sp.diff(Lmix,Sdot))
scalar_Sdotx=sp.simplify(sp.diff(Lmix,Sdotx))
assert scalar_Sdot!=0
assert scalar_Sdotx!=0

# Mixed Hessian entries between scalar velocity jets and gravity time velocities vanish.
cross={}
for sv in (Sdot,Sdotx):
    for gv in gravity_velocities:
        x=sp.simplify(sp.diff(Lmix,sv,gv))
        cross[f'{sv}:{gv}']=x
        assert x==0

out={
  'classification':'RTK_ROUTE_B_U1_MIXED_VELOCITY_SUPPORT_GATE_PASS',
  'operator':'C*(D_i Theta_U)*(D^i Theta_U)',
  'theta':'Theta_U=(dot Sigma-(N^i-N D^i nu)D_i Sigma)/N',
  'gravity_gauge_velocity_derivatives':{k:str(v) for k,v in first.items()},
  'gravity_gauge_velocity_second_derivatives':{k:str(v) for k,v in second.items()},
  'scalar_velocity_support':{
    'dL_d_Sdot_nonzero':str(scalar_Sdot),
    'dL_d_DxSdot_nonzero':str(scalar_Sdotx)
  },
  'scalar_gravity_velocity_cross_hessian':{k:str(v) for k,v in cross.items()},
  'interpretation':'The RTK U(1)-invariant mixed operator adds only the intended Sigma velocity-jet support and does not by itself kinetically activate lapse, shift, A, nu, or metric variables.',
  'non_claims':[
    'does not prove that all original U(1) primary constraints survive as first/second class after interactions',
    'does not compute secondary constraints or their Poisson matrix',
    'does not establish the final coupled physical DOF count',
    'does not address radiative detuning, PPN, GW, or the EFT cutoff'
  ],
  'next_gate':'derive preservation in time of the U(1) gravity primary constraints with the Sigma source terms and compute the coupled secondary-constraint Poisson matrix, keeping lambda_HL symbolic'
}
open('u1_mixed_velocity_support_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_MIXED_VELOCITY_SUPPORT_GATE_PASS',json.dumps(out,sort_keys=True))
