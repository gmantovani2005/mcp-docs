import tomllib
from mcp.server.fastmcp import FastMCP
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

if not DOCS_DIR.exists():
    raise SystemExit(
        f"Error: docs/ directory not found at {DOCS_DIR}\n"
        "Clone the documentation repository into docs/ before starting the server."
    )

_CONFIG_FILE = DOCS_DIR / "config.toml"
_ROOT = Path(__file__).parent.parent


def _load_config() -> dict:
    if _CONFIG_FILE.exists():
        with _CONFIG_FILE.open("rb") as f:
            return tomllib.load(f)
    return {}


_config = _load_config()
_project_section = _config.get("project", {})
_project_name: str = _project_section.get("name", _ROOT.name)
_default_instructions = (
    f"This server provides access to the {_project_name} documentation. "
    "Use the available tools to search and read documentation and answer user questions accurately."
)
_instructions: str = _project_section.get("instructions", _default_instructions).strip()
_config_labels: dict[str, str] = _config.get("categories", {})


def _discover_categories() -> dict[str, str]:
    discovered = {
        d.name: d.name.replace("-", " ").replace("_", " ").title()
        for d in sorted(DOCS_DIR.iterdir())
        if d.is_dir() and d.name != "img"
    }
    discovered.update(_config_labels)
    return discovered


CATEGORY_LABELS: dict[str, str] = _discover_categories()

mcp = FastMCP(_project_name, instructions=_instructions)


def markdown_files() -> list[Path]:
    return sorted(p for p in DOCS_DIR.rglob("*.md") if "img" not in p.parts)


def parse_path(path: Path) -> tuple[str, str]:
    """Returns (category, topic) from a docs path."""
    relative = path.relative_to(DOCS_DIR)
    parts = relative.parts
    topic = "/".join(parts[1:]).removesuffix(".md")
    return parts[0], topic


def resolve_doc(category: str, topic: str) -> Path:
    resolved = (DOCS_DIR / category / f"{topic}.md").resolve()
    if not str(resolved).startswith(str(DOCS_DIR.resolve())):
        raise ValueError(f"Invalid path: {category}/{topic}")
    if not resolved.exists():
        raise FileNotFoundError(f"Documentation not found: {category}/{topic}")
    return resolved
