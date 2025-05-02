import datetime

from jinja2 import BaseLoader, Environment
from tenacity import retry, stop_after_attempt, wait_exponential

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
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=4, max=15),
            before=lambda retry_state: print(
                f"Retrying... {retry_state.attempt_number}"
            ),
            reraise=True,
        )
        def _summarize_with_retry():
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
                    "HTTP-Referer": "https://pynews.chenantunez.com",
                    "X-Title": "pynews",
                },
            ).json()
            if (
                "error" in resp
                and "code" in resp["error"]
                and resp["error"]["code"] == 429
            ):
                raise Exception(f"Open Router rate limit exceeded: {resp}")
            if "choices" not in resp:
                raise Exception(f"No choices found in response: {resp}")
            if len(resp["choices"]) == 0:
                raise Exception(f"Choices are empty in response: {resp}")
            if "text" not in resp["choices"][0]:
                raise Exception(f"Text is not present in response.Choices: {resp}")
            return resp["choices"][0]["text"]

        return _summarize_with_retry()
