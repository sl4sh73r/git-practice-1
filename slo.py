"""Целевые уровни доступности (SLO) и бюджет ошибок."""

SLO_TARGETS = {"web": 99.0, "api": 99.5, "payments": 99.9}


def slo_met(service, availability):
    return availability >= SLO_TARGETS[service]


def error_budget(service):
    """Допустимая доля неуспешных проверок, %."""
    return round(100 - SLO_TARGETS[service], 4)


def budget_left(service, availability):
    """Остаток бюджета ошибок, процентные пункты."""
    return round(error_budget(service) - (100 - availability), 4)
