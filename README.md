# mcp-docs

Generic MCP server that exposes Markdown documentation to LLMs, enabling them to search and answer questions about any software documentation.

The server identity (name, instructions, category labels) is driven entirely by the `docs/` directory — which is a separate repository cloned alongside this one.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Setup

### 1. Clone the documentation repository

The `docs/` directory must exist before the server can start. Clone the documentation repository into it:

```bash
git clone <docs-repo-url> docs
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables (optional)

Copy `.env.example` to `.env` and set `MCP_DOCS_DIR` if your documentation directory lives outside `docs/`:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_DOCS_DIR` | `./docs` | Absolute or relative path to the documentation directory |

## docs/ directory structure

The server auto-discovers categories from subdirectories. The only required file is `config.toml` at the root of `docs/`.

```
docs/
├── config.toml          # required — project identity
├── <category>/
│   ├── <topic>.md
│   └── ...
└── <category>/
    └── ...
```

### config.toml

```toml
[project]
name = "my-project"
instructions = """
System instructions for the LLM. Describe what this documentation covers
and how the model should use the available tools.
"""

[categories]
folder-name = "Human-readable label"
```

- **`[project]`** is required. `name` identifies the server; `instructions` guides the LLM.
- **`[categories]`** is optional. Any subdirectory not listed gets a title-cased label automatically (`my-folder` → `My Folder`).
- Files inside `img/` subdirectories are never served.

## Usage

### Run the server (stdio mode)

```bash
uv run main.py
```

### Development with MCP Inspector

```bash
uv run mcp dev main.py
```

Opens the MCP Inspector in the browser. To connect to a running SSE or Streamable HTTP server, start it first and point the inspector to the printed endpoint:

```bash
uv run main.py --transport sse
uv run main.py --transport streamable-http
```

### Configure with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "my-project": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-docs", "run", "main.py"],
      "env": { "MCP_DOCS_DIR": "/path/to/your/docs" }
    }
  }
}
```

### Configure with Claude Code

```bash
claude mcp add my-project -- uv --directory /path/to/mcp-docs run main.py
```

To pass `MCP_DOCS_DIR` when using Claude Code, add it to the server environment:

```bash
claude mcp add my-project -e MCP_DOCS_DIR=/path/to/your/docs -- uv --directory /path/to/mcp-docs run main.py
```

## Containers

### Build da imagem

```bash
# Docker
docker build -f .containers/Dockerfile -t mcp-docs:latest .

# Podman
podman build -f .containers/Dockerfile -t mcp-docs:latest .
```

### Executar localmente com docker-compose

Certifique-se de que o diretório `docs/` existe e está populado antes de iniciar:

```bash
docker compose up

# ou com Podman
podman compose up
```

O servidor ficará disponível em `http://localhost:8080/mcp`.

### Executar o container manualmente

```bash
# Docker
docker run --rm -p 8080:8080 -v ./docs:/docs:ro mcp-docs:latest

# Podman
podman run --rm -p 8080:8080 -v ./docs:/docs:ro mcp-docs:latest
```

### Deploy no Kubernetes

Os arquivos de deployment e service estão em `.containers/`. Edite `image:` em `deployment.yaml` para apontar para o seu registry antes de aplicar.

```bash
kubectl apply -f .containers/deployment.yaml
kubectl apply -f .containers/service.yaml
```

O Deployment referencia um `PersistentVolumeClaim` chamado `mcp-docs-pvc` para montar os arquivos de documentação em `/docs`. Crie e popule o PVC com a documentação antes de aplicar o Deployment.

### Testando com o MCP Inspector

Com o container rodando localmente (via `docker compose up` ou manualmente), o endpoint Streamable HTTP estará em `http://localhost:8080/mcp`.

1. Abra o MCP Inspector:

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. No inspector, selecione o transport **Streamable HTTP**.

3. Informe a URL: `http://localhost:8080/mcp`

4. Clique em **Connect**.

5. Teste as ferramentas disponíveis: `list_docs`, `read_doc`, `search_docs`.

## Capabilities

### Tools

| Tool | Description |
|------|-------------|
| `list_docs(category?)` | List available documentation files, optionally filtered by category |
| `read_doc(category, topic)` | Read the full content of a documentation file |
| `search_docs(query, category?)` | Full-text search across all documentation |

### Resources

| URI | Description |
|-----|-------------|
| `docs://index` | Full index of all available documentation files |
| `docs://{category}/{topic}` | Content of a specific documentation file |
