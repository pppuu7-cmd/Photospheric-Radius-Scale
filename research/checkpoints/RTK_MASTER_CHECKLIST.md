# RTK / DBI-Khronon — canonical monotonic master checklist

Created: 2026-08-25 00:24 UTC (03:24 Europe/Helsinki)
Status: **CANONICAL MONOTONIC CHECKLIST v1**

## Governance rule

This is the checklist that must be printed after every research iteration.

1. **Never delete an existing checklist ID or row.**
2. **Never hide a negative or superseded result.** If later work changes its interpretation, retain the old row and add the narrower/new row.
3. Status may be refined, but the historical result/evidence remains recorded.
4. New research questions are appended with new immutable IDs.
5. A row is `CLOSED` only by an explicit analytic theorem/derivation, a regression/precision-controlled numerical result, a frozen observational inference, or a rigorous scoped negative result.
6. A workflow launch is not a scientific result. Missing/pending artifacts are not failures.
7. Local likelihood/stationarity results never imply global preference, significance, AIC/BIC, posterior or Bayes evidence unless a separate frozen protocol explicitly establishes that claim.
8. The repository, not chat memory, is authoritative. Relevant live sources include `research/state/current.json`, package-specific state files, `research/RESEARCH_LEDGER.md`, the Formula Bible and frozen target/result files.

Legend: ✅ closed/pass; 🟥 closed negative/scoped obstruction; 🟨 partial/open; 🔵 active computation/gate; ⏳ queued/deferred; ⚪ governance/infrastructure.

---

## F — Foundations, model identity and analytic invariants

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| F01 | Production DBI/Khronon background and perturbation implementation | ✅ | Operational in pinned RT-CLASS production path; historical cosmological calculations reproducible. |
| F02 | Correct transition radius | ✅ | `r_C ~ (r_M/M_K^2)^(1/3)`; older `[M_K^2 r_M]^(1/3)` expression explicitly withdrawn as dimensionally wrong. |
| F03 | Transition-radius mass scaling | ✅ | `r_C ∝ M_b^(1/6)` in the controlled derivation. |
| F04 | Early DBI transition scaling | ✅ | `r_C(a) ∝ a^3`, equivalently `r_C(z) ~ r_C0(1+z)^-3` in the stated regime. |
| F05 | Controlled stationary weak-field slip/lensing relation | ✅ scoped | Leading `Phi ≈ Psi`; lensing inherits the same leading MOND+mass structure. Full galaxy/cluster lensing fit remains separate. |
| F06 | Controlled external-condition sensitivity | ✅ scoped | `d ln g/d p_ext ≈ -(1/6)(r/r_C)^3`; 1% radius `r < 0.391 r_C`. |
| F07 | Cosmological environment vs local external field | ✅ boundary | Linear cosmological environmental field cannot simply be inserted as a galaxy external field; spatial/nonlinear environmental treatment required. |
| F08 | Production species/source identity | ✅ | In baseline RTK: physical CDM absent; fitted historical key `Om` maps to `Omega_khronon`; ordinary filtered source is baryons+photons+massless relativistic species under current C10 contract. |
| F09 | Canonical Formula Bible / derivation archive | ✅ ongoing | Formula Bible, appendices, chronology and recovery documents exist; update whenever frontier changes. |
| F10 | One complete canonical covariant/fixed action and parameter dictionary for the final completion | 🟨 | Production phenomenology plus candidate/U(1) completion pieces exist, but final same-action completion with all sectors frozen is not yet globally closed. |

## A — Baseline cosmology, likelihood and local numerical certification

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| A01 | Pinned CLASS upstream/source provenance | ✅ | Upstream boundary pinned at `36cf283628c4a3330ec9fd3d84239bf775f77317` for current production family. |
| A02 | Planck likelihood runtime and self-tests | ✅ | Planck baseline runtime and component self-tests operational under pinned stack. |
| A03 | Pantheon covariance / implementation validation | ✅ | Pinned Pantheon provenance and covariance handling validated. |
| A04 | BOSS covariance, units and convention audit | ✅ | Dense BOSS conventions and unit checks established; `eff` and `k01` remain distinct outputs. |
| A05 | Exact-float likelihood/cache semantics | ✅ | Full-precision cache keys; old rounded-`A_s` optimizer-convergence claims withdrawn. |
| A06 | Modern primordial inputs | ✅ | `A_s`,`n_s` enforced; historical `A_s_ad`,`n_s_ad` usage withdrawn. |
| A07 | Positive bracketed Khronon gamma root | ✅ | Silent tiny fallback prohibited; bracketed positive root implemented and replayed. |
| A08 | Preserve Khronon variables across CLASS approximation-vector recreation | ✅ | Production patch/invariant established. |
| A09 | Final dense production objective freeze | ✅ | `matched-ultra-linstep2+dense-BOSS`, mapping `eff`, fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`. |
| A10 | Historical RTK local stationarity | ✅ | Historical RTK accepted point passed base+half local stencil and independent fresh-tree replay. |
| A11 | Historical matched RTK/LCDM fresh-tree replay | ✅ historical | `S_LCDM=1049.966118347761`, `S_RTK=1050.249912429787`, `ΔS=+0.2837940820259064`; local raw-objective comparison only. |
| A12 | Audit historical LCDM stationarity semantics | ✅ | Found historical accepted LCDM score point was not the exact center of its cited Hessian; triggered cross-basin audit rather than silently retaining certification. |
| A13 | LCDM cross-basin line continuation | ✅ | New lower navigation basin found near `t=1.1`; forward continuation recenter-clear in that one-dimensional direction. |
| A14 | LCDM cross-basin base stationarity | ✅ subgate | Base stationarity chain reached the t=1.1 center and advanced to half-scale. |
| A15 | LCDM cross-basin half-scale stationarity | 🟥 recenter required | Half-scale found exact improvement `0.008263249722176624 > 0.005`, best `S=1049.3550570964142`; mandatory recenter. This is not a model failure. |
| A16 | LCDM recenter1 base/conditional half/fresh-tree chain | 🔵 | Must certify the new `S≈1049.3550571` center before any new common paired A5 comparison. |
| A17 | Re-freeze common A5 RTK/LCDM pair after LCDM cross-basin closure | ⏳ | Do not overwrite `research/state/current.json` accepted pair until multiscale stationarity + fresh-tree + common paired replay pass. |
| A18 | Search for an RTK cross-basin analogue after A5 refreeze | ⏳ | B9-neighborhood RTK points do not beat the historical RTK local point, but another RTK basin remains logically possible. |
| A19 | Global minimum claim | 🟨 open | No global optimization theorem/certificate. |
| A20 | AIC/BIC/Wilks/significance | ⏳ separate protocol | Forbidden until final paired objective/minima are re-frozen under a statistic-specific protocol. |
| A21 | Posterior/prior sensitivity/Bayes evidence | ⏳ separate protocol | Not yet performed on a final same-action frozen objective. |

## B — Robustness packages and observational extensions

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| B01 | CLASS precision rescue / ultra objective controls | ✅ | Historical production precision preset frozen and used by accepted dense objective. |
| B02 | Keep alternative RSD mappings (`eff`,`k01`) separate | ✅ | Both retained; never mix scores as identical objectives. |
| B04.1 | Minimal-neutrino objective definition | ✅ | Separate `+nu0p06-additive-v1` objective; absolute scores not compared directly with massless A5. |
| B04.2 | B4 base/half stationarity history | ✅ diagnostic chain | Soft/negative curvature discovered and exact rays used rather than forcing PD certification. |
| B04.3 | B4 v4 half eigenmode rays | ✅ | No exact descent above `0.005`; half-scale non-PD therefore requires preregistered quarter-scale resolution. |
| B04.4 | B4 v4 quarter-scale Hessian | 🔵 | Preregistered/triggered; result file not yet authoritative at this checklist revision. |
| B04.5 | B4 fresh-tree/local closure | ⏳ | Only if quarter-scale decision tree permits it. |
| B05.1 | BOSS linear scale-dependence | ✅ subgate | RTK max relative scale-dependence `1.7612134061906204e-4`, strict sub-percent in the tested linear gate. |
| B05.2 | Survey-window convolution | 🟨 | Required for full B5. |
| B05.3 | Alcock-Paczynski mapping | 🟨 | Required for full B5. |
| B05.4 | Nonlinear RSD template | 🟨 | Required for full B5. |
| B05.5 | Bias marginalization | 🟨 | Required for full B5. |
| B05.6 | Full-shape likelihood or justified bound | 🟨 | Required before B5 can close globally. |
| B06.1 | Entropy-aware BBN `H(T)` mapping | ✅ | `R_H(T)` deviation is at ~`10^-9` level with refinement controls. |
| B06.2 | Paired AlterBBN differential abundances | ✅ | Differential abundance robustness closed; RTK-induced shifts observationally negligible under frozen paired protocol. |
| B06.3 | Absolute BBN goodness-of-fit / nuclear-rate theory / eta refit | 🟨 | Separate from differential B6; reference D/H diagnostic itself is offset under the simplified frozen observational comparison. |
| B09.1 | Standalone Planck R3 lensing interface | ✅ | Pinned likelihood interface validated. |
| B09.2 | Matched RTK lensing stationarity + fresh-tree | ✅ | RTK B9 center locally certified and independently reproduced. |
| B09.3 | Matched LCDM lensing stationarity | ✅ | v7 center locally certified under frozen protocol. |
| B09.4 | Final paired B9 exact replay | ✅ | `S_LCDM=1058.2173424114785`, `S_RTK=1059.2719553175134`, `ΔS=1.0546129060348903`; local robustness only. |
| B09.5 | Global/nonlinear/full-lensing inference | 🟨 | Not authorized by B9-v1 local closure. |
| B10.1 | Fixed-shared lambda-tail reconnaissance | ✅ | Large-lambda tail located; fixed-center flatness treated only as reconnaissance. |
| B10.2 | Profiled T2/T3 + multiscale tail stationarity | ✅ | Factors 64 and 16384 validated. |
| B10.3 | Lambda identifiability protocol v1 | ✅ | `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`; do not reopen without new protocol. |
| B10.4 | Posterior/profile confidence interval/prior sensitivity for lambda | ⏳ | Separate A6-style inference question. |

## C8 — Carrier/completion construction, rank and local gravity

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| C08.01 | Full FLRW Schur-complement rational matching framework | ✅ | Exact lapse/shift elimination and single-pole algebraic rank condition established. |
| C08.02 | Direct local FLRW scalar kinetic carrier | ✅ scoped | Fixed local action reproduces exact rational RTK scalar dispersion in the controlled quadratic FLRW sector. |
| C08.03 | Standard beta=0 universal low-energy Hořava embedding | 🟥 scoped no-go | Healthy positive-finite-Newton exact solution absent on that direct branch. |
| C08.04 | Standard universal matter-frame direct carrier | 🟥 scoped no-go | BBN/PPN/GW-normalization incompatibility on frozen direct slice; does not exclude broader matter/constraint architectures. |
| C08.05 | Minimal static-safe mixed-gradient escape | 🟥 scoped obstruction | Smallest tested basis cannot lower/remove direct static acceleration coefficient while exactly retaining target kernel. |
| C08.06 | Rank-one Dirac one-scalar mechanism | ✅ toy/quadratic | One-DOF theorem and lapse/shift Schur bridge established. |
| C08.07 | Exact mixed-kinetic scalar EFT | ✅ scoped | Reproduces production RTK dispersion in an isolated aligned rank-one sector. |
| C08.08 | Alignment condition for rank preservation | ✅ | Independent kinetic direction generically opens a second scalar; exact rank-one preservation requires aligned directions. |
| C08.09 | Background-silent aligned companion | 🟥 scoped obstruction | Same aligned rolling combination cannot also be background-silent under tested construction. |
| C08.10 | Small-background-speed escape | 🟥 scoped obstruction | Invariant product fixes acceleration-strength issue; small rolling speed alone does not cure it. |
| C08.11 | Local U(1) special-family PPN search | ✅ progressed | Concrete family/tuple work produced GR weak-field PPN quartet on the certified branch. |
| C08.12 | Same-action weak-field PPN quartet | ✅ scoped | `gamma=beta=1`, `alpha1=alpha2=0`, `G_N=G` on the certified weak-field slow-matter rolling branch. |
| C08.13 | Exact k=0 source/background bridge | ✅ scoped | Exact homogeneous mode retained for source/background statements, not as a propagating-rank certificate. |
| C08.14 | Punctured-low-k pure-gravity rank | ✅ | `det B_g ~ B2^2 k^4` on stated special U(1) branch for `0<|k|<epsilon`. |
| C08.15 | General low-k perturbation rank margin | ✅ | Sufficient singular-value/norm bound derived. |
| C08.16 | Neutral-RTK leading-symbol rank hardening | ✅ | Neutral RTK direct correction cannot kill leading punctured-low-k determinant through the certified channel. |
| C08.17 | Filtered-matter symbolic rank/source-separation window | ✅ scoped algebra | Symbolic nonempty-window conditions derived; physical coefficient/source-history verification carried into C10. |
| C08.18 | Local-rest scalar spatial-principal degeneracy | ✅ | Exact `P_X=0`, `c_s^2=0` rest surface; no quadratic `|grad phi|^2` restoring term. |
| C08.19 | Full scalar quadratic rank enhancement at local rest | ✅ | Fully constrained finite-k quadratic RTK scalar action vanishes on the frozen local-rest slice; strong-coupling/constraint-bifurcation warning. |
| C08.20 | First constrained nonlinear order (quartic/time-dependent) | 🟨 | Dedicated quartic/quintic gates were launched; retain results/scopes individually and finish a quantitative cutoff interpretation. |
| C08.21 | Minimal higher-spatial rescue | 🟨 | Scoped rescue bounds/pointwise escapes exist; no broad UV completion theorem yet. |
| C08.22 | Intermediate/high-k full rank/root scan | ✅ scoped pieces / 🟨 completion-wide | Finite-k all-q rank domain later closes for C10 completion family, but final same-action full-history implementation remains open. |
| C08.23 | Compact-object/static strong-field continuation | 🟨 | Weak-field PPN is insufficient; stars/BHs/universal-horizon sector remains open. |
| C08.24 | Exact `alpha=0` / universal-horizon boundary | 🟥 scoped warning | Current exact rational positive-pole construction has `alpha>0` for finite allowed parameters; higher-spatial/strong-field completion must address the low-energy universal-horizon issue rather than assuming it away. |

## C9 — Technical naturalness, EFT cutoff and radiative protection

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| C09.01 | Test whether existing `U(1) x Diff(M,F)` + internal shift protects exceptional surface | 🟥 closed negative | Existing declared symmetries do **not** protect the required `sigma1=sigma2=0`-type surface; corresponding marginal operators are allowed. |
| C09.02 | Additional Ward symmetry candidate | 🟨 | Need explicit symmetry and Ward identities if this route is used. |
| C09.03 | Counterterm-stable degeneracy mechanism | 🟨 | Alternative protection route not yet closed. |
| C09.04 | RG fixed surface | 🟨 | Alternative protection route not yet closed. |
| C09.05 | Quantitative induced-coupling/tuning bound | 🟨 | Must be below a demonstrated EFT cutoff if no exact protection exists. |
| C09.06 | Strong-coupling / EFT cutoff on the same final action | 🟨 | Local-rest rank enhancement gives warning, not yet a quantitative final cutoff. |
| C09.07 | Hyperbolicity/causal-domain statement for the final same action | 🟨 | Must include any superluminal characteristics and intended causal interpretation. |

## C10 — Same-full-action cosmological completion and production bridge

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| C10.01 | Elliptic auxiliary projection + exact k=0 bridge | ✅ | Closed. |
| C10.02 | Finite-k all-q rank domain | ✅ scoped | Closed with explicit domain assumptions. |
| C10.03 | History-wide symbolic `M_c` window | ✅ scoped | Nonempty window theorem with explicit finite EFT onset; no numerical `M_c` selected. |
| C10.04 | Production ordinary-source identity | ✅ | Baryons+photons+massless relativistic species ordinary source; Khronon neutral/unfiltered in baseline contract. |
| C10.05 | A-source normalization / Helmholtz constraint | ✅ | Exact `k>0` normalization and `a1_eff=k^2/(k^2+a^2 M_c^2)` bridge. |
| C10.06 | Prepotential Ward normalization | ✅ | Closed scoped. |
| C10.07 | Linear prepotential redundancy | ✅ | Closed for `k>0` with total momentum guard. |
| C10.08 | Minimal linear metric reduction | ✅ | A fixes `psi`; momentum fixes preferred shear/shift; Hamiltonian fixes lapse; trace has no metric second-time derivative. |
| C10.09 | Trace compatibility = total momentum conservation | ✅ | Exact closure identity established. |
| C10.10 | `S_mix` IR lapse kernel | ✅ scoped | `E_th,IR=2`; no scoped finite-k lapse pole for `lambda_HL>1`. |
| C10.11 | `S_mix` source ratio / rational inertia | ✅ scoped | Same `F=1+k_phys^2/M_K^2` factor in scalar inertia and lapse variation. |
| C10.12 | Local full-action effective-fluid equivalence | ✅ scoped | Locally frozen principal continuity/Euler structure recovered. |
| C10.13 | Action-fluid detached shadow interface | ✅ | Production untouched. |
| C10.14 | Twin CLASS spectra action-fluid check | ✅ | Overall normalized difference `3.538390324840441e-11`; same gamma root. |
| C10.15 | Fixed historical action-fluid likelihood replay | ✅ scoped | Score shift `1.8189894035458565e-10 << 0.005`; not completed-U1 metric likelihood. |
| C10.16 | Physical metric map | ✅ scoped | Preferred-foliation physical shear prevents direct naive CLASS-Newtonian identification. |
| C10.17 | Newtonian/Stueckelberg metric bridge | ✅ scoped | Exact bridge for `Phi_N`,`Psi_N`; preferred `chi` kept distinct from DBI Sigma/U1 prepotential. |
| C10.18 | Total momentum source scope | ✅ | Neutral Khronon included in total metric momentum; ordinary A-source remains restricted. |
| C10.19 | Newtonian source transform | ✅ | Exact maps for `delta_mu,q,delta_p,Pi,deltaH0`. |
| C10.20 | Newtonian transformed pole/determinant audit | ✅ scoped | No new finite-k physical pole; exact k=0 separate. |
| C10.21 | Completed gravity shadow metric API v1 | ✅ | Determinant factorization, constraints and source round trip smoke-tested. |
| C10.22 | Reordered shadow metric solver v2 | ✅ | Removes spurious algebraic solve-basis crossing from physical interpretation; finite-k algebra closed. |
| C10.23 | Native CLASS-unit shadow solver v3 | ✅ | Exact `(8πG/3)` source normalization fixed; v2↔v3 physical regression error 0; determinant and lambda-cancellation controls pass. |
| C10.24 | Parameter-free physical RT-CLASS source-history export | ✅ | 9 real `k` histories exported read-only; required diagnostics finite; production unmodified. |
| C10.25 | Small-k regularity lambda cancellation | ✅ | In conservation-consistent completed-U1 bracket, `lambda_HL` cancels; no arbitrary epsilon choice required for this diagnostic. |
| C10.26 | Exploratory `C_com` small-k scaling | ✅ diagnostic | Shows clean `k^2` plateaus on resolved scales and identifies cancellation/interpolation sensitivity at the smallest k. |
| C10.27 | Frozen ultra-small-k confirmatory compatibility gate | 🟥 FAIL scoped | Predeclared smallest-k thresholds fail at core epochs. Result retained exactly; not automatically a physical no-go. |
| C10.28 | Diagnose model-2 auxiliary terms | ✅ boundary | Legacy production metric equations contain `Z,V` auxiliary terms; matter-only identity is not assumed to be a legacy gravity equation. |
| C10.29 | Small-k precision/interpolation convergence diagnosis | 🔵 | Frozen target created; historical-ultra and 4x tighter direct-Ccom runs launched. Parent FAIL cannot be retroactively changed by this diagnosis. |
| C10.30 | Separately frozen small-k compatibility rerun after convergence diagnosis | ⏳ conditional | Required if numerical-floor support is established; only this can create a new PASS/FAIL under revised numerically justified resolution domain. |
| C10.31 | Choose/freeze diagnostic or physical completion parameters (`M_c`,`lambda_HL`, etc.) | ⏳ | Do not choose arbitrarily before parameter-independent history/conditioning screens are exhausted. |
| C10.32 | Full physical completed-U1 history replay with finite `chi` prescription | 🟨 | Source histories and solver exist; boundary/initial prescription + conditioning route still required. |
| C10.33 | Opt-in completed-U1 Boltzmann shadow with metric feedback | ⏳ | Only after detached history/conditioning gates pass; production path must not be overwritten. |
| C10.34 | Completed-metric fixed-parameter spectra | ⏳ | Must precede likelihood/refit. |
| C10.35 | Completed-action likelihood/refit | ⏳ | Historical phenomenological A5 score cannot be transferred to completed action. |
| C10.36 | Massive-neutrino completion-source extension | 🟨 | Baseline source contract excludes `ncdm`; B4 completion extension separate. |

## T — Cross-framework translation and observable atlas

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| T01 | EFT-of-dark-energy / ADM dictionary | 🟨 | Partial ADM/U1 structures known; reusable full dictionary not yet delivered. |
| T02 | Effective alpha-like functions / failure map | 🟨 | Open. |
| T03 | PPF dictionary `mu(k,a), Sigma(k,a), eta(k,a)` | 🟨 | Open; C10 physical metric/source bridge provides ingredients. |
| T04 | Khronometric/Einstein-Aether parameter dictionary | 🟨 | Several low-energy mappings used for scoped constraints; compact reusable dictionary still open. |
| T05 | Machine-readable `RTK -> phenomenology` export | 🟨 | C10 source exports exist; general public translation export remains open. |
| T06 | CMB TT/TE/EE/lensing residual atlas | 🟨 | Some twin/residual diagnostics exist, not full atlas. |
| T07 | Matter `P(k,z)`, growth, `fσ8`, Weyl/lensing atlas | 🟨 | B5 linear scale diagnostic is a subpiece only. |
| T08 | Derivative/Fisher atlas `dO/dtheta` | 🟨 | Open. |
| T09 | Orthogonality vs LCDM/wCDM/f(R)/Horndeski/khronometric phenomenology | 🟨 | Open. |
| T10 | Background-vs-perturbation degeneracy decomposition | 🟨 | Partial B9/C10 decomposition exists; systematic atlas open. |
| T11 | Matched wCDM benchmark | ⏳ | Frozen benchmark protocol exists; execute after A5 refreeze. |
| T12 | Full CPL `w0-wa` benchmark | 🟨 blocked on current solver boundary | Pinned CLASS branch rejects `w=-1` crossings; requires crossing-safe PPF/fluid implementation before calling it full CPL. |

## E — Early universe and thermal history beyond closed B6 differential gate

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| E01 | Radiation-era/BBN expansion robustness | ✅ differential | B6 `H(T)` + paired abundance effect closed for frozen massless point. |
| E02 | Recombination robustness | 🟨 | Open beyond current late-time fit usage. |
| E03 | Drag epoch robustness | 🟨 | Open beyond current validated likelihood path. |
| E04 | Early-time attractor existence/stability | 🟨 | Open. |
| E05 | Adiabatic initial-condition derivation | 🟨 | Production IC implementation exists, but same-final-action analytic uniqueness/stability map remains open. |
| E06 | Isocurvature structure | 🟨 | Unsupported modes currently fail closed; physical derivation still open. |
| E07 | Inflationary extrapolation or explicit cutoff | 🟨 | Open; acceptable outcome is a demonstrated validity cutoff. |

## G — Gravitational waves and multimessenger sector

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| G01 | Tensor propagation speed on the same final action | 🟨 | Low-energy mappings constrain candidate slices, but final same-action derivation required. |
| G02 | Tensor damping/friction and effective Planck-mass evolution | 🟨 | Open. |
| G03 | Extra GW polarizations | 🟨 | Open for final completion. |
| G04 | GW170817-like low-z compatibility | 🟨 | Used as a scoped carrier constraint; final same-action certification open. |
| G05 | GW vs EM luminosity distance | 🟨 | Open. |
| G06 | Standard-siren observable/forecast module | 🟨 | Open. |

## N — Nonlinear structure, local gravity and compact objects

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| N01 | Quasistatic limit | 🟨 | Open for final completion. |
| N02 | Weakly nonlinear limit | 🟨 | Open. |
| N03 | Spherical collapse/effective force law | 🟨 | Open. |
| N04 | Screening/recovery mechanism | 🟨 | Open beyond controlled stationary scaling results. |
| N05 | Halo-model/emulator validity | 🟨 | Open. |
| N06 | N-body implementation ingredients | 🟨 | Open. |
| N07 | Static stellar equations | 🟨 | Open. |
| N08 | Binary-pulsar consistency | 🟨 | Open. |
| N09 | Black-hole/horizon solutions | 🟨 | Open; universal-horizon issue tracked separately in C08.24. |
| N10 | Strong-field preferred-frame/rotation effects | 🟨 | Weak-field PPN quartet does not close this. |

## I — Reproducibility, infrastructure and community release

| ID | Item | Status | Current durable result / remaining work |
|---|---|---|---|
| I01 | Chat-independent recovery guide | ✅ | Repository recovery guide/methodology/chronology exist. |
| I02 | Append-only scientific chronology | ✅ ongoing | Existing chronology and iteration records; continue updating. |
| I03 | Immutable objective/source fingerprints | ✅ production / 🟨 all outputs | Production objective/source locked; extend systematic versioning to every public artifact. |
| I04 | Environment/package pinning | ✅ core / 🟨 release | Python/numpy/scipy/CLASS/Planck/Pantheon locks used in major workflows; public container recipe still open. |
| I05 | One-command benchmark | 🟨 | Open: theory limits + Planck self-tests + one LCDM + one RTK point. |
| I06 | Background-only example | 🟨 | Open as polished community example. |
| I07 | Perturbations-only example | 🟨 | Open. |
| I08 | Likelihood example | 🟨 | Internal workflows exist; polished public example open. |
| I09 | Parameter-scan example | 🟨 | Open. |
| I10 | Failure-mode documentation | 🟨 | Many guards exist; consolidate gamma/stability/timeouts/boundaries/precision sensitivity. |
| I11 | `main` vs `rtk-class-build` source divergence | 🟨 | Either collapse branches or enforce a single immutable scientific source fingerprint everywhere. |
| I12 | Home runner 12-logical-CPU saturation/checkpoint bootstrap | 🟨 infra | Architecture designed; do not route unique science until clean saturation/checkpoint artifact is certified. |
| I13 | Canonical monotonic master checklist | ✅ new | This file. Existing IDs must never be removed; print full checklist after every research iteration. |

---

## Current strict frontier order

1. C10.29 — finish the frozen small-k precision/interpolation convergence diagnosis; preserve C10.27 parent FAIL unchanged.
2. A16 — finish LCDM recenter1 multiscale/fresh-tree chain, then A17 common A5 refreeze.
3. B04.4 — inspect/persist B4 quarter-scale Hessian and follow its frozen decision tree.
4. C09.02-C09.06 — obtain an explicit protection/tuning/cutoff mechanism for the same completion rather than treating exceptional operator surfaces as natural.
5. C10.30-C10.35 — only after numerical regularity/conditioning closure, advance to opt-in completed-U1 Boltzmann spectra and then completed-action likelihood/refit.
6. T01-T12, G01-G06, N01-N10 — build the cross-framework, GW and nonlinear/compact-object utility packages without deleting any earlier scoped obstruction.

## Non-negotiable interpretation guard

The project currently contains both strong positive results and strong scoped negative results. A scoped no-go excludes only its declared ansatz/assumptions. Conversely, a successful historical phenomenological likelihood fit does not certify the still-under-construction same-full-action U(1) completion. Both facts must remain visible in every future checklist.
