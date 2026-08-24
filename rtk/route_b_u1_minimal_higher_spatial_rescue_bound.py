#!/usr/bin/env python3
"""Deterministic replay of the minimal higher-spatial rescue compatibility bound."""
import json, math

TARGET='research/theory_targets/RTK_C8_U1_MINIMAL_HIGHER_SPATIAL_RESCUE_BOUND_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_C8_U1_MINIMAL_HIGHER_SPATIAL_RESCUE_BOUND_TARGET_V1'
r=t['reference']

C_KM_S=299792.458
h=float(r['h']); Om=float(r['Omega_K0']); lam=float(r['lambda_D']); gamma=float(r['gamma'])
H0=(100.0*h)/C_KM_S # Mpc^-1
mu=3.0*H0*math.sqrt(gamma)
A=Om/(6.0*gamma)
D=1.0+2.0*A+lam*A*A
x0=A*(2.0+lam*A)/(1.0+lam*A+math.sqrt(D))
assert H0>0 and mu>0 and x0>0

def state(a):
    x=x0/a**3
    s=math.sqrt(1.0+lam*x*x)
    rr=x/s
    Q=1.0+rr
    ca2=rr/(s*(s+x))
    MK=mu*Q*s*math.sqrt(s)
    identity_lhs=MK*MK*ca2
    identity_rhs=mu*mu*Q*x
    dln_aQ=1.0-3.0*rr/(Q*s*s)
    return dict(a=a,x=x,s=s,r=rr,Q=Q,ca2=ca2,MK=MK,
                identity_rel=abs(identity_lhs-identity_rhs)/max(abs(identity_lhs),abs(identity_rhs),1e-300),
                dln_aQ=dln_aQ)

# Dense deterministic audit of z in [0,1], together with analytic derivative formula.
rows=[]
for i in range(1001):
    z=i/1000.0
    a=1.0/(1.0+z)
    st=state(a); st['z']=z; rows.append(st)
assert max(x['identity_rel'] for x in rows)<1e-12
assert min(x['dln_aQ'] for x in rows)>0.0

kcom=float(r['production_kmax_h_per_Mpc'])*h
# R/eta = Q k_com^2 a/(mu^2 x0); monotonicity above makes z=0 the maximum.
def coeff(st): return st['Q']*kcom*kcom*st['a']/(mu*mu*x0)
coeffs=[coeff(x) for x in rows]
imax=max(range(len(rows)),key=lambda i:coeffs[i])
worst=rows[imax]; cmax=coeffs[imax]
assert abs(worst['z'])<1e-15

bounds={
 '1_percent':0.01/cmax,
 '0p5_percent':0.005/cmax,
 '0p1_percent':0.001/cmax,
 '0p01_percent':0.0001/cmax,
}

out={
 'classification':'RTK_C8_U1_MINIMAL_HIGHER_SPATIAL_RESCUE_COMPATIBILITY_BOUND_REPLAY_PASS',
 'status':'SINGLE_OPERATOR_RESCUE_REQUIRES_VERY_SMALL_ETA4_TO_PRESERVE_PRODUCTION_KERNEL',
 'target':TARGET,
 'reference':r,
 'reconstructed':{
   'H0_over_c_Mpc_inv':H0,'mu_K_Mpc_inv':mu,'x0':x0,
   'kmax_comoving_Mpc_inv':kcom,
   'z0':state(1.0)
 },
 'exact_identities':{
   'MK2_ca2':'mu_K^2 Q x',
   'R_HS_over_eta4':'Q k_com^2 a/(mu_K^2 x0)',
   'd_ln_aQ_d_ln_a':'1-3r/(Q s^2)'
 },
 'redshift_audit':{
   'z_min':0.0,'z_max':1.0,'points':1001,
   'min_d_ln_aQ_d_ln_a':min(x['dln_aQ'] for x in rows),
   'max_identity_relative_error':max(x['identity_rel'] for x in rows),
   'worst_contamination_z':worst['z']
 },
 'R_HS_over_eta4_at_worst':cmax,
 'eta4_upper_bounds_for_fractional_kernel_contamination':bounds,
 'local_rest_rescue_dispersion':'omega^2=eta4 k^4/(mu_K^2+k^2) for the isolated candidate operator with eta4>0',
 'interpretation':'For this single normalized (D^2 Sigma)^2 rescue, even percent-level preservation of the historical production RTK gradient kernel forces eta4 to be of order 1e-11 or smaller. This is a quantitative tuning signal, not a no-go: multi-operator cancellations, symmetry relations, or a different completion can change the conclusion.',
 'non_claims':t['non_claims'],
 'next_gate':t['next_gate']
}
open('u1_minimal_higher_spatial_rescue_bound_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
