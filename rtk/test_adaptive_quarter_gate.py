#!/usr/bin/env python3
"""Synthetic no-network tests for parsed-half stability and quarter dispatch."""
import importlib.util, json, tempfile
from pathlib import Path

MODULE=Path(__file__).with_name('enforce_adaptive_quarter_gate.py')
spec=importlib.util.spec_from_file_location('rtk_adaptive_quarter_gate',MODULE)
G=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(G)
CENTER={'lam':2.2e5,'h':0.69,'Ob':0.047,'Om':0.253,'As':2.08e-9,'ns':0.964,'zre':7.3}
LCDM={'certification':'local_dense_accepted','accepted_score_eff':1049.9}

def summary(pd,scale,S=1050.3):
    return {'objective':'matched-ultra-linstep2+dense-BOSS','center':dict(CENTER),'stencil_scale':scale,
      'eff':{'S_center':S,'best_exact_S':S,'best_improvement':0.0,'best_params':dict(CENTER),'positive_definite':pd,'eigenvalues_y':([0.01,0.02] if pd else [-0.01,0.02]),'hessian_y':[[1,0],[0,1]]}}
def base_state(base_pd,half_pd):
    b=summary(base_pd,1.0);h=summary(half_pd,0.5)
    return {'objective':{'name':'matched-ultra-linstep2+dense-BOSS','recenter_tolerance_S':0.005},'lcdm':dict(LCDM),'comparison':{'dense_raw_delta_S':None},'rtk':{
      'accepted_center':dict(CENTER),'hessian_result':b,'hessian_run':{'run_id':1,'parsed':True},
      'half_hessian_result':h,'half_hessian_run':{'run_id':2,'parsed':True,'status':'completed','conclusion':'success'},
      'negative_eigenray_certification':('exact_negative_eigenrays_recenter_clear' if not base_pd else None)}}

def run_case(s):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'state.json';p.write_text(json.dumps(s))
        old_state,old_dispatch,old_fn,old_get=G.STATE,G.DISPATCH,G.dispatch,G.get_run
        G.STATE=p;G.DISPATCH=Path(td)/'dispatch.json'
        G.dispatch=lambda st,wf,target,reason,changes,label:changes.append(label)
        # Synthetic tests must never reach GitHub.  A pre-existing run id is
        # represented as a completed successful run; parsed/unparsed semantics
        # are tested by the state fields themselves.
        G.get_run=lambda run_id:{'id':int(run_id),'status':'completed','conclusion':'success','html_url':f'https://example.invalid/runs/{int(run_id)}'}
        try:G.main()
        finally:G.STATE,G.DISPATCH,G.dispatch,G.get_run=old_state,old_dispatch,old_fn,old_get
        return json.loads(p.read_text())

# Parsed ordinary base+half PD result must remain accepted on later iterations.
s=run_case(base_state(True,True))
assert s['rtk']['certification']=='local_dense_accepted'
assert s['rtk']['interior_minimum_certification']=='N5_BASE_AND_HALF_STENCIL_PASS'
assert s['stage']=='matched_dense_ready'
assert s['comparison']['interior_minimum_certified'] is True

# Pre-registered adaptive case must request quarter rather than accept half alone.
s=run_case(base_state(False,True))
assert s['rtk']['quarter_hessian_run']['status']=='requested'
assert s['rtk']['quarter_hessian_run']['expected_stencil_scale']==0.25
assert s['rtk']['certification']=='pending_quarter_stencil'
assert s['rtk']['interior_minimum_certification']=='N5_ADAPTIVE_PENDING_QUARTER'
assert s['stage']=='rtk_quarter_stencil_running'
assert s['comparison']['dense_raw_delta_S'] is None

# Once an adaptive half+quarter proof has already been parsed, every later cron
# pass must reconstruct the interior-certified comparison.  This protects the
# final clean-room replay gate from an ordering regression where the generic
# orchestrator/multiscale stages temporarily rewrite comparison first.
s=base_state(False,True)
s['rtk']['quarter_hessian_run']={'run_id':3,'parsed':True,'status':'completed','conclusion':'success','expected_stencil_scale':0.25}
s['rtk']['quarter_hessian_result']=summary(True,0.25,S=1050.29)
s['rtk']['certification']='matched_raw_candidate_only_curvature_unresolved'
s['rtk']['interior_minimum_certification']='N5_CURVATURE_UNRESOLVED'
s['comparison']={'status':'matched_dense_raw_candidate_ready_curvature_unresolved','dense_raw_delta_S':None,'interior_minimum_certified':False}
s=run_case(s)
assert s['rtk']['certification']=='local_dense_accepted'
assert s['rtk']['interior_minimum_certification']=='N5_ADAPTIVE_HALF_AND_QUARTER_PASS'
assert s['stage']=='matched_dense_ready'
assert s['comparison']['status']=='matched_local_dense_raw_fit_ready'
assert s['comparison']['interior_minimum_certified'] is True
assert abs(float(s['rtk']['accepted_score_eff'])-1050.29)<1e-12

print('RTK_ADAPTIVE_QUARTER_GATE_UNIT_PASS')
