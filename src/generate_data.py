
"""Generate synthetic transaction data for two simulated institutions.

All records are artificial and intended for research and testing only.
"""

import csv
import random
from pathlib import Path


def generate_transactions(
    institution: str,
    number_of_transactions: int = 500,
    seed: int = 42,
) -> list[dict]:
    """Generate reproducible synthetic transaction records."""
    rng = random.Random(seed)
    transactions = []

    for number in range(1, number_of_transactions + 1):
        is_fraud = int(rng.random() < 0.08)

        if is_fraud:
            amount = round(rng.uniform(500, 5000), 2)
            hour = rng.choice([0, 1, 2, 3, 4, 23])
            recent_transactions = rng.randint(6, 15)
        else:
            amount = round(rng.uniform(5, 1000), 2)
            hour = rng.randint(5, 22)
            recent_transactions = rng.randint(1, 5)

        transactions.append(
            {
                "transaction_id": f"{institution}-{number:05d}",
                "amount": amount,
                "hour": hour,
                "transactions_last_24h": recent_transactions,
                "is_fraud": is_fraud,
            }
        )

    return transactions


def save_transactions(
    transactions: list[dict],
    output_path: Path,
) -> None:
    """Save transactions as a CSV file."""
    if not transactions:
        raise ValueError("transactions must not be empty")

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=list(transactions[0].keys()),
        )
        writer.writeheader()
        writer.writerows(transactions)


def main() -> None:
    """Generate and save datasets for both institutions."""
    project_root = Path(__file__).resolve().parent.parent
    data_directory = project_root / "data"
    data_directory.mkdir(exist_ok=True)

    institution_a = generate_transactions("BANK_A", seed=42)
    institution_b = generate_transactions("BANK_B", seed=43)

    save_transactions(
        institution_a,
        data_directory / "institution_a.csv",
    )
    save_transactions(
        institution_b,
        data_directory / "institution_b.csv",
    )

    print(f"Institution A: {len(institution_a)} transactions")
    print(f"Institution B: {len(institution_b)} transactions")
    print(f"Datasets saved to: {data_directory}")


if __name__ == "__main__":
    main()
