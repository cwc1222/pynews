import datetime
import json
import smtplib
from dataclasses import asdict, dataclass
from email.mime.text import MIMEText
from pathlib import Path

from src.python.config import get_config
from src.python.httpclient import default_client
from src.python.newsfetcher.abccolor import ABCColorNewsFetcher
from src.python.newsfetcher.lanacion import LaNacionNewsFetcher
from src.python.newsfetcher.newsfetcher import NewsFetcher
from src.python.summarizer import Summarizer


@dataclass
class NewsSource:
    fetcher: NewsFetcher
    persist_to: str


@dataclass
class FetchedNews:
    provider: str
    news: list[dict]


config = get_config()
generated_folder = "generated"
fetchers: list[NewsFetcher] = [
    ABCColorNewsFetcher(
        "https://www.abc.com.py",
        "/pf/api/v3/content/fetch/sections-api",
        default_client,
    ),
    LaNacionNewsFetcher(
        "https://www.lanacion.com.py",
        "/pf/api/v3/content/fetch/content-search-feed",
        default_client,
    ),
]
summarizer = Summarizer(
    api_token=config.OPEN_ROUTER_API_KEY,
    http_client=default_client,
    preferred_lang="繁體中文",
)


def fetch_news() -> None:
    """
    Fetches news from the configured news sources and saves the result as a JSON file.

    Iterates through the configured news fetchers, fetches news from each source,
    and stores the results in a list of FetchedNews objects. Each FetchedNews object
    contains the provider name and a list of news items in dictionary format.
    """
    fetched: list[FetchedNews] = [
        FetchedNews(
            provider=fetcher.provider,
            news=[n.to_dict() for n in fetcher.fetch_news()],
        )
        for fetcher in fetchers
    ]
    with open(f"{generated_folder}/news.json", "w", encoding="utf-8") as f:
        json.dump([asdict(item) for item in fetched], f, ensure_ascii=False, indent=4)


def summarize_news() -> None:
    """
    Summarizes the news fetched from the sources and saves the result as an HTML file.

    Reads the news data from the JSON file and passes it to the summarizer.
    The summarized result is then written to an HTML file.
    """
    summarized = ""
    with open(f"{generated_folder}/news.json", encoding="utf-8") as f:
        news = f.read()
        summarized = summarizer.summarize(news)
    with open(f"{generated_folder}/summary.html", "w", encoding="utf-8") as f:
        f.write(summarized)


def dispatch_summary() -> None:
    """
    Dispatches the generated news summary via email.

    Reads the summary from the generated HTML file and sends it as an HTML email
    using Gmail SMTP. The email is sent from the configured sender address to the
    configured recipient list, with the subject containing the current date.

    Uses Gmail app password authentication for sending the email securely.
    """
    summary = ""
    with open(f"{generated_folder}/summary.html", encoding="utf-8") as f:
        summary = f.read()

    sender = config.GMAIL_SENDER
    recipients = config.GMAIL_RECIPIENTS
    app_password = config.GMAIL_APP_PASSWORD

    message = MIMEText(summary, 'html')
    message['Subject'] = (
        f"{datetime.datetime.now().strftime("%Y-%m-%d")} Paraguay News Summary"
    )
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipients, message.as_string())


if __name__ == "__main__":
    Path(generated_folder).mkdir(parents=True, exist_ok=True)
    fetch_news()
    print("News fetched successfully.")
    summarize_news()
    print("News summarized successfully.")
    dispatch_summary()
    print("Summary dispatched successfully.")
