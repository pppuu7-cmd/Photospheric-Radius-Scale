# RT + DBI-Khronon CLASS integration testbed

This repository is being used as a reproducible CI testbed for integrating the tested DBI-Khronon modules into the public `dirian/class_public` `nonlocal` branch.

The GitHub Actions workflow checks out the upstream RT-CLASS branch, stages the Khronon C modules, compiles the standalone perturbation tests, and attempts a full `make class` build.

This is a research prototype, not an observationally validated cosmological model.

## Continue the research without chat history

Start with [`research/checkpoints/RTK_CHAT_INDEPENDENT_RECOVERY.md`](research/checkpoints/RTK_CHAT_INDEPENDENT_RECOVERY.md) for the human-readable recovery guide and [`research/checkpoints/RTK_CHAT_INDEPENDENT_STATE.json`](research/checkpoints/RTK_CHAT_INDEPENDENT_STATE.json) for a compact machine-readable snapshot.

The live production source of truth remains `research/state/current.json` on branch `rtk-class-build`; recent monitored workflow state is stored in `research/runtime/actions_index.json` on that branch. Historical checkpoints must not override those live records when they disagree.
