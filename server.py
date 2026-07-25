import os
import engine
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fishing")

@mcp.tool()
def play_fishing(command: str) -> str:
    """fishing game command"""
    return engine.cmd(command)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
