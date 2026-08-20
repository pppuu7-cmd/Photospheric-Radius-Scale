# RTK Route-B U-DHOST rescue note — 2026-08-20

## Source-of-truth checkpoint

Branch: `rtk-class-build`.
Observed branch head before this note: `9e9f1bcc286532b1731879a33a376aaf0d6f3665` (autonomous iteration 144 chronology/state update).
Frozen matched objective remains `matched-ultra-linstep2+dense-BOSS` with replay-certified local scores `S_RTK=1050.249912429787`, `S_LCDM=1049.966118347761`, raw local `Delta S=+0.2837940820259064`. These are not AIC/BIC/Bayes evidence or global-optimum claims.

## Why this route is being tested

The exact BPS single-scalar rational embedding is incompatible with exact `alpha=0` at finite healthy parameters, and the correlated `alpha -> 0`, `lambda-1 -> 0` limit collapses the low-energy cutoff. This motivates a broader fixed-action preferred-foliation completion rather than further tuning of the same BPS family.

## Primary-source facts used in this iteration

Saito, Yao & Kobayashi, arXiv:2402.10459 / JCAP 06 (2024) 040, formulate U-DHOST in EFT language. For the unitary-degenerate class they give

`beta2 = -6 beta1^2/(1+alphaL)`

and state that, aside from this, the EFT parameters are independent. They identify `alphaT = c_GW^2 - 1`. The paper also gives an explicit U-DHOST Lagrangian whose PPN parameters take their GR values. This proves existence of nontrivial weak-field-safe directions in a class broader than khronometric theory; it does not prove that the RTK-matched acceleration channel lies on that GR-PPN submanifold.

Kobayashi & Hiramatsu, arXiv:2310.11041, independently identify a subset of U-DHOST theories that evades solar-system tests while gravitational waves propagate at light speed, with cosmological deviations still possible.

Saito & Kobayashi, arXiv:2408.14004, construct slowly moving black-hole solutions in a higher-order Lorentz-violating scalar-tensor family extending khronometric theory and find generic solutions regular outside the universal horizon. This prevents promoting the old khronometric compact-object result into a universal no-go for all preferred-foliation scalar-tensor completions.

## New exact result added to the repository

`rtk/route_b_udhost_parameter_freedom.py` proves the deliberately narrow algebraic statement that U-DHOST degeneracy plus luminal tensors do not force the scalar/constraint EFT sector onto the old khronometric `alpha=0` boundary. In particular, imposing the sourced degeneracy relation and `alphaT=0` leaves `beta3` algebraically independent.

This is a **parameter-freedom gate**, not a physical RTK completion theorem.

## What remains open

1. Derive the exact unitary-gauge operator dictionary connecting the RTK-required `a_i a^i -> (grad dot pi)^2` channel to U-DHOST EFT/covariant coefficients.
2. Intersect that operator requirement with the exact GR-like PPN conditions of arXiv:2402.10459 rather than assuming compatibility from parameter counting.
3. Require `alphaT=0` in the physical matter frame.
4. Derive one fixed-action FLRW quadratic constraint/propagator matrix and test whether it reproduces replay-certified `C(a)` and `M_K(a)` without hand-inserted time-dependent Wilson coefficients.
5. Only after 1–4: redo compact-object, strong-coupling, radiative-stability and matter-Lorentz gates for the selected completion.

## Classification

**OPEN BUT CONSTRUCTIVE.** The original BPS rescue by exact `alpha=0` is closed, but the broader U-DHOST/spatially-covariant route is not excluded. This iteration proves only that the degeneracy and luminal-tensor constraints alone leave nontrivial EFT freedom; it does not yet prove that the same freedom can carry the exact RTK rational pole while satisfying GR-like PPN conditions.
