import json
from pathlib import Path


DEFAULT_VENDOR_PATH = Path("data/vendor_scenarios.json")

VALUE_WEIGHTS = {
    "business_criticality": {
        "Low": 0,
        "Moderate": 2,
        "High": 4,
        "Critical": 6,
    },
    "data_sensitivity": {
        "Public": 0,
        "Internal": 1,
        "Confidential": 3,
        "Restricted": 5,
    },
    "operational_dependency": {
        "Low": 0,
        "Moderate": 2,
        "High": 4,
        "Critical": 6,
    },
    "replacement_difficulty": {
        "Low": 0,
        "Moderate": 1,
        "High": 3,
    },
    "geographic_scope": {
        "Domestic": 0,
        "Regional": 1,
        "Global": 1,
    },
}

BOOLEAN_WEIGHTS = {
    "personal_information": 2,
    "regulated_data": 3,
    "confidential_business_data": 2,
    "customer_content": 3,
    "production_access": 3,
    "privileged_access": 4,
    "api_integration": 2,
    "subprocessors_used": 1,
    "artificial_intelligence": 1,
    "generative_ai": 2,
    "model_training_on_customer_data": 3,
    "internet_facing": 2,
}

TIER_DEFINITIONS = {
    "Tier 1 - Critical": {
        "minimum_score": 20,
        "review_depth": "Enhanced",
        "reassessment_frequency": "Annual with continuous monitoring",
        "approval": "Security, Privacy, Legal, Procurement, and business owner",
    },
    "Tier 2 - High": {
        "minimum_score": 12,
        "review_depth": "Full",
        "reassessment_frequency": "Annual",
        "approval": "Security, Procurement, and business owner",
    },
    "Tier 3 - Moderate": {
        "minimum_score": 6,
        "review_depth": "Targeted",
        "reassessment_frequency": "Every two years",
        "approval": "Security or delegated risk owner",
    },
    "Tier 4 - Low": {
        "minimum_score": 0,
        "review_depth": "Baseline",
        "reassessment_frequency": "At material change or every three years",
        "approval": "Business owner with automated controls",
    },
}


def load_vendors(path=DEFAULT_VENDOR_PATH):
    """Load the synthetic vendor-intake scenarios."""
    vendor_path = Path(path)

    with vendor_path.open(encoding="utf-8") as vendor_file:
        vendors = json.load(vendor_file)

    if not isinstance(vendors, list):
        raise ValueError("Vendor data must contain a JSON list.")

    required_fields = {
        "vendor_id",
        "vendor_name",
        "service_description",
        "business_criticality",
        "data_sensitivity",
        "operational_dependency",
        "replacement_difficulty",
    }

    for vendor in vendors:
        missing_fields = required_fields.difference(vendor)

        if missing_fields:
            raise ValueError(
                f"{vendor.get('vendor_id', 'Unknown vendor')} is missing "
                f"required fields: {sorted(missing_fields)}"
            )

    return vendors


def calculate_inherent_risk(vendor):
    """Calculate a transparent inherent-risk score with traceable factors."""
    score = 0
    factors = []

    for field, weights in VALUE_WEIGHTS.items():
        value = vendor.get(field)
        points = weights.get(value, 0)

        if points:
            score += points
            factors.append(
                {
                    "factor": field,
                    "value": value,
                    "points": points,
                }
            )

    for field, points in BOOLEAN_WEIGHTS.items():
        if vendor.get(field, False):
            score += points
            factors.append(
                {
                    "factor": field,
                    "value": True,
                    "points": points,
                }
            )

    return score, factors


def determine_tier(score):
    """Map the inherent-risk score to a vendor tier."""
    for tier_name, definition in TIER_DEFINITIONS.items():
        if score >= definition["minimum_score"]:
            return tier_name, definition

    raise ValueError("Unable to determine vendor tier.")


def identify_mandatory_escalations(vendor):
    """Flag conditions that require specialist or leadership review."""
    escalations = []

    if vendor.get("regulated_data"):
        escalations.append(
            "Privacy and Compliance review required for regulated data."
        )

    if vendor.get("privileged_access"):
        escalations.append(
            "Security Architecture and IAM review required for privileged access."
        )

    if vendor.get("generative_ai") and vendor.get("customer_content"):
        escalations.append(
            "AI Governance review required because generative AI processes "
            "customer content."
        )

    if vendor.get("model_training_on_customer_data"):
        escalations.append(
            "Executive Privacy and Legal review required before customer data "
            "may be used for model training."
        )

    if vendor.get("business_criticality") == "Critical":
        escalations.append(
            "Operational Resilience review required for a critical service."
        )

    return escalations


def classify_vendor(vendor):
    """Return the complete, explainable risk-tiering decision."""
    score, factors = calculate_inherent_risk(vendor)
    tier, definition = determine_tier(score)

    return {
        "vendor_id": vendor["vendor_id"],
        "vendor_name": vendor["vendor_name"],
        "inherent_risk_score": score,
        "tier": tier,
        "review_depth": definition["review_depth"],
        "reassessment_frequency": definition["reassessment_frequency"],
        "required_approval": definition["approval"],
        "risk_factors": factors,
        "mandatory_escalations": identify_mandatory_escalations(vendor),
        "decision_status": "Preliminary - human validation required",
    }


def classify_portfolio(vendors=None):
    """Classify every vendor in the synthetic portfolio."""
    if vendors is None:
        vendors = load_vendors()

    return [classify_vendor(vendor) for vendor in vendors]


if __name__ == "__main__":
    for result in classify_portfolio():
        print(
            f"{result['vendor_id']} | {result['vendor_name']} | "
            f"Score: {result['inherent_risk_score']} | {result['tier']}"
        )

        for escalation in result["mandatory_escalations"]:
            print(f"  Escalation: {escalation}")