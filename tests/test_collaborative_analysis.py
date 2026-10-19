
import csv

import pytest

from src.collaborative_analysis import count_fraud_transactions


def test_count_fraud_transactions_counts_labels_correctly(tmp_path):
    csv_path = tmp_path / "transactions.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["transaction_id", "is_fraud"])
        writer.writeheader()
        writer.writerows(
            [
                {"transaction_id": "A-001", "is_fraud": "0"},
                {"transaction_id": "A-002", "is_fraud": "1"},
                {"transaction_id": "A-003", "is_fraud": "1"},
                {"transaction_id": "A-004", "is_fraud": "0"},
            ]
        )

    assert count_fraud_transactions(csv_path) == 2


def test_count_fraud_transactions_returns_zero_when_no_fraud(tmp_path):
    csv_path = tmp_path / "normal.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["is_fraud"])
        writer.writeheader()
        writer.writerows([{"is_fraud": "0"}, {"is_fraud": "0"}])

    assert count_fraud_transactions(csv_path) == 0


def test_missing_dataset_raises_error(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="Dataset not found"):
        count_fraud_transactions(missing_path)


def test_missing_fraud_column_raises_error(tmp_path):
    csv_path = tmp_path / "invalid.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["transaction_id"])
        writer.writeheader()
        writer.writerow({"transaction_id": "A-001"})

    with pytest.raises(ValueError, match="Missing 'is_fraud' column"):
        count_fraud_transactions(csv_path)


def test_invalid_fraud_label_raises_error(tmp_path):
    csv_path = tmp_path / "invalid_label.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["is_fraud"])
        writer.writeheader()
        writer.writerow({"is_fraud": "unknown"})

    with pytest.raises(ValueError, match="Invalid fraud label"):
        count_fraud_transactions(csv_path)


def test_non_binary_fraud_label_raises_error(tmp_path):
    csv_path = tmp_path / "invalid_binary.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["is_fraud"])
        writer.writeheader()
        writer.writerow({"is_fraud": "2"})

    with pytest.raises(ValueError, match="Fraud labels must be 0 or 1"):
        count_fraud_transactions(csv_path)
