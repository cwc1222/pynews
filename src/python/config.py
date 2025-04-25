import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    OPEN_ROUTER_API_KEY: str
    GMAIL_APP_PASSWORD: str
    GMAIL_SENDER: str
    GMAIL_RECIPIENTS: list[str]


def get_config() -> Config:
    load_dotenv()
    OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
    if OPEN_ROUTER_API_KEY is None:
        raise ValueError("OPEN_ROUTER_API_KEY not set in .env file")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    if GMAIL_APP_PASSWORD is None:
        raise ValueError("GMAIL_APP_PASSWORD not set in .env file")
    GMAIL_SENDER = os.getenv("GMAIL_SENDER")
    if GMAIL_SENDER is None:
        raise ValueError("GMAIL_SENDER not set in .env file")
    GMAIL_RECIPIENTS = os.getenv("GMAIL_RECIPIENTS")
    if GMAIL_RECIPIENTS is None:
        raise ValueError("GMAIL_RECIPIENTS not set in .env file")
    recipients_list = GMAIL_RECIPIENTS.split(",")
    return Config(
        OPEN_ROUTER_API_KEY=OPEN_ROUTER_API_KEY,
        GMAIL_APP_PASSWORD=GMAIL_APP_PASSWORD,
        GMAIL_SENDER=GMAIL_SENDER,
        GMAIL_RECIPIENTS=recipients_list,
    )
