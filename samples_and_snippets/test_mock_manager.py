import unittest
import os
from mocks import MockCarparkManager


class TestMockCarparkManager(unittest.TestCase):

    def setUp(self):
        self.manager = MockCarparkManager()
        self.plate1 = "ABC123"
        self.plate2 = "XYZ789"
        # Clear log file before each test
        if os.path.exists("log.txt"):
            os.remove("log.txt")

    def test_temperature_setting(self):
        self.manager.temperature_reading(22.5)
        self.assertEqual(self.manager.temperature, 22.5)

    def test_incoming_car_adds_plate_and_reduces_space(self):
        initial_spaces = self.manager.available_spaces
        self.manager.incoming_car(self.plate1)
        self.assertIn(self.plate1, self.manager._cars_inside)
        self.assertEqual(self.manager.available_spaces, initial_spaces - 1)

    def test_duplicate_car_cannot_enter(self):
        self.manager.incoming_car(self.plate1)
        initial_spaces = self.manager.available_spaces
        self.manager.incoming_car(self.plate1)  # Try again
        self.assertEqual(self.manager.available_spaces, initial_spaces)

    def test_outgoing_car_removes_plate_and_increases_space(self):
        self.manager.incoming_car(self.plate1)
        spaces_after_entry = self.manager.available_spaces
        self.manager.outgoing_car(self.plate1)
        self.assertNotIn(self.plate1, self.manager._cars_inside)
        self.assertEqual(self.manager.available_spaces, spaces_after_entry + 1)

    def test_outgoing_car_not_inside_is_ignored(self):
        initial_spaces = self.manager.available_spaces
        self.manager.outgoing_car(self.plate2)  # Not in carpark
        self.assertEqual(self.manager.available_spaces, initial_spaces)

    def test_no_entry_when_carpark_is_full(self):
        self.manager._spaces = 0
        self.manager.incoming_car(self.plate1)
        self.assertNotIn(self.plate1, self.manager._cars_inside)
        self.assertEqual(self.manager.available_spaces, 0)

    def test_logging(self):
        self.manager.incoming_car(self.plate1)
        self.manager.outgoing_car(self.plate1)
        with open("log.txt", "r") as f:
            logs = f.readlines()
        self.assertEqual(len(logs), 2)
        self.assertTrue(logs[0].startswith("[IN]"))
        self.assertTrue(logs[1].startswith("[OUT]"))


if __name__ == "__main__":
    unittest.main()
