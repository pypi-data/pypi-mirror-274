import requests

class buyersAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/buyers'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/buyers'
        else:
            raise ValueError("Invalid environment specified")

    def create(self, document, name, email, phone):
        headers = {
            'X-Token-Api': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'document': document,
            'name': name,
            'email': email,
            'httpMethod': 'POST',
            'phone': phone
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.json()
