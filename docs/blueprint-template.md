# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Group15-E402
- [REPO_URL]: https://github.com/Nekoishere/Group15-E402-Day13
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Blueprint & Demo Lead

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 30
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/screenshots/evidence_correlation_id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/screenshots/evidence_pii_redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/screenshots/evidence_trace_waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: The "run" span contains two child spans: "retrieve" (mock RAG lookup, ~50ms) and "generate" (mock LLM, ~100ms). During the rag_slow incident, the "retrieve" span expanded to ~2200ms, demonstrating how distributed tracing pinpoints bottlenecks at the span level without needing log correlation.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/screenshots/evidence_dashboard.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 2651ms (SLO met — includes incident data) |
| Error Rate | < 2% | 28d | 0% (0 errors in 30 requests) |
| Cost Budget | < $2.5/day | 1d | $0.0665 total / ~$0.002 avg per request |
| Quality Score Avg | ≥ 0.75 | 28d | 0.88 ✅ |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/screenshots/evidence_alert_rules.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Latency spike from ~460ms (normal) to ~2654ms per request immediately after enabling the rag_slow incident toggle via POST /incidents/rag_slow/enable. P95 latency breached from ~770ms to 2651ms (approaching the 3000ms SLO threshold).
- [ROOT_CAUSE_PROVED_BY]: Langfuse trace waterfall — the "retrieve" span duration increased from ~50ms to ~2200ms, consuming >83% of total request latency. Log lines with correlation_id show consistent high latency_ms values (2653-2657ms) across all requests during the incident window.
- [FIX_ACTION]: Disabled the incident toggle via POST /incidents/rag_slow/disable. Latency immediately returned to normal (~460ms). In production, this maps to: identify the bottleneck RAG service, apply fallback retrieval source or truncate queries.
- [PREVENTIVE_MEASURE]: Alert rule `high_latency_p95` (Severity P2) triggers when latency_p95_ms > 5000ms for 30 minutes. Additional proactive measure: set a symptom-based alert at 2500ms threshold (closer to SLO) to catch degradation earlier.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_E_NAME] — Blueprint & Demo Lead
- [TASKS_COMPLETED]:
  1. Implemented `app/middleware.py` — Correlation ID middleware: generate `req-<8hex>`, bind to structlog contextvars, propagate to response headers `x-request-id` and `x-response-time-ms`
  2. Implemented `app/main.py` — Log enrichment: `bind_contextvars(user_id_hash, session_id, feature, model, env)` on every `/chat` request
  3. Enabled PII scrubbing in `app/logging_config.py` — registered `scrub_event` processor in structlog pipeline
  4. Fixed `.env` Langfuse key format (removed erroneous single quotes) and added `load_dotenv()` to `app/main.py` to enable tracing
  5. Ran `scripts/load_test.py` to generate 30 traces across normal and incident scenarios
  6. Validated implementation: `scripts/validate_logs.py` → **100/100** (0 PII leaks, 20 unique correlation IDs, full enrichment)
  7. Authored complete group blueprint report (sections 1–4) with real system metrics
  8. Prepared 5-minute live demo script and incident response walkthrough
- [EVIDENCE_LINK]: https://github.com/Nekoishere/Group15-E402-Day13/commits/main

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Average cost per request = $0.0022. Total 30 requests cost $0.0665 — well within $2.5/day budget. Optimization opportunity: route `summary` feature requests (higher token count) to cheaper model tier.
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: Added quality_avg metric to `/metrics` endpoint snapshot — tracks semantic quality heuristic per request. Current average: 0.88/1.0 across 30 requests.
