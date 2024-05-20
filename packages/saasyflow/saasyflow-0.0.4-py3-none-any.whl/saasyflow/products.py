from .http_client import HttpClient
from .exception import SaasyflowException


class Products:
    def __init__(self, client: HttpClient):
        self.client = client

    def get_products(self, take=50, skip=0):
        url = f"/products"
        payload = {"take": take, "skip": skip}
        response = self.client.get(url, params=payload)
        json = response.json()
        if response.status_code >= 400:
            raise SaasyflowException(
                json["message"],
                status_code=json["statusCode"],
                errors=json["errors"],
                is_general=json["isGeneral"],
            )
        else:
            return json

    def get_product(self, id: str):
        url = f"/products/{id}"
        response = self.client.get(url)
        json = response.json()
        if response.status_code >= 400:
            raise SaasyflowException(
                json["message"],
                status_code=json["statusCode"],
                errors=json["errors"],
                is_general=json["isGeneral"],
            )
        else:
            return json

    def create_plan_payment_link(
        self, product_id: str, plan_id: str, customer_id: str, redirect_url: str
    ):
        url = f"/products/{product_id}/plans/{plan_id}/create-payment-link"
        payload = {"customerId": customer_id, "gateway": "TAP", "redirectURL": redirect_url}
        response = self.client.post(url, json=payload)
        json = response.json()
        if response.status_code >= 400:
            raise SaasyflowException(
                json["message"],
                status_code=json["statusCode"],
                errors=json["errors"],
                is_general=json["isGeneral"],
            )
        else:
            return json

    def create_package_payment_link(
        self, product_id: str, package_id: str, customer_id: str, redirect_url: str
    ):
        url = f"/products/{product_id}/packages/{package_id}/create-payment-link"
        payload = {"customerId": customer_id, "gateway": "TAP", "redirectURL": redirect_url}
        response = self.client.post(url, json=payload)
        json = response.json()
        if response.status_code >= 400:
            raise SaasyflowException(
                json["message"],
                status_code=json["statusCode"],
                errors=json["errors"],
                is_general=json["isGeneral"],
            )
        else:
            return json
