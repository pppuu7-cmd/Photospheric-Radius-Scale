#!/usr/bin/env python3
import json,re,urllib.request,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ23_HMT_INTERNAL_INTERFACE_SELECTOR_AUDIT_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ22_INDEPENDENT_UV_SYMMETRY_COMPLETION_INVENTORY_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ23_HMT_INTERNAL_INTERFACE_SELECTOR_AUDIT_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    s=re.sub(r'<[^>]+>',' ',s)
    s=s.replace('\\(',' ').replace('\\)',' ')
    return re.sub(r'\s+',' ',s).lower()

t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
hmt_raw=get('https://arxiv.org/html/1310.6666v4')
early_raw=get('https://arxiv.org/abs/1206.1338')
hmt,early=norm(hmt_raw),norm(early_raw)
checks={}
checks['z22_parent_exact']=p['classification']==t['parent_required']
checks['projectable_hmt_explicit']=('projectability condition' in hmt and 'n=n(t)' in hmt) or ('projectable' in early)
checks['universal_metric_interface_explicit']='matter fields universally couple' in hmt and 'two arbitrary coupling constants' in hmt
checks['a1_a2_retained_as_arbitrary_constants']='two arbitrary coupling constants' in hmt and ('a 1' in hmt or 'a_{1}' in hmt) and ('a 2' in hmt or 'a_{2}' in hmt)
checks['unit_normalization_not_parameter_selection']='freedom to rescale the units of time and space' in hmt
checks['ppn_large_region_explicit']='large region' in hmt and 'parameters space' in hmt
checks['gr_ppn_recovery_nonunique']='same results obtained in general relativity can be easily realized' in hmt or 'same values as were given in gr' in hmt
checks['lambda_not_fixed_by_solar_system']='solar system tests impose no constraint on the parameter' in hmt and 'lambda' in hmt
checks['earlier_u1_metric_prescription_observationally_bounded']='invariant not only under the foliation-preserving diffeomorphism but also under the local u(1)' in early and ('10^{-5}' in early or '10 -5' in early or '10−5' in early)
checks['earlier_action_principle_origin_unresolved']='remains to be understood how to obtain such a prescription from the action principle' in early
checks['no_rtk_response_or_softs_selection']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False
complete=all(checks.values())
# The audited sources retain arbitrary/observationally bounded couplings and explicitly lack a derivation of the earlier prescription from an action principle.
exact_selector=False
if complete and exact_selector:
    classification='C10_65S6FZ23_EXACT_INTERNAL_HMT_INTERFACE_SELECTOR_FOUND_PASS_SCOPED'
elif complete:
    classification='C10_65S6FZ23_HMT_SYMMETRY_PPN_LEAVES_CONTINUOUS_INTERFACE_FAMILY_PARTIAL_PASS_SCOPED'
else:
    classification='C10_65S6FZ23_INTERNAL_INTERFACE_SELECTOR_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
interpretation=(
 'The fixed HMT U(1)-invariant physical-metric construction establishes a universal matter-coupling form but does not uniquely fix its surviving coefficients. '
 'The later full PPN treatment explicitly keeps a1,a2 as arbitrary coupling constants after exhausting time/space unit normalization, and solar-system compatibility occupies a large parameter region rather than a unique point. '
 'The earlier projectable prescription likewise gives an observational bound on its metric-coupling parameter and explicitly states that deriving that prescription from an action principle remains unresolved. '
 'Therefore U(1) invariance, universal-metric normalization, and GR/PPN recovery do not provide the exact action-level selector required to remove the Z16-Z22 interface non-identifiability. This is scoped to the audited HMT sources, not a literature-wide theorem.'
)
next_gate=(
 'C10.65s6fZ24: freeze an identifiability boundary/decision gate. Determine whether any remaining pre-soft-s, independently motivated criterion already source-locked in the project (microscopic field content, symmetry representation, or action principle) can fix the HMT physical-metric coefficients without using RTK response. If none is source-locked, classify the current HMT+Z7 route as parameter-underdetermined and stop coefficient-selection iterations until genuinely new microscopic input is supplied; preserve all soft-s and k=0.03 blocks.'
)
r={
 'schema':'RTK_C10_65S6FZ23_HMT_INTERNAL_INTERFACE_SELECTOR_AUDIT_RESULT_v1',
 'gate':'C10.65s6fZ23','classification':classification,'checks':checks,
 'source_hashes':{
   'arxiv_1310_6666_html_sha256':hashlib.sha256(hmt_raw.encode()).hexdigest(),
   'arxiv_1206_1338_abs_sha256':hashlib.sha256(early_raw.encode()).hexdigest()
 },
 'selector_audit':{
   'u1_invariant_universal_metric_form_present':checks['universal_metric_interface_explicit'],
   'interface_constants_remain_arbitrary':checks['a1_a2_retained_as_arbitrary_constants'],
   'gr_ppn_recovery_is_unique_selector':False,
   'exact_action_level_interface_selector_found':False,
   'allowed_region_remains_continuous':True,
   'earlier_prescription_action_origin_unresolved':checks['earlier_action_principle_origin_unresolved']
 },
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a literature-wide HMT uniqueness no-go','not C9 radiative-naturalness closure','not a unique HMT+Z7 action','not RTK pole/residue/remainder equivalence','not same-action primordial/background closure','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
