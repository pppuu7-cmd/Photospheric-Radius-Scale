#!/usr/bin/env python3
"""Evaluate long-wave P(X) interaction ratios for the DBI-Khronon background.

Inputs are the physical closure parameters used by khronon_background.c.
This is a conditional Route-A1/P(X) diagnostic, not a full RTK cutoff theorem.
The reported Lambda_i values are canonical coefficient-suppression proxies for
D3 operators only; they are explicitly not identified with the physical strong-
coupling cutoff because small-c_s/dispersive D4/D5 effects remain open.
"""
import argparse, json, math

# Fixed unit conventions used only for the coefficient proxies.
MPC_M=3.0856775814913673e22
HBARC_EV_M=1.973269804e-7
INV_MPC_EV=HBARC_EV_M/MPC_M
MPL_REDUCED_EV=2.435e27

p=argparse.ArgumentParser()
p.add_argument('--gamma',type=float,required=True)
p.add_argument('--lambda-D',dest='lam',type=float,required=True)
p.add_argument('--Omega-K0',dest='Om',type=float,required=True)
p.add_argument('--H0',type=float,required=True,help='CLASS H0 in 1/Mpc')
a=p.parse_args()
if not (a.gamma>0 and a.lam>0 and a.Om>0 and a.H0>0):
    raise SystemExit('positive parameters required')

A=a.Om/(6*a.gamma)
D=1+2*A+a.lam*A*A
x0=A*(2+a.lam*A)/(1+a.lam*A+math.sqrt(D))
mu=3*a.H0*math.sqrt(a.gamma)
H0_eV=a.H0*INV_MPC_EV

def vals(scale):
    x=x0/scale**3
    s=math.hypot(1.0,math.sqrt(a.lam)*x)
    r=x/s
    t=x/(s+1.0)
    G=2*mu*mu*(x*(1+t)+r*t)
    ca2=r/(s*(s+x))
    K=G/ca2
    # c2=-(K-G)/2 exactly.
    c2_over_K=-0.5*(1-G/K)
    # c1/K=[(d ln K/d ln x)/(2 ca2)-1]/3.
    # Evaluate d ln K/d ln x with a symmetric log derivative; the exact
    # thermodynamic identity and its dust-limit asymptotics are proved
    # symbolically by quantum_route_a1_px_reconstruction.py.
    eps=1e-5
    def kval(xx):
        ss=math.hypot(1.0,math.sqrt(a.lam)*xx)
        rr=xx/ss; tt=xx/(ss+1.0)
        GG=2*mu*mu*(xx*(1+tt)+rr*tt)
        cc=rr/(ss*(ss+xx))
        return GG/cc
    kp=kval(x*math.exp(eps)); km=kval(x*math.exp(-eps))
    dlnK=(math.log(kp)-math.log(km))/(2*eps)
    c1_over_K=(dlnK/(2*ca2)-1)/3
    rho=2*mu*mu*x*(1+t); pr=2*mu*mu*r*t
    w=pr/rho
    Q=1+r
    MK=mu*Q*s*math.sqrt(s)

    # For a spatially homogeneous long-wave fluctuation, all D4/D5 spatial
    # vertices vanish and the Route-A1/P(X) velocity Hessian is K+6*c1*dot(pi).
    # The symmetric sufficient positivity region is therefore
    # |dot(pi)| < 1/(6|c1/K|). This is a dimensionless Legendre-map radius,
    # NOT an energy cutoff and NOT a statement about the mapping of CLASS fluid
    # perturbations to pi.
    homogeneous_safe_abs_dotpi=1.0/(6.0*abs(c1_over_K))

    # Code K is 8*pi*G times the physical kinetic density, with units Mpc^-2.
    # K_phys=Mpl_bar^2*K. For L3=c_i O_i and chi=sqrt(K_phys)*pi,
    # coefficient 1/Lambda_i^2=|c_i,phys|/K_phys^(3/2), hence
    # Lambda_i^2=Mpl_bar*sqrt(K_8piG)/|c_i/K|.
    sqrtK_eV=math.sqrt(K)*INV_MPC_EV
    lambda1_eV=math.sqrt(MPL_REDUCED_EV*sqrtK_eV/abs(c1_over_K))
    lambda2_eV=math.sqrt(MPL_REDUCED_EV*sqrtK_eV/abs(c2_over_K))
    return {'a':scale,'z':1/scale-1,'x':x,'w':w,'ca2':ca2,
            'K_over_H0sq':K/(a.H0*a.H0),
            'c1_over_K':c1_over_K,'c2_over_K':c2_over_K,
            'ca2_times_c1_over_K':ca2*c1_over_K,
            'homogeneous_safe_abs_dotpi':homogeneous_safe_abs_dotpi,
            'homogeneous_safe_abs_dotpi_over_ca2':homogeneous_safe_abs_dotpi/ca2,
            'Lambda1_D3_coefficient_proxy_eV':lambda1_eV,
            'Lambda2_D3_coefficient_proxy_eV':lambda2_eV,
            'Lambda1_over_H0':lambda1_eV/H0_eV,
            'Lambda2_over_H0':lambda2_eV/H0_eV,
            'M_K_over_H0':MK/a.H0,'dbi_margin':1/(s*s)}

scales=[1.0,0.8,0.67,0.5,1/3,0.2,0.1,0.01,0.001]
rows=[vals(s) for s in scales]
out={'classification':'RTK_ROUTE_A1_BACKGROUND_RATIOS_COMPLETE',
     'gamma':a.gamma,'lambda_D':a.lam,'Omega_K0':a.Om,'H0_class':a.H0,
     'H0_eV':H0_eV,'x0':x0,'mu_over_H0':mu/a.H0,'rows':rows,
     'proxy_conventions':{'reduced_Planck_mass_eV':MPL_REDUCED_EV,
                          'inverse_Mpc_eV':INV_MPC_EV,
                          'Lambda_i_definition':'Lambda_i^2=Mpl_bar*sqrt(K_8piG)/abs(c_i/K)',
                          'homogeneous_legendre_radius':'abs(dot(pi)) < 1/(6 abs(c1/K))'},
     'interpretation_boundary':{
       'D3_longwave_only':True,
       'c3_c4_known':False,
       'finite_k_completion_reconstructed':False,
       'full_strong_coupling_cutoff_known':False,
       'homogeneous_safe_dotpi_is_not_energy_cutoff':True,
       'fluid_to_pi_mapping_established':False,
       'Lambda1_Lambda2_are_not_declared_cutoffs':True,
       'M_K_is_not_declared_cutoff':True}}
print('RTK_ROUTE_A1_BACKGROUND_RATIOS_COMPLETE',json.dumps(out,sort_keys=True))
