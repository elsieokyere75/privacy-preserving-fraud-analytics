
import csv

from src.generate_data import generate_transactions, save_transactions


def test_generates_requested_number_of_transactions():
    transactions = generate_transactions("BANK_A", number_of_transactions=25)
    assert len(transactions) == 25


def test_transaction_has_expected_fields():
    transactions = generate_transactions("BANK_A", number_of_transactions=1)
    assert set(transactions[0]) == {
        "transaction_id",
        "amount",
        "hour",
        "transactions_last_24h",
        "is_fraud",
    }


def test_transaction_values_are_valid():
    transactions = generate_transactions("BANK_A", number_of_transactions=100)

    for transaction in transactions:
        assert transaction["amount"] > 0
        assert 0 <= transaction["hour"] <= 23
        assert transaction["transactions_last_24h"] >= 1
        assert transaction["is_fraud"] in (0, 1)


def test_same_seed_produces_same_transactions():
    first = generate_transactions("BANK_A", number_of_transactions=20, seed=123)
    second = generate_transactions("BANK_A", number_of_transactions=20, seed=123)

    assert first == second


def test_different_seeds_produce_different_transactions():
    first = generate_transactions("BANK_A", number_of_transactions=20, seed=123)
    second = generate_transactions("BANK_A", number_of_transactions=20, seed=456)

    assert first != second


def test_save_transactions_creates_readable_csv(tmp_path):
    transactions = generate_transactions("BANK_A", number_of_transactions=3)
    output_file = tmp_path / "transactions.csv"

    save_transactions(transactions, output_file)

    with output_file.open(newline="", encoding="utf-8") as csv_file:
        saved_records = list(csv.DictReader(csv_file))

    assert len(saved_records) == 3
    assert saved_records[0]["transaction_id"] == "BANK_A-00001"
