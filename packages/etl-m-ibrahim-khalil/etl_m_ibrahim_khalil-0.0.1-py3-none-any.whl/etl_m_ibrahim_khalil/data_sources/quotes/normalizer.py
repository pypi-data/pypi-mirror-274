import json
import logging

import pandas as pd

from etl.data_sources.quotes.constants import NORMALIZED_TABLE_NAME, RAW_FILE_PATH
from etl.supabase_repository import SupabaseRepository


class QuotesNormalizer:
    def __init__(self, repository: SupabaseRepository) -> None:
        self._repository = repository

    def _transform_quotes(self, quotes_df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Normalizing quotes shape: %s", quotes_df.shape)
        quotes_df = quotes_df.assign(tags=quotes_df["tags"]).explode("tags")
        quotes_df = quotes_df.rename(columns={"quote": "quote_message", "tags": "tag"})
        quotes_df = quotes_df.drop_duplicates(subset=["author", "quote_message", "tag"])
        quotes_df = quotes_df.reset_index(drop=True)
        quotes_df = quotes_df.astype({"author": str, "quote_message": str, "tag": str})
        logging.info("Normalized quotes shape: %s", quotes_df.shape)
        return quotes_df

    def _save_normalized_quotes(self, quotes_df: pd.DataFrame) -> None:
        quotes = quotes_df.to_dict(orient="records")
        self._repository.insert_data_into_table(NORMALIZED_TABLE_NAME, quotes)
        logging.info("Normalized quotes saved successfully!")

    def normalize_quotes(self) -> None:
        quotes = self._repository.download_file_from_bucket(RAW_FILE_PATH)
        if quotes:
            quotes = json.loads(quotes)
            quotes_df = pd.DataFrame(quotes)
            quotes_df = self._transform_quotes(quotes_df)
            self._save_normalized_quotes(quotes_df)
            logging.info("Quotes normalized successfully!")
        else:
            logging.error("Failed to normalize quotes")


if __name__ == "__main__":
    supabase_repository = SupabaseRepository()
    quotes_normalizer = QuotesNormalizer(supabase_repository)
    quotes_normalizer.normalize_quotes()
