# RTK Formula Bible — C8 local-U(1) gauge/constraint completion appendix

Updated: 2026-08-22
Status: YELLOW overall; individual algebraic/gauge statements marked below

## Purpose

This appendix records the current local-`U(1) x Diff(M,F)` completion route after the direct standard-universal-matter acceleration carrier failed its scoped BBN/PPN/GW gates.

The point of the U(1) route is not to assert that Hořava-U(1) solves RTK. It supplies an enlarged constraint/gauge architecture that may allow the exact RTK mixed scalar kinetic operator while controlling unwanted gravitational scalar degrees of freedom and static preferred-frame response.

Primary literature used for the explicit gauge transformations and PPN families:

- Kai Lin, Shinji Mukohyama, Anzhong Wang, Tao Zhu, `arXiv:1310.6666`, *Post-Newtonian approximations in the Hořava-Lifshitz gravity with extra U(1) symmetry*.

The paper gives the local U(1) transformation of the shift, gauge field and Newtonian prepotential and exhibits explicit parameter families for which all PPN parameters equal their GR values. This appendix records only the pieces directly used by the executable gates.

## 1. U(1)-invariant shift

Use the convention

`delta_alpha N_i = N D_i alpha`,

`delta_alpha nu = alpha`,

`delta_alpha N = 0`.

Define

`Ntilde^i = N^i - N D^i nu`.

Then

`delta_alpha Ntilde^i = 0`.

For a U(1)-neutral scalar `Sigma`, define

`Theta_U = [dot Sigma - Ntilde^i D_i Sigma]/N`.

Therefore

`delta_alpha Theta_U = 0`,

and a local spatial operator

`C D_i Theta_U D^i Theta_U`

is U(1)-invariant when its coefficient is a neutral state invariant.

CI provenance:

- run `32529835219`;
- artifact `9463470436`;
- digest `sha256:de07dea62ab61573a0395271d4f5c22edad2b5257a1760641b54412104e10f66`;
- source commit `5b5e91571849f54acfe8d0138032a1877a5c37d9`;
- marker `RTK_ROUTE_B_U1_INVARIANT_MIXED_SCALAR_GATE_PASS`.

Status: GREEN for the gauge-invariance statement only.

Non-claims: this does not prove the combined gravity+RTK scalar DOF count, PPN viability, Newton normalization, radiative stability, or the exact nonlinear DBI coefficient map.

## 2. Direct RTK acceleration coefficient in the U(1)-Hořava notation

Use the IR potential convention

`L_V = 2 Lambda - beta0 a_i a^i + gamma1 R + ...`

inside

`S = zeta^2 int N sqrt(g) [L_K - L_V + ...]`,

with

`zeta^2 = M_Pl^2/2`.

Hence the action coefficient multiplying `+a_i a^i` is

`(M_Pl^2/2) beta0`.

The production RTK direct/rolling mixed-kinetic identity is

`K = 2 M_Pl^2 M_K^2`,

so the exact direct acceleration coefficient is

`C_acc = K/(2M_K^2) = M_Pl^2`.

Matching gives

`(M_Pl^2/2) beta0 = M_Pl^2`,

therefore

`beta0_RTK = 2`.

Status: GREEN algebraic dictionary under the stated action normalization.

## 3. Explicit GR-PPN family II — direct RTK slice excluded in scope

The PPN literature displays the exact-GR family

`sigma2 = 4(1-a1)`,

`beta0 = -2(gamma1+1)`.

Canonical IR curvature normalization requires

`gamma1=-1`

because `-L_V` then supplies `+R`.

Thus this family gives

`beta0=0`,

whereas the direct RTK slice requires

`beta0=2`.

Therefore this explicit GR-PPN family does not contain the direct RTK coefficient slice.

Executable source:

- `rtk-class-build:rtk/route_b_u1_ppn_family2_rtk_slice_gate.py`;
- source commit `bb04a706a7742005569dfa5feeb27bc59e42ef8c`;
- workflow commit `343943c6d35404c72bf7dbd830ed846a2bce3065`;
- trigger commit `1ad8f32ce6d857016cc1717d135ac06081df4164`.

Status at writing: YELLOW pending independent CI artifact. The algebra itself is exact and narrow.

Non-claim: this is not a U(1)-completion no-go because a distinct explicit exact-GR family exists and more general matter frames are possible.

## 4. Explicit GR-PPN family I — algebraically open, not certified

A second explicit exact-GR family is

`a1 = kappa = 1`,

`sigma2 = 0`.

These displayed conditions do not themselves fix `beta0`. Therefore adding

`beta0=2`

does not algebraically contradict the three family-I equalities.

This is only an *algebraic opening*. It is not evidence that a fully specified beta0=2 parameter tuple automatically has acceptable PPN behavior once the remaining gravity/matter parameters, static equations and constraint conditions are fixed.

Executable source:

- `rtk-class-build:rtk/route_b_u1_ppn_family1_rtk_slice_gate.py`;
- source commit `21fff2f9911350bd4fe4d701559acaf71821705d`;
- workflow commit `fbab5cb514d7babee97cfc68c12bcd2eae1d84cb`;
- trigger commit `4247ed53d5d9f4d7850318c6ea34a03c6a467fd9`.

Status at writing: YELLOW pending independent CI artifact.

## 5. Why U(1) is not automatically a solution

The current RTK mixed-kinetic chain already proves several constraints that any U(1) implementation must respect:

1. The exact scalar mixed-kinetic law exists in an isolated aligned rank-one sector.
2. A generic misalignment of the ordinary and mixed kinetic field-space directions opens a second scalar kinetic direction.
3. Simply adding an independent healthy companion on top of the existing rolling DBI scalar also opens a second kinetic direction.
4. If the same aligned combination carries the rolling DBI background, it cannot simultaneously be background-silent.
5. Rescaling a separate rolling scalar cannot weaken the exact direct acceleration strength because the invariant product is `C q^2=M_Pl^2`.

Thus a successful U(1) completion must derive the desired one-scalar structure from the *full constrained action*, not append another generic propagating scalar.

## 6. Next preregistered action-level gate

If the family-I and family-II CI gates pass their encoded statements, freeze one concrete nonprojectable U(1) family-I candidate with

`a1=1`, `kappa=1`, `sigma2=0`, `beta0=2`,

plus one explicit choice for every other gravity and matter-frame parameter needed by the IR equations.

Then, without retuning between subtests:

1. derive the static weak-field equations;
2. evaluate the published PPN expressions on the same tuple;
3. derive the complete Hamiltonian/Dirac constraint count after coupling the RTK scalar;
4. require exactly two tensor plus one intended RTK scalar propagating modes in the stated low-energy domain;
5. derive Newton/Friedmann normalization consistently;
6. check the tensor/GW sector;
7. check whether radiative corrections regenerate operators that destroy the exceptional scalar-removal/degeneracy surface;
8. compute the C9 cutoff/strong-coupling scale.

No family-I result is to be called viable before these same-tuple gates pass.
