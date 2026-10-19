
"""Summarize synthetic transaction data for two institutions.

This script reports descriptive statistics only. It does not train a model.
"""

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"


def load_transactions(csv_path: Path) -> list[dict]:
    """Load transaction records from a CSV file."""
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def summarize_transactions(institution: str, transactions: list[dict]) -> None:
    """Print basic transaction and fraud-label statistics."""
    if not transactions:
        raise ValueError(f"No transactions found for {institution}")

    total = len(transactions)
    fraud_transactions = [
        transaction
        for transaction in transactions
        if int(transaction["is_fraud"]) == 1
    ]
    normal_transactions = [
        transaction
        for transaction in transactions
        if int(transaction["is_fraud"]) == 0
    ]

    fraud_rate = len(fraud_transactions) / total * 100

    print(f"\n{'=' * 45}")
    print(f"Institution: {institution}")
    print(f"{'=' * 45}")
    print(f"Total transactions: {total}")
    print(f"Fraud-labelled transactions: {len(fraud_transactions)}")
    print(f"Normal transactions: {len(normal_transactions)}")
    print(f"Fraud-label rate: {fraud_rate:.2f}%")

    for label, group in (
        ("Fraud-labelled", fraud_transactions),
        ("Normal", normal_transactions),
    ):
        if group:
            average_amount = sum(
                float(transaction["amount"]) for transaction in group
            ) / len(group)

            print(
                f"Average {label.lower()} transaction amount: "
                f"{average_amount:.2f}"
            )

    print("\nFraud-labelled transactions by hour:")
    fraud_by_hour = {}

    for transaction in fraud_transactions:
        hour = int(transaction["hour"])
        fraud_by_hour[hour] = fraud_by_hour.get(hour, 0) + 1

    if fraud_by_hour:
        for hour, count in sorted(fraud_by_hour.items()):
            print(f"  {hour:02d}:00 -> {count}")
    else:
        print("  No fraud-labelled transactions")


def main() -> None:
    """Analyze both synthetic datasets."""
    for filename, institution in (
        ("institution_a.csv", "BANK_A"),
        ("institution_b.csv", "BANK_B"),
    ):
        csv_path = DATA_DIRECTORY / filename

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {csv_path}. "
                "Run src/generate_data.py first."
            )

        transactions = load_transactions(csv_path)
        summarize_transactions(institution, transactions)


if __name__ == "__main__":
    main()
