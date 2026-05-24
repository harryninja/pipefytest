class ClientAlreadyExistsError(Exception):
    pass


class ClientNotFoundError(Exception):
    pass


class WebhookAlreadyProcessedError(Exception):
    pass
