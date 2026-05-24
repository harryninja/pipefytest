from app.domain.constants import PRIORIDADE_ALTA, PRIORIDADE_NORMAL
from app.domain.rules.priority import calculate_priority


def test_calculate_priority_returns_high_for_large_wealth():
    assert calculate_priority(200000) == PRIORIDADE_ALTA
    assert calculate_priority(250000) == PRIORIDADE_ALTA


def test_calculate_priority_returns_normal_for_small_wealth():
    assert calculate_priority(199999.99) == PRIORIDADE_NORMAL
