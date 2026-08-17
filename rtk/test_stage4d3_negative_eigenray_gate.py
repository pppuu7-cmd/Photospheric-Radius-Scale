#!/usr/bin/env python3
"""Unit-level regression for the Stage4D3 negative-eigenray control logic.

No likelihood or GitHub API calls are made. External effects are monkeypatched.
"""
import copy
import importlib.util
from pathlib import Path

MODULE=Path(__file__).with_name('enforce_stage4d3_multiscale_gate.py')
spec=importlib.util.spec_from_file_location('rtk_stage4d3_gate',MODULE)
G=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(G)

CENTER={'lam':2.2e5,'h':0.69,'Ob':0.047,'Om':0.253,'As':2.08e-9,'ns':0.964,'zre':7.3}
BASE={'objective':'matched-ultra-linstep2+dense-BOSS','center':dict(CENTER),'eff':{'S_center':1050.3,'best_exact_S':1050.3,'best_improvement':0.0,'best_params':dict(CENTER),'positive_definite':False,'eigenvalues_y':[-0.004,0.02]}}

def state():
    return {'iteration':1,'updated_at':'x','objective':{'name':'matched-ultra-linstep2+dense-BOSS','recenter_tolerance_S':0.005},'production_mapping':'eff','comparison':{'dense_raw_delta_S':None},'rtk':{'accepted_center':dict(CENTER),'hessian_result':copy.deepcopy(BASE),'hessian_run':{'run_id':10,'parsed':True}}}

s=state();changes=[];called=[]
old_req=G.request_negative_ray
G.request_negative_ray=lambda st,ch:(called.append('ray'),st['rtk'].__setitem__('negative_eigenray_run',{'run_id':None,'workflow':G.RAY_WF,'artifact':G.RAY_ART,'status':'requested'}))
try:
    status=G.process_negative_ray(s,s['rtk']['hessian_result'],s['rtk']['hessian_result']['eff'],0.005,changes)
finally:
    G.request_negative_ray=old_req
assert status=='pending' and called==['ray']
assert s['rtk'].get('half_hessian_run') is None
assert s['stage']=='rtk_negative_eigenray_running'

s=state();s['rtk']['negative_eigenray_run']={'run_id':20,'workflow':G.RAY_WF,'artifact':G.RAY_ART,'status':'completed','conclusion':'success'};changes=[]
clear_summary={'objective':s['objective']['name'],'center':dict(CENTER),'best_improvement':0.001,'best_exact_S':1050.299,'best_params':dict(CENTER)}
old_get,old_down=G.get_run,G.download_summary
G.get_run=lambda rid:{'status':'completed','conclusion':'success','html_url':'u'}
G.download_summary=lambda rid,art:copy.deepcopy(clear_summary)
try:
    status=G.process_negative_ray(s,s['rtk']['hessian_result'],s['rtk']['hessian_result']['eff'],0.005,changes)
finally:
    G.get_run,G.download_summary=old_get,old_down
assert status=='clear'
assert s['rtk']['negative_eigenray_run']['parsed'] is True
assert s['rtk']['negative_eigenray_certification']=='exact_negative_eigenrays_recenter_clear'

NEW=dict(CENTER);NEW['h']=0.691
s=state();s['rtk']['negative_eigenray_run']={'run_id':21,'workflow':G.RAY_WF,'artifact':G.RAY_ART,'status':'completed','conclusion':'success'};changes=[]
down_summary={'objective':s['objective']['name'],'center':dict(CENTER),'best_improvement':0.02,'best_exact_S':1050.28,'best_params':dict(NEW)}
old_get,old_down,old_write=G.get_run,G.download_summary,G.write_dispatch
G.get_run=lambda rid:{'status':'completed','conclusion':'success','html_url':'u'}
G.download_summary=lambda rid,art:copy.deepcopy(down_summary)
G.write_dispatch=lambda st,wf,target,reason,ch,label:ch.append(label)
try:
    status=G.process_negative_ray(s,s['rtk']['hessian_result'],s['rtk']['hessian_result']['eff'],0.005,changes)
finally:
    G.get_run,G.download_summary,G.write_dispatch=old_get,old_down,old_write
assert status=='recentered'
assert s['rtk']['accepted_center']==NEW
assert s['rtk']['hessian_result'] is None and s['rtk']['hessian_run'] is None
assert s['rtk']['axis_run']['status']=='requested'
assert s['stage']=='rtk_axis_recenter_running'
assert s['comparison']['dense_raw_delta_S'] is None
assert 'recenter_from_negative_eigenray_and_dispatch_axis' in changes

print('RTK_STAGE4D3_NEGATIVE_EIGENRAY_UNIT_PASS')
