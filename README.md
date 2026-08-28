# Enterprise TPRM Lifecycle Control Tower

[![TPRM Control Tower Tests](https://github.com/creativesolutions2013-debug/enterprise-tprm-lifecycle-control-tower/actions/workflows/control-tower-tests.yml/badge.svg)](https://github.com/creativesolutions2013-debug/enterprise-tprm-lifecycle-control-tower/actions/workflows/control-tower-tests.yml)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-tprm-control-tower.streamlit.app/)

## Try the Live Demo

Explore the complete risk-based third-party lifecycle using fictional vendor scenarios:

**[Launch the Enterprise TPRM Lifecycle Control Tower](https://enterprise-tprm-control-tower.streamlit.app/)**

The dashboard demonstrates portfolio risk reporting, vendor tiering, due-diligence gates, lifecycle ownership, remediation tracking, contractual accountability, continuous monitoring, and human risk-decision boundaries.

> Use fictional or synthetic information only. Do not submit actual vendor evidence, personal information, credentials, or confidential employer documentation.

A portfolio demonstration of a scalable, risk-based third-party risk management program covering the complete vendor lifecycle.

This project shows how I approach third-party governance strategically and hands-on: establishing control baselines, tiering vendors by inherent risk, scaling due diligence, enforcing decision gates, tracking remediation, monitoring material changes, and preserving accountable human oversight.

> **Synthetic-data notice:** Every vendor, finding, and scenario in this repository is fictional. Do not use confidential vendor evidence, personal information, credentials, or employer documentation.

## Business Problem

Growing organizations need to evaluate vendors quickly without applying the same review depth to every third party. A scalable program must concentrate resources on vendors with the greatest data exposure, access, criticality, privacy impact, operational dependency, and emerging-technology risk.

This control tower demonstrates how to:

- Establish third-party security and governance baselines
- Classify vendors using transparent inherent-risk factors
- Scale due diligence according to risk
- Coordinate Security, Privacy, Legal, Procurement, and business stakeholders
- Block premature onboarding when material risks remain unresolved
- Translate findings into remediation and contractual requirements
- Monitor the portfolio throughout the vendor lifecycle
- Preserve accountable human approval and risk acceptance

## Demonstrated Capabilities

### Risk-Based Vendor Tiering

The tiering engine evaluates factors such as:

- Business criticality
- Data sensitivity
- Personal-information processing
- Production connectivity
- API access
- Privileged access
- Operational dependency
- AI-enabled processing

The resulting tier determines review depth, evidence requirements, reassessment frequency, monitoring expectations, and approval groups.

### Control Baselines

The project applies baseline and conditional controls across:

- Information security governance
- Identity and access management
- Privileged access
- Encryption and data protection
- Privacy
- Independent assurance
- Vulnerability management
- Penetration testing
- Incident response
- Business continuity and resilience
- Financial risk
- Subprocessor management
- Continuous monitoring
- AI governance
- Secure offboarding

### End-to-End Lifecycle Governance

The lifecycle model contains nine ordered stages:

1. Intake
2. Tiering
3. Due diligence
4. Risk decision
5. Contracting
6. Onboarding
7. Continuous monitoring
8. Reassessment
9. Offboarding

Due diligence and accountable risk decisions must occur before onboarding. The application never automatically approves a vendor or accepts risk.

### Remediation and Contractual Accountability

The synthetic portfolio includes examples involving:

- Missing independent penetration-testing evidence
- Insufficient security-log retention
- Incomplete AI-governance evidence
- Privileged-access certification gaps
- Incomplete recovery-exercise evidence

A contractual commitment does not close a finding. Risk remains open until implementation evidence is received, validated, and formally recorded.

## Synthetic Portfolio

| Vendor | Scenario | Preliminary Path |
|---|---|---|
| Fictional RevenueAI Cloud | AI-enabled revenue-intelligence platform processing customer content | Tier 1 review and accountable decision required |
| Fictional CoreCloud Hosting | Critical infrastructure provider with privileged production access | Tier 1 review and accountable decision required |
| Fictional Training Advisors | Low-risk professional service with no system connectivity | Standard low-risk approval path |

The current portfolio contains:

- 3 fictional vendors
- 5 open findings
- 3 high findings
- 2 moderate findings
- 2 vendors blocked pending accountable decisions

## Interactive Dashboard

The Streamlit dashboard provides:

- Portfolio risk metrics
- Vendor-level risk dossiers
- Findings and onboarding gates
- Lifecycle ownership and required outcomes
- Scalable review guidance
- Remediation tracking and severity filtering
- Generated Markdown report previews
- Downloadable governance artifacts
- Explicit human-decision boundaries

Run it locally:

```bash
python -m pip install -r requirements.txt
streamlit run web_app.py
```

## Command-Line Assessment

Generate the portfolio summary and vendor dossiers:

```bash
python app.py
```

Generated reports are written to:

```text
outputs/
```

## Automated Validation

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The repository includes 18 automated tests covering:

- Vendor-tier consistency
- Low-risk and critical-vendor classification
- AI-governance escalation
- IAM and privileged-access escalation
- Control-baseline selection
- Lifecycle-stage ordering
- Reassessment frequency
- Findings and portfolio metrics
- High-risk onboarding blocks
- Human-approval boundaries
- Report-generation consistency

GitHub Actions automatically validates Python syntax, synthetic JSON data, report generation, all automated tests, and generated-report consistency on every push and pull request.

## Project Structure

```text
.
├── .github/workflows/
│   └── control-tower-tests.yml
├── data/
│   ├── vendor_findings.json
│   └── vendor_scenarios.json
├── outputs/
│   ├── portfolio-summary.md
│   └── vendor risk dossiers
├── tests/
│   └── test_control_tower.py
├── app.py
├── controls.py
├── lifecycle.py
├── reporting.py
├── tiering.py
├── web_app.py
└── requirements.txt
```

## Governance Boundary

This project supports analysis, routing, reporting, and decision preparation. It does not:

- Approve a vendor
- Accept security or privacy risk
- Replace Legal or Procurement review
- Replace qualified security judgment
- Provide audit or legal assurance
- Validate real vendor evidence

Material findings require documented remediation, approved compensating controls, contractual treatment, or formal risk acceptance by authorized stakeholders.

## Portfolio Purpose

This project demonstrates practical capability in:

- Building and maturing a TPRM program
- Establishing risk and control baselines
- Applying scalable risk-based reviews
- Communicating technical risk in business terms
- Coordinating cross-functional decision owners
- Holding vendors accountable to contractual requirements
- Managing remediation and continuous monitoring
- Automating repeatable governance workflows
- Maintaining human oversight over consequential decisions

