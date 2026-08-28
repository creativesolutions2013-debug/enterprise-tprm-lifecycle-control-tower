from controls import build_control_baseline
from tiering import classify_vendor


LIFECYCLE_STAGES = [
    "Intake",
    "Tiering",
    "Due Diligence",
    "Risk Decision",
    "Contracting",
    "Onboarding",
    "Continuous Monitoring",
    "Reassessment",
    "Offboarding",
]

MONITORING_TRIGGERS = [
    "Confirmed or suspected security incident",
    "Material change in service scope or data access",
    "New privileged access or production connectivity",
    "Addition of AI processing or model training",
    "Material subprocessor change",
    "Significant adverse security-rating change",
    "Financial distress or ownership change",
    "Repeated missed remediation commitments",
]

OFFBOARDING_REQUIREMENTS = [
    "Disable vendor accounts, credentials, tokens, and integrations",
    "Revoke privileged and production access",
    "Confirm return or secure deletion of organizational data",
    "Obtain deletion certification when contractually required",
    "Preserve required legal, audit, and risk records",
    "Close or formally transfer outstanding remediation items",
    "Document lessons learned and update the vendor inventory",
]


def build_stage(
    name,
    owner,
    status,
    entry_criteria,
    exit_criteria,
    required_artifacts,
):
    """Create a consistent lifecycle-stage record."""
    return {
        "name": name,
        "owner": owner,
        "status": status,
        "entry_criteria": entry_criteria,
        "exit_criteria": exit_criteria,
        "required_artifacts": required_artifacts,
    }


def build_lifecycle_plan(vendor):
    """Create the complete governed third-party lifecycle plan."""
    classification = classify_vendor(vendor)
    baseline = build_control_baseline(vendor)

    contract_controls = [
        control
        for control in baseline["controls"]
        if control["contract_requirement"]
    ]

    stages = [
        build_stage(
            name="Intake",
            owner="Business Owner and Procurement",
            status="Completed",
            entry_criteria="Business request submitted",
            exit_criteria="Service scope, owner, data, access, and criticality documented",
            required_artifacts=[
                "Vendor intake",
                "Service description",
                "Business justification",
                "Data and access classification",
            ],
        ),
        build_stage(
            name="Tiering",
            owner="Third-Party Risk Management",
            status="Completed",
            entry_criteria="Complete intake information",
            exit_criteria="Inherent-risk score and vendor tier validated",
            required_artifacts=[
                "Risk-factor calculation",
                "Tiering rationale",
                "Mandatory escalation record",
            ],
        ),
        build_stage(
            name="Due Diligence",
            owner="Third-Party Risk Management and Domain Specialists",
            status="Required",
            entry_criteria="Approved vendor tier and control baseline",
            exit_criteria="Required evidence reviewed and findings documented",
            required_artifacts=[
                control["evidence"]
                for control in baseline["controls"]
            ],
        ),
        build_stage(
            name="Risk Decision",
            owner="Accountable Risk Owner",
            status="Blocked pending due diligence",
            entry_criteria="Completed assessment and documented findings",
            exit_criteria="Remediate, accept, avoid, or transfer decision recorded",
            required_artifacts=[
                "Assessment report",
                "Residual-risk statement",
                "Remediation plan",
                "Risk acceptance when applicable",
            ],
        ),
        build_stage(
            name="Contracting",
            owner="Legal and Procurement",
            status="Blocked pending risk decision",
            entry_criteria="Approved security and privacy position",
            exit_criteria="Required obligations incorporated into executed agreement",
            required_artifacts=[
                f"{control['control_id']}: {control['requirement']}"
                for control in contract_controls
            ],
        ),
        build_stage(
            name="Onboarding",
            owner="Business Owner, IT, Security, and Procurement",
            status="Blocked pending contract execution",
            entry_criteria="Executed agreement and approved risk decision",
            exit_criteria="Access provisioned according to approved scope and controls",
            required_artifacts=[
                "Final approval record",
                "Access authorization",
                "Vendor inventory record",
                "Monitoring owner assignment",
            ],
        ),
        build_stage(
            name="Continuous Monitoring",
            owner="Third-Party Risk Management",
            status="Scheduled after onboarding",
            entry_criteria="Active vendor relationship",
            exit_criteria="Alerts reviewed and material changes escalated",
            required_artifacts=[
                "Monitoring alerts",
                "Issue and remediation tracker",
                "Material-change assessments",
            ],
        ),
        build_stage(
            name="Reassessment",
            owner="Third-Party Risk Management and Business Owner",
            status=classification["reassessment_frequency"],
            entry_criteria="Scheduled date or material-change trigger",
            exit_criteria="Tier, evidence, findings, and risk decision refreshed",
            required_artifacts=[
                "Updated intake",
                "Current security and privacy evidence",
                "Remediation status",
                "Revalidated risk decision",
            ],
        ),
        build_stage(
            name="Offboarding",
            owner="Business Owner, IT, Legal, and Procurement",
            status="Required at termination",
            entry_criteria="Contract termination, expiration, or replacement",
            exit_criteria="Access revoked, data disposition confirmed, and records closed",
            required_artifacts=OFFBOARDING_REQUIREMENTS,
        ),
    ]

    return {
        "vendor_id": vendor["vendor_id"],
        "vendor_name": vendor["vendor_name"],
        "tier": classification["tier"],
        "inherent_risk_score": classification["inherent_risk_score"],
        "review_depth": classification["review_depth"],
        "required_approval": classification["required_approval"],
        "reassessment_frequency": classification["reassessment_frequency"],
        "mandatory_escalations": classification["mandatory_escalations"],
        "control_count": baseline["control_count"],
        "contract_control_count": baseline["contract_control_count"],
        "contract_controls": contract_controls,
        "monitoring_triggers": MONITORING_TRIGGERS,
        "stages": stages,
        "current_gate": "Due diligence must be completed before risk approval",
        "human_decision_required": True,
    }


def validate_stage_order(plan):
    """Ensure the plan contains every lifecycle stage in order."""
    stage_names = [stage["name"] for stage in plan["stages"]]
    return stage_names == LIFECYCLE_STAGES


if __name__ == "__main__":
    from tiering import load_vendors

    for vendor in load_vendors():
        plan = build_lifecycle_plan(vendor)

        print(
            f"{plan['vendor_id']} | {plan['tier']} | "
            f"Current gate: {plan['current_gate']} | "
            f"Stage order valid: {validate_stage_order(plan)}"
        )

        print(
            "  Reassessment: "
            f"{plan['reassessment_frequency']}"
        )