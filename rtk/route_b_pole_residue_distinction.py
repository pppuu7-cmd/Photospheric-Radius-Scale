#!/usr/bin/env python3
"""Route-B guard: exact dispersion/pole matching does not imply off-shell kernel matching.

Compare a reduced BPS-type scalar kernel whose rational factor appears in the
spatial term with the constructive RTK mixed-kinetic kernel. They differ by a
positive momentum-dependent factor, so they have exactly the same pole but
not the same propagator normalization/residue for a fixed source coupling.

This prevents overinterpreting the constructive BPS dispersion embedding as an
already completed off-shell RTK action/observable mapping.
"""
import json
import sympy as sp

A,G,r,q,y=sp.symbols('A G r q y', positive=True, finite=True, real=True)
fac=1+r*q**2
K_bps=sp.simplify(A*y-G*q**2/fac)
K_rtk=sp.expand(A*fac*y-G*q**2)
assert sp.simplify(K_rtk-fac*K_bps)==0

# Same physical pole in y=omega^2.
pole_bps=sp.solve(sp.Eq(K_bps,0),y)[0]
pole_rtk=sp.solve(sp.Eq(K_rtk,0),y)[0]
assert sp.simplify(pole_bps-pole_rtk)==0
assert sp.simplify(pole_rtk-G*q**2/(A*fac))==0

# But the two fixed-source propagators differ by the momentum factor.
D_bps=sp.simplify(1/K_bps)
D_rtk=sp.simplify(1/K_rtk)
assert sp.simplify(D_bps-fac*D_rtk)==0

# Residue with respect to y is inverse dK/dy at the simple pole.
res_bps=sp.simplify(1/sp.diff(K_bps,y))
res_rtk=sp.simplify(1/sp.diff(K_rtk,y))
assert sp.simplify(res_bps-fac*res_rtk)==0
assert sp.simplify(res_bps/res_rtk-fac)==0

out={
  'classification':'RTK_ROUTE_B_POLE_RESIDUE_DISTINCTION_PASS',
  'bps_kernel':'K_BPS=A omega^2-G q^2/(1+r q^2)',
  'rtk_kernel':'K_RTK=A(1+r q^2) omega^2-G q^2',
  'exact_relation':'K_RTK=(1+r q^2) K_BPS',
  'shared_pole':'omega^2=(G/A) q^2/(1+r q^2)',
  'propagator_relation':'D_BPS=(1+r q^2) D_RTK for the same fixed source normalization',
  'residue_relation':'Res_BPS=(1+r q^2) Res_RTK in omega^2',
  'theorem':'Exact matching of the rational scalar dispersion is weaker than matching the off-shell quadratic kernel and source-coupled two-point response. The BPS constructive family is therefore an exact pole/dispersion embedding, not yet an exact RTK propagator/observable mapping.',
  'what_is_needed_for_full_mapping':[
    'explicit field normalization/transformation between the BPS scalar and intended RTK Khronon variable',
    'consistent mapping of matter/source couplings and constraint variables',
    'comparison of gauge-invariant transfer functions/residues, not only pole locations',
    'generic-background constraint and stability analysis'
  ],
  'non_claims':[
    'does not invalidate the BPS healthy quadratic dispersion embedding',
    'does not prove no field/source mapping exists',
    'does not establish full nonlinear equivalence or inequivalence'
  ]
}
print('RTK_ROUTE_B_POLE_RESIDUE_DISTINCTION_PASS',json.dumps(out,sort_keys=True))
