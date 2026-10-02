"""Каталог сервисов продукта."""

SERVICES = {
    "web": {"title": "Сайт", "owner": "команда витрины"},
    "api": {"title": "Публичный API", "owner": "команда платформы"},
    "payments": {"title": "Платежи", "owner": "команда платежей"},
}


def owner(service):
    """Команда, отвечающая за сервис."""
    return SERVICES.get(service, {}).get("owner", "не назначен")
