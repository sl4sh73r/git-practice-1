"""Расчёт показателей доступности сервисов по результатам проверок."""
import csv


def load_checks(path):
    """Читает журнал проверок из CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def for_service(checks, service):
    """Проверки одного сервиса."""
    return [c for c in checks if c["service"] == service]


def availability(checks):
    if not checks:
        return 0.0
    ok = sum(1 for c in checks if c["status"] == "up")
    return 100 * ok / len(checks)


def avg_response(checks):
    times = [int(c["response_ms"]) for c in checks if c["status"] == "up"]
    if not times:
        return 0
    return sum(times) / len(times)


def p95_response(checks):
    times = sorted(int(c["response_ms"]) for c in checks if c["status"] == "up")
    if not times:
        return 0
    return times[max(0, round(0.95 * len(times)) - 1)]


def downtime_minutes(checks, interval_min=5):
    return interval_min * sum(1 for c in checks if c["status"] == "down")
