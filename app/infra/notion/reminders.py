import os
from datetime import datetime
from dotenv import load_dotenv

from app.infra.notion.client import get_notion_client

load_dotenv()


def create_notion_reminder(
    title: str,
    reminder_datetime: str,
    tags: list[str] | None = None,
    source: str = "telegram",
    memory_id: str | None = None,
):
    """
    Cria um lembrete no Notion Calendar.
    """

    notion = get_notion_client()
    database_id = os.getenv("NOTION_REMINDERS_DB_ID")

    if not database_id:
        raise RuntimeError("NOTION_REMINDERS_DB_ID is not set")

    properties = {
        "Title": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "Date": {
            "date": {
                "start": reminder_datetime
            }
        },
        "Source": {
            "select": {
                "name": source
            }
        },
    }

    if tags:
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in tags]
        }

    if memory_id:
        properties["Memory ID"] = {
            "rich_text": [
                {
                    "text": {
                        "content": memory_id
                    }
                }
            ]
        }

    return notion.pages.create(
        parent={"database_id": database_id},
        properties=properties,
    )
