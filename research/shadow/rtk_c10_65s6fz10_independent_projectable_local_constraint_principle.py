#!/usr/bin/env python3
import json, pathlib, re, urllib.request, html

ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ10_INDEPENDENT_PROJECTABLE_LOCAL_CONSTRAINT_PRINCIPLE_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ9_PRE_SOFTS_LOCAL_CONSTRAINT_SOURCE_LOCK_AUDIT_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ10_INDEPENDENT_PROJECTABLE_LOCAL_CONSTRAINT_PRINCIPLE_RESULT_v1.json'

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
assert p['soft_s_retest_allowed'] is False and p['production_k003_unblocked'] is False

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'RTK-source-lock/1.0 research audit'})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.read().decode('utf-8','replace')

def textify(s):
    s=re.sub(r'<script.*?</script>|<style.*?</style>',' ',s,flags=re.I|re.S)
    s=re.sub(r'<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',html.unescape(s)).strip()

urls={
  'hmt_abs':'https://arxiv.org/abs/1007.2410',
  'hmt_html':'https://arxiv.org/html/1007.2410',
  'ww_abs':'https://arxiv.org/abs/1009.2089'
}
raw={}
errors={}
for k,u in urls.items():
    try:
        raw[k]=textify(fetch(u))
    except Exception as e:
        errors[k]=repr(e)

source_complete=(len(errors)==0)
checks={
  'parent_exact': True,
  'target_frozen_semantics': t['threshold_changed'] is False,
  'no_soft_s_or_k003': t['soft_s_retest_allowed'] is False and t['production_k003_unblocked'] is False,
  'external_source_fetch_complete': source_complete,
  'hmt_title_exact': False,
  'hmt_projectable_lapse_explicit': False,
  'hmt_local_u1_explicit': False,
  'hmt_scalar_graviton_elimination_explicit': False,
  'ww_title_exact': False,
  'ww_prepotential_explicit': False,
  'ww_local_u1_gauge_field_A_explicit': False,
  'ww_constraint_equations_explicit': False,
  'no_coefficient_or_rtk_action_selected': True,
  'nonprojectable_not_reinterpreted': True
}

if source_complete:
    hmt_abs=raw['hmt_abs']
    hmt_html=raw['hmt_html']
    ww=raw['ww_abs']
    checks['hmt_title_exact']='General Covariance in Quantum Gravity at a Lifshitz Point' in hmt_abs
    # HMT full text explicitly states N(t) is constant on spatial slices and calls the minimal theory projectable.
    checks['hmt_projectable_lapse_explicit']=(
        bool(re.search(r'N\s*\(t\)',hmt_html,re.I)) and
        bool(re.search(r'projectable',hmt_html,re.I)) and
        bool(re.search(r'constant along the spatial slices|only a function of time',hmt_html,re.I))
    )
    checks['hmt_local_u1_explicit']=(
        bool(re.search(r'local\s+U\s*\(1\)',hmt_abs,re.I)) or
        bool(re.search(r'U\s*\(1\).*Diff',hmt_html,re.I))
    )
    checks['hmt_scalar_graviton_elimination_explicit']=bool(
        re.search(r'(eliminates|eliminate).*scalar graviton|scalar graviton.*(eliminated|eliminate)',hmt_abs,re.I)
    )
    checks['ww_title_exact']='Cosmology in nonrelativistic general covariant theory of gravity' in ww
    checks['ww_prepotential_explicit']=bool(re.search(r'Newtonian pre-?potential|Newtonian prepotential',ww,re.I))
    checks['ww_local_u1_gauge_field_A_explicit']=bool(
        re.search(r'local\s+U\s*\(1\)',ww,re.I) and re.search(r'gauge field\s+A',ww,re.I)
    )
    checks['ww_constraint_equations_explicit']=bool(
        re.search(r'Hamiltonian.*super-?momentum constraints',ww,re.I) and
        re.search(r'equations for.*(?:phi|prepotential).*A|equations for.*A',ww,re.I)
    )

principle_found=all([
    checks['hmt_title_exact'],
    checks['hmt_projectable_lapse_explicit'],
    checks['hmt_local_u1_explicit'],
    checks['hmt_scalar_graviton_elimination_explicit'],
    checks['ww_title_exact'],
    checks['ww_prepotential_explicit'],
    checks['ww_local_u1_gauge_field_A_explicit'],
    checks['ww_constraint_equations_explicit']
])

if not source_complete:
    classification='C10_65S6FZ10_EXTERNAL_SOURCE_LOCK_INCOMPLETE_BLOCKED_SCOPED'
elif principle_found:
    classification='C10_65S6FZ10_INDEPENDENT_PROJECTABLE_LOCAL_U1_PRINCIPLE_FOUND_PASS_SCOPED'
else:
    classification='C10_65S6FZ10_NO_INDEPENDENT_PROJECTABLE_LOCAL_CONSTRAINT_PRINCIPLE_FOUND_PASS_SCOPED'

result={
  'schema':'RTK_C10_65S6FZ10_INDEPENDENT_PROJECTABLE_LOCAL_CONSTRAINT_PRINCIPLE_RESULT_v1',
  'gate':'C10.65s6fZ10',
  'classification':classification,
  'checks':checks,
  'source_urls':urls,
  'source_errors':errors,
  'source_lock':{
    'HMT_2010':{
      'arxiv':'1007.2410',
      'role':'independent projectable local-U1 gravitational constraint/gauge principle',
      'nonclaim':'not yet coupled to the frozen RTK Z7 carrier and not an RTK action'
    },
    'WANG_WU_2010':{
      'arxiv':'1009.2089',
      'role':'independent source for Newtonian prepotential, local U1 gauge field A, and explicit constraint/equation structure',
      'nonclaim':'cosmology of the literature architecture is not RTK background equivalence'
    }
  },
  'interpretation':(
    'An independently motivated projectable local-U1 gravitational constraint/gauge principle exists in pre-existing literature: projectable N=N(t), local U(1), auxiliary/prepotential structure, and scalar-graviton elimination are source-locked. This licenses only a separate fixed-action RTK embedding audit; it does not license borrowing the literature action as RTK or retesting soft-s.' if principle_found else
    'The frozen external literature audit did not establish every required projectable local-constraint fact. No new RTK multiplier action is licensed by this gate.'
  ),
  'next_gate':(
    'C10.65s6fZ11: freeze one explicit projectable local-U1 ADM action/interface from the independently motivated literature principle, couple only the predeclared Z7 gauge-invariant carrier representation, and perform a same-action full scalar constraint-rank/DOF preflight before any background or soft-s matching.' if principle_found else
    'Keep s6fT blocked; improve or replace the independent projectable constraint principle without using soft-s.'
  ),
  'threshold_changed':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False,
  'nonclaims':[
    'not a full RTK completion',
    'not full coupled Dirac closure',
    'not radiative naturalness',
    'not background equivalence',
    'not a soft-s result',
    'not a k=0.03 production result'
  ]
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
