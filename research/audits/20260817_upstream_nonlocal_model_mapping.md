# Pinned upstream nonlocal model mapping audit

Status: **resolved: model=1 is RR, model=2 is RT**.

Pinned upstream: `dirian/class_public` commit `36cf283628c4a3330ec9fd3d84239bf775f77317`.

## Why this audit was necessary

The pinned upstream contains contradictory comments:

- `include/background.h` labels `model` as `0=LCDM, 1=R Box^-2 R, 2=(g_munu R)^T`, i.e. 1=RR and 2=RT.
- a nearby parser comment in `source/input.c` says `0 -> LCDM, 1 -> RT, 2 -> RR`.

The comments therefore cannot be used as authority.

## Resolution from the implemented equations

The actual branch equations resolve the mapping.

### model == 1

The auxiliary fields obey, schematically,

`U'' + 2 a H U' = a^2 R`,

and

`V'' + 2 a H V' = a^2 H0^2 U`.

This is the sequential scalar inverse-box structure of the `R Box^-2 R` / RR model: U is sourced by R and the second scalar auxiliary field is sourced by U.

### model == 2

U has the same inverse-box Ricci source, but V obeys the distinct transverse-projection dynamics, schematically

`V'' = a^2 [ U' + (H'/a + 5 H^2) V ]`,

and the background nonlocal density/pressure enter through the RT-style transverse construction rather than the RR scalar `R Box^-2 R` action branch.

Therefore the actual code semantics are:

- `model = 0`: LCDM;
- `model = 1`: RR (`R Box^-2 R`);
- `model = 2`: RT (`(g_munu Box^-1 R)^T`).

This agrees with `background.h` and shows that the contradictory parser comment is stale.

## Consequence for RTK

The RTK patch deliberately hooks Khronon behavior under `pba->model == 2`. This is therefore the intended **RT** branch, not RR. No reinterpretation of the current RTK results as RR+Khronon is required.

## Required future guard

Any rebuild from upstream must verify the model mapping from code/equations or a trusted mapping lock, not from the stale `input.c` comment. Future pinned-build workflows should fail closed if the upstream branch semantics change around `model==2`.
