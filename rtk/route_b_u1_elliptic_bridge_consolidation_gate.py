#!/usr/bin/env python3
"""Current-lineage replay/consolidation of the elliptic U(1) matter bridge.

This is deliberately a replay gate.  It re-executes the exact symbolic workers
that survived in rtk-class-build and consolidates only their proven overlap.
Finite-k physical Pfaffian rank and the production CLASS observable bridge are
kept OPEN by construction.
"""
import json, subprocess, sys
from pathlib import Path

TARGET=Path('research/theory_targets/RTK_ROUTE_B_U1_ELLIPTIC_BRIDGE_CONSOLIDATION_TARGET_v1.json')
t=json.loads(TARGET.read_text())
assert t['classification']=='RTK_ROUTE_B_U1_ELLIPTIC_BRIDGE_CONSOLIDATION_TARGET_V1_FROZEN'

jobs=[
 ('rtk/route_b_u1_elliptic_compensator_dirac_projection_gate.py','u1_elliptic_compensator_dirac_projection_result.json','RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_DIRAC_PROJECTION_PASS'),
 ('rtk/route_b_u1_elliptic_compensator_reduced_chain_support_gate.py','u1_elliptic_compensator_reduced_chain_support_result.json','RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_REDUCED_CHAIN_SUPPORT_PASS'),
 ('rtk/route_b_u1_elliptic_compensator_reduced_constraint_chain_gate.py','u1_elliptic_compensator_reduced_constraint_chain_result.json','RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_REDUCED_CONSTRAINT_CHAIN_PASS'),
 ('rtk/route_b_u1_elliptic_compensator_resolvent_metric_variation_gate.py','u1_elliptic_compensator_resolvent_metric_variation_result.json','RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_RESOLVENT_METRIC_VARIATION_PASS'),
 ('rtk/route_b_u1_elliptic_compensator_k0_matter_rank_inheritance_gate.py','u1_elliptic_compensator_k0_matter_rank_inheritance_result.json','RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_K0_MATTER_RANK_INHERITANCE_PASS'),
 ('rtk/route_b_u1_elliptic_compensator_flrw_a_source_resolution_gate.py','u1_elliptic_compensator_flrw_a_source_resolution_result.json','RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_FLRW_A_SOURCE_RESOLUTION_PASS'),
 ('rtk/route_b_u1_elliptic_k0_rtk_lapse_rank_gate.py','u1_elliptic_k0_rtk_lapse_rank_result.json','RTK_ROUTE_B_U1_ELLIPTIC_K0_RTK_LAPSE_RANK_EXACT_PASS'),
]

replayed=[]
for script,result,expected in jobs:
    assert Path(script).is_file(), script
    cp=subprocess.run([sys.executable,script],text=True,capture_output=True)
    if cp.returncode!=0:
        print(cp.stdout)
        print(cp.stderr,file=sys.stderr)
        raise SystemExit(f'worker failed: {script}')
    p=Path(result)
    assert p.is_file() and p.stat().st_size>0, result
    r=json.loads(p.read_text())
    assert r['classification']==expected,(script,r.get('classification'),expected)
    replayed.append({'script':script,'result':result,'classification':expected})

# Cross-result consistency checks.
rproj=json.loads(Path(jobs[0][1]).read_text())
rchain=json.loads(Path(jobs[2][1]).read_text())
rres=json.loads(Path(jobs[3][1]).read_text())
rmat=json.loads(Path(jobs[4][1]).read_text())
rflrw=json.loads(Path(jobs[5][1]).read_text())
rrtk=json.loads(Path(jobs[6][1]).read_text())

assert rproj['auxiliary_physical_dof_count'].startswith('0:')
assert rproj['projected_constraints']['a1_eff']=='1-1/ell = k_phys^2/(M_c^2+k_phys^2)'
assert rchain['physical_rank_basis']==['pi_N','Jhat','Hperp_hat','phi_hat']
assert 'no zero eigenvalue' in rres['spectral_results']['no_filter_pole']
assert rmat['exact_k0_results']['a1_eff']=='0'
assert 'Q-H0=0' in rflrw['homogeneous_constraint']
assert rrtk['canonical_derivation']['delta_a_RTK']=='{pi_N,H_perp}_RTK=0'

out={
 'classification':'RTK_ROUTE_B_U1_ELLIPTIC_BRIDGE_CURRENT_LINEAGE_REPLAY_PASS',
 'status':'HOMOGENEOUS_BRIDGE_AND_AUXILIARY_PROJECTION_GREEN_FINITE_K_PFAFFIAN_AND_PRODUCTION_OBSERVABLE_BRIDGE_OPEN',
 'target':str(TARGET),
 'replayed_workers':replayed,
 'certified_overlap':{
   'auxiliary_physical_dof':'0 after exact (p_Q,C_Lambda) Dirac projection plus trivial p_Lambda multiplier pair removal',
   'projected_source':'Jhat=J_A^(g)-a1_eff H0',
   'a1_eff':'k_phys^2/(M_c^2+k_phys^2)',
   'filter_domain':'M_c>0; L=1-D^2/M_c^2 has no pole for nonnegative self-adjoint -D^2',
   'homogeneous_FLRW':'k=0 gives Q=H0, cancelling the old evolving ordinary-matter A-source exactly for arbitrary H0(a)',
   'homogeneous_ordinary_matter_rank':'no direct correction to the special-U1 cross block on the stated k=0 support',
   'homogeneous_neutral_RTK_rank':'delta_a_RTK={pi_N,H_perp}_RTK=0 on the rolling k=0 support',
   'reduced_constraint_basis':['pi_N','Jhat','Hperp_hat','phi_hat'],
   'resolvent_variation':'delta a_eff=-(1/M_c^2)L^{-1}[delta(D^2)]L^{-1}, with ||L^{-1}||<=1'
 },
 'critical_current_boundary':{
   'finite_k_reduced_pfaffian':'OPEN: metric dependence of L^{-1} must be retained in the four surviving Poisson operators',
   'production_CLASS_observables':'OPEN: current matched CLASS likelihood does not yet implement the elliptic filtered A-source/constraint dynamics',
   'same_full_action_cosmology_plus_PPN':'NOT YET CERTIFIED until the finite-k bridge is implemented and replayed; local PPN and phenomenological production cosmology remain separately valid scoped results'
 },
 'interpretation':'The old homogeneous family-I FLRW A-source BLACK result is superseded by the elliptic-compensator architecture at k=0, and the auxiliary canonical sector itself is under control. The remaining completion problem is localized to finite-k reduced rank and then to an explicit production-observable implementation; this consolidation does not silently transfer the existing CLASS fit to the new full action.',
 'non_claims':t['non_claims'],
 'next_gate':t['next_gate_if_pass']
}
Path('u1_elliptic_bridge_consolidation_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
