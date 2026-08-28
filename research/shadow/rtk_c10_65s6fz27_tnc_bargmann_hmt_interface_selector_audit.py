#!/usr/bin/env python3
import json, pathlib, re, urllib.request

TARGET = pathlib.Path('research/theory_targets/RTK_C10_65S6FZ27_TNC_BARGMANN_HMT_INTERFACE_SELECTOR_AUDIT_TARGET_v1.json')
PARENT = pathlib.Path('research/theory_results/RTK_C10_65S6FZ26_COVARIANT_AETHER_HMT_INTERFACE_MATCHING_AUDIT_RESULT_v1.json')
RESULT = pathlib.Path('research/theory_results/RTK_C10_65S6FZ27_TNC_BARGMANN_HMT_INTERFACE_SELECTOR_AUDIT_RESULT_v1.json')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
assert t['frozen_before_execution'] is True
assert t['threshold_changed'] is False
assert t['soft_s_retest_allowed'] is False
assert t['production_k003_unblocked'] is False

url='https://export.arxiv.org/api/query?id_list=1504.07461'
try:
    with urllib.request.urlopen(url, timeout=30) as r:
        src=r.read().decode('utf-8','replace')
    retrieved=True
except Exception:
    src=''; retrieved=False
low=' '.join(src.lower().split())

def any_re(*patterns):
    return any(re.search(p,low,re.I) is not None for p in patterns)

def all_re(*patterns):
    return all(re.search(p,low,re.I) is not None for p in patterns)

geo={
  'source_retrieved': retrieved,
  'projectable_horava_from_torsionless_newton_cartan': all_re(r'projectable',r'newton.?cartan') and any_re(r'without torsion',r'torsionless'),
  'precise_field_dictionary_including_khronon': all_re(r'precise dictionary',r'khronon'),
  'hmt_u1_from_bargmann_extension': all_re(r'u\(1\)',r'bargmann extension') and any_re(r'horava and melby',r'horava-melby'),
  'tnc_is_matter_coupling_geometry': all_re(r'geometr',r'field theories couple')
}

# These are deliberately strict: a geometric origin of U(1) is not itself an HMT physical-metric selector.
selector={
  'explicit_hmt_physical_metric_matter_interface': all_re(r'physical metric',r'matter') and any_re(r'a_1',r'a1'),
  'unique_a1_a2_equivalent_relation': any_re(r'a_1',r'a1') and any_re(r'a_2',r'a2') and any_re(r'unique',r'fixed relation',r'determined'),
  'same_principle_derives_matter_coefficients': any_re(r'matter coupling coefficients',r'matter coefficients') and any_re(r'determined',r'fixed',r'derived')
}

if not all(geo.values()):
    cls='C10_65S6FZ27_SOURCE_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
elif all(selector.values()):
    cls='C10_65S6FZ27_TNC_BARGMANN_HMT_INTERFACE_SELECTOR_FOUND_PASS_SCOPED'
else:
    cls='C10_65S6FZ27_TNC_BARGMANN_HMT_U1_ORIGIN_NO_UNIQUE_MATTER_INTERFACE_PARTIAL_PASS_SCOPED'

if cls.endswith('NO_UNIQUE_MATTER_INTERFACE_PARTIAL_PASS_SCOPED'):
    interpretation=(
      'The audited dynamical Newton-Cartan source is a materially stronger geometric bridge than Z26: it source-locks projectable Horava gravity as torsionless dynamical Newton-Cartan geometry, gives a field dictionary including the khronon, and identifies the HMT U(1) with the Bargmann extension. '
      'However, the audited source metadata does not derive the later HMT physical-metric matter interface or a unique a1,a2-equivalent coefficient relation. Therefore the geometric origin of HMT U(1) does not by itself resolve the matter-interface identifiability blocker.'
    )
elif cls.endswith('SELECTOR_FOUND_PASS_SCOPED'):
    interpretation='The audited Newton-Cartan/Bargmann source independently satisfies every frozen geometric and physical-matter-interface selector requirement.'
else:
    interpretation='The primary-source metadata did not establish all frozen Newton-Cartan/Bargmann geometric claims; the gate fails closed.'

out={
  'schema':'RTK_C10_65S6FZ27_TNC_BARGMANN_HMT_INTERFACE_SELECTOR_AUDIT_RESULT_v1',
  'gate':'C10.65s6fZ27',
  'classification':cls,
  'source':{'arxiv':'1504.07461','api_url':url,'retrieved':retrieved},
  'geometric_checks':geo,
  'selector_checks':selector,
  'checks':{
    'parent_exact':p['classification']==t['parent_required'],
    'new_input_preregistered':t['new_independent_input']['pre_soft_s'] is True,
    'u1_origin_not_reinterpreted_as_interface_selector':True,
    'no_rtk_response_or_softs_selection':True,
    'soft_s_and_k003_stay_blocked':True,
    'threshold_unchanged':True
  },
  'interpretation':interpretation,
  'next_gate':'If Z27 does not find a unique matter-interface selector, stop treating geometric/covariant reformulations as coefficient selectors. Continue only with a genuinely microscopic action that derives both the HMT/Bargmann auxiliary structure and matter coupling coefficients, or record a scoped identifiability stop for this search class.',
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False,
  'threshold_changed':False
}
RESULT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
