import re

from server.app import mcp, CATEGORY_LABELS, markdown_files, parse_path, resolve_doc


@mcp.tool()
def list_docs(category: str | None = None) -> list[dict]:
    """
    Lists all available documentation files.

    Args:
        category: Optional filter by category folder name.
    """
    result = []
    for f in markdown_files():
        cat, topic = parse_path(f)
        if category and cat != category:
            continue
        result.append({
            "category": cat,
            "category_label": CATEGORY_LABELS.get(cat, cat),
            "topic": topic,
            "resource_uri": f"docs://{cat}/{topic}",
        })
    return result


@mcp.tool()
def read_doc(category: str, topic: str) -> str:
    """
    Reads the full content of a documentation file.

    Args:
        category: The category folder name.
        topic: The topic name within the category.
    """
    return resolve_doc(category, topic).read_text(encoding="utf-8")


@mcp.tool()
def search_docs(query: str, category: str | None = None) -> list[dict]:
    """
    Searches documentation by keyword matching. Tokenizes the query and scores
    each document by term occurrence (title matches count 3x more). Returns the
    5 most relevant documents with full Markdown content.

    Args:
        query: Natural language query or keywords.
        category: Optional category filter.
    """
    tokens = [t for t in re.sub(r"[^\w\s]", " ", query.lower()).split() if len(t) > 2]
    if not tokens:
        return []

    results = []
    for f in markdown_files():
        cat, topic = parse_path(f)
        if category and cat != category:
            continue
        content = f.read_text(encoding="utf-8")
        content_lower = content.lower()

        score = 0
        for token in tokens:
            score += content_lower.count(token)
            for line in content_lower.splitlines():
                if line.startswith("#") and token in line:
                    score += 3

        if score > 0:
            results.append({
                "category": cat,
                "topic": topic,
                "resource_uri": f"docs://{cat}/{topic}",
                "score": score,
                "content": content,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]
