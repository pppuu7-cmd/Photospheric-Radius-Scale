#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_TARGET_v1.json'
P65C=ROOT/'research/theory_results/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_RESULT_v1.json'
PREADY=ROOT/'research/theory_results/RTK_C10_65B_IMPLEMENTATION_READINESS_RESULT_v1.json'


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def must(text: str, pattern: str, label: str):
    if re.search(pattern,text,re.S) is None:
        raise RuntimeError(f'missing frozen source marker: {label}')
    return label


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    t=json.loads(TARGET.read_text())
    p65c=json.loads(P65C.read_text())
    ready=json.loads(PREADY.read_text())
    assert t['status']=='FROZEN_BEFORE_SOURCE_AUDIT'
    assert p65c['classification']=='C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_PASS_SCOPED'
    assert ready['classification']=='C10_65B_IMPLEMENTATION_READY_ARCHITECTURE_HIERARCHY_PORT_INCOMPLETE_SCOPED'

    cr=Path(args.class_root)
    inp=(cr/'source/input.c').read_text()
    per=(cr/'source/perturbations.c').read_text()
    labels=[]
    labels.append(must(inp,r'ppr->tight_coupling_trigger_tau_c_over_tau_h\s*=\s*0\.015\s*;', 'default_trigger_tau_c_over_tau_h'))
    labels.append(must(inp,r'ppr->tight_coupling_trigger_tau_c_over_tau_k\s*=\s*0\.01\s*;', 'default_trigger_tau_c_over_tau_k'))
    labels.append(must(inp,r'ppr->tight_coupling_approximation\s*=\s*\(int\)compromise_CLASS\s*;', 'default_compromise_CLASS'))
    labels.append(must(per,r'tau_c/tau_h\s*<\s*ppr->tight_coupling_trigger_tau_c_over_tau_h.*?tau_c/tau_k\s*<\s*ppr->tight_coupling_trigger_tau_c_over_tau_k', 'runtime_tca_switch_uses_both_triggers'))
    labels.append(must(per,r'metric_continuity\s*=\s*-3\.\*pvecmetric\[ppw->index_mt_phi_prime\]\s*;\s*metric_euler\s*=\s*k2\*pvecmetric\[ppw->index_mt_psi\]\s*;\s*metric_shear\s*=\s*0\.', 'newtonian_metric_interface'))
    labels.append(must(per,r'dy\[pv->index_pt_delta_g\]\s*=\s*-4\./3\.\*\(theta_g\+metric_continuity\)\s*;', 'photon_density_equation'))
    labels.append(must(per,r'dy\[pv->index_pt_delta_b\]\s*=\s*-\(theta_b\+metric_continuity\)\s*;', 'baryon_density_equation'))
    labels.append(must(per,r'class_call\(perturb_tca_slip_and_shear\(y,pppaw,error_message\)', 'tca_helper_invocation'))
    labels.append(must(per,r'int\s+perturb_tca_slip_and_shear\s*\(', 'tca_helper_definition'))
    labels.append(must(per,r'shear_g\s*=\s*16\./45\.\*tau_c\*\(theta_g\+metric_shear\)\s*;', 'first_order_photon_shear'))
    labels.append(must(per,r'if\s*\(ppr->tight_coupling_approximation\s*==\s*\(int\)compromise_CLASS\).*?slip\s*=\s*\(1\.-2\.\*a_prime_over_a\*F\)\*slip.*?shear_g\s*=\s*\(1\.-11\./6\.\*dtau_c\)\*shear_g', 'compromise_second_order_slip_and_shear'))
    labels.append(must(per,r'dy\[pv->index_pt_theta_b\]\s*=\s*\(\s*-a_prime_over_a\*theta_b\s*\+k2\*\(cb2\*\(delta_b\+delta_temp\)\+R\*\(delta_g/4\.-s2_squared\*ppw->tca_shear_g\)\)\s*\+R\*ppw->tca_slip\)\/\(1\.\+R\)\s*\+metric_euler\s*;', 'baryon_tca_momentum_equation'))

    out={
      'schema':'RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1',
      'gate':'C10.65d',
      'classification':'C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED',
      'target':'research/theory_targets/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_TARGET_v1.json',
      'pinned_upstream':t['pinned_upstream'],
      'audited_source_hashes_sha256':{
        'source/input.c':sha256(cr/'source/input.c'),
        'source/perturbations.c':sha256(cr/'source/perturbations.c')
      },
      'verified_marker_count':len(labels),
      'verified_markers':labels,
      'frozen_port_contract':t['required_source_facts'],
      'completed_interface_rule':{
        'density':'port the pinned photon/baryon equations in curvature-dressed D_i so the common metric_continuity term cancels exactly at constant w',
        'momentum':'preserve pinned thermodynamic R, cb2, tau_c, slip and shear coefficients; replace metric_euler by k^2 Phi_N from the certified physical completed metric map',
        'shear':'carry the pinned compromise_CLASS shear/slip correction with the completed shear-aware metric derivative input rather than silently setting preferred B to zero'
      },
      'interpretation':'The missing C10.65 hierarchy port is now source-locked to the exact pinned CLASS compromise_CLASS implementation. This closes ambiguity in the collision/TCA coefficients; it does not yet solve the completed-U1 O(k^2) coefficient rank system.',
      'next_gate':t['next_if_pass'],
      'non_claims':t['non_claims']
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps({'verified_marker_count':len(labels),'hashes':out['audited_source_hashes_sha256']},sort_keys=True))

if __name__=='__main__': main()
