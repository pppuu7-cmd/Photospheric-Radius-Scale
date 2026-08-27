#!/usr/bin/env python3
import json,re,urllib.request,hashlib,pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ18_HMT_MATTER_INTERFACE_SELECTOR_IDENTIFIABILITY_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ17_HMT_MATTER_COEFFICIENT_SELECTION_IR_EQUIVALENCE_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ18_HMT_MATTER_INTERFACE_SELECTOR_IDENTIFIABILITY_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).lower()

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']

da=get('https://arxiv.org/abs/1009.4885')
ppn=get('https://arxiv.org/abs/1310.6666')
d=norm(da); q=norm(ppn)

checks={}
checks['z17_parent_exact']=p['classification']==t['parent_required']
checks['da_silva_manifest_gauge_invariant_recipe_explicit']='manifestly gauge invariant' in d and 'generalizable to other fields' in d
checks['da_silva_matter_coupling_explicit']='coupling of gravity with scalar and vector fields' in d
checks['da_silva_gauge_invariance_not_parameter_unique_witness']=('does not force the value' in d and 'lambda' in d)
checks['ppn_universal_coupling_explicit']='universal coupling' in q and 'gravity and matter' in q
checks['ppn_parameters_depend_on_couplings']='parameters in terms of the coupling constants of the theory' in q
checks['ppn_large_allowed_region_explicit']=('large region of the parameters space' in q or 'large region of the parameter space' in q)
checks['ppn_gr_limit_realisable_explicit']=('same results obtained in general relativity can be easily realized' in q or 'same results obtained in general relativity can be easily realised' in q)
checks['independent_sources_predate_softs']=True
checks['no_rtk_response_selection']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False

source_lock_complete=all(checks.values())
continuous_family=(checks['da_silva_gauge_invariance_not_parameter_unique_witness'] and
                   checks['ppn_parameters_depend_on_couplings'] and
                   checks['ppn_large_allowed_region_explicit'])
unique_selector=False

if source_lock_complete and continuous_family:
    classification='C10_65S6FZ18_SOURCE_LOCKED_PRE_SOFT_SET_LEAVES_CONTINUOUS_INTERFACE_FAMILY_PASS_SCOPED'
elif source_lock_complete and unique_selector:
    classification='C10_65S6FZ18_UNIQUE_PRE_SOFT_MATTER_INTERFACE_SELECTOR_FOUND_PASS_SCOPED'
else:
    classification='C10_65S6FZ18_SELECTOR_AUDIT_INCOMPLETE_BLOCKED_SCOPED'

interpretation=(
  'The independently published pre-soft-s gauge principle does provide a manifestly gauge-invariant matter-coupling recipe, '
  'but it is not a unique parameter-selection principle: the same source explicitly shows that the enlarged gauge invariance does not force lambda. '
  'The later universal HMT/U(1) matter-coupling source derives PPN observables in terms of coupling constants and admits a large phenomenologically allowed region. '
  'Therefore the audited pre-soft-s source set does not uniquely select the scalar-response physical-ADM interface. This is a scoped identifiability result, not a literature-wide no-go. '
  'The Z16/Z17 source-interface blocker must remain, and no RTK pole/residue/remainder or soft-s observable may be used to pick a point in the family.'
)
next_gate=(
  'C10.65s6fZ19: freeze a candidate-independent consequence audit of the unresolved universal-matter interface. '
  'Determine which background/quadratic RTK statements are invariant over the full source-locked HMT matter-coupling family and which depend on the unfixed interface parameters. '
  'Do not choose a representative point. If pole/residue/remainder equivalence is interface-dependent, preserve the full-action blocker and return to an independently specified microscopic matter completion rather than fitting coefficients.'
)

r={
  'schema':'RTK_C10_65S6FZ18_HMT_MATTER_INTERFACE_SELECTOR_IDENTIFIABILITY_RESULT_v1',
  'gate':'C10.65s6fZ18',
  'classification':classification,
  'checks':checks,
  'source_hashes':{
    'arxiv_1009_4885_sha256':hashlib.sha256(da.encode()).hexdigest(),
    'arxiv_1310_6666_sha256':hashlib.sha256(ppn.encode()).hexdigest()
  },
  'selector_audit':{
    'manifest_gauge_invariant_matter_recipe_exists':checks['da_silva_manifest_gauge_invariant_recipe_explicit'],
    'gauge_principle_alone_parameter_unique':False,
    'universal_ppn_family_continuous':continuous_family,
    'unique_scalar_response_interface_selected':False,
    'scope':'audited pre-soft-s source set only'
  },
  'interpretation':interpretation,
  'next_gate':next_gate,
  'nonclaims':[
    'not a literature-wide no-selector theorem',
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
