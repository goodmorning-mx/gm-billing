from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class UsageRecord:
    id: str
    product_id: str
    organization_id: str
    user_id: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int = 0
    request_id: str | None = None
    created_at: datetime = None  # type: ignore[assignment]
    provider_cost: Decimal = Decimal("0")
    goodmorning_charge: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if self.created_at is None:
            object.__setattr__(self, "created_at", utcnow())
        for value in (self.input_tokens, self.output_tokens, self.cached_tokens):
            if value < 0:
                raise ValueError("Token counts cannot be negative")


@dataclass(frozen=True, slots=True)
class PricingRule:
    provider: str
    model: str
    input_per_million: Decimal
    output_per_million: Decimal
    cached_input_per_million: Decimal = Decimal("0")
    markup: Decimal = Decimal("1")

    def calculate(self, *, input_tokens: int, output_tokens: int, cached_tokens: int) -> tuple[Decimal, Decimal]:
        cost = (
            Decimal(input_tokens - cached_tokens) * self.input_per_million
            + Decimal(cached_tokens) * self.cached_input_per_million
            + Decimal(output_tokens) * self.output_per_million
        ) / Decimal(1_000_000)
        return cost.quantize(Decimal("0.00000001")), (cost * self.markup).quantize(Decimal("0.00000001"))


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    id: str
    product_id: str
    organization_id: str
    user_id: str
    usage_id: str
    amount: Decimal
    currency: str = "USD"
    entry_type: str = "usage_charge"
    created_at: datetime = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.created_at is None:
            object.__setattr__(self, "created_at", utcnow())
