from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.webhooks import WebhookRequest, WebhookResponse
from app.application.use_cases.process_pipefy_webhook import ProcessPipefyWebhookUseCase
from app.core.database import get_db
from app.domain.exceptions import ClientNotFoundError, WebhookAlreadyProcessedError
from app.infrastructure.integrations.pipefy_client import PipefyClientSimulator
from app.infrastructure.repositories.client_repository import ClientRepository
from app.infrastructure.repositories.webhook_event_repository import WebhookEventRepository

router = APIRouter(tags=["webhooks"])


@router.post(
    "/webhooks/pipefy/card-updated",
    response_model=WebhookResponse,
    status_code=status.HTTP_200_OK,
)
def process_pipefy_webhook_endpoint(
    payload: WebhookRequest,
    db: Session = Depends(get_db),
) -> WebhookResponse:
    use_case = ProcessPipefyWebhookUseCase(
        client_repository=ClientRepository(db),
        webhook_event_repository=WebhookEventRepository(db),
        pipefy_client=PipefyClientSimulator(),
    )
    try:
        client, pipefy_updates = use_case.execute(
            event_id=payload.event_id,
            card_id=payload.card_id,
            cliente_email=str(payload.cliente_email),
        )
    except WebhookAlreadyProcessedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ClientNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return WebhookResponse(
        event_id=payload.event_id,
        card_id=payload.card_id,
        cliente_email=payload.cliente_email,
        status=client.status,
        prioridade=client.prioridade or "",
        pipefy_updates=pipefy_updates,
    )
