from app.domain.constants import PRIORIDADE_ALTA, PRIORIDADE_NORMAL


HIGH_PRIORITY_THRESHOLD = 200000


def calculate_priority(valor_patrimonio: float) -> str:
    if valor_patrimonio >= HIGH_PRIORITY_THRESHOLD:
        return PRIORIDADE_ALTA
    return PRIORIDADE_NORMAL
