# Privacy-Preserving Collaborative Fraud Analytics

A Python research prototype exploring additive secret sharing, collaborative fraud analysis, and computational overhead using synthetic financial data.

## Research Motivation

Financial institutions may benefit from collaborating on fraud analysis, but sharing raw transaction data can create privacy, confidentiality, and governance risks.

This project investigates the following question:

**Can multiple simulated financial institutions contribute fraud-related statistics to a shared analysis without directly exposing their individual counts to an aggregation server?**

The initial implementation uses additive secret sharing over integers modulo a large prime. The project also explores synthetic fraud data, baseline classification, collaborative fraud-count aggregation, and preliminary performance measurements.

## Research Objectives

- Implement and test additive secret sharing for integer values.
- Simulate collaborative fraud analysis across multiple institutions.
- Establish a baseline fraud-classification experiment using synthetic data.
- Compare ordinary addition with local secret-share aggregation.
- Document security assumptions, experimental methodology, and limitations.
- Establish a foundation for future work in privacy-preserving machine learning and secure multi-party computation.

## Current Features

- Additive secret sharing and reconstruction of integer values.
- Aggregation of contributions from multiple simulated institutions.
- Input validation and automated tests.
- Reproducible synthetic transaction datasets.
- Exploratory data analysis of synthetic fraud labels.
- Baseline comparison using a dummy classifier and a decision tree.
- Collaborative fraud-count aggregation.
- Performance benchmarking with median, first-quartile (Q1), and third-quartile (Q3) timing statistics.
- CSV export of benchmark results.
- A documented threat model and explicit security limitations.

## Project Structure

```text
src/
    secure_aggregation.py
    generate_data.py
    analyze_data.py
    baseline_model.py
    collaborative_analysis.py
    benchmark_aggregation.py

tests/
    test_secure_aggregation.py
    test_generate_data.py
    test_analyze_data.py
    test_baseline_model.py
    test_collaborative_analysis.py
    test_benchmark_aggregation.py

data/
    institution_a.csv
    institution_b.csv

results/
    aggregation_benchmark.csv

README.md
THREAT_MODEL.md
```

The synthetic CSV files are generated locally and may be excluded from version control.

## Technology

- Python
- Python `secrets` module for secure random share generation
- pandas and scikit-learn for synthetic-data analysis and baseline classification
- pytest for automated testing
- Git and GitHub for version control

## Setup on Windows PowerShell

Create a virtual environment from the project root:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install pytest pandas scikit-learn
```

If your environment uses a dependency file, install from that file instead.

## Run the Demonstration

```powershell
python -m src.secure_aggregation
```

The demonstration uses synthetic contributions of 17 and 23 and should reconstruct a combined total of 40.

## Generate and Analyze Synthetic Data

Generate the datasets:

```powershell
python -m src.generate_data
```

Analyze the generated data:

```powershell
python -m src.analyze_data
```

The datasets represent two simulated institutions. Their records and fraud labels are artificial and are intended for experimentation, not for estimating real banking fraud rates.

## Run the Baseline Classifier

```powershell
python -m src.baseline_model
```

The experiment compares a majority-class dummy classifier with a decision tree.

**Important limitation:** the synthetic fraud labels are deliberately correlated with selected transaction features. Very high classification performance, including perfect results in this experiment, is therefore not evidence that the model would perform similarly on real financial transactions.

## Run Collaborative Fraud Analysis

```powershell
python -m src.collaborative_analysis
```

This experiment compares the combined fraud-label count with the result obtained through additive secret-share aggregation.

Both methods should return the same total.

## Benchmark Aggregation Performance

Run the benchmark:

```powershell
python -m src.benchmark_aggregation
```

The current benchmark evaluates simulated workloads of 2, 10, 50, and 100 institutions, using 101 timing repetitions per method and workload.

It reports:

- Median execution time.
- First quartile (Q1).
- Third quartile (Q3).
- The ratio of secret-share aggregation time to ordinary addition time.
- Whether both methods return the same total.

Results are saved to:

```text
results/aggregation_benchmark.csv
```

### Interpreting the Benchmark

The current local experiment shows that secret-share aggregation takes longer than ordinary addition. The additional work includes random share generation and modular arithmetic.

The overhead ratio increases with the number of simulated institutions in the tested workloads. However, ordinary addition is extremely fast, so ratios can appear large even when the absolute time difference is small.

These are preliminary, machine-dependent microbenchmark results. They do not measure network communication, independent aggregation servers, serialization, concurrent execution, or adversarial behaviour. They should not be interpreted as performance measurements of a deployed distributed MPC system.

## Run the Automated Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The latest verified run completed with **40 passing tests**. Re-run the tests after making changes to confirm the current project state.

## Architecture

1. Each simulated institution splits its contribution into two shares.
2. Each aggregation server conceptually receives one share from every institution.
3. Each server adds its shares modulo the chosen prime.
4. The two aggregate shares are combined to recover the total modulo the prime.

The current implementation performs these operations within a single Python process. It demonstrates the arithmetic of additive secret sharing but does not implement a networked two-server deployment.

## Security Scope and Limitations

This is an educational research prototype, not a production-ready multi-party computation system.

The current implementation does not provide:

- Networked or independently administered aggregation servers.
- Authenticated communication between institutions and servers.
- Protection against malicious participants or malicious server behaviour.
- Protection against collusion between both aggregation servers.
- Differential privacy or formal privacy guarantees for released statistics.
- Deployment hardening, key management, or operational monitoring.

The security properties of additive secret sharing depend on the threat model and on how shares are distributed, stored, processed, and released. See [THREAT_MODEL.md](THREAT_MODEL.md) for the project's stated assumptions and limitations.

## Planned Research Work

- Strengthen the experimental methodology and reporting.
- Evaluate additional workload sizes and measurement variability.
- Investigate privacy-preserving collaborative machine learning.
- Explore secure aggregation protocols and their threat assumptions.
- Study the trade-offs between privacy, predictive performance, and computational cost.
- Consider communication overhead and multi-process or distributed experiments.
- Investigate privacy-enhancing technologies relevant to financial fraud analytics.

## Research Integrity

All initial demonstrations use synthetic values and artificial datasets. The prototype should not be used with real customer records or confidential banking data.

Performance measurements are preliminary and environment-dependent. Synthetic classification results are not evidence of real-world fraud-detection effectiveness.

Security and performance claims will be updated only when supported by implementation, testing, and documented experimental evidence.

## Status

**Current stage:** additive secret-sharing prototype, synthetic-data analysis, baseline classification, collaborative fraud-count aggregation, and preliminary local benchmarking.

Further research and evaluation are planned.
