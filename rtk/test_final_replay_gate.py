#!/usr/bin/env python3
from __future__ import annotations

import copy
import json

import enforce_final_replay_gate as G


def params(lam):
    return {'lam':lam,'h':0.69,'Ob':0.047,'Om':0.25,'As':2.08e-9,'ns':0.965,'zre':7.3}


def state():
    obj={'name':'matched-ultra-linstep2+dense-BOSS','dense_z_pk':'0.,1.','recenter_tolerance_S':0.005,'ultra':{'l_linstep':'2'}}
    r=params(2.2e5);l=params(0.0)
    return {
        'iteration':100,'updated_at':'2026-08-18T13:00:00Z','objective':obj,'production_mapping':'eff',
        'rtk':{'certification':'local_dense_accepted','interior_minimum_certification':'N5_BASE_AND_HALF_STENCIL_PASS','accepted_score_params':r,'accepted_score_eff':1050.25},
        'lcdm':{'certification':'local_dense_accepted','accepted_score_params':l,'accepted_score_eff':1049.97},
        'comparison':{'status':'matched_local_dense_raw_fit_ready','interior_minimum_certified':True,'dense_raw_delta_S':0.28},
    }


def lock():
    return {
        'external_git':{
            'class_public':{'commit':'36cf283628c4a3330ec9fd3d84239bf775f77317'},
            'pantheon':{'commit':'7eb29dc87ba223b4ec8457cd3cccba1216c36fb7'},
        },
        'likelihood':{'planck_baseline_sha256':'0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6'},
        'python_packages':{'numpy':'2.5.2','scipy':'1.18.0'},
    }


def summary(s):
    r=s['rtk'];l=s['lcdm'];delta=float(r['accepted_score_eff'])-float(l['accepted_score_eff'])
    return {
        'status':'PASS','classification':G.CLASSIFICATION,'objective':copy.deepcopy(s['objective']),'production_mapping':'eff',
        'rtk_interior_minimum_certification':r['interior_minimum_certification'],'score_tolerance_abs':G.TOL,
        'provenance':{
            'research_source_commit':'f'*40,
            'class_upstream_commit':'36cf283628c4a3330ec9fd3d84239bf775f77317',
            'class_upstream_sha_expected':'36cf283628c4a3330ec9fd3d84239bf775f77317',
            'pantheon_commit':'7eb29dc87ba223b4ec8457cd3cccba1216c36fb7',
            'pantheon_sha_expected':'7eb29dc87ba223b4ec8457cd3cccba1216c36fb7',
            'planck_sha256_expected':'0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6',
            'numpy_version':'2.5.2','numpy_version_expected':'2.5.2','scipy_version':'1.18.0','scipy_version_expected':'1.18.0',
            'cache_key_version':'clean-room-exact-float-v2',
        },
        'rtk':{'params':copy.deepcopy(r['accepted_score_params']),'expected_score_eff':r['accepted_score_eff'],'replayed_score_eff':r['accepted_score_eff']+1e-7,'score_error_eff':1e-7},
        'lcdm':{'params':copy.deepcopy(l['accepted_score_params']),'expected_score_eff':l['accepted_score_eff'],'replayed_score_eff':l['accepted_score_eff']-1e-7,'score_error_eff':-1e-7},
        'comparison':{'replayed_delta_S_eff':delta+2e-7},
    }


def main():
    s=state();lk=lock();sm=summary(s)
    assert G.ready(s)
    assert G.validate_summary(sm,s,lk,check_git=False)==[]

    # Fingerprint is deterministic and changes when either accepted minimum changes.
    f1=G.target_fingerprint(s);f2=G.target_fingerprint(copy.deepcopy(s));assert f1==f2 and len(f1)==64
    moved=copy.deepcopy(s);moved['rtk']['accepted_score_params']['h']+=1e-6
    assert G.target_fingerprint(moved)!=f1

    # No N5 => no replay dispatch eligibility.
    bad=copy.deepcopy(s);bad['rtk']['interior_minimum_certification']='N5_PENDING_HALF_STENCIL';assert not G.ready(bad)
    bad=copy.deepcopy(s);bad['comparison']['interior_minimum_certified']=False;assert not G.ready(bad)

    # Parameter, score and provenance mutations fail closed.
    badsm=copy.deepcopy(sm);badsm['rtk']['params']['h']+=1e-6
    assert 'rtk_params_mismatch' in G.validate_summary(badsm,s,lk,check_git=False)
    badsm=copy.deepcopy(sm);badsm['rtk']['score_error_eff']=3e-6
    assert 'rtk_replay_error' in G.validate_summary(badsm,s,lk,check_git=False)
    badsm=copy.deepcopy(sm);badsm['provenance']['numpy_version']='9.9.9'
    assert 'numpy_provenance_mismatch' in G.validate_summary(badsm,s,lk,check_git=False)
    badsm=copy.deepcopy(sm);badsm['status']='FAIL'
    assert 'status_not_PASS' in G.validate_summary(badsm,s,lk,check_git=False)

    # Internal delta must equal the two replayed scores, independent of state rounding.
    badsm=copy.deepcopy(sm);badsm['comparison']['replayed_delta_S_eff']+=1e-4
    assert 'delta_internal_inconsistency' in G.validate_summary(badsm,s,lk,check_git=False)

    print('RTK_FINAL_REPLAY_GATE_UNIT_PASS',json.dumps({'fingerprint':f1,'checks':'ready+identity+score+provenance'}))


if __name__=='__main__':main()
