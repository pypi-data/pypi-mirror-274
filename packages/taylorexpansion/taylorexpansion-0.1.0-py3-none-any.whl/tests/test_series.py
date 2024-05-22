# tests/test_series.py

import unittest
from taylorexpansion.series import taylor_series
import sympy as sp

class TestTaylorSeries(unittest.TestCase):

    def test_taylor_series(self):
        x = sp.symbols('x')
        func = sp.sin
        series = taylor_series(func, 5, x0=0)
        expected = x - x**3/6 + x**5/120
        self.assertEqual(series, expected)

if __name__ == '__main__':
    unittest.main()

