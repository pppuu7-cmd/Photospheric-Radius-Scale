#!/usr/bin/env python3
"""Heavy source-specific O(4) resolvent mode-mixing shape audit.

This is a deliberately scoped numerical component of the full finite-Mc O(4)
problem, not a PPN pass.  It evaluates the exact metric-variation convolution
for a uniform spherical source using the already certified d=3 kernel.

Set R=1 and define m=M_c R, K=k R, Q=q R,
 P=|k-q| R=sqrt(K^2+Q^2-2 K Q mu),
 S(x)=3[sin x-x cos x]/x^3 (normalized uniform-sphere Fourier form factor).
The dimensionless shape integral (overall G, rho and gamma stripped) is
 C(K,m)=2pi int Q^2 dQ int_{-1}^1 dmu
   {-m^2[3Q^2-KQ mu]/[(m^2+K^2)(m^2+Q^2)]}
   * S(P)/(P^2+m^2) * S(Q).

The scan maps this isolated nonlinear resolvent contribution over many decades
in m and K and performs a resolution-convergence audit at representative points.
It must not be interpreted as beta/alpha2 or a complete O(4) observable.
"""
import json, math, time
import numpy as np
from numpy.polynomial.legendre import leggauss


def sphere_ff(x):
    x=np.asarray(x,dtype=float)
    out=np.empty_like(x)
    ax=np.abs(x)
    small=ax<1e-4
    xs=x[small]
    out[small]=1.0-xs*xs/10.0+xs**4/280.0-xs**6/15120.0
    y=x[~small]
    out[~small]=3.0*(np.sin(y)-y*np.cos(y))/(y**3)
    return out


def integral(K,m,nq=1400,nmu=48,qmin=1e-5,qmax=2e4):
    mu,w=leggauss(nmu)
    # log Q with trapezoid in t=ln Q, Q^2 dQ = Q^3 dt
    t=np.linspace(math.log(qmin),math.log(qmax),nq)
    Q=np.exp(t)
    SQ=sphere_ff(Q)
    vals=np.empty(nq)
    denomK=m*m+K*K
    for i,q in enumerate(Q):
        P2=K*K+q*q-2.0*K*q*mu
        P2=np.maximum(P2,0.0)
        P=np.sqrt(P2)
        kernel=-(m*m)*(3.0*q*q-K*q*mu)/(denomK*(m*m+q*q))
        Ushape=sphere_ff(P)/(P2+m*m)
        ang=np.dot(w,kernel*Ushape)
        vals[i]=(q**3)*SQ[i]*ang
    return float(2.0*math.pi*np.trapezoid(vals,t))

start=time.time()
ms=np.logspace(-3,3,15)
Ks=np.logspace(-3,3,21)
rows=[]
max_abs=(-1.0,None)
for m in ms:
    for K in Ks:
        v=integral(float(K),float(m))
        row={'m_McR':float(m),'K_kR':float(K),'C_shape':v,'abs_C_shape':abs(v)}
        rows.append(row)
        if abs(v)>max_abs[0]: max_abs=(abs(v),row.copy())

# Representative resolution audit, including m~K~1 and separated regimes.
audit=[]
for K,m in [(0.03,0.03),(1.0,0.1),(1.0,1.0),(1.0,10.0),(30.0,3.0)]:
    coarse=integral(K,m,nq=900,nmu=32,qmax=1e4)
    base=integral(K,m,nq=1400,nmu=48,qmax=2e4)
    fine=integral(K,m,nq=2200,nmu=72,qmax=4e4)
    scale=max(1.0,abs(fine))
    audit.append({'K_kR':K,'m_McR':m,'coarse':coarse,'base':base,'fine':fine,
                  'base_minus_fine_abs':abs(base-fine),
                  'base_minus_fine_rel_scaled':abs(base-fine)/scale,
                  'coarse_minus_fine_rel_scaled':abs(coarse-fine)/scale})

# Structural checks: this isolated metric-variation component must disappear
# toward the local-parent m->0 limit at fixed K. Use direct sample hierarchy,
# not an overstrong monotonic claim for all m.
local_samples=[]
for K in [0.1,1.0,10.0]:
    vals=[integral(K,m,nq=1000,nmu=40) for m in [1e-4,3e-4,1e-3]]
    local_samples.append({'K':K,'m':[1e-4,3e-4,1e-3],'C':vals})
    assert abs(vals[0]) < max(1e-8, 0.2*max(abs(vals[2]),1e-30))

max_audit=max(a['base_minus_fine_rel_scaled'] for a in audit)
out={
 'classification':'RTK_C9_PROJECTABLE_U1_O4_UNIFORM_SPHERE_RESOLVENT_CONVOLUTION_SCAN_COMPLETE',
 'status_scope':'GREEN_NUMERICAL_SHAPE_AUDIT_ISOLATED_RESOLVENT_COMPONENT_FULL_O4_SOURCE_TRANSFER_PENDING',
 'definition':'C(K,m)=uniform-sphere dimensionless convolution of the exact d=3 delta-a_eff metric-variation kernel with one O2 Yukawa potential factor and one density form factor; overall G,rho,gamma stripped',
 'grid':{'m_McR':[float(v) for v in ms],'K_kR':[float(v) for v in Ks],'nq':1400,'nmu':48,'qmin':1e-5,'qmax':2e4},
 'maximum_abs_on_grid':max_abs[1],
 'resolution_audit':audit,
 'max_base_fine_rel_scaled':max_audit,
 'local_limit_samples':local_samples,
 'elapsed_seconds':time.time()-start,
 'rows':rows,
 'interpretation':'This isolates how the finite-Mc O4 resolvent metric variation redistributes a smooth extended source in momentum space. It is a source-shape diagnostic for the generalized nonlocal PPN calculation, not a standalone observable or experimental constraint.',
 'non_claims':['not beta, alpha2, zeta_i or xi','not the complete Eq.(6.17) source transfer','overall gravitational/source normalization stripped','no nonlinear screening or compact-object self-gravity','uniform density only'],
 'next_gate':'add filtered J_A O4 source terms and ordinary stress/H0 metric variation with the same Fourier conventions, then solve the generalized h00 kernel and compare source-specific acceleration observables.'
}
open('c9_projectable_u1_o4_uniform_sphere_resolvent_convolution_scan_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps({k:out[k] for k in ['status_scope','maximum_abs_on_grid','max_base_fine_rel_scaled','elapsed_seconds']},sort_keys=True))
