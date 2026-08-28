from tiering import classify_vendor


BASELINE_CONTROLS = [
    {
        "control_id": "GOV-01",
        "domain": "Governance",
        "requirement": "Document the business owner, service purpose, and approved use.",
        "evidence": "Completed vendor intake and accountable business owner",
        "contract_requirement": False,
    },
    {
        "control_id": "SEC-01",
        "domain": "Security",
        "requirement": "Maintain reasonable administrative, technical, and physical safeguards.",
        "evidence": "Baseline security questionnaire or equivalent representation",
        "contract_requirement": True,
    },
    {
        "control_id": "IR-01",
        "domain": "Incident Response",
        "requirement": "Notify the organization of a confirmed security incident within the contractually defined period.",
        "evidence": "Incident-notification clause and incident-response contact",
        "contract_requirement": True,
    },
    {
        "control_id": "OFF-01",
        "domain": "Offboarding",
        "requirement": "Return or securely delete organizational data at termination.",
        "evidence": "Data-return or deletion commitment",
        "contract_requirement": True,
    },
]

TIER_CONTROLS = {
    "Tier 1 - Critical": [
        {
            "control_id": "ASSUR-01",
            "domain": "Independent Assurance",
            "requirement": "Provide current independent security assurance.",
            "evidence": "SOC 2 Type II report or ISO 27001 certification and Statement of Applicability",
            "contract_requirement": False,
        },
        {
            "control_id": "TEST-01",
            "domain": "Security Testing",
            "requirement": "Perform independent penetration testing at least annually.",
            "evidence": "Current penetration-test executive summary and remediation status",
            "contract_requirement": True,
        },
        {
            "control_id": "VUL-01",
            "domain": "Vulnerability Management",
            "requirement": "Maintain risk-based vulnerability remediation timelines.",
            "evidence": "Vulnerability-management policy and remediation evidence",
            "contract_requirement": True,
        },
        {
            "control_id": "RES-01",
            "domain": "Operational Resilience",
            "requirement": "Maintain and test business-continuity and disaster-recovery capabilities.",
            "evidence": "BCDR plan, test summary, recovery objectives, and unresolved issues",
            "contract_requirement": True,
        },
        {
            "control_id": "FIN-01",
            "domain": "Financial Risk",
            "requirement": "Evaluate financial viability and concentration risk.",
            "evidence": "Financial review, insurance evidence, and concentration-risk assessment",
            "contract_requirement": False,
        },
        {
            "control_id": "MON-01",
            "domain": "Continuous Monitoring",
            "requirement": "Monitor material security, privacy, resilience, and financial changes.",
            "evidence": "Monitoring record, alerts, reassessment triggers, and accountable owner",
            "contract_requirement": False,
        },
    ],
    "Tier 2 - High": [
        {
            "control_id": "ASSUR-01",
            "domain": "Independent Assurance",
            "requirement": "Provide current independent security assurance.",
            "evidence": "SOC 2 Type II report, ISO 27001 certification, or equivalent evidence",
            "contract_requirement": False,
        },
        {
            "control_id": "TEST-01",
            "domain": "Security Testing",
            "requirement": "Perform periodic independent penetration testing.",
            "evidence": "Current penetration-test summary and remediation status",
            "contract_requirement": False,
        },
        {
            "control_id": "RES-01",
            "domain": "Operational Resilience",
            "requirement": "Maintain documented continuity and recovery capabilities.",
            "evidence": "BCDR documentation and latest exercise summary",
            "contract_requirement": True,
        },
        {
            "control_id": "FIN-01",
            "domain": "Financial Risk",
            "requirement": "Perform a proportionate financial-risk review.",
            "evidence": "Financial review or approved financial-risk screening",
            "contract_requirement": False,
        },
    ],
    "Tier 3 - Moderate": [
        {
            "control_id": "DUE-01",
            "domain": "Due Diligence",
            "requirement": "Complete targeted due diligence based on service scope.",
            "evidence": "Targeted questionnaire and applicable supporting evidence",
            "contract_requirement": False,
        }
    ],
    "Tier 4 - Low": [],
}


def conditional_controls(vendor):
    """Return controls triggered by vendor scope rather than tier alone."""
    controls = []

    if (
        vendor.get("personal_information")
        or vendor.get("regulated_data")
        or vendor.get("customer_content")
    ):
        controls.append(
            {
                "control_id": "PRIV-01",
                "domain": "Privacy",
                "requirement": "Define permitted processing, retention, deletion, and privacy obligations.",
                "evidence": "DPA, data-flow description, retention terms, and deletion requirements",
                "contract_requirement": True,
            }
        )

    if vendor.get("production_access") or vendor.get("api_integration"):
        controls.append(
            {
                "control_id": "IAM-01",
                "domain": "Identity and Access Management",
                "requirement": "Enforce least privilege, strong authentication, and timely access removal.",
                "evidence": "SSO and MFA configuration, access model, and deprovisioning process",
                "contract_requirement": True,
            }
        )

    if vendor.get("privileged_access"):
        controls.append(
            {
                "control_id": "PAM-01",
                "domain": "Privileged Access",
                "requirement": "Control, monitor, and periodically review privileged access.",
                "evidence": "PAM design, privileged-access inventory, logging, and review evidence",
                "contract_requirement": True,
            }
        )

    if vendor.get("subprocessors_used"):
        controls.append(
            {
                "control_id": "SUB-01",
                "domain": "Subprocessor Risk",
                "requirement": "Maintain oversight of subprocessors and provide notice of material changes.",
                "evidence": "Subprocessor list, oversight process, and contractual flow-down requirements",
                "contract_requirement": True,
            }
        )

    if vendor.get("artificial_intelligence"):
        controls.append(
            {
                "control_id": "AI-01",
                "domain": "AI Governance",
                "requirement": "Document AI use, data flows, human oversight, model limitations, and prohibited uses.",
                "evidence": "AI system description, data-use statement, model governance, and human-oversight controls",
                "contract_requirement": True,
            }
        )

    if vendor.get("model_training_on_customer_data"):
        controls.append(
            {
                "control_id": "AI-02",
                "domain": "AI Data Use",
                "requirement": "Prohibit model training on customer data unless specifically reviewed and approved.",
                "evidence": "Contractual data-use restriction and documented executive approval",
                "contract_requirement": True,
            }
        )

    return controls


def build_control_baseline(vendor):
    """Build the tiered and scope-specific control baseline."""
    classification = classify_vendor(vendor)
    controls = list(BASELINE_CONTROLS)
    controls.extend(TIER_CONTROLS[classification["tier"]])
    controls.extend(conditional_controls(vendor))

    unique_controls = {}

    for control in controls:
        unique_controls[control["control_id"]] = control

    ordered_controls = sorted(
        unique_controls.values(),
        key=lambda control: control["control_id"],
    )

    return {
        "vendor_id": vendor["vendor_id"],
        "vendor_name": vendor["vendor_name"],
        "tier": classification["tier"],
        "review_depth": classification["review_depth"],
        "controls": ordered_controls,
        "control_count": len(ordered_controls),
        "contract_control_count": sum(
            control["contract_requirement"]
            for control in ordered_controls
        ),
        "decision_status": "Proposed baseline - human approval required",
    }


if __name__ == "__main__":
    from tiering import load_vendors

    for vendor in load_vendors():
        baseline = build_control_baseline(vendor)

        print(
            f"{baseline['vendor_id']} | {baseline['tier']} | "
            f"Controls: {baseline['control_count']} | "
            f"Contract requirements: {baseline['contract_control_count']}"
        )

        print(
            "  IDs: "
            + ", ".join(
                control["control_id"]
                for control in baseline["controls"]
            )
        )