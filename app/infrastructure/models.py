from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cliente_nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cliente_email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    tipo_solicitacao: Mapped[str] = mapped_column(String(255), nullable=False)
    valor_patrimonio: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=False)
    prioridade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pipefy_card_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProcessedWebhookEvent(Base):
    __tablename__ = "processed_webhook_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    card_id: Mapped[str] = mapped_column(String(100), nullable=False)
    cliente_email: Mapped[str] = mapped_column(String(255), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
