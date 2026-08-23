#!/usr/bin/env python3
"""RTK scalar single-channel partial-wave / phase-space unitarity gate.

Scope
-----
Frozen replay-certified RTK scalar background, P(X)-sector elastic 2->2 tree
amplitude only.  The external oscillators are canonically normalized with
Z(k)=1+k^2/M_K^2 and have exact monotonic isotropic dispersion

    omega(k)=c_a k/sqrt(1+k^2/M_K^2).

For a canonically normalized identical scalar with a general monotonic isotropic
dispersion omega(k), the COM two-particle phase-space factor entering the
partial-wave optical theorem is

    g(k)=k^2/[2 omega(k)^2 v_g(k)],   v_g=d omega/dk.

This follows directly from the radial delta-function in the two-particle phase
space, with the normalization calibrated to the published linear-dispersion
result g=1/(2 c_s^3) for omega=c_s k.  The single-channel tree-level bound is

    |Re[g(k) a_l(k)]| <= 1/2.

The gate derives g(k), exact l=0 and l=2 projections of the previously certified
P(X) amplitude, proves the UV phase-space divergence for the rational frequency
saturation, derives the early-DBI-edge finite momentum cutoff analytically, and
locates the first numerical l=0 crossing along the frozen cosmological trajectory.

This is substantially stronger than the earlier |M|~1 benchmark, but still not a
complete all-sector EFT unitarity theorem: mixed C(X), metric/U(1)/auxiliary
exchange, loops, inelastic channels and the UV completion are not included.
"""

import json
import math
import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# Symbolic phase-space and partial-wave theorem
# ---------------------------------------------------------------------------
y, ca, MK = sp.symbols('y c_a M_K', positive=True, finite=True)
k = sp.symbols('k', positive=True, finite=True)
omega = ca*k/sp.sqrt(1+k**2/MK**2)
vg = sp.factor(sp.diff(omega, k))
g = sp.factor(k**2/(2*omega**2*vg))
g_expected = (1+k**2/MK**2)**sp.Rational(5, 2)/(2*ca**3)
assert sp.simplify(g-g_expected) == 0
assert sp.simplify(g_expected.subs(k, y*MK) - (1+y**2)**sp.Rational(5,2)/(2*ca**3)) == 0
assert sp.limit(g_expected.subs(k, y*MK), y, 0, dir='+') == 1/(2*ca**3)

w, c = sp.symbols('omega c', real=True, finite=True)
C3t, C3s, C4t, C4ts, C4s = sp.symbols('C3t C3s C4t C4ts C4s', real=True, finite=True)
Z = sp.symbols('Z', positive=True, finite=True)
Mamp = (
    24*C4t*w**4
    - 8*C4ts*k**2*w**2
    + 8*C4s*k**4*(1+2*c**2)
    + 4*(C3s*k**2-3*C3t*w**2)**2
)/Z**2
P2 = sp.Rational(1,2)*(3*c**2-1)
a0 = sp.factor(sp.integrate(Mamp, (c,-1,1))/(32*sp.pi))
a2 = sp.factor(sp.integrate(P2*Mamp, (c,-1,1))/(32*sp.pi))
a0_expected = sp.factor((48*C4t*w**4 - 16*C4ts*k**2*w**2 + sp.Rational(80,3)*C4s*k**4 + 8*(C3s*k**2-3*C3t*w**2)**2)/(32*sp.pi*Z**2))
a2_expected = sp.factor(2*C4s*k**4/(15*sp.pi*Z**2))
assert sp.simplify(a0-a0_expected) == 0
assert sp.simplify(a2-a2_expected) == 0

# UV: omega -> c_a M_K, Z~y^2.  Only spatial quartic and spatial-cubic
# s-exchange remain in a0.  The phase-space factor grows as y^5.
a0_uv = MK**4*(3*C3s**2 + 10*C4s)/(12*sp.pi)
a2_uv = 2*C4s*MK**4/(15*sp.pi)
assert sp.simplify(sp.limit(a0_expected.subs({k:y*MK, w:ca*y*MK/sp.sqrt(1+y**2), Z:1+y**2}), y, sp.oo)-a0_uv) == 0
assert sp.simplify(sp.limit(a2_expected.subs({k:y*MK, Z:1+y**2}), y, sp.oo)-a2_uv) == 0

# ---------------------------------------------------------------------------
# Early DBI-edge theorem
# ---------------------------------------------------------------------------
lam, delta, Mpl, mu = sp.symbols('lambda_D delta M_Pl mu_K', positive=True, finite=True)
sL = sp.sqrt(lam)
r_edge = 1/sL
ca2_edge = delta/(sL+1)
w2_edge = ca2_edge*k**2
C3t_e = sp.sqrt(2)*lam*r_edge/(4*Mpl*mu*delta**sp.Rational(1,4))
C3s_e = -sp.sqrt(2)*(1+lam*r_edge**3)*delta**sp.Rational(3,4)/(4*Mpl*mu*(1+r_edge)**2)
C4t_e = lam*(1+4*lam*r_edge**2)/(16*Mpl**2*mu**2*sp.sqrt(delta))
C4ts_e = -sp.sqrt(delta)*(2*lam**2*r_edge**5+lam*r_edge**3+8*lam*r_edge**2+3*lam*r_edge-2)/(8*Mpl**2*mu**2*(1+r_edge)**3)
C4s_e = delta**sp.Rational(3,2)*(1+lam*r_edge**3)/(16*Mpl**2*mu**2*(1+r_edge)**3)

a0_edge = sp.factor((48*C4t_e*w2_edge**2 - 16*C4ts_e*k**2*w2_edge + sp.Rational(80,3)*C4s_e*k**4 + 8*(C3s_e*k**2-3*C3t_e*w2_edge)**2)/(32*sp.pi))
a2_edge = sp.factor(2*C4s_e*k**4/(15*sp.pi))
g_edge = (sL+1)**sp.Rational(3,2)/(2*delta**sp.Rational(3,2))
ga0_edge = sp.factor(sp.simplify(g_edge*a0_edge))
ga2_edge = sp.factor(sp.simplify(g_edge*a2_edge))
ga0_ref = 29*lam*k**4/(48*sp.pi*Mpl**2*mu**2*sp.sqrt(sL+1))
assert sp.simplify(ga0_edge-ga0_ref) == 0
assert sp.simplify(ga2_edge/ga0_edge-sp.Rational(1,145)) == 0
kunit4 = sp.factor(24*sp.pi*Mpl**2*mu**2*sp.sqrt(sL+1)/(29*lam))
assert sp.simplify(ga0_ref.subs(k, kunit4**sp.Rational(1,4))-sp.Rational(1,2)) == 0

# ---------------------------------------------------------------------------
# Frozen replay-certified numerical background
# ---------------------------------------------------------------------------
h=0.691103719964454
OmegaK0=0.2522864064078236
lambdaD=219457.5727136581
gamma=0.05170371280716
MPC_M=3.0856775814913673e22
HBARC_EV_M=1.973269804e-7
INV_MPC_EV=HBARC_EV_M/MPC_M
MPL=2.435e27
H0=100.0*h/299792.458
mu_mpc=3.0*H0*math.sqrt(gamma)
mu_eV=mu_mpc*INV_MPC_EV
A0=OmegaK0/(6.0*gamma)
x0=A0*(2.0+lambdaD*A0)/(1.0+lambdaD*A0+math.sqrt(1.0+2.0*A0+lambdaD*A0*A0))


def state(z):
    x=x0*(1.0+z)**3
    s=math.hypot(1.0,math.sqrt(lambdaD)*x)
    r=x/s
    d=1.0/(s*s)
    ca2=r*d/(1.0+r)
    MKv=mu_eV*(1.0+r)*s*math.sqrt(s)
    C3tv=math.sqrt(2.0)*lambdaD*r/(4.0*MPL*mu_eV*d**0.25)
    C3sv=-math.sqrt(2.0)*(1.0+lambdaD*r**3)*d**0.75/(4.0*MPL*mu_eV*(1.0+r)**2)
    C4tv=lambdaD*(1.0+4.0*lambdaD*r*r)/(16.0*MPL**2*mu_eV**2*math.sqrt(d))
    C4tsv=-math.sqrt(d)*(2.0*lambdaD**2*r**5+lambdaD*r**3+8.0*lambdaD*r*r+3.0*lambdaD*r-2.0)/(8.0*MPL**2*mu_eV**2*(1.0+r)**3)
    C4sv=d**1.5*(1.0+lambdaD*r**3)/(16.0*MPL**2*mu_eV**2*(1.0+r)**3)
    return {'r':r,'delta':d,'ca2':ca2,'MK':MKv,'C3t':C3tv,'C3s':C3sv,'C4t':C4tv,'C4ts':C4tsv,'C4s':C4sv}


def measures(z,yv):
    s=state(z)
    cav=math.sqrt(s['ca2'])
    ZZ=1.0+yv*yv
    kv=yv*s['MK']
    wv=cav*kv/math.sqrt(ZZ)
    core=24.0*s['C4t']*wv**4 - 8.0*s['C4ts']*kv**2*wv**2 + 4.0*(s['C3s']*kv**2-3.0*s['C3t']*wv**2)**2
    a0v=(2.0*core+(80.0/3.0)*s['C4s']*kv**4)/(32.0*math.pi*ZZ**2)
    a2v=(2.0/(15.0*math.pi))*s['C4s']*kv**4/ZZ**2
    gv=ZZ**2.5/(2.0*cav**3)
    return {
      'g':gv,
      'a0':a0v,
      'a2':a2v,
      'g_a0':gv*a0v,
      'g_a2':gv*a2v,
      'k_eV':kv,
      'omega_eV':wv,
      'y_k_over_MK':yv,
      'M_K_eV':s['MK'],
      'c_a':cav,
      'delta':s['delta']
    }


def first_crossing(z):
    # Find the first y>0 where max_l |g a_l| reaches 1/2.
    ylo=1.0e-50
    flo=max(abs(measures(z,ylo)['g_a0']),abs(measures(z,ylo)['g_a2']))-0.5
    assert flo < 0
    yhi=ylo
    for _ in range(100):
        yhi*=10.0
        m=measures(z,yhi)
        fhi=max(abs(m['g_a0']),abs(m['g_a2']))-0.5
        if fhi >= 0:
            break
    else:
        raise AssertionError('failed to bracket partial-wave crossing')
    # logarithmic bisection
    for _ in range(140):
        ym=math.sqrt(ylo*yhi)
        m=measures(z,ym)
        fm=max(abs(m['g_a0']),abs(m['g_a2']))-0.5
        if fm < 0:
            ylo=ym
        else:
            yhi=ym
    yr=math.sqrt(ylo*yhi)
    out=measures(z,yr)
    out['reduced_wavelength_1_over_k_m']=HBARC_EV_M/out['k_eV']
    out['ordinary_wavelength_2pi_over_k_m']=2.0*math.pi*HBARC_EV_M/out['k_eV']
    out['dominant_partial_wave']='l=0' if abs(out['g_a0']) >= abs(out['g_a2']) else 'l=2'
    return out

refs_z=[0.0,1.0,10.0,100.0,1100.0,1.0e4,1.0e5,1.0e6,1.0e7,1.0e9,1.0e12]
rows=[]
for z in refs_z:
    r=first_crossing(z)
    rows.append({'z':z, **r})
    assert r['dominant_partial_wave']=='l=0'
    assert abs(abs(r['g_a0'])-0.5) < 2e-12
    assert abs(r['g_a2']) < 0.5

# Monotonicity audit on representative epochs: the first crossing is unique on
# the sampled domain; this is a numerical audit, not a global symbolic proof.
monotonic_audit={}
for z in [0.0,1100.0,1.0e6,1.0e9,1.0e12]:
    vals=[]
    for ey in np.linspace(-40.0,30.0,1401):
        m=measures(z,10.0**float(ey))
        vals.append(max(abs(m['g_a0']),abs(m['g_a2'])))
    decreases=sum(1 for a,b in zip(vals,vals[1:]) if b < a*(1.0-1e-10))
    monotonic_audit[str(z)]={'grid_points':len(vals),'decreases_beyond_1e-10_relative':decreases}
    assert decreases==0

kearly=(24.0*math.pi*MPL**2*mu_eV**2*math.sqrt(math.sqrt(lambdaD)+1.0)/(29.0*lambdaD))**0.25
early_row=first_crossing(1.0e9)
early_rel=abs(early_row['k_eV']/kearly-1.0)
assert early_rel < 2e-12
assert abs(early_row['g_a2']/early_row['g_a0']-1.0/145.0) < 2e-12

# Deep-UV positivity at each reference state guarantees eventual tree-level
# breakdown of the rational-dispersion P(X) truncation because g~y^5.
uv_rows=[]
for z in [0.0,1100.0,1.0e6,1.0e9]:
    s=state(z)
    a0inf=s['MK']**4*(3.0*s['C3s']**2+10.0*s['C4s'])/(12.0*math.pi)
    assert a0inf > 0
    uv_rows.append({'z':z,'a0_infinity':a0inf})

out={
  'classification':'RTK_C9_RTK_SCALAR_PARTIAL_WAVE_PHASE_SPACE_UNITARITY_PASS',
  'status_scope':'YELLOW_SINGLE_CHANNEL_PX_TREE_PARTIAL_WAVE_CUTOFF_CERTIFIED_ALL_SECTOR_UNITARITY_AND_UV_COMPLETION_PENDING',
  'literature_calibration':{
    'reference':'Ageeva & Petrov, arXiv:2206.03516, identical-scalar linear-dispersion result',
    'published_g_linear':'g=1/(2 c_s^3)',
    'published_tree_bound':'|Re(tilde a_l)|<=1/2 with tilde a_l=g a_l for one identical-scalar channel'
  },
  'general_phase_space':{
    'formula':'g(k)=k^2/[2 omega(k)^2 v_g(k)] for one canonically normalized identical scalar with monotonic isotropic omega(k)',
    'rtk_group_velocity':'v_g=c_a/[1+(k/M_K)^2]^(3/2)',
    'rtk_g':'g=[1+(k/M_K)^2]^(5/2)/(2 c_a^3)',
    'linear_limit':'k/M_K->0 gives g=1/(2 c_a^3)'
  },
  'partial_waves':{
    'a0':'[48 C4t omega^4-16 C4ts k^2 omega^2+(80/3)C4s k^4+8(C3s k^2-3C3t omega^2)^2]/[32 pi Z^2]',
    'a2':'2 C4s k^4/[15 pi Z^2]',
    'all_other_even_l_tree_PX':'0 for the certified polynomial elastic amplitude'
  },
  'uv_theorem':{
    'a0_infinity':'M_K^4[3 C3s^2+10 C4s]/(12 pi)>0 on the production branch',
    'a2_infinity':'2 C4s M_K^4/(15 pi)>0',
    'phase_space':'g~(k/M_K)^5/(2 c_a^3)',
    'consequence':'g a0 diverges as k^5, so the rational frequency-saturating P(X) truncation cannot remain perturbatively unitary to arbitrarily large momentum'
  },
  'early_edge':{
    'g_a0':'29 lambda_D k^4/[48 pi M_Pl^2 mu_K^2 sqrt(sqrt(lambda_D)+1)]',
    'g_a2_over_g_a0':'1/145',
    'k_unitarity_fourth_power':'24 pi M_Pl^2 mu_K^2 sqrt(sqrt(lambda_D)+1)/(29 lambda_D)',
    'k_unitarity_eV':kearly,
    'reduced_wavelength_1_over_k_m':HBARC_EV_M/kearly,
    'ordinary_wavelength_2pi_over_k_m':2.0*math.pi*HBARC_EV_M/kearly,
    'z_1e9_relative_difference_to_asymptote':early_rel
  },
  'frozen_point':{'h':h,'Omega_K0':OmegaK0,'lambda_D':lambdaD,'gamma':gamma,'x0':x0,'mu_K_Mpc_inv':mu_mpc,'mu_K_eV':mu_eV},
  'crossing_rows':rows,
  'monotonicity_grid_audit':monotonic_audit,
  'uv_reference_rows':uv_rows,
  'interpretation':'The exact rational dispersion softens fixed-amplitude vertices but simultaneously drives v_g->0. The resulting two-particle density of states grows as k^5 and produces a finite single-channel P(X) tree partial-wave cutoff. Along the frozen cosmological trajectory the cutoff rises from ~2.78e-9 eV today to the early-time plateau ~1.98072e-4 eV. This is a momentum-EFT cutoff signal, not a cosmological phase transition.',
  'non_claims':[
    'does not include mixed C(X) tree vertices or exchange in the partial waves',
    'does not include metric, U(1), auxiliary, graviton or matter exchange channels',
    'does not include loop running or inelastic/multiparticle channels',
    'does not prove a specific UV completion',
    'does not identify 1/k with the resolution of any particular experiment',
    'does not by itself invalidate cosmological perturbations; comparison to the actual physical k-range must be made separately'
  ],
  'next_gate':'compare the certified k_unitarity(z) curve to the exact physical wavenumber range used by B6/B9 cosmology; then test minimal higher-spatial kinetic completions that make omega(k) grow again before the phase-space cutoff while leaving the observed rational regime unchanged.'
}
with open('c9_rtk_scalar_partial_wave_phase_space_unitarity_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps({'early_edge':out['early_edge'],'selected_rows':[rows[0],rows[4],rows[7],rows[-1]]},sort_keys=True))
