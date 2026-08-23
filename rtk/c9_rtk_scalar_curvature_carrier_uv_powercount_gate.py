#!/usr/bin/env python3
"""High-k power counting for intrinsic-curvature RTK UV carriers.

Consider the unitary-gauge spatial carrier family whose quadratic scalar piece
adds k^(2n+2) zeta^2 to the potential while the already certified mixed kinetic
term gives Z(k)~k^2/M_K^2.  The completed dispersion then scales as
omega^2~k^(2n).

Intrinsic-curvature invariants of the schematic family
  [D^(n-1) R3]^2
carry 2n+2 spatial derivatives at every nonlinear order before constraint
reduction.  With one external canonical normalization Z^(-1/2)~M_K/k per leg,
a bare m-point spatial vertex scales as k^(2n+2-m). Thus
  V3~k^(2n-1), V4~k^(2n-2).
A generic nonresonant cubic exchange uses a propagator ~k^(-2n), so
  M_exchange~V3^2/k^(2n)~k^(2n-2),
matching the quartic contact scaling.

The exact isotropic two-body phase-space scaling of the completed dispersion is
  g~k^(3-3n).
Therefore the phase-space weighted partial wave scales as
  g a_l ~ k^(1-n).

This is a scoped asymptotic power-counting theorem. It assumes no inverse-power
enhancement from nonlinear lapse/shift reduction and time-only unitary-gauge
carrier coefficients. Full reduced vertices must still be computed.
"""
import json

rows=[]
for n in [1,2,3,4]:
    derivative_order=2*n+2
    v3=derivative_order-3
    v4=derivative_order-4
    propagator=-2*n
    exchange=2*v3+propagator
    amplitude=v4
    phase=3-3*n
    weighted=amplitude+phase
    assert exchange==amplitude==2*n-2
    assert weighted==1-n
    rows.append({
      'n':n,
      'carrier_spatial_derivatives':derivative_order,
      'omega_squared_power_k':2*n,
      'V3_power_k':v3,
      'V4_power_k':v4,
      'exchange_amplitude_power_k':exchange,
      'contact_amplitude_power_k':amplitude,
      'phase_space_power_k':phase,
      'weighted_partial_wave_power_k':weighted,
    })

assert rows[0]['weighted_partial_wave_power_k']==0
assert rows[1]['weighted_partial_wave_power_k']==-1
assert rows[2]['weighted_partial_wave_power_k']==-2

out={
 'classification':'RTK_C9_RTK_SCALAR_CURVATURE_CARRIER_UV_POWERCOUNT_PASS',
 'status_scope':'GREEN_BARE_SPATIAL_CARRIER_UV_POWERCOUNT_FULL_REDUCED_AMPLITUDE_PENDING',
 'assumptions':[
   'Z(k)~k^2/M_K^2 from the certified RTK mixed kinetic term',
   'quadratic UV carrier produces omega^2~k^(2n)',
   'schematic intrinsic carrier [D^(n-1)R3]^2 has 2n+2 total spatial derivatives at every bare nonlinear order',
   'one external field normalization contributes k^-1 per leg',
   'generic nonresonant internal propagator scales as k^(-2n)',
   'nonlinear constraint elimination produces no additional positive-power UV enhancement beyond the bare carrier counting',
   'carrier coefficient is a prescribed time/background function in unitary gauge, so no additional fluctuating-X time-derivative vertex is included in this theorem'
 ],
 'generic':{
   'V3':'~k^(2n-1)',
   'V4':'~k^(2n-2)',
   'tree_exchange':'~k^(2n-2)',
   'tree_contact':'~k^(2n-2)',
   'phase_space':'g~k^(3-3n)',
   'phase_space_weighted_partial_wave':'g a_l~k^(1-n)'
 },
 'cases':rows,
 'interpretation':'n=1 can at best make the high-k weighted partial waves approach finite constants and therefore still requires an explicit coefficient-level amplitude check. n>=2 is asymptotically softer in the phase-space weighted tree partial waves under the stated assumptions; n=2 gives k^-1 and n=3 gives k^-2.',
 'non_claims':[
   'does not compute the exact curvature-carrier cubic/quartic coefficients',
   'does not include nonlinear lapse/shift constraint corrections',
   'does not include mixed C(X), metric/U1/auxiliary exchange, loops or inelastic channels',
   'does not establish power-counting renormalizability or choose n',
   'does not prove a covariant state-dependent coefficient avoids extra interactions'
 ],
 'next_gate':'perform the explicit cubic/quartic ADM expansion and nonlinear constraint reduction for n=1 and n=2 first; verify the assumed UV derivative counting survives, then compute exact elastic partial waves including interference with the original P(X) sector.'
}
open('c9_rtk_scalar_curvature_carrier_uv_powercount_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
