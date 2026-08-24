#!/usr/bin/env python3
"""Static DBI reality-domain gate for the frozen U(1)+RTK scalar action.

On the exact static clock solution Sigma=q t with zero invariant shift,
  sqrt(X_U/X_star)=1/N.
The DBI square root is real only if
  R_DBI = 1-lambda_D(1/N-1)^2 >= 0.

This script evaluates that necessary domain condition on a GR-like exterior
solar-photosphere lapse using IAU 2015 nominal conversion constants and the
frozen finite/B10 lambda anchors.  It also records the analytic fact that the
formal lambda_D->infinity limit is not uniform at fixed N != 1.
"""
from __future__ import annotations

import json, math

GM_SUN=1.3271244e20      # m^3 s^-2, IAU 2015 nominal conversion constant
R_SUN=6.957e8            # m, IAU 2015 nominal conversion constant
C=299792458.0            # m/s, exact SI
LAMBDAS={
  'finite_certified':219457.5727136581,
  'B10_factor64':14045284.653674118,
  'B10_factor16384':3595592871.3405743,
}

compactness=GM_SUN/(R_SUN*C*C)
assert 0 < compactness < 1e-4
N=math.sqrt(1.0-2.0*compactness)
delta=1.0/N-1.0
lambda_max=1.0/(delta*delta)

rows={}
for name,lam in LAMBDAS.items():
    radicand=1.0-lam*delta*delta
    rows[name]={
      'lambda_D':lam,
      'lambda_delta2':lam*delta*delta,
      'R_DBI':radicand,
      'real_static_clock_domain':bool(radicand>=0.0),
      'lambda_max_over_lambda':lambda_max/lam,
    }

assert rows['finite_certified']['real_static_clock_domain']
assert rows['B10_factor64']['real_static_clock_domain']
assert rows['B10_factor16384']['real_static_clock_domain']
assert lambda_max > LAMBDAS['B10_factor16384']

# Analytic lambda->infinity statement at any fixed nonzero delta:
# R_DBI=1-lambda*delta^2 -> -infinity.
assert delta != 0.0

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_DBI_REALITY_DOMAIN_SCOPED_PASS_WITH_NONUNIFORM_TAIL_BOUND',
 'status':'FINITE_AND_PREREGISTERED_B10_ANCHORS_REAL_ON_SOLAR_REFERENCE;_FORMAL_INFINITE_TAIL_NOT_UNIFORM',
 'solar_reference':{
   'GM_sun_nominal_m3_s2':GM_SUN,
   'R_sun_nominal_m':R_SUN,
   'c_m_s':C,
   'compactness_GM_over_Rc2':compactness,
   'N_schwarzschild_exterior_at_Rsun':N,
   'delta_abs_1_over_N_minus_1':abs(delta),
   'source':'IAU 2015 Resolution B3 nominal conversion constants; c exact SI'
 },
 'domain':{
   'R_DBI':'1-lambda_D(1/N-1)^2',
   'lambda_D_max_on_reference':lambda_max,
   'fixed_nonzero_lapse_lambda_to_infinity':'R_DBI -> -infinity; the static-clock real branch cannot be continued uniformly to lambda_D=infinity'
 },
 'anchors':rows,
 'interpretation':[
   'The certified finite lambda_D and both preregistered B10 tail anchors remain inside the real DBI domain at the nominal solar photospheric weak-field reference.',
   'The largest B10 factor-16384 anchor retains a finite domain margin, but only about lambda_max/lambda ~= %.6g further multiplicative room on this reference.' % (lambda_max/LAMBDAS['B10_factor16384']),
   'Therefore B10 cosmological numerical non-identifiability does not justify treating lambda_D=infinity as a uniformly admissible local static-clock limit.'
 ],
 'non_claims':[
   'does not invalidate B10 cosmological protocol-v1 closure',
   'does not rule out alternative local solutions with spatial Sigma gradients or nonzero invariant shift for larger lambda_D',
   'does not assert the exact modified-gravity solar solution is Schwarzschild',
   'does not extrapolate this weak-field photospheric gate to neutron stars or black holes',
   'does not establish compact-object regularity near X_U=0'
 ],
 'next_gate':'use the exact static variation bridge plus finite-lambda DBI source to derive the Solar-System finite-mu_K correction bound; separately investigate whether alternative scalar profiles can extend the local domain beyond lambda_D_max'
}
open('u1_static_dbi_reality_domain_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
