from .charges import ChargesAPI
from .reportsellers import ReportSellersAPI

class BarteSDK:
    def __init__(self, api_key):
        self.api_key = api_key
        self.charges = ChargesAPI(api_key)
        self.reportsellers = ReportSellersAPI(api_key)
