from __future__ import annotations

from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .models import PricingRule
from .service import BillingService, InMemoryBillingStore


class UsageInput(BaseModel):
    product_id: str
    organization_id: str
    user_id: str
    provider: str
    model: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_tokens: int = Field(default=0, ge=0)
    request_id: str | None = None


def create_app(service: BillingService | None = None) -> FastAPI:
    service = service or BillingService(InMemoryBillingStore(), [])
    app = FastAPI(title="gm-billing", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/usage")
    async def usage(payload: UsageInput) -> dict[str, object]:
        try:
            result = service.record_usage(**payload.model_dump())
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {"id": result.id, "providerCost": str(result.provider_cost), "goodmorningCharge": str(result.goodmorning_charge)}

    @app.get("/usage/summary")
    async def summary(organization_id: str, product_id: str | None = None) -> dict[str, object]:
        return {key: (str(value) if isinstance(value, Decimal) else value) for key, value in service.summary(organization_id=organization_id, product_id=product_id).items()}

    return app
