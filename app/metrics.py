from __future__ import annotations

from collections import Counter
from statistics import mean
import time

REQUEST_LATENCIES: list[int] = []
REQUEST_COSTS: list[float] = []
REQUEST_TOKENS_IN: list[int] = []
REQUEST_TOKENS_OUT: list[int] = []
ERRORS: Counter[str] = Counter()
TRAFFIC: int = 0
QUALITY_SCORES: list[float] = []
STARTED_AT = time.time()
LATENCY_SLO_MS = 3000


def record_request(latency_ms: int, cost_usd: float, tokens_in: int, tokens_out: int, quality_score: float) -> None:
    global TRAFFIC
    TRAFFIC += 1
    REQUEST_LATENCIES.append(latency_ms)
    REQUEST_COSTS.append(cost_usd)
    REQUEST_TOKENS_IN.append(tokens_in)
    REQUEST_TOKENS_OUT.append(tokens_out)
    QUALITY_SCORES.append(quality_score)



def record_error(error_type: str) -> None:
    ERRORS[error_type] += 1



def percentile(values: list[int], p: int) -> float:
    if not values:
        return 0.0
    items = sorted(values)
    idx = max(0, min(len(items) - 1, round((p / 100) * len(items) + 0.5) - 1))
    return float(items[idx])



def snapshot() -> dict:
    total_errors = sum(ERRORS.values())
    uptime_seconds = max(1.0, time.time() - STARTED_AT)
    uptime_hours = uptime_seconds / 3600
    over_slo_requests = sum(1 for latency in REQUEST_LATENCIES if latency > LATENCY_SLO_MS)
    error_rate_pct = round((total_errors / TRAFFIC) * 100, 2) if TRAFFIC else 0.0
    hourly_cost_usd = round(sum(REQUEST_COSTS) / uptime_hours, 4) if REQUEST_COSTS else 0.0

    return {
        "traffic": TRAFFIC,
        "uptime_s": round(uptime_seconds, 1),
        "latency_p50": percentile(REQUEST_LATENCIES, 50),
        "latency_p95": percentile(REQUEST_LATENCIES, 95),
        "latency_p99": percentile(REQUEST_LATENCIES, 99),
        "requests_over_slo": over_slo_requests,
        "requests_over_slo_pct": round((over_slo_requests / TRAFFIC) * 100, 2) if TRAFFIC else 0.0,
        "avg_cost_usd": round(mean(REQUEST_COSTS), 4) if REQUEST_COSTS else 0.0,
        "total_cost_usd": round(sum(REQUEST_COSTS), 4),
        "hourly_cost_usd": hourly_cost_usd,
        "tokens_in_total": sum(REQUEST_TOKENS_IN),
        "tokens_out_total": sum(REQUEST_TOKENS_OUT),
        "tokens_in_avg": round(mean(REQUEST_TOKENS_IN), 2) if REQUEST_TOKENS_IN else 0.0,
        "tokens_out_avg": round(mean(REQUEST_TOKENS_OUT), 2) if REQUEST_TOKENS_OUT else 0.0,
        "total_errors": total_errors,
        "error_rate_pct": error_rate_pct,
        "success_rate_pct": round(100 - error_rate_pct, 2) if TRAFFIC else 0.0,
        "error_breakdown": dict(ERRORS),
        "quality_avg": round(mean(QUALITY_SCORES), 4) if QUALITY_SCORES else 0.0,
    }
