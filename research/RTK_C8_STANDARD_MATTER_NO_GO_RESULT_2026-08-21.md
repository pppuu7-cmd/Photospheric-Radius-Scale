# RTK C8 standard universal-matter no-go result

Date: 2026-08-21
Status: **GREEN scoped negative theorem**

## Question

Can the constructive direct spatial-covariant FLRW exact-match carrier be identified with the standard universally coupled low-energy Hořava matter frame while simultaneously satisfying the usual cosmological/Newton, PPN and GW constraints?

## Starting exact-match relation

The direct FLRW theorem gives the required acceleration coefficient

`C_acc,required = M_cosm^2`

when production `8 pi G` is interpreted as the carrier Friedmann coupling.

In the standard low-energy matter frame of Gumrukcuoglu, Saravani and Sotiriou, PRD 97, 024032 (2018), arXiv:1711.08845, Eqs. (7)-(12),

`G_cosm = 1/[4 pi M_*^2 (2+3 gamma+beta)]`,

`G_N = 1/[8 pi M_*^2 (1-alpha/2)]`,

and the acceleration coefficient is `M_*^2 alpha/2`.

Exact matching therefore forces

`alpha = 2+3 gamma+beta`.

On this hypersurface,

`G_cosm/G_N = (2-alpha)/alpha`.

## BBN reduction

The cited BBN bound is

`|(alpha+3 gamma+beta)/(2+3 gamma+beta)| < 1/8`.

Using the exact-match relation gives

`|2(alpha-1)/alpha| < 1/8`.

For positive alpha this is exactly

`16/17 < alpha < 16/15`,

or approximately

`0.9411764706 < alpha < 1.0666666667`.

## PPN + GW contradiction

The first translated preferred-frame PPN bound in the same source is

`|4(alpha-2 beta)/(1-beta)| <=~ 1e-4`.

Post-GW170817 tensor-speed phenomenology gives the benchmark

`|beta| <=~ 1e-15`.

Across the entire BBN-allowed alpha interval and the entire GW beta interval, triangle inequalities give

`|4(alpha-2 beta)/(1-beta)|`

`>= 4[(16/17)-2*10^-15]/(1+10^-15)`

`= 3.7647058823529296...`.

This is at least

`37647.058823529296`

times larger than the `1e-4` PPN benchmark.

Therefore there is **no parameter overlap** satisfying all of:

1. direct exact RTK FLRW matching;
2. the cited standard-matter BBN `G_cosm/G_N` bound;
3. the post-GW170817 beta bound;
4. the first preferred-frame PPN bound.

## Executable provenance

Source theorem:

- `rtk-class-build:rtk/route_b_spatial_covariant_standard_matter_no_go.py`
- source commit `303e1922cc0950ece6cf77f24525ed3e564ccd07`.

CI:

- run `32518936616` — success;
- artifact `9459822043`;
- digest `sha256:07f9e3bb7e64139a5f35df9e7aa2d77a7bfe2b06b4578a545e14354c046aca02`;
- artifact marker `RTK_ROUTE_B_SPATIAL_COVARIANT_STANDARD_MATTER_NO_GO_PASS`.

The artifact reports the exact rational lower bound

`63999999999999864/17000000000000017`

for the PPN expression on the BBN+GW allowed region.

## Scope / non-claims

This excludes only the direct acceleration-only exact carrier when mapped to the cited **standard universal low-energy Hořava matter frame**.

It does **not** exclude:

- nonminimal/disformal matter coupling;
- fixed companion operators that change static/Newton/PPN response while preserving the FLRW scalar kinetic factor;
- auxiliary constrained-field realizations;
- broader spatially covariant/covariant carriers;
- higher-spatial-gradient UV operators;
- the exact quadratic FLRW scalar theorem itself.

It is not a cosmological model-selection statement.

## Next gate

The carrier search must now move away from the standard universal matter frame. The smallest candidate deformation must be tested simultaneously for:

- exact/controlled RTK FLRW kinetic recovery;
- Newton and Friedmann normalization;
- PPN preferred-frame parameters;
- tensor/GW speed;
- scalar stability and DOF count;
- compact-object behavior;
- EFT cutoff/strong coupling;
- matter/source transfer functions.
