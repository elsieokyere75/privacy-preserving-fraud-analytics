
"""Compare ordinary fraud-count aggregation with secret-share aggregation.

This is a single-process educational simulation, not a distributed MPC system.
The transaction records are synthetic.
"""

import csv
from pathlib import Path

from src.secure_aggregation import aggregate_shares, split_secret


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"


def count_fraud_transactions(csv_path: Path) -> int:
    """Count fraud-labelled transactions for one simulated institution."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}. "
            "Run python .\\src\\generate_data.py first."
        )

    fraud_count = 0

    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        if "is_fraud" not in (reader.fieldnames or []):
            raise ValueError(f"Missing 'is_fraud' column in {csv_path.name}")

        for row in reader:
            try:
                label = int(row["is_fraud"])
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid fraud label in {csv_path.name}"
                ) from error

            if label not in (0, 1):
                raise ValueError(
                    f"Fraud labels must be 0 or 1 in {csv_path.name}"
                )

            fraud_count += label

    return fraud_count


def main() -> None:
    """Compare conventional aggregation with secret-share aggregation."""
    bank_a_path = DATA_DIRECTORY / "institution_a.csv"
    bank_b_path = DATA_DIRECTORY / "institution_b.csv"

    bank_a_fraud = count_fraud_transactions(bank_a_path)
    bank_b_fraud = count_fraud_transactions(bank_b_path)

    # Conventional approach: the individual counts are added directly.
    ordinary_total = bank_a_fraud + bank_b_fraud

    # Privacy-preserving simulation: split each count into two shares.
    a_share_1, a_share_2 = split_secret(bank_a_fraud)
    b_share_1, b_share_2 = split_secret(bank_b_fraud)

    # Each simulated server aggregates only the shares it holds.
    secure_total = aggregate_shares(
        [a_share_1, b_share_1],
        [a_share_2, b_share_2],
    )

    print("COLLABORATIVE FRAUD-COUNT EXPERIMENT")
    print("=" * 42)
    print("Input: synthetic transaction records")
    print(f"Bank A fraud count: {bank_a_fraud}")
    print(f"Bank B fraud count: {bank_b_fraud}")
    print(f"Ordinary combined count: {ordinary_total}")
    print(f"Secret-share combined count: {secure_total}")
    print(f"Results match: {ordinary_total == secure_total}")

    if ordinary_total != secure_total:
        raise RuntimeError("The two aggregation methods produced different results.")

    print("\nLIMITATION")
    print(
        "This experiment simulates secret sharing in one process. "
        "It does not establish security between independently operated "
        "institutions or servers."
    )


if __name__ == "__main__":
    main()
