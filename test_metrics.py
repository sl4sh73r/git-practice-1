"""Тесты расчёта показателей: python3 -m unittest"""
import unittest

import metrics

UP = {"service": "api", "status": "up", "response_ms": "100"}
DOWN = {"service": "api", "status": "down", "response_ms": "0"}


class MetricsTest(unittest.TestCase):
    def test_availability(self):
        self.assertEqual(metrics.availability([UP, UP, UP, DOWN]), 75)
        self.assertEqual(metrics.availability([]), 0)


if __name__ == "__main__":
    unittest.main()
