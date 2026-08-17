#!/usr/bin/env python3
"""Fail-closed source audit for the minimal causal RT auxiliary-field initial data.

This is an implementation/reproducibility invariant, not a full nonlinear DOF theorem.
It expects the pinned nonlocal CLASS tree after
upgrade_rtk_nonlocal_initial_conditions.py has been applied.
"""
from pathlib import Path
import json, re, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
input_c=(root/'source/input.c').read_text()
pert_c=(root/'source/perturbations.c').read_text()
bg_c=(root/'source/background.c').read_text()
bg_h=(root/'include/background.h').read_text()

checks={}
def require(name, cond, detail):
    if not cond:
        raise SystemExit(f'RTK_RETARDED_AUX_IC_AUDIT_FAIL {name}: {detail}')
    checks[name]=True

# Background minimal homogeneous solution must be explicit, exactly once each
# in the audited input block. This removes dependence on uninitialized storage.
for field in ('U_ini_nlde','U_prime_ini_nlde','V_ini_nlde','V_prime_ini_nlde'):
    pat=rf'pba->{field}\s*=\s*0\.;'
    require('background_'+field, len(re.findall(pat,input_c))==1,
            f'expected exactly one explicit {field}=0 assignment')

require('no_duplicate_Uprime_background_ic',
        len(re.findall(r'pba->U_prime_ini_nlde\s*=\s*0\.;',input_c))==1,
        'upstream copy/paste duplicate U_prime assignment must be removed')
require('Vprime_declared', 'double V_prime_ini_nlde' in bg_h,
        'V_prime_ini_nlde must be an explicit background field')
require('Vprime_consumed_by_background',
        'pba->V_prime_ini_nlde' in bg_c and 'index_bi_V_prime_nlde' in bg_c,
        'background evolution must consume the explicitly initialized V prime')

# The adiabatic nonlocal perturbation IC block in the pinned implementation
# fixes localized auxiliary perturbations to zero. Check all RT/model-2 slots.
patterns={
 'deltaU':'index_pt_deltaU_nlde',
 'deltaUprime':'index_pt_deltaU_prime_nlde',
 'deltaV':'index_pt_deltaV_nlde',
 'deltaVprime':'index_pt_deltaV_prime_nlde',
 'deltaZ':'index_pt_deltaZ_nlde',
 'deltaZprime':'index_pt_deltaZ_prime_nlde',
}
for name,index in patterns.items():
    # Accept whitespace and integer/float zero spellings, but require a direct
    # assignment in perturbations.c to the relevant perturbation vector slot.
    pat=rf'\[{re.escape(index)}\]\s*=\s*0(?:\.0*)?\s*;'
    require('perturbation_'+name+'_zero', bool(re.search(pat,pert_c)),
            f'missing explicit zero assignment for {index}')

# Z auxiliaries belong to the RT/model-2 branch in this pinned implementation;
# require that the source contains the model-2 condition near their IC use.
for index in ('index_pt_deltaZ_nlde','index_pt_deltaZ_prime_nlde'):
    pos=pert_c.find(index)
    require('rt_model2_context_'+index, pos>=0 and 'model == 2.' in pert_c[max(0,pos-1200):pos+300],
            f'{index} not found in expected model==2 context')

result={
 'classification':'RTK_RETARDED_AUX_IC_IMPLEMENTATION_PASS',
 'background_zero_fields':['U','U_prime','V','V_prime'],
 'perturbation_zero_fields':['deltaU','deltaU_prime','deltaV','deltaV_prime','deltaZ','deltaZ_prime'],
 'model':'RT/model=2',
 'claim_boundary':'implementation-level minimal causal auxiliary IC invariant; not a full nonlinear RT physical-DOF proof',
 'checks':sorted(checks),
}
print('RTK_RETARDED_AUX_IC_AUDIT_PASS',json.dumps(result,sort_keys=True))
