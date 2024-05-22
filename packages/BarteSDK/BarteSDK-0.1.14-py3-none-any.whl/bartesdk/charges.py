import requests

class ChargesAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api2.barte.com/v2/charges'

    def list_by_uuid(self, charge_uuid):
        headers = {
            'X-Token-Api': self.api_key
        }
        url = f"{self.base_url}/{charge_uuid}"
        response = requests.get(url, headers=headers)
        return response.json()

    def list(self, **params):
        headers = {
            'X-Token-Api': self.api_key
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()

