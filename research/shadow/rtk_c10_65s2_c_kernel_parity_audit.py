#!/usr/bin/env python3
from __future__ import annotations
import ctypes as C, json, math, pathlib, subprocess, sys
P=pathlib.Path
ROOT=P(__file__).resolve().parents[2]

def L(p): return json.load(open(ROOT/p))
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(abs(a),abs(b),1e-300)

class In(C.Structure):
    _fields_=[(x,C.c_double) for x in [
      'k','a','H','Hprime','rb','rg','ru','rk','pk','lambda_HL','Mc','cb2','tau_c','dtau_c','PsiN',
      'delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','sigma_ur','delta_khr_N','theta_khr_N',
      'w_khr','ca2_khr','cs2_khr']]
class Out(C.Structure):
    _fields_=[(x,C.c_double) for x in [
      'B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N_reconstructed','Psi_N_prime','Phi_N','sigma_g','tca_slip',
      'theta_b_prime','theta_g_prime','theta_ur_prime','delta_khr_pref_prime','theta_khr_pref_prime','delta_khr_N_prime','theta_khr_N_prime',
      'metric_continuity','metric_euler','Bprime_affine_f0','Bprime_affine_coefficient','Bprime_implicit_denominator','weighted_slip_cancel',
      'A_residual','A_residual_normalized','Hamiltonian_residual','Hamiltonian_residual_normalized','momentum_residual','momentum_residual_normalized',
      'traceless_residual','traceless_residual_normalized','Psi_reconstruction_relative','feedback_denominator']]

def main():
    s2=L('research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json')
    e=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
    fcond=L('research/theory_results/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_RESULT_v1.json')
    s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    pack=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')['coefficient_pack']
    b=L('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json')
    cur=L('research/state/current.json')
    assert s2['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert fcond['classification']=='C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_PASS_SCOPED'
    so=ROOT/'/tmp/never'
    lib=P('/tmp/libc10_65s2_kernel.so')
    subprocess.run(['gcc','-std=c99','-O2','-shared','-fPIC','-I'+str(ROOT/'rtk'),str(ROOT/'rtk/c10_65s2_kernel.c'),'-lm','-o',str(lib)],check=True)
    dll=C.CDLL(str(lib)); fn=dll.rtk_c10_65s2_current_state; fn.argtypes=[C.POINTER(In),C.POINTER(Out)]; fn.restype=C.c_int

    bg=n['background']; a=float(bg['a']); H=float(bg['H']); rb=float(bg['rhob']); rg=float(bg['rhog']); ru=float(bg['rhour']); rk=float(bg['rho_khr']); pk=float(bg['p_khr'])
    Hps=[float(q['Hc_prime_reconstructed']) for q in b['records']]; Hp=sum(Hps)/len(Hps)
    cb2=float(pack['cb2']); tau=float(pack['tau_c_Mpc']); dtau=float(pack['dtau_c'])
    lamD=float(cur['final_replay_result']['rtk']['params']['lam']); xbg=float(b['background_audit']['x_large_branch_reconstructed'])
    sbg=math.hypot(1.0,math.sqrt(lamD)*xbg); ca2=xbg/(sbg*sbg*(sbg+xbg)); tt=xbg/(sbg+1.0); Q=1.0+xbg/sbg
    mu2=3.0*rk/(2.0*xbg*(1.0+tt)); MK=math.sqrt(mu2)*Q*sbg*math.sqrt(sbg); kstar=a*MK; w=pk/rk
    states={(float(q['lambda_HL']),float(q['M_c_Mpc_inv']),float(q['k'])):q for q in s1['completed_states']}
    emap={(float(q['lambda_HL']),float(q['M_c_Mpc_inv']),float(q['k'])):q for q in e['records']}
    fields={
      'B':'B','B_prime':'B_prime','psi_pref':'psi_pref','psi_pref_prime':'psi_pref_prime','phi_pref':'phi_pref',
      'Psi_N_reconstructed':'Psi_N_reconstructed','Psi_N_prime':'Psi_N_prime','Phi_N':'Phi_N','sigma_g':'sigma_g','tca_slip':'tca_slip',
      'theta_b_prime':'theta_b_prime','theta_g_prime':'theta_g_prime','theta_ur_prime':'theta_ur_prime',
      'delta_khr_pref_prime':'delta_khr_pref_prime','theta_khr_pref_prime':'theta_khr_pref_prime',
      'delta_khr_N_prime':'delta_khr_N_prime','theta_khr_N_prime':'theta_khr_N_prime',
      'metric_continuity':'metric_continuity','metric_euler':'metric_euler',
      'Bprime_affine_coefficient':'Bprime_affine_coefficient','Bprime_implicit_denominator':'Bprime_implicit_denominator',
      'weighted_slip_cancel':'weighted_slip_cancel','feedback_denominator':'feedback_denominator'
    }
    maxima={k:0.0 for k in fields}; records=[]; finite=True; rcok=True
    for key,st in states.items():
        lam,Mc,k=key; cs2=ca2/(1.0+(k/kstar)**2)
        inp=In(k,a,H,Hp,rb,rg,ru,rk,pk,lam,Mc,cb2,tau,dtau,float(st['phi_CLASS']),
          float(st['delta_b']),float(st['theta_b']),float(st['delta_g']),float(st['theta_g']),float(st['delta_ur']),float(st['theta_ur']),float(st['shear_ur']),
          float(st['delta_cdm_khr']),float(st['theta_cdm_khr']),w,ca2,cs2)
        out=Out(); rc=fn(C.byref(inp),C.byref(out)); rcok &= rc==0
        ex=emap[key]['dynamic']; errs={}
        for cfield,pfield in fields.items():
            cv=float(getattr(out,cfield)); pv=float(ex[pfield]); er=rel(cv,pv); errs[cfield]=er; maxima[cfield]=max(maxima[cfield],er); finite &= math.isfinite(cv)
        records.append({'lambda_HL':lam,'M_c_Mpc_inv':Mc,'k':k,'return_code':rc,'errors':errs})
    phys=[k for k in maxima if k not in ['Bprime_affine_coefficient','Bprime_implicit_denominator','weighted_slip_cancel']]
    max_phys=max(maxima[k] for k in phys)
    max_imp=max(maxima['Bprime_affine_coefficient'],maxima['Bprime_implicit_denominator'])
    lim=float(s2['frozen_checks']['max_first_production_rhs_vs_certified_r2_relative'])
    checks={'compile_and_return_codes':rcok,'record_count':len(records)==36,'physical_parity':max_phys<=lim,'implicit_parity':max_imp<=5e-11,'finite':finite,
            'conditioning':float(fcond['global']['max_scalar_implicit_amplification'])<=2.0}
    passed=all(checks.values())
    outj={'schema':'RTK_C10_65S2_C_KERNEL_PARITY_AUDIT_RESULT_v1','classification':'C10_65S2_C_KERNEL_PARITY_PASS_SCOPED' if passed else 'C10_65S2_C_KERNEL_PARITY_FAIL_SCOPED',
          'checks':checks,'maxima':maxima,'max_physical_relative':max_phys,'max_implicit_relative':max_imp,'inherited_rhs_limit':lim,'records':records,'threshold_changed':False,
          'interpretation':'Implementation audit only: standalone C port of the already-certified current-state stack, before production mutation.'}
    (ROOT/'research/theory_results/RTK_C10_65S2_C_KERNEL_PARITY_AUDIT_RESULT_v1.json').write_text(json.dumps(outj,indent=2,sort_keys=True)+'\n')
    print(outj['classification']); print(json.dumps({'max_physical':max_phys,'max_implicit':max_imp},sort_keys=True))
    return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
