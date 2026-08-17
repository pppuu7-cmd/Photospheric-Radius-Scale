#!/usr/bin/env python3
"""Audit direct RTK/Khronon ↔ matter couplings in the implemented linear sector.

This is a source-level and equation-structure audit of the current linear
implementation. It can establish absence of explicit direct CDM/baryon source
terms in the Khronon continuity/Euler equations as implemented; it does not
prove absence of all nonlinear or UV interactions in an unknown completion.
"""
from pathlib import Path
import json,re

p=Path(__file__).with_name('khronon_perturbations.c')
s=p.read_text()

# Explicit matter-species identifiers that would signal direct source terms in
# this standalone Khronon module. Keep metric variables separate: those encode
# gravitational coupling and are expected to be present.
forbidden_patterns={
 'cdm':r'\b(cdm|rho_cdm|delta_cdm|theta_cdm)\b',
 'baryon':r'\b(baryon|baryons|rho_b|delta_b|theta_b)\b',
 'photon_direct_source':r'\b(delta_g|theta_g|rho_g)\b',
 'neutrino_direct_source':r'\b(ncdm|ur|delta_nu|theta_nu)\b',
 'explicit_exchange_vector':r'\b(Q_mu|Qnu|Q_nu|interaction_rate|coupling_beta)\b',
}
found={k:sorted(set(re.findall(v,s,re.I))) for k,v in forbidden_patterns.items()}
metric_required={
 'psi':'m->psi' in s,
 'phi_prime':'m->phi_prime' in s,
 'Hc':'m->Hc' in s,
}
self_required={
 'delta':'y->delta' in s,
 'theta':'y->theta' in s,
 'w':'bg->w' in s,
 'cs2':'bg->cs2' in s,
 'ca2':'bg->ca2' in s,
}

# The adiabatic IC helper may mention photons by design; it is an initial-
# condition relation, not an ongoing direct energy-momentum exchange term.
ic_helper_present='khr_delta_adiabatic_from_photon' in s

no_explicit_direct_sources=all(len(v)==0 for v in found.values())
gravity_present=all(metric_required.values())
self_closed=all(self_required.values())
status='PASS' if no_explicit_direct_sources and gravity_present and self_closed else 'FAIL'
out={
 'status':status,
 'scope':'CURRENT_IMPLEMENTED_LINEAR_KHRONON_MODULE',
 'direct_matter_exchange_in_khronon_continuity_euler':'NOT_PRESENT_EXPLICITLY' if no_explicit_direct_sources else 'FOUND',
 'metric_gravitational_coupling':'PRESENT' if gravity_present else 'MISSING',
 'adiabatic_photon_ic_helper':ic_helper_present,
 'forbidden_direct_source_matches':found,
 'metric_sources':metric_required,
 'self_variables':self_required,
 'interpretation':{
   'Q_mu_in_current_linear_module':'ZERO_BY_IMPLEMENTED_EQUATION_STRUCTURE' if no_explicit_direct_sources else 'NONZERO_OR_UNCLEAR',
   'gravitational_interaction_with_matter':'INDIRECT_THROUGH_SHARED_METRIC',
   'all_nonlinear_direct_interactions':'NOT_PROVEN_ABSENT',
   'fundamental_sequestering_symmetry':'NOT_YET_DERIVED',
   'superluminality_required_for_decoupling':'FALSE',
 },
 'warning':'This audits the current linear implementation, not an unknown nonlinear/UV completion.'
}
print(json.dumps(out,indent=2,sort_keys=True))
if status!='PASS': raise SystemExit(2)
