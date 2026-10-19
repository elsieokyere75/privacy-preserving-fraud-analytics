
"""Baseline fraud detection model for synthetic transactions.

Results are educational and do not demonstrate real-world fraud detection
performance.
"""

import csv
from pathlib import Path

from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"


def load_combined_transactions() -> tuple[list[list[float]], list[int]]:
    """Load and combine the synthetic records from both institutions."""
    features = []
    labels = []

    filenames = ("institution_a.csv", "institution_b.csv")

    for filename in filenames:
        csv_path = DATA_DIRECTORY / filename

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {csv_path}. "
                "Run python .\\src\\generate_data.py first."
            )

        with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
            for row in csv.DictReader(csv_file):
                features.append(
                    [
                        float(row["amount"]),
                        float(row["hour"]),
                        float(row["transactions_last_24h"]),
                    ]
                )
                labels.append(int(row["is_fraud"]))

    if not features:
        raise ValueError("No transaction records found.")

    return features, labels


def report_model(name, model, features_test, labels_test) -> None:
    """Print classification metrics and the confusion matrix."""
    predictions = model.predict(features_test)

    print(f"\n{name}")
    print("-" * len(name))
    print(f"Accuracy:  {accuracy_score(labels_test, predictions):.3f}")
    print(
        f"Precision: {precision_score(labels_test, predictions, zero_division=0):.3f}"
    )
    print(
        f"Recall:    {recall_score(labels_test, predictions, zero_division=0):.3f}"
    )
    print(f"F1-score:  {f1_score(labels_test, predictions, zero_division=0):.3f}")
    print("Confusion matrix:")
    print("Rows = actual [normal, fraud], columns = predicted [normal, fraud]")
    print(confusion_matrix(labels_test, predictions, labels=[0, 1]))


def main() -> None:
    """Train and compare a simple baseline and a decision tree."""
    features, labels = load_combined_transactions()

    total = len(labels)
    fraud_count = sum(labels)
    normal_count = total - fraud_count

    print("SYNTHETIC FRAUD DETECTION: BASELINE EXPERIMENT")
    print("=" * 48)
    print(f"Total transactions: {total}")
    print(f"Normal transactions: {normal_count}")
    print(f"Fraud-labelled transactions: {fraud_count}")
    print(f"Fraud-label rate: {fraud_count / total * 100:.2f}%")
    print("Features: amount, hour, transactions_last_24h")

    (
        features_train,
        features_test,
        labels_train,
        labels_test,
    ) = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    majority_baseline = DummyClassifier(strategy="most_frequent")
    majority_baseline.fit(features_train, labels_train)
    report_model(
        "Majority-class baseline",
        majority_baseline,
        features_test,
        labels_test,
    )

    decision_tree = DecisionTreeClassifier(
        max_depth=4,
        random_state=42,
    )
    decision_tree.fit(features_train, labels_train)
    report_model(
        "Decision tree",
        decision_tree,
        features_test,
        labels_test,
    )

    print("\nIMPORTANT LIMITATION")
    print(
        "These are artificial records. The data generator deliberately "
        "correlates fraud labels with some features, so performance may "
        "be unrealistically high. These results are not evidence of "
        "real-world fraud detection capability."
    )


if __name__ == "__main__":
    main()
