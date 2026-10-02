"""PulseWatch: мониторинг доступности сервисов. Запуск: python3 monitor.py [checks.csv]"""
import sys

import alerts
import metrics
import slo

VERSION = "1.3"


def build_report(checks):
    lines = [
        f"PulseWatch v{VERSION}: отчёт о доступности сервисов",
        f"{'сервис':<10}{'доступность':>12}{'ответ, мс':>11}{'p95, мс':>9}{'простой, мин':>14}",
    ]
    notes = []
    for name in sorted({c["service"] for c in checks}):
        rows = metrics.for_service(checks, name)
        avail = metrics.availability(rows)
        lines.append(
            f"{name:<10}{avail:>11.2f}%{metrics.avg_response(rows):>11.0f}"
            f"{metrics.p95_response(rows):>9}{metrics.downtime_minutes(rows):>14}"
        )
        if name in slo.SLO_TARGETS:
            state = "выполнен" if slo.slo_met(name, avail) else "НАРУШЕН"
            notes.append(
                f"SLO {name} ({slo.SLO_TARGETS[name]}%): {state}, "
                f"расход бюджета ошибок x{slo.burn_rate(name, avail)} от нормы"
            )
        for alert in (
            alerts.availability_alert(name, avail),
            alerts.slow_alert(name, metrics.avg_response(rows)),
        ):
            if alert:
                notes.append(f"{alert} [{alerts.severity(avail)}]")
    return "\n".join(lines + [""] + notes)


def main(argv):
    path = argv[0] if argv else "checks.csv"
    print(build_report(metrics.load_checks(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
