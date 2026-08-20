# RTK Route-B research iteration — 2026-08-20T01:16:19Z

Europe/Helsinki time: `2026-08-20T04:16:19+03:00`  
Status: **mixed: production-code dictionary established; new theorem/numerical gates pending CI artifact validation**

## Scope

This manual theory iteration continues from `RTK_ROUTE_B_BPS_TARGET_INVERSION_C8_CANDIDATE.md` and is deliberately independent of chat history. The repository remains authoritative.

## 1. Production-code RTK -> rational-pole dictionary established

Direct audit of `rtk/khronon_background.c` gives

- `x(a) = x0/a^3`;
- `s = sqrt(1 + lambda_D x^2)`;
- `r = x/s`;
- `Q = 1+r`;
- `c_a^2 = r/[s(s+x)]`;
- `M_K = mu_K Q s^(3/2)`;
- `k_* = a M_K`;
- `c_s^2(k,a) = c_a^2/[1 + (k/k_*)^2]`.

Therefore, with physical momentum `p=k/a`, the exact quadratic target dictionary used by the Route-B BPS theorem is

`C(a) = c_a^2(a)`,  
`Mdisp(a) = M_K(a)`,  
`k_*(a) = a M_K(a)`.

**Guard:** `lambda_D` is not `Mdisp`. It affects `x0`, `s`, and hence `c_a^2` and `M_K` indirectly. A direct numerical identification `lambda_D=Mdisp` is forbidden.

The positive `gamma` entering `mu_K=3 H0 sqrt(gamma)` must be the same bracketed full-CLASS normalization root used by the frozen RTK point; it is not guessed from `lambda_D`.

## 2. Production momentum domain frozen for the dictionary gate

The production likelihood harness uses `P_k_max_h/Mpc = 5.0` and the frozen dense redshift grid extending through `z=1`. For physical momentum this means

`p_max(z) = [5 h/Mpc]/a = 5 h (1+z) / Mpc`.

The new state-driven gate evaluates the full 27-point frozen dense-z grid rather than choosing a single convenient epoch.

## 3. New exact constrained-cutoff theorem candidate

Research worker commit: `8d71bec481b6f2285d210fa76e6827db34b11794`  
Workflow commit: `3505adab7689ae42e846ccafedaf3ee5bbe2aca9`  
Launch commit: `478b6e2a0cafcb78e194c5a409866533032c7fa6`

For the exact inverse family

`alpha(h)=2h/(3C+h)`,  
`ell(h)=lambda-1=2h/[3(1-h)]`,

impose abstract low-energy caps

`0 < alpha <= alpha_cap < 2`,  
`0 < ell <= ell_cap`.

Both parameters are strictly increasing in `h`, so the caps invert exactly to

`h_alpha = 3 alpha_cap C/(2-alpha_cap)`,  
`h_ell = 3 ell_cap/(2+3 ell_cap)`.

Let the unconstrained optimum be

- `h0=3(1-C)/4` for `0<C<=1/3`;
- `h0=6C/(9C+1)` for `C>=1/3`.

Then the constrained optimum candidate is exactly

`h_opt,cap = min(h0, h_alpha, h_ell)`.

No parameter scan is required. The cutoff is evaluated on the same exact BPS branches at this `h`.

Small-cap asymptotics show explicitly that forcing the LV parameters to zero collapses the available cutoff only as a square root of the active cap:

- `C<1`, alpha-cap active: `Lambda_p/M_P ~ sqrt(alpha_cap) C^(3/4)`;
- `C<1`, ell-cap active: `Lambda_p/M_P ~ sqrt(ell_cap) C^(1/4)`;
- `C>1`, alpha-cap active: `Lambda_p/M_P ~ sqrt(alpha_cap) C^(-1/4)`;
- `C>1`, ell-cap active: `Lambda_p/M_P ~ sqrt(ell_cap) C^(-3/4)`.

**Interpretation:** the relevant future phenomenological criterion is the capped hierarchy `p_req < M_P F_cap(C,alpha_cap,ell_cap)`, not merely the unconstrained `Fmax(C)`.

Status remains **CANDIDATE** until the dedicated GitHub Actions artifact is inspected.

## 4. State-driven current-center scale dictionary gate launched

Research script commit: `ce12bc4683266c9190b456157993edbdded3f6f6`  
Initial workflow commit: `1c11191b5296006a76bd2757801541808f86e490`  
Hardened workflow commit: `397521d3142f3e2fe299a5dd634de49924c90c6a`  
Launch commit: `a500c421d006cf2ff5332bed593aca5989e3c1e7`

The workflow is fail-closed against the independently replay-certified state:

- requires replay status `PASS`;
- requires objective fingerprint `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`;
- requires pinned CLASS upstream `36cf283628c4a3330ec9fd3d84239bf775f77317`;
- requires the top-level accepted score parameters to equal the independent replay RTK parameters exactly;
- solves the positive full-CLASS `gamma` root;
- evaluates `C(a)`, `M_K(a)`, `k_*(a)` over all 27 frozen dense redshifts;
- uses production `P_k_max_h/Mpc=5.0`;
- reports the dimensionless required hierarchy `M_P/M_K` for `epsilon=1e-2,1e-3,1e-4` without yet assigning a numerical Planck-mass convention.

This separation is intentional: the dictionary gate should not be contaminated by a unit/convention assumption about `M_P`.

## 5. Pending gates after this iteration

1. Inspect and validate the original composed BPS inversion+C8 workflow artifact launched at commit `efc6813e52d3f9f147aa4cedc68f5fdd03339087`.
2. Inspect and validate the constrained-cutoff theorem artifact launched at `478b6e2a0cafcb78e194c5a409866533032c7fa6`.
3. Inspect the current-center scale dictionary artifact launched at `a500c421d006cf2ff5332bed593aca5989e3c1e7` and record the worst hierarchy requirements over the dense-z grid.
4. Freeze a separate Planck-mass convention/unit audit before comparing the numerical physical hierarchy to the required hierarchy.
5. Source phenomenological `alpha`/`ell` constraints separately, then apply the constrained theorem. Do not hard-code unsourced observational caps into the theorem.
6. Continue nonlinear DOF/constraint closure, radiative stability, matter-sector Lorentz-violation and off-shell source/residue equivalence as independent gates.

## Non-claims

This iteration does not establish global cosmological preference, posterior evidence, nonlinear completion, radiative stability, matter-sector safety, or off-shell equivalence. A workflow launch is not a scientific PASS.
