from pathlib import Path

from controls import build_control_baseline
from lifecycle import build_lifecycle_plan, validate_stage_order
from reporting import (
    build_portfolio_report,
    build_vendor_report,
    load_findings,
    render_portfolio_report,
)
from tiering import classify_vendor, load_vendors


OUTPUT_DIRECTORY = Path("outputs")


def build_vendor_dossier(vendor, findings):
    """Combine all TPRM decisions for one synthetic vendor."""
    classification = classify_vendor(vendor)
    baseline = build_control_baseline(vendor)
    lifecycle = build_lifecycle_plan(vendor)
    risk_report = build_vendor_report(vendor, findings)

    if classification["tier"] != baseline["tier"]:
        raise ValueError("Tier mismatch between classification and baseline.")

    if classification["tier"] != lifecycle["tier"]:
        raise ValueError("Tier mismatch between classification and lifecycle.")

    if not validate_stage_order(lifecycle):
        raise ValueError("Lifecycle stages are incomplete or out of order.")

    return {
        "vendor": vendor,
        "classification": classification,
        "baseline": baseline,
        "lifecycle": lifecycle,
        "risk_report": risk_report,
        "governance_notice": (
            "This output is a preliminary recommendation. Vendor approval, "
            "exceptions, and risk acceptance require accountable human owners."
        ),
    }


def run_control_tower(vendors=None, findings=None):
    """Run the complete synthetic third-party lifecycle workflow."""
    if vendors is None:
        vendors = load_vendors()

    if findings is None:
        findings = load_findings()

    dossiers = [
        build_vendor_dossier(vendor, findings)
        for vendor in vendors
    ]
    portfolio = build_portfolio_report(vendors, findings)

    return {
        "dossiers": dossiers,
        "portfolio": portfolio,
        "vendor_count": len(dossiers),
        "human_approval_required": True,
    }


def render_vendor_dossier(dossier):
    """Render a complete vendor decision record in Markdown."""
    vendor = dossier["vendor"]
    classification = dossier["classification"]
    baseline = dossier["baseline"]
    lifecycle = dossier["lifecycle"]
    risk_report = dossier["risk_report"]

    lines = [
        f"# Third-Party Risk Dossier: {vendor['vendor_name']}",
        "",
        "> Synthetic portfolio demonstration. No actual vendor or employer data is used.",
        "",
        "## Intake Summary",
        "",
        f"- Vendor ID: **{vendor['vendor_id']}**",
        f"- Business owner: **{vendor['business_owner']}**",
        f"- Service model: **{vendor['service_model']}**",
        f"- Service: {vendor['service_description']}",
        "",
        "## Inherent Risk and Tiering",
        "",
        f"- Inherent-risk score: **{classification['inherent_risk_score']}**",
        f"- Tier: **{classification['tier']}**",
        f"- Review depth: **{classification['review_depth']}**",
        f"- Required approval: **{classification['required_approval']}**",
        f"- Reassessment: **{classification['reassessment_frequency']}**",
        "",
        "### Scoring Factors",
        "",
    ]

    for factor in classification["risk_factors"]:
        lines.append(
            f"- {factor['factor']}: {factor['value']} "
            f"(**+{factor['points']} points**)"
        )

    lines.extend(
        [
            "",
            "## Mandatory Escalations",
            "",
        ]
    )

    if classification["mandatory_escalations"]:
        lines.extend(
            f"- {escalation}"
            for escalation in classification["mandatory_escalations"]
        )
    else:
        lines.append("- No mandatory specialist escalation triggered.")

    lines.extend(
        [
            "",
            "## Required Control Baseline",
            "",
            f"- Total controls: **{baseline['control_count']}**",
            f"- Contract requirements: **{baseline['contract_control_count']}**",
            "",
        ]
    )

    for control in baseline["controls"]:
        contract_label = (
            "Contract requirement"
            if control["contract_requirement"]
            else "Due-diligence requirement"
        )

        lines.extend(
            [
                f"### {control['control_id']} — {control['domain']}",
                "",
                f"- Requirement: {control['requirement']}",
                f"- Evidence: {control['evidence']}",
                f"- Treatment: {contract_label}",
                "",
            ]
        )

    lines.extend(
        [
            "## Findings and Risk Disposition",
            "",
            f"- Residual risk: **{risk_report['residual_risk']}**",
            f"- Onboarding gate: **{risk_report['onboarding_gate']}**",
            f"- Recommended treatment: {risk_report['recommended_treatment']}",
            "",
        ]
    )

    if risk_report["findings"]:
        for finding in risk_report["findings"]:
            lines.extend(
                [
                    f"### {finding['finding_id']} — {finding['title']}",
                    "",
                    f"- Severity: **{finding['severity']}**",
                    f"- Condition: {finding['condition']}",
                    f"- Risk: {finding['risk']}",
                    f"- Recommendation: {finding['recommendation']}",
                    f"- Vendor commitment: {finding['vendor_commitment']}",
                    f"- Owner: {finding['owner']}",
                    f"- Status: {finding['status']}",
                    "",
                ]
            )
    else:
        lines.append("- No findings identified in the synthetic scenario.")
        lines.append("")

    lines.extend(
        [
            "## Lifecycle Governance",
            "",
            f"- Current gate: **{lifecycle['current_gate']}**",
            "",
        ]
    )

    for stage in lifecycle["stages"]:
        lines.append(
            f"- **{stage['name']}** — {stage['status']} "
            f"(Owner: {stage['owner']})"
        )

    lines.extend(
        [
            "",
            "## Governance Notice",
            "",
            dossier["governance_notice"],
        ]
    )

    return "\n".join(lines)


def write_control_tower_outputs(result):
    """Write portfolio and vendor reports for employer review."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    portfolio_path = OUTPUT_DIRECTORY / "portfolio-summary.md"
    portfolio_path.write_text(
        render_portfolio_report(result["portfolio"]),
        encoding="utf-8",
    )

    vendor_paths = []

    for dossier in result["dossiers"]:
        vendor_id = dossier["vendor"]["vendor_id"].lower()
        vendor_path = OUTPUT_DIRECTORY / f"{vendor_id}-risk-dossier.md"
        vendor_path.write_text(
            render_vendor_dossier(dossier),
            encoding="utf-8",
        )
        vendor_paths.append(vendor_path)

    return portfolio_path, vendor_paths


if __name__ == "__main__":
    result = run_control_tower()
    portfolio_path, vendor_paths = write_control_tower_outputs(result)

    print(f"Vendors processed: {result['vendor_count']}")
    print(
        "Portfolio posture: "
        f"{result['portfolio']['portfolio_posture']}"
    )
    print(
        "Human approval required: "
        f"{result['human_approval_required']}"
    )
    print(f"Portfolio report: {portfolio_path}")

    for vendor_path in vendor_paths:
        print(f"Vendor dossier: {vendor_path}")