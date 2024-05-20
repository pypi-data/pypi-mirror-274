from .http_client import HttpClient
from .exception import SaasyflowException


class Customers:
    def __init__(self, client: HttpClient):
        self.client = client

    def get_customers(self, take=50, skip=0):
        url = f"/customers"
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

    def create_customer(self, name: str, email: str):
        url = f"/customers"
        payload = {"name": name, "email": email}
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

    def get_customer(self, id: str):
        url = f"/customers/{id}"
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

    def update_customer(self, id: str, name="", email=""):
        url = f"/customers/{id}"
        payload = {}

        if len(name) > 0:
            payload["name"] = name
        if len(email) > 0:
            payload["email"] = email

        response = self.client.put(url, json=payload)
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

    def delete_customer(self, id: str):
        url = f"/customers/{id}"
        response = self.client.delete(url)
        if response.status_code >= 400:
            json = response.json()
            raise SaasyflowException(
                json["message"],
                status_code=json["statusCode"],
                errors=json["errors"],
                is_general=json["isGeneral"],
            )
        else:
            return None
