import unittest
from decimal import Decimal

from gm_billing import BillingService, InMemoryBillingStore, PricingRule


class BillingTests(unittest.TestCase):
    def setUp(self):
        self.store = InMemoryBillingStore()
        self.service = BillingService(self.store, [PricingRule("openai", "gpt-4o-mini", Decimal("0.15"), Decimal("0.60"), Decimal("0.075"), Decimal("1.2"))])

    def test_records_usage_and_ledger_charge(self):
        usage = self.service.record_usage(product_id="academy", organization_id="org", user_id="user", provider="openai", model="gpt-4o-mini", input_tokens=1000, output_tokens=500, cached_tokens=200, request_id="req")
        self.assertEqual(usage.provider_cost, Decimal("0.00043500"))
        self.assertEqual(usage.goodmorning_charge, Decimal("0.00052200"))
        self.assertEqual(len(self.store.ledger), 1)

    def test_summary_is_scoped(self):
        self.service.record_usage(product_id="academy", organization_id="org", user_id="u", provider="openai", model="gpt-4o-mini", input_tokens=1, output_tokens=2)
        self.service.record_usage(product_id="other", organization_id="org", user_id="u", provider="openai", model="gpt-4o-mini", input_tokens=3, output_tokens=4)
        self.assertEqual(self.service.summary(organization_id="org", product_id="academy")["requests"], 1)
        self.assertEqual(self.service.summary(organization_id="org")["requests"], 2)
