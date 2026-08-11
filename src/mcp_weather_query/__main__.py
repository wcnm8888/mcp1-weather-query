"""Run the local MCP server over the SDK's default stdio transport."""

from mcp_weather_query.server import mcp


def main() -> None:
    """Block on MCP stdio; the Host owns stdin and stdout."""
    mcp.run()


if __name__ == "__main__":
    main()
