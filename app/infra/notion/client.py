import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()


def get_notion_client() -> Client:
    token = os.getenv("NOTION_API_TOKEN")

    if not token:
        raise RuntimeError("NOTION_API_TOKEN is not set")

    return Client(auth=token)
