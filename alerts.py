"""Правила оповещений о проблемах с сервисами."""

AVAILABILITY_THRESHOLD = 99.0


def availability_alert(service, availability):
    if availability < AVAILABILITY_THRESHOLD:
        return f"ALERT {service}: доступность {availability:.2f}% ниже {AVAILABILITY_THRESHOLD}%"
    return None


RESPONSE_THRESHOLD_MS = 300


def slow_alert(service, avg_ms):
    if avg_ms > RESPONSE_THRESHOLD_MS:
        return f"ALERT {service}: среднее время ответа {avg_ms:.0f} мс выше {RESPONSE_THRESHOLD_MS} мс"
    return None


def severity(availability):
    """Уровень критичности инцидента по доступности."""
    return "critical" if availability < 95 else "warning"


CHANNELS = {"critical": "дежурный инженер (звонок)", "warning": "чат команды"}


def channel(level):
    return CHANNELS[level]
