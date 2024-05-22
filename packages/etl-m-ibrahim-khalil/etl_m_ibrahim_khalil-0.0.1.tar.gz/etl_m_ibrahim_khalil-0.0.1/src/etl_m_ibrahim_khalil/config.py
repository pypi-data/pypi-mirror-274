import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Configuration for the Supabase API
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
    SUPABASE_BUCKET_ACCESS_KEY = os.getenv("ACCESS_TOKEN_SECRET")

    # Configuration for the Postgres database
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
