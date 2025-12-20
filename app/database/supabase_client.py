import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # <-- carrega o .env automaticamente

_SUPABASE_CLIENT: Client | None = None


def get_supabase_client() -> Client:
    """
    Returns a singleton Supabase client.
    """
    global _SUPABASE_CLIENT

    if _SUPABASE_CLIENT is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

        if not supabase_url or not supabase_key:
            raise RuntimeError("Supabase environment variables are not set")

        _SUPABASE_CLIENT = create_client(supabase_url, supabase_key)

    return _SUPABASE_CLIENT
