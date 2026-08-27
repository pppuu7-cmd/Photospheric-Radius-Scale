# RTK C10.65s6fZ12 checkpoint

Classification: `C10_65S6FZ12_BACKGROUND_QUADRATIC_UNDERSPECIFIED_BLOCKED_SCOPED`.

The HMT Eq.104 + Z7 interface fixes the scalar DOF architecture but does not yet fix a unique same-action FLRW carrier background or finite-k quadratic response. At least the carrier potential/background data, spatial-gradient coefficient, and matter/source map remain unfrozen. Two completions consistent with every Z11 interface statement therefore yield inequivalent background equations and finite-k inverse kernels. The old RTK pole/residue/remainder must not be used to choose these missing functions after the fact.

Missing same-action inputs: full_local_potential_U_Phi, background_Phi_bar_or_boundary_data, finite_k_spatial_gradient_coefficient, matter_source_coupling, carrier_HMT_auxiliary_couplings.

Frozen guards remain: no soft-s retest and no k=0.03 production.

Next: C10.65s6fZ13: independently preregister one full local HMT+Z7 carrier action (potential/background prescription, spatial-gradient sector, source/matter coupling, and any HMT-auxiliary couplings) from a pre-soft-s physical principle; only then rerun the unchanged Z12 match-ready audit and proceed to background/quadratic RTK equivalence.
