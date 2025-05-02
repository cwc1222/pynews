import datetime
import json
import re
import urllib.parse
from dataclasses import dataclass

import requests

from src.python.httpclient import HttpClient
from src.python.newsfetcher.newsfetcher import News, NewsFetcher


@dataclass
class QueryABCColor:
    arc_site: str
    excludedSections: str
    id: str
    limit: str
    offset: str
    sort: str
    uri: str

    def to_dict(self):
        return {
            "arc-site": self.arc_site,
            "id": self.id,
            "limit": self.limit,
            "offset": self.offset,
            "sort": self.sort,
            "uri": self.uri,
        }


@dataclass
class QueryParams:
    query: QueryABCColor
    d: int
    mxId: int
    _website: str

    def to_dict(self):
        query_json = json.dumps(self.query.to_dict())

        return {
            "query": query_json,
            "d": self.d,
            "mxId": self.mxId,
            "_website": self._website,
        }


class ABCColorNewsFetcher(NewsFetcher):
    def __init__(self, base_url: str, api_path: str, http_client: HttpClient):
        self.provider = "ABC Color"
        self.base_url = base_url
        self.api_path = api_path
        self.http_client = http_client

    def clean_author(self, author: str) -> str:
        author = author.strip()
        if author.strip().lower() != "abc color":
            # Remove ", ABC Color" suffix
            author = author.replace(", ABC Color", "")
            # Normalize multiple spaces to a single space
            author = re.sub(r'\s+', ' ', author)
        return author

    def parse_display_date(self, date_str: str) -> datetime.datetime:
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {date_str}")

    def fetch_news(self) -> list[News]:
        query_params = QueryParams(
            query=QueryABCColor(
                arc_site="abccolor",
                excludedSections="",
                id="/policiales",
                limit="10",
                offset="0",
                sort="display_date:desc",
                uri="/policiales/",
            ),
            d=2197,
            mxId=00000000,
            _website="abccolor",
        )
        try:
            resp = self.http_client.get(
                f"{self.base_url}{self.api_path}", params=query_params.to_dict()
            )
            json = resp.json()
            return [
                News(
                    headLine=item["headlines"]["basic"],
                    subHeadLine=item["subheadlines"]["basic"],
                    publishedDate=self.parse_display_date(item["publish_date"]),
                    type=item["type"],
                    url=f"{self.base_url}{item["website_url"]}",
                    author=", ".join(
                        [
                            self.clean_author(str(a["name"]))
                            for a in item["credits"]["by"]
                        ]
                    ),
                    content="\n".join(
                        [
                            c["content"]
                            for c in list(item["content_elements"])
                            if c["type"] == "text"
                        ]
                    ),
                )
                for item in list(json["content_elements"])
            ]
        except requests.HTTPError as e:
            print(f"HTTP error occurred: [{e.response.status_code}] {e.response.text}")
            return []
        except Exception as e:
            print(f"Other error occurred: {e}")
            print(
                f"{self.base_url}{self.api_path}?{urllib.parse.urlencode(query_params.to_dict())}"
            )
            return []
