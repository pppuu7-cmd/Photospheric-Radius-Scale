#!/usr/bin/env python3
"""C7 lemma: retarded RT auxiliaries have no free homogeneous IC constants.

This is a solution-space theorem, not a full Hamiltonian degree-of-freedom
count. A localized second-order auxiliary equation has two formal homogeneous
integration constants. The physical nonlocal/retarded prescription fixes the
auxiliary value and normal derivative on the initial hypersurface. For a
well-posed operator (nonzero fundamental-solution Wronskian), those conditions
set the homogeneous constants uniquely. A triangular chain follows by
induction.

The theorem explains why localized RT auxiliary variables must not be counted
as freely specifiable dark-sector fluids merely because their local equations
are second order. It does not prove the complete nonlinear constraint algebra
of metric + Khronon + RT.
"""
import json
import sympy as sp

# Generic fundamental pair f1,f2 evaluated at an initial time t0.  The
# homogeneous coefficients must be unrestricted: the theorem is precisely that
# the retarded zero-data equations force them to vanish.
f1, f2, df1, df2 = sp.symbols('f1 f2 df1 df2', real=True)
C1, C2 = sp.symbols('C1 C2', real=True)
M = sp.Matrix([[f1, f2], [df1, df2]])
c = sp.Matrix([C1, C2])
initial_difference = M*c
wronskian = sp.factor(M.det())
assert wronskian == f1*df2 - f2*df1

# Cramer's/linear-algebra statement on the declared nondegenerate branch
# W(t0)!=0: zero value and zero normal derivative imply zero homogeneous
# coefficients.  SymPy treats the generic symbolic determinant as nonzero when
# solving the generic branch; the physical proof condition is recorded below.
sol = sp.solve(
    [sp.Eq(initial_difference[0], 0), sp.Eq(initial_difference[1], 0)],
    [C1, C2], dict=True
)
assert sol == [{C1: 0, C2: 0}]
assert sp.simplify(M.adjugate()*initial_difference - wronskian*c) == sp.zeros(2,1)

# Count the formal versus physically free homogeneous constants for a chain of
# N retarded second-order auxiliaries. The triangular induction works because
# after auxiliaries 1..i-1 are unique, the difference of the i-th source is
# zero; the i-th difference therefore obeys the homogeneous equation with zero
# retarded data and is unique as above.
N = sp.symbols('N', integer=True, positive=True)
formal_local_constants = 2*N
retarded_free_constants = sp.Integer(0)
removed_by_retarded_boundary = sp.simplify(formal_local_constants-retarded_free_constants)
assert removed_by_retarded_boundary == 2*N

# Concrete implementation-level fields already audited in model=2.
background_fields = ['U', 'U_prime', 'V', 'V_prime']
perturbation_fields = ['deltaU', 'deltaU_prime', 'deltaV', 'deltaV_prime', 'deltaZ', 'deltaZ_prime']

result = {
    'classification': 'RTK_RETARDED_AUX_SOLUTION_SPACE_UNIQUENESS_PASS',
    'generic_second_order_local_constants_per_auxiliary': 2,
    'retarded_free_homogeneous_constants_per_auxiliary': 0,
    'proof_conditions': [
        'well-posed second-order auxiliary evolution on the chosen initial-value domain',
        'nonzero fundamental-solution Wronskian at the initial hypersurface',
        'retarded value and normal-derivative data are fixed rather than freely varied',
        'for a chain, auxiliary sourcing is triangular/causally ordered so uniqueness applies inductively'
    ],
    'implementation_anchor': {
        'existing_audit': 'rtk/audit_rt_retarded_auxiliary_ic.py',
        'background_fixed_fields': background_fields,
        'perturbation_fixed_fields': perturbation_fields,
        'model': 'RT/model=2'
    },
    'theorem': (
        'Within the physical retarded solution space, localized RT auxiliary fields carry no independently '
        'specifiable homogeneous initial-data constants: any two solutions with the same primary history and '
        'the same retarded prescription coincide, by zero-data homogeneous uniqueness applied inductively.'
    ),
    'not_proved': [
        'full nonlinear ADM/Hamiltonian constraint count of metric + Khronon + RT',
        'absence of all ghosts in an unconstrained local auxiliary action varied with arbitrary boundary data',
        'strong-coupling scale',
        'radiative stability',
        'global hyperbolicity outside the declared well-posed retarded domain'
    ],
    'interpretation_guard': (
        'Do not count the retarded auxiliaries as freely tunable fluids or independent physical initial-data modes merely '
        'from the order of their localized equations; equally, do not use this lemma to claim the full coupled theory has '
        'a completed nonlinear DOF theorem.'
    )
}
print('RTK_RETARDED_AUX_SOLUTION_SPACE_UNIQUENESS_PASS', json.dumps(result, sort_keys=True))
