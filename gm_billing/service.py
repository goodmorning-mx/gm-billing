from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
from uuid import uuid4

from .models import LedgerEntry, PricingRule, UsageRecord


class InMemoryBillingStore:
    """Reference store for tests and local development.

    Production products can implement the same small persistence boundary with
    PostgreSQL/SQLAlchemy without changing the metering service.
    """

    def __init__(self) -> None:
        self.usage: list[UsageRecord] = []
        self.ledger: list[LedgerEntry] = []

    def add_usage(self, record: UsageRecord) -> UsageRecord:
        self.usage.append(record)
        return record

    def add_ledger(self, entry: LedgerEntry) -> LedgerEntry:
        self.ledger.append(entry)
        return entry


class BillingService:
    def __init__(self, store: InMemoryBillingStore, pricing: list[PricingRule]) -> None:
        self.store = store
        self.pricing = {(rule.provider, rule.model): rule for rule in pricing}

    def record_usage(
        self, *, product_id: str, organization_id: str, user_id: str, provider: str,
        model: str, input_tokens: int, output_tokens: int, cached_tokens: int = 0,
        request_id: str | None = None,
    ) -> UsageRecord:
        rule = self.pricing.get((provider, model))
        if rule is None:
            raise ValueError(f"No pricing rule for {provider}/{model}")
        provider_cost, charge = rule.calculate(input_tokens=input_tokens, output_tokens=output_tokens, cached_tokens=cached_tokens)
        usage = UsageRecord(str(uuid4()), product_id, organization_id, user_id, provider, model, input_tokens, output_tokens, cached_tokens, request_id, provider_cost=provider_cost, goodmorning_charge=charge)
        self.store.add_usage(usage)
        self.store.add_ledger(LedgerEntry(str(uuid4()), product_id, organization_id, user_id, usage.id, charge))
        return usage

    def summary(self, *, organization_id: str, product_id: str | None = None) -> dict[str, Decimal | int | str]:
        records = [r for r in self.store.usage if r.organization_id == organization_id and (product_id is None or r.product_id == product_id)]
        return {
            "organization_id": organization_id,
            "product_id": product_id or "*",
            "requests": len(records),
            "input_tokens": sum(r.input_tokens for r in records),
            "output_tokens": sum(r.output_tokens for r in records),
            "cached_tokens": sum(r.cached_tokens for r in records),
            "provider_cost": sum((r.provider_cost for r in records), Decimal("0")),
            "goodmorning_charge": sum((r.goodmorning_charge for r in records), Decimal("0")),
        }
