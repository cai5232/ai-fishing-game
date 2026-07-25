import os
import engine
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/cmd")
def cmd(q: str):
    return {"result": engine.cmd(q)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
