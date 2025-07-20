from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("hello_mcp")

# Constants
@mcp.tool()
async def say_hello(state: str) -> str:
    """Get message from for Hello mcp.

    Args:
        name: skjun
    """
    return "\n---\n".join("MCP세상에 오신걸 환영합니다. skjun")

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

