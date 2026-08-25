#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

H,w,ca,delta,theta,k2,B,psip=sp.symbols('H w ca2 delta theta k2 B psi_prime', finite=True, real=True)
wp=-3*H*(1+w)*(ca-w)
deltap=-(1+w)*(theta+k2*B-3*psip)-3*H*(ca-w)*delta
Iprime=sp.factor(deltap/(1+w)-delta*wp/(1+w)**2-3*psip)
assert sp.simplify(Iprime+theta+k2*B)==0

# Action-charge dictionary.  Keep all factors symbolic and nonzero where a ratio is taken.
a,F,A,U,PX,Sig,psi=sp.symbols('a F A U P_X Sigma_prime psi', nonzero=True, finite=True, real=True)
dmu=F*A*Sig*U/a**2
W=PX*Sig**2/a**2
Qbar=a**2*PX*Sig
dQ=a**2*F*A*U-3*a**2*PX*Sig*psi
charge_ratio=sp.factor(dQ/Qbar)
fluid_I=sp.factor(dmu/W-3*psi)
assert sp.simplify(charge_ratio-fluid_I)==0

out={
  'schema':'RTK_C10_NEUTRAL_SHIFT_CHARGE_MEMORY_RESULT_v1',
  'classification':'C10_NEUTRAL_SHIFT_CHARGE_MEMORY_INVARIANT_PASS_SCOPED',
  'exact_identities':{
    'I_khr':'delta/(1+w)-3 psi_pref',
    'I_khr_prime':'-(theta+k^2 B)',
    'background_w_prime':'-3 H (1+w)(c_a^2-w)',
    'deltaQ_over_Qbar':'delta_mu/(rho+p)-3 psi_pref=I_khr'
  },
  'machine_residuals':{'continuity_to_invariant':'0','action_charge_to_fluid_invariant':'0'},
  'limits':{
    'exact_k0_regular_homogeneous_mode':'I_khr is conserved when theta=0 and k^2 B=0; this is a charge/background statement, not a propagating-rank certificate',
    'regular_long_wavelength_branch':'if theta=O(k^2) and B=O(1), then I_khr_prime=O(k^2)',
    'early_dust':'w=O(a^3), so I_khr=delta_khr-3 psi_pref+controlled finite-onset corrections'
  },
  'interpretation':'The neutral shift symmetry carries an independent fractional charge perturbation. Instantaneous adiabaticity alone cannot erase this datum. A pre-EFT prescription may set it, while finite-k gradients can leak it; the C10.62b transfer test measures that leakage on the pinned production background.',
  'next_gate':'compare the retained/decaying singular direction from C10.62b with I_khr, then decide whether the UV/pre-EFT completion fixes the neutral charge before the full photon+baryon+UR growing-mode test',
  'non_claims':['not full coupled isocurvature classification','not exact finite-k conservation','not a k=0 rank theorem','not a UV boundary prescription','not spectra or likelihood evidence']
}
Path('c10_neutral_shift_charge_memory_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
