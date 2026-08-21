# RTK Experiment Protocol

## Goal

Define reproducible numerical research iterations.

## Before each run

Record:

- git SHA
- configuration hash
- dataset versions
- model parameters
- numerical tolerances

## During run

Store:

- checkpoint state
- intermediate results
- warnings/errors
- runtime statistics

## After run

Produce:

- result summary
- scientific interpretation
- limitations
- next action

## Decision rule

A result closes a question only when the mathematical argument or numerical experiment is independently reproducible.
