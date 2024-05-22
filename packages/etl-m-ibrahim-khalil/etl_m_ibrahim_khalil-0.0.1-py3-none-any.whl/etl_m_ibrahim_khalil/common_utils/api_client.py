import logging

import requests
from circuitbreaker import circuit
from requests.exceptions import HTTPError


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @circuit(failure_threshold=3, expected_exception=HTTPError, recovery_timeout=10)
    def get_quotes(self) -> bytes:
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return response.content
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None


if __name__ == "__main__":
    api_client = ApiClient("https://quotes.toscrape.com/")
    x = api_client.get_quotes()
