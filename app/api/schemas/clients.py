from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientCreateRequest(BaseModel):
    cliente_nome: str = Field(min_length=1)
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(min_length=1)
    valor_patrimonio: float = Field(ge=0)


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str | None = None
    pipefy_request: dict[str, Any]
