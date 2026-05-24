from app.infrastructure.models import Client, ProcessedWebhookEvent


def test_create_client_with_valid_payload_and_persist_in_database(client, db_session):
    payload = {
        "cliente_nome": "Joao Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualizacao cadastral",
        "valor_patrimonio": 250000,
    }

    response = client.post("/clientes", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "Aguardando Análise"
    assert data["pipefy_request"]["variables"]["clienteNome"] == payload["cliente_nome"]
    assert data["pipefy_request"]["variables"]["clienteEmail"] == payload["cliente_email"]
    assert data["pipefy_request"]["variables"]["valorPatrimonio"] == "250000.00"

    saved_client = (
        db_session.query(Client)
        .filter(Client.cliente_email == payload["cliente_email"])
        .first()
    )
    assert saved_client is not None
    assert saved_client.status == "Aguardando Análise"


def test_process_webhook_applies_high_priority_rule(client, db_session):
    client.post(
        "/clientes",
        json={
            "cliente_nome": "Joao Silva",
            "cliente_email": "joao.silva@example.com",
            "tipo_solicitacao": "Atualizacao cadastral",
            "valor_patrimonio": 250000,
        },
    )

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_123",
            "card_id": "card_456",
            "cliente_email": "joao.silva@example.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Processado"
    assert data["prioridade"] == "prioridade_alta"
    assert len(data["pipefy_updates"]) == 2
    assert data["pipefy_updates"][0]["variables"]["newValue"] == ["Processado"]
    assert data["pipefy_updates"][1]["variables"]["newValue"] == ["prioridade_alta"]

    saved_client = (
        db_session.query(Client)
        .filter(Client.cliente_email == "joao.silva@example.com")
        .first()
    )
    assert saved_client is not None
    assert saved_client.status == "Processado"
    assert saved_client.prioridade == "prioridade_alta"


def test_process_webhook_blocks_duplicate_event_id(client, db_session):
    client.post(
        "/clientes",
        json={
            "cliente_nome": "Maria Souza",
            "cliente_email": "maria.souza@example.com",
            "tipo_solicitacao": "Atualizacao cadastral",
            "valor_patrimonio": 150000,
        },
    )

    webhook_payload = {
        "event_id": "evt_duplicate",
        "card_id": "card_789",
        "cliente_email": "maria.souza@example.com",
        "timestamp": "2026-05-18T12:00:00Z",
    }

    first_response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    second_response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Evento ja processado anteriormente."

    processed_events = (
        db_session.query(ProcessedWebhookEvent)
        .filter(ProcessedWebhookEvent.event_id == webhook_payload["event_id"])
        .all()
    )
    assert len(processed_events) == 1

    saved_client = (
        db_session.query(Client)
        .filter(Client.cliente_email == webhook_payload["cliente_email"])
        .first()
    )
    assert saved_client is not None
    assert saved_client.prioridade == "prioridade_normal"
