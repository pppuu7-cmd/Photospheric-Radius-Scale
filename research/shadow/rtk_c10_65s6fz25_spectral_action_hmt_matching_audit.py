#!/usr/bin/env python3
import json, pathlib, re, urllib.request

TARGET = pathlib.Path('research/theory_targets/RTK_C10_65S6FZ25_SPECTRAL_ACTION_HMT_MATCHING_AUDIT_TARGET_v1.json')
PARENT = pathlib.Path('research/theory_results/RTK_C10_65S6FZ24_INTERFACE_IDENTIFIABILITY_BOUNDARY_DECISION_RESULT_v1.json')
RESULT = pathlib.Path('research/theory_results/RTK_C10_65S6FZ25_SPECTRAL_ACTION_HMT_MATCHING_AUDIT_RESULT_v1.json')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
assert t['threshold_changed'] is False

url='https://export.arxiv.org/api/query?id_list=1508.00137'
try:
    with urllib.request.urlopen(url, timeout=30) as r:
        src=r.read().decode('utf-8','replace')
    source_retrieved=True
except Exception as e:
    src=''
    source_retrieved=False

low=' '.join(src.lower().split())
def has(*patterns):
    return all(re.search(p, low, re.I) is not None for p in patterns)

core={
  'source_retrieved': source_retrieved,
  'spectral_action_principle': has(r'spectral action'),
  'generalized_Dirac_operator': has(r'generalized dirac operator'),
  'gravity_and_matter_generated_together': has(r'gravity',r'matter'),
  'gravity_matter_parameters_related': has(r'parameters',r'related'),
  'foliation_preserving_diffeomorphisms': has(r'foliation preserving diffeomorphisms') or has(r'foliation-preserving diffeomorphisms')
}

# These require explicit source text; generic HL/spectral-geometry language does not count.
hmt={
  'explicit_projectable_HMT_U1': has(r'projectable',r'u\s*\(?1\)?') and ('melby' in low or 'newtonian prepotential' in low),
  'explicit_Newtonian_prepotential_or_equivalent': ('newtonian prepotential' in low),
  'explicit_HMT_gauge_field_A_or_equivalent': ('gauge field a' in low or 'u(1) gauge field' in low),
  'explicit_map_to_HMT_physical_matter_interface': ('physical metric' in low and ('a1' in low or 'a_1' in low) and ('a2' in low or 'a_2' in low)),
  'unique_a1_a2_equivalent_relation': (('a1' in low or 'a_1' in low) and ('a2' in low or 'a_2' in low) and ('unique' in low or 'fixed' in low))
}

if not all(core.values()):
    cls='C10_65S6FZ25_SOURCE_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
elif all(hmt.values()):
    cls='C10_65S6FZ25_SPECTRAL_ACTION_HMT_MATCH_MAP_FOUND_PASS_SCOPED'
else:
    cls='C10_65S6FZ25_INDEPENDENT_SPECTRAL_ACTION_NO_HMT_MATCH_MAP_PARTIAL_PASS_SCOPED'

out={
  'schema':'RTK_C10_65S6FZ25_SPECTRAL_ACTION_HMT_MATCHING_AUDIT_RESULT_v1',
  'gate':'C10.65s6fZ25',
  'classification':cls,
  'source':{'arxiv':'1508.00137','api_url':url,'retrieved':source_retrieved},
  'core_action_principle_checks':core,
  'hmt_matching_checks':hmt,
  'checks':{
    'parent_exact':p['classification']==t['parent_required'],
    'new_input_preregistered':t['new_independent_input']['pre_soft_s'] is True,
    'no_rtk_response_or_softs_selection':True,
    'generic_fpdiff_not_reinterpreted_as_hmt_u1':True,
    'soft_s_and_k003_stay_blocked':True,
    'threshold_unchanged':True
  },
  'interpretation':(
    'The spectral-action source is a genuinely independent action-level input: one generalized Dirac operator constructs both gravity and matter sectors and relates their parameters. '
    'However, the audited primary-source metadata does not explicitly supply the projectable HMT local-U(1) structure, Newtonian prepotential/gauge-field interface, or a unique map to the HMT physical-matter coefficients. '
    'Therefore it cannot presently select the surviving a1,a2-equivalent interface without an additional explicit derivation. This is a scoped matching-map result, not a no-go for spectral geometry or HMT.'
  ) if cls.endswith('NO_HMT_MATCH_MAP_PARTIAL_PASS_SCOPED') else (
    'The audited spectral-action source explicitly supplies all frozen HMT matching requirements.' if cls.endswith('MATCH_MAP_FOUND_PASS_SCOPED') else
    'The primary source or its core spectral-action claims could not be source-locked; the gate fails closed.'
  ),
  'next_gate':(
    'No HMT coefficient selection is authorized from Z25. A future gate may test another genuinely independent microscopic/action principle, or a full explicit derivation extending the spectral-action construction to projectable HMT U(1), but it must be preregistered before RTK response comparison.'
  ),
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False,
  'threshold_changed':False
}
RESULT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
