# RTK / DBI-Khronon restore point — neutral-charge frontier through C10.63

Date: 2026-08-26
Branch: `rtk-class-build`
Pinned upstream nonlocal CLASS: `36cf283628c4a3330ec9fd3d84239bf775f77317`

## Purpose

This checkpoint is the chat-independent continuation point after reconciling the RTK1 and RTK2 research threads with the repository. It records the decisive neutral preferred-sector memory results and prevents later chats from confusing a coordinate-norm amplification with a physical long-wave instability theorem.

## 1. Prior production result remains scoped

The independently replayed matched local dense objective remains

- `S_LCDM = 1049.966118347761`
- `S_RTK = 1050.249912429787`
- `Delta S = 0.2837940820259064`.

This is a raw matched local objective comparison only. It is not AIC/BIC/Bayes evidence and it is not a completed-U1 cosmological likelihood result.

## 2. Production source histories are available

C10 physical CLASS source export is green on the pinned historical RTK trajectory:

- 9 Fourier histories
- `k = 1e-5 ... 0.1 Mpc^-1`
- production `gamma_root = 0.05170371280716`
- no completion parameters selected in that source-export gate.

Authoritative result:
`research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json`.

## 3. Exact neutral shift-charge identity

The authoritative neutral-memory identity is

`I_khr = delta_khr/(1+w_khr) - 3 psi_pref`

with

`I_khr' = -(theta_khr + k^2 B)`.

Equivalently the fractional preferred-sector shift-charge perturbation is the same invariant:

`delta Q / Qbar = I_khr`.

At exact regular `k=0`, with `theta=0`, this is conserved. For a regular long-wave family

- `theta = O(k^2)`
- `B = O(1)`

so

`I_khr' = O(k^2)`.

Authoritative parent:
`research/theory_results/RTK_C10_NEUTRAL_SHIFT_CHARGE_MEMORY_RESULT_v1.json`.

## 4. New finite-time long-wave theorem

C10 continuation derived and froze the following bound using only the exact identity above.

Assume on a finite conformal interval `[tau_i,tau_f]`

`|theta| <= C_theta k^2`,

`|B| <= C_B`,

with finite `k`-independent constants. Then

`I_f-I_i = - integral (theta+k^2 B) d tau`

and therefore

`|I_f-I_i| <= (C_theta+C_B) k^2 Delta_tau`.

If additionally `|I_i| >= I_min > 0` independently of `k`,

`|I_f/I_i - 1| <= ((C_theta+C_B) Delta_tau/I_min) k^2`.

Hence on every fixed finite regular in-EFT interval

`lim_{k->0} I_f/I_i = 1`.

Scoped consequence: no regular finite-time in-EFT attractor can uniformly erase every nonzero O(1) neutral charge as `k->0`. This does not exclude finite-k damping, intervals scaling as `k^-2`, singular branches, or a pre-EFT/UV rule that fixes the initial charge.

Authoritative target/result:

- `research/theory_targets/RTK_C10_NEUTRAL_CHARGE_LONG_WAVE_MEMORY_BOUND_TARGET_v1.json`
- `research/theory_results/RTK_C10_NEUTRAL_CHARGE_LONG_WAVE_MEMORY_BOUND_RESULT_v1.json`

Classification:
`C10_NEUTRAL_CHARGE_LONG_WAVE_FINITE_TIME_MEMORY_BOUND_PASS_SCOPED`.

## 5. C10.62b preregistered neutral finite-onset transfer

Frozen C10.62b evolves only neutral preferred-fluid onset differences while the ordinary production trajectory is held fixed. Its coordinate state is

`Y = (delta_khr, theta_khr/k)`.

The ordinary-only difference constraint forces `Delta psi=0`, so the elliptic `M_c` filter cancels on this subspace. The test therefore probes whether the neutral action-fluid state forgets onset data through the coupled lapse/shift response.

### Technical execution history

The first execution, run `32914231981`, failed before scientific classification because the worker compared the exact nonlinear reconstructed `c_a^2(a)` against a linearly interpolated exported `c_a^2` at artificial boundary nodes. The maximum mismatch was about `0.0220872`.

This was a validator bug, not a model result. The frozen physical thresholds and transfer equations were not changed. The correction evaluates the exact reconstruction identity on actual raw CLASS samples and retains the interpolated-boundary mismatch only as a numerical diagnostic.

Corrected worker commit:
`cb65b742ac987bcc149698bd6813340b6c6ad8bb`.

Corrected run `32914400252` completed successfully.

### Scientific result

Classification:
`C10_NEUTRAL_FINITE_ONSET_MEMORY_RETAINED_OR_AMPLIFIED_SCOPED`.

Across the frozen grid:

- 81 total runs
- 27 unique `(k,lambda_HL)` pairs
- `min final sigma_max = 1.0000482312543617`
- `max final sigma_max = 179.46512104685894`
- monotone contraction is false
- `max M_c` duplicate transfer difference = `0.0`
- raw CLASS `c_a^2` reconstruction error = `3.219607487724663e-12`
- maximum Hamiltonian/momentum constraint residual = `2.407977978833279e-12`.

Authoritative result:
`research/theory_results/RTK_C10_NEUTRAL_FINITE_ONSET_MEMORY_RESULT_v1.json`.

Important scope: `sigma_max>1` in the frozen `Y=(delta,theta/k)` norm is not by itself a long-wave physical instability theorem. A unit velocity basis in Y has `theta=O(k)`, whereas the regular theorem assumes `theta=O(k^2)`.

## 6. C10.63 charge-aware projection

To remove that coordinate ambiguity, C10.63 was frozen before execution.

On the fixed-ordinary difference subspace `Delta psi_pref=0`, so

`I_khr = delta/(1+w)`.

If the C10.62b final columns are `[d1,t1,d2,t2]`, the Y transfer matrix is

`T_Y = [[d1,d2],[t1/k,t2/k]]`.

The pure-charge transfer ratio is

`R_Q = T11 * (1+w_i)/(1+w_f)`.

For a genuinely regular velocity family define

`U = H_EFT theta/k^2`,

hence

`theta/k = (k/H_EFT) U`.

The regular velocity-to-charge leakage is therefore

`L_QU = (k/H_EFT) * T12/(1+w_f)`.

Frozen low-k set:

`k = [1e-5, 3e-5, 1e-4] Mpc^-1`.

Run `32914637706` executed the preregistered projection.

Classification:
`C10_NEUTRAL_CHARGE_PROJECTION_RETENTION_PASS_SCOPED`.

For all three frozen `lambda_HL` values:

- `|R_Q-1|` decreases monotonically toward small k
- `|L_QU|` decreases monotonically toward small k
- all preregistered asymptotic conditions pass
- minimum fitted `p_Q = 2.07425909653829`
- minimum fitted `p_U = 1.990875741462291`
- `M_c` duplicate transfer difference remains exactly `0.0`.

At `k=1e-5 Mpc^-1` the three pure-charge transfer ratios are approximately

- `0.9999700559`
- `0.9999571881`
- `0.9999314528`.

Thus the numerical low-k transfer agrees with the exact `O(k^2)` finite-time charge-memory theorem.

Authoritative target/worker/result:

- `research/theory_targets/RTK_C10_NEUTRAL_CHARGE_PROJECTION_TARGET_v1.json`
- `research/shadow/rtk_c10_neutral_charge_projection.py`
- `research/theory_results/RTK_C10_NEUTRAL_CHARGE_PROJECTION_RESULT_v1.json`.

## 7. Scientific consequence for the cosmology architecture

The neutral preferred-sector charge is an independent boundary datum on the regular long-wave branch. The completed cosmological architecture cannot rely on ordinary finite-time in-EFT evolution to erase an arbitrary initial charge.

Therefore the next cosmology gate must explicitly separate:

1. the declared adiabatic/preferred branch, for which a pre-EFT/UV boundary prescription fixes the independent charge datum, from
2. the independent neutral-charge/isocurvature branch, whose existence must not be silently removed by a coordinate choice.

A minimal declaration such as `I_khr(tau_on)=0` may be used to define the adiabatic branch, but it is a boundary prescription, not a derived dynamical protection mechanism. Its consistency and downstream growing-mode behavior must be tested explicitly.

## 8. Independent C9 blocker remains open

C9 is not solved by the C10 progress.

The currently declared local `U(1) x Diff(M,F)` plus internal Sigma-shift symmetries do not protect the exceptional surface

`sigma1 = sigma2 = 0`.

The corresponding pure-gravity operators are allowed marginal operators. C9 therefore still requires at least one explicit mechanism:

- an additional exact symmetry/Ward identity,
- a counterterm-stable structural degeneracy,
- an explicit RG fixed surface with both beta functions zero, or
- a quantitative induced-coupling tolerance below a demonstrated physical EFT cutoff.

Authoritative result:
`research/theory_results/RTK_C9_U1_EXISTING_SYMMETRY_PROTECTION_RESULT_v1.json`.

## 9. Recovery procedure / next gates

A new chat should resume in this order:

1. Read this restore point and the three neutral-charge results named above.
2. Do not reinterpret C10.62b's large finite-k Y singular values as a proved physical instability; use C10.63 for the regular charge statement.
3. Freeze an explicit pre-EFT/UV neutral-charge boundary prescription for the adiabatic branch, while preserving the independent charge-isocurvature branch as a separate physical mode.
4. Implement the photon+baryon+massless-UR dual-interface growing/decaying-mode test with the completed-U1 metric constraints and the frozen charge prescription.
5. Only after self-consistent coupled evolution exists should completed-U1 spectra and likelihoods be compared with the historical action-fluid shadow.
6. Keep C9 radiative protection as an independent mandatory gate; C10 cannot close it.
7. Preserve every scoped negative or inconclusive legacy result rather than overwriting it with later interpretation.
