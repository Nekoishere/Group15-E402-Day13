# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95 > 3000 for 15m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 2 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache

## 4. Quality regression
- Severity: P3
- Trigger: `quality_avg < 0.75 for 30m`
- Impact: responses remain available but usefulness drops below expected baseline
- First checks:
  1. Sample low-scoring traces and compare retrieved docs vs final answer
  2. Check whether prompts became too generic or docs stopped matching the query
  3. Confirm whether redact logic removed too much useful content from prompts or answers
- Mitigation:
  - tighten retrieval matching
  - improve prompt instructions for concise grounded answers
  - add a fallback answer for low-context queries
