import json
from collections import Counter
from pathlib import Path

from lifecycle import build_lifecycle_plan
from tiering import load_vendors


DEFAULT_FINDINGS_PATH = Path("data/vendor_findings.json")
DEFAULT_OUTPUT_PATH = Path("outputs/portfolio-summary.md")

SEVERITY_ORDER = {
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Critical": 4,
}


def load_findings(path=DEFAULT_FINDINGS_PATH):
    """Load and validate synthetic vendor findings."""
    findings_path = Path(path)

    with findings_path.open(encoding="utf-8") as findings_file:
        findings = json.load(findings_file)

    if not isinstance(findings, list):
        raise ValueError("Findings data must contain a JSON list.")

    required_fields = {
        "finding_id",
        "vendor_id",
        "control_id",
        "title",
        "severity",
        "risk",
        "recommendation",
        "vendor_commitment",
        "owner",
        "target_days",
        "status",
        "contract_dependency",
    }

    for finding in findings:
        missing_fields = required_fields.difference(finding)

        if missing_fields:
            raise ValueError(
                f"{finding.get('finding_id', 'Unknown finding')} is missing "
                f"required fields: {sorted(missing_fields)}"
            )

    return findings


def highest_open_severity(findings):
    """Return the highest severity among open findings."""
    open_findings = [
        finding
        for finding in findings
        if finding["status"] == "Open"
    ]

    if not open_findings:
        return "Low"

    return max(
        (
            finding["severity"]
            for finding in open_findings
        ),
        key=lambda severity: SEVERITY_ORDER[severity],
    )


def determine_risk_disposition(vendor_findings):
    """Recommend governed treatment without making the human decision."""
    open_findings = [
        finding
        for finding in vendor_findings
        if finding["status"] == "Open"
    ]
    highest_severity = highest_open_severity(vendor_findings)

    if highest_severity == "Critical":
        return {
            "residual_risk": "Critical",
            "onboarding_gate": "Blocked",
            "recommended_treatment": (
                "Remediate before onboarding. Any exception requires "
                "executive risk acceptance."
            ),
            "human_decision_required": True,
        }

    if highest_severity == "High":
        return {
            "residual_risk": "High",
            "onboarding_gate": "Blocked pending accountable risk decision",
            "recommended_treatment": (
                "Remediate before onboarding or execute a time-bound risk "
                "acceptance with compensating controls and vendor commitments."
            ),
            "human_decision_required": True,
        }

    if highest_severity == "Moderate":
        return {
            "residual_risk": "Moderate",
            "onboarding_gate": "Conditional",
            "recommended_treatment": (
                "Track remediation with an accountable owner and approved "
                "target date."
            ),
            "human_decision_required": True,
        }

    if open_findings:
        return {
            "residual_risk": "Low",
            "onboarding_gate": "Standard approval",
            "recommended_treatment": "Track findings through normal governance.",
            "human_decision_required": True,
        }

    return {
        "residual_risk": "Low",
        "onboarding_gate": "Eligible for standard approval",
        "recommended_treatment": "Complete accountable human approval.",
        "human_decision_required": True,
    }


def build_vendor_report(vendor, all_findings):
    """Build the risk and remediation report for one vendor."""
    lifecycle = build_lifecycle_plan(vendor)
    vendor_findings = [
        finding
        for finding in all_findings
        if finding["vendor_id"] == vendor["vendor_id"]
    ]
    disposition = determine_risk_disposition(vendor_findings)
    severity_counts = Counter(
        finding["severity"]
        for finding in vendor_findings
        if finding["status"] == "Open"
    )

    return {
        "vendor_id": vendor["vendor_id"],
        "vendor_name": vendor["vendor_name"],
        "tier": lifecycle["tier"],
        "inherent_risk_score": lifecycle["inherent_risk_score"],
        "residual_risk": disposition["residual_risk"],
        "onboarding_gate": disposition["onboarding_gate"],
        "recommended_treatment": disposition["recommended_treatment"],
        "human_decision_required": disposition["human_decision_required"],
        "required_approval": lifecycle["required_approval"],
        "reassessment_frequency": lifecycle["reassessment_frequency"],
        "open_findings": len(
            [
                finding
                for finding in vendor_findings
                if finding["status"] == "Open"
            ]
        ),
        "high_findings": severity_counts["High"],
        "moderate_findings": severity_counts["Moderate"],
        "contract_dependencies": sum(
            finding["contract_dependency"]
            for finding in vendor_findings
            if finding["status"] == "Open"
        ),
        "findings": vendor_findings,
    }


def build_portfolio_report(vendors=None, findings=None):
    """Build leadership metrics and all vendor risk reports."""
    if vendors is None:
        vendors = load_vendors()

    if findings is None:
        findings = load_findings()

    vendor_reports = [
        build_vendor_report(vendor, findings)
        for vendor in vendors
    ]
    open_findings = [
        finding
        for finding in findings
        if finding["status"] == "Open"
    ]

    metrics = {
        "total_vendors": len(vendors),
        "critical_vendors": sum(
            report["tier"] == "Tier 1 - Critical"
            for report in vendor_reports
        ),
        "vendors_with_open_findings": sum(
            report["open_findings"] > 0
            for report in vendor_reports
        ),
        "open_findings": len(open_findings),
        "high_findings": sum(
            finding["severity"] == "High"
            for finding in open_findings
        ),
        "moderate_findings": sum(
            finding["severity"] == "Moderate"
            for finding in open_findings
        ),
        "contract_dependencies": sum(
            finding["contract_dependency"]
            for finding in open_findings
        ),
        "vendors_blocked": sum(
            report["onboarding_gate"].startswith("Blocked")
            for report in vendor_reports
        ),
    }

    return {
        "metrics": metrics,
        "vendor_reports": vendor_reports,
        "portfolio_posture": (
            "High"
            if metrics["high_findings"] > 0
            else "Moderate"
            if metrics["open_findings"] > 0
            else "Low"
        ),
        "decision_notice": (
            "All risk dispositions are recommendations. Approval, exception, "
            "and risk-acceptance decisions require accountable human owners."
        ),
    }


def render_portfolio_report(portfolio):
    """Render an employer-facing Markdown leadership report."""
    metrics = portfolio["metrics"]

    lines = [
        "# Third-Party Risk Portfolio Summary",
        "",
        "> Synthetic portfolio demonstration. No actual vendor or employer data is used.",
        "",
        "## Leadership Metrics",
        "",
        f"- Portfolio posture: **{portfolio['portfolio_posture']}**",
        f"- Total vendors: **{metrics['total_vendors']}**",
        f"- Tier 1 critical vendors: **{metrics['critical_vendors']}**",
        f"- Vendors with open findings: **{metrics['vendors_with_open_findings']}**",
        f"- Open findings: **{metrics['open_findings']}**",
        f"- High findings: **{metrics['high_findings']}**",
        f"- Moderate findings: **{metrics['moderate_findings']}**",
        f"- Contract-dependent findings: **{metrics['contract_dependencies']}**",
        f"- Vendors blocked from onboarding: **{metrics['vendors_blocked']}**",
        "",
        "## Vendor Risk Decisions",
        "",
    ]

    for report in portfolio["vendor_reports"]:
        lines.extend(
            [
                f"### {report['vendor_name']} ({report['vendor_id']})",
                "",
                f"- Tier: **{report['tier']}**",
                f"- Inherent-risk score: **{report['inherent_risk_score']}**",
                f"- Residual risk: **{report['residual_risk']}**",
                f"- Onboarding gate: **{report['onboarding_gate']}**",
                f"- Open findings: **{report['open_findings']}**",
                f"- Reassessment: **{report['reassessment_frequency']}**",
                f"- Treatment: {report['recommended_treatment']}",
                "",
            ]
        )

        for finding in report["findings"]:
            lines.extend(
                [
                    f"- **{finding['finding_id']} — {finding['title']} "
                    f"({finding['severity']})**",
                    f"  - Owner: {finding['owner']}",
                    f"  - Commitment: {finding['vendor_commitment']}",
                    f"  - Recommendation: {finding['recommendation']}",
                ]
            )

        lines.append("")

    lines.extend(
        [
            "## Governance Notice",
            "",
            portfolio["decision_notice"],
        ]
    )

    return "\n".join(lines)


def write_portfolio_report(path=DEFAULT_OUTPUT_PATH):
    """Generate and save the current synthetic portfolio report."""
    portfolio = build_portfolio_report()
    report = render_portfolio_report(portfolio)

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    return portfolio, output_path


if __name__ == "__main__":
    portfolio, output_path = write_portfolio_report()
    metrics = portfolio["metrics"]

    print(f"Portfolio posture: {portfolio['portfolio_posture']}")
    print(f"Total vendors: {metrics['total_vendors']}")
    print(f"Open findings: {metrics['open_findings']}")
    print(f"High findings: {metrics['high_findings']}")
    print(f"Vendors blocked: {metrics['vendors_blocked']}")
    print(f"Report written to: {output_path}")