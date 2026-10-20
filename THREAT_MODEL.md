# Threat Model: Privacy-Preserving Fraud Analytics

## 1. Project purpose

This project explores whether simulated financial institutions can contribute fraud-related statistics to a shared analysis without directly disclosing their individual counts.

The initial prototype implements additive secret sharing over integers modulo a large prime. It is an educational research prototype, not a production-ready multi-party computation system.

## 2. System participants

- **Institution A:** Holds its own fraud-related count.

- **Institution B:** Holds its own fraud-related count.

- **Aggregation Server 1:** Receives the first share from each institution and adds the shares modulo the chosen prime.

- **Aggregation Server 2:** Receives the second share from each institution and adds the shares modulo the same prime.

- **Analyst:** Receives the reconstructed aggregate total.

## 3. Assets to protect

- Each institution's individual fraud-related count.

- The confidentiality of institution-specific contributions during aggregation.

- The integrity and correctness of the reported aggregate.

The current prototype uses synthetic counts only. It does not process real customer or transaction records.

## 4. Adversary and trust assumptions

The intended design considers an honest-but-curious aggregation server. Such a server follows the prescribed computation but may attempt to infer information from the share it receives.

The additive secret-sharing scheme assumes that each secret is split using a uniformly random share modulo the selected modulus, and that an individual server cannot access the other share. Under these assumptions, one share alone does not reveal the secret.

The default modulus is a large prime, `2^127 - 1`. The implementation validates that a modulus is greater than two, but it does not verify that a custom modulus is prime. The modular reconstruction identity holds for any modulus greater than two; the documented default is prime.

The current implementation creates, stores and aggregates both sets of shares within one Python process. It therefore does not enforce separation between aggregation servers, and it does not demonstrate security against collusion or compromise in a real distributed deployment.

The prototype does not establish security against malicious participants, compromised software, or side-channel attacks. Those threats require additional protocol design, implementation controls and security analysis.

## 5. Security properties intended

- **Share-level confidentiality:** Under the additive secret-sharing assumptions, one uniformly random share alone does not reveal the corresponding secret. This property is mathematical and does not mean that the current single-process application provides distributed-system security.

- **Correct modular reconstruction:** Combining valid shares reconstructs the aggregate modulo the selected modulus. This equals the ordinary integer sum only when the true aggregate is smaller than the modulus.

- **Basic input validation:** The implementation rejects invalid types, out-of-range shares, invalid moduli, and mismatched share-list lengths. These checks help prevent malformed inputs but do not provide authentication or protection against malicious participants.

## 6. Limitations and out-of-scope threats

The current prototype does not provide:

- Protection if both aggregation servers collude and combine their shares.

- Authentication of institutions or aggregation servers.

- Secure network communication or protection against interception.

- Integrity guarantees against malicious participants or servers.

- Availability guarantees or protection against denial of service.

- Differential privacy or protection against inference from the released aggregate.

- Protection against information leakage from future machine-learning gradients or model updates.

- Production deployment controls, key management, audit logging or independent cryptographic review.

The current code runs in one Python process. It simulates share distribution in memory and does not implement two independently operated servers.

## 7. Numerical assumptions

All values and shares must be integers in the range from zero to one less than the modulus.

Aggregation is performed modulo the chosen prime. To interpret the reconstructed result as an ordinary integer sum rather than a wrapped modular sum, the true aggregate must be smaller than the modulus.

## 8. Planned research extensions

1\. Generate reproducible synthetic transaction datasets for two simulated institutions.

2\. Compare conventional aggregation with additive secret sharing.

3\. Explore collaborative fraud-model training using synthetic data.

4\. Measure model performance and computational overhead.

5\. Refine the threat model as the prototype gains functionality.

## 9. Responsible research statement

The prototype is intended for learning and research into privacy-enhancing technologies. It must not be used to process confidential banking data or be represented as a secure production banking system without substantial additional engineering, security analysis and independent review.
