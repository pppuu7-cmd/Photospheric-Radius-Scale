#!/usr/bin/env python3
"""Idempotently sync current RTK frontier into the monotonic master checklist.

Never deletes existing checklist IDs. It only updates explicitly named stale
rows and appends missing newer rows. Full checklist display in chat is by
explicit user request; routine iteration reports should show only changed/current
rows.
"""
from pathlib import Path
import json

p=Path('research/checkpoints/RTK_MASTER_CHECKLIST.md')
s=p.read_text()

old='This is the checklist that must be printed after every research iteration.'
new=('This is the canonical repository checklist. Print the **full** checklist in chat only on explicit user request; '
     'after a normal research iteration report only the rows/statuses changed in that iteration.')
if old in s:
    s=s.replace(old,new,1)

oldrow='| C10.29 | Precision-convergence follow-up of C10.27 | 🔵 | Frozen next gate: compare baseline, exact historical ultra precision and tighter diagnostic tier plus interpolation convergence before interpreting the smallest-k residual. |'
newrow='| C10.29 | Precision-convergence follow-up of C10.27 | ✅ diagnostic INCONCLUSIVE | Early-epoch residuals fall strongly with tighter precision, while late-epoch residuals are precision-stable; no single numerical-floor explanation closes all epochs. Parent C10.27 FAIL remains retained and scoped. |'
if oldrow in s:
    s=s.replace(oldrow,newrow,1)

anchor='| C10.36 | Massive-neutrino completion-source extension | 🟨 | Separate B4/C10 source generalization. |'
newrows=[
'| C10.37 | Legacy RT auxiliary external 00/0i roundtrip | 🟥 diagnostic not closed | Literature-derived auxiliary reconstruction does not close on production RTK histories; this is retained as a translation/constraint diagnostic, not a completed-U1 no-go. |',
'| C10.38 | Untouched upstream native RT external-roundtrip control | 🟥 diagnostic FAIL | The same mismatch exists in pinned upstream model=2 before any DBI-Khronon patch; Khronon source replacement is excluded as the cause of this mismatch. |',
'| C10.39 | Fixed-source replay scope theorem | ✅ | Raw legacy RT stress histories are metric-history dependent; detached C10.27 FAIL does not exclude a self-consistent coupled completed-U1 solution after reintegration with U1 metric feedback. |',
'| C10.40 | Legacy RT convention / Hamiltonian-00 translation origin | 🟨 | The simple convention map is now audited; remaining question is why the separately translated literature 00 first-integral is not numerically closed by this fork. |',
'| C10.41 | Direct native model2 psi/0i metric identities | 🔵 | Frozen executable test compares the literal model=2 algebraic psi and phi-prime/0i code equations in untouched upstream and production RTK. |',
'| C10.42 | RT literature ↔ CLASS fork 00 translation audit | ✅ scoped | Exact Phi/Psi, x/eta, V/Z, H0, a and CLASS-density conversion reproduces the already used external 00 residual; a simple unit/coordinate/sign normalization error is excluded. Independent numerical 00 closure remains separate. |',
'| C10.43 | Coupled replay architecture correction | ✅ | Physically decisive completion test is an opt-in self-consistent U1+matter/Khronon Boltzmann evolution; historical RT histories remain controls/initial guesses, not immutable completion sources. |',
'| C10.44 | Legacy RT initial 00 first-integral projection/propagation | 🟨 | The audited IC block uses the standard GR Newtonian gauge transform and then zeroes all nonlocal auxiliary perturbations; no explicit literature-00 projection is visible there. Earliest-state and start-time convergence test is required before calling the old fork inconsistent. |'
]
if anchor not in s:
    raise SystemExit('C10.36 anchor missing; refuse non-monotonic checklist edit')
for row in newrows:
    ident=row.split('|')[1].strip()
    if f'| {ident} |' not in s:
        s=s.replace(anchor,anchor+'\n'+row,1)
        anchor=row

# Upgrade stale C10.42 wording if a previous sync inserted it before the analytic audit closed.
old42='| C10.42 | RT literature ↔ CLASS fork 00 translation audit | 🟨 | After direct-native identities, isolate variable normalization, sign, definition or derived-constraint differences in the old fork rather than fitting arbitrary coefficients. |'
new42='| C10.42 | RT literature ↔ CLASS fork 00 translation audit | ✅ scoped | Exact Phi/Psi, x/eta, V/Z, H0, a and CLASS-density conversion reproduces the already used external 00 residual; a simple unit/coordinate/sign normalization error is excluded. Independent numerical 00 closure remains separate. |'
if old42 in s:
    s=s.replace(old42,new42,1)

# If the new direct-native result has appeared, upgrade C10.41 deterministically.
r=Path('research/theory_results/RTK_C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITY_RESULT_v1.json')
if r.exists():
    d=json.loads(r.read_text())
    current='| C10.41 | Direct native model2 psi/0i metric identities | 🔵 | Frozen executable test compares the literal model=2 algebraic psi and phi-prime/0i code equations in untouched upstream and production RTK. |'
    if d.get('classification')=='C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITIES_PASS_BOTH_UPSTREAM_AND_RTK':
        repl='| C10.41 | Direct native model2 psi/0i metric identities | ✅ scoped | Literal implemented psi and phi-prime/0i identities close within the frozen tolerance in both untouched upstream and production RTK; this is an implementation-consistency certificate, not an independent Hamiltonian/00 theorem. |'
    else:
        repl='| C10.41 | Direct native model2 psi/0i metric identities | 🟥 diagnostic FAIL | At least one literal implemented metric identity failed the frozen direct-native residual criterion; localize tree/equation before advancing coupled completion integration. |'
    if current in s:
        s=s.replace(current,repl,1)

p.write_text(s)
print('RTK_MASTER_CHECKLIST_FRONTIER_SYNCED')
