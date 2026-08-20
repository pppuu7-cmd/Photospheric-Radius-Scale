#!/usr/bin/env python3
"""State-point RTK -> rational-pole/BPS scale dictionary.

This script mirrors the production Khronon background formulas exactly and
turns a solved positive CLASS gamma into the physical target parameters used by
the Route-B BPS inverse theorem:

  C(a)     = c_a^2(a),
  Mdisp(a) = M_K(a),
  k_*(a)   = a M_K(a),

because production uses

  c_s^2(k,a) = c_a^2(a)/[1 + (k/k_*)^2]
             = C(a)/[1 + (p/Mdisp)^2],  p=k/a.

No Planck-unit conversion is needed here.  For a requested finite-range
accuracy epsilon and physical p_max, the script reports the *required*
dimensionless hierarchy M_P/M_K > threshold implied by the exact unconstrained
BPS cutoff theorem.  A later convention audit may compare that requirement to
a numerical Planck hierarchy without contaminating this dictionary gate.
"""
import argparse,json,math


def closure(H0,gamma,lambda_D,Omega_K0):
    if not (H0>0 and gamma>0 and lambda_D>0 and Omega_K0>0):
        raise ValueError('positive H0,gamma,lambda_D,Omega_K0 required')
    muK=3.0*H0*math.sqrt(gamma)
    A=Omega_K0/(6.0*gamma)
    if abs(lambda_D-1.0)<64.0*2.220446049250313e-16:
        x0=A*(A+2.0)/(2.0*(A+1.0))
    else:
        D=1.0+2.0*A+lambda_D*A*A
        rootD=math.sqrt(D)
        x0=A*(2.0+lambda_D*A)/(1.0+lambda_D*A+rootD)
    if not (muK>0 and x0>0 and math.isfinite(muK) and math.isfinite(x0)):
        raise ValueError('nonphysical closure')
    return muK,x0


def state_at_a(muK,x0,lambda_D,a):
    x=x0/(a*a*a)
    s=math.hypot(1.0,math.sqrt(lambda_D)*x)
    r=x/s
    Q=1.0+r
    ca2=r/(s*(s+x))
    MK=muK*Q*s*math.sqrt(s)
    kstar=a*MK
    if not (0<ca2 and MK>0 and kstar>0):
        raise ValueError('nonphysical state')
    return {'a':a,'x':x,'s':s,'r':r,'Q':Q,'C_ca2':ca2,'Mdisp_MK':MK,'kstar':kstar}


def fmax(C):
    if C<=0:
        raise ValueError('C must be positive')
    if C<=1.0/3.0:
        return math.sqrt(2.0*(1.0-C)/(1.0+3.0*C))
    return (16.0/(27.0*C*(3.0*C+1.0)**2))**0.25


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--gamma',type=float,required=True)
    ap.add_argument('--H0',type=float,required=True,help='CLASS H0 in 1/Mpc (100 h/c)')
    ap.add_argument('--lambda-D',type=float,required=True)
    ap.add_argument('--Omega-K0',type=float,required=True)
    ap.add_argument('--h-reduced',type=float,required=True)
    ap.add_argument('--z-grid',required=True,help='comma-separated production redshifts')
    ap.add_argument('--pmax-h-mpc',type=float,default=5.0,help='production comoving P_k_max in h/Mpc')
    ap.add_argument('--epsilons',default='1e-2,1e-3,1e-4')
    args=ap.parse_args()
    zs=[float(x) for x in args.z_grid.split(',') if x.strip()]
    eps=[float(x) for x in args.epsilons.split(',') if x.strip()]
    if not zs or any(z<0 for z in zs): raise SystemExit('invalid z grid')
    if any(not (0<e<1) for e in eps): raise SystemExit('epsilons must lie in (0,1)')
    muK,x0=closure(args.H0,args.gamma,args.lambda_D,args.Omega_K0)
    kmax_comoving=args.pmax_h_mpc*args.h_reduced # 1/Mpc
    rows=[]
    for z in zs:
        a=1.0/(1.0+z)
        r=state_at_a(muK,x0,args.lambda_D,a)
        C=r['C_ca2']; MK=r['Mdisp_MK']; F=fmax(C)
        pmax=kmax_comoving/a
        pmax_over_MK=pmax/MK
        req={}
        for e in eps:
            preq_over_MK=max(1.0,pmax_over_MK*e**(-1.0/6.0))
            req[format(e,'.0e')]={
                'p_req_over_MK':preq_over_MK,
                'required_MP_over_MK_unconstrained':preq_over_MK/F,
            }
        r.update({
            'z':z,'pmax_physical_per_Mpc':pmax,'pmax_over_MK':pmax_over_MK,
            'Fmax_unconstrained':F,'requirements':req
        })
        rows.append(r)
    worst={}
    for e in eps:
        key=format(e,'.0e')
        row=max(rows,key=lambda q:q['requirements'][key]['required_MP_over_MK_unconstrained'])
        worst[key]={
            'z':row['z'],
            'required_MP_over_MK_unconstrained':row['requirements'][key]['required_MP_over_MK_unconstrained'],
            'p_req_over_MK':row['requirements'][key]['p_req_over_MK'],
            'C_ca2':row['C_ca2'],'Mdisp_MK':row['Mdisp_MK']
        }
    out={
      'classification':'RTK_ROUTE_B_SCALE_DICTIONARY_PASS',
      'dictionary':{'C':'c_a^2(a)','Mdisp':'M_K(a)','kstar':'a M_K(a)','physical_p':'k/a'},
      'inputs':vars(args),
      'closure':{'muK':muK,'x0':x0},
      'kmax_comoving_per_Mpc':kmax_comoving,
      'rows':rows,
      'worst_unconstrained_hierarchy':worst,
      'interpretation':'Thresholds are requirements on M_P/M_K only; this gate intentionally does not assign a numerical M_P convention or observational alpha/ell caps.',
      'guards':['gamma must come from the same positive CLASS root as the frozen current center','P_k_max is a coverage choice, not an observational bound','unconstrained BPS cutoff only; use constrained theorem once alpha/ell caps are sourced','no off-shell/radiative/nonlinear equivalence claim']
    }
    print('RTK_ROUTE_B_SCALE_DICTIONARY_PASS',json.dumps(out,sort_keys=True))

if __name__=='__main__': main()
