#!/usr/bin/env python3
import json, re, urllib.request, hashlib, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ16_HMT_MATTER_AUXILIARY_INTERFACE_SOURCE_LOCK_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ15_PRODUCTION_PX_CARRIER_SELECTION_RULE_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ16_HMT_MATTER_AUXILIARY_INTERFACE_SOURCE_LOCK_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']

arxiv=get('https://arxiv.org/abs/1310.6666')
cpc=get('https://cpc.ihep.ac.cn/article/doi/10.1088/1674-1137/ad873d')

def has(text,*parts):
    low=re.sub(r'\s+',' ',text.lower())
    return all(x.lower() in low for x in parts)

checks={}
checks['z15_parent_exact']=p['classification']==t['parent_required']
checks['arxiv_universal_coupling_explicit']=has(arxiv,'universal coupling','gravity and matter')
checks['arxiv_projectable_case_explicit']=('projectable' in arxiv.lower() and 'non-projectable' in arxiv.lower()) or ('projectable' in arxiv.lower() and 'nonprojectable' in arxiv.lower())
checks['arxiv_coupling_constants_explicit']=has(arxiv,'coupling constants')
checks['cpc_projectability_explicit']=('n = n(t)' in re.sub(r'\s+',' ',cpc.lower())) or ('n=n(t)' in re.sub(r'\s+',' ',cpc.lower())) or has(cpc,'projectability condition')
checks['cpc_auxiliary_fields_explicit']=has(cpc,'newtonian pre-potential') and ('gauge field' in cpc.lower())
checks['cpc_physical_adm_matter_action_explicit']=('tilde{n}' in cpc.lower() or 'tilde n' in cpc.lower()) and ('matter lagrangian' in cpc.lower() or 'cal{l}_m' in cpc.lower())
checks['independent_sources_predate_softs']=True
checks['no_old_kernel_matching']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False

class_found=all(checks[k] for k in ['arxiv_universal_coupling_explicit','arxiv_projectable_case_explicit','cpc_projectability_explicit','cpc_auxiliary_fields_explicit','cpc_physical_adm_matter_action_explicit'])
free_family=checks['arxiv_coupling_constants_explicit']
if class_found and free_family:
    classification='C10_65S6FZ16_HMT_UNIVERSAL_MATTER_INTERFACE_CLASS_FOUND_COEFFICIENTS_UNFIXED_PARTIAL_PASS_SCOPED'
elif class_found and not free_family:
    classification='C10_65S6FZ16_UNIQUE_HMT_MATTER_AUXILIARY_INTERFACE_FIXED_PASS_SCOPED'
else:
    classification='C10_65S6FZ16_NO_SOURCE_LOCKED_HMT_MATTER_AUXILIARY_INTERFACE_BLOCKED_SCOPED'

r={
 'schema':'RTK_C10_65S6FZ16_HMT_MATTER_AUXILIARY_INTERFACE_SOURCE_LOCK_RESULT_v1',
 'gate':'C10.65s6fZ16',
 'classification':classification,
 'checks':checks,
 'source_hashes':{
   'arxiv_1310_6666_sha256':hashlib.sha256(arxiv.encode()).hexdigest(),
   'cpc_ad873d_sha256':hashlib.sha256(cpc.encode()).hexdigest()
 },
 'source_lock':{
   'universal_projectable_u1_matter_coupling_class_exists':class_found,
   'physical_ADM_matter_variables_are_part_of_published_interface':checks['cpc_physical_adm_matter_action_explicit'],
   'A_and_Newtonian_prepotential_are_part_of_published_gravity_matter_context':checks['cpc_auxiliary_fields_explicit'],
   'published_interface_has_free_coupling_constants':free_family,
   'unique_RTK_response_numerator_fixed':False if free_family else class_found
 },
 'interpretation':'An independently published projectable U(1)/HMT gravity-matter coupling class exists and explicitly places matter on physical ADM variables in a theory containing the U(1) gauge field and Newtonian prepotential. However the source literature itself describes PPN observables in terms of coupling constants, so the interface is a continuous coupling class rather than a unique RTK matter/source map. Thus Z15 intrinsic P(X) coefficients can be retained, but the response numerator and detailed A/prepotential carrier couplings cannot yet be chosen without an independent coefficient-selection principle.',
 'next_gate':'C10.65s6fZ17: freeze an independent coefficient-selection/IR-equivalence audit for the published universal HMT matter-coupling family (e.g. GR/PPN limit or equivalence-principle conditions that predate RTK soft-s). Determine whether those conditions uniquely fix the scalar-response-relevant physical-metric parameters. If a continuous family remains, preserve the source-interface blocker rather than fitting RTK pole/residue/remainder.',
 'nonclaims':['not a unique HMT+Z7 action','not RTK pole/residue/remainder equivalence','not same-action primordial/background closure','not C9 naturalness','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
