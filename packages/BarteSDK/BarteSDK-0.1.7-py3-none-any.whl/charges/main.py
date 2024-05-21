import requests

class ChargesAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api2.barte.com/v2/charges'

    def list(self, charge_uuid):
        headers = {
            'X-Token-Api': self.api_key
        }
        url = f"{self.base_url}/{charge_uuid}"
        response = requests.get(url, headers=headers)
        return response.json()

    def create(self, data):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json'
        }
        url = self.base_url
        response = requests.post(url, headers=headers, json=data)
        return response.json()
