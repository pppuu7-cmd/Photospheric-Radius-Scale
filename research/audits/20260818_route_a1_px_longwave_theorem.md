# Route A1 long-wave P(X) reconstruction theorem

Date: 2026-08-18

Status: **D3 long-wave coefficient reconstruction closed conditionally within the explicitly postulated Route A1 / shift-symmetric barotropic P(X) subsector. Full finite-k nonlinear completion remains open.**

## Scope

This result applies only to the reduced scalar Route A1 research completion in the long-wavelength shift-symmetric barotropic P(X) subsector. It is not a derivation of a covariant fundamental RTK action and is not a proof of the full coupled metric + RT + Khronon theory.

## Exact identities proved

Using the implemented Khronon background formulas with x=x0/a^3, symbolic CI proves:

1. `x d rho/dx = rho + p`;
2. `dp/d rho = c_a^2`;
3. for the conserved-density reconstruction `sqrt(2X) proportional to (rho+p)/x`, `d ln X/d ln x = 2 c_a^2`;
4. the quadratic Goldstone coefficients are
   - `G = rho+p`,
   - `K = (rho+p)/c_a^2`.

For a shift-symmetric P(X) expansion the two D3 cubic operators are therefore fixed by background thermodynamics:

`c1 = (dK/dlnX - K)/3 = ((dK/dlnx)/(2 c_a^2) - K)/3`,

`c2 = -(K-G)/2`.

Thus the D3 long-wave coefficients are not free parameters once the Route A1/P(X) conditional completion is selected.

## What is not fixed

The higher-spatial-derivative D4 Route-A1 operators, represented by coefficients `c3` and `c4`, are not determined by the homogeneous barotropic background. Pure P(X) also does not by itself reproduce the finite-k quadratic term responsible for the implemented scale-dependent sound-speed suppression. Therefore:

- finite-k nonlinear completion is still open;
- c3 and c4 remain open;
- the full strong-coupling/EFT cutoff remains open;
- M_K or k_star must not be relabeled as the strong-coupling cutoff without a separate derivation.

## Machine proof provenance

Workflow run: `32074936280`

Job: `95525982737`

RTK source SHA checked out by theorem run: `2d60d0223158435b60d29d6963ea654252f303ee`

Artifact: `9303072040` (`rtk-route-a1-px-reconstruction`)

Artifact SHA256: `4d51c32d2a1537c013746a1dfe56074ed05d348f7d5117a11d6f4fb8434d7a73`

Classification: `RTK_ROUTE_A1_PX_LONGWAVE_RECONSTRUCTION_PASS`

## Closure statement

✅ Closed: long-wave D3 thermodynamic reconstruction of c1 and c2 within Route A1/P(X).

🔴 Open: D4 coefficients c3,c4 and finite-k completion.

🔴 Open: physical strong-coupling scale and full coupled ghost/constraint theorem.
