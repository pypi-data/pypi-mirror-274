import requests

class VINValidator:
    @staticmethod
    def validate_vin(vin: str) -> (bool, dict):
        if len(vin) != 17:
            return False, {}
        
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
        response = requests.get(url)
        data = response.json()
        
        if data['Results'][0]['ErrorCode'] == '0':
            return True, data['Results'][0]
        else:
            return False, {}

