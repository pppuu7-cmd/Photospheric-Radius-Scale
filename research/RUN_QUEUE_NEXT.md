# RTK Research Queue Next

Date: 2026-08-21

## Current decision

Continue using existing GitHub research architecture. Do not start old benchmark jobs.

## Priority queue

1. B10 lambda identifiability
   - profile lambda_D with re-optimization
   - store objective curve
   - preserve provenance

2. B6 AlterBBN
   - move from H(T) validation to abundance observables
   - paired RTK/LCDM comparison

3. B9 lensing
   - validate Phi+Psi pipeline
   - compare CMB lensing residuals

4. Formula Bible expansion
   - action
   - variation
   - background
   - perturbations

## Required outputs

Every run must save:

- run id
- git SHA
- parameters
- checkpoint
- result summary
- conclusion
