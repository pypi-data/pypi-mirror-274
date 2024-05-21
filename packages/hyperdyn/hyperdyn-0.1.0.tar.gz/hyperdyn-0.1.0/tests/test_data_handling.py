# tests/test_data_handling.py

from unittest import TestCase
from hyperdyn.data_handling import load_data

class TestDataHandling(TestCase):
    def test_load_data(self):
        # Arrange
        input_file = "tests/data/input_data.csv"
        expected_data = ["Expected Data"]

        # Act
        data = load_data(input_file)

        # Assert
        self.assertEqual(data.tolist(), expected_data)
