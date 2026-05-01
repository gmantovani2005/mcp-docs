import argparse
from server.app import mcp
import server.tools
import server.resources


def main():
    parser = argparse.ArgumentParser(description="MCP Documentation Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for network transports (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6060,
        help="Port for network transports (default: 6060)",
    )
    args = parser.parse_args()

    if args.transport in ("sse", "streamable-http"):
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        base = f"http://{args.host}:{args.port}"
        endpoint = "/sse" if args.transport == "sse" else "/mcp"
        print(f"MCP server running at {base}{endpoint}", flush=True)

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
