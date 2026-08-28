# Third-Party Risk Dossier: Fictional CoreCloud Hosting

> Synthetic portfolio demonstration. No actual vendor or employer data is used.

## Intake Summary

- Vendor ID: **VND-002**
- Business owner: **Engineering**
- Service model: **IaaS**
- Service: Cloud infrastructure provider hosting business-critical production systems and supporting administrative operations.

## Inherent Risk and Tiering

- Inherent-risk score: **38**
- Tier: **Tier 1 - Critical**
- Review depth: **Enhanced**
- Required approval: **Security, Privacy, Legal, Procurement, and business owner**
- Reassessment: **Annual with continuous monitoring**

### Scoring Factors

- business_criticality: Critical (**+6 points**)
- data_sensitivity: Confidential (**+3 points**)
- operational_dependency: Critical (**+6 points**)
- replacement_difficulty: High (**+3 points**)
- geographic_scope: Global (**+1 points**)
- personal_information: True (**+2 points**)
- confidential_business_data: True (**+2 points**)
- customer_content: True (**+3 points**)
- production_access: True (**+3 points**)
- privileged_access: True (**+4 points**)
- api_integration: True (**+2 points**)
- subprocessors_used: True (**+1 points**)
- internet_facing: True (**+2 points**)

## Mandatory Escalations

- Security Architecture and IAM review required for privileged access.
- Operational Resilience review required for a critical service.

## Required Control Baseline

- Total controls: **14**
- Contract requirements: **10**

### ASSUR-01 — Independent Assurance

- Requirement: Provide current independent security assurance.
- Evidence: SOC 2 Type II report or ISO 27001 certification and Statement of Applicability
- Treatment: Due-diligence requirement

### FIN-01 — Financial Risk

- Requirement: Evaluate financial viability and concentration risk.
- Evidence: Financial review, insurance evidence, and concentration-risk assessment
- Treatment: Due-diligence requirement

### GOV-01 — Governance

- Requirement: Document the business owner, service purpose, and approved use.
- Evidence: Completed vendor intake and accountable business owner
- Treatment: Due-diligence requirement

### IAM-01 — Identity and Access Management

- Requirement: Enforce least privilege, strong authentication, and timely access removal.
- Evidence: SSO and MFA configuration, access model, and deprovisioning process
- Treatment: Contract requirement

### IR-01 — Incident Response

- Requirement: Notify the organization of a confirmed security incident within the contractually defined period.
- Evidence: Incident-notification clause and incident-response contact
- Treatment: Contract requirement

### MON-01 — Continuous Monitoring

- Requirement: Monitor material security, privacy, resilience, and financial changes.
- Evidence: Monitoring record, alerts, reassessment triggers, and accountable owner
- Treatment: Due-diligence requirement

### OFF-01 — Offboarding

- Requirement: Return or securely delete organizational data at termination.
- Evidence: Data-return or deletion commitment
- Treatment: Contract requirement

### PAM-01 — Privileged Access

- Requirement: Control, monitor, and periodically review privileged access.
- Evidence: PAM design, privileged-access inventory, logging, and review evidence
- Treatment: Contract requirement

### PRIV-01 — Privacy

- Requirement: Define permitted processing, retention, deletion, and privacy obligations.
- Evidence: DPA, data-flow description, retention terms, and deletion requirements
- Treatment: Contract requirement

### RES-01 — Operational Resilience

- Requirement: Maintain and test business-continuity and disaster-recovery capabilities.
- Evidence: BCDR plan, test summary, recovery objectives, and unresolved issues
- Treatment: Contract requirement

### SEC-01 — Security

- Requirement: Maintain reasonable administrative, technical, and physical safeguards.
- Evidence: Baseline security questionnaire or equivalent representation
- Treatment: Contract requirement

### SUB-01 — Subprocessor Risk

- Requirement: Maintain oversight of subprocessors and provide notice of material changes.
- Evidence: Subprocessor list, oversight process, and contractual flow-down requirements
- Treatment: Contract requirement

### TEST-01 — Security Testing

- Requirement: Perform independent penetration testing at least annually.
- Evidence: Current penetration-test executive summary and remediation status
- Treatment: Contract requirement

### VUL-01 — Vulnerability Management

- Requirement: Maintain risk-based vulnerability remediation timelines.
- Evidence: Vulnerability-management policy and remediation evidence
- Treatment: Contract requirement

## Findings and Risk Disposition

- Residual risk: **High**
- Onboarding gate: **Blocked pending accountable risk decision**
- Recommended treatment: Remediate before onboarding or execute a time-bound risk acceptance with compensating controls and vendor commitments.

### FND-004 — Privileged-access monitoring requires improvement

- Severity: **High**
- Condition: Privileged activity is logged, but periodic privileged-access certification is not consistently documented.
- Risk: Excessive or inappropriate administrative access may persist without detection across business-critical infrastructure.
- Recommendation: Implement documented quarterly privileged-access certification with accountable reviewers and tracked removals.
- Vendor commitment: Implement quarterly certification within 30 days.
- Owner: Vendor IAM Director
- Status: Open

### FND-005 — Recovery exercise evidence is incomplete

- Severity: **High**
- Condition: The vendor supplied a recovery plan but did not provide complete evidence showing that critical recovery objectives were achieved during the latest exercise.
- Risk: The vendor may be unable to restore critical hosted services within business-approved recovery requirements.
- Recommendation: Provide the latest exercise results, achieved recovery times, unresolved issues, and remediation ownership.
- Vendor commitment: Complete and document a recovery exercise within 60 days.
- Owner: Vendor Resilience Director
- Status: Open

## Lifecycle Governance

- Current gate: **Due diligence must be completed before risk approval**

- **Intake** — Completed (Owner: Business Owner and Procurement)
- **Tiering** — Completed (Owner: Third-Party Risk Management)
- **Due Diligence** — Required (Owner: Third-Party Risk Management and Domain Specialists)
- **Risk Decision** — Blocked pending due diligence (Owner: Accountable Risk Owner)
- **Contracting** — Blocked pending risk decision (Owner: Legal and Procurement)
- **Onboarding** — Blocked pending contract execution (Owner: Business Owner, IT, Security, and Procurement)
- **Continuous Monitoring** — Scheduled after onboarding (Owner: Third-Party Risk Management)
- **Reassessment** — Annual with continuous monitoring (Owner: Third-Party Risk Management and Business Owner)
- **Offboarding** — Required at termination (Owner: Business Owner, IT, Legal, and Procurement)

## Governance Notice

This output is a preliminary recommendation. Vendor approval, exceptions, and risk acceptance require accountable human owners.