#!/usr/bin/env python3
"""Exact resolution of the old universal family-I FLRW A-source obstruction.

Old architecture at a1=1,a2=0 had ordinary matter Hamiltonian
  H_m=[N-(A-Acal)] H0 + ...,
so the A coefficient contained -H0 and the homogeneous A constraint tied a
constant geometric left-hand side to evolving ordinary rho(a), producing the
scoped BLACK result for flat production cosmology.

Current elliptic auxiliary architecture adds
  H_aux=(A-Acal) Q + Lambda[(1-D^2/M_c^2)Q-H0].
At homogeneous k=0, D^2=0 and the auxiliary constraint gives Q=H0 exactly.
Therefore the total coefficient of (A-Acal) is -H0+Q=0 for arbitrary H0(a).
The A constraint reverts to its pure-gravity geometric source; on flat FLRW it
can impose the corresponding constant gauge-curvature condition (Omega=0 in
the current flat branch) without requiring ordinary rho(a) to be constant.
"""
import json
import sympy as sp

H0,Q,A,Acal,Lam,ell=sp.symbols('H0 Q A Acal Lambda ell', real=True, finite=True)
Hm=-(A-Acal)*H0
Haux=(A-Acal)*Q+Lam*(ell*Q-H0)
Atotal=sp.simplify(sp.diff(Hm+Haux,A))
assert sp.simplify(Atotal-(Q-H0))==0
# Homogeneous filter ell=1; auxiliary constraint Q=H0.
Atotal_k0=sp.simplify(Atotal.subs({ell:1,Q:H0}))
assert Atotal_k0==0
# Off homogeneous mode, Q=H0/ell gives the expected filtered source.
Atotal_filter=sp.factor(Atotal.subs(Q,H0/ell))
assert sp.simplify(Atotal_filter-H0*(1/ell-1))==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_FLRW_A_SOURCE_RESOLUTION_PASS',
  'status_scope':'GREEN_EXACT_HOMOGENEOUS_A_SOURCE_CANCELLATION_OLD_UNIVERSAL_FRAME_BLACK_SUPERSEDED_BY_NEW_ARCHITECTURE',
  'old_obstruction':'The unchanged universal family-I frame had an A-source proportional to evolving ordinary H0/rho, incompatible with a flat homogeneous constant geometric A-constraint.',
  'current_A_coefficient':'J_A ordinary+auxiliary is proportional to Q-H0.',
  'homogeneous_constraint':'k=0 -> ell=1 and Q=H0 exactly, hence Q-H0=0 for arbitrary time-dependent H0(a).',
  'finite_k_source':'Q=H0/ell gives H0(1/ell-1), i.e. the intended scale-dependent filtered A-source rather than a homogeneous obstruction.',
  'flat_branch_consequence':'The homogeneous A constraint is no longer forced to track evolving ordinary rho(a); the current flat branch may impose its pure-gravity constant condition (Omega=0 in the present convention) independently.',
  'interpretation':'The previous BLACK_SCOPED_CURRENT_UNIVERSAL_FAMILY1_MATTER_FRAME_FLRW result remains valid for the old unchanged matter architecture but is superseded for the current elliptic-compensator architecture at homogeneous k=0.',
  'non_claims':[
    'does not by itself prove finite-k rank or perturbation stability',
    'does not choose M_c; the homogeneous cancellation is exact for every positive M_c',
    'does not certify PPN or equivalence-principle behavior of the filtered finite-k matter source',
    'does not solve radiative protection or compact-object gates'
  ],
  'next_gate':'combine this exact homogeneous A-source cancellation with the lambda_HL>1 same-action Friedmann normalization and the all-q rank-safe barotropic theorem in one frozen action-domain checkpoint.'
}
open('u1_elliptic_compensator_flrw_a_source_resolution_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
