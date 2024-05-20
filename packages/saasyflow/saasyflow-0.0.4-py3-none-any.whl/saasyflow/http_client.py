import requests


class HttpClient(requests.Session):
    def __init__(self, base_url, api_key):
        super().__init__()
        self.base_url = f"{base_url}/api"
        self.headers.update({"Authorization": f"Bearer {api_key}"})

    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return super().get(url, **kwargs)

    def post(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return super().post(url, **kwargs)

    def put(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return super().put(url, **kwargs)

    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return super().delete(url, **kwargs)
