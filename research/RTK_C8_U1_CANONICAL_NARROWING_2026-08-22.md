# RTK C8 U(1) canonical narrowing — 2026-08-22

Status: **YELLOW / classically narrowed; full coupled DOF rank still open**

## Scope

This note records the action-level narrowing of the nonprojectable local-U(1) completion route. It does not promote the route to a physical completion. The same candidate must still pass the complete coupled Dirac rank, static/Newton/PPN, tensor/GW, radiative, cutoff/strong-coupling and nonlinear/compact-object gates.

## Literature identities used

For the universal IR matter coupling of Lin, Mukohyama, Wang and Zhu, arXiv:1310.6666,

`Nbar = F(sigma) N`, `gbar_ij = Omega(sigma)^2 g_ij`,

with `F=1-a1 sigma`, `Omega=1-a2 sigma` and `a1,a2` arbitrary coupling constants.

For `sigma1=sigma2=0`, their Eq. (5.43) is

`beta0 (a1^2 kappa gamma1 + 1) + 2 kappa (a1 gamma1 + 1)^2 = 0`.

On the published exact-GR PPN family-I condition `a1=kappa=1`, this factorizes exactly as

`(gamma1+1) [beta0 + 2(gamma1+1)] = 0`.

Hence the canonical curvature branch `gamma1=-1` satisfies Eq. (5.43) identically and does not force `beta0=0`; it therefore algebraically admits the direct RTK normalization `beta0=2`. The other factor gives `beta0=-2(gamma1+1)` and yields `beta0=0` at `gamma1=-1`.

The paper separately states that `a1=kappa=1` reduces the displayed PPN parameters to their GR values. This is a literature branch statement, not an independent RTK static-field solution.

For the Hamiltonian structure, Mukohyama, Namba, Saitou and Watanabe, arXiv:1504.07357, show that the nonprojectable U(1) gravity scalar is absent classically iff the two coefficients of `a_i a^i sigma` and `D_i a^i sigma` vanish exactly. On that exceptional surface the Poisson bracket between `pi_N` and `J_A` vanishes identically, so preservation in time yields two extra secondary constraints `H_perp` and `phi_A` which remove the scalar-graviton canonical pair.

The same paper emphasizes that the two operators are marginal and expected to be regenerated radiatively. Thus the exceptional surface remains technically unnatural absent additional protection.

## Frozen partial IR slice

The current partial slice is frozen at

- `a1=1`;
- `a2=0`;
- `kappa=1`;
- `sigma1=sigma2=0`;
- `beta0=2`;
- `gamma1=-1`;
- `lambda_HL` intentionally **unfrozen** pending the coupled constraint calculation.

Canonical file: `rtk-class-build:research/RTK_C8_U1_FAMILY1_FIXED_IR_SLICE_v1.json`, commit `73ac2bb8c7cbee06d525b3af43acccffef3c0d34`.

`lambda_HL` is not chosen by hand because doing so before the coupled DOF calculation would violate same-action discipline. The next Hamiltonian gate must keep it symbolic and derive an admissible domain before one complete tuple is frozen.

## Executable gates completed

### Eq. (5.43) fixed-slice factorization

Source commit `8ea66e5fa6722427ba0bbf20e4730477a35bc268`; workflow commit `2afbb1bdbdb5def9ad64cd02cf1805b0864f0565`; trigger `caa0897c4df7d9fbb68ccbf29294c5a96e034e34`.

CI run `32565270839`: **success**. Artifact `9473907426`, digest `sha256:f5ca513ee4cc6a8bf5db02b08725dfbee87bb7dfdc233fecaba525e8ef41a021`.

Classification: `RTK_ROUTE_B_U1_FAMILY1_EQ543_FIXED_SLICE_PASS`.

### RTK mixed-operator velocity support

For `Theta_U=[dot Sigma-(N^i-N D^i nu)D_i Sigma]/N`, the operator `C D_i Theta_U D^i Theta_U` has scalar velocity support through `dot Sigma` and `D_i dot Sigma`, but no `dot N`, `dot N^i`, `dot A`, `dot nu` or `dot g_ij` support. Its scalar/gravity velocity cross-Hessian entries vanish at this jet level.

Source commit `490f92018f22d93615095fb3d061f964e065d8b8`; workflow `80af6e4e46cfada46ae0fcd175b936cdcf5fa8c0`; trigger `b585abee3481e9c85760e6a211cc75b5eac728e7`.

CI run `32565318332`: **success**. Artifact `9473919972`, digest `sha256:40706765440f4c66091eb83d29c468a7e585a08d84f3768bdb2c6f0d62d6423d`.

Classification: `RTK_ROUTE_B_U1_MIXED_VELOCITY_SUPPORT_GATE_PASS`.

This proves only that the mixed operator itself does not kinetically activate the U(1) multiplier/gauge variables. Secondary constraints can still change.

### Why `a2=0` is structurally preferred

For `a2=0`, the physical spatial metric equals `g_ij`, so a generic matter Hamiltonian already Legendre-transformed in its own variables has ADM form

`H_m = Nbar H_0 + Nbar^i H_i`

with `H_0,H_i` independent of `N,A,dot nu`. Using the published universal frame,

`Nbar = N-a1(A-Acal)`

is affine in lapse, gauge field and prepotential velocity. Exact symbolic algebra gives

`p_nu^m + J_A^m = 0`,

and

`d J_A^m/dN = 0`.

Thus `a2=0` is no longer merely the simplest arbitrary representative: it is structurally motivated because it prevents hidden `sigma` dependence of the physical spatial metric from feeding `A/N/dot nu` dependence into the matter Hamiltonian generators.

Source commit `816aaf48c1cf0e2e6286ed0121a43ae4697749dc`; workflow `8b9eda8a0eb0a3fa45cff1fe61835d986e167c6a`; trigger `14685a1407d767cdd07e024b70b13979286c0cbe`.

CI run `32565392364`: **success**. Artifact `9473937737`, digest `sha256:c8fac75e2f8fb2e968265705d7d998b382440efb87c1aa60eb61b2112cd73492`.

Classification: `RTK_ROUTE_B_U1_A2ZERO_CANONICAL_AFFINITY_GATE_PASS`.

Non-claim: this does not prove that every `a2 != 0` matter sector fails.

## Coupled primary identity gate

The next executable gate combines:

1. the exceptional pure-gravity identity on `sigma1=sigma2=0`;
2. the `a2=0` ordinary-matter identities above;
3. the neutral RTK Sigma sector, whose `Theta_U` construction carries no direct `A` or `dot nu` support.

The target statement is that the total primary combination `p_nu+J_A=0` and the vanishing `dJ_A/dN=0` condition survive coupling. Passing this would establish the algebraic prerequisite for the two extra secondary constraints, but **not** their independence or Poisson rank.

Source commit `9a5ec7125ab2ed0433a6136cdaa44c7b5375a16f`; workflow `94dca8b407b73cc9cf410440fc8c6f3fbb3f7206`; trigger `e6f5c45b64411d255d40f57c8babbe5112b786e4`.

## Next mandatory C8 gate

Derive the Sigma-source modifications of `H_perp` and `phi_A`, then compute the coupled second-class Poisson submatrix/rank with `lambda_HL` symbolic. Only if the two modified constraints remain independent and remove the unwanted gravity scalar may `lambda_HL` be restricted and one **complete** action tuple frozen.

Even a classical DOF pass leaves C9 radiative protection mandatory because `sigma1=sigma2=0` is not technically natural under the cited Hamiltonian analysis.
