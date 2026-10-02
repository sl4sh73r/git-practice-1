"""Тесты SLO и бюджета ошибок."""
import unittest

import slo


class SloTest(unittest.TestCase):
    def test_budget(self):
        self.assertEqual(slo.error_budget("api"), 0.5)
        self.assertTrue(slo.slo_met("web", 99.2))
        self.assertFalse(slo.slo_met("payments", 99.2))


if __name__ == "__main__":
    unittest.main()
