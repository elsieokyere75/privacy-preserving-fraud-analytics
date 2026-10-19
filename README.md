\# Privacy-Preserving Collaborative Fraud Analytics



A Python research prototype exploring secure aggregation and privacy-preserving collaborative fraud detection using synthetic financial data.



\## Research motivation



Financial institutions may benefit from collaborating on fraud analysis, but sharing raw transaction data can create privacy, confidentiality and governance risks.



This project investigates a narrower question first:



\*\*Can multiple simulated institutions contribute fraud-related statistics to a shared analysis without directly revealing their individual counts to a single aggregation server?\*\*



The initial implementation uses additive secret sharing over integers modulo a large prime. Future work will explore collaborative machine-learning experiments and evaluate the trade-offs between privacy assumptions, predictive performance and computational cost.



\## Current features



\- Additive secret sharing of integer values.

\- Reconstruction of a value from two shares.

\- Aggregation of contributions from multiple simulated institutions.

\- Input validation and automated tests.

\- A documented threat model and explicit security limitations.



\## Architecture



1\. Each simulated institution splits its contribution into two shares.

2\. Each aggregation server receives one share from every institution.

3\. Each server adds its shares modulo the chosen prime.

4\. The two aggregate shares are combined to recover the total modulo the prime.



The design aims to prevent either aggregation server, acting alone, from learning an institution's individual count from its share, under the documented assumptions.



\## Technology



\- Python

\- `secrets` for cryptographically secure random share generation

\- `pytest` for automated testing

\- Git and GitHub for version control



\## Requirements



\- Python 3.11 or later

\- `pytest`



The initial prototype uses Python's standard library for its implementation. The automated tests require `pytest`.



\## Setup on Windows PowerShell



Clone the repository or open the existing project directory, then create a virtual environment:



```powershell

py -m venv .venv

```



Activate it in PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



If PowerShell blocks activation, follow your organisation's device policies. On a personal computer, a temporary process-scoped execution-policy change may be used if permitted, or the environment's Python executable can be invoked directly.



Install the testing dependency:



```powershell

python -m pip install pytest

```



\## Run the demonstration



From the project root:



```powershell

python -m src.secure\_aggregation

```



The demonstration uses synthetic contributions of 17 and 23 and should reconstruct a combined total of 40.



\## Run the automated tests



```powershell

python -m pytest -v

```



The tests check reconstruction, aggregation, boundary conditions and input validation.



\## Security scope and limitations



This is an educational research prototype, not a production-ready multi-party computation system.



The current implementation runs in one process and simulates share distribution in memory. It does not provide authenticated communication, malicious-party protection, differential privacy, deployment security or resistance to collusion between both aggregation servers.



See \[THREAT\_MODEL.md](THREAT\_MODEL.md) for the threat assumptions, intended protections and limitations.



\## Planned research work



\- Generate reproducible synthetic transaction datasets for two simulated financial institutions.

\- Compare ordinary aggregation with secure aggregation.

\- Explore collaborative fraud-model training using synthetic data.

\- Evaluate predictive performance, runtime and computational overhead.

\- Document experimental methods, results, limitations and reproducibility.



\## Research integrity



All initial demonstrations use synthetic values. The prototype should not be used with real customer records or confidential banking data.



Security and performance claims will be updated only after they have been implemented and tested.



\## Status



\*\*Stage 1:\*\* Additive secret-sharing prototype and initial automated tests.



Further research and evaluation are planned.



