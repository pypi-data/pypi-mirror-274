# VIN Validator

`vin-validator` is a Python package to validate Vehicle Identification Numbers (VINs) using the NHTSA API.

## Installation

To install the package, use the following command:

```bash
pip install vin-validator
```

## Usage

Here's an example of how to use the `vin-validator` package to validate a VIN and retrieve vehicle details:

```python
from vin_validator.validator import VINValidator

vin = "1HGCM82633A004352"
is_valid, details = VINValidator.validate_vin(vin)

if is_valid:
    print(f"VIN '{vin}' is valid.")
    print("Vehicle Details:")
    print(f"Make: {details.get('Make')}")
    print(f"Model: {details.get('Model')}")
    print(f"Model Year: {details.get('ModelYear')}")
    print(f"Body Class: {details.get('BodyClass')}")
else:
    print(f"VIN '{vin}' is invalid.")
```

## Example Script

You can also find an example script in the [examples](examples/validate_vin.py) directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.