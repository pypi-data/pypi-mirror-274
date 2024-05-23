import unittest
from .entities import TemperatureData, TemperatureType


class TestTemperature(unittest.TestCase):

    def test_initialization(self):
        temp = TemperatureData(25.0, TemperatureType.CELSIUS)
        self.assertEqual(temp.type, TemperatureType.CELSIUS)
        self.assertEqual(temp.value, 25.0)

    def test_celsius_property(self):
        temp_c = TemperatureData(25.0, TemperatureType.CELSIUS)
        self.assertEqual(temp_c.celsius, 25.0)

        temp_f = TemperatureData(77.0, TemperatureType.FAHRENHEIT)
        self.assertAlmostEqual(temp_f.celsius, 25.0, places=2)

    def test_fahrenheit_property(self):
        temp_f = TemperatureData(77.0, TemperatureType.FAHRENHEIT)
        self.assertEqual(temp_f.fahrenheit, 77.0)

        temp_c = TemperatureData(25.0, TemperatureType.CELSIUS)
        self.assertAlmostEqual(temp_c.fahrenheit, 77.0, places=2)

