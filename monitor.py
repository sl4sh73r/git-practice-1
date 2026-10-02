"""PulseWatch: мониторинг доступности сервисов. Запуск: python3 monitor.py [checks.csv]"""
import sys

import metrics

VERSION = "1.2"


def build_report(checks):
    lines = [
        f"PulseWatch v{VERSION}: отчёт о доступности сервисов",
        f"{'сервис':<10}{'доступность':>12}{'ответ, мс':>11}",
    ]
    for name in sorted({c["service"] for c in checks}):
        rows = metrics.for_service(checks, name)
        lines.append(
            f"{name:<10}{metrics.availability(rows):>11.2f}%{metrics.avg_response(rows):>11.0f}"
        )
    return "\n".join(lines)


def main(argv):
    path = argv[0] if argv else "checks.csv"
    print(build_report(metrics.load_checks(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
