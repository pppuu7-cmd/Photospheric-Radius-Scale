# RTK Local Compute Node Architecture

Created: 2026-08-21

## Goal

Transform RTK research from chat-dependent experiments into a reproducible distributed local computation system.

## Design

```
Local PC
  |
  +-- Ubuntu WSL2
        |
        +-- RTK Engine
              |
              +-- Worker pool
              +-- Checkpoint manager
              +-- Progress monitor
              +-- Result validator
              +-- Research ledger
```

## Requirements

Every computation must record:

- run id
- UTC timestamp
- source commit SHA
- configuration hash
- worker count
- elapsed time
- checkpoint state
- scientific conclusion

## Failure recovery

A stopped calculation must resume from the latest valid checkpoint without losing completed work.

## Scientific reproducibility

Performance improvements are secondary to exact reproducibility. Numerical results must remain traceable to code, data and configuration.

## Future expansion

Possible extensions:

- multiple home compute nodes
- community contributed runners
- independent verification runs
- public benchmark datasets
