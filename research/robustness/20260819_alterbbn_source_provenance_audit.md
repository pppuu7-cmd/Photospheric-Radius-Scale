# AlterBBN source provenance audit — 2026-08-19

**Scope:** B6 source selection only. This note does not execute a BBN network and does not close B6.

## Published source target

The primary source remains the published AlterBBN v2 program-file dataset associated with:

- A. Arbey, J. Auffinger, K. P. Hickerson, E. S. Jenssen, *AlterBBN v2: A public code for calculating Big-Bang nucleosynthesis constraints in alternative cosmologies*;
- program-files DOI: `10.17632/k7j3b9zyvf.1`;
- dataset version: `1`;
- publication date shown by Mendeley Data: `2019-10-30`;
- published file name: `alterbbn_v2.2.tar.xz`;
- published file size shown by Mendeley Data: approximately `2.47 MB`;
- dataset licence shown by Mendeley Data: `GPLv3`.

The published description explicitly identifies AlterBBN v2 as an open BBN code supporting standard and alternative cosmologies. This matches the architecture required by `RTK_BBN_ABUNDANCE_PROTOCOL_v1.md`.

## GitHub mirrors examined

Two repositories under the account `espensem` were checked as possible immutable source mirrors because E. S. Jenssen is an AlterBBN v2 author.

### `espensem/AlterBBN`

- latest observed commit: `d3cc09ade68eac73a864323ae3c3a5fa130675be`;
- latest commit date: `2017-05-16`;
- tree therefore predates the 2018 AlterBBN v2 paper and the 2019 published v2.2 program-file dataset.

### `espensem/AlterBBN_master`

- latest observed commit: `8219dd4b578244e36d56ebda31541705ae382093`;
- latest commit date: `2016-09-07`;
- this tree also predates the published AlterBBN v2/v2.2 release.

## Fail-closed source decision

Neither inspected GitHub tree is accepted as a drop-in substitute for the DOI-published `alterbbn_v2.2.tar.xz` snapshot. They may be useful historical references, but their content identity relative to the published v2.2 archive has not been demonstrated.

The B6 abundance workflow must therefore **not** clone either moving/default branch and call it AlterBBN v2.2.

## Remaining source-provenance gate

Before first BBN network execution:

1. obtain the immutable DOI-published `alterbbn_v2.2.tar.xz` bytes or an independently mirrored copy whose byte identity to the DOI file can be established;
2. compute and freeze its cryptographic digest (SHA-256 preferred);
3. record archive file list / extracted source identity;
4. build with a declared compiler/runtime environment;
5. reproduce a standard-cosmology self-test before applying any RTK H(T) modification.

Until those steps pass, B6 remains open. The existing high-redshift RTK/LCDM H(z) convergence result is background evidence only and is not an abundance calculation.
