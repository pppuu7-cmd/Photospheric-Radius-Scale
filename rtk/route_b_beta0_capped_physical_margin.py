#!/usr/bin/env python3
"""Source-locked physical-unit margin for the validated Route-B capped hierarchy.

Inputs are read from the frozen validated hierarchy manifest produced from
GitHub Actions run 32322717923. Unit constants are deliberately kept in one
small auditable module:

- Planck length l_P = 1.616255e-35 m, 2022 CODATA/NIST recommended value;
  relative standard uncertainty 1.1e-5.
- 1 au = 149597870700 m exactly, NIST SP 330 table of non-SI units accepted
  for use with SI, reflecting the IAU 2012 redefinition.
- parsec convention: 1 pc = (648000/pi) au; 1 Mpc = 1e6 pc.

For the conditional beta=0 branch, the measured reduced Newton scale is
Mbar_N = (8 pi G_N)^(-1/2), hence in inverse-length units
Mbar_N = 1/(sqrt(8 pi) l_P).
"""
import json, math, pathlib

LP_M = 1.616255e-35
LP_REL_STD_UNC = 1.1e-5
AU_M = 149_597_870_700.0
PC_M = AU_M * 648000.0 / math.pi
MPC_M = 1.0e6 * PC_M
MBAR_N_PER_M = 1.0/(math.sqrt(8.0*math.pi)*LP_M)
MBAR_N_PER_MPC = MBAR_N_PER_M * MPC_M

manifest_path=pathlib.Path('research/route_b/RTK_ROUTE_B_CURRENT_BETA0_CAPPED_HIERARCHY_PASS.json')
m=json.loads(manifest_path.read_text())
assert m['classification']=='RTK_ROUTE_B_CURRENT_BETA0_CAPPED_HIERARCHY_PASS'
assert m['route_b_run_id']==32322717923
assert m['objective_fingerprint']=='754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666'

rows={}
for eps,v in m['worst_capped_hierarchy'].items():
    MK=float(v['Mdisp_MK_per_Mpc'])
    req=float(v['required_MbarN_over_MK'])
    actual=MBAR_N_PER_MPC/MK
    margin=actual/req
    # A 1.1e-5 relative standard uncertainty in l_P is utterly negligible
    # compared with the >1e44 dimensionless hierarchy margin; still record a
    # conservative one-sigma-lower value because Mbar_N ∝ 1/l_P.
    lower_1sigma=margin/(1.0+LP_REL_STD_UNC)
    assert actual>req
    assert lower_1sigma>1e40
    rows[eps]={
      'z':v['z'],'M_K_per_Mpc':MK,
      'required_MbarN_over_MK':req,
      'physical_MbarN_per_Mpc':MBAR_N_PER_MPC,
      'physical_MbarN_over_MK':actual,
      'safety_margin':margin,
      'log10_safety_margin':math.log10(margin),
      'one_sigma_lower_safety_margin':lower_1sigma,
    }

out={
  'classification':'RTK_ROUTE_B_BETA0_CAPPED_PHYSICAL_MARGIN_PASS',
  'source_hierarchy_run_id':m['route_b_run_id'],
  'source_hierarchy_artifact':m['artifact'],
  'unit_sources':{
    'planck_length_m':LP_M,
    'planck_length_relative_standard_uncertainty':LP_REL_STD_UNC,
    'planck_length_source':'NIST 2022 CODATA recommended values',
    'astronomical_unit_m':int(AU_M),
    'astronomical_unit_exact':True,
    'astronomical_unit_source':'NIST SP 330, non-SI units accepted for use with SI; IAU 2012 definition',
    'parsec_convention':'pc=(648000/pi) au',
  },
  'derived':{
    'pc_m':PC_M,'Mpc_m':MPC_M,'Mbar_N_per_Mpc':MBAR_N_PER_MPC,
  },
  'margins':rows,
  'interpretation':'Under the conditional beta=0 normalization and alpha=1e-7/ell=1e-2 benchmark caps, the measured-Newton hierarchy exceeds the validated strong-coupling requirement by more than 1e44 over the frozen accuracy targets. This closes the numerical hierarchy concern only within those assumptions.',
  'guards':['beta=0 conditional','benchmark low-energy caps are not a generic matter-coupling theorem','does not establish compact-object UV regularity','does not establish radiative stability, matter Lorentz safety, nonlinear DOF closure, or off-shell source equivalence']
}
print('RTK_ROUTE_B_BETA0_CAPPED_PHYSICAL_MARGIN_PASS',json.dumps(out,sort_keys=True))
