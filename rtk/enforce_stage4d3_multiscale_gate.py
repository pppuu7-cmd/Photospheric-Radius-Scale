#!/usr/bin/env python3
"""Conservative post-orchestrator Stage-4D3 multiscale gate.

The generic matched-comparison orchestrator uses the predeclared 0.005 recenter
rule. Stage-4D3 is stronger: before an interior-minimum claim it requires
positive curvature and a smaller-stencil repeat.  In addition, a recenter-clear
but non-PD base Hessian must now pass an exact ray test along every strictly
negative eigenmode before any smaller full Hessian is dispatched.  This closes
the mixed-direction gap exposed by run 32079620601.
"""
from __future__ import annotations
import json,os,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'research/state/current.json';DISPATCH=ROOT/'research/state/dispatch_request.json'
REPO=os.environ.get('GITHUB_REPOSITORY','pppuu7-cmd/Photospheric-Radius-Scale')
TOKEN=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
HALF_WF='rtk-autonomous-dense-rtk-half-stencil.yml';HALF_ART='rtk-autonomous-dense-rtk-half-stencil'
RAY_WF='rtk-autonomous-negative-eigenray.yml';RAY_ART='rtk-autonomous-negative-eigenray'

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
    td=Path(tempfile.mkdtemp(prefix=f'rtk-stage4d3-{run_id}-'))
    try:
        p=run(['gh','run','download',str(run_id),'-R',REPO,'-n',artifact,'-D',str(td)],check=False)
        if p.returncode:return None
        hits=list(td.rglob('summary.json'))
        if len(hits)!=1:raise RuntimeError(f'run {run_id}: expected one summary.json, found {len(hits)}')
        return json.loads(hits[0].read_text())
    finally:shutil.rmtree(td,ignore_errors=True)
def exact_center_equal(a,b):
    keys=('lam','h','Ob','Om','As','ns','zre')
    try:return all(float(a[k])==float(b[k]) for k in keys)
    except Exception:return False

def write_dispatch(state,workflow,target,reason,changes,change_label):
    if DISPATCH.exists():return
    req={'created_at':state.get('updated_at'),'iteration':state.get('iteration'),'workflow':workflow,'ref':'main','reason':reason,'target':target}
    DISPATCH.write_text(json.dumps(req,indent=2,sort_keys=True)+'\n');state['dispatch']=req;changes.append(change_label)

def request_half(state,changes):
    if state['rtk'].get('half_hessian_run') is None:
        state['rtk']['half_hessian_run']={'run_id':None,'workflow':HALF_WF,'artifact':HALF_ART,'status':'requested','expected_stencil_scale':0.5}
    write_dispatch(state,HALF_WF,'rtk_half_hessian','Stage4D3 N5 requires 1/2-stencil stability after base RTK Hessian',changes,'dispatch_RTK_half_stencil_N5')

def request_negative_ray(state,changes):
    if state['rtk'].get('negative_eigenray_run') is None:
        state['rtk']['negative_eigenray_run']={'run_id':None,'workflow':RAY_WF,'artifact':RAY_ART,'status':'requested'}
    write_dispatch(state,RAY_WF,'rtk_negative_eigenray','Stage4D3 exact-ray falsification required for non-PD recenter-clear RTK Hessian',changes,'dispatch_RTK_negative_eigenray_gate')

def set_raw_score_from_base(state,eff):
    if eff.get('best_exact_S') is None:return
    state['rtk']['accepted_score_eff']=float(eff['best_exact_S'])
    if isinstance(eff.get('best_params'),dict):state['rtk']['accepted_score_params']=dict(eff['best_params'])
    state['rtk']['accepted_score_semantics']='best_exact_base_stencil_within_recenter_tolerance'
    state['rtk']['raw_candidate_certification']='matched_dense_recenter_clear_pending_curvature_proof'

def rebuild_comparison(state,tol,curvature_ok):
    if state.get('lcdm',{}).get('certification')!='local_dense_accepted':return
    sr=state.get('rtk',{}).get('accepted_score_eff');sl=state.get('lcdm',{}).get('accepted_score_eff')
    if sr is None or sl is None:return
    sr=float(sr);sl=float(sl);delta=sr-sl
    state['comparison']={'status':('matched_local_dense_raw_fit_ready' if curvature_ok else 'matched_dense_raw_candidate_ready_curvature_unresolved'),
      'mapping':'eff','S_RTK':sr,'S_LCDM':sl,'dense_raw_delta_S':delta,'numerically_indistinguishable_at_0p005':abs(delta)<=tol,
      'interior_minimum_certified':bool(curvature_ok),'warning':'Raw local objective comparison only; not AIC/BIC/Bayes evidence/significance. Stage4D3 interior-minimum wording requires the multiscale curvature gate.'}

def recenter_from_ray(state,base,summary,tol,changes):
    rtk=state['rtk'];imp=float(summary['best_improvement']);pars=summary.get('best_params')
    if not isinstance(pars,dict):raise RuntimeError('negative-eigenray recenter required but best_params missing')
    rtk.setdefault('hessian_history',[]).append(base)
    rtk.setdefault('negative_eigenray_history',[]).append(summary)
    rtk['accepted_center']=dict(pars);rtk['accepted_score_eff']=None;rtk['accepted_score_params']=None
    rtk['accepted_score_semantics']='pending_stationarity_after_negative_eigenray_recenter'
    rtk['raw_candidate_certification']='pending_stationarity_after_negative_eigenray_recenter'
    rtk['hessian_result']=None;rtk['hessian_run']=None;rtk['negative_eigenray_result']=None;rtk['negative_eigenray_run']=None
    rtk['half_hessian_result']=None;rtk['half_hessian_run']=None;rtk['quarter_hessian_run']=None;rtk['multiscale_curvature']=None
    rtk['certification']='needs_recenter_from_negative_eigenray';rtk['interior_minimum_certification']='N5_RESTART_AFTER_NEGATIVE_EIGENRAY_DOWNHILL'
    rtk['axis_result']=None;rtk['axis_run']={'run_id':None,'workflow':'rtk-autonomous-dense-rtk-axis.yml','artifact':'rtk-autonomous-dense-rtk-axis','status':'requested'}
    state['stage']='rtk_axis_recenter_running';state['comparison']={'status':'pending_matched_stationarity','dense_raw_delta_S':None}
    write_dispatch(state,'rtk-autonomous-dense-rtk-axis.yml','rtk_axis',f'negative-eigenray exact improvement {imp:.12g} > {tol}',changes,'recenter_from_negative_eigenray_and_dispatch_axis')

def process_negative_ray(state,base,eff,tol,changes):
    """Return 'clear', 'pending', 'recentered', or 'failed'."""
    rtk=state['rtk']
    if bool(eff.get('positive_definite')):return 'clear'
    slot=rtk.get('negative_eigenray_run')
    if slot is None:
        request_negative_ray(state,changes);rtk['certification']='pending_negative_eigenray';rtk['interior_minimum_certification']='N5_PENDING_NEGATIVE_EIGENRAY';state['stage']='rtk_negative_eigenray_running';return 'pending'
    just_attached=False
    if not slot.get('run_id'):
        rr=latest(slot['workflow'])
        if rr:
            slot['run_id']=int(rr['id']);slot['status']=rr.get('status');slot['conclusion']=rr.get('conclusion');slot['html_url']=rr.get('html_url');just_attached=True;changes.append(f"attach_negative_eigenray_run_{slot['run_id']}")
    elif slot.get('run_id'):
        rr=get_run(slot['run_id']);slot['status']=rr.get('status');slot['conclusion']=rr.get('conclusion');slot['html_url']=rr.get('html_url')
    if slot.get('status')=='completed' and slot.get('conclusion')=='success' and not slot.get('parsed') and not just_attached:
        rs=download_summary(slot['run_id'],slot['artifact'])
        if rs is None:raise RuntimeError('completed negative-eigenray run has no summary')
        if rs.get('objective')!=state['objective']['name']:raise RuntimeError('negative-eigenray objective mismatch')
        if not exact_center_equal(rs.get('center'),rtk['accepted_center']):raise RuntimeError('negative-eigenray center mismatch')
        rtk['negative_eigenray_result']=rs;slot['parsed']=True
        imp=float(rs.get('best_improvement',1e99));changes.append(f'parse_negative_eigenray_improvement_{imp:.12g}')
        if imp>tol:
            recenter_from_ray(state,base,rs,tol,changes);return 'recentered'
        rtk['negative_eigenray_certification']='exact_negative_eigenrays_recenter_clear'
        changes.append('negative_eigenray_gate_clear');return 'clear'
    if slot.get('status')=='completed' and slot.get('conclusion') not in (None,'success'):
        rtk['negative_eigenray_compute_failure']={'run_id':slot.get('run_id'),'conclusion':slot.get('conclusion')};rtk['certification']='negative_eigenray_compute_failure';rtk['interior_minimum_certification']='N5_BLOCKED_BY_NEGATIVE_EIGENRAY_FAILURE';state['stage']='rtk_negative_eigenray_compute_failure';changes.append('record_negative_eigenray_compute_failure');return 'failed'
    if slot.get('parsed') and isinstance(rtk.get('negative_eigenray_result'),dict):
        imp=float(rtk['negative_eigenray_result'].get('best_improvement',1e99))
        if imp<=tol:return 'clear'
    rtk['certification']='pending_negative_eigenray';rtk['interior_minimum_certification']='N5_PENDING_NEGATIVE_EIGENRAY';state['stage']='rtk_negative_eigenray_running';return 'pending'

def main():
    state=json.loads(STATE.read_text());changes=[];tol=float(state['objective']['recenter_tolerance_S']);rtk=state.setdefault('rtk',{})
    base=rtk.get('hessian_result') or {};eff=base.get('eff') or {};base_imp=float(eff.get('best_improvement',1e99));base_slot=rtk.get('hessian_run') or {}
    if base_slot.get('parsed') and eff and base_imp<=tol:
        set_raw_score_from_base(state,eff)
        ray_status=process_negative_ray(state,base,eff,tol,changes)
        if ray_status!='clear':
            state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None}
            STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_MULTISCALE_GATE',json.dumps(changes,sort_keys=True));return
        half=rtk.get('half_hessian_run')
        if half is None:
            rtk['certification']='pending_half_stencil';rtk['interior_minimum_certification']='N5_PENDING_HALF_STENCIL';state['stage']='rtk_half_stencil_running';request_half(state,changes)
        else:
            just_attached=False
            if not half.get('run_id'):
                rr=latest(half['workflow'])
                if rr:
                    half['run_id']=int(rr['id']);half['status']=rr.get('status');half['conclusion']=rr.get('conclusion');half['html_url']=rr.get('html_url');just_attached=True;changes.append(f"attach_half_run_{half['run_id']}")
            elif half.get('run_id'):
                rr=get_run(half['run_id']);half['status']=rr.get('status');half['conclusion']=rr.get('conclusion');half['html_url']=rr.get('html_url')
            if half.get('status')=='completed' and half.get('conclusion')=='success' and not half.get('parsed') and not just_attached:
                hs=download_summary(half['run_id'],half['artifact'])
                if hs is None:raise RuntimeError('completed half-stencil run has no summary')
                if hs.get('objective')!=state['objective']['name']:raise RuntimeError('half-stencil objective mismatch')
                if not exact_center_equal(hs.get('center'),rtk['accepted_center']):raise RuntimeError('half-stencil center mismatch')
                if float(hs.get('stencil_scale',-1))!=0.5:raise RuntimeError('half-stencil scale mismatch')
                rtk['half_hessian_result']=hs;half['parsed']=True;he=hs.get('eff') or {};himp=float(he.get('best_improvement',1e99));changes.append(f'parse_half_stencil_improvement_{himp:.12g}')
                if himp>tol:
                    pars=he.get('best_params')
                    if not isinstance(pars,dict):raise RuntimeError('half-stencil recenter needed but best_params missing')
                    rtk.setdefault('hessian_history',[]).append(base);rtk.setdefault('half_hessian_history',[]).append(hs);rtk['accepted_center']=dict(pars)
                    rtk['accepted_score_eff']=None;rtk['accepted_score_params']=None;rtk['accepted_score_semantics']='pending_stationarity_after_half_stencil_recenter';rtk['raw_candidate_certification']='pending_stationarity_after_half_stencil_recenter'
                    rtk['hessian_result']=None;rtk['hessian_run']=None;rtk['negative_eigenray_result']=None;rtk['negative_eigenray_run']=None;rtk['half_hessian_result']=None;rtk['half_hessian_run']=None;rtk['quarter_hessian_run']=None
                    rtk['certification']='needs_recenter_from_half_stencil';rtk['interior_minimum_certification']='N5_RESTART_AFTER_HALF_STENCIL_DOWNHILL';rtk['axis_result']=None;rtk['axis_run']={'run_id':None,'workflow':'rtk-autonomous-dense-rtk-axis.yml','artifact':'rtk-autonomous-dense-rtk-axis','status':'requested'};state['stage']='rtk_axis_recenter_running';state['comparison']={'status':'pending_matched_stationarity','dense_raw_delta_S':None}
                    write_dispatch(state,'rtk-autonomous-dense-rtk-axis.yml','rtk_axis',f'half-stencil exact improvement {himp:.9g} > {tol}',changes,'recenter_from_half_stencil_and_dispatch_axis')
                else:
                    candidates=[(float(eff['best_exact_S']),eff.get('best_params')),(float(he['best_exact_S']),he.get('best_params'))];sbest,pbest=min(candidates,key=lambda x:x[0]);rtk['accepted_score_eff']=sbest
                    if isinstance(pbest,dict):rtk['accepted_score_params']=dict(pbest)
                    rtk['accepted_score_semantics']='best_exact_across_base_and_half_stencils_within_recenter_tolerance';base_pd=bool(eff.get('positive_definite'));half_pd=bool(he.get('positive_definite'))
                    rtk['multiscale_curvature']={'base_positive_definite':base_pd,'half_positive_definite':half_pd,'base_min_eigenvalue':min(eff.get('eigenvalues_y',[float('nan')])),'half_min_eigenvalue':min(he.get('eigenvalues_y',[float('nan')])),'half_best_improvement':himp,'negative_eigenray_gate':rtk.get('negative_eigenray_certification')}
                    if base_pd and half_pd:
                        rtk['certification']='local_dense_accepted';rtk['interior_minimum_certification']='N5_BASE_AND_HALF_STENCIL_PASS';state['stage']='matched_dense_ready';rebuild_comparison(state,tol,True);changes.append('Stage4D3_N5_multiscale_pass')
                    else:
                        rtk['certification']='matched_raw_candidate_only_curvature_unresolved';rtk['interior_minimum_certification']='N5_CURVATURE_UNRESOLVED';state['stage']='rtk_curvature_unresolved';rebuild_comparison(state,tol,False);changes.append('Stage4D3_N5_curvature_unresolved')
            elif half.get('status')=='completed' and half.get('conclusion') not in (None,'success'):
                rtk['half_hessian_run_compute_failure']={'run_id':half.get('run_id'),'conclusion':half.get('conclusion')};rtk['certification']='half_stencil_compute_failure';rtk['interior_minimum_certification']='N5_BLOCKED_BY_COMPUTE_FAILURE';state['stage']='rtk_half_stencil_compute_failure';changes.append('record_half_stencil_compute_failure')
            else:
                rtk['certification']='pending_half_stencil';rtk['interior_minimum_certification']='N5_PENDING_HALF_STENCIL';state['stage']='rtk_half_stencil_running'
        if rtk.get('certification') in ('pending_half_stencil','pending_negative_eigenray'):
            state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None}
    STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
    print('RTK_STAGE4D3_MULTISCALE_GATE',json.dumps(changes,sort_keys=True))
if __name__=='__main__':main()
