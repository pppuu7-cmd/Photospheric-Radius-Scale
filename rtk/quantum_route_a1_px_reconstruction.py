#!/usr/bin/env python3
"""Symbolically reconstruct the minimal long-wave barotropic P(X) subsector.

Conditional theorem only: this does not reconstruct the higher-spatial-derivative
finite-k Khronon completion.
"""
import json
import sympy as sp

x, lam, C = sp.symbols('x lam C', positive=True, finite=True)
s = sp.sqrt(1 + lam*x**2)
r = x/s
t = x/(s+1)
rho = C*x*(1+t)
p = C*r*t
ca2 = r/(s*(s+x))
G = sp.simplify(rho+p)
K = sp.simplify(G/ca2)

# Exact barotropic identity already used by the implementation.
ca2_from_derivatives = sp.simplify(sp.diff(p,x)/sp.diff(rho,x))
assert sp.simplify(ca2_from_derivatives-ca2) == 0

# Conserved-density reconstruction: n proportional to x and
# sqrt(2X)=(rho+p)/n. Overall X normalization is conventional.
h = sp.simplify(G/x)
X = sp.simplify(h**2/2)
dlnh_dlnx = sp.simplify(x*sp.diff(h,x)/h)
dlnX_dlnx = sp.simplify(x*sp.diff(X,x)/X)
assert sp.simplify(dlnh_dlnx-ca2) == 0
assert sp.simplify(dlnX_dlnx-2*ca2) == 0

# Treat P(X(x)) = p(x), use chain rule to reconstruct P_X, P_XX, P_XXX.
dXdx = sp.diff(X,x)
PX = sp.simplify(sp.diff(p,x)/dXdx)
PXX = sp.simplify(sp.diff(PX,x)/dXdx)
PXXX = sp.simplify(sp.diff(PXX,x)/dXdx)

# Goldstone time-shift quadratic matching.
G_px = sp.simplify(2*X*PX)
K_px = sp.simplify(2*X*PX + 4*X**2*PXX)
assert sp.simplify(G_px-G) == 0
assert sp.simplify(K_px-K) == 0

# Cubic coefficients from direct P(X) expansion.
c1_direct = sp.simplify(2*X**2*PXX + sp.Rational(4,3)*X**3*PXXX)
c2_direct = sp.simplify(-2*X**2*PXX)

# Thermodynamic forms.
c2_thermo = sp.simplify(-(K-G)/2)
dK_dlnX = sp.simplify((x*sp.diff(K,x))/dlnX_dlnx)
c1_thermo = sp.simplify((dK_dlnX-K)/3)
c1_xform = sp.simplify(((x*sp.diff(K,x))/(2*ca2)-K)/3)
assert sp.simplify(c2_direct-c2_thermo) == 0
assert sp.simplify(c1_direct-c1_thermo) == 0
assert sp.simplify(c1_direct-c1_xform) == 0

# Pure P(X) has no D=4 higher-spatial-derivative Route-A1 vertices.
# It therefore cannot by itself generate K/(2M^2)(grad dot pi)^2.
result={
 'classification':'RTK_ROUTE_A1_PX_LONGWAVE_RECONSTRUCTION_PASS',
 'barotropic_identity':True,
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
