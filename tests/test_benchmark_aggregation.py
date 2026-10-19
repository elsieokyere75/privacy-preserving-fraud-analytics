
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


import csv

from src.benchmark_aggregation import save_results


def test_save_results_creates_readable_csv(tmp_path):
    output_path = tmp_path / "results" / "benchmark.csv"

    results = [
        {
            "institutions": 2,
            "total": 51,
            "ordinary_ms": 0.001,
            "secret_share_ms": 0.005,
            "overhead_ratio": 5.0,
            "repetitions": 101,
            "results_match": True,
        }
    ]

    save_results(results, output_path)

    assert output_path.exists()

    with output_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["institutions"] == "2"
    assert rows[0]["total"] == "51"
    assert rows[0]["repetitions"] == "101"
    assert rows[0]["results_match"] == "True"


def test_save_results_rejects_empty_results(tmp_path):
    output_path = tmp_path / "benchmark.csv"

    with pytest.raises(ValueError, match="results must not be empty"):
        save_results([], output_path)
