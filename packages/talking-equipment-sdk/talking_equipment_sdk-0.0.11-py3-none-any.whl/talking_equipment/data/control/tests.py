import unittest
from .entities import ControlData


class TestTemperature(unittest.TestCase):
    def setUp(self):
        self.control = ControlData(
            'False|True',
            'RelayState1|RelayState2',
        )

    def test_initialization(self):
        self.assertEqual(self.control.value, 'False|True')
        self.assertEqual(self.control.key, 'RelayState1|RelayState2')

    def test_value_property(self):
        self.assertEqual(self.control.values[1], 'True')
        self.assertEqual(self.control.as_dict()['RelayState1'], 'False')

    def test_key_property(self):
        self.assertEqual(self.control.keys[0], 'RelayState1')

