# RTK Route-B: U-DHOST acceleration channel and full-DHOST boundary

Date: 2026-08-20
Branch: `rtk-class-build`

## Source-of-truth state checked

- Branch head before this iteration: `b352614a85119a87b8d86a0d7c1d3736df0dff37`.
- `research/state/current.json` reports autonomous iteration 146.
- Frozen matched comparison remains `S_RTK=1050.249912429787`, `S_LCDM=1049.966118347761`, `Delta S=+0.2837940820259064`, with the existing warning that this is a local matched raw objective comparison only.

## New primary-source correction

Primary source: Langlois, Mancarella, Noui, Vernizzi, arXiv:1703.03797 / JCAP 05 (2017) 033.

Their quadratic unitary-gauge EFT contains

`(M^2/2) beta3 a^{-2} (partial_i delta N)^2`,

and explicitly identifies `beta3` with the gradient energy arising from the acceleration of the normal,

`a_i = partial_i N / N`.

Restoring the clock Stueckelberg mode gives `delta N = +/- dot(pi)` at linear order around Minkowski, hence

`(partial_i delta N)^2 -> (grad dot(pi))^2`.

Therefore beta3 is not merely a free bookkeeping parameter: it is exactly the EFT acceleration channel needed by the RTK mixed spatial-kinetic fingerprint.

A pointwise quadratic coefficient match is

`beta3 = K/(M^2 M_K^2)`

for the target term `K/(2 M_K^2) (grad dot(pi))^2`.

## Important boundary: fully degenerate DHOST is not the rescue route

The same primary source states that the generic higher-order EFT has a rational scalar dispersion in `k^2`, but that imposing either complete DHOST degeneracy set `C_I` or `C_II` simplifies the scalar dispersion to a linear form `omega^2 = c_s^2 k^2`.

This means the previous idea of using fully degenerate Class-Ia DHOST as the direct home of the exact RTK rational pole was too broad.  Within this quadratic EFT framework, full DHOST degeneracy removes precisely the rational momentum dependence we want to retain.

This is a boundary on the completion architecture, not a no-go for RTK phenomenology.

## Surviving rescue route

The correct surviving target is **U-DHOST / partial unitary-gauge degeneracy**, not full DHOST degeneracy.

Relevant primary sources:

- De Felice, Langlois, Mukohyama, Noui, Wang, arXiv:1803.06241: U-degenerate theories can possess an instantaneous/shadowy mode rather than an Ostrogradsky propagating ghost.
- Kobayashi, Hiramatsu, arXiv:2310.11041 / PRD 109, 064091 (2024): a subset of U-DHOST evades solar-system tests while gravitational waves propagate luminally, while still allowing cosmological tests.
- Saito, Yao, Kobayashi, arXiv:2402.10459 / JCAP 06 (2024) 040: PPN parameters are mapped to EFT parameters and an explicit U-degenerate model with GR-valued PPN parameters is exhibited.

Thus the high-priority intersection problem becomes:

1. retain nonzero `beta3` at the value required by the RTK acceleration channel;
2. impose only the U-DHOST degeneracy relation needed to avoid a propagating Ostrogradsky ghost;
3. impose `alpha_T=0` / luminal tensors;
4. impose the exact weak-field/PPN-safe subspace from the 2024 analyses;
5. derive the resulting scalar constraint matrix and test whether the RTK rational denominator survives;
6. only then attempt one-fixed-action FLRW matching to replay-certified `C(a), M_K(a)`.

## Proven in this iteration

- `beta3` is the acceleration/lapse-gradient EFT channel.
- At quadratic operator level it maps to `(grad dot(pi))^2`.
- The RTK target coefficient can be matched pointwise by `beta3 = K/(M^2 M_K^2)`.
- Fully degenerate DHOST is not the correct direct rescue branch for an exact rational scalar dispersion in the cited quadratic EFT; the partially degenerate U-DHOST branch remains open.

## Not proven

- The PPN-safe U-DHOST subset has nonzero beta3 compatible with the RTK value.
- The exact RTK rational pole survives after all U-DHOST constraints and matter coupling are imposed.
- A single fixed covariant action reproduces the entire cosmological `C(a), M_K(a)` history.
- Compact-object/universal-horizon regularity for the selected completion.
- Nonlinear strong-coupling and radiative stability.

## Next gate

Extract the explicit U-DHOST PPN-safe conditions from arXiv:2310.11041 and arXiv:2402.10459, translate them into the `{alpha_L, alpha_T, alpha_H, beta1, beta2, beta3, ...}` basis, and solve the algebraic intersection with `beta3 != 0` and the RTK coefficient requirement.  A nonempty intersection would be the first real PPN+GW+operator-level rescue candidate; an empty intersection would close this U-DHOST sub-route.
