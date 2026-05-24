from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.clients import ClientCreateRequest, ClientResponse
from app.application.use_cases.create_client import CreateClientUseCase
from app.core.database import get_db
from app.domain.exceptions import ClientAlreadyExistsError
from app.infrastructure.integrations.pipefy_client import PipefyClientSimulator
from app.infrastructure.repositories.client_repository import ClientRepository

router = APIRouter(tags=["clientes"])


@router.post("/clientes", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client_endpoint(
    payload: ClientCreateRequest,
    db: Session = Depends(get_db),
) -> ClientResponse:
    use_case = CreateClientUseCase(
        client_repository=ClientRepository(db),
        pipefy_client=PipefyClientSimulator(),
    )
    try:
        client, pipefy_request = use_case.execute(
            cliente_nome=payload.cliente_nome,
            cliente_email=str(payload.cliente_email),
            tipo_solicitacao=payload.tipo_solicitacao,
            valor_patrimonio=payload.valor_patrimonio,
        )
    except ClientAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ClientResponse.model_validate(
        {
            "id": client.id,
            "cliente_nome": client.cliente_nome,
            "cliente_email": client.cliente_email,
            "tipo_solicitacao": client.tipo_solicitacao,
            "valor_patrimonio": client.valor_patrimonio,
            "status": client.status,
            "prioridade": client.prioridade,
            "pipefy_request": pipefy_request,
        }
    )
