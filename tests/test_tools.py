"""Checks for the planning scripts:  python3 -m unittest discover -s tests"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

import link_budget as lb  # noqa: E402
import size_estimate as se  # noqa: E402


class LinkBudget(unittest.TestCase):
    def test_sensitivity_formula(self):
        # SF7 / 500 kHz: -174 + 57.0 + NF 6 - 7.5 + 3 implementation loss
        self.assertAlmostEqual(lb.sensitivity_dbm(500e3, 7), -115.5, places=1)

    def test_higher_spreading_factor_reaches_further(self):
        r = [lb.range_km(20, 2, lb.sensitivity_dbm(812.5e3, sf), 2.44e9, 9) for sf in (5, 6, 7, 8)]
        self.assertEqual(r, sorted(r))

    def test_free_space_path_loss_reference(self):
        # FSPL at 1 km, 2440 MHz is about 100.2 dB: a 100.2 dB budget must give ~1 km
        self.assertAlmostEqual(lb.range_km(100.2, 0, 0, 2.44e9, 0), 1.0, delta=0.01)

    def test_radio_horizon(self):
        self.assertAlmostEqual(lb.horizon_km(), 4.12 * (math.sqrt(2) + math.sqrt(120)), places=6)


class SizeEstimate(unittest.TestCase):
    def test_double_sided_is_smaller(self):
        raw, one, two = se.area()
        self.assertLess(raw, two)
        self.assertLess(two, one)


if __name__ == '__main__':
    unittest.main()
