# RTK U(1) fixed-action frontier — 2026-08-22 17:05 +03

Status: **classically open/strongly narrowed; radiative protection, full 1PN preferred-frame sector, strong coupling and compact objects remain open**.

This checkpoint is deliberately chat-independent. It supersedes any intermediate C8 reasoning that treated the RTK mixed coefficient as lapse-independent off shell or used a scalar-derivative-free `p_Sigma=0` slice after the fixed action acquired `C(X_U) proportional to 1/X_U`.

## 1. Frozen IR representative

Current low-energy gravity/matter-coupling representative:

- `a1=1`, `a2=0`, `kappa=1`;
- `sigma1=sigma2=0`;
- `beta0_bare=0`;
- `gamma1=-1`;
- `lambda_HL=1` as an IR representative, not a UV completion.

Canonical file: `research/RTK_C8_U1_FIXED_IR_REPRESENTATIVE_v3.json` on `rtk-class-build`.

The published nonprojectable U(1) PPN family with `a1=kappa=1` admits GR PPN values and does not constrain `lambda_HL`. This literature fact is only imported where the full fixed RTK scalar action has been shown to reduce to the same source/operator structure.

## 2. Fixed scalar action

Define

`Theta_U = [dot Sigma - (N^i-N D^i nu) D_i Sigma]/N`,

`X_U = 1/2 [Theta_U^2-D_i Sigma D^i Sigma]`.

The production RTK background is reproduced by the shift-symmetric purely kinetic action

`P_8piG(X_U)=2 mu_K^2/lambda_D * [1-sqrt(1-lambda_D (sqrt(X_U/X_star)-1)^2)]`,

with smooth `lambda_D -> 0` limit

`P_8piG -> mu_K^2 (sqrt(X_U/X_star)-1)^2`.

The mixed coefficient is frozen as

`C(X_U)=M_Pl^2/(2 X_U)`.

Production domain: `X_U>0`. The singular limit `X_U->0` is outside the currently certified branch and is an explicit compact-object/nonlinear gate.

Canonical file: `research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json`.

## 3. Exact background and static identities

The reconstruction satisfies exactly on the production trajectory:

- `P=p`;
- `2 X P_X-P=rho`;
- `2 X P_X=rho+p`;
- `c_s^2=dp/d rho=c_a^2`;
- `K_phys=2 M_Pl^2 M_K^2`.

DBI reconstruction Actions run `32568038426`, attempt 2: **SUCCESS**.
Static-clock consistency run `32568097865`, attempt 2: **SUCCESS**.

For a static zero-shift timelike clock with `D_i Sigma=0`,

`X_U=Theta_U^2/2`, `D_i Theta_U=-Theta_U a_i`.

Therefore the fixed mixed operator reduces **exactly** to

`C(X_U) D_iTheta_U D^iTheta_U = M_Pl^2 a_i a^i`

at all lapse orders, as long as `X_U>0`.

Exact-static Actions run `32568207582`, attempt 2: **SUCCESS**.

This exact identity supersedes the intermediate fixed-C calculation that found a cubic difference between `(1+n)^-3` and `(1+n)^-1`. That mismatch belonged to holding `C` artificially fixed during lapse variation and is not a property of the final `C(X_U)` action.

## 4. Velocity support, Noether identity and classical DOF

The fixed `C(X_U)` operator does not give canonical time velocities to lapse, shift, U(1) gauge field, prepotential or the spatial metric. Fixed-C(X) velocity-support Actions run `32568412562`: **SUCCESS**.

The invariant-shift Noether identity is functional rather than constant-coefficient-specific: for local `L(v,Dv,neutral jets)`, with `v=N^i-N D^i nu`, the `nu` equation is the spatial divergence of the shift equation. Hence allowing `C=C(X_U)` does not invalidate that identity.

An earlier generic coupled-rank slice used `p_Sigma=0`. After freezing `C(X_U)=M_Pl^2/(2X_U)`, that slice approaches `X_U=0` and is not a valid regular fixed-action certification. It is superseded.

The replacement regular slice has `X_U=X0>0`, `D_iSigma=D_iTheta_U=0`, finite `C(X0)`, and nonzero canonical scalar momentum. The Legendre-transformed shift-symmetric `P(X)` Hamiltonian is lapse-linear on this regular slice, while the homogeneous rolling production branch is checked separately.

Fixed-action classical DOF recertification Actions run `32568498574`: **SUCCESS**; artifact `9474707285`. Scoped result in d=3: **3 physical DOF = 2 tensor + 1 intended RTK scalar** on the regular certified phase-space region and rolling branch.

This remains a classical statement. It does not solve radiative detuning, strong coupling, all-background rank, or the `X_U->0` problem.

## 5. Tensor and static weak-field gates

IR quadratic TT run `32567703718`: **SUCCESS**. Scoped two-derivative tensor result: positive canonical TT kinetic/gradient structure and `c_T^2=1`; higher-spatial UV dispersion remains a separate gate.

Static O(v^2) Newton/gamma run `32567850878`: **SUCCESS**. On the frozen family-I representative the solved linear static system gives the GR Newton normalization and `gamma_PPN=1` in the imported weak-field source structure.

ADM-lapse PN-order audit run `32567940387`: **SUCCESS**.

Full `beta_PPN` and preferred-frame `alpha1,alpha2` are **not yet certified** for the complete fixed scalar action. They require the O(v^4) and moving-source source/constraint equations respectively.

## 6. Quantitative local scale separation

Replay-certified scale dictionary run `32568333920`: **SUCCESS**, artifact `9474667297`, digest `sha256:7337f02e8f217e22decf8b425e87e9f730cb3189fa1baad981c8b5ae566f74e8`.

At z=0 it gives

- positive CLASS root `gamma=0.05170371280716`;
- `mu_K=1.572550669049847e-4 Mpc^-1`;
- `M_K=1.1681315109161161 Mpc^-1`;
- `M_K^-1=0.8560679946179539 Mpc`;
- `c_a^2=1.4738358401883835e-8`.

Using the exact identity `K_phys=2 M_Pl^2 M_K^2`, define the hierarchy against a local spatial gravity operator by

`epsilon_clock = K_phys/(M_Pl^2 k^2) = 2(M_K/k)^2`.

Representative values:

- solar radius: `1.3873e-27`;
- 1 AU: `6.4145e-23`;
- 100 AU: `6.4145e-19`;
- 1 pc: `2.7291e-12`;
- 1 kpc: `2.7291e-6`.

A dedicated CI gate has been launched to freeze this as a scale-separation theorem. These numbers do **not** by themselves set a PPN parameter; they justify treating local P(X) background stiffness as parametrically tiny compared with local spatial gradients before solving the full PPN equations.

## 7. C9 and remaining failure modes

The exceptional gravity surface `sigma1=sigma2=0` remains technically unnatural under the cited Hamiltonian analysis because the associated marginal operators are expected to be radiatively generated. Current classification remains:

`CLASSICALLY_OPEN_BUT_RADIATIVE_PROTECTION_REQUIRED`.

Mandatory remaining same-action gates include:

1. complete static O(v^4) / `beta_PPN` derivation;
2. moving-source preferred-frame `alpha1,alpha2`;
3. radiative protection/RG/counterterm analysis of `sigma1=sigma2=0` and of the fixed scalar functions;
4. strong-coupling/EFT cutoff;
5. higher-spatial tensor/UV dispersion;
6. nonlinear and compact-object evolution, especially whether physically relevant solutions approach `X_U=0`;
7. environmental/galaxy nonlinear connection.

No one of these failures, if encountered, should be promoted to a no-go for RTK outside the explicitly frozen U(1) fixed-action architecture.

## 8. Numerical robustness frontier at this checkpoint

B9 RTK Planck-lensing local stationarity is independently fresh-tree certified: run `32564687851`, exact `S=1059.2719553175134`, improvement `0`, PD Hessian with minimum eigenvalue `5.825694e-4`, replay error `0`.

B9 LCDM v3 run `32564665932` found exact descent `0.05793626365493765 > 0.005`, so recenter-v4 is mandatory. Frozen v4 target commit `26997b005bd9d6930d4446626a4b2e8cfa2e55f7`; workflow commit `01ec47309818e305cd0a7a85f7c229216c36d24e`; launch commit `10b2381305b1cb00dfee41d8424413b7e7eaf7cb`.

B4 minimal-neutrino v4 base run `32565150038` is exact-recenter-clear (`best improvement=7.20729706245038e-5`) but has one soft negative Hessian mode `lambda_min=-6.643686349509472e-5`, overwhelmingly aligned with `loglambda`. The preregistered response is exact eigenmode-ray falsification at the same scale, not a minimum claim. Frozen ray target commit `3107e561f5daa3ce42181401eb3fddec2437036b`; worker `bea93400f9b371e2ee8bf03e437ff977e8328a0d`; workflow `22dd983482be0254b14f26ef49176fbecbe4ec85`; launch `36c3b9ffad85b82663b692ed2affad80e038518e`.
