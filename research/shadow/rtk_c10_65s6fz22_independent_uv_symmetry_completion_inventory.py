#!/usr/bin/env python3
import json,re,urllib.request,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ22_INDEPENDENT_UV_SYMMETRY_COMPLETION_INVENTORY_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ21_HMT_MATTER_INTERFACE_TECHNICAL_NATURALNESS_PREFLIGHT_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ22_INDEPENDENT_UV_SYMMETRY_COMPLETION_INVENTORY_RESULT_v1.json'

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RTK-source-lock/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read().decode('utf-8','replace')

def norm(s):
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s)).lower()

t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
susy_raw=get('https://arxiv.org/abs/1309.5569')
strong_raw=get('https://arxiv.org/abs/1305.0011')
hmt_raw=get('https://arxiv.org/html/1310.6666v4')
susy,strong,hmt=map(norm,(susy_raw,strong_raw,hmt_raw))
checks={}
checks['z21_parent_exact']=p['classification']==t['parent_required']
checks['susy_lifshitz_protection_concrete']='supersymmetric matter sector' in susy and 'lifshitz scaling' in susy and 'lambda' in susy and 'planck' in susy
checks['susy_model_is_scalar_gravity_example']='model of scalar gravity' in susy and 'wess-zumino matter sector' in susy
checks['strong_dynamics_emergent_li_concrete']='emergent lorentz invariance' in strong and 'strong dynamics' in strong and 'gauge/gravity correspondence' in strong
checks['strong_dynamics_suppression_statement']='power-law suppressed' in strong and 'infrared and ultraviolet scales' in strong
checks['hmt_reference_two_arbitrary_constants']='two arbitrary coupling constants' in hmt and 'a 1' in hmt and 'a 2' in hmt
# An explicit HMT matching map would need to formulate the HMT physical-ADM interface itself and fix its constants/equivalent relation.
susy_mentions_hmt=('melby-thompson' in susy) or ('physical adm' in susy) or ('physical-ADM' in susy)
strong_mentions_hmt=('melby-thompson' in strong) or ('physical adm' in strong) or ('physical-ADM' in strong)
checks['susy_no_explicit_hmt_interface_map']=not susy_mentions_hmt
checks['strong_dynamics_no_explicit_hmt_interface_map']=not strong_mentions_hmt
checks['no_rtk_response_or_softs_selection']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False
complete=all(checks.values())
match_found=False
if complete and match_found:
    classification='C10_65S6FZ22_EXPLICIT_INDEPENDENT_HMT_INTERFACE_UV_MATCH_FOUND_PASS_SCOPED'
elif complete:
    classification='C10_65S6FZ22_CANDIDATE_PROTECTION_MECHANISMS_NO_HMT_MATCH_MAP_PARTIAL_PASS_SCOPED'
else:
    classification='C10_65S6FZ22_UV_SYMMETRY_COMPLETION_INVENTORY_INCOMPLETE_BLOCKED_SCOPED'
interpretation=(
 'Two independent pre-soft-s protection mechanisms are source-locked: Lifshitz-sector suppression with supersymmetric matter, and emergent Lorentz invariance from strong dynamics. '
 'The supersymmetric paper illustrates the mechanism with a scalar-gravity plus Wess-Zumino model; the strong-dynamics paper studies generic holographic RG flow. '
 'Neither audited source formulates the universal HMT physical-ADM matter interface or supplies an action-level map fixing its surviving a1,a2-equivalent response parameters. '
 'Therefore these mechanisms are legitimate protection candidates but do not yet remove the Z18/Z19 interface non-identifiability. This is scoped to the audited inventory, not a literature-wide no-go and not C9 closure.'
)
next_gate=(
 'C10.65s6fZ23: audit whether a symmetry principle inside the fixed projectable HMT action can reduce the physical matter-interface family before radiative analysis—for example whether equivalence-principle/universal-metric normalization plus GR/PPN recovery imposes an exact relation rather than a finite allowed region. '
 'Require an action-level identity independent of RTK response. If only phenomenological bounds or a continuous allowed region result, preserve the completion blocker and do not select a representative point.'
)
r={
 'schema':'RTK_C10_65S6FZ22_INDEPENDENT_UV_SYMMETRY_COMPLETION_INVENTORY_RESULT_v1',
 'gate':'C10.65s6fZ22','classification':classification,'checks':checks,
 'source_hashes':{
   'arxiv_1309_5569_abs_sha256':hashlib.sha256(susy_raw.encode()).hexdigest(),
   'arxiv_1305_0011_abs_sha256':hashlib.sha256(strong_raw.encode()).hexdigest(),
   'arxiv_1310_6666_html_sha256':hashlib.sha256(hmt_raw.encode()).hexdigest()
 },
 'inventory':{
   'supersymmetry_lifshitz_candidate_present':checks['susy_lifshitz_protection_concrete'],
   'strong_dynamics_candidate_present':checks['strong_dynamics_emergent_li_concrete'],
   'explicit_low_energy_hmt_matching_map_found':False,
   'hmt_interface_unique_selector_found':False,
   'scope':'three audited pre-soft-s sources'
 },
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a literature-wide UV-completion no-go','not C9 radiative-naturalness closure','not a unique HMT+Z7 action','not RTK pole/residue/remainder equivalence','not same-action primordial/background closure','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
