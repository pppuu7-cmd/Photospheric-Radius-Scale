#!/usr/bin/env python3
"""Replay-state RTK -> beta=0 fixed-G_N BPS hierarchy with low-energy caps.

This composes three independently guarded ingredients:
  1. production RTK scale dictionary C(a)=c_a^2(a), Mdisp=M_K(a), p=k/a;
  2. exact beta=0 fixed-measured-Newton BPS cutoff;
  3. exact alpha/ell cap inversion.

The default alpha_cap=1e-7 and ell_cap=1e-2 are a sourced *benchmark* for the
generic low-energy branch.  They are not promoted here into a generic matter
coupling theorem: beta=0 remains an explicit conditional choice.
"""
import argparse,json,math
from route_b_rtk_scale_dictionary import closure,state_at_a


def h0_newton(C):
    if not C>0: raise ValueError('C>0 required')
    if C<=0.2:
        return 3.0*(1.0-C)/4.0
    return (1.0-9.0*C+math.sqrt(81.0*C*C+30.0*C+1.0))/4.0


def capped_point(C,alpha_cap,ell_cap):
    if not (C>0 and 0<alpha_cap<2 and ell_cap>0):
        raise ValueError('invalid positive domain')
    h_alpha=3.0*alpha_cap*C/(2.0-alpha_cap)
    h_ell=3.0*ell_cap/(2.0+3.0*ell_cap)
    h0=h0_newton(C)
    h=min(h0,h_alpha,h_ell)
    if not (0<h<1): raise ValueError('nonphysical h optimum')
    alpha=2.0*h/(3.0*C+h)
    ell=2.0*h/(3.0*(1.0-h))
    if ell<=alpha:
        branch='ell_le_alpha'
        g4=4.0*h*h*(3.0*C+h)**3/(243.0*C*C*(1.0-h)**3)
    else:
        branch='ell_ge_alpha'
        g4=4.0*h*h*(1.0-h)/(3.0*C*C*(3.0*C+h))
    if not g4>0: raise ValueError('nonpositive physical cutoff')
    return {
      'h0_newton':h0,'h_alpha':h_alpha,'h_ell':h_ell,'h_opt':h,
      'active_cap':min((('unconstrained',h0),('alpha',h_alpha),('ell',h_ell)),key=lambda x:x[1])[0],
      'alpha':alpha,'ell':ell,'branch':branch,
      'Lambda_p_over_MbarN':g4**0.25,
    }


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
    ap.add_argument('--alpha-cap',type=float,default=1e-7)
    ap.add_argument('--ell-cap',type=float,default=1e-2)
    args=ap.parse_args()
    zs=[float(x) for x in args.z_grid.split(',') if x.strip()]
    eps=[float(x) for x in args.epsilons.split(',') if x.strip()]
    if len(zs)==0 or any(z<0 for z in zs): raise SystemExit('invalid z grid')
    if any(not (0<e<1) for e in eps): raise SystemExit('invalid epsilon')

    muK,x0=closure(args.H0,args.gamma,args.lambda_D,args.Omega_K0)
    kmax=args.pmax_h_mpc*args.h_reduced
    rows=[]
    for z in zs:
        a=1.0/(1.0+z)
        row=state_at_a(muK,x0,args.lambda_D,a)
        C=row['C_ca2']; MK=row['Mdisp_MK']
        # Production-domain theorem should hold numerically on every replay row.
        if not (0<C<1): raise SystemExit(f'production C outside (0,1) at z={z}: {C}')
        cp=capped_point(C,args.alpha_cap,args.ell_cap)
        # The generic alpha=1e-7, ell>=1e-2 benchmark is analytically alpha-active
        # for all production 0<C<1. Fail closed if the numerical composition disagrees.
        if args.alpha_cap==1e-7 and args.ell_cap>=1e-2:
            if cp['active_cap']!='alpha':
                raise SystemExit(f'expected alpha-active benchmark at z={z}, got {cp["active_cap"]}')
        pmax=(kmax/a); pmax_over_MK=pmax/MK
        requirements={}
        for e in eps:
            preq=max(1.0,pmax_over_MK*e**(-1.0/6.0))
            requirements[format(e,'.0e')]={
              'p_req_over_MK':preq,
              'required_MbarN_over_MK':preq/cp['Lambda_p_over_MbarN'],
            }
        row.update({'z':z,'pmax_physical_per_Mpc':pmax,'pmax_over_MK':pmax_over_MK,
                    'capped':cp,'requirements':requirements})
        rows.append(row)

    worst={}
    for e in eps:
        key=format(e,'.0e')
        r=max(rows,key=lambda q:q['requirements'][key]['required_MbarN_over_MK'])
        worst[key]={
          'z':r['z'],'C_ca2':r['C_ca2'],'Mdisp_MK':r['Mdisp_MK'],
          'Lambda_p_over_MbarN':r['capped']['Lambda_p_over_MbarN'],
          'p_req_over_MK':r['requirements'][key]['p_req_over_MK'],
          'required_MbarN_over_MK':r['requirements'][key]['required_MbarN_over_MK'],
          'active_cap':r['capped']['active_cap'],
        }

    out={
      'classification':'RTK_ROUTE_B_CURRENT_BETA0_CAPPED_HIERARCHY_PASS',
      'scope':'replay-certified RTK state; conditional beta=0 measured-G_N normalization; generic low-energy cap benchmark',
      'inputs':vars(args),'closure':{'muK':muK,'x0':x0},
      'dictionary':{'C':'c_a^2(a)','Mdisp':'M_K(a)','physical_p':'k/a'},
      'rows':rows,'worst_capped_hierarchy':worst,
      'guards':['beta=0 remains conditional','alpha/ell values are benchmark caps, not a generic-matter theorem','required_MbarN_over_MK is a threshold; no numerical Planck-unit conversion is made here','no compact-object/radiative/off-shell/nonlinear-DOF closure claim'],
      'interpretation':'If the physical measured-Newton reduced Planck hierarchy Mbar_N/M_K exceeds the reported threshold at every row, a strict pre-cutoff crossover exists for the requested finite-range accuracy under the previously stated sufficient frequency guard.'
    }
    print('RTK_ROUTE_B_CURRENT_BETA0_CAPPED_HIERARCHY_PASS',json.dumps(out,sort_keys=True))

if __name__=='__main__': main()
