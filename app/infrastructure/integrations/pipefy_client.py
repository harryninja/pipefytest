PIPEFY_PIPE_ID = "123456789"
PIPEFY_FIELDS = {
    "cliente_nome": "cliente_nome",
    "cliente_email": "cliente_email",
    "tipo_solicitacao": "tipo_solicitacao",
    "valor_patrimonio": "valor_patrimonio",
    "status": "status",
    "prioridade": "prioridade",
}


class PipefyClientSimulator:
    def build_create_card_payload(
        self,
        *,
        cliente_nome: str,
        cliente_email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float,
    ) -> dict:
        query = f"""
mutation CreateCard(
  $pipeId: ID!,
  $clienteNome: String!,
  $clienteEmail: String!,
  $tipoSolicitacao: String!,
  $valorPatrimonio: String!
) {{
  createCard(
    input: {{
      pipe_id: $pipeId
      fields_attributes: [
        {{ field_id: "{PIPEFY_FIELDS["cliente_nome"]}", field_value: $clienteNome }}
        {{ field_id: "{PIPEFY_FIELDS["cliente_email"]}", field_value: $clienteEmail }}
        {{ field_id: "{PIPEFY_FIELDS["tipo_solicitacao"]}", field_value: $tipoSolicitacao }}
        {{ field_id: "{PIPEFY_FIELDS["valor_patrimonio"]}", field_value: $valorPatrimonio }}
      ]
    }}
  ) {{
    card {{
      id
    }}
  }}
}}
""".strip()

        variables = {
            "pipeId": PIPEFY_PIPE_ID,
            "clienteNome": cliente_nome,
            "clienteEmail": cliente_email,
            "tipoSolicitacao": tipo_solicitacao,
            "valorPatrimonio": f"{valor_patrimonio:.2f}",
        }
        return {"query": query, "variables": variables}

    def build_update_card_payloads(self, *, card_id: str, status: str, prioridade: str) -> list[dict]:
        query = """
mutation UpdateCardField($cardId: ID!, $fieldId: ID!, $newValue: [UndefinedInput]) {
  updateCardField(
    input: {
      card_id: $cardId
      field_id: $fieldId
      new_value: $newValue
    }
  ) {
    success
    card {
      id
    }
  }
}
""".strip()

        return [
            {
                "query": query,
                "variables": {
                    "cardId": card_id,
                    "fieldId": PIPEFY_FIELDS["status"],
                    "newValue": [status],
                },
            },
            {
                "query": query,
                "variables": {
                    "cardId": card_id,
                    "fieldId": PIPEFY_FIELDS["prioridade"],
                    "newValue": [prioridade],
                },
            },
        ]
