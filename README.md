# pynews

Fetching Paraguayan news from La Nacion and ABC color, summarizing them using LLM via Openrouter, and sending it to subscribers.

## Quickstart

1. Create an .env file

```env

# REF: https://openrouter.ai/docs/quickstart
OPEN_ROUTER_API_KEY=""

# REF: https://support.google.com/mail/answer/185833?hl=en
GMAIL_APP_PASSWORD=""
GMAIL_SENDER=""
GMAIL_RECIPIENTS=""
```

```bash
uv run main.py
```

## Common commands

```bash
uv init -p 3.13 .
uv run main.py
uv sync
uv lock --upgrade

pre-commit install
pre-commit run --all-files
pre-commit autoupdate
```
