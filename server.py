import os
import engine
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("钓鱼游戏")

@mcp.tool()
def play_fishing(command: str) -> str:
    """
    钓鱼游戏指令。
    常用：status / shop / cast / cast 10 / cast 10 stop=rare /
    buy basic_worm 5 / goto / goto reed_river / sell all /
    inventory / encyclopedia / help
    多指令用分号：buy basic_worm 10; cast 10
    """
    return engine.cmd(command)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
