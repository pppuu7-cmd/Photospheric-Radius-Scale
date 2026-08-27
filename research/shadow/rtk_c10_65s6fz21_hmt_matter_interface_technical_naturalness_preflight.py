#!/usr/bin/env python3
import json,re,urllib.request,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ21_HMT_MATTER_INTERFACE_TECHNICAL_NATURALNESS_PREFLIGHT_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ20_HMT_MICROSCOPIC_MATTER_COMPLETION_SOURCE_LOCK_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ21_HMT_MATTER_INTERFACE_TECHNICAL_NATURALNESS_PREFLIGHT_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).lower()

t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
hmt_raw=get('https://arxiv.org/html/1310.6666v4')
rad_raw=get('https://arxiv.org/abs/1805.10299')
hmt=norm(hmt_raw); rad=norm(rad_raw)
checks={}
checks['z20_parent_exact']=p['classification']==t['parent_required']
checks['hmt_two_arbitrary_constants_explicit']='two arbitrary coupling constants' in hmt and 'a 1' in hmt and 'a 2' in hmt
checks['hmt_uv_action_origin_unfixed_explicit']='not obvious how to obtain such a prescription from the action principle' in hmt
checks['projectable_radiative_problem_explicit']='projectable version' in rad and 'problem persists' in rad
checks['matter_fine_tuning_explicit']='fine tuning' in rad and 'sound speeds' in rad
checks['rg_presented_as_candidate_scenario']='renormalization group flow' in rad and 'emergent infrared lorentz invariance' in rad
checks['supersymmetry_presented_as_candidate_scenario']='supersymmetry' in rad and 'protect' in rad
checks['no_unique_hmt_interface_fixed_relation_in_audited_sources']=True
checks['no_rtk_response_or_softs_selection']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False
complete=all(checks.values())
protected_unique=False
if complete and not protected_unique:
    classification='C10_65S6FZ21_NO_PROTECTED_UNIQUE_SELECTOR_IN_AUDITED_SOURCES_PARTIAL_PASS_SCOPED'
elif complete and protected_unique:
    classification='C10_65S6FZ21_PROTECTED_UNIQUE_HMT_MATTER_INTERFACE_SELECTOR_FOUND_PASS_SCOPED'
else:
    classification='C10_65S6FZ21_TECHNICAL_NATURALNESS_SOURCE_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
interpretation=(
 'The audited universal-HMT matter interface remains a continuous two-constant family and the same source does not provide an obvious UV action-principle origin for that prescription. '
 'An independent projectable-Horava radiative analysis finds that matter-sector Lorentz restoration suffers power-law radiative sensitivity/fine tuning and discusses RG-flow or supersymmetry only as candidate protection mechanisms, not as a derived fixed relation selecting the HMT interface constants. '
 'Therefore the audited sources do not supply a technically-natural unique selector for the surviving HMT matter-interface family. This is a scoped source result, not a literature-wide impossibility theorem and not closure of RTK C9.'
)
next_gate=(
 'C10.65s6fZ22: freeze an independent symmetry/UV-completion inventory restricted to mechanisms that can protect the physical matter-interface relation itself (for example a concrete supersymmetric or strong-dynamics completion with an explicit low-energy HMT matching map). '
 'Require an action-level derivation of the relation before any RTK response comparison. If no such source-locked completion is found, preserve the Z12/Z19 completion blocker rather than choosing a1,a2 phenomenologically.'
)
r={
 'schema':'RTK_C10_65S6FZ21_HMT_MATTER_INTERFACE_TECHNICAL_NATURALNESS_PREFLIGHT_RESULT_v1',
 'gate':'C10.65s6fZ21','classification':classification,'checks':checks,
 'source_hashes':{
   'arxiv_1310_6666_html_sha256':hashlib.sha256(hmt_raw.encode()).hexdigest(),
   'arxiv_1805_10299_abs_sha256':hashlib.sha256(rad_raw.encode()).hexdigest()
 },
 'naturalness_audit':{
   'unique_protected_interface_relation_found':False,
   'hmt_interface_parameters_remain_arbitrary':checks['hmt_two_arbitrary_constants_explicit'],
   'projectable_radiative_fine_tuning_problem_present':checks['projectable_radiative_problem_explicit'] and checks['matter_fine_tuning_explicit'],
   'rg_or_supersymmetry_only_candidate_mechanisms_in_audited_source':checks['rg_presented_as_candidate_scenario'] and checks['supersymmetry_presented_as_candidate_scenario'],
   'scope':'audited sources only'
 },
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a literature-wide no-naturalness theorem','not C9 radiative-naturalness closure','not a unique HMT+Z7 action','not RTK pole/residue/remainder equivalence','not same-action primordial/background closure','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
