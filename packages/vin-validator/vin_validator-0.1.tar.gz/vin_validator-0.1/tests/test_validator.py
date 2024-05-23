import unittest
from vin_validator.validator import VINValidator

class TestVINValidator(unittest.TestCase):
    def test_valid_vin(self):
        vin = "1HGCM82633A004352"  # Example of a valid VIN
        self.assertTrue(VINValidator.validate_vin(vin))

    def test_invalid_vin(self):
        vin = "1HGCM82633A00435"  # Example of an invalid VIN (length not 17)
        self.assertFalse(VINValidator.validate_vin(vin))

if __name__ == '__main__':
    unittest.main()
