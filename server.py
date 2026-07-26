import os
import json
import engine
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

@app.get("/cmd")
def cmd_api(q: str, user: str = "default"):
    engine._SAVE = "/data/fishing_save_{}.json".format(user)
    engine.S = None
    return {"result": engine.cmd(q)}


@app.get("/cmd")
def cmd(q: str, user: str = "default"):
    return {"result": engine.cmd(q, user)}

@app.get("/mcp/fishing")
def mcp_fishing(q: str):
    return {"result": engine.cmd(q)}

@app.get("/mcp/info")
def mcp_info(request: Request):
    base = str(request.base_url).rstrip("/")
    return {"endpoint": f"{base}/mcp/fishing", "param": "q"}

# 标准 MCP Streamable HTTP 端点
MCP_TOOLS = [
    {
        "name": "fishing_cmd",
        "description": "向钓鱼游戏发送指令。常用指令：cast(钓鱼)、cast N(连钓N竿)、status(查看状态)、inventory(查看鱼篓)、sell all(卖出全部)、buy <id> <数量>(购买鱼饵)、goto <地点id>(前往地点)、encyclopedia(查看图鉴)、help(帮助)。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "游戏指令，如 cast、cast 10、status、sell all 等"
                }
            },
            "required": ["q"]
        }
    }
]

@app.get("/mcp")
async def mcp_get():
    return JSONResponse({
        "jsonrpc": "2.0",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "fishing", "version": "1.0.0"}
        }
    })

@app.post("/mcp")
async def mcp_post(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"jsonrpc":"2.0","id":None,"error":{"code":-32700,"message":"Parse error"}})

    method = body.get("method")
    req_id = body.get("id")

    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "fishing", "version": "1.0.0"}
            }
        })

    elif method == "notifications/initialized":
        return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": {}})

    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0", "id": req_id,
            "result": {"tools": MCP_TOOLS}
        })

    elif method == "tools/":
        params = body.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "fishing_cmd":
            q = args.get("q", "status")
            result = engine.cmd(q, "kiro")
            return JSONResponse({
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result}],
                    "isError": False
                }
            })
        else:
            return JSONResponse({
                "jsonrpc": "2.0", "id": req_id,
                "error": {"code": -32601, "message": f"Tool not found: {name}"}
            })

    elif method == "ping":
        return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": {}})

    else:
        return JSONResponse({
            "jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
