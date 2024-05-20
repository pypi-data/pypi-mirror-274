from .products import Products
from .customers import Customers
from .subscriptions import Subscriptions
from .http_client import HttpClient


class SaasyflowClient:
    def __init__(self, base_url, api_key):
        self.client = HttpClient(base_url, api_key)
        self.products = Products(self.client)
        self.customers = Customers(self.client)
        self.subscriptions = Subscriptions(self.client)
