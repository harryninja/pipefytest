from app.domain.constants import STATUS_AGUARDANDO_ANALISE
from app.domain.exceptions import ClientAlreadyExistsError
from app.infrastructure.integrations.pipefy_client import PipefyClientSimulator
from app.infrastructure.repositories.client_repository import ClientRepository


class CreateClientUseCase:
    def __init__(self, client_repository: ClientRepository, pipefy_client: PipefyClientSimulator):
        self.client_repository = client_repository
        self.pipefy_client = pipefy_client

    def execute(
        self,
        *,
        cliente_nome: str,
        cliente_email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float,
    ) -> tuple[object, dict]:
        existing_client = self.client_repository.get_by_email(cliente_email)
        if existing_client:
            raise ClientAlreadyExistsError("Ja existe um cliente cadastrado com este e-mail.")

        client = self.client_repository.create(
            cliente_nome=cliente_nome,
            cliente_email=cliente_email,
            tipo_solicitacao=tipo_solicitacao,
            valor_patrimonio=valor_patrimonio,
            status=STATUS_AGUARDANDO_ANALISE,
        )
        pipefy_request = self.pipefy_client.build_create_card_payload(
            cliente_nome=client.cliente_nome,
            cliente_email=client.cliente_email,
            tipo_solicitacao=client.tipo_solicitacao,
            valor_patrimonio=client.valor_patrimonio,
        )
        return client, pipefy_request
