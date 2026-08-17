# RTK current-center gravitational-wave standard-siren prediction

Date: 2026-08-18

## Status

This checkpoint closes the **late-time linear GW propagation prediction at the current RTK center**. It does not close the full tensor sector: primordial tensor initial conditions/CMB B modes, nonlinear GW generation, compact-object screening/local physics and a full tensor-sector likelihood remain separate questions.

## Code-level equation

The pinned nonlocal CLASS `model=2` tensor equation is

`h'' + [2 a H - 3 H0^2 gamma V(a)] h' + k^2 h = source`.

Therefore the tensor phase speed is exactly luminal in the implemented branch, while the cosmological amplitude friction differs from GR.

Writing

`h'' + 2 Hconf [1-delta(z)] h' + k^2 h = source`,

gives

`delta(z) = 3 H0^2 gamma V(z) / [2 a H(z)]`.

For sub-horizon standard sirens,

`dL_gw/dL_em = exp[- integral_0^z delta(z')/(1+z') dz']`.

The Khronon patch contains no additional tensor evolution branch; its effect on this prediction enters through the common RTK background and the one-scale closure root `gamma`.

## Reproducible CLASS prediction

Workflow run: `32079453967` — success.

Artifact:
- name: `rtk-current-standard-siren`;
- ID: `9304596044`;
- digest: `sha256:ede9bdac9ba80f7be536e06c6effbc5c33c9bf291b1cc61ae5feaf4bd6cb1952`.

The run used the state-driven accepted RTK center and solved

`gamma = 0.051663386535`.

The resulting GW/EM luminosity-distance ratios are:

| z | delta(z) | dL_gw/dL_em | fractional shift |
|---:|---:|---:|---:|
| 0.0 | 0.15226219 | 1.00000000 | 0 |
| 0.1 | 0.12877097 | 0.98671488 | -1.3285% |
| 0.38 | 0.08179418 | 0.96367029 | -3.6330% |
| 0.51 | 0.06683183 | 0.95726032 | -4.2740% |
| 0.61 | 0.05745702 | 0.95345791 | -4.6542% |
| 1.0 | 0.03313596 | 0.94432014 | -5.5680% |
| 2.0 | 0.01058087 | 0.93671665 | -6.3283% |
| 5.0 | 0.00131094 | 0.93381842 | -6.6182% |

The full CLASS background extends to very high redshift and the numerical ratio approaches approximately

`Xi_infinity = 0.9334210241`.

## Independent ODE replay

The same pinned `model=2` background equations were independently integrated outside CLASS using the explicit RT equations for `U,V,H` plus the analytical DBI-Khronon density and pressure.

The independent integration reproduced `H(a=1)/H0` to about `4e-6` using independently reconstructed radiation constants. Its predicted standard-siren ratios differ from the CLASS artifact by only roughly `1e-6 ... 3e-6` fractionally across z=0.1...5.

This is an independent equation-level replay, not merely a re-read of the CLASS output table.

## Xi0-n compression

The current RTK prediction is extremely well approximated by the common luminal modified-propagation parametrization

`dL_gw/dL_em = Xi0 + (1-Xi0)/(1+z)^n`.

A least-squares fit to the explicit RTK target points gives approximately

- `Xi0 = 0.93239`;
- `n = 2.4317`;
- RMS ratio residual `4.58e-4`.

Fixing `Xi0` to the explicit high-z asymptote `0.933421` gives `n ~= 2.51` with RMS residual `6.28e-4`.

Thus the standard Xi0-n compression is adequate for a first observational comparison, although a future direct RTK likelihood should use the exact curve rather than the fitted parametrization.

## Current observational sanity check

Primary reference: LVK, `GWTC-5.0: Constraints on the Cosmic Expansion Rate and Modified Gravitational-wave Propagation`, arXiv:2605.27227v2 (2026-08-04 revision).

That analysis reports, for the Xi0-n parametrization:

- wide H0 prior: `Xi0 = 1.1 +0.6/-0.3` (68.3% interval), `n = 3.4 +4.2/-2.6`;
- narrow H0 prior: `Xi0 = 1.0 +0.3/-0.2`, `n = 3.8 +3.8/-2.8`;
- no statistically significant departure from GR.

The RTK compression `(Xi0,n) ~ (0.932,2.43)` lies comfortably inside these present broad constraints. Therefore **current GWTC-5.0 modified-propagation constraints do not exclude the current RTK center**.

This statement is only a parameterized sanity check, not an RTK-specific reanalysis of the LVK event likelihood.

## Scientific significance

The scalar-sector matched fit can be highly degenerate with standard cosmological parameters, while the GW propagation ratio is a direct RT-sector amplitude effect. At z~0.4-1 the predicted deviation is already about 3.6-5.6%, making standard sirens a potentially much cleaner distinguishing observable than the sub-percent matched CMB residuals.

## Claim boundary

Established:

- current implemented tensor propagation is luminal;
- current RTK center predicts a reproducible non-GR cosmological GW amplitude friction;
- exact `dL_gw/dL_em(z)` has been computed from pinned CLASS and independently replayed at equation level;
- the current prediction is not excluded by the published GWTC-5.0 Xi0-n constraints.

Still open:

- full RTK-specific event-level GWTC likelihood;
- primordial tensor spectrum / CMB B-mode prediction;
- nonlinear GW generation and compact-object/local-gravity consistency;
- whether nonlinear screening/backreaction alters the homogeneous propagation law;
- future ET/LISA/3G forecast using the exact RTK curve.
