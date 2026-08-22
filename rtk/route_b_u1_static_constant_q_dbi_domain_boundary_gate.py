#!/usr/bin/env python3
"""Exact DBI-domain boundary for the fixed constant-q static clock branch.

For the certified static ansatz Sigma=q t, zero invariant shift and D_iSigma=0,
X=q^2/(2N^2).  Normalize the asymptotic/frozen production state at N=1 with
u0=sqrt(X0/X_star)=1+r0.  Then locally

    u(N)=u0/N.

The reconstructed DBI P(X) is real only when

    1-lambda_D [u(N)-1]^2 >= 0.

This gives an exact lapse interval.  Crossing either endpoint invalidates the
constant-q real DBI branch.  It does not exclude a different inhomogeneous
Sigma profile that keeps X inside the domain, and therefore is a scoped branch
boundary rather than a no-go for the fixed U1 action.
"""
import json, math

lam=219457.5727136581
r0=0.0021346329644460586
u0=1.0+r0
sqrti=1.0/math.sqrt(lam)
assert 0<sqrti<1
N_lower=u0/(1.0+sqrti)
N_upper=u0/(1.0-sqrti)
assert N_lower<1.0<N_upper
lower_margin=1.0-N_lower
upper_margin=N_upper-1.0

# Exact boundary checks.
for N,sgn in ((N_lower,+1.0),(N_upper,-1.0)):
    u= u0/N
    residual=1.0-lam*(u-1.0)**2
    assert abs(residual)<5e-13
    assert abs((u-1.0)-sgn*sqrti)<5e-13

# Illustrative conditional points: no compact-object metric assumption is made.
def real_margin(N):
    return 1.0-lam*(u0/N-1.0)**2
assert real_margin(1.0)>0
assert real_margin(N_lower*(1-1e-9))<0
assert real_margin(N_upper*(1+1e-9))<0

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_CONSTANT_Q_DBI_DOMAIN_BOUNDARY_PASS',
 'scientific_status':'BLACK_SCOPED_CONSTANT_Q_STATIC_BRANCH_OUTSIDE_EXACT_LAPSE_INTERVAL',
 'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
 'static_clock_run_id':32568097865,
 'scale_dictionary_run_id':32568333920,
 'z0':{'lambda_D':lam,'r0':r0,'u0':u0,'inv_sqrt_lambda_D':sqrti},
 'exact_condition':'1-lambda_D*(u0/N-1)^2 >= 0 for the real constant-q static branch',
 'exact_interval':{'N_lower':N_lower,'N_upper':N_upper,'negative_lapse_margin_from_1':lower_margin,'positive_lapse_margin_from_1':upper_margin},
 'result':'The exact Sigma=q t constant-q static branch is real only inside the displayed ADM-lapse interval. Any solution point crossing an endpoint requires leaving this branch (for example through an inhomogeneous/time-adjusted Sigma profile) or leaving the fixed real DBI action domain.',
 'solar_system_relation':'The existing family-I O(2) gate gives ADM n2=0, so physical Newtonian N_tilde=1-U does not imply ADM N=1-U. Solar-system safety therefore depends on the O(4) ADM-lapse solution and is not ruled out by this narrow interval.',
 'compact_object_implication':'A compact-object solution cannot assume Sigma=q t unchanged if its ADM lapse leaves this narrow interval; a new nonlinear scalar-profile/constraint solve is mandatory.',
 'non_claims':[
   'does not prove that every compact-object solution has ADM N outside the interval',
   'does not exclude nontrivial Sigma(t,x) solutions that keep X_U inside the DBI domain',
   'does not exclude UV completion changing the P(X) domain',
   'does not modify the already certified cosmological rolling branch'
 ],
 'next_gate':'solve the fixed-action static/spherical scalar equation allowing a nontrivial Sigma profile together with U1 constraints, and determine whether regular stellar/compact-object solutions can keep X_U within the real DBI domain'
}
open('u1_static_constant_q_dbi_domain_boundary_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
