#!/usr/bin/env python3
"""C8 scoped obstruction: kinetic alignment versus a rolling background-silent carrier.

Minimal setup
-------------
Let a two-field vector q carry the production background through one rolling
rank-one DBI combination

    Phi = v . q,       dot(Phi_bar) != 0.

Let the mixed-derivative kinetic operator act on

    Sigma = w . q.

The finite-momentum one-DOF alignment theorem requires w to be collinear with v
if both the p^0 and p^2 kinetic matrices are positive rank-one contributions:

    w = c v.

Then automatically

    dot(Sigma_bar) = c dot(Phi_bar).

For a nontrivial mixed term c!=0 and a rolling DBI background, Sigma cannot be
background-silent.  Therefore the minimal aligned two-field construction cannot
simultaneously satisfy:

  1. a rolling DBI background in the same kinetic direction;
  2. one scalar DOF through exact p^0/p^2 kinetic alignment;
  3. a background-silent mixed carrier that removes the direct lapse-gradient
     contribution.

Escapes require a genuinely different architecture: e.g. background stress
carried by a nondynamical/constrained sector, an action-derived cancellation of
the rolling carrier's static acceleration term, or a nonstandard matter/source
frame.  This is not a no-go for those broader classes.
"""

import json
import sympy as sp

c,qdot = sp.symbols('c qdot', nonzero=True, finite=True, real=True)
v1,v2 = sp.symbols('v1 v2', finite=True, real=True)

v = sp.Matrix([v1,v2])
w = c*v
# Treat qdot as the already-projected rolling velocity dot(Phi_bar)=v.qdotbar.
Sigma_dot = sp.simplify(c*qdot)
assert Sigma_dot != 0
assert sp.simplify(Sigma_dot/c-qdot) == 0

# Algebraic wedge vanishes: exact alignment.
wedge = sp.factor(v[0]*w[1]-v[1]*w[0])
assert wedge == 0

out = {
  'classification':'RTK_ROUTE_B_ALIGNMENT_BACKGROUND_SILENCE_OBSTRUCTION_PASS',
  'assumptions':[
    'two-field minimal construction',
    'rolling production background Phi=v.q with dot(Phi_bar)!=0',
    'positive rank-one IR and mixed kinetic pieces',
    'one-DOF alignment w=c v with c!=0'
  ],
  'identity':'dot(Sigma_bar)=c dot(Phi_bar)',
  'obstruction':'A nontrivial aligned mixed carrier cannot be background-silent if the same aligned combination carries the rolling DBI background.',
  'meaning':'The simple idea of using the same linear two-field combination for the DBI background and for a background-silent mixed derivative is internally incompatible under the stated one-DOF alignment assumptions.',
  'escapes':[
    'carry the background stress in a separate nondynamical/constrained sector while the physical mixed combination is background-silent',
    'retain a rolling mixed carrier but derive a same-action static acceleration cancellation',
    'use a nonminimal/disformal matter/source frame that changes the weak-field interpretation',
    'use a broader indefinite/constraint-degenerate kinetic architecture not expressible as a sum of two positive rank-one pieces'
  ],
  'non_claims':[
    'not a no-go for multi-field degenerate theories in general',
    'not a no-go for cuscuton/mimetic/nondynamical background sectors',
    'not a no-go for action-derived PPN screening/cancellation',
    'not a no-go for nonminimal matter frames'
  ],
  'next_step':'Test the two remaining minimal escapes separately: (A) a nondynamical background carrier plus background-silent one-DOF perturbation pair; (B) rolling aligned carrier plus explicit static acceleration cancellation in the full lapse/auxiliary constraint block.'
}

print('RTK_ROUTE_B_ALIGNMENT_BACKGROUND_SILENCE_OBSTRUCTION_PASS',json.dumps(out,sort_keys=True))
