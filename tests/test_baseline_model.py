
import csv

import pytest

from src.baseline_model import load_combined_transactions


def test_load_combined_transactions_returns_records_and_labels():
    features, labels = load_combined_transactions()

    assert len(features) == 1000
    assert len(labels) == 1000


def test_features_contain_three_numeric_values():
    features, _ = load_combined_transactions()

    assert len(features[0]) == 3
    assert all(isinstance(value, float) for value in features[0])


def test_labels_are_binary():
    _, labels = load_combined_transactions()

    assert set(labels).issubset({0, 1})


def test_combined_data_contains_normal_and_fraud_labels():
    _, labels = load_combined_transactions()

    assert 0 in labels
    assert 1 in labels


def test_missing_dataset_raises_error(tmp_path, monkeypatch):
    import src.baseline_model as baseline_model

    monkeypatch.setattr(baseline_model, "DATA_DIRECTORY", tmp_path)

    with pytest.raises(FileNotFoundError, match="Dataset not found"):
        load_combined_transactions()
