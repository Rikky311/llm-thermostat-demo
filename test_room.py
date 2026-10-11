
"""Tests for the simulated room heating model."""

import math
import unittest

from room import simulate


class TestRoomSimulation(unittest.TestCase):

    def test_simulation_runs_for_24_hours(self):
        history, energy = simulate(
            setpoint=21.0,
            hours=24,
            start_temp=21.0,
        )

        self.assertEqual(len(history), 1440)

    def test_energy_is_non_negative(self):
        _, energy = simulate(
            setpoint=21.0,
            hours=24,
            start_temp=21.0,
        )

        self.assertGreaterEqual(energy, 0.0)

    def test_energy_matches_heater_runtime(self):
        history, energy = simulate(
            setpoint=21.0,
            hours=24,
            start_temp=21.0,
        )

        heater_minutes = sum(
            1 for _, _, heater_on in history if heater_on
        )

        expected_energy = 2.0 * heater_minutes / 60

        self.assertAlmostEqual(energy, expected_energy, places=8)

    def test_temperatures_are_finite(self):
        history, _ = simulate(
            setpoint=21.0,
            hours=24,
            start_temp=21.0,
        )

        for _, temperature, _ in history:
            self.assertTrue(math.isfinite(temperature))


if __name__ == "__main__":
    unittest.main()