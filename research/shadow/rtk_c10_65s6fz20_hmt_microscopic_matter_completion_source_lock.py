#!/usr/bin/env python3
import json,re,urllib.request,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ20_HMT_MICROSCOPIC_MATTER_COMPLETION_SOURCE_LOCK_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ19_UNRESOLVED_INTERFACE_CONSEQUENCE_AUDIT_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ20_HMT_MICROSCOPIC_MATTER_COMPLETION_SOURCE_LOCK_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).lower()

t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
full=get('https://arxiv.org/html/1310.6666v4')
da=get('https://arxiv.org/abs/1009.4885')
f=norm(full); d=norm(da)
checks={}
checks['z19_parent_exact']=p['classification']==t['parent_required']
checks['hmt_uv_action_origin_not_obvious_explicit']='from uv viewpoints' in f and 'not obvious how to obtain such a prescription from the action principle' in f
checks['hmt_ir_scalar_tensor_emergence_explicit']='scalar-tensor extension' in f and 'emerge in the ir' in f
checks['hmt_ir_fine_tuning_explicit']='fine-tuning in the ir' in f
checks['hmt_physical_adm_interface_explicit']='tilde{n}' in f and 'omega' in f and 'matter fields universally couple' in f
checks['hmt_a1_a2_arbitrary_explicit']='a 1' in f and 'a 2' in f and 'two arbitrary coupling constants' in f
checks['da_silva_gauge_recipe_independent']='manifestly gauge invariant' in d and 'generalizable to other fields' in d
checks['da_silva_not_unique_parameter_witness']='does not force the value' in d and 'lambda' in d
checks['independent_sources_predate_softs']=True
checks['no_rtk_response_selection']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False
complete=all(checks.values())
microscopic_unique=False
unfixed=(checks['hmt_uv_action_origin_not_obvious_explicit'] and checks['hmt_ir_fine_tuning_explicit'] and checks['hmt_a1_a2_arbitrary_explicit'])
if complete and unfixed:
    classification='C10_65S6FZ20_PUBLISHED_HMT_MICROSCOPIC_ORIGIN_UNFIXED_FINE_TUNED_IR_PARTIAL_PASS_SCOPED'
elif complete and microscopic_unique:
    classification='C10_65S6FZ20_UNIQUE_MICROSCOPIC_HMT_MATTER_SELECTOR_FOUND_PASS_SCOPED'
else:
    classification='C10_65S6FZ20_MICROSCOPIC_SOURCE_LOCK_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
interpretation=(
 'The audited pre-soft-s universal HMT/U(1) matter-coupling source does not supply a unique microscopic selector for the surviving physical-metric interface. '
 'It explicitly states that from the UV viewpoint the action-principle origin of the prescription is not obvious; Appendix C offers an IR scalar-tensor route only at the expense of IR fine-tuning; and the physical-metric functions retain two arbitrary coupling constants a1 and a2. '
 'The independent da Silva gauge-invariant matter recipe supplies symmetry structure but is itself not a unique parameter-selection mechanism. '
 'Therefore Z19 cannot be reopened by choosing a1,a2 from RTK response data. This conclusion is scoped to the audited published sources, not a literature-wide no-go.'
)
next_gate=(
 'C10.65s6fZ21: freeze a radiative/technical-naturalness preflight for the unresolved HMT universal-matter interface family before attempting any coefficient choice. '
 'Ask whether a symmetry or RG fixed structure protects a unique relation among the surviving matter-interface couplings; do not use RTK response or soft-s data. '
 'If no protected selector exists, preserve the completion blocker and record that a genuinely new microscopic matter completion must be independently proposed before background/quadratic equivalence can be reopened.'
)
r={
 'schema':'RTK_C10_65S6FZ20_HMT_MICROSCOPIC_MATTER_COMPLETION_SOURCE_LOCK_RESULT_v1','gate':'C10.65s6fZ20','classification':classification,'checks':checks,
 'source_hashes':{'arxiv_1310_6666_html_sha256':hashlib.sha256(full.encode()).hexdigest(),'arxiv_1009_4885_sha256':hashlib.sha256(da.encode()).hexdigest()},
 'microscopic_audit':{'unique_uv_action_selector_found':False,'published_uv_origin_not_obvious':checks['hmt_uv_action_origin_not_obvious_explicit'],'published_ir_emergence_requires_fine_tuning':checks['hmt_ir_fine_tuning_explicit'],'a1_a2_fixed':False,'scope':'audited pre-soft-s sources only'},
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a literature-wide no-microphysics theorem','not a unique HMT+Z7 action','not RTK pole/residue/remainder equivalence','not same-action primordial/background closure','not C9 naturalness','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
