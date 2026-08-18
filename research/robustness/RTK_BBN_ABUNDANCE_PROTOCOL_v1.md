# RTK BBN abundance robustness protocol v1

Status: **FROZEN BEFORE ABUNDANCE NETWORK EXECUTION**.

This protocol upgrades B6 from an early-time background sanity check to an abundance-level Big-Bang Nucleosynthesis test. It does not alter the matched late-time/CMB likelihood objective.

## Existing evidence and limitation

The current early-universe CLASS check reaches very high redshift and finds the RTK-vs-ΛCDM same-shared-parameter fractional expansion-rate difference rapidly tending to zero (already ~O(1e-12) by z~1e10). This is strong background evidence but it is **not** a BBN abundance calculation and cannot close B6 by itself.

## Primary solver choice

Use **AlterBBN v2 or a provenance-pinned later compatible AlterBBN release** as the primary alternative-cosmology abundance harness. The published AlterBBN design explicitly supports modifications of the cosmological expansion rate and entropy history and is therefore suited to a non-standard H(T) robustness test.

Primary references to preserve in the eventual result checkpoint:

- A. Arbey, *AlterBBN: A program for calculating the BBN abundances of the elements in alternative cosmologies*, Comput. Phys. Commun. 183 (2012) 1822–1831, arXiv:1106.1363.
- A. Arbey et al., *AlterBBN v2: A public code for calculating Big-Bang nucleosynthesis constraints in alternative cosmologies*, Comput. Phys. Commun. 248 (2020) 106982, arXiv:1806.11095.

PArthENoPE may be used later as an independent standard-BBN cross-check, but is not required for the first RTK custom-expansion gate.

## Required execution sequence

1. Pin the exact AlterBBN source revision/archive hash and compiler environment.
2. Reproduce an unmodified standard-cosmology AlterBBN reference run and record the standard light-element yields.
3. Construct an RTK expansion-history table over the BBN thermal range from the pinned RTK background implementation. The table must contain a monotone temperature/redshift coordinate and the ratio `H_RTK/H_reference` (or the exact equivalent interface required by the chosen AlterBBN modification).
4. Validate interpolation of the RTK expansion modification: positive H, no extrapolation through the nuclear-network integration range, and convergence under a denser background table.
5. Run the same nuclear network and nuclear rates for reference and RTK; **the only cosmology modification in the paired comparison is the RTK expansion history being tested**.
6. Report at minimum `Y_p` (He-4 mass fraction) and primordial D/H; also retain other AlterBBN yields produced by the run.
7. Repeat with a denser H(T) table and/or tighter integration controls. The abundance difference must be numerically stable relative to the scientific tolerance used in the interpretation.
8. Compare with a separately frozen, cited observational BBN abundance dataset/constraint set. Do not silently use whichever observational compilation is most favorable after seeing the RTK result.

## Parameter semantics

The abundance-level B6 test must state explicitly which late-time matched parameter point supplies the physical baryon density and which radiation/neutrino convention is used. The current massless production baseline and the separate 0.06-eV neutrino robustness branch must not be mixed implicitly.

The first B6 run should use the frozen massless matched parameter semantics for continuity with A1–A5. A later `m_nu=0.06 eV` BBN robustness variant may be added as a separate labeled calculation after B4.

## Acceptance semantics

B6 may receive 🚀 only when all of the following are present:

- pinned and reproducible abundance-network code;
- successful standard reference self-test;
- explicit RTK H(T) injection with provenance;
- stable paired abundance results under a numerical refinement;
- explicit observational-constraint comparison using a preregistered source;
- a checkpoint that distinguishes background agreement, abundance prediction, and observational consistency.

Until then, the existing high-redshift H(z) result remains ✅ background evidence but B6 remains open.

No claim about resolving the primordial lithium problem is permitted unless Li-7 is separately analysed with the relevant nuclear/observational systematics.
