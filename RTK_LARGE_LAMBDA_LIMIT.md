# RT+DBI-Khronon — large-lambda_D limit

## Purpose

The exact joint-likelihood searches repeatedly move toward larger `lambda_D`.
This note records the analytic meaning of that direction before interpreting
any numerical boundary hit as a parameter measurement.

This is a model-internal asymptotic derivation, not an observational result.

## Present normalization

Let

A = Omega_K0 / (6 gamma)

and use the exact stable normalization

x0 = A (2 + lambda_D A) /
     [1 + lambda_D A + sqrt(1 + 2 A + lambda_D A^2)].

For fixed positive A,

x0 -> A    as lambda_D -> infinity,

with corrections beginning at order lambda_D^(-1/2).

The one-scale relation is

mu_K = 3 H0 sqrt(gamma).

Therefore at a=1,

8 pi G rho_K0 -> 2 mu_K^2 A
                = 3 H0^2 Omega_K0,

so the normalization remains finite and correct in the large-lambda limit.

## Background limit at finite scale factor

At fixed finite a > 0,

x = x0 a^(-3) -> A a^(-3),
s = sqrt(1 + lambda_D x^2) ~ sqrt(lambda_D) x,
r = x/s ~ lambda_D^(-1/2),
t = x/(s+1) ~ lambda_D^(-1/2),
Q = 1+r -> 1.

Using

8 pi G rho_K = 2 mu_K^2 x (1+t),
8 pi G P_K   = 2 mu_K^2 r t,

we obtain

rho_K -> rho_K0 a^(-3),
P_K -> 0,
w_K -> 0.

Thus the Khronon background tends to pressureless matter.

## Perturbation scales

The exact adiabatic sound speed is

c_a^2 = r/[s(s+x)].

At fixed finite a,

c_a^2 ~ 1/[lambda_D^(3/2) x^2] -> 0.

The Khronon mass and transition scale are

M_K = mu_K Q s^(3/2),
k_* = a M_K.

Hence

M_K ~ mu_K lambda_D^(3/4) x^(3/2),
k_* ~ lambda_D^(3/4) a^(-7/2)

(up to factors independent of lambda_D), so k_* -> infinity.
For any fixed cosmological wavenumber k,

c_s^2(a,k) = c_a^2/[1 + k^2/k_*^2] -> 0.

Therefore the linear Khronon perturbations approach the pressureless-dust
limit as lambda_D grows.

## Physical interpretation

The large-lambda_D limit does **not** turn the full model into LambdaCDM.
The dark-matter role becomes CDM-like, but the late-time dark-energy sector
remains the RT nonlocal model. The limiting cosmology is therefore best viewed
as

RT dark energy + pressureless Khronon dark matter.

If a properly profiled likelihood keeps improving toward lambda_D -> infinity,
then the data have not detected a finite DBI transition scale. The appropriate
statistical result would be a lower bound on lambda_D (or an upper bound on a
finite-deviation parameter such as epsilon_D = lambda_D^(-1/2)), not a finite
best-fit measurement of lambda_D.

A Bayesian evidence result in such a situation will be prior-sensitive in the
lambda_D direction. A future production inference should therefore declare the
prior/reparameterization before looking at the posterior and should not use a
data-tuned upper lambda_D cutoff as though it were a physical prior.

## Current numerical motivation

The conditional exact likelihood scan at fixed recovered RTK cosmological
parameters was monotonic over lambda_D = 1e3 ... 1e5 and showed rapid approach
to a plateau. That scan is diagnostic only because the other cosmological
parameters were held fixed. The dedicated fixed-large-lambda six-parameter
profile is the correct next local test.
