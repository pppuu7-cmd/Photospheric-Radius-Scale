#!/usr/bin/env python3
"""Validate the RTK scientific utility capability contract.

This validator is intentionally conservative: pending theoretical quantities
must never be promoted to implemented by name alone, while production
capabilities required by the frozen final objective must be present.
"""
import json, sys
from pathlib import Path

p=Path(sys.argv[1] if len(sys.argv)>1 else 'rtk/scientific_utility_manifest.json')
d=json.loads(p.read_text())
allowed=set(d['status_vocabulary'])
seen=[]
for group,items in d['capabilities'].items():
    for name,meta in items.items():
        st=meta.get('status')
        if st not in allowed:
            raise SystemExit(f'INVALID_STATUS {group}.{name}={st!r}')
        seen.append((group,name,st))

required_impl={
 ('likelihood','Planck_2018_Commander_SimAll_PlikLite'),
 ('likelihood','Pantheon_full_covariance'),
 ('likelihood','BOSS_DR12_full_covariance'),
 ('likelihood','dense_BOSS_growth_sampling'),
 ('likelihood','final_objective_v1'),
 ('community_interface','capability_manifest'),
 ('community_interface','objective_provenance_manifest'),
}
for key in required_impl:
    meta=d['capabilities'][key[0]][key[1]]
    if meta['status']!='implemented':
        raise SystemExit(f'REQUIRED_NOT_IMPLEMENTED {key}={meta["status"]}')

# Guard the quantities that still require action-level or cross-framework theory.
forbidden_promotions=[
 ('common_modified_gravity_language','mu_k_a'),
 ('common_modified_gravity_language','Sigma_k_a'),
 ('common_modified_gravity_language','eta_slip_k_a'),
 ('common_modified_gravity_language','EFT_ADM_dictionary'),
 ('common_modified_gravity_language','PPF_dictionary'),
 ('theory_consistency','no_ghost_coefficient_Qs'),
 ('theory_consistency','degrees_of_freedom_constraint_count'),
 ('theory_consistency','strong_coupling_or_EFT_cutoff'),
 ('gravitational_waves','tensor_speed_cT'),
 ('local_and_strong_field','PPN'),
]
for key in forbidden_promotions:
    st=d['capabilities'][key[0]][key[1]]['status']
    if st=='implemented':
        raise SystemExit(f'UNJUSTIFIED_THEORY_PROMOTION {key}')

counts={s:0 for s in allowed}
for _,_,s in seen:counts[s]+=1
print('SCIENTIFIC_UTILITY_COUNTS',json.dumps(counts,sort_keys=True))
print('SCIENTIFIC_UTILITY_MANIFEST_PASS')
