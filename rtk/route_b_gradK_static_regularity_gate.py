#!/usr/bin/env python3
import json
import sympy as sp

# Exact C8 regularity test for the required grad-K scalar coefficients.
# M2 denotes M_*^2 and MK2 denotes M_K^2.
H,M2,Kc,MK2,Mcos2=sp.symbols('H M2 Kc MK2 Mcos2', positive=True, finite=True, real=True)

W=sp.factor(2*H**2*M2**2/(Kc*MK2))
r=sp.factor((6*H**2*M2-Kc)/(4*H**2*M2))
U=sp.factor(r**2*W)
V=sp.factor(r*W)

Ue=sp.factor((6*H**2*M2-Kc)**2/(8*Kc*MK2*H**2))
Ve=sp.factor(M2*(6*H**2*M2-Kc)/(2*Kc*MK2))
assert sp.simplify(U-Ue)==0
assert sp.simplify(V-Ve)==0

lim_H2U=sp.limit(H**2*U,H,0,dir='+')
lim_V=sp.limit(V,H,0,dir='+')
lim_W=sp.limit(W,H,0,dir='+')
assert sp.simplify(lim_H2U-Kc/(8*MK2))==0
assert sp.simplify(lim_V+M2/(2*MK2))==0
assert lim_W==0

# Production DBI identity K_clock=2 M_cosm^2 M_K^2.
lim_dbi=sp.simplify(lim_H2U.subs(Kc,2*Mcos2*MK2))
assert sp.simplify(lim_dbi-Mcos2/4)==0

out={
 'classification':'RTK_ROUTE_B_GRADK_STATIC_REGULARITY_GATE_PASS',
 'required':{
   'U':'(6 H^2 M_*^2-K_clock)^2/(8 K_clock M_K^2 H^2)',
   'V':'M_*^2(6 H^2 M_*^2-K_clock)/(2 K_clock M_K^2)',
   'W':'2 H^2 M_*^4/(K_clock M_K^2)'},
 'limit':{
   'H2U':'K_clock/(8 M_K^2)',
   'V':'-M_*^2/(2 M_K^2)',
   'W':'0'},
 'production_DBI':{
   'identity':'K_clock=2 M_cosm^2 M_K^2',
   'H2U_limit':'M_cosm^2/4'},
 'theorem':'For finite positive K_clock/M_K^2, the U coefficient required by the minimal EH+clock grad-K exact cosmological match scales as H^-2 as H approaches zero. With the production DBI identity its H^2 U limit is M_cosm^2/4, so the same scalar carrier does not have a finite-coefficient zero-H continuation.',
 'scope':'This is only the minimal EH+clock grad-K constraint structure. Auxiliary constraints, modified base constraints, a distinct branch with K_clock/M_K^2 scaling as H^2, or a deliberately cosmology-only EFT remain open.',
 'next_step':'Test a regular auxiliary or modified-constraint carrier that avoids the H^-2 coefficient.'}
print('RTK_ROUTE_B_GRADK_STATIC_REGULARITY_GATE_PASS',json.dumps(out,sort_keys=True))
