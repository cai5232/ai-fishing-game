import os
import engine
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🎣 钓鱼游戏</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0d1117; color: #c9d1d9; font-family: monospace; height: 100vh; display: flex; flex-direction: column; }
#output { flex: 1; overflow-y: auto; padding: 12px; white-space: pre-wrap; font-size: 14px; line-height: 1.6; }
.line { margin-bottom: 8px; }
.cmd-line { color: #58a6ff; }
.res-line { color: #c9d1d9; }
#quick-btns { display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 12px; border-top: 1px solid #21262d; }
#quick-btns button { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; padding: 4px 10px; font-size: 13px; cursor: pointer; }
#quick-btns button:active { background: #388bfd22; }
#input-row { display: flex; gap: 8px; padding: 10px 12px; border-top: 1px solid #21262d; }
#cmd-input { flex: 1; background: #161b22; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; font-size: 14px; font-family: monospace; }
#send-btn { background: #238636; color: #fff; border: none; border-radius: 6px; padding: 8px 16px; font-size: 14px; cursor: pointer; }
#send-btn:active { background: #2ea043; }
</style>
</head>
<body>
<div id="output"><div class="line res-line">🎣 欢迎来到钓鱼游戏！输入指令或点下方快捷键开始～</div></div>
<div id="quick-btns">
  <button onclick="send('status')">状态</button>
  <button onclick="send('cast')">钓一竿</button>
  <button onclick="send('cast 10')">钓10竿</button>
  <button onclick="send('shop')">商店</button>
  <button onclick="send('goto')">钓点</button>
  <button onclick="send('inventory')">渔篓</button>
  <button onclick="send('sell all')">卖鱼</button>
  <button onclick="send('encyclopedia')">图鉴</button>
  <button onclick="send('help')">帮助</button>
</div>
<div id="input-row">
  <input id="cmd-input" placeholder="输入指令，如 cast / buy basic_worm 5" onkeydown="if(event.key==='Enter')send()">
  <button id="send-btn" onclick="send()">发送</button>
</div>
<script>
const output = document.getElementById('output');
const input = document.getElementById('cmd-input');
async function send(cmd) {
  const q = cmd || input.value.trim();
  if (!q) return;
  input.value = '';
  appendLine('▶ ' + q, 'cmd-line');
  try {
    const r = await fetch('/cmd?q=' + encodeURIComponent(q));
    const d = await r.json();
    appendLine(d.result, 'res-line');
  } catch(e) {
    appendLine('请求失败：' + e, 'res-line');
  }
  output.scrollTop = output.scrollHeight;
}
function appendLine(text, cls) {
  const div = document.createElement('div');
  div.className = 'line ' + cls;
  div.textContent = text;
  output.appendChild(div);
}
send('status');
</script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML

@app.get("/cmd")
def cmd(q: str):
    return {"result": engine.cmd(q)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
