# RTK B4 neutrino stationarity chain

Date reconstructed: 2026-08-21
Status: canonical provenance/audit chain; final B4 closure still open

## Purpose

This document reconstructs the exact reason B4 moved from a coordinate Hessian at the first recentered neutrino RTK point to negative-mode rays and then to a second frozen recenter target. It prevents a future recovery session from mistaking an older successful GitHub Actions job for a certified local minimum.

B4 uses a separate objective from the massless production comparison:

`matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1`.

Its absolute scores must not be numerically mixed with the frozen massless A1-A5 objective.

Frozen recenter tolerance:

`Delta S = 0.005`.

---

## 1. First recentered RTK base Hessian

GitHub Actions run:

`32252398625`

Artifact:

- id `9371716156`;
- name `rtk-b4-neutrino-rtk-recenter-base`;
- digest `sha256:a356d57f18aed230093b319a8f0e47bbd9d53260fa8541cfe3fb34f1b6a71753`.

The workflow itself completed successfully. That means the calculation executed; it does **not** mean the center was a local minimum.

Center:

- `As = 2.0874853364554216e-9`
- `Ob = 0.04722503932186544`
- `Om = 0.2528668961185522`
- `h = 0.688550855870249`
- `lambda_D = 3043232.309640512`
- `ns = 0.9657228676316294`
- `zre = 7.391020782396863`

Center score:

`S_eff = 1050.6979573843187`.

The best exact coordinate-stencil point improved the center by only

`6.251691934267001e-05`,

which is below the frozen `0.005` recenter tolerance.

However, the reconstructed Hessian eigenvalues were

- `-0.0324084135524679`
- `-0.0015792056227914312`
- `-1.9922876135075676e-05`
- `+0.02157822766827596`
- `+0.23778276866304618`
- `+3.0494639799061405`
- `+7.274214504938618`

so the Hessian had **three negative modes**.

Therefore the correct classification is not `stationary local minimum`; it is an indefinite local quadratic candidate requiring exact evaluations along negative-eigenvector rays.

This demonstrates why axis-only polls are insufficient: a direction assembled from multiple parameter coordinates can lower the objective even when every individual coordinate displacement is below the recenter threshold.

---

## 2. Mandatory negative-mode rays

GitHub Actions run:

`32284932113`

Artifact:

- id `9378827376`;
- name `rtk-b4-neutrino-rtk-negative-mode-rays`;
- digest `sha256:e320c38ee09001ff66676a2ed0e06e8dd5861d85434b18dad2dfbfe5a42d5a01`.

The exact-ray result classified the parent point as requiring recentering.

Strongest ray:

- Hessian mode index `0`;
- parent eigenvalue approximately `-0.0324084`;
- ray coefficient `alpha = +2.0`;
- exact score `S_eff = 1050.5880475140204`;
- improvement from parent center `0.10990987029822463`.

Since

`0.10990987029822463 > 0.005`,

the old center is decisively invalid under the preregistered local stationarity rule.

Other negative modes also contained exact improvements above tolerance:

- mode 1, best at `alpha=-2`, improvement about `0.05367855`;
- mode 2, best at `alpha=-2`, improvement about `0.01586085`.

Thus the indefinite Hessian was not a harmless finite-difference artifact: all three negative-mode directions were physically falsified by exact objective evaluations, with mode 0 giving the strongest recenter.

---

## 3. Frozen second recenter target

The exact best mode-0/alpha=+2 point became the frozen target

`rtk-class-build:research/robustness/b4_neutrino_rtk_ray_recenter_target_v2.json`.

The target records:

- parent negative-ray run `32284932113`;
- parent artifact `9378827376` and its digest;
- parent center `S_eff = 1050.6979573843187`;
- exact new center `S_eff = 1050.5880475140204`;
- improvement `0.10990987029822463`;
- mode index `0`;
- `alpha=2.0`.

Frozen second-center parameters:

- `As = 2.0920212896820786e-9`
- `Ob = 0.04722200104991654`
- `Om = 0.2528393318824633`
- `h = 0.6885660022475836`
- `lambda_D = 3043326.1774413693`
- `ns = 0.9657332769496741`
- `zre = 7.506210209218662`.

The parameters in target v2 match the exact ray winner, so the second recenter is provenance-consistent rather than a manually altered point.

Target commit recorded by the replay workflow:

`3b9acfb25a01c6107a4a8427ef2b51ae61017d20`.

---

## 4. Current mandatory replay

A fresh base-Hessian replay at target v2 was launched on 2026-08-21 because the historical workflow state was not represented as a closed scientific result in the current live state.

Main workflow:

`.github/workflows/rtk-b4-neutrino-rtk-ray-recenter-base.yml`

Trigger commit:

`c71058fe5cb21e033e73b6966baca99686ffd851`.

The workflow checks before calculation that:

- target classification is `B4_NEUTRINO_RTK_RAY_RECENTER_TARGET_V2_FROZEN`;
- parent ray run/artifact match the frozen provenance;
- parent improvement exceeds `0.005`;
- best mode is 0 and alpha is +2;
- the B4 objective name is exact;
- the base replay score agrees with the parent exact ray winner within `2e-6`.

No B4 closure is declared until the fresh artifact is inspected.

---

## 5. Decision tree after the target-v2 base replay

Apply mechanically:

1. If an exact stencil point improves the new center by more than `0.005`, freeze that winner and recenter again.
2. If no coordinate improvement exceeds `0.005` but the Hessian is non-positive-definite, evaluate exact rays along every negative/near-zero mode before progressing.
3. If base scale passes with a positive-definite Hessian, run the independent half-scale (`0.5`) Hessian/stationarity gate.
4. Require adjacent base and half scales to be positive definite and consistent.
5. Then require fresh-tree replay before declaring the local B4 RTK point certified.
6. Apply the same frozen protocol to the LCDM side before making a paired robustness comparison.

The target-v2 JSON itself records the closure rule:

`recenter until exact best improvement <=0.005; then require adjacent base and half positive-definite Hessian scales and fresh-tree replay`.

---

## 6. Scientific interpretation boundary

B4 tests robustness to the pinned minimal-neutrino branch. It is not a replacement for the massless A1-A5 production objective.

A B4 local-minimum result would establish only the paired/local robustness statement defined by its frozen protocol. It would not imply:

- a global minimum;
- neutrino-mass inference;
- posterior preference;
- AIC/BIC/Bayes evidence;
- a proof of the covariant RTK carrier.

Current B4 status: **OPEN — target-v2 ray-recenter base replay/certification pending**.
