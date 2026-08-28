# Third-Party Risk Dossier: Fictional RevenueAI Cloud

> Synthetic portfolio demonstration. No actual vendor or employer data is used.

## Intake Summary

- Vendor ID: **VND-001**
- Business owner: **Revenue Operations**
- Service model: **SaaS**
- Service: AI-enabled revenue intelligence platform that processes recorded customer conversations and generates sales insights.

## Inherent Risk and Tiering

- Inherent-risk score: **35**
- Tier: **Tier 1 - Critical**
- Review depth: **Enhanced**
- Required approval: **Security, Privacy, Legal, Procurement, and business owner**
- Reassessment: **Annual with continuous monitoring**

### Scoring Factors

- business_criticality: High (**+4 points**)
- data_sensitivity: Restricted (**+5 points**)
- operational_dependency: High (**+4 points**)
- replacement_difficulty: High (**+3 points**)
- geographic_scope: Global (**+1 points**)
- personal_information: True (**+2 points**)
- confidential_business_data: True (**+2 points**)
- customer_content: True (**+3 points**)
- production_access: True (**+3 points**)
- api_integration: True (**+2 points**)
- subprocessors_used: True (**+1 points**)
- artificial_intelligence: True (**+1 points**)
- generative_ai: True (**+2 points**)
- internet_facing: True (**+2 points**)

## Mandatory Escalations

- AI Governance review required because generative AI processes customer content.

## Required Control Baseline

- Total controls: **14**
- Contract requirements: **10**

### AI-01 — AI Governance

- Requirement: Document AI use, data flows, human oversight, model limitations, and prohibited uses.
- Evidence: AI system description, data-use statement, model governance, and human-oversight controls
- Treatment: Contract requirement

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

### FND-001 — Independent penetration test not completed

- Severity: **High**
- Condition: The vendor has not completed an independent penetration test for the current production environment.
- Risk: Undetected exploitable weaknesses could expose customer conversations, personal information, and confidential business data.
- Recommendation: Complete an independent penetration test, remediate material findings, and provide an executive summary for validation.
- Vendor commitment: Complete testing within 120 days after contract execution.
- Owner: Vendor Security Lead
- Status: Open

### FND-002 — Security-log retention below baseline

- Severity: **Moderate**
- Condition: The vendor retains security logs for 30 days rather than the required 180-day baseline.
- Risk: Limited retention may prevent timely investigation of security events discovered after the available log window.
- Recommendation: Increase security-log retention to at least 180 days and validate centralized monitoring coverage.
- Vendor commitment: Increase retention within 60 days after contract execution.
- Owner: Vendor Security Operations
- Status: Open

### FND-003 — AI governance evidence requires clarification

- Severity: **Moderate**
- Condition: The vendor provided limited documentation describing model limitations, human oversight, and controls preventing customer content from being used for model training.
- Risk: Insufficient transparency could result in customer data being processed outside approved expectations or AI outputs being relied upon without appropriate oversight.
- Recommendation: Provide the AI system description, data-use restrictions, human-oversight process, and documented model limitations.
- Vendor commitment: Provide documentation before production onboarding.
- Owner: Vendor AI Governance Lead
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