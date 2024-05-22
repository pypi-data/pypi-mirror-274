import json
import logging
import tempfile

from bs4 import BeautifulSoup

from etl_m_ibrahim_khalil.common_utils.api_client import ApiClient
from etl_m_ibrahim_khalil.common_utils.json_encoder import CommonJSONEncoder
from etl_m_ibrahim_khalil.data_sources.quotes.constants import RAW_FILE_PATH, ROOT_URL
from etl_m_ibrahim_khalil.models import Quote
from etl_m_ibrahim_khalil.supabase_repository import SupabaseRepository


class QuotesExtractor:
    def __init__(self, api_client: ApiClient, repository: SupabaseRepository) -> None:
        self._api_client = api_client
        self._repository = repository
        self._quotes = []

    def _parse_quotes_from_html(self, quotes: bytes) -> None:
        soup = BeautifulSoup(quotes, "html.parser")
        quotes_list = soup.find_all("div", class_="quote")
        for quote in quotes_list:
            quote_message = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            self._quotes.append(Quote(author=author, quote=quote_message, tags=tags))

        logging.info("%s quotes extracted successfully!", len(quotes_list))

        next_page = soup.find("li", class_="next")
        if next_page:
            next_page_url = next_page.find("a").get("href")
            # Extract quotes from the next page
            self._api_client.base_url = f"{ROOT_URL}{next_page_url}"
            self.extract_quotes()
        else:
            logging.info("All quotes extracted successfully! Total quotes: %s", len(self._quotes))

    def _save_quotes_to_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            json.dump([quote.dict() for quote in self._quotes], temp_file, cls=CommonJSONEncoder)
            temp_file.flush()
            self._repository.upload_file_to_bucket(RAW_FILE_PATH, temp_file.name)

    def extract_quotes(self) -> None:
        quotes: bytes = self._api_client.get_quotes()

        if quotes:
            self._parse_quotes_from_html(quotes)
            self._save_quotes_to_json()
        else:
            logging.error("Failed to extract quotes")


if __name__ == "__main__":
    api_client = ApiClient("https://quotes.toscrape.com")
    supabase_repository = SupabaseRepository()
    quotes_extractor = QuotesExtractor(api_client, supabase_repository)
    quotes_extractor.extract_quotes()
