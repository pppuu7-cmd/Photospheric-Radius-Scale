#!/usr/bin/env python3
"""Symbolically reconstruct the minimal long-wave barotropic P(X) subsector.

Conditional theorem only: this does not reconstruct the higher-spatial-derivative
finite-k Khronon completion. The proof is split into exact Khronon thermodynamic
identities plus model-independent P(X) algebra to avoid fragile giant P_XXX
simplifications.
"""
import json
import sympy as sp

# ----- Exact Khronon thermodynamic identities -----
x, lam, C = sp.symbols('x lam C', positive=True, finite=True)
s = sp.sqrt(1 + lam*x**2)
r = x/s
t = x/(s+1)
rho = C*x*(1+t)
p = C*r*t
ca2 = r/(s*(s+x))
G = sp.simplify(rho+p)
K = sp.simplify(G/ca2)

# Implemented barotropic identity.
assert sp.simplify(sp.diff(p,x) - ca2*sp.diff(rho,x)) == 0
# Conserved-density first law for n proportional to x.
assert sp.simplify(x*sp.diff(rho,x)-G) == 0

# sqrt(2X)=(rho+p)/x, up to an irrelevant constant field normalization.
h = sp.simplify(G/x)
X_of_x = sp.simplify(h**2/2)
assert sp.simplify(x*sp.diff(h,x)-ca2*h) == 0
assert sp.simplify(x*sp.diff(X_of_x,x)-2*ca2*X_of_x) == 0

# From dp/dx=c_a^2*d rho/dx and x*rho'=G, while x*X'=2 c_a^2 X,
# the reconstructed pressure P(X(x)) has 2X P_X = G exactly.
PX_chain = sp.simplify(sp.diff(p,x)/sp.diff(X_of_x,x))
assert sp.simplify(2*X_of_x*PX_chain-G) == 0

# K matching can be proved without constructing the enormous explicit P_XX:
# for P(X), K = 2 dG/dlnX - G. Check this against G/c_a^2 using the exact
# x->X map.
dlnX_dlnx = sp.simplify(x*sp.diff(X_of_x,x)/X_of_x)
dG_dlnX = sp.simplify((x*sp.diff(G,x))/dlnX_dlnx)
K_from_G = sp.simplify(2*dG_dlnX-G)
assert sp.simplify(K_from_G-K) == 0

# ----- Model-independent P(X) cubic algebra -----
X = sp.symbols('X', positive=True, finite=True)
P = sp.Function('P')(X)
P1, P2, P3 = sp.diff(P,X), sp.diff(P,X,2), sp.diff(P,X,3)
Gpx = 2*X*P1
Kpx = 2*X*P1 + 4*X**2*P2
c1_direct = 2*X**2*P2 + sp.Rational(4,3)*X**3*P3
c2_direct = -2*X**2*P2
assert sp.simplify(c2_direct + (Kpx-Gpx)/2) == 0
assert sp.simplify(c1_direct - (X*sp.diff(Kpx,X)-Kpx)/3) == 0

# Pull the c1 derivative back to the exact Khronon density coordinate.
c1_xform = sp.simplify(((x*sp.diff(K,x))/(2*ca2)-K)/3)
dK_dlnX_exact = sp.simplify((x*sp.diff(K,x))/dlnX_dlnx)
assert sp.simplify(c1_xform-(dK_dlnX_exact-K)/3) == 0

result={
 'classification':'RTK_ROUTE_A1_PX_LONGWAVE_RECONSTRUCTION_PASS',
 'khronon_first_law':'x*d rho/dx = rho+p',
 'barotropic_identity':'dp/d rho = c_a^2',
 'dlnX_dlnx':'2*c_a^2',
 'quadratic_matching':{'G':'rho+p','K':'(rho+p)/c_a^2'},
 'D3_cubic_coefficients':{
   'c1':'(dK/dlnX-K)/3 = ((dK/dlnx)/(2*c_a^2)-K)/3',
   'c2':'-(K-G)/2'
 },
 'D4_coefficients_fixed_by_background':False,
 'finite_k_completion_reconstructed':False,
 'strong_coupling_scale_determined':False,
}
print('RTK_ROUTE_A1_PX_RECONSTRUCTION_PASS',json.dumps(result,sort_keys=True))
