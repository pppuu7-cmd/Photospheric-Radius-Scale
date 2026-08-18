# RTK AlterBBN standard-network self-test protocol v1

Status: **FROZEN BEFORE FIRST STANDARD-NETWORK EXECUTION**.

This is the first executable subgate of B6 after the published AlterBBN v2.2 source bytes were pinned. It does not inject RTK H(T), does not compare RTK to observations, and does not alter the frozen late-time matched objective.

## Source lock

Use exactly `research/robustness/alterbbn_v2_2_source_lock.json`:

- DOI `10.17632/k7j3b9zyvf.1`;
- file `alterbbn_v2.2.tar.xz`;
- SHA-256 `2bcb7d2e3f4a74f59cd589e60f0923892bb90296a793f80016897405920c5fae`;
- 2,586,656 bytes;
- published AlterBBN version string `2.2 (16th July 2019)`.

Any byte mismatch is a hard failure.

## Build environment

- GitHub runner `ubuntu-24.04`;
- explicitly select `gcc-13` when available from the runner image/package manager;
- record the exact compiler version;
- compile the unmodified published source first;
- preserve the source Makefile's physics/numerical source files and rate tables.

No RTK patch is permitted in this self-test.

## Runs

Build `stand_cosmo.x` and execute two declared precision modes:

1. `failsafe=1` — the published README describes modes 1–3 as more precise stiff methods;
2. `failsafe=7` — stiff method with the README's 0.1% precision-test setting.

The published `stand_cosmo.c` returns exit status 1 even after its normal reporting path, so the workflow must validate output content explicitly rather than incorrectly treating return code 1 as a physics failure.

## Parsed quantities

From each run record the central (`cent:`) values of at least:

- `Yp`;
- `H2/H` (D/H);
- `He3/H`;
- `Li7/H`;
- `Li6/H`;
- `Be7/H`.

Retain full stdout/stderr.

## Fail-closed acceptance criteria

Both precision modes must:

1. reach the normal abundance-reporting path;
2. produce finite positive central abundances;
3. satisfy broad predeclared physical sanity ranges:
   - `0.20 < Yp < 0.30`;
   - `1e-5 < D/H < 5e-5`;
4. agree under refinement at least to:
   - relative `Yp` difference `< 0.005` (0.5%);
   - relative D/H difference `< 0.02` (2%).

These broad tolerances are self-test criteria, not observational abundance constraints and not the final B6 numerical-refinement tolerance.

## Required provenance artifact

The self-test artifact must record:

- source DOI/file/SHA/byte count;
- compiler version;
- runner OS information;
- archive member list or source-tree digest;
- build commands;
- return codes;
- parsed central abundances for both precision modes;
- relative refinement differences;
- an explicit warning that no RTK H(T) has yet been injected.

## Closure semantics

Passing this protocol earns only:

`✅ AlterBBN published-source + standard-network self-test subgate closed`.

It does **not** close B6. B6 still requires RTK H(T) injection, no-extrapolation/interpolation validation, paired abundance calculation, numerical refinement of the RTK effect, and comparison with a separately preregistered observational abundance set.
