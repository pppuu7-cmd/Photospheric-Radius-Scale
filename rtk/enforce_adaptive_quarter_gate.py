#!/usr/bin/env python3
"""Post-Stage4D3 adaptive 1/2 -> 1/4 curvature convergence gate.

This layer implements the pre-registered ADAPTIVE_MULTISCALE_CURVATURE_PROTOCOL.
It is intentionally downstream of enforce_stage4d3_multiscale_gate.py and only
acts once a parsed 1/2-stencil result exists.  It also stabilizes already-parsed
half results across later cron iterations.
"""
from __future__ import annotations
import json, os, shutil, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'research/state/current.json'
DISPATCH=ROOT/'research/state/dispatch_request.json'
REPO=os.environ.get('GITHUB_REPOSITORY','pppuu7-cmd/Photospheric-Radius-Scale')
TOKEN=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
QWF='rtk-autonomous-dense-rtk-quarter-stencil.yml'
QART='rtk-autonomous-dense-rtk-quarter-stencil'


def run(cmd,check=True):
    env=os.environ.copy()
    if TOKEN:env['GH_TOKEN']=TOKEN
    p=subprocess.run(cmd,text=True,capture_output=True,env=env)
    if check and p.returncode:raise RuntimeError(p.stderr.strip())
    return p

def gh(endpoint):return json.loads(run(['gh','api',endpoint]).stdout)
def latest(workflow):
    rs=gh(f'repos/{REPO}/actions/workflows/{workflow}/runs?per_page=1').get('workflow_runs',[])
    return rs[0] if rs else None
def get_run(run_id):return gh(f'repos/{REPO}/actions/runs/{int(run_id)}')
def download_summary(run_id,artifact):
    td=Path(tempfile.mkdtemp(prefix=f'rtk-quarter-gate-{run_id}-'))
    try:
        p=run(['gh','run','download',str(run_id),'-R',REPO,'-n',artifact,'-D',str(td)],check=False)
        if p.returncode:return None
        hits=list(td.rglob('summary.json'))
        if len(hits)!=1:raise RuntimeError(f'quarter run {run_id}: expected one summary.json, found {len(hits)}')
        return json.loads(hits[0].read_text())
    finally:shutil.rmtree(td,ignore_errors=True)
def exact_center_equal(a,b):
    keys=('lam','h','Ob','Om','As','ns','zre')
    try:return all(float(a[k])==float(b[k]) for k in keys)
    except Exception:return False

def dispatch(state,wf,target,reason,changes,label):
    if DISPATCH.exists():return
    req={'created_at':state.get('updated_at'),'iteration':state.get('iteration'),'workflow':wf,'ref':'main','reason':reason,'target':target}
    DISPATCH.write_text(json.dumps(req,indent=2,sort_keys=True)+'\n');state['dispatch']=req;changes.append(label)

def comparison(state,tol):
    if state.get('lcdm',{}).get('certification')!='local_dense_accepted':return
    sr=state['rtk'].get('accepted_score_eff');sl=state['lcdm'].get('accepted_score_eff')
    if sr is None or sl is None:return
    sr=float(sr);sl=float(sl)
    state['comparison']={'status':'matched_local_dense_raw_fit_ready','mapping':'eff','S_RTK':sr,'S_LCDM':sl,
      'dense_raw_delta_S':sr-sl,'numerically_indistinguishable_at_0p005':abs(sr-sl)<=tol,
      'interior_minimum_certified':True,
      'warning':'Raw local objective comparison only; not AIC/BIC/Bayes evidence/significance. Adaptive Stage4D3 used adjacent 1/2 and 1/4 PD stencils after exact negative-eigenray falsification of the coarse non-PD scale.'}

def normalized_hessian_diagnostics(half,quarter):
    # NumPy is only needed when a real parsed half+quarter pair exists. Keep it
    # out of import-time control flow so synthetic state-machine tests remain
    # dependency-free on the lightweight orchestrator runner.
    import numpy as np
    he=np.asarray(half['eff']['hessian_y'],float)/(0.5**2)
    qe=np.asarray(quarter['eff']['hessian_y'],float)/(0.25**2)
    rel=float(np.linalg.norm(qe-he)/max(np.linalg.norm(he),1e-300))
    out={'normalized_hessian_frobenius_relative_change_half_to_quarter':rel,
         'half_normalized_eigenvalues':[float(x)/(0.5**2) for x in half['eff']['eigenvalues_y']],
         'quarter_normalized_eigenvalues':[float(x)/(0.25**2) for x in quarter['eff']['eigenvalues_y']]}
    hv=half['eff'].get('eigenvectors_y');qv=quarter['eff'].get('eigenvectors_y')
    if isinstance(hv,list) and isinstance(qv,list) and len(hv)==len(qv)==7:
        H=np.asarray(hv,float);Q=np.asarray(qv,float)
        out['sorted_eigenvector_absolute_overlaps_half_to_quarter']=[float(abs(np.dot(H[i],Q[i]))) for i in range(7)]
    return out

def set_best_score(state,summaries,semantics):
    candidates=[]
    for s in summaries:
        e=s['eff'];candidates.append((float(e['best_exact_S']),e.get('best_params')))
    sbest,pbest=min(candidates,key=lambda x:x[0])
    state['rtk']['accepted_score_eff']=sbest
    if isinstance(pbest,dict):state['rtk']['accepted_score_params']=dict(pbest)
    state['rtk']['accepted_score_semantics']=semantics

def recenter_quarter(state,base,half,quarter,tol,changes):
    rtk=state['rtk'];e=quarter['eff'];imp=float(e['best_improvement']);pars=e.get('best_params')
    if not isinstance(pars,dict):raise RuntimeError('quarter recenter required but best_params missing')
    rtk.setdefault('hessian_history',[]).append(base);rtk.setdefault('half_hessian_history',[]).append(half);rtk.setdefault('quarter_hessian_history',[]).append(quarter)
    rtk['accepted_center']=dict(pars);rtk['accepted_score_eff']=None;rtk['accepted_score_params']=None
    rtk['accepted_score_semantics']='pending_stationarity_after_quarter_stencil_recenter';rtk['raw_candidate_certification']='pending_stationarity_after_quarter_stencil_recenter'
    for k in ('hessian_result','hessian_run','negative_eigenray_result','negative_eigenray_run','half_hessian_result','half_hessian_run','quarter_hessian_result','quarter_hessian_run','multiscale_curvature'):
        rtk[k]=None
    rtk['certification']='needs_recenter_from_quarter_stencil';rtk['interior_minimum_certification']='N5_RESTART_AFTER_QUARTER_STENCIL_DOWNHILL'
    rtk['axis_result']=None;rtk['axis_run']={'run_id':None,'workflow':'rtk-autonomous-dense-rtk-axis.yml','artifact':'rtk-autonomous-dense-rtk-axis','status':'requested'}
    state['stage']='rtk_axis_recenter_running';state['comparison']={'status':'pending_matched_stationarity','dense_raw_delta_S':None}
    dispatch(state,'rtk-autonomous-dense-rtk-axis.yml','rtk_axis',f'quarter-stencil exact improvement {imp:.12g} > {tol}',changes,'recenter_from_quarter_and_dispatch_axis')

def main():
    state=json.loads(STATE.read_text());changes=[];tol=float(state['objective']['recenter_tolerance_S']);rtk=state.get('rtk',{})
    base=rtk.get('hessian_result');half=rtk.get('half_hessian_result');hslot=rtk.get('half_hessian_run')
    if not (isinstance(base,dict) and isinstance(half,dict) and isinstance(hslot,dict) and hslot.get('parsed')):
        print('RTK_ADAPTIVE_QUARTER_GATE',json.dumps(changes));return
    be=base.get('eff') or {};he=half.get('eff') or {}
    if float(be.get('best_improvement',1e99))>tol or float(he.get('best_improvement',1e99))>tol:
        print('RTK_ADAPTIVE_QUARTER_GATE',json.dumps(changes));return
    base_pd=bool(be.get('positive_definite'));half_pd=bool(he.get('positive_definite'))
    ray_clear=(base_pd or rtk.get('negative_eigenray_certification')=='exact_negative_eigenrays_recenter_clear')
    if not ray_clear:
        print('RTK_ADAPTIVE_QUARTER_GATE',json.dumps(changes));return

    if base_pd and half_pd:
        set_best_score(state,[base,half],'best_exact_across_base_and_half_stencils_within_recenter_tolerance')
        rtk['certification']='local_dense_accepted';rtk['interior_minimum_certification']='N5_BASE_AND_HALF_STENCIL_PASS';state['stage']='matched_dense_ready'
        rtk['multiscale_curvature']={'base_positive_definite':True,'half_positive_definite':True,
          'base_min_eigenvalue':min(be['eigenvalues_y']),'half_min_eigenvalue':min(he['eigenvalues_y']),
          'half_best_improvement':float(he['best_improvement']),'negative_eigenray_gate':rtk.get('negative_eigenray_certification')}
        comparison(state,tol);changes.append('stabilize_parsed_base_half_N5_pass')
        STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_ADAPTIVE_QUARTER_GATE',json.dumps(changes));return

    if (not base_pd) and half_pd:
        qslot=rtk.get('quarter_hessian_run')
        if qslot is None:
            rtk['quarter_hessian_run']={'run_id':None,'workflow':QWF,'artifact':QART,'status':'requested','expected_stencil_scale':0.25}
            rtk['certification']='pending_quarter_stencil';rtk['interior_minimum_certification']='N5_ADAPTIVE_PENDING_QUARTER';state['stage']='rtk_quarter_stencil_running';state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None}
            dispatch(state,QWF,'rtk_quarter_hessian','Pre-registered adaptive N5 requires 1/4 stencil after non-PD coarse base, exact-ray clear, and PD half stencil',changes,'dispatch_RTK_quarter_stencil_N5')
            STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_ADAPTIVE_QUARTER_GATE',json.dumps(changes));return
        just_attached=False
        if not qslot.get('run_id'):
            rr=latest(qslot['workflow'])
            if rr:
                qslot['run_id']=int(rr['id']);qslot['status']=rr.get('status');qslot['conclusion']=rr.get('conclusion');qslot['html_url']=rr.get('html_url');just_attached=True;changes.append(f"attach_quarter_run_{qslot['run_id']}")
        else:
            rr=get_run(qslot['run_id']);qslot['status']=rr.get('status');qslot['conclusion']=rr.get('conclusion');qslot['html_url']=rr.get('html_url')
        if qslot.get('status')=='completed' and qslot.get('conclusion')=='success' and not qslot.get('parsed') and not just_attached:
            quarter=download_summary(qslot['run_id'],qslot['artifact'])
            if quarter is None:raise RuntimeError('completed quarter run has no summary')
            if quarter.get('objective')!=state['objective']['name'] or not exact_center_equal(quarter.get('center'),rtk['accepted_center']) or float(quarter.get('stencil_scale',-1))!=0.25:
                raise RuntimeError('quarter artifact identity mismatch')
            rtk['quarter_hessian_result']=quarter;qslot['parsed']=True;qe=quarter.get('eff') or {};qimp=float(qe.get('best_improvement',1e99));changes.append(f'parse_quarter_improvement_{qimp:.12g}')
            if qimp>tol:
                recenter_quarter(state,base,half,quarter,tol,changes)
            elif bool(qe.get('positive_definite')):
                set_best_score(state,[base,half,quarter],'best_exact_across_base_half_quarter_stencils_within_recenter_tolerance')
                diag=normalized_hessian_diagnostics(half,quarter)
                rtk['multiscale_curvature']={'base_positive_definite':False,'half_positive_definite':True,'quarter_positive_definite':True,
                  'base_min_eigenvalue':min(be['eigenvalues_y']),'half_min_eigenvalue':min(he['eigenvalues_y']),'quarter_min_eigenvalue':min(qe['eigenvalues_y']),
                  'half_best_improvement':float(he['best_improvement']),'quarter_best_improvement':qimp,'negative_eigenray_gate':'exact_negative_eigenrays_recenter_clear',**diag}
                rtk['certification']='local_dense_accepted';rtk['interior_minimum_certification']='N5_ADAPTIVE_HALF_AND_QUARTER_PASS';rtk['accepted_proof_stencil_scale']=0.5;rtk['proof_validation_stencil_scale']=0.25
                state['stage']='matched_dense_ready';comparison(state,tol);changes.append('Stage4D3_N5_adaptive_half_quarter_pass')
            else:
                rtk['certification']='matched_raw_candidate_only_curvature_unresolved';rtk['interior_minimum_certification']='N5_ADAPTIVE_QUARTER_NON_PD';state['stage']='rtk_curvature_unresolved';state['comparison']={'status':'matched_dense_raw_candidate_ready_curvature_unresolved','dense_raw_delta_S':None};changes.append('adaptive_quarter_curvature_unresolved')
        elif qslot.get('status')=='completed' and qslot.get('conclusion') not in (None,'success'):
            rtk['certification']='quarter_stencil_compute_failure';rtk['interior_minimum_certification']='N5_BLOCKED_BY_QUARTER_COMPUTE_FAILURE';state['stage']='rtk_quarter_stencil_compute_failure';changes.append('record_quarter_compute_failure')
        elif qslot.get('parsed') and isinstance(rtk.get('quarter_hessian_result'),dict):
            quarter=rtk['quarter_hessian_result'];qe=quarter['eff']
            if float(qe['best_improvement'])<=tol and bool(qe.get('positive_definite')):
                set_best_score(state,[base,half,quarter],'best_exact_across_base_half_quarter_stencils_within_recenter_tolerance')
                rtk['certification']='local_dense_accepted';rtk['interior_minimum_certification']='N5_ADAPTIVE_HALF_AND_QUARTER_PASS';state['stage']='matched_dense_ready';comparison(state,tol);changes.append('stabilize_parsed_adaptive_half_quarter_pass')
        else:
            rtk['certification']='pending_quarter_stencil';rtk['interior_minimum_certification']='N5_ADAPTIVE_PENDING_QUARTER';state['stage']='rtk_quarter_stencil_running';state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None}
        STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
    print('RTK_ADAPTIVE_QUARTER_GATE',json.dumps(changes,sort_keys=True))

if __name__=='__main__':main()
