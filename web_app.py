import json
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


st.set_page_config(
    page_title="Enterprise TPRM Lifecycle Control Tower",
    page_icon="🛡️",
    layout="wide",
)


def load_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def extract_records(data, possible_keys):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in possible_keys:
            records = data.get(key)
            if isinstance(records, list):
                return records

    return []


def value(record, *keys, default="Not specified"):
    for key in keys:
        if key in record and record[key] not in (None, ""):
            return record[key]
    return default


def display_value(item):
    if isinstance(item, bool):
        return "Yes" if item else "No"
    if isinstance(item, list):
        return ", ".join(str(value) for value in item) or "None"
    if isinstance(item, dict):
        return ", ".join(
            f"{key.replace('_', ' ').title()}: {display_value(value)}"
            for key, value in item.items()
        )
    return str(item)


vendor_data = load_json("vendor_scenarios.json")
finding_data = load_json("vendor_findings.json")

vendors = extract_records(
    vendor_data,
    ["vendors", "vendor_scenarios", "scenarios"],
)
findings = extract_records(
    finding_data,
    ["findings", "vendor_findings"],
)

if not vendors:
    st.error("No synthetic vendor scenarios were found.")
    st.stop()


st.title("Enterprise TPRM Lifecycle Control Tower")

st.caption(
    "A risk-based third-party governance demonstration covering intake, "
    "tiering, due diligence, contracting, remediation, continuous monitoring, "
    "reassessment, and offboarding."
)

st.warning(
    "Portfolio demonstration: all vendors and findings are fictional. "
    "Do not enter or upload confidential, personal, or production information."
)

with st.sidebar:
    st.header("Governance boundary")

    st.write(
        "This control tower supports risk analysis and decision preparation. "
        "It does not approve vendors, accept risk, or replace accountable "
        "Security, Privacy, Legal, Procurement, or business-owner decisions."
    )

    st.info(
        "High-risk findings remain subject to documented remediation, "
        "contractual commitments, compensating controls, or formal risk "
        "acceptance."
    )

    st.header("Program principles")

    st.markdown(
        """
        - Risk-based review depth
        - Transparent tiering
        - Evidence-driven decisions
        - Contractual accountability
        - Continuous monitoring
        - Human approval gates
        """
    )


vendor_ids = {
    value(vendor, "vendor_name", "name", default=f"Vendor {index + 1}"):
    value(vendor, "vendor_id", "id", default=str(index))
    for index, vendor in enumerate(vendors)
}

open_findings = [
    finding
    for finding in findings
    if str(value(finding, "status", default="Open")).lower()
    not in {"closed", "remediated", "resolved"}
]

high_findings = [
    finding
    for finding in open_findings
    if str(value(finding, "severity", "risk_rating", default="")).lower()
    in {"high", "critical"}
]

blocked_vendor_ids = {
    str(value(finding, "vendor_id", default=""))
    for finding in high_findings
}

tab_overview, tab_vendor, tab_lifecycle, tab_remediation, tab_reports = st.tabs(
    [
        "Portfolio Overview",
        "Vendor Dossier",
        "Lifecycle and Controls",
        "Remediation Tracker",
        "Generated Reports",
    ]
)


with tab_overview:
    st.subheader("Portfolio risk posture")

    metric_one, metric_two, metric_three, metric_four = st.columns(4)

    metric_one.metric("Vendors", len(vendors))
    metric_two.metric("Open findings", len(open_findings))
    metric_three.metric("High findings", len(high_findings))
    metric_four.metric(
        "Blocked vendors",
        len(blocked_vendor_ids - {""}),
    )

    if high_findings:
        st.error(
            "Portfolio posture: High — one or more vendors have material "
            "findings requiring accountable human decisions."
        )
    elif open_findings:
        st.warning(
            "Portfolio posture: Moderate — open findings require tracking "
            "and validation."
        )
    else:
        st.success(
            "Portfolio posture: Low — no open findings are recorded in the "
            "current synthetic dataset."
        )

    portfolio_rows = []

    for vendor in vendors:
        vendor_id = str(value(vendor, "vendor_id", "id", default=""))
        vendor_findings = [
            finding
            for finding in open_findings
            if str(value(finding, "vendor_id", default="")) == vendor_id
        ]

        portfolio_rows.append(
            {
                "Vendor": value(vendor, "vendor_name", "name"),
                "Service": value(
                    vendor,
                    "service",
                    "service_description",
                    "service_category",
                ),
                "Criticality": value(
                    vendor,
                    "business_criticality",
                    "criticality",
                ),
                "Open Findings": len(vendor_findings),
                "Onboarding Gate": (
                    "Blocked pending decision"
                    if vendor_id in blocked_vendor_ids
                    else "Standard approval path"
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(portfolio_rows),
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "The onboarding gate is a workflow indicator—not an automated vendor "
        "approval or risk-acceptance decision."
    )


with tab_vendor:
    st.subheader("Vendor risk dossier")

    selected_name = st.selectbox(
        "Select a fictional vendor",
        list(vendor_ids.keys()),
    )

    selected_id = str(vendor_ids[selected_name])

    selected_vendor = next(
        vendor
        for vendor in vendors
        if str(value(vendor, "vendor_id", "id", default="")) == selected_id
    )

    selected_findings = [
        finding
        for finding in findings
        if str(value(finding, "vendor_id", default="")) == selected_id
    ]

    vendor_column, decision_column = st.columns([2, 1])

    with vendor_column:
        st.markdown(f"### {selected_name}")

        detail_rows = []

        for key, item in selected_vendor.items():
            detail_rows.append(
                {
                    "Attribute": key.replace("_", " ").title(),
                    "Value": display_value(item),
                }
            )

        st.dataframe(
            pd.DataFrame(detail_rows),
            width="stretch",
            hide_index=True,
        )

    with decision_column:
        st.markdown("### Decision gate")

        if selected_id in blocked_vendor_ids:
            st.error("Blocked pending accountable risk decision")
            st.write(
                "Complete remediation, establish approved compensating "
                "controls, or document formal risk acceptance before onboarding."
            )
        else:
            st.success("Standard approval path")
            st.write(
                "Complete required review and obtain the designated human "
                "approvals before onboarding."
            )

        st.metric("Recorded findings", len(selected_findings))

    st.markdown("### Findings")

    if not selected_findings:
        st.success("No findings are recorded for this synthetic vendor.")
    else:
        for number, finding in enumerate(selected_findings, start=1):
            title = value(
                finding,
                "title",
                "finding_title",
                default=f"Finding {number}",
            )
            severity = value(
                finding,
                "severity",
                "risk_rating",
                default="Not rated",
            )

            with st.expander(
                f"{number}. {title} — {severity}",
                expanded=number == 1,
            ):
                for key, item in finding.items():
                    st.write(
                        f"**{key.replace('_', ' ').title()}:** "
                        f"{display_value(item)}"
                    )


with tab_lifecycle:
    st.subheader("End-to-end third-party lifecycle")

    lifecycle_stages = [
        {
            "Stage": "1. Intake",
            "Required outcome": "Defined service, owner, data, access, and criticality",
            "Decision owner": "Business and Procurement",
        },
        {
            "Stage": "2. Tiering",
            "Required outcome": "Transparent inherent-risk classification",
            "Decision owner": "TPRM",
        },
        {
            "Stage": "3. Due Diligence",
            "Required outcome": "Evidence review scaled to inherent risk",
            "Decision owner": "Security, Privacy, and TPRM",
        },
        {
            "Stage": "4. Risk Decision",
            "Required outcome": "Documented findings and accountable disposition",
            "Decision owner": "Risk owner and control stakeholders",
        },
        {
            "Stage": "5. Contracting",
            "Required outcome": "Security, privacy, resilience, and remedy obligations",
            "Decision owner": "Legal and Procurement",
        },
        {
            "Stage": "6. Onboarding",
            "Required outcome": "Approval gates completed before production use",
            "Decision owner": "Business and designated approvers",
        },
        {
            "Stage": "7. Continuous Monitoring",
            "Required outcome": "Material changes and external signals evaluated",
            "Decision owner": "TPRM and Security",
        },
        {
            "Stage": "8. Reassessment",
            "Required outcome": "Risk-tier-based periodic review",
            "Decision owner": "TPRM",
        },
        {
            "Stage": "9. Offboarding",
            "Required outcome": "Access removed, data returned or destroyed",
            "Decision owner": "Business, IT, Privacy, and Procurement",
        },
    ]

    st.dataframe(
        pd.DataFrame(lifecycle_stages),
        width="stretch",
        hide_index=True,
    )

    st.markdown("### Scalable review model")

    st.markdown(
        """
        - **Tier 1 – Critical:** Comprehensive due diligence, annual
          reassessment, continuous monitoring, and multi-function approval.
        - **Tier 2 – High:** Enhanced evidence review and scheduled
          reassessment.
        - **Tier 3 – Moderate:** Targeted control validation proportional to
          access and data exposure.
        - **Tier 4 – Low:** Baseline review with reassessment after material
          change or at the defined low-risk interval.
        """
    )

    st.info(
        "Due diligence must be completed before the onboarding decision. "
        "Automation may route and summarize evidence, but accountable people "
        "retain approval and risk-acceptance authority."
    )


with tab_remediation:
    st.subheader("Remediation and contractual commitments")

    if not findings:
        st.success("No findings are recorded.")
    else:
        remediation_rows = []

        for finding in findings:
            vendor_id = str(value(finding, "vendor_id", default=""))
            vendor_name = next(
                (
                    value(vendor, "vendor_name", "name")
                    for vendor in vendors
                    if str(value(vendor, "vendor_id", "id", default=""))
                    == vendor_id
                ),
                vendor_id,
            )

            remediation_rows.append(
                {
                    "Vendor": vendor_name,
                    "Finding": value(
                        finding,
                        "title",
                        "finding_title",
                    ),
                    "Severity": value(
                        finding,
                        "severity",
                        "risk_rating",
                    ),
                    "Status": value(finding, "status", default="Open"),
                    "Target": value(
                        finding,
                        "target",
                        "target_date",
                        "remediation_timeline",
                        "due_date",
                    ),
                    "Contract Dependent": display_value(
                        value(
                            finding,
                            "contract_dependent",
                            default="Not specified",
                        )
                    ),
                }
            )

        remediation_frame = pd.DataFrame(remediation_rows)

        severity_filter = st.multiselect(
            "Filter by severity",
            sorted(remediation_frame["Severity"].astype(str).unique()),
            default=sorted(
                remediation_frame["Severity"].astype(str).unique()
            ),
        )

        filtered_frame = remediation_frame[
            remediation_frame["Severity"].astype(str).isin(severity_filter)
        ]

        st.dataframe(
            filtered_frame,
            use_container_width=True,
            hide_index=True,
        )

        st.warning(
            "A contractual commitment does not close a finding. Risk remains "
            "open until implementation evidence is received, validated, and "
            "formally recorded."
        )


with tab_reports:
    st.subheader("Generated governance artifacts")

    report_files = sorted(OUTPUT_DIR.glob("*.md"))

    if not report_files:
        st.warning("Run `python app.py` to generate the Markdown reports.")
    else:
        selected_report = st.selectbox(
            "Select a generated report",
            report_files,
            format_func=lambda path: path.name,
        )

        report_text = selected_report.read_text(encoding="utf-8")

        st.download_button(
            "Download selected report",
            data=report_text,
            file_name=selected_report.name,
            mime="text/markdown",
        )

        st.markdown(report_text)


st.divider()

st.caption(
    "Synthetic portfolio demonstration. Outputs support analysis and "
    "workflow governance; they do not constitute vendor approval, legal "
    "advice, audit assurance, or risk acceptance."
)