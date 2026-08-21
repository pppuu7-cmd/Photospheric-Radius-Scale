# RTK Formula Bible

Version: 2026-08-21

## Purpose

Central mathematical reference for reconstructing RTK derivations independently of chat history. This file distinguishes exact/scoped statements from open conjectures. A negative result for one carrier must never be promoted to a no-go for all covariant completions.

## Status notation

- GREEN: derived and/or numerically validated within explicitly stated assumptions
- YELLOW: partial derivation or pending independent audit
- RED: open problem
- BLACK: scoped negative result; excluded only under the listed assumptions

---

# 1. Fundamental action / covariant carrier

The final covariant completion is not yet fixed. The reconstruction target is schematically

S[g_{mu nu}, u^mu, phi, ...]

with a unit-timelike/khronon structure and an IR limit reproducing the tested RTK phenomenology.

Required for any proposed carrier:

1. define all fields and symmetries;
2. state the unit-timelike/foliation constraint;
3. derive the Hamiltonian/constraint structure and degree-of-freedom count;
4. derive the scalar quadratic kernel rather than matching background equations only;
5. recover the fixed Newton normalization and tensor/GW limits;
6. state the EFT cutoff and the domain in which the low-energy action is trusted.

Status: RED for the final carrier.

---

# 2. Background and observationally frozen cosmology

The production cosmology is evaluated on the frozen dense objective

matched-ultra-linstep2+dense-BOSS

with exact-float cache semantics and pinned CLASS/Pantheon/Planck provenance.

Frozen local replay points:

LCDM:

S_eff = 1049.966118347761

RTK:

S_eff = 1050.249912429787

Therefore

Delta S_eff = S_RTK - S_LCDM = +0.2837940820259064.

This is a reproducible local raw-objective difference only. It is not a global optimum statement, posterior preference, significance, AIC/BIC result, or Bayes factor.

Status: GREEN for the frozen local replay; RED/PARTIAL for global model comparison.

---

# 3. Khronon / DBI sector

Implementation invariants that must be preserved:

- physical RTK/Khronon branch uses Omega_cdm = 0;
- any reused upstream CDM slot must be documented as storage, not physical CDM;
- primordial inputs are A_s and n_s, not historical A_s_ad / n_s_ad;
- solve the Khronon gamma normalization with a positive bracketed root; no silent tiny-value fallback;
- preserve Khronon perturbation variables across CLASS approximation-vector recreation;
- unsupported Khronon isocurvature modes must fail closed;
- the controlled implementation has zero leading shear in the relevant sector.

Status: GREEN/YELLOW: implementation is operational, but the final covariant UV carrier is open.

---

# 4. Perturbations and stability

The numerical perturbation implementation is operational in the tested branch, but implementation success is not equivalent to a proof of a healthy UV theory.

Any completion must establish at quadratic order:

- positive kinetic residue (no ghost);
- positive physical gradient term / no gradient instability;
- hyperbolicity on the stated background;
- correct number of propagating degrees of freedom;
- absence of an unwanted extra low-scale mode;
- a cutoff parametrically above all scales used in the cosmological and galaxy calculations.

Status: GREEN for tested numerical perturbation evolution; RED for a final all-background stability/cutoff theorem.

---

# 5. Weak-field transition-radius invariants

The dimensionally correct controlled transition-radius estimate is

r_C ~= (r_M / M_K^2)^(1/3).

The alternative expression (M_K^2 r_M)^(1/3) is dimensionally wrong and must not be reused.

Consequences:

r_C proportional to M_b^(1/6).

In the early DBI scaling regime,

r_C(a) proportional to a^3,

or equivalently

r_C(z) ~= r_C0 (1+z)^(-3).

For the controlled stationary external-condition estimate,

d ln g / d p_ext ~= -(1/6) (r/r_C)^3.

A one-percent sensitivity criterion therefore gives approximately

r < 0.391 r_C.

These are controlled-limit statements, not substitutes for nonlinear environment simulations or lensing fits.

Status: GREEN within the stated controlled limits.

---

# 6. Exact rational / alpha boundary

For the exact rational embedding studied in the current finite-positive-pole construction,

alpha = 2 h / (3 C + h).

For 0 < h < 1 and positive finite denominator,

alpha > 0.

Therefore exact alpha = 0 cannot be obtained inside this specific construction while keeping those assumptions. This is a boundary of that embedding, not an exclusion of RTK itself. A higher-spatial-gradient or other UV completion may change the low-energy universal-horizon/compact-object conclusion and must be tested explicitly.

Status: BLACK scoped boundary.

---

# 7. Scoped lapse-only two-derivative carrier no-go

Consider the direct ADM/lapse-only ansatz

S = integral N sqrt(gamma) [ M^2(N)/2 R^(3) + A(N) K_ij K^ij + B(N) K^2 + U(N) ].

Exact scalar-kernel matching requires, in the tested mapping,

B/A = - f_K/f_L.

For the RTK target,

- f_K/f_L = (2 + X)/(2 - X),

with

X = M_K^2/Q.

At fixed lapse, A(N) and B(N) make B/A independent of Fourier momentum, while the RTK right-hand side is k-dependent through Q. Therefore this simple lapse-only, two-derivative carrier cannot reproduce the exact RTK scalar kernel over the full Fourier axis.

This proves only a scoped no-go for this ansatz. It does not exclude full DHOST, mixed derivative operators, higher-spatial-gradient terms, additional fields, or other covariant carriers.

Status: BLACK scoped no-go.

---

# 8. Route-B U-DHOST PPN algebra and minimal-branch obstruction

Use the pinned workbench relations

beta_3 = gamma^2,

g_1 = -2 G_GW (beta_1 + beta_3 + 2 - gamma),

g_2 = -2 G_GW beta_1,

where

gamma = G_GW/G_N.

The preferred-frame parameter is represented as

alpha_1 = 4 [ 2 gamma - ((1-g_1)(1-g_2))/(1-g_1-g_2) ].

For the minimal beta_1 = 0 branch the rational factor reduces to unity, giving

alpha_1 = 4 (2 gamma - 1).

Thus small alpha_1 requires gamma approximately 1/2, while the Route-B phenomenological regime of interest lies near gamma approximately 1. Under this closure the minimal direct branch is therefore incompatible with the required PPN regime.

For nonzero beta_1, define

A0 = (1 - alpha_1/4)/(2 gamma).

The algebraic rescue condition becomes

beta_1^2 + [(gamma^2 + 2 - gamma) - A0] beta_1
+ A0/[gamma(A0-1)] = 0.

At gamma = 1 and alpha_1 = 0 the roots are not real, so there is no exact real rescue at that point. For gamma slightly below one, narrow real algebraic windows can appear. Real roots alone are not a viable theory: the exact U-DHOST closure, denominator exclusions, stability, PPN bounds, Newton normalization and GW constraints must all be imposed simultaneously.

Status: BLACK for the minimal beta_1=0 branch under the pinned closure; YELLOW for the narrow nonzero-beta_1 algebraic window.

---

# 9. Route-B acceleration-sector mapping

With the acceleration operator

alpha_ax a_i a^i

and the khronometric-style candidate relations

beta_1 = -c_sigma/c_omega,

beta_2 = -c_theta/3,

beta_3 = gamma^2,

one obtains the acceleration coefficient

alpha_ax = c_a/(1-c_a/2).

For the tested mode relation

p/(1-q) = R_c^2 M_K^2,

solving for p yields

p = R_c^2 M_K^2 / (1 - beta_1 R_c^2 M_K^2).

With c_a = beta_3 p,

alpha_ax = beta_3 R_c^2 M_K^2 /
[1 - beta_1 R_c^2 M_K^2 - (beta_3/2) R_c^2 M_K^2].

At this level the expression is independent of beta_2. This is a diagnostic relation, not a proof that beta_1, beta_2 and beta_3 are independent in a regular exact U-DHOST completion.

In particular one must not impose beta_3 = 2 gamma without deriving the independent F3/(X A1)-type ratio of the chosen covariant theory.

Status: YELLOW diagnostic boundary.

---

# 10. Observational pipeline and robustness gates

Operational chain:

Theory -> CLASS -> Planck + Pantheon + dense BOSS -> exact objective -> local stationarity/replay.

Current high-value robustness gates:

- B4: minimal-neutrino paired stationarity/recenter validation — OPEN;
- B6: paired AlterBBN differential abundance robustness — CLOSED under its frozen paired protocol; see section 14;
- B9: matched/reoptimized lensing comparison — OPEN; fixed-center lensing is diagnostic only;
- B10: profiled lambda_D identifiability and multiscale fixed-lambda stationarity — OPEN;
- A6: BIC/Bayes/posterior-level model comparison — OPEN.

Status: mixed; never infer global model preference from any one robustness gate.

---

# 11. Completion frontier

The main theoretical frontier is not another local cosmological optimizer pass. It is:

1. C7: construct a broader healthy carrier/completion;
2. C8: derive an exact UV/IR interpolation whose scalar kernel reproduces the RTK target in its validity domain;
3. C9: compute the EFT cutoff / strong-coupling scale;
4. close B4/B9/B10 on matched frozen protocols while retaining B6 as closed differential robustness;
5. connect the controlled galaxy/weak-field sector to nonlinear environment and lensing data without inserting a linear cosmological environmental field by hand.

Candidate completion classes still open include higher-spatial-gradient, mixed-gradient/mixed-derivative and full-DHOST constructions, provided their degeneracy and stability conditions are derived rather than assumed.

Status: RED.

---

# 12. FLRW constraint kernel and exact Schur-complement gate

The fixed-Minkowski obstruction cannot automatically be extended to a fixed-action FLRW background because background quantities can enter the nondynamical constraint kernel. A representative healthy-Horava-style lapse kernel has the structural form

D_phi(p,H) = 3(3 lambda - 1) H^2
             - eta p^2
             - eta_2 p^4/M_Pl^2
             + eta_4 p^6/M_Pl^4.

For a simple root y=p^2 defined by D_phi(y,H)=0,

d y_pole / d(H^2)
= -3(3 lambda - 1) / [d D_phi / d(p^2)],

which is generically nonzero. In the two-spatial-derivative truncation eta_2=eta_4=0,

p_pole^2 = 3(3 lambda - 1) H^2 / eta.

Therefore fixed Wilson coefficients do not imply a fixed effective pole on FLRW.

This structural fact is still insufficient for RTK matching because lapse and scalar shift must be eliminated together. Let

x = (delta N, chi),

M(q,H) = [[A,C],[C,B]],

J(q,H) = (P,R),

and write the quadratic scalar sector as

L = 1/2 x^T M x + x^T J zeta + 1/2 K0 zeta^2.

The nondynamical equations are

M x + J zeta = 0,

hence

x = - M^{-1} J zeta.

Substitution gives the exact Schur complement

K_eff(q,H)
= K0(q,H)
- [B P^2 - 2 C P R + A R^2]/[A B - C^2].

Define

D(q,H)=A B-C^2,

N(q,H)=B P^2-2 C P R+A R^2.

The zero of D controls a constraint-pole location, while N/D controls its rational remainder/residue. Matching D alone is therefore not an RTK completion test.

For the diagnostic linear-in-q form

A=a0+a1 q,
B=b0+b1 q,
C=c0+c1 q,

the determinant is

D=D0+D1 q+D2 q^2,

with

D0=a0 b0-c0^2,

D1=a0 b1+a1 b0-2 c0 c1,

D2=a1 b1-c1^2.

A strict target with one linear denominator has the necessary algebraic condition

D2 = a1 b1-c1^2 = 0.

This condition is only a constraint-determinant condition. It must not be called DHOST degeneracy unless a specific covariant action has been mapped to A,B,C and its full degeneracy/constraint algebra has been derived.

For a linear denominator D=D0+D1 q with D1 nonzero, the invariant numerator remainder after division by D is N evaluated at

q_pole = -D0/D1.

Thus a viable C8 candidate must match, using one fixed underlying coefficient tuple across multiple epochs:

1. denominator/pole;
2. rational residue/remainder;
3. physical kinetic sign;
4. gradient stability/hyperbolicity;
5. degree-of-freedom count;
6. IR recovery and EFT cutoff;
7. PPN/Newton/GW constraints.

Canonical algebraic tool: `rtk/route_b_flrw_schur_kernel.py` on `rtk-class-build`.
Canonical protocol: `research/RTK_C8_FLRW_SCHUR_MATCHING_PROTOCOL_2026-08-21.md` on `rtk-class-build`.

Status: GREEN for the exact Schur algebra and necessary single-linear-pole condition; YELLOW/RED for mapping a fixed healthy action to the full RTK pole+residue target.

---

# 13. Derivation and provenance discipline

Every new formula admitted to this Bible must carry enough information to reconstruct it without a chat transcript. At minimum record:

1. starting action/equations or frozen numerical definition;
2. field/gauge/Fourier conventions and dimensional definitions;
3. algebraic substitutions or elimination steps;
4. assumptions/limits used;
5. exact domain of validity;
6. symbolic/numerical verification tool when available;
7. source file, commit/workflow/run provenance;
8. status GREEN/YELLOW/RED/BLACK;
9. explicit statement of what the result does not prove.

Corrections are append-and-explain operations. If an older formula is dimensionally or algebraically wrong, retain enough chronology to show why it changed; do not silently rewrite the project's history.

The current canonical state split is:

- formulas and derivations: `research/methods/RTK_FORMULA_BIBLE.md`;
- current scientific gate state: `research/RESEARCH_LEDGER.md`;
- chronological development: `research/RTK_MODEL_CHRONOLOGY.md`;
- compute architecture/provenance: `docs/RTK_COMPUTE_ARCHITECTURE.md` and `docs/COMPUTE_LOG.md`.

Status: GREEN methodological rule.

---

# 14. B6 paired AlterBBN differential-abundance closure

The B6 gate isolates only the effect of the RTK expansion-history perturbation on primordial abundances. Reference and RTK use the same frozen baryon ratio, radiation semantics, nuclear network, compiler/runtime settings and abundance parser; the scientific difference is the injected ratio

R_H(T) = H_RTK(T)/H_reference(T).

At the preregistered massless A1-A5 point,

eta = 6.122532926262666e-10,

and the mapped expansion perturbation satisfies

max |R_H-1| = 2.422446243599552e-09

over the injected BBN temperature interval.

For each abundance X define the paired shift

delta_X = X_RTK - X_reference.

The primary shift is the refined 512-point table at AlterBBN failsafe=1. Numerical sensitivity is

noise_X = max(
 |delta_refined,f1 - delta_nominal,f1|,
 |delta_refined,f1 - delta_refined,f7|
).

A nonzero shift is declared numerically resolved only if

|delta_refined,f1| > 5 noise_X.

Otherwise the physical statement is not `delta_X=0`; the retained conservative bound is

|delta_X| <= |delta_refined,f1| + 5 noise_X.

Results:

- Yp: `delta = +1.4314660568004456e-12`, numerically resolved; conservative bound `1.5052958879380185e-12`;
- D/H: `delta = +1.6226982865047423e-15`, unresolved; conservative bound `4.560750648668899e-15`;
- He3/H, Li7/H, Li6/H and Be7/H are also unresolved under the same preregistered rule and retain explicit conservative bounds in the canonical B6 result document.

With the observations frozen before the output,

Yp_obs = 0.2458 +/- 0.0013,

(D/H)_obs = (2.533 +/- 0.024)e-5,

the RTK perturbation changes the standardized residual by only about

1.10e-9 sigma for Yp

and

6.76e-9 sigma for D/H.

Therefore the RTK modification to H(T) is observationally negligible in this paired B6 sense.

Important scope boundary: the reference AlterBBN value itself gives approximately `z=-4.706` for the frozen D/H observational sigma, so this gate is not an absolute BBN goodness-of-fit certification. It isolates the differential RTK effect and does not include a full nuclear-rate/theory-error likelihood, refit eta, solve the lithium problem, or provide model evidence.

Canonical result: `research/robustness/RTK_B6_ALTERBBN_RESULT_2026-08-21.md`.
Workflow run: `32285359564`, attempt 2; artifact id `9447623417`.

Status: GREEN for differential B6 abundance robustness under the frozen protocol; absolute BBN likelihood remains a separate future gate if required.
