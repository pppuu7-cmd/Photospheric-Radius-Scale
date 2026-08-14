# RT + DBI-Khronon CLASS integration testbed

This repository is being used as a reproducible CI testbed for integrating the tested DBI-Khronon modules into the public `dirian/class_public` `nonlocal` branch.

The GitHub Actions workflow checks out the upstream RT-CLASS branch, stages the Khronon C modules, compiles the standalone perturbation tests, and attempts a full `make class` build.

This is a research prototype, not an observationally validated cosmological model.
