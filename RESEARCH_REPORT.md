\# Research Report: Privacy-Preserving Collaborative Fraud Analytics



\## Abstract



Financial institutions may benefit from combining fraud-related statistics, but sharing institution-level data can create confidentiality and governance risks. This project implements an educational prototype that explores additive secret sharing as a method for aggregating integer contributions without directly revealing each contribution to a single share holder under the scheme's assumptions.



The prototype includes synthetic transaction data, exploratory analysis, a baseline classification experiment, collaborative fraud-count aggregation, and a local performance benchmark. Automated tests assess input validation, share reconstruction, and aggregation behavior. The current implementation demonstrates the arithmetic of additive secret sharing in a single Python process. It does not constitute a distributed secure multi-party computation deployment or establish production-level security.



\## 1. Research Motivation



Fraud patterns can cross institutional boundaries, while privacy, confidentiality, and governance requirements may limit direct data sharing. Privacy-enhancing technologies offer possible ways to analyze selected statistics collaboratively while limiting exposure of individual contributions.



This project investigates the following question:



\*\*Can simulated financial institutions combine fraud-related counts using additive secret sharing without directly exposing their individual counts to an aggregation server, and what computational overhead does this introduce in a local prototype?\*\*



The work is exploratory. It provides an implementation and testing foundation for future research into secure aggregation and privacy-preserving collaborative analytics.



\## 2. Objectives



The project has five main objectives:



1\. Implement additive secret sharing and modular reconstruction for integer values.

2\. Simulate contributions from multiple institutions and compare the reconstructed result with ordinary aggregation.

3\. Explore synthetic transaction data and a baseline fraud-classification task.

4\. Measure local execution time for ordinary addition and secret-share aggregation across several workload sizes.

5\. Document the security assumptions, limitations, and possible extensions of the prototype.



\## 3. Methodology



\### 3.1 Additive secret sharing



The implementation uses a default modulus of \\(p = 2^{127}-1\\). For a secret \\(s\\), it generates a random share \\(a\\) and calculates the second share as



\\\[

b = (s-a) \\bmod p.

\\]



The shares reconstruct the original secret through



\\\[

s = (a+b) \\bmod p.

\\]



For several institutions, each share holder sums its corresponding shares modulo the selected modulus. The resulting aggregate shares can then be combined to recover the total modulo that modulus.



Exact reconstruction of the ordinary integer sum requires the aggregate to be smaller than the modulus. Otherwise, the result wraps around modulo the selected value.



\### 3.2 Synthetic transaction data



Two synthetic institution datasets are used for exploratory analysis and baseline classification. The data are artificial, and the fraud labels are deliberately correlated with selected features.



These data support demonstration and testing only. They are not a representative sample of real financial transactions, and their fraud rate and classification performance should not be interpreted as estimates of real-world banking performance.



\### 3.3 Baseline classification



A majority-class dummy classifier is compared with a decision tree classifier. The purpose is to demonstrate a basic modelling workflow and establish a baseline for future experiments.



The synthetic labels were deliberately constructed to correlate with selected transaction features. Perfect or very high classification metrics in this setting are therefore expected to overstate what could be achieved on realistic, independently collected data. No claim of operational fraud-detection effectiveness is made.



\### 3.4 Performance benchmark



The benchmark compares ordinary addition with the local secret-share aggregation workflow for simulated workloads of 2, 10, 50, and 100 institutions. It uses 101 timing repetitions per method and workload, reporting the median, first quartile (Q1), third quartile (Q3), and the ratio of secret-share aggregation time to ordinary addition time.



The benchmark records are saved to `results/aggregation\_benchmark.csv`. The recorded results are machine-dependent microbenchmark observations. The measured workflow includes share-generation and modular-arithmetic costs that ordinary addition does not incur.



The benchmark does not measure network communication, serialization, independent aggregation servers, concurrent execution, or adversarial behavior. It therefore cannot establish the performance of a deployed distributed multi-party computation system.



\## 4. Results



\### 4.1 Functional correctness



The collaborative aggregation experiment compares the sum obtained through ordinary addition with the total reconstructed through additive secret sharing. In the tested demonstration, both approaches return the same total.



The current automated test suite contains 46 passing tests. The tests cover core secret-sharing behavior, reconstruction, aggregation, input validation, synthetic-data functions, baseline modelling, collaborative analysis, and benchmarking.



\### 4.2 Benchmark observations



The recorded benchmark results are:



| Simulated institutions | Ordinary addition median (ms) | Secret-share aggregation median (ms) | Observed ratio |

|---:|---:|---:|---:|

| 2 | 0.000066 | 0.004196 | 63.3× |

| 10 | 0.000135 | 0.014248 | 105.2× |

| 50 | 0.000255 | 0.062978 | 247.3× |

| 100 | 0.000383 | 0.126567 | 330.7× |



Both methods produced matching totals in the recorded runs.



Secret-share aggregation took longer than ordinary addition in these local measurements. The ratio increased with workload size in the tested configurations. However, ordinary addition takes extremely little time, so a large ratio does not by itself establish that the absolute overhead is substantial in a practical distributed deployment.



These measurements are observations from the recorded local benchmark, not universal performance estimates. They should be reproduced on the target environment before being used in comparative research claims.



\## 5. Security Analysis and Threat Model



The intended scheme considers an honest-but-curious share holder that follows the prescribed computation but may try to infer information from its share.



Under the mathematical assumptions of additive secret sharing, a uniformly random share alone does not reveal the corresponding secret when the other share remains unavailable. This property depends on correct share generation and on the separation and confidentiality of the shares.



The current prototype creates, stores, and aggregates both sets of shares within one Python process. Consequently, it does not enforce separation between independently administered aggregation servers. It does not demonstrate security against collusion or compromise in a distributed deployment.



The implementation also does not provide authenticated communication, protection against malicious participants, differential privacy, network security, or protection against side-channel attacks. Input validation is useful for rejecting malformed values but does not replace protocol-level security controls.



The detailed assumptions and limitations are documented in `THREAT\_MODEL.md`.



\## 6. Limitations



The main limitations are:



\- The datasets and fraud labels are synthetic.

\- The classification experiment is not evidence of real-world fraud-detection performance.

\- The aggregation workflow is a single-process simulation rather than a distributed protocol.

\- The benchmark excludes communication, serialization, server separation, and deployment overhead.

\- The implementation does not establish malicious-security guarantees or differential privacy.

\- The recorded timing results are machine-dependent and based on the tested workloads.

\- No independent cryptographic review or production security assessment has been conducted.



These limitations restrict the conclusions that can be drawn from the prototype.



\## 7. Future Work



Possible extensions include:



1\. Implementing separate aggregation processes and explicit share-distribution boundaries.

2\. Measuring communication and serialization overhead in a controlled multi-process experiment.

3\. Evaluating stronger threat models and protocols designed to handle malicious participants.

4\. Investigating privacy-preserving machine learning and secure aggregation of model updates.

5\. Comparing alternative privacy-enhancing technologies and their computational and communication trade-offs.

6\. Using more realistic, ethically sourced datasets or carefully designed simulations with transparent assumptions.

7\. Improving the statistical methodology through repeated runs, confidence intervals, and documented hardware and software configurations.



\## 8. Conclusion



This project provides a tested educational prototype for additive secret sharing and collaborative fraud-count aggregation. It combines implementation, synthetic-data analysis, baseline classification, benchmarking, and explicit threat-model documentation.



The results show that the prototype can reconstruct tested aggregate counts correctly and that its secret-share workflow incurs additional local computation compared with ordinary addition. They do not demonstrate the security or performance of a production distributed system.



The main contribution is a reproducible starting point for further investigation into privacy-enhancing technologies and collaborative financial analytics. Future work should focus on genuine share separation, stronger protocol-level security, and more comprehensive experimental evaluation.



\## Reproducibility



The project is implemented in Python and uses pytest for automated tests, with pandas and scikit-learn for synthetic-data analysis and baseline classification.



From the project root, the main experiments can be run with:



```powershell

python -m src.generate\_data

python -m src.analyze\_data

python -m src.baseline\_model

python -m src.collaborative\_analysis

python -m src.benchmark\_aggregation

python -m pytest -q

```



The results should be interpreted alongside the project's README and threat model. Benchmark results can vary by environment, and all reported test counts should be confirmed by rerunning the test suite after changes.



