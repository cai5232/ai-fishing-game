import os
import engine
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/cmd")
def cmd(q: str):
    return {"result": engine.cmd(q)}

@app.get("/mcp/fishing")
def mcp_fishing(q: str):
    return {"result": engine.cmd(q)}

@app.get("/mcp/info")
def mcp_info(request: Request):
    base = str(request.base_url).rstrip("/")
    return {"endpoint": f"{base}/mcp/fishing", "param": "q"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
