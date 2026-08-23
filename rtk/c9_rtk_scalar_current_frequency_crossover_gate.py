#!/usr/bin/env python3
"""Current-point ordering of the DBI cubic coefficient scale and RTK frequency cap.

This is NOT a strong-coupling/unitarity-cutoff theorem.  It asks a narrower,
well-defined question on the replay-certified RTK background: at what redshift
does the low-k time-cubic coefficient scale Lambda3_coeff become equal to the
maximum frequency of the exact quadratic rational mode, omega_inf=c_a M_K?

If Lambda3_coeff >> omega_inf, the quadratic mode enters its high-k/frequency-
saturation regime before it can reach the naive low-k coefficient energy scale,
so low-k power counting alone cannot diagnose strong coupling there.
"""
import json, math

# Replay-certified matched-local RTK point.
h=0.691103719964454
OmegaK0=0.2522864064078236
lambdaD=219457.5727136581
gamma=0.05170371280716  # replay-certified current-scale dictionary positive CLASS root

# Same constants/conventions as quantum_route_a1_background_ratios.py.
MPC_M=3.0856775814913673e22
HBARC_EV_M=1.973269804e-7
INV_MPC_EV=HBARC_EV_M/MPC_M
MPL_REDUCED_EV=2.435e27
T_CMB_K=2.7255
KB_EV_K=8.617333262e-5

H0=100.0*h/299792.458
mu=3.0*H0*math.sqrt(gamma)
mu_eV=mu*INV_MPC_EV
A=OmegaK0/(6.0*gamma)
D=1.0+2.0*A+lambdaD*A*A
x0=A*(2.0+lambdaD*A)/(1.0+lambdaD*A+math.sqrt(D))
assert x0>0 and mu>0

# Exact production functions.
def row(z):
    zp1=1.0+z
    x=x0*zp1**3
    s=math.hypot(1.0,math.sqrt(lambdaD)*x)
    r=x/s
    delta=1.0/(s*s)
    ca2=r*delta/(1.0+r)
    MK_mpc=mu*(1.0+r)*s*math.sqrt(s)
    MK_eV=MK_mpc*INV_MPC_EV
    omega_inf=math.sqrt(ca2)*MK_eV
    # Canonical low-k time-cubic coefficient C3t and its dimensional scale.
    C3t=math.sqrt(2.0)*lambdaD*r/(4.0*MPL_REDUCED_EV*mu_eV*delta**0.25)
    Lambda3=1.0/math.sqrt(C3t)
    return {
      'z':z,'x':x,'r':r,'delta':delta,'ca2':ca2,'M_K_Mpc_inv':MK_mpc,
      'omega_inf_eV':omega_inf,'Lambda3_coeff_eV':Lambda3,
      'Lambda3_over_omega_inf':Lambda3/omega_inf
    }

# Current-point identity used by the DBI-edge theorem.
assert abs(lambdaD*x0*x0-144525.6802817155) < 5e-10
r0=row(0.0)
assert abs(r0['ca2']-1.4738358401883835e-8) < 5e-20
assert abs(r0['M_K_Mpc_inv']-1.1681315109161161) < 5e-12

# Ratio is huge through late and standard early-cosmology reference redshifts.
refs=[row(z) for z in [0.0,1100.0,1.0e9]]
assert refs[0]['Lambda3_over_omega_inf']>1e28
assert refs[1]['Lambda3_over_omega_inf']>1e21
assert refs[2]['Lambda3_over_omega_inf']>1e8

# Locate the unique current-point crossing in a deliberately broad logarithmic
# bracket.  This is a numerical evaluation of exact state functions, not a fit.
lo,hi=1.0e9,1.0e15
flo=row(lo)['Lambda3_over_omega_inf']-1.0
fhi=row(hi)['Lambda3_over_omega_inf']-1.0
assert flo>0 and fhi<0
for _ in range(160):
    mid=math.sqrt(lo*hi)
    fm=row(mid)['Lambda3_over_omega_inf']-1.0
    if fm>0: lo=mid
    else: hi=mid
zcross=math.sqrt(lo*hi)
cross=row(zcross)
assert abs(cross['Lambda3_over_omega_inf']-1.0) < 5e-13
Tcross_eV=T_CMB_K*(1.0+zcross)*KB_EV_K

out={
  'classification':'RTK_C9_RTK_SCALAR_CURRENT_FREQUENCY_CROSSOVER_PASS',
  'status_scope':'GREEN_CURRENT_POINT_KINETIC_ORDERING_TRUE_UNITARITY_CUTOFF_PENDING',
  'frozen_point':{
    'h':h,'Omega_K0':OmegaK0,'lambda_D':lambdaD,'gamma':gamma,
    'x0':x0,'mu_K_Mpc_inv':mu,'lambda_D_x0_squared':lambdaD*x0*x0
  },
  'definitions':{
    'delta_z':'1/[1+lambda_D x0^2(1+z)^6]',
    'omega_infinity':'c_a M_K, the k->infinity frequency limit of omega^2=c_a^2 k^2/(1+k^2/M_K^2)',
    'Lambda3_coeff':'|C_dotpi^3|^(-1/2) from the low-k canonically normalized DBI P(X) cubic'
  },
  'reference_rows':refs,
  'crossing':{
    'z':zcross,
    'T_CMB_scaled_eV':Tcross_eV,
    'T_CMB_scaled_GeV':Tcross_eV/1e9,
    'row':cross
  },
  'interpretation':'For z below the crossing, Lambda3_coeff exceeds the entire quadratic mode frequency range. Therefore the mode reaches the dispersive/high-k normalization regime before the naive low-k cubic coefficient scale, so that coefficient cannot by itself be called the physical strong-coupling cutoff. The ordering reverses only at an extremely early current-point epoch near the reported crossing, where a full Lifshitz/amplitude analysis is mandatory.',
  'non_claims':[
    'does not identify the crossing with a physical phase transition or EFT cutoff',
    'does not prove perturbative unitarity below or above the crossing',
    'does not include gravity/U1/auxiliary exchange or loop corrections',
    'T_CMB_scaled is only the adiabatic photon-temperature redshift conversion and is not a statement that the same particle content/thermal history applies arbitrarily early',
    'does not choose a UV-completion scale'
  ],
  'next_gate':'derive dimensionless 2-to-2 power-counting parameters with the exact high-k normalization and compare the current-point perturbative scale to H(z) over the certified BBN/CMB history; then include exchange diagrams.'
}
open('c9_rtk_scalar_current_frequency_crossover_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
