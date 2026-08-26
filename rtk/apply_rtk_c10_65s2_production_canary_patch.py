#!/usr/bin/env python3
"""Apply the frozen C10.65s2 one-step production canary to a disposable pinned CLASS tree.

The patch is opt-in and dormant by default.  Ordinary/full scalar initial data are
written only from perturb_initial_conditions ownership.  The only explicit writes
after perturb_vector_init are the two Khronon carrier slots (CDM delta/theta).
During the canary step, the completed current-state C kernel replaces only the
Newtonian metric constraint outputs and the two CDM/Khronon RHS slots.  Native
photon/baryon/UR and compromise_CLASS TCA equations remain source-locked.
"""
from pathlib import Path
import json,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public').resolve()
repo=Path(__file__).resolve().parents[1]
pt=root/'source'/'perturbations.c'; ph=root/'include'/'perturbations.h'
bh=root/'include'/'background.h'; inc=root/'source'/'input.c'; mk=root/'Makefile'
ps=pt.read_text(); hs=ph.read_text(); bs=bh.read_text(); ins=inc.read_text(); ms=mk.read_text()
marker='RTK_C10_65S2_PRODUCTION_CANARY_V1'
if marker in ps:
    print('C10_65S2_PRODUCTION_CANARY_PATCH_ALREADY_APPLIED'); raise SystemExit(0)

plan=json.loads((repo/'research/theory_targets/RTK_C10_65S2_PRODUCTION_IMPLEMENTATION_PLAN_v1.json').read_text())
target=json.loads((repo/'research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json').read_text())
s1=json.loads((repo/'research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json').read_text())
assert plan['status']=='FROZEN_BEFORE_PRODUCTION_EXECUTION'
assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
dom=plan['scope']; lam=float(dom['lambda_HL']); Mc=float(dom['M_c_Mpc_inv']); aon=float(dom['a_on'])
ks=[float(x) for x in dom['k_Mpc_inv']]
states=[q for q in s1['completed_states'] if float(q['lambda_HL'])==lam and float(q['M_c_Mpc_inv'])==Mc and float(q['k']) in ks]
states.sort(key=lambda q:ks.index(float(q['k'])))
assert len(states)==4
assert s1['approximation_state']['TCA_enum']==0 and s1['approximation_state']['RSA_enum']==0 and s1['approximation_state']['UFA_enum']==0
assert int(s1['approximation_state']['l_max_ur'])==17

# Background runtime inputs. Defaults are dormant and frozen-domain values.
needle='  double gnl;/**gamma*/\n'
if needle not in bs: raise SystemExit('background gnl anchor missing')
add=('  double c10_65s2_canary;/** frozen C10.65s2 opt-in production canary */\n'
     '  double c10_65s2_lambda_HL;/** completed gravity lambda */\n'
     '  double c10_65s2_Mc;/** completed gravity mass in 1/Mpc */\n'
     '  double c10_65s2_a_on;/** direct certified onset scale factor */\n')
bs=bs.replace(needle,needle+add,1)

read_anchor='  class_read_double("model",pba->model);\n'
if read_anchor not in ins: raise SystemExit('model parser anchor missing')
read_add=f'''  pba->c10_65s2_canary = 0.;
  pba->c10_65s2_lambda_HL = {lam:.17g};
  pba->c10_65s2_Mc = {Mc:.17g};
  pba->c10_65s2_a_on = {aon:.17g};
  class_read_double("c10_65s2_canary",pba->c10_65s2_canary);
  class_read_double("c10_65s2_lambda_HL",pba->c10_65s2_lambda_HL);
  class_read_double("c10_65s2_Mc",pba->c10_65s2_Mc);
  class_read_double("c10_65s2_a_on",pba->c10_65s2_a_on);
  class_test((pba->c10_65s2_canary != 0.) && (pba->c10_65s2_canary != 1.),errmsg,"c10_65s2_canary must be 0 or 1");
  class_test((pba->c10_65s2_canary > 0.5) && !(pba->c10_65s2_lambda_HL > 1.),errmsg,"c10_65s2_lambda_HL must exceed 1");
  class_test((pba->c10_65s2_canary > 0.5) && !(pba->c10_65s2_Mc > 0.),errmsg,"c10_65s2_Mc must be positive");
  class_test((pba->c10_65s2_canary > 0.5) && !(pba->c10_65s2_a_on > 0.),errmsg,"c10_65s2_a_on must be positive");
'''
ins=ins.replace(read_anchor,read_add+read_anchor,1)

# Canary-only workspace counters; initialized per solve.
wa='  int index_ikout; /**< index for output k value */\n'
if wa not in hs: raise SystemExit('workspace anchor missing')
hs=hs.replace(wa,wa+'  int c10_65s2_active; /**< completed-U1 canary feedback active only during frozen short step */\n  int c10_65s2_rhs_calls; /**< metric RHS evaluations during the short-step audit */\n',1)

# Build immutable boundary table from the already-certified s1 finite states.
def f(x): return format(float(x),'.17g')
rows=[]
for q in states:
    F=[float(q['higher_order_historical_control'][str(l)]) for l in range(3,18)]
    rows.append('  {'+','.join([f(q['k']),f(q['phi_CLASS']),f(q['delta_b']),f(q['theta_b']),f(q['delta_g']),f(q['theta_g']),f(q['delta_ur']),f(q['theta_ur']),f(q['shear_ur']),f(q['delta_cdm_khr']),f(q['theta_cdm_khr'])]) + ',{' + ','.join(f(x) for x in F) + '}}')
seed_table=',\n'.join(rows)
bridge_h=f'''#ifndef RTK_C10_65S2_CLASS_BRIDGE_H
#define RTK_C10_65S2_CLASS_BRIDGE_H
#include "perturbations.h"
#include "c10_65s2_kernel.h"
int rtk_c10_65s2_mode_enabled(struct background*,struct perturbs*,int,double);
int rtk_c10_65s2_seed_owned(struct background*,struct perturbs*,int,double,struct perturb_workspace*,ErrorMsg);
int rtk_c10_65s2_handoff_khronon(struct background*,struct perturbs*,int,double,struct perturb_workspace*,ErrorMsg);
int rtk_c10_65s2_metric(struct precision*,struct background*,struct thermo*,struct perturbs*,int,double,double*,struct perturb_workspace*,ErrorMsg);
int rtk_c10_65s2_cdm_rhs(struct background*,struct perturbs*,int,double,double*,double*,struct perturb_workspace*,ErrorMsg);
int rtk_c10_65s2_observe(const char*,double,double*,double*,void*,ErrorMsg);
#endif
'''
(root/'include'/'rtk_c10_65s2_class_bridge.h').write_text(bridge_h)
bridge_c=f'''/* {marker}: generated from frozen s1 boundary data; dynamic feedback uses c10_65s2_kernel. */
#include "rtk_c10_65s2_class_bridge.h"
#include "khronon_background.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {{ double k,phi,db,tb,dg,tg,du,tu,su,dk,tk; double Fl[15]; }} s2seed;
static const s2seed S[4]={{
{seed_table}
}};
static const double DT={float(plan['execution']['short_step_delta_tau_Mpc']):.17g};
double rtk_c10_65s2_short_dt(void){{return DT;}}
static const s2seed *seed(double k){{
  int i; for(i=0;i<4;i++) if (fabs(k-S[i].k)<=1e-13*fmax(1.,fabs(S[i].k))) return &S[i]; return NULL;
}}
int rtk_c10_65s2_mode_enabled(struct background *pba,struct perturbs *ppt,int index_md,double k){{
  return pba->c10_65s2_canary>0.5 && ppt->has_scalars==_TRUE_ && index_md==ppt->index_md_scalars && seed(k)!=NULL;
}}
int rtk_c10_65s2_seed_owned(struct background *pba,struct perturbs *ppt,int index_md,double k,struct perturb_workspace *ppw,ErrorMsg error_message){{
  const s2seed *s; int l; struct perturb_vector *pv=ppw->pv;
  if(!rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) return _SUCCESS_;
  s=seed(k); class_test(s==NULL,error_message,"C10.65s2 seed lookup failed");
  class_test(ppt->gauge!=newtonian,error_message,"C10.65s2 requires Newtonian gauge");
  class_test(ppw->approx[ppw->index_ap_tca]!=(int)tca_on || ppw->approx[ppw->index_ap_rsa]!=(int)rsa_off || ppw->approx[ppw->index_ap_ufa]!=(int)ufa_off,error_message,"C10.65s2 frozen approximation state mismatch");
  class_test(pv->l_max_ur!=17,error_message,"C10.65s2 requires l_max_ur=17");
  pv->y[pv->index_pt_phi]=s->phi;
  pv->y[pv->index_pt_delta_b]=s->db; pv->y[pv->index_pt_theta_b]=s->tb;
  pv->y[pv->index_pt_delta_g]=s->dg; pv->y[pv->index_pt_theta_g]=s->tg;
  pv->y[pv->index_pt_delta_ur]=s->du; pv->y[pv->index_pt_theta_ur]=s->tu; pv->y[pv->index_pt_shear_ur]=s->su;
  for(l=3;l<=17;l++) pv->y[pv->index_pt_l3_ur+(l-3)]=s->Fl[l-3];
  return _SUCCESS_;
}}
int rtk_c10_65s2_handoff_khronon(struct background *pba,struct perturbs *ppt,int index_md,double k,struct perturb_workspace *ppw,ErrorMsg error_message){{
  const s2seed *s; struct perturb_vector *pv=ppw->pv;
  if(!rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) return _SUCCESS_;
  s=seed(k); class_test(s==NULL,error_message,"C10.65s2 handoff seed lookup failed");
  class_test(pv->index_pt_delta_cdm<0 || pv->index_pt_theta_cdm<0,error_message,"C10.65s2 Khronon carrier slots unavailable");
  /* Frozen post-vector write whitelist: exactly these two integrated slots. */
  pv->y[pv->index_pt_delta_cdm]=s->dk;
  pv->y[pv->index_pt_theta_cdm]=s->tk;
  return _SUCCESS_;
}}
static int eval(struct background *pba,struct perturbs *ppt,int index_md,double k,double *y,struct perturb_workspace *ppw,rtk_c10_65s2_output *o,ErrorMsg error_message){{
  rtk_c10_65s2_input in; khr_params kp; khr_closure kc; khr_state kb; int st; double a,H,tau_c;
  if(!rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) return _FAILURE_;
  a=ppw->pvecback[pba->index_bg_a]; H=a*ppw->pvecback[pba->index_bg_H];
  kp.H0=pba->H0; kp.gamma=pba->gnl; kp.lambda_D=pba->lambda_D; kp.Omega_K0=pba->Omega0_cdm;
  st=khr_closure_from_params(&kp,&kc); class_test(st!=KHR_OK,error_message,"C10.65s2 Khronon closure failed: %s",khr_status_string(st));
  st=khr_background(&kp,&kc,a/pba->a_today,k,&kb); class_test(st!=KHR_OK,error_message,"C10.65s2 Khronon background failed: %s",khr_status_string(st));
  tau_c=1./ppw->pvecthermo[pth->index_th_dkappa];
  memset(&in,0,sizeof(in));
  in.k=k; in.a=a; in.H=H; in.Hprime=a*ppw->pvecback[pba->index_bg_H_prime]+H*H;
  in.rb=ppw->pvecback[pba->index_bg_rho_b]; in.rg=ppw->pvecback[pba->index_bg_rho_g]; in.ru=ppw->pvecback[pba->index_bg_rho_ur];
  in.rk=kb.rho8piG/3.; in.pk=kb.p8piG/3.; in.lambda_HL=pba->c10_65s2_lambda_HL; in.Mc=pba->c10_65s2_Mc;
  in.cb2=ppw->pvecthermo[pth->index_th_cb2]; in.tau_c=tau_c; in.dtau_c=-ppw->pvecthermo[pth->index_th_ddkappa]*tau_c*tau_c;
  in.PsiN=y[ppw->pv->index_pt_phi];
  in.delta_b=y[ppw->pv->index_pt_delta_b]; in.theta_b=y[ppw->pv->index_pt_theta_b];
  in.delta_g=y[ppw->pv->index_pt_delta_g]; in.theta_g=y[ppw->pv->index_pt_theta_g];
  in.delta_ur=y[ppw->pv->index_pt_delta_ur]; in.theta_ur=y[ppw->pv->index_pt_theta_ur]; in.sigma_ur=y[ppw->pv->index_pt_shear_ur];
  in.delta_khr_N=y[ppw->pv->index_pt_delta_cdm]; in.theta_khr_N=y[ppw->pv->index_pt_theta_cdm];
  in.w_khr=kb.w; in.ca2_khr=kb.ca2; in.cs2_khr=kb.cs2;
  st=rtk_c10_65s2_current_state(&in,o); class_test(st!=0,error_message,"C10.65s2 current-state kernel failed code %d",st);
  return _SUCCESS_;
}}
int rtk_c10_65s2_metric(struct precision *ppr,struct background *pba,struct thermo *pth,struct perturbs *ppt,int index_md,double k,double *y,struct perturb_workspace *ppw,ErrorMsg error_message){{
  rtk_c10_65s2_output o; class_call(eval(pba,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);
  ppw->pvecmetric[ppw->index_mt_psi]=o.Phi_N;
  ppw->pvecmetric[ppw->index_mt_phi_prime]=o.Psi_N_prime;
  ppw->c10_65s2_rhs_calls++;
  return _SUCCESS_;
}}
int rtk_c10_65s2_cdm_rhs(struct background *pba,struct perturbs *ppt,int index_md,double k,double *y,double *dy,struct perturb_workspace *ppw,ErrorMsg error_message){{
  rtk_c10_65s2_output o; class_call(eval(pba,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);
  dy[ppw->pv->index_pt_delta_cdm]=o.delta_khr_N_prime;
  dy[ppw->pv->index_pt_theta_cdm]=o.theta_khr_N_prime;
  return _SUCCESS_;
}}
int rtk_c10_65s2_observe(const char *phase,double tau,double *y,double *dy,void *parameters_and_workspace,ErrorMsg error_message){{
  struct perturb_parameters_and_workspace *ppaw=(struct perturb_parameters_and_workspace*)parameters_and_workspace; struct perturb_workspace *ppw=ppaw->ppw; struct perturb_vector *pv=ppw->pv;
  struct background *pba=ppaw->pba; struct perturbs *ppt=ppaw->ppt; const char *path=getenv("RTK_C10_65S2_OBSERVER_FILE"); FILE *fp; rtk_c10_65s2_output o; int l;
  if(path==NULL || path[0]=='\\0' || !rtk_c10_65s2_mode_enabled(pba,ppt,ppaw->index_md,ppaw->k)) return _SUCCESS_;
  class_call(eval(pba,ppt,ppaw->index_md,ppaw->k,y,ppw,&o,error_message),error_message,error_message);
  fp=fopen(path,"a"); class_test(fp==NULL,error_message,"C10.65s2 cannot open observer file");
  fprintf(fp,"%s,%.17e,%.17e,%.17e,%d,%d,%d,%d,%d",phase,tau,ppw->pvecback[pba->index_bg_a],ppaw->k,ppw->approx[ppw->index_ap_tca],ppw->approx[ppw->index_ap_rsa],ppw->approx[ppw->index_ap_ufa],pv->l_max_ur,ppw->c10_65s2_rhs_calls);
  fprintf(fp,",%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e",y[pv->index_pt_phi],y[pv->index_pt_delta_b],y[pv->index_pt_theta_b],y[pv->index_pt_delta_g],y[pv->index_pt_theta_g],y[pv->index_pt_delta_ur],y[pv->index_pt_theta_ur],y[pv->index_pt_shear_ur],y[pv->index_pt_delta_cdm],y[pv->index_pt_theta_cdm]);
  if(dy) fprintf(fp,",%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e",dy[pv->index_pt_phi],dy[pv->index_pt_delta_b],dy[pv->index_pt_theta_b],dy[pv->index_pt_delta_g],dy[pv->index_pt_theta_g],dy[pv->index_pt_delta_ur],dy[pv->index_pt_theta_ur],dy[pv->index_pt_delta_cdm],dy[pv->index_pt_theta_cdm]);
  else fprintf(fp,",nan,nan,nan,nan,nan,nan,nan,nan,nan");
  fprintf(fp,",%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e",o.B,o.B_prime,o.psi_pref,o.psi_pref_prime,o.phi_pref,o.Psi_N_reconstructed,o.Psi_N_prime,o.Phi_N,o.sigma_g,o.tca_slip);
  fprintf(fp,",%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e",o.A_residual,o.A_residual_normalized,o.Hamiltonian_residual,o.Hamiltonian_residual_normalized,o.momentum_residual,o.momentum_residual_normalized,o.traceless_residual,o.traceless_residual_normalized,o.feedback_denominator,o.Bprime_implicit_denominator);
  for(l=3;l<=17;l++) fprintf(fp,",%.17e",y[pv->index_pt_l3_ur+(l-3)]);
  fputc('\\n',fp); fclose(fp); return _SUCCESS_;
}}
'''
(root/'source'/'rtk_c10_65s2_class_bridge.c').write_text(bridge_c)

# Copy the already-audited pure dynamic kernel into this disposable CLASS tree.
(root/'source'/'c10_65s2_kernel.c').write_text((repo/'rtk/c10_65s2_kernel.c').read_text())
(root/'include'/'c10_65s2_kernel.h').write_text((repo/'rtk/c10_65s2_kernel.h').read_text())

# Include bridge API in perturbations.c.
inc_anchor='#include "perturbations.h"\n'
if inc_anchor not in ps: raise SystemExit('perturbations include anchor missing')
ps=ps.replace(inc_anchor,inc_anchor+'#include "rtk_c10_65s2_class_bridge.h" /* '+marker+' */\n',1)

# Start the four opt-in modes directly at frozen a_on before approximation interval construction.
solve_start=ps.find('int perturb_solve('); solve_end=ps.find('int perturb_prepare_output(',solve_start)
if solve_start<0 or solve_end<0: raise SystemExit('cannot bound perturb_solve')
seg=ps[solve_start:solve_end]
tau_anchor='  tau = tau_mid;\n'
if tau_anchor not in seg: raise SystemExit('perturb_solve tau anchor missing')
tau_add='''  if (rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) {
    class_call(background_tau_of_z(pba,1./pba->c10_65s2_a_on-1.,&tau),pba->error_message,ppt->error_message);
  }
'''
pos=solve_start+seg.index(tau_anchor)+len(tau_anchor); ps=ps[:pos]+tau_add+ps[pos:]

# Initialize canary workspace state once per perturb_solve.
solve_start=ps.find('int perturb_solve('); solve_end=ps.find('int perturb_prepare_output(',solve_start); seg=ps[solve_start:solve_end]
k_anchor='  k = ppt->k[index_md][index_k];\n'
pos=solve_start+seg.index(k_anchor)+len(k_anchor); ps=ps[:pos]+'  ppw->c10_65s2_active = 0;\n  ppw->c10_65s2_rhs_calls = 0;\n'+ps[pos:]

# Ordinary/full-state boundary ownership: append completed seed at the end of perturb_initial_conditions.
def insert_before_success(text,funcsig,code):
    st=text.find(funcsig); 
    if st<0: raise SystemExit('function missing '+funcsig)
    nx=text.find('\nint ',st+len(funcsig)); en=len(text) if nx<0 else nx
    seg=text[st:en]; r=seg.rfind('return _SUCCESS_;')
    if r<0: raise SystemExit('success return missing '+funcsig)
    p=st+r; return text[:p]+code+text[p:]
ps=insert_before_success(ps,'int perturb_initial_conditions(','  class_call(rtk_c10_65s2_seed_owned(pba,ppt,index_md,k,ppw,ppt->error_message),ppt->error_message,ppt->error_message);\n\n  ')

# Metric feedback: insert a canary branch before historical model=2 equations.
old='''      else if (pba->model == 2.){
          /* equation for psi */'''
new='''      else if ((pba->model == 2.) && (ppw->c10_65s2_active == 1) && rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)){
          class_call(rtk_c10_65s2_metric(ppr,pba,pth,ppt,index_md,k,y,ppw,ppt->error_message),ppt->error_message,ppt->error_message);
      }
      else if (pba->model == 2.){
          /* equation for psi */'''
if old not in ps: raise SystemExit('model2 metric anchor missing')
ps=ps.replace(old,new,1)

# Khronon production RHS: only the two repurposed CDM derivative slots change while active.
old='''      if (ppt->gauge == newtonian) {
        dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity); /* cdm density */

        dy[pv->index_pt_theta_cdm] = - a_prime_over_a*y[pv->index_pt_theta_cdm] + metric_euler; /* cdm velocity */
      }'''
new='''      if (ppt->gauge == newtonian) {
        if ((pba->model == 2.) && (ppw->c10_65s2_active == 1) && rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) {
          class_call(rtk_c10_65s2_cdm_rhs(pba,ppt,index_md,k,y,dy,ppw,error_message),error_message,error_message);
        }
        else {
          dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity); /* cdm density */
          dy[pv->index_pt_theta_cdm] = - a_prime_over_a*y[pv->index_pt_theta_cdm] + metric_euler; /* cdm velocity */
        }
      }'''
if old not in ps: raise SystemExit('CDM derivative anchor missing')
ps=ps.replace(old,new,1)

# One-step canary after normal vector initialization and evolver selection.  It performs
# the only allowed post-vector writes, captures the first production RHS, then runs
# exactly one prospective short RK interval.  The ON solve terminates afterwards so
# completed state is never silently handed back to historical model=2 evolution.
solve_start=ps.find('int perturb_solve('); solve_end=ps.find('int perturb_prepare_output(',solve_start); seg=ps[solve_start:solve_end]
evol_anchor='''    else{
      generic_evolver = evolver_ndf15;
    }

    class_call(generic_evolver(perturb_derivs,'''
if evol_anchor not in seg: raise SystemExit('generic evolver anchor missing')
canary='''    else{
      generic_evolver = evolver_ndf15;
    }

    if ((index_interval==0) && rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) {
      double c10_65s2_end;
      class_test(ppr->evolver != rk,ppt->error_message,"C10.65s2 frozen implementation requires evolver=rk");
      class_call(rtk_c10_65s2_handoff_khronon(pba,ppt,index_md,k,ppw,ppt->error_message),ppt->error_message,ppt->error_message);
      ppw->c10_65s2_active=1;
      ppw->c10_65s2_rhs_calls=0;
      class_call(perturb_derivs(interval_limit[index_interval],ppw->pv->y,ppw->pv->dy,&ppaw,ppt->error_message),ppt->error_message,ppt->error_message);
      class_call(rtk_c10_65s2_observe("BEFORE",interval_limit[index_interval],ppw->pv->y,ppw->pv->dy,&ppaw,ppt->error_message),ppt->error_message,ppt->error_message);
      ppw->c10_65s2_rhs_calls=0;
      c10_65s2_end=interval_limit[index_interval]+rtk_c10_65s2_short_dt();
      class_test(!(c10_65s2_end < interval_limit[index_interval+1]),ppt->error_message,"C10.65s2 short step does not fit first approximation interval");
      class_call(generic_evolver(perturb_derivs,
                                 interval_limit[index_interval],c10_65s2_end,
                                 ppw->pv->y,ppw->pv->used_in_sources,ppw->pv->pt_size,&ppaw,
                                 ppr->tol_perturb_integration,ppr->smallest_allowed_variation,
                                 perturb_timescale,ppr->perturb_integration_stepsize,
                                 ppt->tau_sampling,tau_actual_size,perturb_sources,NULL,ppt->error_message),
                 ppt->error_message,ppt->error_message);
      class_call(rtk_c10_65s2_observe("AFTER",c10_65s2_end,ppw->pv->y,NULL,&ppaw,ppt->error_message),ppt->error_message,ppt->error_message);
      ppw->c10_65s2_active=0;
      tau_actual_size=0;
      goto c10_65s2_finish;
    }

    class_call(generic_evolver(perturb_derivs,'''
abspos=solve_start+seg.index(evol_anchor); ps=ps[:abspos]+canary+ps[abspos+len(evol_anchor):]
# Label existing zero-fill/cleanup tail.
solve_start=ps.find('int perturb_solve('); solve_end=ps.find('int perturb_prepare_output(',solve_start); seg=ps[solve_start:solve_end]
finish_anchor='''  /** - if perturbations were printed in a file, close the file */'''
if finish_anchor not in seg: raise SystemExit('finish anchor missing')
pos=solve_start+seg.index(finish_anchor); ps=ps[:pos]+'c10_65s2_finish:\n\n'+ps[pos:]

pt.write_text(ps); ph.write_text(hs); bh.write_text(bs); inc.write_text(ins)

# Link bridge + pure kernel into disposable CLASS.
source_anchor='SOURCE = input.o background.o thermodynamics.o perturbations.o primordial.o nonlinear.o transfer.o spectra.o lensing.o'
if source_anchor not in ms: raise SystemExit('Makefile SOURCE anchor missing')
if 'rtk_c10_65s2_class_bridge.o' not in ms:
    ms=ms.replace(source_anchor,source_anchor+' rtk_c10_65s2_class_bridge.o c10_65s2_kernel.o',1)
mk.write_text(ms)

print('C10_65S2_PRODUCTION_CANARY_PATCH_APPLIED')
