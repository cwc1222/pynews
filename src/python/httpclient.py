import requests
from tenacity import retry, stop_after_attempt, wait_exponential


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

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=4, max=15),
            before=lambda retry_state: print(
                f"Retrying... {retry_state.attempt_number}"
            ),
            reraise=True,
        )
        def _get_with_retry():
            try:
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                return response
            except requests.HTTPError as e:
                raise Exception(
                    f"HTTP error occurred: [{e.response.status_code}] {e.response.text}"
                )
            except Exception as e:
                raise Exception(f"Unexpected error occurred: {e}")

        return _get_with_retry()

    def post(
        self, url: str, data: dict | None = None, headers: dict | None = None
    ) -> requests.Response:
        """
        Make a POST request to the specified URL with optional data.
        """

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=4, max=15),
            before=lambda retry_state: print(
                f"Retrying... {retry_state.attempt_number}"
            ),
            reraise=True,
        )
        def _post_with_retry(headers: dict):
            try:
                response = requests.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response
            except requests.HTTPError as e:
                raise Exception(f"HTTP error occurred: {e}")
            except Exception as e:
                raise Exception(f"Unexpected error occurred: {e}")

        picked_headers = headers or self.headers
        return _post_with_retry(picked_headers)


default_client = HttpClient()
