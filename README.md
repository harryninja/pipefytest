# Mundo Invest - Teste Tecnico Backend

API backend em Python para gerenciamento de clientes, persistencia local em SQLite e simulacao de integracao com Pipefy via GraphQL.

## Objetivo

Esta API implementa os dois fluxos pedidos no desafio:

- `POST /clientes` para criar o cliente no banco local e montar a mutation `createCard`.
- `POST /webhooks/pipefy/card-updated` para processar o webhook, aplicar a regra de prioridade e montar as mutations `updateCardField`.

Mesmo sem integrar com o Pipefy real, o codigo deixa pronta a estrutura GraphQL seguindo o formato oficial esperado pela documentacao publica do Pipefy.

## Tecnologias

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pytest

## Como executar localmente

1. Crie e ative um ambiente virtual.
2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Inicie a API:

```bash
uvicorn app.main:app --reload
```

4. Acesse a documentacao interativa:

- `http://127.0.0.1:8000/docs`

## Como rodar os testes

```bash
pytest
```

Resultado atual da suite:

- `5 passed`

## Estrutura do projeto

```text
app/
  api/
    routers/
      clients.py
      health.py
      webhooks.py
    schemas/
      clients.py
      webhooks.py
  application/
    use_cases/
      create_client.py
      process_pipefy_webhook.py
  core/
    database.py
  domain/
    constants.py
    exceptions.py
    rules/
      priority.py
  infrastructure/
    integrations/
      pipefy_client.py
    repositories/
      client_repository.py
      webhook_event_repository.py
    models.py
  main.py
tests/
  integration/
    test_api.py
  unit/
    test_priority.py
  conftest.py
README.md
VIDEO_DEFESA.md
requirements.txt
```

## Arquitetura em camadas

- `api`: camada HTTP com rotas e schemas de entrada e saida.
- `application`: casos de uso que orquestram o fluxo de negocio.
- `domain`: regras puras, constantes e excecoes de negocio.
- `infrastructure`: persistencia, repositorios e integracao simulada com Pipefy.
- `core`: configuracao compartilhada, como sessao e inicializacao do banco.

## Endpoints implementados

### POST /clientes

Responsabilidades:

- Validar os campos obrigatorios.
- Validar formato de e-mail.
- Persistir o cliente com status inicial `Aguardando Análise`.
- Montar o payload GraphQL da mutation `createCard`.

Exemplo:

```bash
curl --request POST http://127.0.0.1:8000/clientes \
  --header "Content-Type: application/json" \
  --data "{\"cliente_nome\":\"João Silva\",\"cliente_email\":\"joao.silva@example.com\",\"tipo_solicitacao\":\"Atualização cadastral\",\"valor_patrimonio\":250000}"
```

### POST /webhooks/pipefy/card-updated

Responsabilidades:

- Garantir idempotencia por `event_id`.
- Buscar o cliente pelo `cliente_email`.
- Aplicar a regra de prioridade com base no patrimonio.
- Atualizar o cliente para status `Processado`.
- Montar os payloads GraphQL da mutation `updateCardField`.

Exemplo:

```bash
curl --request POST http://127.0.0.1:8000/webhooks/pipefy/card-updated \
  --header "Content-Type: application/json" \
  --data "{\"event_id\":\"evt_123\",\"card_id\":\"card_456\",\"cliente_email\":\"joao.silva@example.com\",\"timestamp\":\"2026-05-18T12:00:00Z\"}"
```

## Regras de negocio implementadas

- Cadastro de cliente com unicidade por e-mail.
- Status inicial `Aguardando Análise` na criacao.
- Prioridade `prioridade_alta` quando `valor_patrimonio >= 200000`.
- Prioridade `prioridade_normal` quando `valor_patrimonio < 200000`.
- Idempotencia de webhook por `event_id`.
- Atualizacao do cliente para status `Processado` apos o webhook.

## Onde estao as mutations GraphQL

As duas mutations ficaram centralizadas em `app/infrastructure/integrations/pipefy_client.py`.

- `build_create_card_payload()` monta a mutation `createCard`.
- `build_update_card_payloads()` monta as mutations `updateCardField`.

Essa separacao facilita a manutencao e deixa explicito que a montagem do payload GraphQL faz parte da integracao com um sistema externo.

## Testes implementados

- Integracao de criacao de cliente com persistencia no banco.
- Integracao de processamento do webhook com prioridade alta.
- Integracao de bloqueio de `event_id` duplicado.
- Unidade para a regra isolada de prioridade.

## Arquivos de apoio para a defesa

- `README.md`: visao geral do projeto, execucao local, testes e arquitetura.
  
## Visao de producao na AWS

Uma evolucao natural desta solucao em producao poderia ser:

- `API Gateway` para expor os endpoints HTTP.
- `AWS Lambda` para executar os fluxos de criacao e webhook.
- `DynamoDB` para controle de idempotencia por `event_id`.
- `RDS PostgreSQL` para persistencia relacional dos clientes.
- `SQS` para desacoplar o recebimento do webhook do processamento.
- `CloudWatch` para logs, metricas e alarmes.
- `Secrets Manager` para tokens e configuracoes sensiveis.

Essa arquitetura mantem a mesma regra de negocio implementada localmente, mas melhora escalabilidade, tolerancia a falhas e observabilidade.
