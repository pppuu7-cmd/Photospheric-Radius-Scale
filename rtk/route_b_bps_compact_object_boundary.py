#!/usr/bin/env python3
"""Exact boundary between the selected Route-B rational-pole family and the
alpha=beta=0 low-energy compact-object regularity subspace.

Primary phenomenology source for the boundary assumption:
  E. Barausse, arXiv:1907.05958 (v4), Introduction.
It summarizes that after GW170817 the low-energy khronometric coupling beta is
bounded at ~1e-15, alpha at ~1e-7 on the generic lambda branch, and that the
slowly-moving black-hole analysis selects alpha=beta=0 for absence of the
reported universal-horizon curvature pathology.

This script proves only the algebraic intersection statement for the selected
BPS exact-rational embedding.  It does NOT elevate the low-energy black-hole
statement into a theorem about the full higher-spatial-derivative UV theory.
"""
import json
import sympy as sp

C,h=sp.symbols('C h', positive=True, finite=True, real=True)
alpha=sp.simplify(2*h/(3*C+h))
ell=sp.simplify(2*h/(3*(1-h)))
z=sp.simplify(h/(3*C))
s=alpha

# Exact selected inverse family is strictly inside alpha>0, ell>0, z>0, s>0
# for C>0 and h>0.  Hence it has no finite-h member in alpha=0.
assert alpha.is_positive is True
assert ell.is_positive is True
assert z.is_positive is True
assert s.is_positive is True

# The only way to approach alpha=0 inside this parameterization is h->0.
assert sp.limit(alpha,h,0,dir='+')==0
assert sp.limit(ell,h,0,dir='+')==0
assert sp.limit(z,h,0,dir='+')==0

# But the BPS low-energy momentum cutoff simultaneously collapses in that
# limit on either algebraic cutoff branch.  Fourth powers are enough.
F_low4=sp.simplify(ell**3/alpha)
F_high4=sp.simplify(alpha**3/ell)
assert sp.limit(F_low4,h,0,dir='+')==0
assert sp.limit(F_high4,h,0,dir='+')==0

# The target sound speed remains exactly C for all h>0, but h=0 itself is a
# singular boundary of the constructive coefficient map (z=ell=alpha=s=0),
# not a member of the proven healthy rational family.
cs2=sp.simplify(ell/(z*(2+3*ell)))
assert sp.simplify(cs2-C)==0

out={
  'classification':'RTK_ROUTE_B_BPS_COMPACT_OBJECT_BOUNDARY_PASS',
  'selected_family':{
    'alpha':'2h/(3C+h)>0','ell':'2h/[3(1-h)]>0','z':'h/(3C)>0','s':'alpha>0',
    'domain':'C>0, 0<h<1'
  },
  'exact_intersection_result':'The selected exact-rational BPS family has no member with alpha=0 at finite h; alpha=0 is reached only as the singular boundary h->0 where alpha, ell, z and s all vanish.',
  'cutoff_boundary':'As h->0, both BPS low-energy momentum-cutoff branch expressions tend to zero in Planck units.',
  'phenomenology_boundary':'Therefore the selected family does not literally intersect the alpha=beta=0 low-energy compact-object regularity subspace quoted in arXiv:1907.05958, except as a degenerate zero-cutoff boundary.',
  'interpretation':'This is a conditional negative intersection result, not a no-go for the full higher-spatial-derivative completion. The UV operators responsible for the Route-B completion may alter the universal-horizon region; that requires a dedicated compact-object calculation.',
  'guards':['does not prove the full UV theory has singular black holes','does not prove low-energy alpha must vanish exactly for all astrophysical solutions','does not fix beta because beta belongs to the matter/effective-metric sector','does not replace a full moving-black-hole solution with the selected higher-spatial operators'],
  'next_step':'Test the observationally allowed small-nonzero-alpha region with the capped cutoff theorem, and separately formulate the moving-black-hole/UV-operator problem for the selected Route-B coefficients.'
}
print('RTK_ROUTE_B_BPS_COMPACT_OBJECT_BOUNDARY_PASS',json.dumps(out,sort_keys=True))
