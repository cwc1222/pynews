import requests


class HttpClient:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept": "application/json",
        }

    def get(self, url: str, params: dict | None = None) -> requests.Response:
        """
        Make a GET request to the specified URL with optional parameters.
        """
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response

    def post(
        self, url: str, data: dict | None = None, headers: dict | None = None
    ) -> requests.Response:
        """
        Make a POST request to the specified URL with optional data.
        """
        headers = headers or self.headers
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response


default_client = HttpClient()
