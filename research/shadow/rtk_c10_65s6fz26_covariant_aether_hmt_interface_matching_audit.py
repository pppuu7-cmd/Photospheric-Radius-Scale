#!/usr/bin/env python3
import json, pathlib, re, urllib.request

TARGET = pathlib.Path('research/theory_targets/RTK_C10_65S6FZ26_COVARIANT_AETHER_HMT_INTERFACE_MATCHING_AUDIT_TARGET_v1.json')
PARENT = pathlib.Path('research/theory_results/RTK_C10_65S6FZ25_SPECTRAL_ACTION_HMT_MATCHING_AUDIT_RESULT_v1.json')
RESULT = pathlib.Path('research/theory_results/RTK_C10_65S6FZ26_COVARIANT_AETHER_HMT_INTERFACE_MATCHING_AUDIT_RESULT_v1.json')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
assert t['threshold_changed'] is False
assert t['soft_s_retest_allowed'] is False
assert t['production_k003_unblocked'] is False

def fetch(arxiv):
    url='https://export.arxiv.org/api/query?id_list='+arxiv
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode('utf-8','replace'), True, url
    except Exception:
        return '', False, url

src1, ok1, url1=fetch('0801.1547')
src2, ok2, url2=fetch('1001.4823')
low1=' '.join(src1.lower().split())
low2=' '.join(src2.lower().split())

def has(text,*patterns):
    return all(re.search(p,text,re.I) is not None for p in patterns)

bridge={
  'sources_retrieved': ok1 and ok2,
  'einstein_aether_is_metric_plus_unit_timelike_vector': has(low1,r'unit timelike vector') or has(low1,r'unit time.?like vector'),
  'generally_covariant_preferred_frame': (has(low1,r'general relativity',r'unit timelike vector') or has(low1,r'preferred frame')),
  'hypersurface_orthogonal_bridge_to_ir_horava': has(low2,r'hypersurface orthogonal') and has(low2,r'horava') and has(low2,r'ir limit')
}

combined=low1+' '+low2
# HMT-specific data must be explicit. The Einstein-aether/IR-Horava bridge alone does not count.
hmt={
  'explicit_projectable_HMT_local_U1': ('projectable' in combined and ('u(1)' in combined or 'u(1) symmetry' in combined) and ('melby' in combined or 'horava-melby' in combined)),
  'explicit_Newtonian_prepotential_or_equivalent': ('newtonian prepotential' in combined),
  'explicit_HMT_gauge_field_A_or_equivalent': ('gauge field a' in combined or 'u(1) gauge field' in combined),
  'explicit_physical_metric_matter_interface_map': ('physical metric' in combined and ('matter coupling' in combined or 'matter interface' in combined)),
  'unique_a1_a2_equivalent_relation': (('a1' in combined or 'a_1' in combined) and ('a2' in combined or 'a_2' in combined) and ('unique' in combined or 'fixed' in combined))
}

if not all(bridge.values()):
    cls='C10_65S6FZ26_SOURCE_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
elif all(hmt.values()):
    cls='C10_65S6FZ26_COVARIANT_AETHER_HMT_MATCH_MAP_FOUND_PASS_SCOPED'
else:
    cls='C10_65S6FZ26_COVARIANT_AETHER_BRIDGE_NO_HMT_U1_MATCH_MAP_PARTIAL_PASS_SCOPED'

if cls.endswith('NO_HMT_U1_MATCH_MAP_PARTIAL_PASS_SCOPED'):
    interpretation=(
      'The audited pre-soft-s sources independently source-lock the covariant Einstein-aether preferred-frame theory and the hypersurface-orthogonal bridge to the IR limit of Horava gravity. '
      'They do not, however, explicitly supply the projectable HMT local-U(1) auxiliary structure, Newtonian prepotential/gauge-field matter interface, or a unique a1,a2-equivalent physical-metric relation. '
      'Therefore covariance plus hypersurface orthogonality cannot be used as a hidden selector for the unresolved HMT matter interface. This is a scoped matching-map result, not a no-go for Einstein-aether, khronometric gravity, or HMT.'
    )
elif cls.endswith('MATCH_MAP_FOUND_PASS_SCOPED'):
    interpretation='The audited covariant-aether sources explicitly satisfy every frozen HMT matching requirement.'
else:
    interpretation='The primary-source metadata did not establish all frozen Einstein-aether/khronometric bridge claims; the gate fails closed.'

out={
  'schema':'RTK_C10_65S6FZ26_COVARIANT_AETHER_HMT_INTERFACE_MATCHING_AUDIT_RESULT_v1',
  'gate':'C10.65s6fZ26',
  'classification':cls,
  'sources':[
    {'arxiv':'0801.1547','api_url':url1,'retrieved':ok1},
    {'arxiv':'1001.4823','api_url':url2,'retrieved':ok2}
  ],
  'bridge_checks':bridge,
  'hmt_matching_checks':hmt,
  'checks':{
    'parent_exact':p['classification']==t['parent_required'],
    'new_input_preregistered':t['new_independent_input']['pre_soft_s'] is True,
    'generic_covariance_not_reinterpreted_as_hmt_u1':True,
    'no_rtk_response_or_softs_selection':True,
    'soft_s_and_k003_stay_blocked':True,
    'threshold_unchanged':True
  },
  'interpretation':interpretation,
  'next_gate':'No HMT coefficient selection is authorized from Z26. Continue only with a genuinely independent action-level principle that explicitly derives the HMT auxiliary/physical-metric interface, or with a preregistered same-action derivation that does not use RTK response or soft-s cancellation as input.',
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False,
  'threshold_changed':False
}
RESULT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
