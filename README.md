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

## Debug in vscode

```bash
# REF: https://stackoverflow.com/questions/75537379/how-to-debug-server-side-code-in-sveltekit-using-visual-studio-code

# 1. start the vite server
bun run dev
# 2. In Visual Studio Code command palette
#    choose Debug: Attach to node process,
#    which will automatically show the list
#    of running Node.js processes on your local computer
# 3. Pick the node process, and start debugging!
```

```bash
# 1. start the wrangler server
bun run preview
# 2. Use the wrangler debugger
# 3. Only compiled code can have breakpoints using "debugger" keyword
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

# Local d1 query
bunx wrangler d1 migrations list pynews
bunx wrangler d1 migrations apply pynews
bunx wrangler d1 execute pynews --command "select * from d1_migrations"
bunx wrangler d1 execute pynews --command "select * from subscribers"
```

## Reference

- [github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- [github.com/pre-commit/pre-commit](https://github.com/pre-commit/pre-commit)
- [github.com/oven-sh/bun](https://github.com/oven-sh/bun)
- [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers/)
- [svelte.dev/docs/kit/introduction](https://svelte.dev/docs/kit/introduction)
