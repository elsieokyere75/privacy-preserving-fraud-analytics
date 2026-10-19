
import pytest

from src.benchmark_aggregation import (
    benchmark_workload,
    ordinary_aggregate,
    secret_share_aggregate,
)


def test_ordinary_aggregate_adds_counts():
    assert ordinary_aggregate([39, 39]) == 78


def test_secret_share_aggregate_matches_ordinary_total():
    counts = [39, 39, 12, 5]

    assert secret_share_aggregate(counts) == ordinary_aggregate(counts)


def test_secret_share_aggregate_handles_no_institutions():
    assert secret_share_aggregate([]) == 0


def test_benchmark_workload_reports_matching_total():
    result = benchmark_workload(2, repetitions=3)

    assert result["institutions"] == 2
    assert result["total"] == 51
    assert result["ordinary_ms"] >= 0
    assert result["secret_share_ms"] >= 0
    assert result["overhead_ratio"] >= 0


def test_benchmark_workload_rejects_zero_repetitions():
    with pytest.raises(ValueError):
        benchmark_workload(2, repetitions=0)
