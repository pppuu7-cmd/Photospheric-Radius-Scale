# RTK C10.65s6fQ source-locked compensator/spurion audit

Classification: `C10_65S6FQ_NO_SOURCE_LOCKED_COMPENSATOR_PASS_SCOPED`.

The archived fixed U(1) stack was read from commit `13acfdbc16d2f3117f1299b8552bcf7b1f996bd1`. It explicitly source-locks the U(1) rules `delta_alpha N_i=N D_i alpha`, `delta_alpha nu=alpha`, `delta_alpha N=0`, the invariant shift `Ntilde^i=N^i-ND^i nu`, and a U(1)-neutral RTK scalar `Sigma`.

No independent homogeneous spatial-conformal/Weyl transformation law is specified for `nu`, `A`, `Sigma`, or another frozen field. Thus these existing U(1) variables cannot be silently reinterpreted as the compensator/spurion required to evade the s6fO/s6fP soft-weight obstruction. Doing so would be a new nonlinear symmetry/action assumption.

This is not a no-go for enlarged UV completions. It means the current source-locked RTK stack has exhausted the local exact-quadratic-preserving metric/U(1) escape routes checked so far. `k=0.03 Mpc^-1` production remains blocked.

Next frontier: architecture decision between a genuinely enlarged compensator/symmetry completion requiring renewed background/quadratic/DOF certification, or retaining the present field content and accepting the soft-s obstruction as rejection of the minimal nonlinear branch.
