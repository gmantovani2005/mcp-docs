FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY main.py .
COPY server/ ./server/

ENV MCP_DOCS_DIR=/docs

EXPOSE 8080

CMD ["uv", "run", "main.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8080"]
