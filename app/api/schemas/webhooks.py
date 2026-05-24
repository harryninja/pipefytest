from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class WebhookRequest(BaseModel):
    event_id: str = Field(min_length=1)
    card_id: str = Field(min_length=1)
    cliente_email: EmailStr
    timestamp: datetime


class WebhookResponse(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    status: str
    prioridade: str
    pipefy_updates: list[dict[str, Any]]
