# VIN Validator

`vin-validator` is a Python package to validate Vehicle Identification Numbers (VINs) using the NHTSA API.

## Installation

```bash
pip install vin-validator
```

## Usage
```python
from vin_validator.validator import VINValidator

vin = "1HGCM82633A004352"
is_valid = VINValidator.validate_vin(vin)
print(f"VIN is valid: {is_valid}")
```


### 5. License

Choose a license and put the text in the `LICENSE` file. For example, for MIT License:

**`LICENSE`**:
```plaintext
MIT License
...
