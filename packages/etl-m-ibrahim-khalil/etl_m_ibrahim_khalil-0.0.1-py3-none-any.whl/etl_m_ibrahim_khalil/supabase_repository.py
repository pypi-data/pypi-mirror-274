from io import BufferedReader, FileIO

import supabase
from supabase import Client, ClientOptions

from etl_m_ibrahim_khalil.config import Config


class SupabaseRepository:
    def __init__(
        self,
        supabase_url: str = None,
        supabase_key: str = None,
        options: ClientOptions = None,
        bucket_name: str = None,
    ):
        self.client: Client = supabase.create_client(
            supabase_url=supabase_url or Config.SUPABASE_URL,
            supabase_key=supabase_key or Config.SUPABASE_KEY,
            options=options,
        )
        self.bucket = self.client.storage.from_(bucket_name or Config.SUPABASE_BUCKET)

    def download_file_from_bucket(self, file_path: str) -> bytes:
        response = self.bucket.download(file_path)
        return response

    def upload_file_to_bucket(
        self, file_path: str, file_content: bytes | BufferedReader | FileIO | str
    ) -> bool:
        self.delete_file_from_bucket([file_path])
        response = self.bucket.upload(
            path=file_path,
            file=file_content,
            file_options={"cacheControl": "3600", "upsert": "True"},
        )
        return response.status_code == 201

    def update_file_in_bucket(
        self, file_path: str, file_content: bytes | BufferedReader | FileIO | str
    ) -> bool:
        response = self.bucket.update(
            path=file_path,
            file=file_content,
            file_options={"cacheControl": "3600", "upsert": "True"},
        )
        return response.status_code == 200

    def delete_file_from_bucket(self, file_path: str) -> bool:
        response = self.bucket.remove(file_path)
        return response

    def read_data_from_table(self, table_name: str) -> list:
        response = self.client.from_(table_name).select("*").execute()
        return response.get("data", [])

    def insert_data_into_table(self, table_name: str, data: list[dict]) -> bool:
        response = self.client.from_(table_name).insert(data).execute()
        return response
