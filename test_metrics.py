"""Тесты расчёта показателей: python3 -m unittest"""
import unittest

import metrics

UP = {"service": "api", "status": "up", "response_ms": "100"}
DOWN = {"service": "api", "status": "down", "response_ms": "0"}


class MetricsTest(unittest.TestCase):
    def test_availability(self):
        self.assertEqual(metrics.availability([UP, UP, UP, DOWN]), 75)
        self.assertEqual(metrics.availability([]), 0)

    def test_response_and_downtime(self):
        self.assertEqual(metrics.avg_response([UP, DOWN]), 100)
        self.assertEqual(metrics.downtime_minutes([UP, DOWN, DOWN]), 10)


if __name__ == "__main__":
    unittest.main()
