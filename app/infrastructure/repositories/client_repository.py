from sqlalchemy.orm import Session

from app.infrastructure.models import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, cliente_email: str) -> Client | None:
        return self.db.query(Client).filter(Client.cliente_email == cliente_email).first()

    def create(
        self,
        *,
        cliente_nome: str,
        cliente_email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float,
        status: str,
    ) -> Client:
        client = Client(
            cliente_nome=cliente_nome,
            cliente_email=cliente_email,
            tipo_solicitacao=tipo_solicitacao,
            valor_patrimonio=valor_patrimonio,
            status=status,
        )
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update_after_webhook(self, client: Client, *, status: str, prioridade: str, card_id: str) -> Client:
        client.status = status
        client.prioridade = prioridade
        client.pipefy_card_id = card_id
        self.db.commit()
        self.db.refresh(client)
        return client
