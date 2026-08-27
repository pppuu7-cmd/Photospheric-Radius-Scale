# RTK C10.65s6fU projectable rank-one kinematic embedding theorem

Parent s6fT remains `BLOCKED_NO_FULL_PROJECTABLE_ADM_EMBEDDING_SCOPED`: no full RTK ADM action has been supplied or inferred. This gate instead asks a narrower exact question: what kinematic structure must any local two-scalar projectable-ADM realization of the historical rank-one candidate have?

For normal velocities `v_phi=(dot(phi)-N^i partial_i phi)/N` and `v_chi=(dot(chi)-N^i partial_i chi)/N`, write the general quadratic kinetic density as `N sqrt(gamma)/2 [A v_phi^2+2B v_phi v_chi+C v_chi^2]`. Its velocity Hessian is proportional to `K=[[A,B],[B,C]]`; rank one requires `AC-B^2=0`. On the `A!=0` patch, `a=B/A`, `C=a^2 A`, so the kinetic term is exactly proportional to `(v_phi+a v_chi)^2` and the canonical primary constraint is `p_chi-a p_phi=0`.

For any symmetric algebraic/potential matrix `M`, `det(M-zK)` with `z=omega^2` is affine in `z` on the rank-one locus because the quadratic coefficient is exactly `det K=0`. Thus this kinematic class carries at most one finite dynamical pole unless the remaining affine coefficient also degenerates.

This is only a necessary-structure/constructive kinematic theorem. It does not choose the RTK field map, potential sector, source direction, background coefficient functions or nonlinear Dirac completion; it does not rerun soft-s and does not unblock `k=0.03 Mpc^-1`. The next fixed-action construction must be independently motivated and then rerun s6fT unchanged.
