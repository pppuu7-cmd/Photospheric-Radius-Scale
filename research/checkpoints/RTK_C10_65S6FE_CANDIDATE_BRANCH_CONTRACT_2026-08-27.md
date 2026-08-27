# RTK C10.65s6fE candidate nonlinear completion branch

This gate freezes one explicit hypothesis branch, `MINIMAL_PROJECTABLE_N2_S1HALF_v1`, only so the cubic scalar-shift reduction becomes conditionally well-posed. It is not inferred from the certified linear RTK stack.

The branch keeps the projectable ADM kinetic sector `(Mstar^2/2)(K_ij K^ij-lambda_HL K^2)`, the intrinsic IR sector, and the n=2 carrier `alpha6(X) D_i R3 D^i R3`; it fixes the full local carrier rule to the archived special completion `alpha6(X)=alpha6_0 (X/X0)^(1/2)`. Additional state-dependent shear and mixed K-R/DK operators are absent by branch definition, not because lower-order data proved their absence.

No coefficient is fitted to obtain a desired soft-s outcome. In particular, `nu(X)=0` is a hypothesis of this branch and must not be promoted to a property of RTK in general. `k=0.03 Mpc^-1` production remains blocked.

Next gate: rerun the exact scalar-shift cubic reduction conditionally on this branch and classify the reduced q_s=0 soft-s vertex without changing the prior ZERO/NONZERO semantics.
