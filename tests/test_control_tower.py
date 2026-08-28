import unittest

from app import build_vendor_dossier, run_control_tower
from controls import build_control_baseline
from lifecycle import build_lifecycle_plan, validate_stage_order
from reporting import (
    build_portfolio_report,
    determine_risk_disposition,
    load_findings,
)
from tiering import (
    classify_vendor,
    load_vendors,
)


class TieringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vendors = load_vendors()
        cls.revenue_ai = cls.vendors[0]
        cls.core_cloud = cls.vendors[1]
        cls.training = cls.vendors[2]

    def test_three_synthetic_vendors_load(self):
        self.assertEqual(len(self.vendors), 3)

    def test_revenue_ai_is_tier_one(self):
        result = classify_vendor(self.revenue_ai)
        self.assertEqual(result["tier"], "Tier 1 - Critical")
        self.assertEqual(result["inherent_risk_score"], 35)

    def test_core_cloud_is_tier_one(self):
        result = classify_vendor(self.core_cloud)
        self.assertEqual(result["tier"], "Tier 1 - Critical")
        self.assertEqual(result["inherent_risk_score"], 38)

    def test_training_vendor_is_low_risk(self):
        result = classify_vendor(self.training)
        self.assertEqual(result["tier"], "Tier 4 - Low")
        self.assertEqual(result["inherent_risk_score"], 0)

    def test_ai_processing_triggers_governance_escalation(self):
        result = classify_vendor(self.revenue_ai)
        escalations = " ".join(result["mandatory_escalations"])
        self.assertIn("AI Governance", escalations)

    def test_privileged_access_triggers_iam_escalation(self):
        result = classify_vendor(self.core_cloud)
        escalations = " ".join(result["mandatory_escalations"])
        self.assertIn("Security Architecture and IAM", escalations)


class ControlBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vendors = load_vendors()

    def test_revenue_ai_baseline_contains_ai_privacy_and_iam(self):
        baseline = build_control_baseline(self.vendors[0])
        control_ids = {
            control["control_id"]
            for control in baseline["controls"]
        }

        self.assertIn("AI-01", control_ids)
        self.assertIn("PRIV-01", control_ids)
        self.assertIn("IAM-01", control_ids)

    def test_privileged_cloud_baseline_contains_pam(self):
        baseline = build_control_baseline(self.vendors[1])
        control_ids = {
            control["control_id"]
            for control in baseline["controls"]
        }
        self.assertIn("PAM-01", control_ids)

    def test_low_risk_vendor_receives_four_baseline_controls(self):
        baseline = build_control_baseline(self.vendors[2])
        self.assertEqual(baseline["control_count"], 4)


class LifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vendors = load_vendors()

    def test_lifecycle_contains_all_stages_in_order(self):
        plan = build_lifecycle_plan(self.vendors[0])
        self.assertTrue(validate_stage_order(plan))
        self.assertEqual(len(plan["stages"]), 9)

    def test_critical_vendor_receives_continuous_monitoring(self):
        plan = build_lifecycle_plan(self.vendors[0])
        self.assertEqual(
            plan["reassessment_frequency"],
            "Annual with continuous monitoring",
        )

    def test_low_risk_vendor_has_extended_reassessment(self):
        plan = build_lifecycle_plan(self.vendors[2])
        self.assertEqual(
            plan["reassessment_frequency"],
            "At material change or every three years",
        )


class ReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vendors = load_vendors()
        cls.findings = load_findings()

    def test_five_synthetic_findings_load(self):
        self.assertEqual(len(self.findings), 5)

    def test_portfolio_metrics_are_consistent(self):
        portfolio = build_portfolio_report(
            self.vendors,
            self.findings,
        )
        metrics = portfolio["metrics"]

        self.assertEqual(metrics["total_vendors"], 3)
        self.assertEqual(metrics["open_findings"], 5)
        self.assertEqual(metrics["high_findings"], 3)
        self.assertEqual(metrics["vendors_blocked"], 2)

    def test_high_finding_blocks_onboarding(self):
        vendor_findings = [
            finding
            for finding in self.findings
            if finding["vendor_id"] == "VND-001"
        ]
        disposition = determine_risk_disposition(vendor_findings)

        self.assertEqual(disposition["residual_risk"], "High")
        self.assertTrue(
            disposition["onboarding_gate"].startswith("Blocked")
        )

    def test_no_findings_allows_standard_approval_path(self):
        disposition = determine_risk_disposition([])

        self.assertEqual(disposition["residual_risk"], "Low")
        self.assertEqual(
            disposition["onboarding_gate"],
            "Eligible for standard approval",
        )
        self.assertTrue(disposition["human_decision_required"])


class IntegrationTests(unittest.TestCase):
    def test_control_tower_builds_three_consistent_dossiers(self):
        result = run_control_tower()

        self.assertEqual(result["vendor_count"], 3)
        self.assertEqual(len(result["dossiers"]), 3)
        self.assertTrue(result["human_approval_required"])

    def test_vendor_dossier_uses_consistent_tier(self):
        vendor = load_vendors()[0]
        findings = load_findings()
        dossier = build_vendor_dossier(vendor, findings)

        self.assertEqual(
            dossier["classification"]["tier"],
            dossier["baseline"]["tier"],
        )
        self.assertEqual(
            dossier["classification"]["tier"],
            dossier["lifecycle"]["tier"],
        )


if __name__ == "__main__":
    unittest.main()