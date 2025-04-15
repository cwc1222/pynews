# pynews

Fetching Paraguayan news from La Nacion and ABC color, summarizing them using LLM via Openrouter, and sending it to subscribers.

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
