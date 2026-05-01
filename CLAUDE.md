# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Generic MCP server that exposes Markdown documentation to LLMs via tools and resources. Project identity (name, instructions, category labels) is configured via `config.toml` at the project root.

## Commands

```bash
uv sync                        # install dependencies
uv run main.py                 # run server (stdio, default)
uv run main.py --transport sse # run in SSE mode (port 6060)
uv run mcp dev main.py         # open MCP Inspector in browser for development
```

No test suite or linter is configured.

## Configuration

`docs/config.toml` (inside the docs repository) drives the server identity. The file is optional — without it the server uses auto-discovered defaults.

```toml
[project]
name = "my-project"
instructions = "System instructions for the LLM..."

[categories]
folder-name = "Human-readable label"
```

- **`[project].name`** — FastMCP server name. Defaults to the root directory name.
- **`[project].instructions`** — System instructions passed to the LLM. Defaults to a generic English string.
- **`[categories]`** — Optional label overrides. Any subfolder of `docs/` not listed here gets a title-cased label automatically.

The `docs/` directory must exist before the server starts — it is a separate git repository cloned alongside this one and is listed in `.gitignore`.

## Architecture

`main.py` is the entry point. It imports `server.app` (which creates the `FastMCP` instance) and then imports `server.tools` and `server.resources` — these side-effect imports register all handlers onto the shared `mcp` object before `mcp.run()` is called.

**`server/app.py`** is the central module. It defines:
- The `FastMCP` instance (`mcp`)
- `DOCS_DIR` — absolute path to `docs/`
- `CATEGORY_LABELS` — auto-discovered from `docs/` subdirectories, merged with `config.toml` overrides
- `_project_name` — resolved from `config.toml` or directory name
- Shared helpers: `markdown_files()`, `parse_path()`, `resolve_doc()`

All other server modules import from `server.app` — never from each other.

**`server/tools.py`** — registers three tools: `list_docs`, `read_doc`, `search_docs`.

**`server/resources.py`** — registers two resources: `docs://index` and `docs://{category}/{topic}`.

**`docs/`** — Markdown files organized in category subdirectories. Any `.md` file added under any subfolder is automatically discovered and served. Files in `img/` subdirectories are excluded.

## Adding Documentation

Drop a `.md` file into any `docs/<category>/` folder. No code changes required.

## Adding a New Category

1. Create the folder under `docs/`.
2. Optionally add a human-readable label in `config.toml` under `[categories]`. If omitted, the folder name is title-cased automatically.
