# Final-center RTK late-time GW propagation / standard-siren checkpoint

## Scope

This closes the implemented **late-time tensor propagation and standard-siren** subtheory. It does not claim a completed primordial tensor-generation/inflation sector and is not a GW likelihood or new fit.

## Source equation audit

For pinned CLASS `36cf283628c4a3330ec9fd3d84239bf775f77317`, model=2 implements the tensor propagation term equivalent to

`h'' + [2 a H - 3 H0^2 gamma V] h' + k^2 h = source`.

Define

`delta = 3 H0^2 gamma V / (2 a H)`.

Then the equation has the standard modified-friction form

`h'' + 2 a H (1-delta) h' + k^2 h = source`.

The coefficient of `k^2 h` is unchanged, so the implemented propagation speed is `c_T/c = 1`.

The WKB amplitude transport therefore gives

`dL_GW/dL_EM = exp[- integral_0^z delta(z')/(1+z') dz']`.

## Final frozen-center run

- workflow run `32149794234` — success
- artifact `9329259757`, `rtk-current-standard-siren`
- digest `sha256:62e38891099d6368f0d7c07bb340ad2178b5a6f70388d9d02e5212d720f7830e`
- research source SHA in artifact `d7d645dd362c1914410965cbb6d65f51c58ef9e3`
- state iteration `78`
- objective `matched-ultra-linstep2+dense-BOSS`
- axis run `32113618318`
- exact final center:
  - As `2.0877827951474356e-09`
  - Ob `0.046800730927437424`
  - Om `0.2522864064078236`
  - h `0.691103719964454`
  - lambda_D `219457.5727136581`
  - ns `0.9645577770978523`
  - zre `7.328459220286924`
- solved `gamma = 0.05170371280716`
- CLASS background coverage extends to `z = 1e14`.

## Final prediction

| z | dL_GW / dL_EM | fractional difference |
|---:|---:|---:|
| 0.10 | 0.9866958049384597 | -1.3304% |
| 0.38 | 0.9636148308864113 | -3.6385% |
| 0.51 | 0.9571936978078017 | -4.2806% |
| 0.61 | 0.9533843790965835 | -4.6616% |
| 1.00 | 0.9442290020510891 | -5.5771% |
| 2.00 | 0.9366095412646195 | -6.3390% |
| 5.00 | 0.9337048643856870 | -6.6295% |

The background-grid minimum ratio is `0.933306567449696` and `delta_friction` ranges from `0` to `0.15247480191697357` over the stored background.

## Closure

🚀 **B7 late-time tensor/GW propagation and standard-siren sector is closed for the implemented RT model=2 cosmology.** The propagation equation, sign, normalization, unit-speed tensor gradient term, and final-center distance-ratio prediction are reproducibly specified.

Claim boundary: primordial tensor generation, an inflationary tensor spectrum, and observational GW constraints are not implied by this checkpoint.
