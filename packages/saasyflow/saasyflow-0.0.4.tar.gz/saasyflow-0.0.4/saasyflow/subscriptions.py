from .http_client import HttpClient
from .exception import SaasyflowException


class Subscriptions:
    def __init__(self, client: HttpClient):
        self.client = client

    def create(self, customer_id, product_id, plan_id):
        url = f"/subscriptions"
        payload = {
            "customerId": customer_id,
            "productId": product_id,
            "planId": plan_id,
            "state": "ACTIVE",
        }
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

    def get_by_customer_and_product(self, customer_id, product_id):
        url = f"/products/{product_id}/customers/{customer_id}"
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

    def start_customer_product_trial(self, customer_id, product_id):
        url = f"/products/{product_id}/customers/{customer_id}/start-free-trial"
        response = self.client.post(url)
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

    def report_customer_product_usage(self, customer_id, product_id, units):
        if units < 1:
            raise Exception("Units can't be less than 1")

        url = f"/products/{product_id}/customers/{customer_id}/usage"
        payload = {"units": units}
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

    def limit_customer_product_usage(self, customer_id, product_id, units):
        if units < 1:
            raise Exception("Units can't be less than 1")

        url = f"/products/{product_id}/customers/{customer_id}/limit-usage"
        response = self.client.put(url)
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
