# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Nguyễn Công Nhật Tân - 2A202600141] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: ![Trace Waterfall](image.png)
- [TRACE_WATERFALL_EXPLANATION]: Cấu trúc vết (Trace) được trình bày dạng thác nước giúp quan sát rõ thứ tự thực thi. Vỏ bọc ngoài cùng là `run` (toàn bộ phiên xử lý). Bên trong chứa nhánh `retrieve` cho thấy thời gian tìm tài liệu và nhánh `llm-call` bao bọc tác vụ AI. Đáng chú ý là span con `generate` lọt thỏm trong `llm-call` ghi nhận chi tiết thời gian phản hồi là 0.15s, cùng thông số token (Input: 28, Output: 138). Phân tầng rõ ràng như vậy giúp kỹ sư lập tức nhìn ra nguyên nhân gây độ trễ hệ thống nằm ở AI hay do RAG truy xuất chậm.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 Latency spiked dramatically (from ~800ms baseline to >13,000ms under load of 5 concurrent requests). SLO breached.
- [ROOT_CAUSE_PROVED_BY]: The tracing span for `retrieve` showed a manual artificial 2.5s sequentially blocking sleep per query.
- [FIX_ACTION]: Disabled the `rag_slow` incident via `scripts/inject_incident.py --disable`.
- [PREVENTIVE_MEASURE]: Implement strict timeouts on the vector retrieval tool and provide a fallback retrieval strategy to avoid unbounded blocking.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [Nguyễn Công Nhật Tân]
- [TASKS_COMPLETED]: add trace observe for agent and mock_llm, mock_rag, add log enrichment
- [EVIDENCE_LINK]: Commit 9d41730 (add trace), Commit d7d8c99 (add log enrichment)

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
