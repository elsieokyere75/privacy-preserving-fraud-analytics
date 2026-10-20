
"""Benchmark ordinary addition against additive secret-share aggregation.

This is a local Python microbenchmark, not a distributed MPC benchmark.
Timing results depend on the computer and runtime environment.
"""

import csv
import statistics
import time
from pathlib import Path

from src.secure_aggregation import aggregate_shares, split_secret


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIRECTORY = PROJECT_ROOT / "results"
RESULTS_FILE = RESULTS_DIRECTORY / "aggregation_benchmark.csv"


def ordinary_aggregate(counts: list[int]) -> int:
    """Combine institution counts using ordinary addition."""
    return sum(counts)


def secret_share_aggregate(counts: list[int]) -> int:
    """Split each count into two shares and aggregate the shares."""
    first_shares = []
    second_shares = []

    for count in counts:
        first_share, second_share = split_secret(count)
        first_shares.append(first_share)
        second_shares.append(second_share)

    return aggregate_shares(first_shares, second_shares)

def measure_batch_time_ms(
    function,
    counts: list[int],
    batch_size: int,
) -> float:
    """Measure average execution time per call across a batch."""
    if isinstance(batch_size, bool) or not isinstance(batch_size, int):
        raise TypeError("batch_size must be an integer")
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    start = time.perf_counter()

    for _ in range(batch_size):
        function(counts)

    elapsed = time.perf_counter() - start
    return (elapsed * 1000) / batch_size

def summarize_timings(timings_ms: list[float]) -> dict:
    """Summarize timing measurements using the median and quartiles."""
    if len(timings_ms) < 2:
        raise ValueError("at least 2 timing measurements are required")

    quartiles = statistics.quantiles(
        timings_ms, n=4, method="inclusive"
    )

    return {
        "median_ms": statistics.median(timings_ms),
        "q1_ms": quartiles[0],
        "q3_ms": quartiles[2],
    }


def measure_timing_statistics(
    function,
    counts: list[int],
    repetitions: int,
    batch_size: int = 1000,
) -> dict:
    """Return median and quartiles of average execution times in milliseconds."""
    if isinstance(repetitions, bool) or not isinstance(repetitions, int):
        raise TypeError("repetitions must be an integer")
    if repetitions < 2:
        raise ValueError("repetitions must be at least 2")
    if isinstance(batch_size, bool) or not isinstance(batch_size, int):
        raise TypeError("batch_size must be an integer")
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    timings_ms = []

    for _ in range(repetitions):
        elapsed_ms = measure_batch_time_ms(
            function, counts, batch_size
        )
        timings_ms.append(elapsed_ms)

    return summarize_timings(timings_ms)

def measure_median_time(
    function, counts: list[int], repetitions: int
) -> float:
    """Return the median execution time in milliseconds."""
    return measure_timing_statistics(
        function, counts, repetitions
    )["median_ms"]


def benchmark_workload(
    number_of_institutions: int,
    repetitions: int = 101,
) -> dict:
    """Benchmark both methods for a given number of institutions."""
    if (
        isinstance(number_of_institutions, bool)
        or not isinstance(number_of_institutions, int)
    ):
        raise TypeError("number_of_institutions must be an integer")
    if number_of_institutions < 1:
        raise ValueError("number_of_institutions must be at least 1")

    counts = [
        (institution_number * 17) % 100
        for institution_number in range(1, number_of_institutions + 1)
    ]

    ordinary_result = ordinary_aggregate(counts)
    secure_result = secret_share_aggregate(counts)
    results_match = ordinary_result == secure_result

    if not results_match:
        raise AssertionError("Ordinary and secret-share totals do not match.")

    ordinary_stats = measure_timing_statistics(
        ordinary_aggregate, counts, repetitions
    )
    secure_stats = measure_timing_statistics(
        secret_share_aggregate, counts, repetitions
    )

    ordinary_ms = ordinary_stats["median_ms"]
    secure_ms = secure_stats["median_ms"]

    return {
        "institutions": number_of_institutions,
        "total": ordinary_result,
        "ordinary_ms": ordinary_ms,
        "ordinary_q1_ms": ordinary_stats["q1_ms"],
        "ordinary_q3_ms": ordinary_stats["q3_ms"],
        "secret_share_ms": secure_ms,
        "secret_share_q1_ms": secure_stats["q1_ms"],
        "secret_share_q3_ms": secure_stats["q3_ms"],
        "overhead_ratio": (
            secure_ms / ordinary_ms if ordinary_ms > 0 else float("inf")
        ),
        "repetitions": repetitions,
        "results_match": results_match,
    }


def save_results(results: list[dict], output_path: Path = RESULTS_FILE) -> None:
    """Save benchmark measurements to a CSV file."""
    if not results:
        raise ValueError("results must not be empty")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "institutions",
        "total",
        "ordinary_ms",
        "ordinary_q1_ms",
        "ordinary_q3_ms",
        "secret_share_ms",
        "secret_share_q1_ms",
        "secret_share_q3_ms",
        "overhead_ratio",
        "repetitions",
        "results_match",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    """Run the benchmark and save the results."""
    institution_sizes = [2, 10, 50, 100]
    repetitions = 101

    print("AGGREGATION PERFORMANCE MICROBENCHMARK")
    print("=" * 110)
    print(f"Trials per method and workload: {repetitions}")
    print("Reported times: median, Q1, and Q3 in milliseconds\n")

    results = []

    for size in institution_sizes:
        result = benchmark_workload(size, repetitions)
        results.append(result)

        print(
            f"Institutions: {result['institutions']:>3} | "
            f"Total: {result['total']:>5} | "
            f"Ordinary median: {result['ordinary_ms']:.6f} ms | "
            f"Q1: {result['ordinary_q1_ms']:.6f} ms | "
            f"Q3: {result['ordinary_q3_ms']:.6f} ms"
        )
        print(
            f"                 Secret-share median: "
            f"{result['secret_share_ms']:.6f} ms | "
            f"Q1: {result['secret_share_q1_ms']:.6f} ms | "
            f"Q3: {result['secret_share_q3_ms']:.6f} ms | "
            f"Ratio: {result['overhead_ratio']:.1f}x | "
            f"Match: {result['results_match']}"
        )

    save_results(results)

    print(f"\nCSV results saved to: {RESULTS_FILE}")
    print("\nLIMITATIONS")
    print(
        "This local benchmark excludes network communication, independent "
        "servers, serialization, and adversarial behaviour."
    )
    print(
        "Ordinary addition is extremely cheap, so timing ratios can be large "
        "even when absolute execution times are small."
    )
    print(
        "Q1 and Q3 describe the spread of repeated timings. Results are "
        "machine-dependent preliminary measurements, not performance "
        "evidence for a deployed distributed MPC system."
    )


if __name__ == "__main__":
    main()
