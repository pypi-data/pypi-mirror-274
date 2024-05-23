import unittest
from .entities import VibrationData


class TestVibration(unittest.TestCase):
    def setUp(self):
        self.vibration = VibrationData(
            "7|6|22|20|55|18|97",
            "X-Axis Speed|Y-Axis Speed|Z-Axis Speed|X-Axis Frequency|Y-Axis Frequency|Z-Axis Frequency|Duty Cycle"
        )

    def test_initialization(self):
        self.assertEqual(self.vibration.value, "7|6|22|20|55|18|97")
        self.assertEqual(self.vibration.key, "X-Axis Speed|Y-Axis Speed|Z-Axis Speed|X-Axis Frequency|Y-Axis Frequency|Z-Axis Frequency|Duty Cycle")

    def test_value_property(self):
        self.assertEqual(self.vibration.values[3], "20")
        self.assertEqual(self.vibration.as_dict()["Duty Cycle"], "97")

    def test_key_property(self):
        self.assertEqual(self.vibration.keys[5], "Z-Axis Frequency")

