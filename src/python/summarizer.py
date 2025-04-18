import datetime

import requests
from jinja2 import BaseLoader, Environment

from src.python.httpclient import HttpClient


class Summarizer:
    def __init__(
        self,
        api_token: str,
        http_client: HttpClient,
        preferred_lang: str = "traditional chinese",
    ) -> None:
        self.url = "https://openrouter.ai/api/v1/completions"
        self.model = "google/gemini-2.0-flash-exp:free"
        self.api_token = api_token
        self.http_client = http_client
        self.preferred_lang = preferred_lang

    def prompt(self, content: str) -> str:
        with open("summary_prompt.j2", encoding="utf-8") as f:
            template = Environment(loader=BaseLoader()).from_string(f.read())
            prompt = template.render(
                {
                    "preferred_lang": self.preferred_lang,
                    "current_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "model": f"Open Router - {self.model}",
                    "content": content,
                }
            )
            return prompt

    def summarize(self, content: str) -> str:
        try:
            resp = self.http_client.post(
                self.url,
                data={
                    "model": self.model,
                    "prompt": self.prompt(content),
                    # "temperature": 0.7,
                    # "max_new_tokens": 2000,
                    # "top_p": 1,
                    # "top_k": 50,
                    # "repetition_penalty": 1.2,
                    # "stop_sequences": ["\n\n"],
                },
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                },
            ).json()
            return resp["choices"][0]["text"]
        except requests.HTTPError as e:
            return f"HTTP error occurred: [{e.response.status_code}] {e.response.text}"
        except Exception as e:
            return f"Other error occurred: {e}"
