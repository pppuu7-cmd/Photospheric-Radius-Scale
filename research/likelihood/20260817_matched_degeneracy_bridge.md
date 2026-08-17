# Matched RTK–LCDM degeneracy bridge diagnostic

Provenance: GitHub Actions run `32056872370`, artifact `9297510685`, artifact digest `sha256:ae8c45d83546924d2ee192bcedab8ca635eee1a58ee6b37cce99dc6bcb3081b6`.

Objective: `matched-ultra-linstep2+dense-BOSS`.

This is a straight-line diagnostic in the six shared parameters `(As, Ob, Om, h, ns, zre)`, with `alpha=0` at the accepted LCDM shared center and `alpha=1` at the then-current RTK shared center. Both model sectors were evaluated at every shared point. It is not a profile likelihood, posterior, evidence calculation, or proof of topological disconnection.

## Main result

The two good-fit endpoints are not connected by a good-fit straight-line valley. Near the model-sector crossover, around `alpha ≈ 0.503` by interpolation of `S_RTK-S_LCDM`, both models are far above their endpoint minima.

At `alpha=0.5`:

- LCDM: `S = 1104.511501067013`
- RTK: `S = 1105.7611064586556`
- `S_RTK-S_LCDM = +1.2496053916427172`

Relative to the endpoint local scores used by this diagnostic:

- LCDM straight-line ridge height: `1104.511501067013 - 1049.96861444706 = 54.542886619953`
- RTK straight-line ridge height: `1105.7611064586556 - 1050.332707865856 = 55.428398592800`

The model-sector score difference changes from `+1.2496` at `alpha=0.5` to `-55.1460` at `alpha=0.625`, giving a linear-interpolation crossover near `alpha ≈ 0.50277`.

The crossover is dominated by high-ell Planck. At `alpha=0.5`, the Planck contribution to `S_RTK-S_LCDM` is `-0.65797`, while BOSS contributes `+2.06089` and Pantheon `-0.15331`; the total is `+1.24961`.

## Interpretation

The matched RTK and LCDM local candidates occupy strongly different correlated CMB parameter manifolds. A direct straight interpolation of the shared cosmological parameters crosses a high objective ridge of about 55 in `S`. This supports strong non-separability of the model sector and standard-parameter retuning, but does **not** prove that no curved low-score path exists in the full parameter space.
