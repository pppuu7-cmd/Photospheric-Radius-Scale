#!/usr/bin/env python3
"""Idempotent C10.46-C10.47 addendum for the canonical monotonic checklist."""
from pathlib import Path
import json

p=Path('research/checkpoints/RTK_MASTER_CHECKLIST.md')
s=p.read_text()

anchor='| C10.45 | GR comoving-constraint residual floor control | ✅ scoped | Pinned GR model=0 gives late residuals far below RT: GR/RT ≈ 6.72e-3 at a=0.1 and 8.47e-5 at a=0.5. Thus the late ~1e-10 RT residual is not a generic CLASS cancellation floor under the matched diagnostic. |'
rows=[
'| C10.46 | Legacy RT 00 single-direction constraint projection propagation | ✅ scoped negative diagnostic | A well-conditioned deltaU homogeneous projection sets earliest translated R00 to zero, but late residual regenerates: projected/baseline median ratios are ≈0.9997 at a=0.1 and ≈0.9565 at a=0.5 in both untouched upstream and production RTK. This is model=2 implementation provenance, not a completed-U1 no-go. |',
'| C10.47 | Full six-direction auxiliary R00 covector propagation | 🔵 | Frozen normalization-invariant pairwise-minor test spans deltaU,deltaUprime,deltaV,deltaVprime,deltaZ,deltaZprime to determine whether the initial translated-R00 hyperplane is invariant on the local auxiliary IC tangent space. |'
]
if anchor in s:
    pos=anchor
    for row in rows:
        ident=row.split('|')[1].strip()
        if f'| {ident} |' not in s:
            s=s.replace(pos,pos+'\n'+row,1); pos=row
else:
    # Existing master may already contain C10.46 from a newer sync. Never delete/reorder it.
    if '| C10.46 |' not in s:
        raise SystemExit('C10.45 anchor missing and C10.46 absent; refuse ambiguous checklist edit')

old44='| C10.44 | Legacy RT initial 00 first-integral projection/propagation | 🟨 inconclusive | Frozen start-time patterns are mixed; retain the diagnostic without choosing a post-hoc coefficient or threshold. |'
new44='| C10.44 | Legacy RT initial 00 first-integral projection/propagation | 🟨 diagnostic INCONCLUSIVE | ×4 earlier start reduces the earliest residual to ≈0.50 (RTK) / ≈0.45 (upstream) of default, but leaves a=0.1 essentially unchanged and a=0.5 within ≈1.016×. A simple frozen initial-offset explanation is therefore insufficient. |'
if old44 in s: s=s.replace(old44,new44,1)

r46=Path('research/theory_results/RTK_C10_LEGACY_RT_00_CONSTRAINT_PROJECTION_PROPAGATION_RESULT_v1.json')
if r46.exists():
    d=json.loads(r46.read_text()); cls=d.get('classification','')
    active='| C10.46 | Legacy RT 00 single-direction constraint projection propagation | 🔵 | Frozen deltaU homogeneous-mode projection test asks whether an initially exact translated R00=0 condition is preserved without any later correction. |'
    if cls=='C10_LEGACY_RT_00_RESIDUAL_REGENERATED_BY_IMPLEMENTED_MODEL2_EVOLUTION_SCOPED':
        repl='| C10.46 | Legacy RT 00 single-direction constraint projection propagation | ✅ scoped negative diagnostic | A well-conditioned deltaU homogeneous projection sets earliest translated R00 to zero, but late residual regenerates: projected/baseline median ratios are ≈0.9997 at a=0.1 and ≈0.9565 at a=0.5 in both untouched upstream and production RTK. This is model=2 implementation provenance, not a completed-U1 no-go. |'
    else:
        repl=f'| C10.46 | Legacy RT 00 single-direction constraint projection propagation | 🟨 | Persisted classification `{cls}`; retain exact result file and follow its frozen scope before stronger interpretation. |'
    if active in s: s=s.replace(active,repl,1)

r47=Path('research/theory_results/RTK_C10_LEGACY_RT_00_AUXILIARY_COVECTOR_PROPAGATION_RESULT_v1.json')
if r47.exists():
    d=json.loads(r47.read_text()); cls=d.get('classification','')
    active='| C10.47 | Full six-direction auxiliary R00 covector propagation | 🔵 | Frozen normalization-invariant pairwise-minor test spans deltaU,deltaUprime,deltaV,deltaVprime,deltaZ,deltaZprime to determine whether the initial translated-R00 hyperplane is invariant on the local auxiliary IC tangent space. |'
    if cls=='C10_LEGACY_RT_00_AUXILIARY_CONSTRAINT_HYPERPLANE_NONINVARIANT_SCOPED':
        repl='| C10.47 | Full six-direction auxiliary R00 covector propagation | 🟥 scoped implementation diagnostic | Normalization-invariant pairwise minors show the translated-R00 auxiliary IC hyperplane is not invariant under the pinned implemented model=2 flow on the frozen six-direction tangent-space test. This does not test the final coupled U1 completion. |'
    elif cls=='C10_LEGACY_RT_00_AUXILIARY_CONSTRAINT_HYPERPLANE_INVARIANT_SCOPED':
        repl='| C10.47 | Full six-direction auxiliary R00 covector propagation | ✅ scoped | Full auxiliary response covector remains proportional under the frozen test, supporting translated-R00 hyperplane invariance on the sampled local auxiliary tangent space. |'
    elif cls=='C10_LEGACY_RT_00_AUXILIARY_COVECTOR_TEST_DERIVATIVE_LIMITED':
        repl='| C10.47 | Full six-direction auxiliary R00 covector propagation | 🟨 derivative-limited | Independent psi-prime estimators do not support a stable covector-propagation classification. |'
    elif cls=='C10_LEGACY_RT_00_AUXILIARY_COVECTOR_TEST_ILL_CONDITIONED':
        repl='| C10.47 | Full six-direction auxiliary R00 covector propagation | 🟨 ill-conditioned | Too few active normalization-invariant seed-pair minors for a binding classification. |'
    else:
        repl=f'| C10.47 | Full six-direction auxiliary R00 covector propagation | 🟨 | Persisted classification `{cls}`; retain frozen mixed result. |'
    if active in s: s=s.replace(active,repl,1)

s=s.replace('| I13 | Canonical monotonic master checklist | ✅ new | This file. Existing IDs must never be removed; print full checklist after every research iteration. |',
            '| I13 | Canonical monotonic master checklist | ✅ | This file is authoritative and monotonic. Existing IDs must never be removed; routine chat reports show changed rows only, full checklist on explicit request. |')

oldfront='''1. C10.29 — finish the frozen small-k precision/interpolation convergence diagnosis; preserve C10.27 parent FAIL unchanged.\n2. A16 — finish LCDM recenter1 multiscale/fresh-tree chain, then A17 common A5 refreeze.\n3. B04.4 — inspect/persist B4 quarter-scale Hessian and follow its frozen decision tree.\n4. C09.02-C09.06 — obtain an explicit protection/tuning/cutoff mechanism for the same completion rather than treating exceptional operator surfaces as natural.\n5. C10.30-C10.35 — only after numerical regularity/conditioning closure, advance to opt-in completed-U1 Boltzmann spectra and then completed-action likelihood/refit.\n6. T01-T12, G01-G06, N01-N10 — build the cross-framework, GW and nonlinear/compact-object utility packages without deleting any earlier scoped obstruction.'''
newfront='''1. C10.47 — finish the full six-direction legacy model=2 auxiliary-covector propagation diagnostic; preserve C10.27/C10.38/C10.46 scopes unchanged.\n2. C10.41 — persist the already-frozen direct native psi/0i implementation certificate; absence of an artifact is not a scientific FAIL.\n3. A16 — finish LCDM recenter1 multiscale/fresh-tree chain, then A17 common A5 refreeze.\n4. B04.4 — inspect/persist B4 quarter-scale Hessian and follow its frozen decision tree.\n5. C09.02-C09.06 — obtain an explicit protection/tuning/cutoff mechanism for the same completion rather than treating exceptional operator surfaces as natural.\n6. C10.30-C10.35 — after legacy-source provenance is sufficiently localized, advance the physically decisive opt-in self-consistent completed-U1 Boltzmann integration; do not promote frozen legacy RT histories to immutable completion sources.\n7. T01-T12, G01-G06, N01-N10 — build cross-framework, GW and nonlinear/compact-object utility packages without deleting earlier scoped obstructions.'''
if oldfront in s: s=s.replace(oldfront,newfront,1)

p.write_text(s)
print('RTK_MASTER_CHECKLIST_C10_46_47_SYNCED')
