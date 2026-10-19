\# Threat Model: Privacy-Preserving Fraud Analytics



\## 1. Project purpose



This project explores whether simulated financial institutions can contribute fraud-related statistics to a shared analysis without directly disclosing their individual counts.



The initial prototype implements additive secret sharing over integers modulo a large prime. It is an educational research prototype, not a production-ready multi-party computation system.



\## 2. System participants



\- \*\*Institution A:\*\* Holds its own fraud-related count.

\- \*\*Institution B:\*\* Holds its own fraud-related count.

\- \*\*Aggregation Server 1:\*\* Receives the first share from each institution and adds the shares modulo the chosen prime.

\- \*\*Aggregation Server 2:\*\* Receives the second share from each institution and adds the shares modulo the same prime.

\- \*\*Analyst:\*\* Receives the reconstructed aggregate total.



\## 3. Assets to protect



\- Each institution's individual fraud-related count.

\- The confidentiality of institution-specific contributions during aggregation.

\- The integrity and correctness of the reported aggregate.



The current prototype uses synthetic counts only. It does not process real customer or transaction records.



\## 4. Adversary and trust assumptions



The initial design considers an honest-but-curious aggregation server: a server that follows the prescribed computation but may attempt to learn information from the share it receives.



The confidentiality argument assumes that the two aggregation servers do not collude and that shares are generated using a cryptographically secure random-number generator.



For an individual server holding one share, a uniformly random additive share modulo the prime does not reveal the original count by itself, under the scheme's mathematical assumptions.



\## 5. Security properties intended



\- \*\*Confidentiality of individual counts:\*\* A single aggregation server's share does not reveal the individual count, assuming the other share remains secret and shares are generated correctly.

\- \*\*Correct reconstruction:\*\* Combining valid shares recovers the aggregate modulo the prime.

\- \*\*Basic input validation:\*\* The implementation rejects invalid types, out-of-range shares, invalid moduli and mismatched share lists.



\## 6. Limitations and out-of-scope threats



The current prototype does not provide:



\- Protection if both aggregation servers collude and combine their shares.

\- Authentication of institutions or aggregation servers.

\- Secure network communication or protection against interception.

\- Integrity guarantees against malicious participants or servers.

\- Availability guarantees or protection against denial of service.

\- Differential privacy or protection against inference from the released aggregate.

\- Protection against information leakage from future machine-learning gradients or model updates.

\- Production deployment controls, key management, audit logging or independent cryptographic review.



The current code runs in one Python process. It simulates share distribution in memory and does not implement two independently operated servers.



\## 7. Numerical assumptions



All values and shares must be integers in the range from zero to one less than the modulus.



Aggregation is performed modulo the chosen prime. To interpret the reconstructed result as an ordinary integer sum rather than a wrapped modular sum, the true aggregate must be smaller than the modulus.



\## 8. Planned research extensions



1\. Generate reproducible synthetic transaction datasets for two simulated institutions.

2\. Compare conventional aggregation with additive secret sharing.

3\. Explore collaborative fraud-model training using synthetic data.

4\. Measure model performance and computational overhead.

5\. Refine the threat model as the prototype gains functionality.



\## 9. Responsible research statement



The prototype is intended for learning and research into privacy-enhancing technologies. It must not be used to process confidential banking data or be represented as a secure production banking system without substantial additional engineering, security analysis and independent review.

