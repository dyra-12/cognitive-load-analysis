# ⚖️ Ethics Statement – CogniViz

This document outlines the ethical considerations, compliance measures, and participant protection protocols implemented during the CogniViz study. It covers procedures for informed consent, data anonymization, ethics oversight, and risk mitigation.

## 1. Overview

CogniViz investigates real-time cognitive load detection based on non-invasive user interaction patterns, including mouse movement, cursor dynamics, and timing-based keyboard telemetry.

All data collection was behavioral, non-intrusive, and fully anonymized, conducted under informed consent procedures.

The study was classified as IRB-exempt (IRB-free) under institutional and national research ethics guidelines, as it involved:

- No collection of personally identifiable information (PII)
- No intervention, deception, or manipulation
- No physiological, medical, or sensitive psychological data

Despite IRB exemption, the study followed formal ethical review procedures and adhered to established ethical standards, including:

- ACM Code of Ethics (2018)
- Declaration of Helsinki (2013)

## 2. Informed Consent Procedures

### 2.1 Participant Recruitment

Participants were recruited via internal university mailing lists and bulletin announcements.

Eligibility criteria: Age ≥ 18, basic computer literacy, and familiarity with everyday web interfaces.

Participation was entirely voluntary.

No personally identifying information (name, email, IP address, or device identifiers) was collected.

### 2.2 Consent Process

Before participation, each individual:

**Received a written Information Sheet describing:**
- The study's purpose, scope, and expected duration
- The nature of interaction logging (event-level behavioral telemetry only)
- The anonymization process and data usage for academic research
- Their right to withdraw without penalty

**Provided digital consent via a secure web interface confirming that:**
- Participation was voluntary
- Data would be anonymized and used solely for research and publication
- No physical, psychological, or privacy risks were anticipated

### 2.3 Right to Withdraw

Participants could withdraw from the study at any time during or after participation by referencing their anonymized participant identifier. All associated data would be excluded upon request.

## 3. IRB Exemption and Ethics Oversight

### 3.1 IRB-Free Classification

This study was determined to be IRB-exempt (IRB-free) under applicable institutional and national research ethics frameworks, as it meets the criteria for minimal-risk behavioral research:

- No collection of sensitive or identifying data
- No experimental manipulation of participants
- No health, biometric, or clinical measures
- No vulnerable populations involved

Accordingly, formal Institutional Review Board approval was not required.

### 3.2 Institutional Ethics Review

Although IRB approval was not mandatory, the study protocol underwent institutional ethics screening and was reviewed by the University Human Research Ethics Committee (HREC) under protocol reference:

**HCI–2025–04**  
*Behavioral Interaction Study: Cognitive Load Estimation via Interaction Telemetry*

This review confirmed IRB exemption status and verified compliance with ethical best practices.

## 4. Data Anonymization and De-Identification

### 4.1 Data Types Collected

Only non-sensitive interaction telemetry was logged:

- Mouse movement trajectories, click timing, drag actions
- Focus changes and keystroke timing (no keystroke content)
- Idle-time and hover metrics
- Task identifiers (e.g., form-entry, product-exploration, travel-planning)

No personal text input, names, emails, or identifiers were captured.

### 4.2 Anonymization Protocol

- Each participant was assigned a random alphanumeric ID (e.g., P01–P25)
- All data were stored exclusively under these pseudonyms
- No IP addresses, device fingerprints, or session identifiers were logged
- Feature aggregation and normalization were applied prior to analysis

These measures ensured irreversible de-identification, preventing both direct and indirect re-identification.

### 4.3 Data Storage and Access

- Data were stored on encrypted university-managed servers
- Access was restricted to authorized members of the research team
- Raw event logs were retained only for feature extraction and then discarded
- All publicly released datasets contain only aggregated, anonymized features, compliant with GDPR data-minimization principles

## 5. Compliance Frameworks

CogniViz adheres to the following ethical and regulatory standards:

- ACM Ethics and Plagiarism Guidelines (2024)
- GDPR (EU General Data Protection Regulation) for anonymization and data handling
- APA Ethical Principles of Psychologists (2017) for human-participant research
- ISO 9241-210 principles for Human-Centered Design research

## 6. Risk Assessment and Mitigation

| Potential Risk | Description | Mitigation Measures |
|----------------|-------------|---------------------|
| Privacy concerns | Participants may worry about being monitored | Only non-sensitive behavioral telemetry recorded; no content or identity captured |
| Psychological discomfort | Awareness of observation may cause unease | Clear briefing emphasized no performance evaluation; withdrawal allowed anytime |
| Data misuse | Risk of unauthorized access or re-identification | Strong anonymization, encrypted storage, limited access |
| Algorithmic bias | Task- or user-specific behavioral bias | Leave-One-User-Out validation to ensure fairness and generalizability |

**Overall risk classification:** Minimal to none

## 7. Data Retention and Sharing

- **Retention period:** De-identified feature data retained for 5 years post-publication
- **Public release:** Only anonymized, aggregated datasets and source code are shared
- No raw interaction logs, session traces, or identifiable metadata are distributed

## 8. Participant Debriefing

At the end of each session:

- Participants received a debrief explaining the study's goals and potential applications
- Optional follow-up contact was offered to access published results or dataset summaries
- No deception was used at any stage of the study

## 9. Ethical Positioning Summary

CogniViz was conducted as an IRB-exempt, minimal-risk behavioral study, yet implemented full ethical safeguards typically associated with formally approved research. This approach ensures participant dignity, privacy, and autonomy while supporting transparent, reproducible human-centered AI research.