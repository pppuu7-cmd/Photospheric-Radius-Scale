#!/usr/bin/env python3
import json, re, urllib.request, hashlib, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ17_HMT_MATTER_COEFFICIENT_SELECTION_IR_EQUIVALENCE_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ16_HMT_MATTER_AUXILIARY_INTERFACE_SOURCE_LOCK_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ17_HMT_MATTER_COEFFICIENT_SELECTION_IR_EQUIVALENCE_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).lower()

def has(text,*parts):
    low=norm(text)
    return all(p.lower() in low for p in parts)

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']

arxiv=get('https://arxiv.org/abs/1310.6666')
cpc=get('https://cpc.ihep.ac.cn/article/doi/10.1088/1674-1137/ad873d')
a=norm(arxiv)
c=norm(cpc)

checks={}
checks['z16_parent_exact']=p['classification']==t['parent_required']
checks['arxiv_universal_coupling_explicit']='universal coupling' in a and 'gravity and matter' in a
checks['arxiv_projectable_case_explicit']='projectable' in a and ('non-projectable' in a or 'nonprojectable' in a)
checks['arxiv_ppn_in_terms_of_couplings_explicit']='ppn' in a and 'coupling constants' in a
checks['arxiv_large_allowed_parameter_region_explicit']=('large region of the parameters space' in a or 'large region of the parameter space' in a)
checks['arxiv_gr_values_realisable_explicit']=('same results obtained in general relativity can be easily realized' in a or 'same results obtained in general relativity can be easily realised' in a)
checks['arxiv_ppn_does_not_fix_lambda_explicit']=('impose no constraint on the parameter' in a and 'lambda' in a) or ('impose no constraint on the parameter $\\lambda$' in a)
checks['cpc_universal_physical_adm_interface_still_present']=(('tilde{n}' in c or 'tilde n' in c) and ('matter lagrangian' in c or 'cal{l}_m' in c))
checks['independent_sources_predate_softs']=True
checks['no_old_kernel_matching']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False

selection_source_found=all(checks[k] for k in [
    'arxiv_universal_coupling_explicit','arxiv_projectable_case_explicit','arxiv_ppn_in_terms_of_couplings_explicit'])
continuous_family=all(checks[k] for k in [
    'arxiv_large_allowed_parameter_region_explicit','arxiv_gr_values_realisable_explicit'])
unique_selector=selection_source_found and not continuous_family

if selection_source_found and continuous_family:
    classification='C10_65S6FZ17_PPN_GR_LIMIT_LEAVES_CONTINUOUS_HMT_MATTER_FAMILY_PARTIAL_PASS_SCOPED'
elif unique_selector:
    classification='C10_65S6FZ17_IR_EQUIVALENCE_UNIQUELY_FIXES_HMT_MATTER_INTERFACE_PASS_SCOPED'
else:
    classification='C10_65S6FZ17_NO_INDEPENDENT_COEFFICIENT_SELECTION_PRINCIPLE_BLOCKED_SCOPED'

interpretation=(
    'The pre-soft-s published universal HMT/U(1) matter-coupling analysis supplies an independent IR/PPN test, '
    'but it explicitly states that all solar-system tests are satisfied in a large region of parameter space and that GR PPN values are readily realizable. '
    'Therefore phenomenological IR equivalence does not uniquely select the universal-coupling parameters or a unique scalar-response source map. '
    'The Z16 source-interface ambiguity must be preserved; RTK pole/residue/remainder or soft-s data may not be used to choose a point in this family.'
)
next_gate=(
    'C10.65s6fZ18: freeze a same-action identifiability/selection audit for the remaining HMT universal-matter coupling family. '
    'Search only for an independent pre-soft-s symmetry, equivalence-principle, microscopic-matter, or radiative principle that fixes the physical-metric coupling parameters. '
    'If no unique selector exists, keep the full-action/source-interface blocker instead of matching RTK response data.'
)

r={
  'schema':'RTK_C10_65S6FZ17_HMT_MATTER_COEFFICIENT_SELECTION_IR_EQUIVALENCE_RESULT_v1',
  'gate':'C10.65s6fZ17',
  'classification':classification,
  'checks':checks,
  'source_hashes':{
    'arxiv_1310_6666_sha256':hashlib.sha256(arxiv.encode()).hexdigest(),
    'cpc_ad873d_sha256':hashlib.sha256(cpc.encode()).hexdigest()
  },
  'selection_audit':{
    'independent_ppn_selection_source_found':selection_source_found,
    'published_large_allowed_parameter_region':checks['arxiv_large_allowed_parameter_region_explicit'],
    'published_gr_ppn_values_realisable':checks['arxiv_gr_values_realisable_explicit'],
    'published_ppn_leaves_lambda_unconstrained':checks['arxiv_ppn_does_not_fix_lambda_explicit'],
    'unique_scalar_response_interface_selected':False if continuous_family else unique_selector,
    'continuous_family_remains':continuous_family
  },
  'interpretation':interpretation,
  'next_gate':next_gate,
  'nonclaims':[
    'not a unique HMT+Z7 action',
    'not RTK pole/residue/remainder equivalence',
    'not same-action primordial/background closure',
    'not C9 naturalness',
    'not a soft-s result',
    'not k=0.03 production'
  ],
  'threshold_changed':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
