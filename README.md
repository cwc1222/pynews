# pynews

Fetching Paraguayan news from La Nacion and ABC color, summarizing them using LLM via Openrouter, and sending it to subscribers.

## Quickstart

### Run the python script sending news summarization to your email

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

### Host the subscription page locally or publish to cloudflare workers

```bash
# bun upgrade
bun install
bun run dev
bun run preview
bun run deploy
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

## Reference

- [github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- [github.com/pre-commit/pre-commit](https://github.com/pre-commit/pre-commit)
- [github.com/oven-sh/bun](https://github.com/oven-sh/bun)
- [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers/)
- [svelte.dev/docs/kit/introduction](https://svelte.dev/docs/kit/introduction)
