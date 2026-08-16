# RTK AI Auto-Research Agent

This directory contains a guarded OpenAI-driven orchestration layer for the RTK Stage4D3 research frontier.

## What it does

- Reacts immediately to completion of known RTK frontier workflows via `workflow_run`.
- Also polls every 5 minutes as a fallback.
- Downloads JSON summaries from new successful workflow artifacts.
- Sends the compact frontier state and summaries to the OpenAI Responses API.
- Accepts only: `WAIT`, `RECENTER`, `STATIONARITY`, `REDISCOVERY_FOLLOWUP`.
- Re-validates the scientific gate and all numerical parameters locally before any dispatch.
- Dispatches only `.github/workflows/rtk-agent-scientific-gate.yml`.
- Stores `last_processed_run_id` in `rtk/agent/frontier_state.json` to prevent duplicate advances.

The model has no arbitrary shell command or arbitrary repository-write interface.

## Enable

1. Create an OpenAI API key in the OpenAI API Platform.
2. In GitHub open the repository -> Settings -> Secrets and variables -> Actions -> New repository secret.
3. Name the secret exactly `OPENAI_API_KEY` and paste the key value.
4. Optional: Settings -> Secrets and variables -> Actions -> Variables -> New repository variable. Name it `OPENAI_MODEL`. If absent, the orchestrator defaults to `gpt-5`.
5. Run `RTK AI auto-research agent` manually once, or wait for a monitored scientific workflow to complete.

## Disable

Delete or rename the `OPENAI_API_KEY` repository secret. The workflow will then exit without making an API call or dispatching scientific work.

## Security

Never commit an API key to the repository, workflow YAML, logs, issue comments, artifacts, or `frontier_state.json`. A full OpenAI secret key should be treated as a password.

## Scientific guardrails

- No advance from incomplete or failed runs.
- Stationarity requires an exact-poll improvement no larger than `1e-5`.
- Clean-room fixed-lambda rediscovery must first go through a 7D follow-up before stationarity certification.
- Local optimization is never labeled a global minimum.
- All dispatched numerical parameters are range-checked before CLASS is built.
