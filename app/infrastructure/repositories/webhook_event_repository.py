from sqlalchemy.orm import Session

from app.infrastructure.models import ProcessedWebhookEvent


class WebhookEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_event_id(self, event_id: str) -> bool:
        return (
            self.db.query(ProcessedWebhookEvent)
            .filter(ProcessedWebhookEvent.event_id == event_id)
            .first()
            is not None
        )

    def create(self, *, event_id: str, card_id: str, cliente_email: str) -> ProcessedWebhookEvent:
        event = ProcessedWebhookEvent(
            event_id=event_id,
            card_id=card_id,
            cliente_email=cliente_email,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
