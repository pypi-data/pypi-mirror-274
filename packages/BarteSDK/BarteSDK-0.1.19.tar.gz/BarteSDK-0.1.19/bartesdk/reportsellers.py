import requests

class ReportSellersAPI:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.base_url = self._get_base_url(env, api_version)

    def _get_base_url(self, env, api_version):
        if env == "prd":
            return f'https://api.barte.com/{api_version}/report-sellers'
        elif env == "sandbox":
            return f'https://sandbox-api.barte.com/{api_version}/report-sellers'
        else:
            raise ValueError("Invalid environment specified")

    def report_sellers(self, query_file, recipient_email, id_seller, report_name, days_ago):
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'query_file': query_file,
            'recipient_email': recipient_email,
            'id_seller': id_seller,
            'report_name': report_name,
            'days_ago': days_ago
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.json()
