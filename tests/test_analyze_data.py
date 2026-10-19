
import pytest

from src.analyze_data import summarize_transactions


def test_summary_reports_transaction_counts(capsys):
    transactions = [
        {
            "transaction_id": "A-001",
            "amount": "100.00",
            "hour": "12",
            "transactions_last_24h": "2",
            "is_fraud": "0",
        },
        {
            "transaction_id": "A-002",
            "amount": "900.00",
            "hour": "2",
            "transactions_last_24h": "8",
            "is_fraud": "1",
        },
    ]

    summarize_transactions("BANK_A", transactions)
    output = capsys.readouterr().out

    assert "Total transactions: 2" in output
    assert "Fraud-labelled transactions: 1" in output
    assert "Normal transactions: 1" in output
    assert "Fraud-label rate: 50.00%" in output


def test_summary_handles_no_fraud_labels(capsys):
    transactions = [
        {
            "transaction_id": "A-001",
            "amount": "100.00",
            "hour": "12",
            "transactions_last_24h": "2",
            "is_fraud": "0",
        }
    ]

    summarize_transactions("BANK_A", transactions)
    output = capsys.readouterr().out

    assert "Fraud-labelled transactions: 0" in output
    assert "No fraud-labelled transactions" in output


def test_summary_rejects_empty_dataset():
    with pytest.raises(ValueError, match="No transactions found"):
        summarize_transactions("BANK_A", [])
