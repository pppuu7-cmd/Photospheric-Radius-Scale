#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

TARGET=Path('research/theory_targets/RTK_C10_65S6FZ6_PRE_SOFTS_SCALAR_GRAVITY_REPRESENTATION_SOURCE_LOCK_TARGET_v1.json')
PARENT=Path('research/theory_results/RTK_C10_65S6FZ5_SYMMETRY_INTERFACE_CLOSURE_AUDIT_RESULT_v1.json')
OUT=Path('research/theory_results/RTK_C10_65S6FZ6_PRE_SOFTS_SCALAR_GRAVITY_REPRESENTATION_SOURCE_LOCK_RESULT_v1.json')
FROZEN_TARGET_COMMIT='5313cc814314c2f2fb9a45c84b8a8b6145f53f9e'
for p in (TARGET,PARENT):
    if not p.exists(): print('missing',p,file=sys.stderr); sys.exit(3)
t=json.loads(TARGET.read_text()); parent=json.loads(PARENT.read_text())
archive=t['source_scope']['pre_soft_s_archive_commit']

def git(*args):
    return subprocess.run(['git',*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)

obj=git('cat-file','-e',archive+'^{commit}')
if obj.returncode:
    print('archival commit unavailable',archive,obj.stderr,file=sys.stderr); sys.exit(4)

def grep(pattern):
    r=git('grep','-n','-I','-E',pattern,archive)
    if r.returncode not in (0,1):
        print('git grep failed',r.stderr,file=sys.stderr); sys.exit(5)
    return [ln for ln in r.stdout.splitlines() if ln.strip()]

rank_hits=grep(r'Dirac[- ]degenerate|rank[- ]one|p_chi|p_phi|dot X|dot y|aligned[- ]source')
gravity_hits=grep(r'projectable|U\(1\)|Newtonian prepotential|gauge field A|N_i|shift')
joint_hits=grep(r'(rank[- ]one|Dirac[- ]degenerate|p_chi|p_phi).*(U\(1\)|projectable|gauge charge|Newtonian prepotential|invariant shift|D_perp)|(U\(1\)|projectable|gauge charge|Newtonian prepotential|invariant shift|D_perp).*(rank[- ]one|Dirac[- ]degenerate|p_chi|p_phi)')
transform_hits=grep(r'(phi|chi|X|y).*(delta|transform|charge).*(U\(1\)|projectable|gauge)|(U\(1\)|projectable|gauge).*(delta|transform|charge).*(phi|chi|X|y)')
normal_hits=grep(r'(rank[- ]one|Dirac[- ]degenerate|p_chi|p_phi|dot X|dot y).*(invariant shift|D_perp|normal derivative)|(invariant shift|D_perp|normal derivative).*(rank[- ]one|Dirac[- ]degenerate|p_chi|p_phi|dot X|dot y)')
closure_hits=grep(r'(commutator|closure).*(rank[- ]one|Dirac[- ]degenerate|phi|chi).*(U\(1\)|projectable|gauge)|(U\(1\)|projectable|gauge).*(commutator|closure).*(rank[- ]one|Dirac[- ]degenerate|phi|chi)')
checks={
 'target_gate_exact':t.get('gate')=='C10.65s6fZ6',
 'parent_exact':parent.get('classification')=='C10_65S6FZ5_SYMMETRY_INTERFACE_UNDERDETERMINED_PASS_SCOPED',
 'archive_commit_exact':archive=='13acfdbc16d2f3117f1299b8552bcf7b1f996bd1',
 'archive_contains_rank_one_material':len(rank_hits)>0,
 'archive_contains_gravity_gauge_material':len(gravity_hits)>0,
 'no_soft_s':t['guards']['no_soft_s_retest'] is True,
 'no_k003':t['guards']['no_k003_production'] is True,
 'no_new_charge':t['guards']['no_new_charge_assignment'] is True,
 'no_new_field_identification':t['guards']['no_new_field_identification'] is True,
 'threshold_unchanged':t['guards']['threshold_changed'] is False,
}
missing={
 'explicit_joint_field_identification_absent':len(joint_hits)==0,
 'explicit_gravity_transformation_or_charge_absent':len(transform_hits)==0,
 'shared_normal_derivative_or_invariant_shift_absent':len(normal_hits)==0,
 'cross_symmetry_closure_absent':len(closure_hits)==0,
}
base_ok=all(checks.values())
if not base_ok: cls='C10_65S6FZ6_FAIL_SCOPED'
elif all(missing.values()): cls='C10_65S6FZ6_NO_PRE_SOFTS_REPRESENTATION_FOUND_PASS_SCOPED'
else: cls='C10_65S6FZ6_REPRESENTATION_SOURCE_LOCKED_PASS_SCOPED'
r={
 'schema':'RTK_C10_65S6FZ6_PRE_SOFTS_SCALAR_GRAVITY_REPRESENTATION_SOURCE_LOCK_RESULT_v1','gate':'C10.65s6fZ6','classification':cls,
 'checks':checks,'missing_representation_data':missing,
 'archive_evidence_counts':{'rank_one_hits':len(rank_hits),'gravity_gauge_hits':len(gravity_hits),'joint_representation_hits':len(joint_hits),'transformation_hits':len(transform_hits),'shared_normal_derivative_hits':len(normal_hits),'cross_symmetry_closure_hits':len(closure_hits)},
 'archive_evidence_samples':{'rank_one':rank_hits[:8],'gravity_gauge':gravity_hits[:8],'joint_representation':joint_hits[:8],'transform':transform_hits[:8],'shared_normal_derivative':normal_hits[:8],'closure':closure_hits[:8]},
 'finding':('The frozen pre-soft-s archive contains both rank-one/Dirac-degenerate material and gravitational gauge/projectability material, but no explicit source-locked statement was found that identifies the rank-one scalar carrier under the projectable gravitational gauge symmetry, supplies its charge/transformation law, ties its normal derivative to the same invariant shift, and closes the cross-symmetry algebra. The s6fZ5 interface ambiguity therefore cannot be removed from archival data without a new symmetry-first representation choice.' if all(missing.values()) else 'At least one explicit joint representation marker exists in the frozen archive and requires dedicated follow-up before any new representation theorem is introduced.'),
 'what_is_not_claimed':'Absence of a source-locked archival representation is not a no-go for a compatible representation. It forbids only treating an unrecorded neutrality/charge/invariant-shift choice as inherited physics.',
 's6ft_embedding_ready':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,
 'next_gate':('C10.65s6fZ7: freeze a symmetry-first representation theorem/class for the new scalar carrier under the projectable gravitational gauge symmetry, outcome-neutral and without using the soft-s observable, before writing any combined action.' if all(missing.values()) else 'C10.65s6fZ6a: inspect the explicit archival joint-representation candidates before any new theorem.'),
 'threshold_changed':False,
 'provenance':{'workflow':'rtk-c10-65s6fz6-pre-softs-scalar-gravity-representation-source-lock.yml','frozen_target_commit':FROZEN_TARGET_COMMIT,'archive_commit':archive,'threshold_changed':False}
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps(r,indent=2,sort_keys=True)); sys.exit(0 if cls.endswith('PASS_SCOPED') else 2)
