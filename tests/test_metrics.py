from app import metrics
from app.metrics import percentile


def test_percentile_basic() -> None:
    assert percentile([100, 200, 300, 400], 50) >= 100


def test_snapshot_exposes_slo_fields() -> None:
    metrics.REQUEST_LATENCIES.clear()
    metrics.REQUEST_COSTS.clear()
    metrics.REQUEST_TOKENS_IN.clear()
    metrics.REQUEST_TOKENS_OUT.clear()
    metrics.ERRORS.clear()
    metrics.QUALITY_SCORES.clear()
    metrics.TRAFFIC = 0

    metrics.record_request(latency_ms=120, cost_usd=0.01, tokens_in=100, tokens_out=150, quality_score=0.8)
    metrics.record_request(latency_ms=3200, cost_usd=0.02, tokens_in=120, tokens_out=180, quality_score=0.7)
    metrics.record_error("RuntimeError")

    out = metrics.snapshot()

    assert out["traffic"] == 2
    assert out["total_errors"] == 1
    assert out["error_rate_pct"] == 50.0
    assert out["requests_over_slo"] == 1
    assert out["hourly_cost_usd"] >= out["total_cost_usd"]
