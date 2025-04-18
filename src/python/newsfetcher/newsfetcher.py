import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class News:
    headLine: str
    subHeadLine: str
    publishedDate: datetime.datetime
    type: str
    url: str
    author: str
    content: str

    def to_dict(self):
        return {
            "headLine": self.headLine,
            "subHeadLine": self.subHeadLine,
            "publishedDate": self.publishedDate.isoformat(),
            "type": self.type,
            "url": self.url,
            "author": self.author,
            "content": self.content,
        }


class NewsFetcher(ABC):
    provider: str

    @abstractmethod
    def fetch_news(self) -> list[News]:
        """
        Abstract method to fetch news. This should be implemented by subclasses.
        """
        pass
