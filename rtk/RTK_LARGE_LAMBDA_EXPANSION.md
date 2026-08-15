# RT+DBI-Khronon — large-`lambda_D` expansion

This note records the asymptotic expansion that is relevant for Stage 4D1.
It is an analytic model-internal result, not an observational constraint.

Define

\[
A \equiv \frac{\Omega_{K0}}{6\gamma}>0,
\qquad
\epsilon_D \equiv \lambda_D^{-1/2},
\qquad
\delta_D \equiv \lambda_D^{-1}=\epsilon_D^2.
\]

The formulas below hold at fixed positive `A` and fixed finite scale factor `a` while `lambda_D -> infinity`.  A full closure solution can additionally induce a weak `gamma(lambda_D)` dependence; that should be treated separately in numerical profile work.

## Exact present normalization

The stable exact solution for the present DBI integration constant is

\[
x_0=
\frac{A(2+\lambda_D A)}
{1+\lambda_D A+\sqrt{1+2A+\lambda_D A^2}}.
\]

Expanding in `epsilon_D` gives

\[
\boxed{
x_0
=A-A\epsilon_D+(A+1)\epsilon_D^2
-\left(A+1+\frac{1}{2A}\right)\epsilon_D^3
+(A+1)\epsilon_D^4+O(\epsilon_D^5)
}.
\]

Thus `x0` itself contains an `O(epsilon_D)` term.  However, the physical density combination has a first-order cancellation.

## Density: first-order cancellation

With

\[
x=x_0a^{-3},\qquad
s=\sqrt{1+\lambda_Dx^2},\qquad
t=\frac{x}{s+1},
\]

and

\[
8\pi G\rho_K=2\mu_K^2 x(1+t),
\]

the exact large-`lambda_D` expansion is

\[
\boxed{
x(1+t)=
\frac{A}{a^3}
-\frac{a^3-1}{a^3}\,\epsilon_D^2
+\frac{a^6-1}{2Aa^3}\,\epsilon_D^3
+O(\epsilon_D^4)
}.
\]

There is **no `O(epsilon_D)` term**.  Since the present normalization is exact, the correction vanishes at `a=1`.

Using `2 mu_K^2 A = 3 H0^2 Omega_K0`, the relative density departure from pressureless dust is therefore

\[
\boxed{
\frac{\rho_K(a)}{\rho_{K0}a^{-3}}
=1+\frac{1-a^3}{A}\,\frac{1}{\lambda_D}
+O(\lambda_D^{-3/2})
}.
\]

Hence the leading background departure is naturally linear in

\[
\delta_D=\frac{1}{\lambda_D}.
\]

## Pressure and equation of state

For

\[
r=\frac{x}{s},\qquad
8\pi G P_K=2\mu_K^2 rt,
\]

one finds

\[
r=\epsilon_D-\frac{a^6}{2A^2}\epsilon_D^3+O(\epsilon_D^4),
\]

\[
t=\epsilon_D-\frac{a^3}{A}\epsilon_D^2
+\frac{a^3(-2A+a^3)}{2A^2}\epsilon_D^3
+O(\epsilon_D^4),
\]

and therefore

\[
rt=\epsilon_D^2-\frac{a^3}{A}\epsilon_D^3+O(\epsilon_D^4).
\]

The Khronon equation of state is

\[
\boxed{
w_K
=\frac{a^3}{A}\epsilon_D^2
-\frac{a^6}{A^2}\epsilon_D^3
+O(\epsilon_D^4)
=\frac{a^3}{A\lambda_D}+O(\lambda_D^{-3/2})
}.
\]

Thus the pressureless limit is approached as `1/lambda_D` at leading order.

## Adiabatic and rest-frame sound speed

The exact adiabatic sound speed is

\[
c_a^2=\frac{r}{Q s^2},\qquad Q=1+r.
\]

Its asymptotic behavior is

\[
\boxed{
c_a^2
=\frac{a^6}{A^2}\epsilon_D^3
+\frac{a^6}{A^2}\epsilon_D^4
+O(\epsilon_D^5)
=\frac{a^6}{A^2}\lambda_D^{-3/2}+O(\lambda_D^{-2})
}.
\]

The implemented scale-dependent sound speed

\[
c_s^2(a,k)=\frac{c_a^2}{1+k^2/k_*^2}
\]

therefore vanishes at least as fast as `lambda_D^(-3/2)` at fixed finite `k`.

## Transition scale

Since

\[
M_K=\mu_K Q s^{3/2},\qquad k_*=aM_K,
\]

and `s ~ x/epsilon_D`, the leading transition scale is

\[
\boxed{
k_*(a)
\sim \mu_K A^{3/2}a^{-7/2}\epsilon_D^{-3/2}
=\mu_K A^{3/2}a^{-7/2}\lambda_D^{3/4}
}.
\]

Thus `k_* -> infinity`: at every fixed cosmological wavenumber the finite-sound-speed transition is pushed away as the Khronon approaches dust.

## Consequence for the likelihood profile

The physical density and equation-of-state departures begin at

\[
O(\delta_D)=O(1/\lambda_D),
\]

while the sound-speed departure begins at

\[
O(\delta_D^{3/2})=O(\lambda_D^{-3/2}).
\]

Therefore, if the exact profiled objective is minimized at the dust boundary, the high-`lambda_D` tail can naturally have the leading form

\[
\boxed{
S(\lambda_D)=S_\infty+\frac{C}{\lambda_D}+\cdots
}
\]

rather than a leading term proportional to `lambda_D^(-1/2)`.  Stage 4D1 uses this only as an **asymptotic-shape diagnostic**.  A fitted intercept `S_inf` is not a substitute for a global profile likelihood, a confidence construction, or Bayesian evidence.

## Statistical interpretation

If the numerical profile continues to decrease toward `lambda_D -> infinity`, then the DBI scale is not measured at a finite value.  The appropriate reported result is a bound on the finite-deviation coordinate, e.g.

\[
\delta_D=1/\lambda_D\ge0
\]

or equivalently `epsilon_D=lambda_D^(-1/2) >= 0`, with the best-fit boundary at zero.  Because zero is a parameter-space boundary, ordinary interior-point Wilks thresholds must not be converted mechanically into confidence levels.  Stage 4D1 threshold crossings are therefore retained only as numerical profile-shape diagnostics until a boundary-aware frequentist calibration or a declared-prior posterior analysis is performed.
