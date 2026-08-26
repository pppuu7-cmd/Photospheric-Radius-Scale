#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp
R=Path(__file__).resolve().parents[2]
def L(p): return json.loads((R/p).read_text())
def main():
 t=L('research/theory_targets/RTK_C10_65L_UV_MATCHING_INTERFACE_BASIS_TARGET_v1.json')
 k=L('research/theory_results/RTK_C10_65K_NONLOCAL_TEMPORAL_SELECTOR_FEASIBILITY_RESULT_v1.json')
 i=L('research/theory_results/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_RESULT_v1.json')
 h=L('research/theory_results/RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_RESULT_v1.json')
 assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
 assert k['classification']=='C10_65K_NO_CERTIFIED_PRE_ONSET_BACKWARD_INTERVAL_UV_MATCH_REQUIRED_SCOPED'
 assert i['classification']=='C10_65I_COUPLED_COEFFICIENT_NULLITY_REMAINING_TEMPORAL_AMPLITUDES_8_SCOPED'
 assert h['classification']=='C10_65H_C2_GAUGE_INVARIANT_MINIMAL_SHIFT_MATCH_COORDINATE_PASS_SCOPED'
 H,B,w,psi,d=sp.symbols('H B w psi d')
 Psi=psi-H*B; dNr=d/(1+w)-3*H*B
 rJ=sp.simplify(dNr-3*Psi-(d/(1+w)-3*psi)); assert rJ==0
 a,W,x,th=sp.symbols('a W x th', nonzero=True)
 qP=a*W*th/x; qN=qP+a*W*B; thN=sp.simplify(x*qN/(a*W))
 rV=sp.simplify(thN-(th+x*B)); assert rV==0
 Db,Dg,Du,dk,pb,pg,pu,opw=sp.symbols('Db Dg Du dk pb pg pu opw')
 ps2=pb*Db+pg*Dg+pu*Du
 prim=sp.Matrix([Db,Dg,Du,dk])
 inv=sp.Matrix([Db,Dg-sp.Rational(4,3)*Db,Du-sp.Rational(4,3)*Db,dk/opw-3*ps2-Db])
 T=inv.jacobian(prim); det=sp.factor(T.det()); assert sp.simplify(det-1/opw)==0
 dmP,qP2=sp.symbols('dmP qP2'); rp=-3*H*W
 dmN=dmP+rp*B; qN2=qP2+a*W*B
 rC=sp.simplify((3*a*a*dmN+9*H*a*qN2)-(3*a*a*dmP+9*H*a*qP2)); assert rC==0
 fixed=int(i['exact_rank_certificate']['nullity_fixed_C2_after_normalization']); rel=int(i['exact_rank_certificate']['nullity_released_C2_after_normalization'])
 assert (fixed,rel)==(8,9)
 cls='C10_65L_UV_MATCHING_INTERFACE_BASIS_PASS_SCOPED'
 out={'schema':'RTK_C10_65L_UV_MATCHING_INTERFACE_BASIS_RESULT_v1','gate':'C10.65l','classification':cls,'target':'research/theory_targets/RTK_C10_65L_UV_MATCHING_INTERFACE_BASIS_TARGET_v1.json','machine_residuals':{'J_gauge':str(rJ),'velocity_bridge':str(rV),'C_source':str(rC)},'density_gradient_basis':{'primitive':['D_b2','D_g2','D_ur2','delta_khr2'],'invariant':['A2','E_gb2','E_urb2','E_khr2'],'jacobian_determinant':str(det),'guard':'1+w_khr>0'},'boundary_vector':[{'name':'A2','definition':'D_b2'},{'name':'E_gb2','definition':'D_g2-(4/3)D_b2'},{'name':'E_urb2','definition':'D_ur2-(4/3)D_b2'},{'name':'E_khr2','definition':'[I_khr-J_b]_O(k^2)'},{'name':'R_gb0','definition':'V_g0-V_b0'},{'name':'R_urb0','definition':'V_ur0-V_b0'},{'name':'R_khrb0','definition':'V_khr,pref0+B0-V_b,N0'},{'name':'S_ur0','definition':'lim sigma_ur/k^2'},{'name':'C2','definition':'[3a^2 delta_mu+3H Q]_O(k^2)'}],'bridges':{'density':'J=delta/(1+w)-3Psi_N=delta_pref/(1+w)-3psi_pref','velocity':'theta_N=theta_pref+k^2 B','neutral_relative_velocity':'V_khr,N-V_b,N=V_khr,pref+B0-V_b,N','C2':'source-coordinate invariant by C10.65h'},'dimension_accounting':{'fixed_C2_temporal':fixed,'C2':1,'total_matching':rel,'overall_normalization_excluded':True},'phenomenological_regular_control':{'zero':['E_gb2','E_urb2','E_khr2','R_gb0','R_urb0','R_khrb0'],'external':['A2','S_ur0','C2'],'status':'DEFINED_NOT_NUMERIC'},'architecture_decision':'Use this invariant basis or a proven invertible equivalent for onset matching; never subtract preferred neutral and Newtonian baryon velocities without the B0 bridge.','next_gate':t['next_if_pass'],'non_claims':t['non_claims']}
 (R/'research/theory_results/RTK_C10_65L_UV_MATCHING_INTERFACE_BASIS_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(cls,json.dumps({'matching_dimension':9,'density_basis_det':str(det)},sort_keys=True))
if __name__=='__main__': main()
