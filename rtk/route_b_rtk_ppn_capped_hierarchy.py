#!/usr/bin/env python3
"""Replay-state Route-B hierarchy under current low-energy PPN/GW caps.

Scenarios:
1. beta=0 current-pointwise PPN cap, using the exact reduction of the 2018
   low-energy Horava ppN condition for the z=0 inverse:
       alpha_max = 2 C0 * 1e-7/(1-C0).
2. PPN-tuned alpha=2 beta plane, with the post-GW170817 benchmark
       |beta|<=1e-15 -> alpha<=2e-15.

The pure-gravity inverse/cutoff is evaluated pointwise on the replay-certified
RTK background. The measured-Newton normalization for modern Horava parameters
uses Mbar_N^2/M_p^2=(1-alpha/2)/(1-beta), following the ADM/Einstein-aether
mapping and G_N formula summarized in arXiv:1711.08845.

Scope guard: beta!=0 changes the matter-frame dispersion map at O(beta), so the
alpha=2 beta scenario is a scale-separation/normalization theorem for the same
pure-gravity inverse, not yet an exact beta!=0 matter-frame rational embedding.
"""
import argparse,json,math
from route_b_rtk_scale_dictionary import closure,state_at_a

PPN_TRANSLATED_BOUND=1e-7
BETA_GW_BENCH=1e-15


def point(C,A,beta):
    h=3.0*A*C/(2.0-A)
    alpha=2.0*h/(3.0*C+h)
    ell=2.0*h/(3.0*(1.0-h))
    if not (0<h<1 and 0<alpha<2 and ell>0): raise ValueError('bad inverse point')
    # For production C<1 and ultratight A, ell<alpha, so low branch applies.
    if not ell<=alpha: raise ValueError('expected low cutoff branch')
    F4=ell**3/alpha
    # M_p/Mbar_N squared, modern Horava ADM convention.
    mp_over_mbar_sq=(1.0-beta)/(1.0-alpha/2.0)
    if mp_over_mbar_sq<=0: raise ValueError('bad Newton normalization')
    G4=F4*mp_over_mbar_sq**2
    return {'h':h,'alpha':alpha,'ell':ell,'beta':beta,
            'Lambda_p_over_MbarN':G4**0.25,
            'Mp_over_MbarN':math.sqrt(mp_over_mbar_sq)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--gamma',type=float,required=True)
    ap.add_argument('--H0',type=float,required=True)
    ap.add_argument('--lambda-D',type=float,required=True)
    ap.add_argument('--Omega-K0',type=float,required=True)
    ap.add_argument('--h-reduced',type=float,required=True)
    ap.add_argument('--z-grid',required=True)
    ap.add_argument('--pmax-h-mpc',type=float,default=5.0)
    ap.add_argument('--epsilons',default='1e-2,1e-3,1e-4')
    ap.add_argument('--MbarN-per-Mpc',type=float,required=True)
    args=ap.parse_args()
    zs=[float(x) for x in args.z_grid.split(',') if x.strip()]
    eps=[float(x) for x in args.epsilons.split(',') if x.strip()]
    if 0.0 not in zs: raise SystemExit('z=0 required for current PPN cap')
    muK,x0=closure(args.H0,args.gamma,args.lambda_D,args.Omega_K0)
    states=[]
    for z in zs:
        a=1/(1+z); row=state_at_a(muK,x0,args.lambda_D,a); row['z']=z; states.append(row)
    z0=next(r for r in states if r['z']==0.0)
    C0=z0['C_ca2']
    if not 0<C0<1: raise SystemExit('bad C0')
    A_beta0=2.0*C0*PPN_TRANSLATED_BOUND/(1.0-C0)
    A_tuned=2.0*BETA_GW_BENCH
    scenarios={
      'beta0_ppn':{'alpha_cap':A_beta0,'beta':0.0,
                   'origin':'current z=0 inverse + translated ppN ~1e-7 bound'},
      'alpha2beta_gw':{'alpha_cap':A_tuned,'beta':BETA_GW_BENCH,
                       'origin':'alpha=2 beta PPN cancellation + |beta|<=1e-15 GW benchmark'}
    }
    kmax=args.pmax_h_mpc*args.h_reduced
    results={}
    for name,sc in scenarios.items():
        rows=[]
        for base in states:
            z=base['z']; a=1/(1+z); C=base['C_ca2']; MK=base['Mdisp_MK']
            q=point(C,sc['alpha_cap'],sc['beta'])
            pmax=kmax/a; pmax_over_MK=pmax/MK
            reqs={}
            for e in eps:
                preq=max(1.0,pmax_over_MK*e**(-1/6))
                threshold=preq/q['Lambda_p_over_MbarN']
                actual=args.MbarN_per_Mpc/MK
                reqs[format(e,'.0e')]={
                    'p_req_over_MK':preq,
                    'required_MbarN_over_MK':threshold,
                    'physical_MbarN_over_MK':actual,
                    'safety_margin':actual/threshold}
            rows.append({'z':z,'C':C,'MK_per_Mpc':MK,'cutoff':q,'requirements':reqs})
        worst={}
        for e in eps:
            key=format(e,'.0e'); r=min(rows,key=lambda x:x['requirements'][key]['safety_margin'])
            worst[key]={'z':r['z'],'C':r['C'],'MK_per_Mpc':r['MK_per_Mpc'],
                        **r['requirements'][key],
                        'Lambda_p_over_MbarN':r['cutoff']['Lambda_p_over_MbarN']}
            if worst[key]['safety_margin']<=1e30: raise SystemExit('insufficient hierarchy margin')
        results[name]={**sc,'worst':worst,'rows':rows}

    # Exact useful identity on tuned plane: beta=alpha/2 makes Mp/Mbar_N=1.
    tuned0=point(C0,A_tuned,BETA_GW_BENCH)
    assert abs(tuned0['Mp_over_MbarN']-1.0)<1e-14

    out={'classification':'RTK_ROUTE_B_CURRENT_PPN_CAPPED_HIERARCHY_PASS',
         'scope':'replay-state pointwise pure-gravity inverse plus low-energy PPN/GW caps; not fixed-action FLRW completion',
         'inputs':vars(args),'closure':{'muK':muK,'x0':x0},
         'current_z0':{'C':C0,'M_K_per_Mpc':z0['Mdisp_MK']},
         'scenarios':results,
         'interpretation':'Replacing alpha=1e-7 by the much tighter current-pointwise PPN/GW O(1e-15) caps still leaves a huge measured-Newton strong-coupling hierarchy margin on all frozen redshifts. This removes strong coupling as the immediate obstruction but does not solve the missing fixed-action FLRW or beta!=0 matter-frame embedding.',
         'guards':['PPN applies to the current asymptotic low-energy solution, not separately to every cosmological epoch','beta!=0 tuned scenario is not yet an exact matter-frame rational-pole matching theorem','higher-spatial compact-object regularity, radiative stability and matter Lorentz percolation remain open']}
    print('RTK_ROUTE_B_CURRENT_PPN_CAPPED_HIERARCHY_PASS',json.dumps(out,sort_keys=True))

if __name__=='__main__': main()
