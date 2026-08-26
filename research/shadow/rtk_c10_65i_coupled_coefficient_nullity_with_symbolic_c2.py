#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path

import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_TARGET_v1.json'

CORE_FIXED=[
    'D_b0','D_g0','D_ur0','delta_khr0',
    'D_b2','D_g2','D_ur2','delta_khr2',
    'Q_pref0','R_gb0','R_urb0','R_kb0','S_ur0'
]
AUX=['psi_pref0','psi_pref_prime0','phi_pref0','B0','S_g0']
C2_NAME='C2_matching'

def load(rel):
    return json.loads((ROOT/rel).read_text())

def khr_background(prod,gamma,a):
    c_kms=299792.458
    H0=100.0*float(prod['h'])/c_kms
    lamD=float(prod['lam']); Om=float(prod['Om'])
    mu=3.0*H0*math.sqrt(gamma)
    A=Om/(6.0*gamma)
    if abs(lamD-1.0)<1e-14:
        x0=A*(A+2.0)/(2.0*(A+1.0))
    else:
        root=math.sqrt(1.0+2.0*A+lamD*A*A)
        x0=A*(2.0+lamD*A)/(1.0+lamD*A+root)
    x=x0/(a*a*a)
    s=math.hypot(1.0,math.sqrt(lamD)*x)
    r=x/s; t=x/(s+1.0)
    rho8=2.0*mu*mu*x*(1.0+t)
    p8=2.0*mu*mu*r*t
    rho=rho8/3.0; p=p8/3.0
    return {'H0':H0,'rho':rho,'p':p,'w':p/rho,'W':rho+p,'x0':x0}

def numeric_background(prod,gamma,f65,Mc):
    a=float(f65['exact_anchor']['a_on'])
    H=float(f65['coefficient_pack']['Hc_Mpc_inv'])
    R=float(f65['coefficient_pack']['R'])
    kh=khr_background(prod,gamma,a)
    H0=kh['H0']
    rhob=H0*H0*float(prod['Ob'])/(a*a*a)
    rhog=0.75*R*rhob
    N_ur=3.046
    ur_to_g=N_ur*(7.0/8.0)*(4.0/11.0)**(4.0/3.0)
    rhour=ur_to_g*rhog
    Word=rhob+4.0/3.0*(rhog+rhour)
    Wtot=Word+kh['W']
    A_den=Mc*Mc+4.5*Word
    psi_coeff=np.array([-1.5*rhob/A_den,-1.5*rhog/A_den,-1.5*rhour/A_den],dtype=float)
    return {
        'a':a,'H':H,'R':R,'rhob':rhob,'rhog':rhog,'rhour':rhour,
        'rho_khr':kh['rho'],'p_khr':kh['p'],'w_khr':kh['w'],'W_khr':kh['W'],
        'W_ord':Word,'W_total':Wtot,'A_den':A_den,'psi_coeff':psi_coeff,
        'ur_to_gamma':ur_to_g
    }

def core_matrix(bg):
    A=np.zeros((4,len(CORE_FIXED)),dtype=float)
    A[0,0]=-4.0/3.0; A[0,1]=1.0
    A[1,1]=-1.0; A[1,2]=1.0
    c=bg['psi_coeff']; w=bg['w_khr']
    A[2,0]=-1.0-3.0*c[0]
    A[2,1]=-3.0*c[1]
    A[2,2]=-3.0*c[2]
    A[2,3]=1.0/(1.0+w)
    dm=np.array([bg['rhob'],bg['rhog'],bg['rhour']],dtype=float)+3.0*bg['W_ord']*c
    A[3,0:3]=bg['a']*bg['a']*dm
    A[3,3]=bg['a']*bg['a']*bg['rho_khr']
    A[3,8]=bg['H']
    return A

def normalization_vector(bg):
    v=np.zeros(len(CORE_FIXED),dtype=float)
    v[0]=1.0; v[1]=4.0/3.0; v[2]=4.0/3.0
    psi=float(np.dot(bg['psi_coeff'],v[:3]))
    v[3]=(1.0+bg['w_khr'])*(3.0*psi+1.0)
    dm=(bg['rhob']*v[0]+bg['rhog']*v[1]+bg['rhour']*v[2]
        +3.0*bg['W_ord']*psi+bg['rho_khr']*v[3])
    v[8]=-bg['a']*bg['a']*dm/bg['H']
    return v,psi

def row_normalized_singular_values(A):
    norms=np.linalg.norm(A,axis=1)
    if np.any(norms==0.0):
        raise RuntimeError('zero constraint row')
    B=A/norms[:,None]
    return np.linalg.svd(B,compute_uv=False)

def main():
    t=load('research/theory_targets/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_TARGET_v1.json')
    h=load('research/theory_results/RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_RESULT_v1.json')
    g=load('research/theory_results/RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    d=load('research/theory_results/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1.json')
    c=load('research/theory_results/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_RESULT_v1.json')
    p=load('research/theory_results/RTK_C10_PREFERRED_METRIC_PROJECTOR_API_RESULT_v1.json')
    khr=load('research/theory_results/RTK_C10_PREFERRED_KHRONON_ACTION_FLUID_EVOLUTION_RESULT_v1.json')
    protocol=load('research/theory_results/RTK_C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json')
    state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert h['classification']=='C10_65H_C2_GAUGE_INVARIANT_MINIMAL_SHIFT_MATCH_COORDINATE_PASS_SCOPED'
    assert g['classification']=='C10_65G_FINITE_ONSET_SNAPSHOT_RANK_INSUFFICIENT_TEMPORAL_MATCH_REQUIRED_SCOPED'
    assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    assert d['classification']=='C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED'
    assert c['classification']=='C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_PASS_SCOPED'
    assert p['classification']=='C10_PREFERRED_METRIC_PROJECTOR_API_PASS_SCOPED'
    assert khr['classification']=='C10_PREFERRED_KHRONON_ACTION_FLUID_EVOLUTION_PASS_SCOPED'
    assert protocol['classification']=='C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_PASS_SCOPED'
    assert src['classification']=='C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS'

    Hs,ws=sp.symbols('H w', positive=True)
    nb,ng,nu,cb,cg,cu,ck=sp.symbols('nb ng nu cb cg cu ck')
    M=sp.zeros(4,len(CORE_FIXED))
    M[0,0]=-sp.Rational(4,3); M[0,1]=1
    M[1,1]=-1; M[1,2]=1
    M[2,0]=nb; M[2,1]=ng; M[2,2]=nu; M[2,3]=1/(1+ws)
    M[3,0]=cb; M[3,1]=cg; M[3,2]=cu; M[3,3]=ck; M[3,8]=Hs
    minor=sp.simplify(M[:,[1,2,3,8]].det())
    assert sp.simplify(minor-Hs/(1+ws))==0

    n=len(CORE_FIXED); m=len(AUX)
    Gr=sp.Matrix([[sp.Rational((i+1)*(j+2),97) for j in range(n)] for i in range(m)])
    Ar=sp.Matrix([[sp.Rational(int(i==j),1) if j<4 else 0 for j in range(n)] for i in range(4)])
    Full=Ar.row_join(sp.zeros(4,m)).col_join((-Gr).row_join(sp.eye(m)))
    assert Full.rank()==Ar.rank()+m
    assert (n+m)-Full.rank()==n-Ar.rank()

    prod=state['final_replay_result']['rtk']['params']
    gamma=float(src['provenance']['gamma_root'])
    unique_points=[]; seen=set()
    for q in protocol['points']:
        key=(float(q['lambda_HL']),float(q['M_c_Mpc_inv']))
        if key in seen: continue
        seen.add(key); unique_points.append(key)

    records=[]; all_rank=True; max_norm_res=0.0
    min_A_den=float('inf'); min_filter=float('inf'); min_lapse=float('inf'); min_shift=float('inf')
    min_velocity_det=float('inf')
    kseed=min(float(x) for x in f['exact_anchor']['k_Mpc_inv'])
    Eth=2.0
    for lam,Mc in unique_points:
        bg=numeric_background(prod,gamma,f,Mc)
        A=core_matrix(bg)
        sv=row_normalized_singular_values(A)
        rank=int(np.linalg.matrix_rank(A/np.linalg.norm(A,axis=1)[:,None],tol=1e-11))
        null_fixed=len(CORE_FIXED)-rank
        null_fixed_norm=null_fixed-1
        null_released=(len(CORE_FIXED)+1)-rank
        null_released_norm=null_released-1
        vnorm,psi=normalization_vector(bg)
        res=A@vnorm
        maxres=float(np.max(np.abs(res)))
        max_norm_res=max(max_norm_res,maxres)
        if rank!=4 or null_fixed_norm!=8 or null_released_norm!=9:
            all_rank=False

        r=lam-1.0; D=3.0*lam-1.0; L=-(kseed*kseed)
        filter_den=kseed*kseed+bg['a']*bg['a']*Mc*Mc
        lapse_den=r*Eth*L-2.0*D*bg['H']*bg['H']
        shift_den=r*L
        vdet=bg['W_total']
        min_A_den=min(min_A_den,bg['A_den'])
        min_filter=min(min_filter,abs(filter_den))
        min_lapse=min(min_lapse,abs(lapse_den))
        min_shift=min(min_shift,abs(shift_den))
        min_velocity_det=min(min_velocity_det,abs(vdet))
        records.append({
            'lambda_HL':lam,'M_c_Mpc_inv':Mc,'rank_core_fixed_C2':rank,
            'nullity_core_fixed_C2_before_normalization':null_fixed,
            'nullity_core_fixed_C2_after_normalization':null_fixed_norm,
            'nullity_core_released_C2_before_normalization':null_released,
            'nullity_core_released_C2_after_normalization':null_released_norm,
            'row_normalized_singular_values':[float(x) for x in sv],
            'normalization_vector_max_abs_residual':maxres,
            'normalization_psi_pref0':psi,
            'guards':{
                'A_dressed_denominator':bg['A_den'],
                'finite_k_filter_denominator':filter_den,
                'finite_k_lapse_denominator':lapse_den,
                'finite_k_shift_denominator':shift_den,
                'velocity_coordinate_jacobian_det_proportional_W_total':vdet
            }
        })

    assert all_rank
    assert max_norm_res<1e-10
    assert min_A_den>0 and min_filter>0 and min_lapse>0 and min_shift>0 and min_velocity_det>0

    fixed_null_basis=[
        {'name':'overall_adiabatic_normalization','classification':'normalization',
         'coordinates':'D_b0=1,D_g0=4/3,D_ur0=4/3; delta_khr0 and Q_pref0 solved by DeltaI=0 and C0=0'},
        {'name':'D_b2','classification':'unresolved temporal branch / O(k^2) ordinary density-gradient amplitude'},
        {'name':'D_g2','classification':'unresolved temporal branch / O(k^2) photon-baryon entropy-gradient content'},
        {'name':'D_ur2','classification':'unresolved temporal branch / O(k^2) UR entropy-gradient content'},
        {'name':'delta_khr2','classification':'unresolved temporal branch / O(k^2) neutral relative-charge/entropy-gradient content'},
        {'name':'R_gb0','classification':'unresolved temporal branch / photon-baryon relative-velocity amplitude'},
        {'name':'R_urb0','classification':'unresolved temporal branch / UR-baryon relative-velocity amplitude'},
        {'name':'R_kb0','classification':'unresolved temporal branch / neutral-preferred versus baryon relative-velocity amplitude'},
        {'name':'S_ur0','classification':'hierarchy/multipole / massless-UR shear amplitude'}
    ]
    after_norm=fixed_null_basis[1:]
    released_extra={
        'name':'C2_matching','classification':'matching coordinate, not propagating mode',
        'core_change':'zero','auxiliary_response':'delta B0 = delta C2/(2H), with psi_pref0 and phi_pref0 fixed','source':'C10.65h'
    }

    cls='C10_65I_COUPLED_COEFFICIENT_NULLITY_REMAINING_TEMPORAL_AMPLITUDES_8_SCOPED'
    out={
      'schema':'RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_RESULT_v1',
      'gate':'C10.65i','classification':cls,
      'target':'research/theory_targets/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_TARGET_v1.json',
      'ordered_amplitude_ledger':{
        'physical_interface_before_reparameterization':[
          'D_b0','D_g0','D_ur0','delta_khr0','D_b2','D_g2','D_ur2','delta_khr2',
          'V_b0','V_g0','V_ur0','V_khr0','S_ur0'
        ],
        'core_after_invertible_velocity_reparameterization':CORE_FIXED,
        'velocity_reparameterization':{
          'relative_coordinates':['R_gb0=V_g0-V_b0','R_urb0=V_ur0-V_b0','R_kb0=V_khr0-V_b0'],
          'aggregate':'Q_pref0 replaces one common velocity combination after the algebraic B0 projection',
          'jacobian':'proportional to W_total>0; hence the change of coordinates is invertible on the frozen onset branch'
        },
        'algebraic_auxiliaries_eliminated':AUX,
        'derivative_outputs_not_counted_as_constraints':'all local continuity/Euler/UR/neutral derivatives d=Fz, including quantities entering compromise_CLASS slip/shear and psi_pref_prime0',
        'released_matching_extension':CORE_FIXED+[C2_NAME]
      },
      'independent_algebraic_constraints':[
        {'name':'ordinary_entropy_gb0','equation':'D_g0-(4/3)D_b0=0','provenance':'C10.65i frozen target / ordinary adiabatic leading branch'},
        {'name':'ordinary_entropy_ur0','equation':'D_ur0-D_g0=0','provenance':'C10.65i frozen target / ordinary adiabatic leading branch'},
        {'name':'neutral_common_curvature','equation':'delta_khr0/(1+w_khr)-3 psi_pref0-D_b0=0','provenance':'C10.65c; Delta I_iso=0'},
        {'name':'leading_comoving_regularity','equation':'a^2 delta_mu_pref,0+H Q_pref0=0','provenance':'C10.54/C10.55 finite-B regularity'}
      ],
      'auxiliary_elimination':{
        'rule':'psi_pref0, psi_pref_prime0, phi_pref0, B0 and photon S_g0 are uniquely reconstructed outputs; their equations have an identity block in auxiliary columns and do not reduce core nullity',
        'psi_pref0':'dressed ordinary-only A constraint','psi_pref_prime0':'differentiated dressed A output after d=Fz is evaluated',
        'phi_pref0':'Hamiltonian output with nonzero lapse denominator','B0':'(C2+2 Pcal psi0-E_th phi0)/(2H)',
        'S_g0':'source-locked compromise_CLASS TCA shear closure; no independent photon shear amplitude'
      },
      'exact_rank_certificate':{
        'core_variable_count_fixed_C2':len(CORE_FIXED),'core_constraint_count':4,
        'certifying_minor_columns':['D_g0','D_ur0','delta_khr0','Q_pref0'],
        'minor_determinant':'H/(1+w_khr)','guards':['H>0','1+w_khr>0'],'rank_core':4,
        'nullity_fixed_C2_before_normalization':9,'nullity_fixed_C2_after_normalization':8,
        'nullity_released_C2_before_normalization':10,'nullity_released_C2_after_normalization':9,
        'auxiliary_count':len(AUX),'full_pre_elimination_variable_count_fixed_C2':len(CORE_FIXED)+len(AUX),
        'full_pre_elimination_rank_fixed_C2':4+len(AUX),'full_pre_elimination_nullity_fixed_C2':9,
        'block_identity':'[[A,0],[-G,I_aux]] has rank(A)+N_aux and the same nullity as A'
      },
      'null_basis_fixed_C2_before_normalization':fixed_null_basis,
      'null_basis_fixed_C2_after_normalization':after_norm,'released_C2_extra_direction':released_extra,
      'numerical_crosscheck':{
        'k_seed_Mpc_inv':kseed,'record_count':len(records),'records':records,
        'max_normalization_vector_abs_constraint_residual':max_norm_res,
        'minimum_guards':{
          'A_dressed_denominator':min_A_den,'finite_k_filter_abs':min_filter,'finite_k_lapse_abs':min_lapse,
          'finite_k_shift_abs':min_shift,'velocity_reparameterization_abs_det':min_velocity_det
        },
        'background_reconstruction':{
          'N_ur':3.046,'ur_to_gamma_density_ratio':numeric_background(prod,gamma,f,unique_points[0][1])['ur_to_gamma'],
          'gamma_root':gamma,'onset_a':float(f['exact_anchor']['a_on']),
          'Hc_Mpc_inv':float(f['coefficient_pack']['Hc_Mpc_inv']),'R_4rho_gamma_over_3rho_b':float(f['coefficient_pack']['R'])
        }
      },
      'scientific_interpretation':{
        'leading_sector':'After the two ordinary entropy conditions, corrected neutral common-curvature condition and finite-B comoving regularity, the leading k^0 seed has exactly one direction: overall normalization.',
        'subleading_sector':'Snapshot algebra leaves eight independent O(k^2)/velocity/shear amplitudes after normalization even when C2 is fixed. These are temporal-branch data, not extra propagating DOF claims.',
        'C2':'Releasing C2 adds exactly one boundary/matching direction; its core state change is zero and B0 responds by delta C2/(2H).',
        'TCA':'The source-locked compromise_CLASS closure removes photon shear as an auxiliary but does not identify theta_gamma with theta_b or reduce the dynamic velocity nullity.',
        'consequence':'A temporal gradient-recursion/eigenbranch or microscopic pre-EFT matching condition is required before a unique completed-U1 seed can be built.'
      },
      'next_gate':'freeze C10.65j temporal gradient-recursion/eigenbranch contract: use the actual ODE hierarchy as a time-evolution/series recursion (not snapshot constraints) to determine whether the eight fixed-C2 subleading amplitudes are uniquely slaved to normalization and C2 on a regular growing branch; preserve C2 as external until a UV prescription is justified',
      'non_claims':t['non_claims']
    }
    outp=ROOT/'research/theory_results/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_RESULT_v1.json'
    outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'fixed_C2_nullity_after_normalization':8,'released_C2_nullity_after_normalization':9,'record_count':len(records),'min_shift_abs':min_shift,'max_norm_res':max_norm_res},sort_keys=True))

if __name__=='__main__':
    main()
