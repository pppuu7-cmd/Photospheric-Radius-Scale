#!/usr/bin/env python3
"""Synthetic no-network regression tests for the generalized Stage-4D3 ladder.

The terminal 1/8 case is the key invariant: a non-PD eighth Hessian may never be
classified as exhausted curvature until an exact eighth-scale negative-eigenray
has been completed and found recenter-clear.
"""
import importlib.util, json, tempfile
from pathlib import Path

MODULE=Path(__file__).with_name('enforce_stage4d3_scale_ladder_gate.py')
spec=importlib.util.spec_from_file_location('rtk_stage4d3_scale_ladder_gate',MODULE)
G=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(G)

CENTER={'lam':2.2e5,'h':0.69,'Ob':0.047,'Om':0.253,'As':2.08e-9,'ns':0.964,'zre':7.3}
NEW_CENTER={'lam':2.21e5,'h':0.6902,'Ob':0.0469,'Om':0.2528,'As':2.081e-9,'ns':0.9642,'zre':7.31}
OBJ='matched-ultra-linstep2+dense-BOSS'

def hessian(pd,scale,S):
    return {'objective':OBJ,'center':dict(CENTER),'stencil_scale':scale,
      'eff':{'S_center':S,'best_exact_S':S,'best_improvement':0.0,'best_params':dict(CENTER),
             'positive_definite':pd,'eigenvalues_y':([0.01,0.02] if pd else [-0.01,0.02]),
             'hessian_y':[[1.0,0.0],[0.0,1.0]]}}

def ray(source,scale,improvement=0.0,params=None):
    return {'objective':OBJ,'center':dict(CENTER),'eigenray_source':source,'source_stencil_scale':scale,
            'best_improvement':float(improvement),'best_exact_S':1050.0-float(improvement),
            'best_params':dict(params or CENTER)}

def base_state(quarter_pd=True,eighth_pd=False):
    b=hessian(True,1.0,1050.30);h=hessian(False,0.5,1050.30);q=hessian(quarter_pd,0.25,1050.29);e=hessian(eighth_pd,0.125,1050.28)
    return {
      'iteration':1,'updated_at':'synthetic','production_mapping':'eff',
      'objective':{'name':OBJ,'recenter_tolerance_S':0.005},
      'comparison':{'status':'pending_multiscale_stationarity','dense_raw_delta_S':None},
      'lcdm':{'certification':'local_dense_accepted','accepted_score_eff':1049.9},
      'rtk':{
        'accepted_center':dict(CENTER),'accepted_score_eff':None,'accepted_score_params':None,
        'hessian_result':b,'hessian_run':{'run_id':1,'parsed':True,'status':'completed','conclusion':'success'},
        'half_hessian_result':h,'half_hessian_run':{'run_id':2,'parsed':True,'status':'completed','conclusion':'success'},
        'half_negative_eigenray_result':ray('half',0.5,0.0),
        'half_negative_eigenray_run':{'run_id':3,'parsed':True,'status':'completed','conclusion':'success'},
        'half_negative_eigenray_certification':'exact_half_negative_eigenrays_recenter_clear',
        'quarter_hessian_result':q,'quarter_hessian_run':{'run_id':4,'parsed':True,'status':'completed','conclusion':'success','expected_stencil_scale':0.25},
        'eighth_hessian_result':e,'eighth_hessian_run':{'run_id':5,'parsed':True,'status':'completed','conclusion':'success','expected_stencil_scale':0.125},
      }}

def run_case(state,download=None):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'state.json';p.write_text(json.dumps(state))
        old=(G.STATE,G.DISPATCH,G.get_run,G.latest,G.download_summary,G.dispatch)
        calls=[]
        G.STATE=p;G.DISPATCH=Path(td)/'dispatch.json'
        G.get_run=lambda run_id:{'id':int(run_id),'status':'completed','conclusion':'success','html_url':f'https://example.invalid/runs/{int(run_id)}'}
        G.latest=lambda workflow:None
        if download is not None:G.download_summary=download
        def fake_dispatch(st,wf,target,reason,changes,label):
            calls.append((wf,target,label));changes.append(label)
        G.dispatch=fake_dispatch
        try:G.main()
        finally:G.STATE,G.DISPATCH,G.get_run,G.latest,G.download_summary,G.dispatch=old
        return json.loads(p.read_text()),calls

# 1) Terminal non-PD 1/8 must request an exact 1/8 ray. It must NOT exhaust yet.
s,calls=run_case(base_state(quarter_pd=True,eighth_pd=False))
slot=s['rtk']['eighth_negative_eigenray_run']
assert slot['status']=='requested'
assert slot['expected_eigenray_source']=='eighth'
assert abs(float(slot['expected_source_stencil_scale'])-0.125)<1e-15
assert s['rtk']['interior_minimum_certification']=='N5_PENDING_EIGHTH_NEGATIVE_EIGENRAY'
assert s['stage']=='rtk_eighth_negative_eigenray_running'
assert s['comparison']['dense_raw_delta_S'] is None
assert all('exhausted' not in str(v).lower() for v in s['rtk'].values())
assert any(wf==G.EIGHTH_RAY_WF for wf,_,_ in calls)

# 2) A parsed, recenter-clear terminal ray authorizes fail-closed exhaustion when
# quarter is PD but eighth remains non-PD: there is no adjacent PD pair.
s0=base_state(quarter_pd=True,eighth_pd=False)
s0['rtk']['eighth_negative_eigenray_result']=ray('eighth',0.125,0.0)
s0['rtk']['eighth_negative_eigenray_run']={'run_id':6,'parsed':True,'status':'completed','conclusion':'success','expected_source_stencil_scale':0.125,'expected_eigenray_source':'eighth'}
s0['rtk']['eighth_negative_eigenray_certification']='exact_eighth_negative_eigenrays_recenter_clear'
s,_=run_case(s0)
assert s['rtk']['interior_minimum_certification']=='N5_SCALE_LADDER_EXHAUSTED_CURVATURE_UNRESOLVED'
assert s['rtk']['certification']=='matched_raw_candidate_only_curvature_unresolved'
assert s['stage']=='rtk_curvature_unresolved'
assert s['comparison']['interior_minimum_certified'] is False
assert s['rtk']['multiscale_curvature']['eighth_negative_eigenray_gate']=='exact_eighth_negative_eigenrays_recenter_clear'

# 3) A newly parsed terminal ray with > tolerance downhill must recenter/restart,
# never reach exhaustion. This exercises the parse-time transition itself.
s0=base_state(quarter_pd=True,eighth_pd=False)
s0['rtk']['eighth_negative_eigenray_run']={'run_id':7,'parsed':False,'status':'completed','conclusion':'success','expected_source_stencil_scale':0.125,'expected_eigenray_source':'eighth'}
def dl(run_id,artifact):
    assert int(run_id)==7 and artifact==G.EIGHTH_RAY_ART
    return ray('eighth',0.125,0.010,NEW_CENTER)
s,_=run_case(s0,download=dl)
assert s['rtk']['accepted_center']==NEW_CENTER
assert s['rtk']['interior_minimum_certification']=='N5_RESTART_AFTER_SCALE_LADDER_DOWNHILL'
assert s['rtk']['certification']=='needs_recenter_from_scale_ladder'
assert s['stage']=='rtk_axis_recenter_running'
assert s['comparison']['dense_raw_delta_S'] is None
assert s['rtk']['eighth_hessian_result'] is None
assert s['rtk']['eighth_negative_eigenray_run'] is None

# 4) Adjacent quarter+eighth PD stencils close N5 without any eighth ray.
s0=base_state(quarter_pd=True,eighth_pd=True)
s,_=run_case(s0)
assert s['rtk']['certification']=='local_dense_accepted'
assert s['rtk']['interior_minimum_certification']=='N5_ADAPTIVE_QUARTER_AND_EIGHTH_PASS'
assert s['stage']=='matched_dense_ready'
assert s['comparison']['interior_minimum_certified'] is True
assert abs(float(s['rtk']['accepted_proof_stencil_scale'])-0.25)<1e-15
assert abs(float(s['rtk']['proof_validation_stencil_scale'])-0.125)<1e-15
assert 'eighth_negative_eigenray_run' not in s['rtk']

# 5) If quarter is non-PD, its ray must be clear before the eighth branch is even
# considered. A pre-parsed clear quarter ray allows progression to terminal logic.
s0=base_state(quarter_pd=False,eighth_pd=False)
s0['rtk']['quarter_negative_eigenray_result']=ray('quarter',0.25,0.0)
s0['rtk']['quarter_negative_eigenray_run']={'run_id':8,'parsed':True,'status':'completed','conclusion':'success','expected_source_stencil_scale':0.25,'expected_eigenray_source':'quarter'}
s0['rtk']['quarter_negative_eigenray_certification']='exact_quarter_negative_eigenrays_recenter_clear'
s,calls=run_case(s0)
assert s['rtk']['eighth_negative_eigenray_run']['expected_eigenray_source']=='eighth'
assert any(wf==G.EIGHTH_RAY_WF for wf,_,_ in calls)
assert s['comparison']['dense_raw_delta_S'] is None

print('RTK_STAGE4D3_SCALE_LADDER_GATE_UNIT_PASS')
