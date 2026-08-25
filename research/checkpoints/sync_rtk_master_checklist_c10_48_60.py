#!/usr/bin/env python3
"""Idempotently append/update C10.48-C10.60 in the canonical monotonic checklist.
Never deletes an existing checklist ID.
"""
from pathlib import Path
import json

p=Path('research/checkpoints/RTK_MASTER_CHECKLIST.md')
s=p.read_text()
anchor_id='C10.47'
if f'| {anchor_id} |' not in s:
    raise SystemExit('C10.47 anchor missing; refuse ambiguous checklist edit')

rows=[
('| C10.48 | Legacy model2 published-equation provenance and retarded subspace | ✅ scoped | `model=2` is the RT / transverse `g_munu Box^-1 R` branch. Appendix-A auxiliary/metric equations match the pinned fork after the refined temporal-covector map `deltaV_lit=(H0/a)(deltaV_code+Psi Vbar_code)`; arbitrary localized homogeneous auxiliary seeds are not free ICs of the fixed retarded nonlocal theory. |'),
('| C10.49 | Corrected legacy RT 00 covector roundtrip | ✅ scoped | With the refined temporal-covector map, the independent translated 00 residual closes on binding epochs: medians fall from ~2.77e-9 to ~6-8e-13 at a=0.1 and to ~8-9e-15 at a=0.5 in both untouched upstream and historical production RTK; no physical coefficients fitted. |'),
('| C10.50 | Preferred-foliation chi/B initial-data structure | ✅ scoped | Leading small-k regularity does not select a finite chi/B value, but for every certified finite k>0 the preferred A/Hamiltonian/momentum constraints make B algebraic; no independent temporal chi initial datum is required once preferred sources are specified. |'),
('| C10.51 | Preferred-DAE ↔ Newtonian representation roundtrip | ✅ scoped | The Newtonian shadow `chi_prime` equation exactly transports the derivative of the coordinate/source transformation on the preferred constraint manifold; all symbolic roundtrip residuals vanish. Do not add chi as an independent Boltzmann state. |'),
('| C10.52 | Executable preferred metric projector API | ✅ scoped | Standalone A→Hamiltonian→momentum finite-k projector closes preferred constraints to ~3.5e-18 and roundtrips through shadow-v3 to ~1.1e-16; production untouched. Physical Newtonian potentials require no explicit B-prime after traceless reduction. |'),
('| C10.53 | Leading chi/B constraint degeneracy and next-order requirement | ✅ scoped | Leading finite-B condition is exactly total comoving regularity and contains no B0. The first determining coefficient is O(k^2): `B0=-N2/(lambda_HL-1)`. |'),
('| C10.54 | Exact next-order B0 source formula | ✅ scoped | `B0=[C2+2 Pcal psi0-E_th phi0]/(2H)`, with `C2=3a^2 delta_mu2+9Ha q2`; psi_prime2 cancels and C2 is invariant between preferred and Newtonian source representations. |'),
('| C10.55 | Finite-EFT-onset strong-filter gradient domain | ✅ scoped | Existing history-wide Mc bound implies `k_phys^2/Mc^2<=1/99` and `a1_eff<=1/100` on the declared cosmological EFT domain; analytic K-expansion relative error <=1/9801. The fixed-k a→0 and fixed-a k→0 limits do not commute, so finite EFT onset remains mandatory. |'),
('| C10.56 | Neutral Khronon early dust finite-X bounds | ✅ scoped | Exact fixed-action background gives `w=O(a^3)`, `c_a^2=O(a^6)`, `0<=c_s^2<=c_a^2`, `k_star~a^-7/2`, with rigorous finite-X bounds. The production adiabatic density relation differs from dust only by the explicitly bounded factor w. |'),
('| C10.57 | Finite-onset adiabatic invariance | ✅ scoped | Relative-density entropy and relative-velocity adiabatic conditions are exactly invariant under the common preferred-foliation time shift B; all machine residuals vanish. Instantaneous adiabaticity plus leading regularity cannot choose C2/B0, so temporal growing-mode/attractor selection or UV/pre-EFT matching is required. |'),
('| C10.58 | Full-action linear source-channel decomposition | ✅ scoped | Q/elliptic filtering belongs to the ordinary A/prepotential gauge-pair source, not ordinary metric stress. The completed projector must use ordinary physical stress + ordinary-only filtered A source + total Ward momentum + action-derived neutral-Khronon metric stress; historical production-GDM stress is provenance, not the final same-action provider. |'),
('| C10.59 | Preferred-coordinate neutral Khronon action-fluid evolution | ✅ scoped | Direct fixed-action shift-current derivation gives `delta_prime=-(1+w)(theta+k^2 B-3 psi_prime)-3H(c_a^2-w)delta` and `theta_prime=-H(1-3c_a^2)theta+k^2[c_s^2 delta/(1+w)+phi]`; B=0 exactly reproduces the certified action-fluid shadow. |'),
('| C10.60 | Curvature-dressed ordinary DAE closure | 🔵 | Frozen theorem tests `mu_hat=delta_mu_N-3W Psi_N`, `h_hat=deltaH0_N-3W0 Psi_N`: preferred sources and differentiated A constraint should become B-prime/Psi_N-prime free, with dressed A denominator `D_A=1-3KW0>1`. Persisted result controls final status. |')
]

# Insert missing rows directly after the last existing C10.47+ row sequence.
# Never remove/reorder existing IDs.
lines=s.splitlines()
insert_at=None
for i,line in enumerate(lines):
    if line.startswith('| C10.47 |'):
        insert_at=i+1
if insert_at is None: raise SystemExit('anchor not found')
for row in rows:
    ident=row.split('|')[1].strip()
    if not any(x.startswith(f'| {ident} |') for x in lines):
        lines.insert(insert_at,row); insert_at+=1
s='\n'.join(lines)+'\n'

# Upgrade C10.60 if result persisted.
r=Path('research/theory_results/RTK_C10_CURVATURE_DRESSED_ORDINARY_DAE_CLOSURE_RESULT_v1.json')
if r.exists():
    d=json.loads(r.read_text()); cls=d.get('classification','')
    old='| C10.60 | Curvature-dressed ordinary DAE closure | 🔵 | Frozen theorem tests `mu_hat=delta_mu_N-3W Psi_N`, `h_hat=deltaH0_N-3W0 Psi_N`: preferred sources and differentiated A constraint should become B-prime/Psi_N-prime free, with dressed A denominator `D_A=1-3KW0>1`. Persisted result controls final status. |'
    if cls=='C10_CURVATURE_DRESSED_ORDINARY_DAE_CLOSURE_PASS_POLE_FREE_SCOPED':
        new='| C10.60 | Curvature-dressed ordinary DAE closure | ✅ scoped | Curvature-dressed ordinary density/A-source variables remove explicit `Psi_N_prime` and `B_prime`; preferred source transforms are algebraic, `D_A=1-3KW0>1` is pole-free for k>0, Mc>0, W0>0, and direct differentiation confirms `K_prime/K=2H a1_eff`. |'
    else:
        new=f'| C10.60 | Curvature-dressed ordinary DAE closure | 🟥/🟨 diagnostic | Persisted classification `{cls}`; follow the frozen result without promoting a dual-interface solver. |'
    s=s.replace(old,new,1)

# Update strict frontier block when its heading is present; preserve all other sections.
heading='## Current strict frontier order'
if heading in s:
    before,after=s.split(heading,1)
    # replace until next markdown H2 if present
    if '\n## ' in after:
        oldblock,tail=after.split('\n## ',1)
        newblock='''\n\n1. C10.60 — persist/verify curvature-dressed ordinary DAE closure; if PASS, use it as the canonical ordinary-source interface.\n2. C10.61 — build a detached dual-interface ODE/DAE prototype: ordinary physical species in curvature-dressed variables, neutral Khronon in preferred action-fluid variables, algebraic completed-U1 metric projection per step.\n3. C10.62 — freeze and run a finite-onset memory-loss/growing-mode attractor test before introducing any UV matching datum or numerical completion parameter choice.\n4. A16/A17 — finish LCDM recenter/refreeze chain without transferring the historical phenomenological RTK score to the completed action.\n5. B04.4 and C09.02-C09.06 — continue Hessian and radiative-protection/naturalness gates independently.\n6. Only after C10.61-C10.62 and a frozen completion-parameter protocol: opt-in completed-U1 spectra, then completed-action likelihood/refit.\n7. T01-T12, G01-G06, N01-N10 — continue cross-framework, GW and nonlinear/compact-object packages without deleting earlier scoped obstructions.\n'''
        s=before+heading+newblock+'\n## '+tail

p.write_text(s)
print('RTK_MASTER_CHECKLIST_C10_48_60_SYNCED')
