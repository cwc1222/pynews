import datetime
import json
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from src.python.httpclient import HttpClient
from src.python.newsfetcher.newsfetcher import News, NewsFetcher


@dataclass
class QueryLaNacion:
    feedFrom: str
    feedQuery: str
    feedSize: str
    website: str

    def to_dict(self):
        return {
            "feedFrom": self.feedFrom,
            "feedQuery": self.feedQuery,
            "feedSize": self.feedSize,
            "website": self.website,
        }


@dataclass
class QueryParams:
    query: QueryLaNacion
    d: int
    _website: str

    def to_dict(self):
        query_json = json.dumps(self.query.to_dict())
        return {"query": query_json, "d": self.d, "_website": self._website}


class LaNacionNewsFetcher(NewsFetcher):
    def __init__(self, base_url: str, api_path: str, http_client: HttpClient):
        self.provider = "La Nación"
        self.base_url = base_url
        self.api_path = api_path
        self.http_client = http_client

    def fetch_news_content(self, news_url: str) -> str:
        try:
            resp = self.http_client.get(f"{self.base_url}{news_url}")
            soup = BeautifulSoup(resp.content, "html.parser")
            article = soup.find('div', class_="article-body")
            if not isinstance(article, Tag):
                raise Exception("Article body not found")
            paragraphs = article.find_all("p", class_="paragraph")
            filtered_paragraphs = [
                p for p in paragraphs if isinstance(p, Tag) and not p.find("a")
            ]
            return "\n".join([p.get_text() for p in filtered_paragraphs])
        except requests.HTTPError as e:
            return f"HTTP error occurred: [{e.response.status_code}] {e.response.text}"
        except Exception as e:
            return f"Other error occurred: {e}"

    def parse_display_date(self, date_str: str) -> datetime.datetime:
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {date_str}")

    def fetch_news(self) -> list[News]:
        query_params = QueryParams(
            query=QueryLaNacion(
                feedFrom="0",
                feedQuery="taxonomy.sites._id:\"/politica\"",
                feedSize="10",
                website="lanacionpy",
            ),
            d=681,
            _website="lanacionpy",
        )
        resp = self.http_client.get(
            f"{self.base_url}{self.api_path}", params=query_params.to_dict()
        )
        json = resp.json()
        return [
            News(
                headLine=item["headlines"]["basic"],
                subHeadLine=item["description"]["basic"],
                publishedDate=self.parse_display_date(item["display_date"]),
                type="story",
                url=f"{self.base_url}{item["canonical_url"]}",
                author=", ".join([str(a["name"]) for a in item["credits"]["by"]]),
                content=self.fetch_news_content(item["canonical_url"]),
            )
            for item in json["content_elements"]
        ]
