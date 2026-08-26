#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'research/shadow/rtk_c10_65s4b_moderate_k_completed_onset_seed.py'
RESULT=ROOT/'research/theory_results/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1.json'
TARGET=ROOT/'research/theory_targets/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_TARGET_v1.json'
# Execute the frozen numerical analyzer exactly as written. Its historical harness
# mistakenly includes threshold_changed=false inside all(checks.values()), making
# PASS logically impossible. We ignore only that process exit code, then re-evaluate
# the already-written result against every frozen scientific check plus the explicit
# requirement threshold_changed==false. No numerical quantity or threshold changes.
subprocess.run([sys.executable,str(BASE)],cwd=ROOT,check=False)
d=json.loads(RESULT.read_text()); t=json.loads(TARGET.read_text())
checks=d['checks']
scientific={k:v for k,v in checks.items() if k!='threshold_changed'}
passed=(all(v is True for v in scientific.values()) and checks.get('threshold_changed') is False and d.get('threshold_changed') is False)
d['classification']=t['pass_classification'] if passed else t['fail_classification']
d['interpretation']=t['interpretation_if_pass'] if passed else 'The frozen moderate-k completed onset seed gate failed; do not proceed to production/current-state RHS at the new modes.'
d['next_gate']=t['next_if_pass'] if passed else 'Diagnose C10.65s4b without weakening the frozen criteria.'
d['classification_guard_repair']={
  'base_analyzer_executed_unchanged':str(BASE.relative_to(ROOT)),
  'historical_bug':'passed=all(checks.values()) included threshold_changed=false and therefore made PASS impossible',
  'repair_rule':'all frozen scientific checks must be literal true AND threshold_changed must be false',
  'scientific_thresholds_changed':False,
  'numerical_result_changed':False
}
RESULT.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+'\n')
print(d['classification']); print(json.dumps(d['maxima'],sort_keys=True))
raise SystemExit(0 if passed else 2)
