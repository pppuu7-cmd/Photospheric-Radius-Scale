#!/usr/bin/env python3
import json
import sympy as sp

# Generic background/source symbols
H,a,k,Mc=sp.symbols('H a k M_c', positive=True, finite=True)
W,C,W0,C0=sp.symbols('W C W0 C0', positive=True, finite=True)
B,psi,PsiN=sp.symbols('B psi_pref Psi_N', finite=True)
dmuN,dpN,qN=sp.symbols('delta_mu_N delta_p_N q_N', finite=True)
dH0N,dp0N,q0N=sp.symbols('deltaH0_N delta_p0_N q0_N', finite=True)
PsiNp=sp.symbols('Psi_N_prime', finite=True)

rhop=-3*H*W
pp=-3*H*C
H0p=-3*H*W0
p0p=-3*H*C0

# Certified bridge: Psi_N = psi_pref-H B.
bridge=sp.Eq(PsiN,psi-H*B)

mu_hat=dmuN-3*W*PsiN
p_hat=dpN-3*C*PsiN
h_hat=dH0N-3*W0*PsiN
p0_hat=dp0N-3*C0*PsiN

dmu_pref=dmuN-rhop*B
dp_pref=dpN-pp*B
dH0_pref=dH0N-H0p*B

mu_res=sp.simplify((dmu_pref-(mu_hat+3*W*psi)).subs(PsiN,psi-H*B))
p_res=sp.simplify((dp_pref-(p_hat+3*C*psi)).subs(PsiN,psi-H*B))
h_res=sp.simplify((dH0_pref-(h_hat+3*W0*psi)).subs(PsiN,psi-H*B))
assert mu_res==0 and p_res==0 and h_res==0

# Elliptic A constraint in native CLASS units.
a1=k**2/(k**2+a**2*Mc**2)
L=-k**2
K=sp.simplify(sp.Rational(3,2)*a**2*a1/L)
K_closed=-sp.Rational(3,2)*a**2/(k**2+a**2*Mc**2)
assert sp.simplify(K-K_closed)==0
DA=sp.simplify(1-3*K*W0)
# DA=1+positive for declared positive domain.
DA_minus_1=sp.simplify(DA-1)
assert DA_minus_1.is_positive is True
A_eq_res=sp.expand(psi-K*(h_hat+3*W0*psi)-DA*psi+K*h_hat)
assert sp.simplify(A_eq_res)==0

# K derivative: a'=H a, constant k and Mc.
Kp_direct=sp.simplify(sp.diff(K,a)*H*a)
Kp_expected=sp.simplify(2*H*a1*K)
Kp_res=sp.simplify(Kp_direct-Kp_expected)
assert Kp_res==0

# Ordinary aggregate physical-metric conservation for H0 subset:
# dH0_N'=-3H(dH0_N+dp0_N)-(k^2/a)q0_N+3W0 Psi_N'.
# W0' = rho0'+p0' = -3H(W0+C0).
dH0Np=-3*H*(dH0N+dp0N)-(k**2/a)*q0N+3*W0*PsiNp
W0p=-3*H*(W0+C0)
h_hat_p=sp.expand(dH0Np-3*W0p*PsiN-3*W0*PsiNp)
h_hat_expected=-3*H*(h_hat+p0_hat)-(k**2/a)*q0N
hhat_res=sp.simplify(h_hat_p-h_hat_expected)
assert hhat_res==0
assert sp.simplify(sp.diff(h_hat_p,PsiNp))==0

# Differentiate DA psi = K h_hat.  DA'= -3(K'W0+K W0').
psi_p_sym,hhat_p_sym=sp.symbols('psi_prime h_hat_prime', finite=True)
DAp=sp.simplify(-3*(Kp_expected*W0+K*W0p))
psi_p_solution=sp.simplify((Kp_expected*h_hat+K*hhat_p_sym-DAp*psi)/DA)
# No B' or Psi_N' symbols exist; verify algebraic equivalent source-expanded form.
psi_p_alt=sp.simplify((Kp_expected*(h_hat+3*W0*psi)+K*(hhat_p_sym+3*W0p*psi))/DA)
psi_prime_res=sp.simplify(psi_p_solution-psi_p_alt)
assert psi_prime_res==0

# Constant-w species dressed density. Physical Newtonian convention:
# delta' = -(1+w)(theta-3 Psi_N') -3H(cs2-w)delta - entropy_extra.
# We keep a generic non-metric source S; D=delta-3(1+w)Psi_N eliminates Psi_N'.
w,cs2,delta,theta,S=sp.symbols('w cs2 delta theta S', finite=True)
deltap=-(1+w)*(theta-3*PsiNp)-3*H*(cs2-w)*delta+S
Dsp=delta-3*(1+w)*PsiN
Dsp_p=sp.expand(deltap-3*(1+w)*PsiNp)
Dsp_expected=-(1+w)*theta-3*H*(cs2-w)*delta+S
Dsp_res=sp.simplify(Dsp_p-Dsp_expected)
assert Dsp_res==0
assert sp.simplify(sp.diff(Dsp_p,PsiNp))==0

# Algebraic momentum transform remains derivative-free.
q_pref=qN-a*W*B

out={
  'schema':'RTK_C10_CURVATURE_DRESSED_ORDINARY_DAE_CLOSURE_RESULT_v1',
  'classification':'C10_CURVATURE_DRESSED_ORDINARY_DAE_CLOSURE_PASS_POLE_FREE_SCOPED',
  'dressed_definitions':{
    'mu_hat':'delta_mu_N-3 W Psi_N',
    'p_hat':'delta_p_N-3 C Psi_N, C=-p_prime/(3H)',
    'h_hat':'deltaH0_N-3 W0 Psi_N',
    'p0_hat':'delta_p0_N-3 C0 Psi_N'
  },
  'preferred_source_identities':{
    'delta_mu_pref':'mu_hat+3 W psi_pref',
    'delta_p_pref':'p_hat+3 C psi_pref',
    'deltaH0_pref':'h_hat+3 W0 psi_pref',
    'q_pref':'q_N-a W B',
    'Bprime_required':False
  },
  'dressed_A_constraint':{
    'K':'-(3/2) a^2/(k^2+a^2 M_c^2)',
    'D_A':'1-3 K W0',
    'equation':'D_A psi_pref=K h_hat',
    'pole_theorem':'for k>0, a>0, M_c>0, W0>0: K<0 and D_A=1+9 a^2 W0/[2(k^2+a^2 M_c^2)]>1',
    'K_prime':'2 H a1_eff K',
    'K_prime_direct_check':'PASS'
  },
  'dressed_ordinary_continuity':{
    'h_hat_prime':'-3H(h_hat+p0_hat)-(k^2/a) q0_N',
    'Psi_N_prime_coefficient':'0',
    'generic_constant_w_species':'D_i=delta_i-3(1+w_i)Psi_N removes the explicit +3(1+w_i)Psi_N_prime term from the physical Newtonian continuity equation'
  },
  'differentiated_A_constraint':{
    'psi_prime':'[K_prime h_hat+K h_hat_prime-D_A_prime psi]/D_A',
    'D_A_prime':'-3(K_prime W0+K W0_prime)',
    'equivalent':'[K_prime(h_hat+3W0 psi)+K(h_hat_prime+3W0_prime psi)]/D_A',
    'B_prime_present':False,
    'Psi_N_prime_present':False
  },
  'architecture':{
    'ordinary_species':'evolve curvature-dressed physical-metric density variables; velocities/higher multipoles remain physical-interface variables',
    'neutral_khronon':'evolve preferred action-fluid variables from C10.59',
    'gravity':'algebraically project psi_pref,phi_pref,B each sample; construct Phi_N,Psi_N outputs for ordinary species',
    'temporal_chi_state':'not required'
  },
  'machine_residuals':{
    'mu_source_transform':str(mu_res),
    'p_source_transform':str(p_res),
    'H0_source_transform':str(h_res),
    'A_equation':str(sp.simplify(A_eq_res)),
    'K_prime':str(Kp_res),
    'h_hat_continuity':str(hhat_res),
    'h_hat_PsiNprime_coefficient':str(sp.simplify(sp.diff(h_hat_p,PsiNp))),
    'psi_prime_forms':str(psi_prime_res),
    'constant_w_dressed_density':str(Dsp_res),
    'constant_w_PsiNprime_coefficient':str(sp.simplify(sp.diff(Dsp_p,PsiNp)))
  },
  'next_gate':'implement a detached dual-interface ODE/DAE prototype and freeze a finite-onset memory-loss/attractor test before introducing any UV matching parameter',
  'non_claims':['not exact k=0','not massive-neutrino completion','not a full photon hierarchy implementation','not completed-U1 CLASS feedback','not an attractor theorem','not spectra or likelihood evidence']
}
assert all(v=='0' for v in out['machine_residuals'].values())
print(json.dumps(out,indent=2,sort_keys=True))
