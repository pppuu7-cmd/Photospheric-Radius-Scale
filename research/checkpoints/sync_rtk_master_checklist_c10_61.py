#!/usr/bin/env python3
"""Idempotent C10.61 addendum for the monotonic master checklist."""
from pathlib import Path
import json
p=Path('research/checkpoints/RTK_MASTER_CHECKLIST.md')
s=p.read_text()
anchor='| C10.60 |'
if anchor not in s:
    raise SystemExit('C10.60 missing; run prior sync first')
r=Path('research/theory_results/RTK_C10_DUAL_INTERFACE_DAE_PROTOTYPE_RESULT_v1.json')
if not r.exists():
    raise SystemExit('C10.61 authoritative result missing')
d=json.loads(r.read_text()); cls=d.get('classification','')
if cls=='C10_DUAL_INTERFACE_DAE_PROTOTYPE_PASS_SCOPED':
    row='| C10.61 | Detached dual-interface ODE/DAE prototype | ✅ scoped | Synthetic finite-k RK4 smoke-test evolves ordinary curvature-dressed variables plus preferred neutral action fluid with no integrated B/chi state. Max A/H/M residual ≈1.02e-20, source-identity residual ≈2.54e-21, min |coupled phi-B determinant| ≈9.86e-4, and D_A>1 throughout. This validates architecture only, not physical parameters or an attractor. |'
else:
    row=f'| C10.61 | Detached dual-interface ODE/DAE prototype | 🟥/🟨 diagnostic | Persisted classification `{cls}`; do not advance to physical memory-loss testing until the frozen prototype decision tree is resolved. |'
if '| C10.61 |' not in s:
    lines=s.splitlines()
    idx=next(i for i,x in enumerate(lines) if x.startswith('| C10.60 |'))
    lines.insert(idx+1,row)
    s='\n'.join(lines)+'\n'
else:
    lines=s.splitlines()
    lines=[row if x.startswith('| C10.61 |') else x for x in lines]
    s='\n'.join(lines)+'\n'
# Move strict frontier one step forward if current text is present.
s=s.replace('1. C10.60 — persist/verify curvature-dressed ordinary DAE closure; if PASS, use it as the canonical ordinary-source interface.\n2. C10.61 — build a detached dual-interface ODE/DAE prototype: ordinary physical species in curvature-dressed variables, neutral Khronon in preferred action-fluid variables, algebraic completed-U1 metric projection per step.\n3. C10.62 — freeze and run a finite-onset memory-loss/growing-mode attractor test before introducing any UV matching datum or numerical completion parameter choice.',
'''1. C10.62a — freeze a diagnostic completion-parameter/onset protocol inside the already-certified symbolic windows; keep diagnostic choices distinct from a final physical fit.\n2. C10.62b — run a finite-onset memory-loss/growing-mode attractor test with multiple admissible onset perturbations; only a demonstrated decaying memory mode can replace explicit UV matching.\n3. C10.63 — if memory loss passes, extend the dual-interface prototype to the baseline photon+baryon+massless-UR hierarchy before any spectra.''')
p.write_text(s)
print('RTK_MASTER_CHECKLIST_C10_61_SYNCED')
