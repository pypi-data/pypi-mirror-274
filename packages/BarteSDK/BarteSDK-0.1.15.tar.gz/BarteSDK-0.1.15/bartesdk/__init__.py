from .charges import ChargesAPI
from .reportsellers import ReportSellersAPI


class BarteSDK:
    def __init__(self, api_key, env="prd", api_version="v2"):
        self.api_key = api_key
        self.env = env
        self.api_version = api_version
        self.charges = ChargesAPI(api_key, env, api_version)
        self.reportsellers = ReportSellersAPI(api_key, env, api_version)