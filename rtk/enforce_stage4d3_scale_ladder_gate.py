#!/usr/bin/env python3
"""Fallback Stage-4D3 adjacent-scale ladder for base-PD / half-non-PD cases.

Pre-registered in STAGE4D3_ADAPTIVE_SCALE_LADDER_PROTOCOL.md before consuming
run 32133215190. This gate is downstream of the ordinary multiscale and
adaptive-quarter gates and is inert for their already-covered branches.

Every non-PD tested scale, including the terminal 1/8 scale, must be falsified
by an exact negative-eigenray at the same physical stencil scale before the
ladder may descend further or declare curvature unresolved.
"""
from __future__ import annotations
import json,os,shutil,subprocess,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'research/state/current.json';DISPATCH=ROOT/'research/state/dispatch_request.json'
REPO=os.environ.get('GITHUB_REPOSITORY','pppuu7-cmd/Photospheric-Radius-Scale');TOKEN=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
HALF_RAY_WF='rtk-autonomous-half-negative-eigenray.yml';HALF_RAY_ART='rtk-autonomous-half-negative-eigenray'
QUARTER_RAY_WF='rtk-autonomous-quarter-negative-eigenray.yml';QUARTER_RAY_ART='rtk-autonomous-quarter-negative-eigenray'
EIGHTH_RAY_WF='rtk-autonomous-eighth-negative-eigenray.yml';EIGHTH_RAY_ART='rtk-autonomous-eighth-negative-eigenray'
QUARTER_WF='rtk-autonomous-dense-rtk-quarter-stencil.yml';QUARTER_ART='rtk-autonomous-dense-rtk-quarter-stencil'
EIGHTH_WF='rtk-autonomous-dense-rtk-eighth-stencil.yml';EIGHTH_ART='rtk-autonomous-dense-rtk-eighth-stencil'

def run(cmd,check=True):
    env=os.environ.copy()
    if TOKEN:env['GH_TOKEN']=TOKEN
    p=subprocess.run(cmd,text=True,capture_output=True,env=env)
    if check and p.returncode:raise RuntimeError(p.stderr.strip())
    return p

def gh(endpoint):return json.loads(run(['gh','api',endpoint]).stdout)
def latest(workflow):
    rs=gh(f'repos/{REPO}/actions/workflows/{workflow}/runs?per_page=1').get('workflow_runs',[]);return rs[0] if rs else None
def get_run(run_id):return gh(f'repos/{REPO}/actions/runs/{int(run_id)}')
def download_summary(run_id,artifact):
    td=Path(tempfile.mkdtemp(prefix=f'rtk-ladder-{run_id}-'))
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

def dispatch(state,wf,target,reason,changes,label):
    if DISPATCH.exists():return
    req={'created_at':state.get('updated_at'),'iteration':state.get('iteration'),'workflow':wf,'ref':'main','reason':reason,'target':target}
    DISPATCH.write_text(json.dumps(req,indent=2,sort_keys=True)+'\n');state['dispatch']=req;changes.append(label)

def refresh_slot(slot,changes,label):
    """Update run metadata and defer parse one cycle after first completion."""
    if not slot.get('run_id'):
        rr=latest(slot['workflow'])
        if rr:
            slot['run_id']=int(rr['id']);slot['status']=rr.get('status');slot['conclusion']=rr.get('conclusion');slot['html_url']=rr.get('html_url');changes.append(f'attach_{label}_{slot["run_id"]}')
            return slot.get('status')=='completed'
        return False
    old=slot.get('status');rr=get_run(slot['run_id']);slot['status']=rr.get('status');slot['conclusion']=rr.get('conclusion');slot['html_url']=rr.get('html_url')
    return old!='completed' and slot.get('status')=='completed'

def validate_common(state,s,scale=None,source=None):
    if s.get('objective')!=state['objective']['name']:raise RuntimeError('scale-ladder artifact objective mismatch')
    if not exact_center_equal(s.get('center'),state['rtk']['accepted_center']):raise RuntimeError('scale-ladder artifact center mismatch')
    if scale is not None and abs(float(s.get('stencil_scale',-1))-scale)>1e-15:raise RuntimeError('scale-ladder Hessian scale mismatch')
    if source is not None:
        expected={'half':0.5,'quarter':0.25,'eighth':0.125}[source]
        if s.get('eigenray_source')!=source or abs(float(s.get('source_stencil_scale',-1))-expected)>1e-15:raise RuntimeError('scale-ladder eigenray source mismatch')

def clear_for_recenter(rtk):
    for k in ('hessian_result','hessian_run','negative_eigenray_result','negative_eigenray_run',
              'half_hessian_result','half_hessian_run','half_negative_eigenray_result','half_negative_eigenray_run',
              'quarter_hessian_result','quarter_hessian_run','quarter_negative_eigenray_result','quarter_negative_eigenray_run',
              'eighth_hessian_result','eighth_hessian_run','eighth_negative_eigenray_result','eighth_negative_eigenray_run',
              'multiscale_curvature'):
        rtk[k]=None

def recenter(state,summary,reason,changes):
    rtk=state['rtk'];pars=summary.get('best_params') or (summary.get('eff') or {}).get('best_params')
    if not isinstance(pars,dict):raise RuntimeError('scale-ladder recenter required but best_params missing')
    rtk['accepted_center']=dict(pars);rtk['accepted_score_eff']=None;rtk['accepted_score_params']=None;rtk['accepted_score_semantics']='pending_stationarity_after_scale_ladder_recenter';rtk['raw_candidate_certification']='pending_stationarity_after_scale_ladder_recenter'
    clear_for_recenter(rtk);rtk['certification']='needs_recenter_from_scale_ladder';rtk['interior_minimum_certification']='N5_RESTART_AFTER_SCALE_LADDER_DOWNHILL'
    rtk['axis_result']=None;rtk['axis_run']={'run_id':None,'workflow':'rtk-autonomous-dense-rtk-axis.yml','artifact':'rtk-autonomous-dense-rtk-axis','status':'requested'}
    state['stage']='rtk_axis_recenter_running';state['comparison']={'status':'pending_matched_stationarity','dense_raw_delta_S':None}
    dispatch(state,'rtk-autonomous-dense-rtk-axis.yml','rtk_axis',reason,changes,'scale_ladder_recenter_and_dispatch_axis')

def ensure_ray(state,source,changes):
    rtk=state['rtk'];tol=float(state['objective']['recenter_tolerance_S'])
    cfg={
      'half':('half_negative_eigenray_run','half_negative_eigenray_result','half_negative_eigenray_certification',HALF_RAY_WF,HALF_RAY_ART,0.5),
      'quarter':('quarter_negative_eigenray_run','quarter_negative_eigenray_result','quarter_negative_eigenray_certification',QUARTER_RAY_WF,QUARTER_RAY_ART,0.25),
      'eighth':('eighth_negative_eigenray_run','eighth_negative_eigenray_result','eighth_negative_eigenray_certification',EIGHTH_RAY_WF,EIGHTH_RAY_ART,0.125),
    }
    slotk,resk,certk,wf,art,scale=cfg[source];slot=rtk.get(slotk)
    if slot is None:
        rtk[slotk]={'run_id':None,'workflow':wf,'artifact':art,'status':'requested','expected_source_stencil_scale':scale,'expected_eigenray_source':source}
        dispatch(state,wf,f'rtk_{source}_negative_eigenray',f'Stage4D3 scale ladder requires exact {source}-scale negative-eigenray falsification',changes,f'dispatch_{source}_negative_eigenray')
        rtk['certification']=f'pending_{source}_negative_eigenray';rtk['interior_minimum_certification']=f'N5_PENDING_{source.upper()}_NEGATIVE_EIGENRAY';state['stage']=f'rtk_{source}_negative_eigenray_running';return 'pending'
    became=refresh_slot(slot,changes,f'{source}_negative_eigenray')
    if became:return 'pending'
    if slot.get('status')=='completed' and slot.get('conclusion') not in (None,'success'):
        rtk['certification']=f'{source}_negative_eigenray_compute_failure';rtk['interior_minimum_certification']=f'N5_BLOCKED_BY_{source.upper()}_NEGATIVE_EIGENRAY_FAILURE';state['stage']=f'rtk_{source}_negative_eigenray_compute_failure';return 'failed'
    if slot.get('status')=='completed' and slot.get('conclusion')=='success' and not slot.get('parsed'):
        s=download_summary(slot['run_id'],art)
        if s is None:raise RuntimeError(f'completed {source} ray has no summary')
        validate_common(state,s,source=source);rtk[resk]=s;slot['parsed']=True;imp=float(s.get('best_improvement',1e99));changes.append(f'parse_{source}_negative_eigenray_improvement_{imp:.12g}')
        if imp>tol:
            recenter(state,s,f'{source}-scale exact negative-eigenray improvement {imp:.12g} > {tol}',changes);return 'recentered'
        rtk[certk]=f'exact_{source}_negative_eigenrays_recenter_clear';changes.append(f'{source}_negative_eigenray_clear');return 'clear'
    if slot.get('parsed') and isinstance(rtk.get(resk),dict) and float(rtk[resk].get('best_improvement',1e99))<=tol:return 'clear'
    return 'pending'

def ensure_hessian(state,which,changes):
    rtk=state['rtk'];tol=float(state['objective']['recenter_tolerance_S'])
    cfg={
      'quarter':('quarter_hessian_run','quarter_hessian_result',QUARTER_WF,QUARTER_ART,0.25),
      'eighth':('eighth_hessian_run','eighth_hessian_result',EIGHTH_WF,EIGHTH_ART,0.125),
    }
    slotk,resk,wf,art,scale=cfg[which];slot=rtk.get(slotk)
    if slot is None:
        rtk[slotk]={'run_id':None,'workflow':wf,'artifact':art,'status':'requested','expected_stencil_scale':scale}
        dispatch(state,wf,f'rtk_{which}_hessian',f'Pre-registered Stage4D3 adjacent-scale ladder requires {which} Hessian',changes,f'dispatch_{which}_stencil_ladder')
        rtk['certification']=f'pending_{which}_stencil';rtk['interior_minimum_certification']=f'N5_LADDER_PENDING_{which.upper()}';state['stage']=f'rtk_{which}_stencil_running';return None,'pending'
    became=refresh_slot(slot,changes,f'{which}_hessian')
    if became:return None,'pending'
    if slot.get('status')=='completed' and slot.get('conclusion') not in (None,'success'):
        rtk['certification']=f'{which}_stencil_compute_failure';rtk['interior_minimum_certification']=f'N5_BLOCKED_BY_{which.upper()}_COMPUTE_FAILURE';state['stage']=f'rtk_{which}_stencil_compute_failure';return None,'failed'
    if slot.get('status')=='completed' and slot.get('conclusion')=='success' and not slot.get('parsed'):
        s=download_summary(slot['run_id'],art)
        if s is None:raise RuntimeError(f'completed {which} Hessian has no summary')
        validate_common(state,s,scale=scale);rtk[resk]=s;slot['parsed']=True;e=s.get('eff') or {};imp=float(e.get('best_improvement',1e99));changes.append(f'parse_{which}_stencil_improvement_{imp:.12g}')
        if imp>tol:
            recenter(state,{'best_params':e.get('best_params')},f'{which}-stencil exact improvement {imp:.12g} > {tol}',changes);return s,'recentered'
        return s,'ready'
    if slot.get('parsed') and isinstance(rtk.get(resk),dict):return rtk[resk],'ready'
    return None,'pending'

def comparison(state,tol):
    if state.get('lcdm',{}).get('certification')!='local_dense_accepted':return
    sr=state['rtk'].get('accepted_score_eff');sl=state['lcdm'].get('accepted_score_eff')
    if sr is None or sl is None:return
    sr=float(sr);sl=float(sl);state['comparison']={'status':'matched_local_dense_raw_fit_ready','mapping':'eff','S_RTK':sr,'S_LCDM':sl,'dense_raw_delta_S':sr-sl,'numerically_indistinguishable_at_0p005':abs(sr-sl)<=tol,'interior_minimum_certified':True,'warning':'Raw local objective comparison only; Stage4D3 adjacent-scale ladder passed. Not global/AIC/BIC/Bayes/significance.'}

def main():
    state=json.loads(STATE.read_text());changes=[];rtk=state.get('rtk',{});tol=float(state['objective']['recenter_tolerance_S'])
    base=rtk.get('hessian_result');half=rtk.get('half_hessian_result');hslot=rtk.get('half_hessian_run')
    if not (isinstance(base,dict) and isinstance(half,dict) and isinstance(hslot,dict) and hslot.get('parsed')):
        print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes));return
    be=base.get('eff') or {};he=half.get('eff') or {}
    if float(be.get('best_improvement',1e99))>tol or float(he.get('best_improvement',1e99))>tol:
        print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes));return
    if not (bool(be.get('positive_definite')) and not bool(he.get('positive_definite'))):
        print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes));return

    rs=ensure_ray(state,'half',changes)
    if rs!='clear':
        state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None};STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes,sort_keys=True));return

    quarter,qs=ensure_hessian(state,'quarter',changes)
    if qs!='ready':
        if qs!='recentered':state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None}
        STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes,sort_keys=True));return
    qe=quarter['eff'];qpd=bool(qe.get('positive_definite'))
    if not qpd:
        rs=ensure_ray(state,'quarter',changes)
        if rs!='clear':
            state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None};STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes,sort_keys=True));return

    eighth,es=ensure_hessian(state,'eighth',changes)
    if es!='ready':
        if es!='recentered':state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None}
        STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes,sort_keys=True));return
    ee=eighth['eff'];epd=bool(ee.get('positive_definite'))
    if not epd:
        rs=ensure_ray(state,'eighth',changes)
        if rs!='clear':
            state['comparison']={'status':'pending_multiscale_stationarity','dense_raw_delta_S':None};STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes,sort_keys=True));return

    candidates=[base,half,quarter,eighth];best=min((float(s['eff']['best_exact_S']),s['eff'].get('best_params')) for s in candidates)
    rtk['accepted_score_eff']=best[0]
    if isinstance(best[1],dict):rtk['accepted_score_params']=dict(best[1])
    rtk['accepted_score_semantics']='best_exact_across_base_half_quarter_eighth_within_recenter_tolerance'
    rtk['multiscale_curvature']={'base_positive_definite':True,'half_positive_definite':False,'quarter_positive_definite':qpd,'eighth_positive_definite':epd,
      'base_min_eigenvalue':min(be['eigenvalues_y']),'half_min_eigenvalue':min(he['eigenvalues_y']),'quarter_min_eigenvalue':min(qe['eigenvalues_y']),'eighth_min_eigenvalue':min(ee['eigenvalues_y']),
      'half_negative_eigenray_gate':rtk.get('half_negative_eigenray_certification'),'quarter_negative_eigenray_gate':rtk.get('quarter_negative_eigenray_certification'),'eighth_negative_eigenray_gate':rtk.get('eighth_negative_eigenray_certification')}
    if qpd and epd:
        rtk['certification']='local_dense_accepted';rtk['interior_minimum_certification']='N5_ADAPTIVE_QUARTER_AND_EIGHTH_PASS';rtk['accepted_proof_stencil_scale']=0.25;rtk['proof_validation_stencil_scale']=0.125;state['stage']='matched_dense_ready';comparison(state,tol);changes.append('Stage4D3_N5_quarter_eighth_pass')
    else:
        # At this point every non-PD scale encountered by this branch has an
        # exact same-scale ray that is recenter-clear, including 1/8 if non-PD.
        rtk['certification']='matched_raw_candidate_only_curvature_unresolved';rtk['interior_minimum_certification']='N5_SCALE_LADDER_EXHAUSTED_CURVATURE_UNRESOLVED';state['stage']='rtk_curvature_unresolved';state['comparison']={'status':'matched_dense_raw_candidate_ready_curvature_unresolved','dense_raw_delta_S':None,'interior_minimum_certified':False};changes.append('scale_ladder_exhausted_after_all_nonpd_rays_clear')
    STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n');print('RTK_STAGE4D3_SCALE_LADDER_GATE',json.dumps(changes,sort_keys=True))

if __name__=='__main__':main()
