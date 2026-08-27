#!/usr/bin/env python3
import json, pathlib, subprocess, re

ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ9_PRE_SOFTS_LOCAL_CONSTRAINT_SOURCE_LOCK_AUDIT_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ8_MINIMAL_FULL_PROJECTABLE_ACTION_DOF_AUDIT_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ9_PRE_SOFTS_LOCAL_CONSTRAINT_SOURCE_LOCK_AUDIT_RESULT_v1.json'

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
assert p['soft_s_retest_allowed'] is False and p['production_k003_unblocked'] is False
commit=t['historical_source_commit']

# Audit only the pinned pre-soft-s tree. Broad grep first; classification requires
# same historical file to carry projectability + U(1)/gauge architecture + explicit A field/constraint language.
def grep(pattern):
    cp=subprocess.run(['git','grep','-n','-I','-E',pattern,commit,'--','research'],cwd=ROOT,text=True,capture_output=True)
    return cp.stdout.splitlines() if cp.returncode in (0,1) else (_ for _ in ()).throw(RuntimeError(cp.stderr))

lines=grep(r'projectable|U\(1\)|Newtonian prepotential|gauge field|constraint|N_i|\bA\b')
byfile={}
for line in lines:
    # <commit>:<path>:<line>:<text>
    m=re.match(r'[^:]+:([^:]+):(\d+):(.*)',line)
    if not m: continue
    path,lineno,text=m.group(1),int(m.group(2)),m.group(3)
    byfile.setdefault(path,[]).append((lineno,text))

candidates=[]
for path,rows in byfile.items():
    blob='\n'.join(x[1] for x in rows)
    low=blob.lower()
    projectable=('projectable' in low)
    gauge=('u(1)' in low or 'newtonian prepotential' in low or 'gauge field' in low)
    explicit_A=bool(re.search(r'\bgauge field\s+A\b|\bA\s*(?:field|constraint|multiplier)\b|\bA\b.*\bconstraint\b',blob,re.I))
    constraint=('constraint' in low)
    if projectable and gauge and explicit_A and constraint:
        candidates.append({'path':path,'evidence':[{'line':n,'text':s[:500]} for n,s in rows[:40]]})

found=bool(candidates)
classification=('C10_65S6FZ9_PRE_SOFTS_LOCAL_CONSTRAINT_PARENT_FOUND_PASS_SCOPED' if found else
                'C10_65S6FZ9_NO_PRE_SOFTS_LOCAL_CONSTRAINT_PARENT_FOUND_PASS_SCOPED')
result={
  'schema':'RTK_C10_65S6FZ9_PRE_SOFTS_LOCAL_CONSTRAINT_SOURCE_LOCK_AUDIT_RESULT_v1',
  'gate':'C10.65s6fZ9',
  'classification':classification,
  'checks':{
    'parent_exact':True,
    'historical_commit_pinned':True,
    'audit_restricted_to_pre_softs_tree':True,
    'outcome_neutral_classification':True,
    'no_new_multiplier_coefficient':True,
    'no_soft_s_or_k003':True
  },
  'historical_source_commit':commit,
  'candidate_count':len(candidates),
  'candidates':candidates,
  'interpretation':(
    'A pre-soft-s projectable local constraint parent is source-locked in the pinned archive. This only licenses a separate same-action embedding/Dirac audit; it does not prove that the mechanism removes the Z8 extra scalar or cures soft-s.' if found else
    'No pre-soft-s projectable local constraint parent satisfying all frozen source-lock requirements was found in the pinned archive. Adding an A-like multiplier now would therefore be a new completion hypothesis and cannot be justified from the observed soft-s failure.'),
  'next_gate':(
    'C10.65s6fZ10: reconstruct the exact historical local-constraint action/interface and perform a same-action scalar constraint-rank/DOF audit with the frozen Z7 carrier, without soft-s.' if found else
    'C10.65s6fZ10: formulate an independently motivated projectable local-constraint completion principle before writing any new multiplier action; no soft-s-guided coefficient choice is allowed.'),
  'threshold_changed':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False,
  'nonclaims':['not a full coupled Dirac closure','not a soft-s result','not a k=0.03 production result']
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
