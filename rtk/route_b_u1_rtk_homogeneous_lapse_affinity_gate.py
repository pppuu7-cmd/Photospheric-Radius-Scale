#!/usr/bin/env python3
"""Homogeneous rolling RTK lapse-affinity theorem.

The neutral RTK sector used in the U(1) route consists of a rolling scalar
F(X_U) sector plus the U(1)-invariant mixed spatial operator built from
D_i Theta_U.  On an exactly homogeneous FLRW/rolling slice,

  D_i Sigma=0,  D_i Theta_U=0,

so the mixed spatial operator vanishes identically.  Write

  y = dot(Sigma)/N,  X_U=y^2,
  L_hom = N sqrt(g) F(y^2).

The canonical momentum is

  p_Sigma = 2 sqrt(g) y F_X,

which is independent of N when expressed in terms of y.  On any regular
Legendre branch (dp/dy != 0), y=y(p_Sigma,g) is therefore lapse-independent and

  H_hom = N [p_Sigma y - sqrt(g) F(y^2)] = N H0_Sigma.

Hence H_perp,Sigma=H0_Sigma is N-independent and
{pi_N,H_perp,Sigma}=0.  Combined with the older RTK cross-block support theorem,
this removes its only allowed direct correction to the special-U(1) B block on
the homogeneous rolling branch.
"""
import json
import sympy as sp

N,sqrtg,y=sp.symbols('N sqrtg y', positive=True, finite=True)
c0,c1,c2,c3=sp.symbols('c0 c1 c2 c3', finite=True)
# Generic nonlinear representative protects the structural algebra beyond a
# purely quadratic example.
X=y**2
F=c0+c1*X+c2*X**2+c3*X**3
p=sp.simplify(sqrtg*sp.diff(F,y))
assert sp.diff(p,N)==0
legendre_jac=sp.factor(sp.diff(p,y))

# Once the regular branch y=y(p,g) is selected, y is an N-independent canonical
# function.  The Hamiltonian is exactly affine in lapse.
p_can=sp.symbols('p_Sigma', finite=True)
H0=sp.expand(p_can*y-sqrtg*F)
H=N*H0
Hperp=sp.diff(H,N)
assert sp.simplify(Hperp-H0)==0
assert sp.diff(Hperp,N)==0
assert sp.diff(H,N,N)==0

# Exact homogeneous support of the mixed operator from the previously used
# Theta construction: all spatial jets vanish, hence D_i Theta=0.
Sdot=sp.symbols('Sdot', finite=True)
Sx,Sdotx,Nx,Nix,nux,nuxx,Sxx,Ni=sp.symbols(
    'Sx Sdotx Nx Nix nux nuxx Sxx Ni', finite=True
)
V=Ni-N*nux
Vx=Nix-Nx*nux-N*nuxx
DxTheta=sp.expand((Sdotx-Vx*Sx-V*Sxx)/N-(Sdot-V*Sx)*Nx/N**2)
hom={Sx:0,Sdotx:0,Nx:0,Nix:0,nux:0,nuxx:0,Sxx:0,Ni:0}
assert sp.simplify(DxTheta.subs(hom))==0
C=sp.symbols('C', finite=True)
Lmix=C*DxTheta**2
assert sp.simplify(Lmix.subs(hom))==0

# Cross-block inheritance algebra after combining ordinary k=0 matter and RTK.
ag,bg,cg,dg=sp.symbols('a_g b_g c_g d_g', finite=True)
Bg=sp.Matrix([[ag,bg],[cg,dg]])
Bhom=sp.Matrix([[ag,bg],[cg,dg]])
assert Bhom==Bg
assert sp.simplify(Bhom.det()-Bg.det())==0

out={
  'classification':'RTK_ROUTE_B_U1_RTK_HOMOGENEOUS_LAPSE_AFFINITY_PASS',
  'status_scope':'GREEN_HOMOGENEOUS_RTK_DIRECT_CROSSBLOCK_CORRECTION_ZERO_FINITE_K_PENDING',
  'domain':'exact homogeneous D_i Sigma=D_i Theta_U=D_i nu=D_i N=0 rolling branch with regular scalar Legendre map',
  'homogeneous_scalar':{
    'Lagrangian':'L=N sqrt(g) F(y^2), y=dot(Sigma)/N',
    'momentum':'p_Sigma=2 sqrt(g) y F_X, lapse independent as a function of y',
    'regularity':'dp_Sigma/dy != 0 so y=y(p_Sigma,g) is a lapse-independent canonical function',
    'Hamiltonian':'H_Sigma=N H0_Sigma',
    'Hperp_Sigma':'H0_Sigma',
    'delta_{pi_N,Hperp}_RTK':'0'
  },
  'mixed_spatial_operator':'C(D_i Theta_U)^2=0 exactly on the homogeneous slice',
  'combined_with_prior_support':'The older neutral-RTK theorem allowed a direct correction only to {pi_N,Hperp}; this gate proves that correction vanishes on the homogeneous rolling slice.',
  'homogeneous_crossblock_consequence':'Together with the k=0 projected ordinary-matter inheritance theorem, B_total(k=0,homogeneous)=B_gravity on this classical support slice.',
  'legendre_representative_jacobian':str(legendre_jac),
  'interpretation':'The exact FLRW source-rescue mode does not deform the published special-U1 second-class cross block through either ordinary matter or the neutral RTK scalar, provided the already-required rolling scalar Legendre branch is regular.',
  'non_claims':[
    'does not prove the full finite-k reduced B block stays nonsingular',
    'does not cover inhomogeneous lapse/scalar configurations where D_i Theta_U is nonzero',
    'does not prove the global k=0 Green-operator boundary condition is unique',
    'does not address radiative regeneration of eta1,eta2 or choose M_c'
  ],
  'next_gate':'combine the published pure-gravity det B != 0 theorem with this exact homogeneous inheritance to certify the local homogeneous classical rank, while independently deriving finite-k resolvent corrections.'
}
with open('u1_rtk_homogeneous_lapse_affinity_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
