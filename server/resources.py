from server.app import mcp, CATEGORY_LABELS, markdown_files, parse_path, resolve_doc, _project_name


@mcp.resource("docs://index")
def get_docs_index() -> str:
    """Complete index of all available documentation files."""
    lines = [f"# {_project_name} Documentation Index\n"]
    current_cat = None
    for f in markdown_files():
        cat, topic = parse_path(f)
        if cat != current_cat:
            current_cat = cat
            lines.append(f"\n## {CATEGORY_LABELS.get(cat, cat)}")
        lines.append(f"- docs://{cat}/{topic}")
    return "\n".join(lines)


@mcp.resource("docs://{category}/{topic}")
def get_doc(category: str, topic: str) -> str:
    """Content of a specific documentation file."""
    return resolve_doc(category, topic).read_text(encoding="utf-8")
