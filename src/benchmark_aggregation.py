
"""Benchmark ordinary addition against additive secret-share aggregation.

This is a local Python microbenchmark, not a distributed MPC benchmark.
Timing results depend on the computer and runtime environment.
"""

import statistics
import time

from src.secure_aggregation import aggregate_shares, split_secret


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


def measure_median_time(function, counts: list[int], repetitions: int) -> float:
    """Return the median execution time in milliseconds."""
    if isinstance(repetitions, bool) or not isinstance(repetitions, int):
        raise TypeError("repetitions must be an integer")
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1")

    timings_ms = []

    for _ in range(repetitions):
        start = time.perf_counter()
        function(counts)
        elapsed = time.perf_counter() - start
        timings_ms.append(elapsed * 1000)

    return statistics.median(timings_ms)


def benchmark_workload(
    number_of_institutions: int,
    repetitions: int = 101,
) -> dict:
    """Benchmark both methods for a given number of institutions."""
    # Deterministic synthetic counts, not real institutional data.
    counts = [
        (institution_number * 17) % 100
        for institution_number in range(1, number_of_institutions + 1)
    ]

    ordinary_result = ordinary_aggregate(counts)
    secure_result = secret_share_aggregate(counts)

    if ordinary_result != secure_result:
        raise AssertionError("Ordinary and secret-share totals do not match.")

    ordinary_ms = measure_median_time(
        ordinary_aggregate,
        counts,
        repetitions,
    )
    secure_ms = measure_median_time(
        secret_share_aggregate,
        counts,
        repetitions,
    )

    return {
        "institutions": number_of_institutions,
        "total": ordinary_result,
        "ordinary_ms": ordinary_ms,
        "secret_share_ms": secure_ms,
        "overhead_ratio": (
            secure_ms / ordinary_ms if ordinary_ms > 0 else float("inf")
        ),
    }


def main() -> None:
    """Run the microbenchmark for increasing institution counts."""
    institution_sizes = [2, 10, 50, 100]
    repetitions = 101

    print("AGGREGATION PERFORMANCE MICROBENCHMARK")
    print("=" * 76)
    print(f"Trials per method and workload: {repetitions}")
    print("Reported time: median milliseconds per call")
    print("")

    print(
        f"{'Institutions':>12} | {'Total':>8} | {'Ordinary (ms)':>14} | "
        f"{'Secret-share (ms)':>17} | {'Time ratio':>11}"
    )
    print("-" * 76)

    for size in institution_sizes:
        result = benchmark_workload(size, repetitions)

        print(
            f"{result['institutions']:>12} | "
            f"{result['total']:>8} | "
            f"{result['ordinary_ms']:>14.6f} | "
            f"{result['secret_share_ms']:>17.6f} | "
            f"{result['overhead_ratio']:>10.1f}x"
        )

    print("\nINTERPRETATION")
    print(
        "The time ratio compares this local secret-sharing implementation "
        "with ordinary addition. Ordinary addition is extremely cheap, so "
        "the ratio can be large even when absolute times are small."
    )
    print(
        "This benchmark excludes network communication, independent servers, "
        "serialization, and adversarial behaviour. It does not measure the "
        "performance of a deployed distributed MPC system."
    )


if __name__ == "__main__":
    main()
