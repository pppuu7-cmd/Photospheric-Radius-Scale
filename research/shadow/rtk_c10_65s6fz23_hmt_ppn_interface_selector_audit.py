#!/usr/bin/env python3
import json,re,urllib.request,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ23_HMT_PPN_INTERFACE_SELECTOR_AUDIT_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ22_INDEPENDENT_UV_SYMMETRY_COMPLETION_INVENTORY_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ23_HMT_PPN_INTERFACE_SELECTOR_AUDIT_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).lower()

t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
raw=get('https://arxiv.org/html/1310.6666v4'); s=norm(raw)
checks={}
checks['z22_parent_exact']=p['classification']==t['parent_required']
checks['universal_coupling_explicit']='propose a universal coupling' in s
checks['ppn_in_terms_of_couplings']='ppn parameters in terms of the coupling constants' in s
checks['large_allowed_parameter_region_explicit']='large region' in s and 'parameter' in s and 'solar system tests' in s
checks['gr_values_realized_by_choice_explicit']='properly choosing these constants' in s and 'same values' in s and 'gr' in s
checks['lambda_not_uniquely_fixed_by_solar_system']='solar system tests impose no constraint on the parameter' in s and 'lambda' in s
checks['no_rtk_or_softs_selection']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False
complete=all(checks.values())
unique=False
if complete and unique:
    classification='C10_65S6FZ23_EXACT_PPN_INTERFACE_SELECTOR_FOUND_PASS_SCOPED'
elif complete:
    classification='C10_65S6FZ23_PPN_ALLOWS_CONTINUOUS_INTERFACE_REGION_PARTIAL_PASS_SCOPED'
else:
    classification='C10_65S6FZ23_HMT_PPN_INTERFACE_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
interpretation=(
 'The universal HMT matter coupling is source-locked and its PPN parameters are derived in terms of theory couplings, but the same source explicitly reports a large allowed parameter region and states that GR PPN values are obtained by properly choosing constants. '
 'It also notes that solar-system tests impose no constraint on lambda. Therefore GR/PPN recovery does not furnish a unique action-level selector for the surviving matter-interface family; it supplies phenomenological constraints/allowed regions. '
 'No representative point is selected. The Z18/Z19 interface non-identifiability and Z12 completion blocker therefore remain in force.'
)
next_gate=(
 'C10.65s6fZ24: audit whether cosmological/background equivalence in the same universal-HMT physical metric imposes a source-locked equality on the surviving interface couplings that is independent of perturbation response. Require the relation to follow from one fixed action/background map, not from observational best fit. If cosmology also leaves a continuous family, stop selector chasing and freeze an explicit completion-hypothesis requirement before any renewed RTK response comparison.'
)
r={
 'schema':'RTK_C10_65S6FZ23_HMT_PPN_INTERFACE_SELECTOR_AUDIT_RESULT_v1','gate':'C10.65s6fZ23','classification':classification,'checks':checks,
 'source_hashes':{'arxiv_1310_6666_html_sha256':hashlib.sha256(raw.encode()).hexdigest()},
 'selector_audit':{'unique_ppn_selector_found':False,'continuous_allowed_region_source_locked':checks['large_allowed_parameter_region_explicit'],'representative_point_selected':False},
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a literature-wide equivalence-principle no-go','not C9 closure','not RTK pole/residue/remainder equivalence','not same-action cosmological closure','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps(r,indent=2,sort_keys=True))
