from app.domain.constants import STATUS_PROCESSADO
from app.domain.exceptions import ClientNotFoundError, WebhookAlreadyProcessedError
from app.domain.rules.priority import calculate_priority
from app.infrastructure.integrations.pipefy_client import PipefyClientSimulator
from app.infrastructure.repositories.client_repository import ClientRepository
from app.infrastructure.repositories.webhook_event_repository import WebhookEventRepository


class ProcessPipefyWebhookUseCase:
    def __init__(
        self,
        client_repository: ClientRepository,
        webhook_event_repository: WebhookEventRepository,
        pipefy_client: PipefyClientSimulator,
    ):
        self.client_repository = client_repository
        self.webhook_event_repository = webhook_event_repository
        self.pipefy_client = pipefy_client

    def execute(self, *, event_id: str, card_id: str, cliente_email: str) -> tuple[object, list[dict]]:
        if self.webhook_event_repository.exists_by_event_id(event_id):
            raise WebhookAlreadyProcessedError("Evento ja processado anteriormente.")

        client = self.client_repository.get_by_email(cliente_email)
        if not client:
            raise ClientNotFoundError("Cliente nao encontrado para o e-mail informado.")

        prioridade = calculate_priority(client.valor_patrimonio)
        pipefy_updates = self.pipefy_client.build_update_card_payloads(
            card_id=card_id,
            status=STATUS_PROCESSADO,
            prioridade=prioridade,
        )
        self.webhook_event_repository.create(
            event_id=event_id,
            card_id=card_id,
            cliente_email=cliente_email,
        )
        client = self.client_repository.update_after_webhook(
            client,
            status=STATUS_PROCESSADO,
            prioridade=prioridade,
            card_id=card_id,
        )
        return client, pipefy_updates
