# RTK Research Iteration Chronology

Status: canonical append-only iteration timing log
Created: 2026-08-21

Purpose: record the wall-clock start of each assistant-driven research iteration separately from the scientific model chronology. This prevents ambiguity about when a reasoning/repository cycle began. Scientific conclusions remain in `research/RESEARCH_LEDGER.md`, formula derivations in the Formula Bible, and major model evolution in `research/RTK_MODEL_CHRONOLOGY.md`.

Rules:

1. Record the start time as stated at the beginning of the user-facing research iteration.
2. Store both user-local time with UTC offset and UTC.
3. Record the main frontier entered at iteration start.
4. Add commit/run/artifact IDs produced during the iteration when available.
5. Record CI implementation failures separately from scientific failures.
6. This timing log is provenance only; its timestamps do not imply scientific completion.

---

## Iteration started 2026-08-21 23:32:00 UTC+03:00 / 2026-08-21 20:32:00 UTC

User instruction: continue research and explicitly record the time at which the response/research iteration began.

### Frontier at start

- B4 target-v2 half-scale Hessian run `32514077002` still in exact Hessian step.
- B9 RTK recenter base Hessian run `32518496348` still in exact Hessian step.
- B9 LCDM interrupted-recenter base Hessian run `32522002655` still in exact Hessian step.
- C8 corrected TT-safe grad-K basis already CI-verified.
- C8 minimal EH+clock grad-K zero-H regularity obstruction already CI-verified.
- C8 algebraic auxiliary-rank and pure K^2 deformation gates had been launched.

### Algebraic auxiliary-rank result

Run `32523115561` completed successfully.

- artifact `9461246849`;
- digest `sha256:de8b3b6c49d7eb48321ed964059a048a168a818e5b7a521c66f0b8e4ddc84bc6`;
- source `4d8a93f902da53d0a51886080865d353151ccd60`;
- marker `RTK_ROUTE_B_GRADK_AUXILIARY_RANK_GATE_PASS`.

For `C_eff=C-b^T M^{-1}b`, finite regular coefficients and a finite nonsingular auxiliary matrix at `H=0` cannot generate the required `H^-2` reduced coefficient. Generating it through an algebraic auxiliary requires either a singular/divergent unreduced coefficient or an eigenvalue of the auxiliary Hessian approaching zero. Scope: regular algebraic auxiliaries only.

### K^2 / Hořava-lambda deformation result and CI correction

The exact polynomial identity gives the `p^2`-polynomial constant coefficient

`-K_clock^2 M_*^2 M_K^2 eta`.

Thus for finite nonzero physical scales exact RTK matching forces `eta=0` independently of `(U,V,W)`.

The initial CI run `32523351127` failed for an implementation-only reason: the script declared `eta` with the SymPy assumption `nonzero=True` and then asked SymPy to solve for the theorem solution `eta=0`. The analytic coefficient assertions before that line passed. This was **not** a scientific failure.

The guard was corrected in source commit `a5744e9ab4f8cf54d1e376e61a08a17f331305e4` and retriggered by `7d46a4ce28ec328e1c93d79318aa75f995ae22d4`.

Corrected run `32524954554` completed successfully:

- artifact `9461843454`;
- digest `sha256:48a693ffb07afd02d0de5c93b05892c0449c33f39c205fa3ce67ac9fe3972de1`;
- artifact source HEAD `65189ecbcf45b24bb654cbb522489e85f84fa307`;
- marker `RTK_ROUTE_B_GRADK_K2_DEFORMATION_GATE_PASS`.

Scientific classification: BLACK scoped result for the pure `K^2` deformation with unchanged clock sector; broader modified constraints remain open.

### Minimal dynamical auxiliary result and CI correction

Added `rtk-class-build:rtk/route_b_gradK_dynamic_auxiliary_pole_gate.py` initially at commit `66b0c726e0acdff52ef7accb48d870c4dd9fb2a7`.

For

`L = 1/2 K0 X^2 + b X y + 1/2(A-Z omega^2)y^2`,

elimination gives

`K_eff = K0 - b^2/(A-Z omega^2)`

with an extra pole

`omega_aux^2=A/Z`

and residue `b^2/Z` for finite nonzero `b,Z`.

The initial run `32524560684` failed only because the assertion required one literal denominator sign while SymPy returned the equivalent common-negative form `-A+Z omega^2`. Pole and residue identities were unchanged. Source commit `65189ecbcf45b24bb654cbb522489e85f84fa307` changed the guard to accept an overall `+/-1`; trigger commit `79abae881a87ff05dc709ff65ab7b3e2884be22f` launched the corrected run.

Corrected run `32524978316` completed successfully:

- artifact `9461850988`;
- digest `sha256:9b009bf05fa7f6e4cff7806294ed67e3326dac1980345b987644c82bf64160d3`;
- marker `RTK_ROUTE_B_GRADK_DYNAMIC_AUXILIARY_POLE_GATE_PASS`.

If finite `b,Z` and `A~H^2` are used to generate `b^2/A~H^-2`, the extra mode obeys `omega_aux^2~H^2 -> 0`. Scientific classification: BLACK only for the minimal single nondegenerate dynamical auxiliary.

### Two-positive-auxiliary cancellation theorem

Added source commit `71d198c9454a45f358e5995b0db799432b96ac3f`, workflow commit `b53d9ba6e14a4cb487094ba2b1067d3e204ddfb6`, trigger `27bfd06aa708a0c22f92edb7d6a95647716a222c`.

For `M(omega^2)=M0-omega^2 Z`,

`det M = D0-D1 omega^2+D2 omega^4`,

with

- `D0=det M0`;
- `D1=tr(adj(M0) Z)`;
- `D2=det Z`.

For `M0>0` and nonzero `Z>=0`, `adj(M0)>0` and therefore `D1>0`. Rank-one `Z` can remove `D2` but cannot remove the remaining frequency dependence.

Run `32524715584` completed successfully:

- artifact `9461764440`;
- digest `sha256:b67497718867ecf565d944baba13b55a346edf209e9e2bac9b3f42f857047b68`;
- marker `RTK_ROUTE_B_TWO_AUXILIARY_POSITIVE_CANCELLATION_GATE_PASS`.

Scientific classification: BLACK for the ordinary positive two-auxiliary cancellation class. A genuinely Dirac/gauge-degenerate system remains open.

### Constructive Dirac-degenerate one-DOF gate launched

A rank-one kinetic two-field candidate was then constructed:

`L = k/2 (dot X + a dot y)^2 - [1/2 Omega^2 X^2 + g X y + 1/2 m^2 y^2]`.

The velocity Hessian has rank one. The momenta satisfy the primary constraint

`phi1=p_y-a p_X=0`.

Constraint preservation gives

`phi2=(a Omega^2-g)X+(a g-m^2)y=0`.

Their Poisson bracket is

`{phi1,phi2}=m^2+a^2 Omega^2-2ag`.

For a positive-definite potential matrix this is `(a,-1)^T V (a,-1)>0`, so the pair is second class. Four-dimensional phase space minus two second-class constraints leaves exactly one physical configuration-space DOF.

For a source aligned with `v=(1,a)`, define `Q=v^T V^{-1}v`. The exact response is

`v^T(V-k omega^2 vv^T)^{-1}v = Q/(1-kQ omega^2)`.

Thus this genuinely degenerate system has one physical scalar DOF and exactly one finite source-channel frequency pole. It is a constructive escape from the ordinary positive auxiliary pole-count obstruction, but it is not yet an RTK fixed action across momentum/epoch.

Implementation:

- source `rtk-class-build:rtk/route_b_dirac_degenerate_one_dof_gate.py`, commit `bff40e5340d43605cf10dd6ee7eb1d918670ca32`;
- workflow commit `746186301d11c276e71acc138b4a64d984514170`;
- trigger commit `b2934df1715d0fff954e3f64b20234a37b780dc1`.

CI artifact inspection is still required before promotion to GREEN.

### Interpretation guard on the H^-2 coefficient

The proven `U~H^-2` statement is a regularity obstruction for a particular minimal unitary-gauge/EH+clock+grad-K representation. It must not automatically be called physical strong coupling. On a punctured `H!=0` branch a field normalization `X=H chi` converts `(u/H^2)X^2` to `u chi^2`; the transformation itself becomes singular at `H=0`. Therefore the physical question is whether a regular covariant/canonical variable and constraint system exists through the static boundary. Future claims must use canonical kinetic eigenvalues, Dirac rank and cutoff calculations rather than the divergence of one gauge-dependent Wilson coefficient alone.

### Numerical branches during this iteration

At the latest direct check, all three remained in their exact Hessian steps:

- B4 half-scale run `32514077002`;
- B9 RTK recenter base run `32518496348`;
- B9 LCDM recenter base run `32522002655`.

No conclusion is inferred from elapsed runtime.
