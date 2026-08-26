#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path

DIAG=[
'c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime',
'c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total',
'c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
C_LIGHT_KMS=299792.458
EVAL_A=[0.01,0.1,0.5]


def rows(path):
    out=[]
    for raw in Path(path).read_text().splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        v=[float(x) for x in s.split()]
        tail=v[-len(DIAG):]
        d={name:tail[i] for i,name in enumerate(DIAG)}
        d['tau']=v[0]; d['a']=v[1]
        out.append(d)
    if len(out)<3: raise RuntimeError(f'too few rows: {path}')
    return out


def interp_at_a(rr,at):
    if not (rr[0]['a']<=at<=rr[-1]['a']):
        raise RuntimeError(f'a={at} outside [{rr[0]["a"]},{rr[-1]["a"]}]')
    lo=0; hi=len(rr)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if rr[m]['a']<=at: lo=m
        else: hi=m
    x0=rr[lo]; x1=rr[hi]
    f=(at-x0['a'])/(x1['a']-x0['a']) if x1['a']!=x0['a'] else 0.0
    z={}
    for key in x0:
        z[key]=x0[key]+f*(x1[key]-x0[key])
    z['a']=at
    return z


def segment_nodes(rr,a0,a1):
    z=[interp_at_a(rr,a0)]
    z.extend(x for x in rr if a0<x['a']<a1)
    z.append(interp_at_a(rr,a1))
    return z


def khr_closure(prod,gamma):
    H0=100.0*float(prod['h'])/C_LIGHT_KMS
    lamD=float(prod['lam']); Om=float(prod['Om'])
    mu=3.0*H0*math.sqrt(gamma)
    A=Om/(6.0*gamma)
    if abs(lamD-1.0)<1e-14:
        x0=A*(A+2.0)/(2.0*(A+1.0))
    else:
        root=math.sqrt(1.0+2.0*A+lamD*A*A)
        x0=A*(2.0+lamD*A)/(1.0+lamD*A+root)
    return {'H0':H0,'lambda_D':lamD,'Omega_K0':Om,'mu_K':mu,'x0':x0}


def khr_state(a,k,c):
    x=c['x0']/(a*a*a); sl=math.sqrt(c['lambda_D']); s=math.hypot(1.0,sl*x)
    r=x/s; t=x/(s+1.0); Q=1.0+r
    ca=r/(s*(s+x))
    MK=c['mu_K']*Q*s*math.sqrt(s); ks=a*MK
    cs=ca if k==0.0 else ca/(1.0+(k/ks)**2)
    return ca,cs,ks


def bg_from_row(x,k,closure):
    H=x['c10_Hc']; H0p=x['c10_H0_ord_prime']; Wtot=x['c10_W_total']; w=x['c10_khr_w']; ca_exp=x['c10_khr_ca2']
    if H==0.0: raise RuntimeError('Hc zero')
    Wo=-H0p/(3.0*H)
    Wk=Wtot-Wo
    if not (Wo>0.0 and Wk>0.0 and 1.0+w>0.0):
        raise RuntimeError(f'nonpositive inertia Wo={Wo} Wk={Wk} w={w}')
    rhok=Wk/(1.0+w)
    ca,cs,kstar=khr_state(x['a'],k,closure)
    ca_err=abs(ca-ca_exp)/max(abs(ca),abs(ca_exp),1e-300)
    return {'a':x['a'],'H':H,'Wo':Wo,'Wk':Wk,'rhok':rhok,'w':w,'ca':ca,'cs':cs,'kstar':kstar,'ca_err':ca_err}


def raw_ca_error(rr,k,closure):
    err=0.0
    for x in rr:
        ca,_,_=khr_state(x['a'],k,closure)
        ca_exp=x['c10_khr_ca2']
        err=max(err,abs(ca-ca_exp)/max(abs(ca),abs(ca_exp),1e-300))
    return err


def bg_lerp(b0,b1,f):
    return {k:b0[k]+f*(b1[k]-b0[k]) for k in b0}


def svmax(T):
    a,b,c,d=T
    tr=a*a+b*b+c*c+d*d; det=(a*d-b*c)**2
    disc=max(0.0,tr*tr-4.0*det)
    return math.sqrt(max(0.0,0.5*(tr+math.sqrt(disc))))


def integrate_transfer(rr,k,lam,closure,a_on,tracker):
    r=lam-1.0; D=3.0*lam-1.0; L=-k*k; Eth=2.0
    # columns correspond to dimensionless onset Y=(delta,theta/k) basis.
    Y=[1.0,0.0,0.0,k]  # d1,t1,d2,t2
    current=a_on
    sigmas=[]

    def one_rhs(y,bg):
        delta,theta=y
        a=bg['a']; H=bg['H']; Wo=bg['Wo']; Wk=bg['Wk']; rhok=bg['rhok']; w=bg['w']; ca=bg['ca']; cs=bg['cs']
        qk=a*Wk*theta/(k*k); Qbase=3.0*a*qk; dm=rhok*delta; X=3.0*a*a*Wo
        lapse=r*Eth*L-2.0*D*H*H
        a11=D*H; a12=r*L+X; a21=lapse; a22=-D*H*X
        b1=Qbase; b2=-3.0*a*a*r*dm-D*H*Qbase
        det=a11*a22-a12*a21
        if not math.isfinite(det) or det==0.0: raise RuntimeError('algebraic determinant zero/nonfinite')
        phi=(b1*a22-a12*b2)/det; B=(a11*b2-b1*a21)/det
        qpref=-a*Wo*B+qk; Qpref=3.0*a*qpref
        Mres=r*L*B-(Qpref-D*H*phi)
        Hres=lapse*phi-(-3.0*a*a*r*dm-D*H*Qpref)
        tracker['min_det']=min(tracker['min_det'],abs(det)); tracker['max_res']=max(tracker['max_res'],abs(Mres),abs(Hres))
        tracker['max_abs_alg']=max(tracker['max_abs_alg'],abs(phi),abs(B))
        dp=-(1.0+w)*(theta+k*k*B)-3.0*H*(ca-w)*delta
        tp=-H*(1.0-3.0*ca)*theta+k*k*(cs*delta/(1.0+w)+phi)
        if not all(math.isfinite(z) for z in (dp,tp,phi,B)): raise RuntimeError('nonfinite rhs/algebra')
        return (dp,tp)

    def rhs4(y,bg):
        a1=one_rhs((y[0],y[1]),bg); a2=one_rhs((y[2],y[3]),bg)
        return (a1[0],a1[1],a2[0],a2[1])

    for ae in EVAL_A:
        ns=segment_nodes(rr,current,ae)
        for i in range(len(ns)-1):
            x0,x1=ns[i],ns[i+1]; dt=x1['tau']-x0['tau']
            if not dt>0.0: raise RuntimeError('nonpositive dt')
            b0=bg_from_row(x0,k,closure); b1=bg_from_row(x1,k,closure); bm=bg_lerp(b0,b1,0.5)
            # Boundary nodes are linearly interpolated exported rows while ca2 is
            # reconstructed nonlinearly from a.  Keep this interpolation mismatch
            # as a diagnostic, but do not confuse it with the frozen raw-sample
            # reconstruction cross-check below.
            tracker['max_interpolated_ca_rel_error']=max(tracker['max_interpolated_ca_rel_error'],b0['ca_err'],b1['ca_err'])
            k1=rhs4(Y,b0)
            ym=[Y[j]+0.5*dt*k1[j] for j in range(4)]; k2=rhs4(ym,bm)
            ym=[Y[j]+0.5*dt*k2[j] for j in range(4)]; k3=rhs4(ym,bm)
            ye=[Y[j]+dt*k3[j] for j in range(4)]; k4=rhs4(ye,b1)
            Y=[Y[j]+dt*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6.0 for j in range(4)]
            if not all(math.isfinite(z) for z in Y): raise RuntimeError('nonfinite transfer state')
        T=(Y[0],Y[2],Y[1]/k,Y[3]/k)
        sigmas.append(svmax(T)); current=ae
    return sigmas,Y


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',required=True,dest='pattern'); ap.add_argument('--output',required=True); args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_NEUTRAL_FINITE_ONSET_MEMORY_TARGET_v1.json').read_text())
    protocol=json.loads((root/'research/theory_results/RTK_C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_RESULT_v1.json').read_text())
    source_parent=json.loads((root/'research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json').read_text())
    state=json.loads((root/'research/state/current.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'; assert protocol['classification']=='C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_PASS_SCOPED'
    tol=float(target['transfer_test']['floating_relative_tolerance']); a_on=float(protocol['production_history_reference']['a_on_common_support'])
    prod=state['final_replay_result']['rtk']['params']; gamma=float(source_parent['provenance']['gamma_root']); closure=khr_closure(prod,gamma)
    fs=sorted(glob.glob(args.pattern));
    if len(fs)!=9: raise RuntimeError(f'expected 9 histories, got {len(fs)}')
    histories=[]; Hphys_on=[]
    for f in fs:
        rr=rows(f); k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr); histories.append((k,f,rr))
        z=interp_at_a(rr,a_on); Hphys_on.append(z['c10_Hc']/a_on)
    histories.sort()
    expected=[float(x) for x in source_parent['actual_k_values_Mpc_inv']]
    if any(abs(a-b)>1e-10*max(1.0,abs(b)) for (a,_,_),b in zip(histories,expected)): raise RuntimeError('k history mismatch')
    H_EFT=max(Hphys_on)

    # Frozen acceptance asks for reconstruction against the exported production
    # ca2 column.  Evaluate that identity on actual CLASS samples.  Interpolated
    # boundary nodes are a separate numerical approximation and are diagnosed
    # independently during integration.
    max_raw_ca_rel_error=max(raw_ca_error(rr,k,closure) for k,_,rr in histories)

    records=[]; tracker={'min_det':float('inf'),'max_res':0.0,'max_abs_alg':0.0,'max_interpolated_ca_rel_error':0.0}
    by_key={}
    eta_guards=[]
    for point in protocol['points']:
        lam=float(point['lambda_HL']); mc=float(point['M_c_Mpc_inv'])
        eta_min=3.0*(3.0*lam-1.0)*H_EFT*H_EFT/(64.0*mc*mc)
        eta_guards.append(eta_min)
        for k,f,rr in histories:
            sig,Y=integrate_transfer(rr,k,lam,closure,a_on,tracker)
            rec={'k_Mpc_inv':k,'lambda_HL':lam,'M_c_Mpc_inv':mc,'u_fraction':point['u_fraction'],'delta_H_fraction':point['delta_H_fraction'],
                 'sigma_max_at_a':{str(a):s for a,s in zip(EVAL_A,sig)},'final_transfer_columns_physical':Y,'eta0_min_history_guard':eta_min}
            records.append(rec)
            key=(round(k,14),round(lam,14)); by_key.setdefault(key,[]).append(tuple(sig))

    max_mc_invariance=0.0
    for vals in by_key.values():
        ref=vals[0]
        for v in vals[1:]: max_mc_invariance=max(max_mc_invariance,max(abs(a-b) for a,b in zip(ref,v)))

    # Collapse duplicate M_c rows for scientific classification.
    unique=[]
    seen=set()
    for rec in records:
        key=(round(rec['k_Mpc_inv'],14),round(rec['lambda_HL'],14))
        if key in seen: continue
        seen.add(key); unique.append(rec)
    finals=[]; all_monotone=True
    for rec in unique:
        ss=[1.0]+[rec['sigma_max_at_a'][str(a)] for a in EVAL_A]
        finals.append(ss[-1])
        for a,b in zip(ss,ss[1:]):
            if b>a*(1.0+tol): all_monotone=False
    max_final=max(finals)
    if max_final>=1.0*(1.0-tol):
        cls='C10_NEUTRAL_FINITE_ONSET_MEMORY_RETAINED_OR_AMPLIFIED_SCOPED'
    elif all_monotone:
        cls='C10_NEUTRAL_FINITE_ONSET_MEMORY_CONTRACTION_PASS_SCOPED'
    else:
        cls='C10_NEUTRAL_FINITE_ONSET_MEMORY_NONMONOTONE_PARTIAL_CONTRACTION_SCOPED'

    assert max_raw_ca_rel_error<1e-9, max_raw_ca_rel_error
    assert tracker['max_res']<1e-8, tracker['max_res']
    assert tracker['min_det']>0.0
    assert max_mc_invariance<1e-12
    out={
      'schema':'RTK_C10_NEUTRAL_FINITE_ONSET_MEMORY_RESULT_v1','classification':cls,
      'scope':'neutral-Khronon onset-difference transfer at fixed ordinary curvature-dressed production trajectory; not full coupled adiabatic-mode uniqueness',
      'production_reference':{'gamma_root':gamma,'params':prod,'a_on':a_on,'H_EFT_max_Mpc_inv':H_EFT,'k_values_Mpc_inv':[x[0] for x in histories]},
      'khronon_reconstruction':closure,
      'diagnostics':{'max_reconstructed_ca2_relative_error_raw_CLASS_samples':max_raw_ca_rel_error,
                     'max_interpolated_boundary_ca2_relative_mismatch':tracker['max_interpolated_ca_rel_error'],
                     'max_abs_H_M_constraint_residual':tracker['max_res'],
                     'min_abs_coupled_phi_B_determinant':tracker['min_det'],'max_abs_algebraic_phi_or_B':tracker['max_abs_alg'],
                     'max_M_c_transfer_invariance_abs_difference':max_mc_invariance,'all_finite':True,
                     'eta0_min_guard_range':[min(eta_guards),max(eta_guards)]},
      'classification_diagnostics':{'floating_relative_tolerance':tol,'all_unique_k_lambda_monotone':all_monotone,
                                    'max_final_sigma':max_final,'min_final_sigma':min(finals),'unique_k_lambda_count':len(unique),'full_grid_run_count':len(records)},
      'records':records,
      'interpretation':('The ordinary-only A constraint forces Delta psi=0 on this difference subspace, so the elliptic M_c filter cancels exactly. The measured transfer therefore tests whether the neutral preferred action fluid itself forgets onset data through its coupled lapse/shift response on the pinned production background.'),
      'next_gate':('If contraction is not universal, localize the retained singular direction before full Boltzmann feedback. If it is universal, implement photon+baryon+massless-UR dual-interface evolution and repeat a full coupled growing/decaying-mode test.'),
      'non_claims':['not full adiabatic-mode uniqueness','not full Boltzmann hierarchy','not massive-neutrino completion','not exact k=0','not parameter selection','not local-window certification','not spectra or likelihood evidence']
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'max_final_sigma':max_final,'min_final_sigma':min(finals),'monotone':all_monotone,'max_mc_invariance':max_mc_invariance,'max_raw_ca_err':max_raw_ca_rel_error,'max_interp_ca_mismatch':tracker['max_interpolated_ca_rel_error'],'max_constraint':tracker['max_res']},sort_keys=True))

if __name__=='__main__': main()
