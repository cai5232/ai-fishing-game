import os
import engine
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """import os
import engine
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import json, re

app = FastAPI()

HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Fishing</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: #fff;
    color: #111;
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* ── 顶栏 ── */
  #topbar {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 18px 20px 10px;
    border-bottom: 1px solid #f0f0f0;
    flex-shrink: 0;
  }

  #topbar-left { display: flex; align-items: flex-end; gap: 14px; }

  #title {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    color: #111;
  }

  #stats {
    display: flex;
    gap: 10px;
    align-items: flex-end;
    padding-bottom: 3px;
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1px;
  }

  .stat-val {
    font-size: 13px;
    font-weight: 600;
    color: #111;
    line-height: 1;
  }

  .stat-label {
    font-size: 9px;
    color: #aaa;
    letter-spacing: 0.3px;
    line-height: 1;
  }

  .stat-divider {
    width: 1px;
    height: 20px;
    background: #e8e8e8;
    margin-bottom: 2px;
  }

  #topbar-right { display: flex; gap: 16px; align-items: center; }

  .icon-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #111;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .icon-btn svg { width: 22px; height: 22px; }

  /* ── 输出区 ── */
  #output {
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .msg-wrap { display: flex; flex-direction: column; gap: 2px; }

  .msg-cmd {
    font-size: 11px;
    color: #bbb;
    font-family: monospace;
  }

  .msg-card {
    background: #f7f7f7;
    border-radius: 14px;
    padding: 12px 14px;
    font-size: 13.5px;
    line-height: 1.7;
    color: #222;
    white-space: pre-wrap;
    word-break: break-all;
    font-family: monospace;
  }

  /* ── 快捷按钮 ── */
  #quick-btns {
    display: flex;
    gap: 8px;
    padding: 8px 20px;
    overflow-x: auto;
    flex-shrink: 0;
    border-top: 1px solid #f0f0f0;
    scrollbar-width: none;
  }
  #quick-btns::-webkit-scrollbar { display: none; }

  .qbtn {
    background: #f2f2f2;
    color: #333;
    border: none;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    white-space: nowrap;
    cursor: pointer;
    flex-shrink: 0;
    font-family: inherit;
  }
  .qbtn:active { background: #e0e0e0; }

  /* ── 输入栏 ── */
  #input-row {
    display: flex;
    gap: 10px;
    padding: 10px 20px 24px;
    border-top: 1px solid #f0f0f0;
    flex-shrink: 0;
  }

  #cmd-input {
    flex: 1;
    background: #f2f2f2;
    color: #111;
    border: none;
    border-radius: 22px;
    padding: 10px 16px;
    font-size: 14px;
    font-family: monospace;
    outline: none;
  }

  #send-btn {
    background: #111;
    color: #fff;
    border: none;
    border-radius: 22px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    font-family: inherit;
    flex-shrink: 0;
  }
  #send-btn:active { background: #333; }

  /* ── 余额弹窗 ── */
  #wallet-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.15);
    z-index: 100;
    align-items: flex-end;
    justify-content: center;
  }
  #wallet-overlay.open { display: flex; }

  #wallet-sheet {
    background: #fff;
    border-radius: 20px 20px 0 0;
    padding: 24px 24px 40px;
    width: 100%;
    max-width: 480px;
    max-height: 60vh;
    overflow-y: auto;
  }

  #wallet-sheet h2 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  #wallet-sheet h2 button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #aaa;
    line-height: 1;
  }

  .wallet-total {
    font-size: 32px;
    font-weight: 700;
    color: #111;
    margin-bottom: 20px;
  }

  .wallet-total span {
    font-size: 16px;
    font-weight: 400;
    color: #aaa;
    margin-left: 4px;
  }

  .wallet-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #f2f2f2;
    font-size: 14px;
  }

  .wallet-row .label { color: #555; }
  .wallet-row .amount { font-weight: 600; color: #111; }
  .wallet-row .amount.neg { color: #e55; }
</style>
</head>
<body>

<!-- 顶栏 -->
<div id="topbar">
  <div id="topbar-left">
    <div id="title">Fishing</div>
    <div id="stats">
      <div class="stat-item">
        <span class="stat-val" id="stat-pts">—</span>
        <span class="stat-label">点数</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-val" id="stat-loc">—</span>
        <span class="stat-label">地图</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-val" id="stat-turn">—</span>
        <span class="stat-label">回合</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-val" id="stat-enc">—</span>
        <span class="stat-label">图鉴</span>
      </div>
    </div>
  </div>
  <div id="topbar-right">
    <button class="icon-btn" onclick="openWallet()" title="余额">
      <!-- 钱包图标 -->
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="7" width="20" height="14" rx="3"/>
        <path d="M16 3H6a2 2 0 0 0-2 2v2"/>
        <circle cx="17" cy="14" r="1.5" fill="currentColor" stroke="none"/>
      </svg>
    </button>
    <button class="icon-btn" onclick="openSettings()" title="设置">
      <!-- 设置图标 -->
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
      </svg>
    </button>
  </div>
</div>

<!-- 输出区 -->
<div id="output"></div>

<!-- 快捷按钮 -->
<div id="quick-btns">
  <button class="qbtn" onclick="send('status')">状态</button>
  <button class="qbtn" onclick="send('cast')">钓一竿</button>
  <button class="qbtn" onclick="send('cast 10')">钓10竿</button>
  <button class="qbtn" onclick="send('shop')">商店</button>
  <button class="qbtn" onclick="send('goto')">钓点</button>
  <button class="qbtn" onclick="send('inventory')">渔篓</button>
  <button class="qbtn" onclick="send('sell all')">卖鱼</button>
  <button class="qbtn" onclick="send('encyclopedia')">图鉴</button>
  <button class="qbtn" onclick="send('help')">帮助</button>
</div>

<!-- 输入栏 -->
<div id="input-row">
  <input id="cmd-input" placeholder="输入指令，如 cast / buy basic_worm 5"
    onkeydown="if(event.key==='Enter')send()">
  <button id="send-btn" onclick="send()">发送</button>
</div>

<!-- 余额弹窗 -->
<div id="wallet-overlay" onclick="closeWallet(event)">
  <div id="wallet-sheet">
    <h2>余额明细 <button onclick="closeWallet()">×</button></h2>
    <div class="wallet-total" id="wallet-total">— <span>pts</span></div>
    <div id="wallet-rows">
      <div class="wallet-row">
        <span class="label">暂无明细数据</span>
        <span class="amount">—</span>
      </div>
    </div>
  </div>
</div>

<script>
const output = document.getElementById('output');
const input  = document.getElementById('cmd-input');

// 收入明细记录
const ledger = [];

function parseStats(text) {
  const m = text.match(/📊\s*(\{.*\})/);
  if (!m) return null;
  try { return JSON.parse(m[1]); } catch { return null; }
}

function updateTopbar(s) {
  if (!s) return;
  document.getElementById('stat-pts').textContent  = s.pts  ?? '—';
  document.getElementById('stat-loc').textContent  = s.loc  ?? '—';
  document.getElementById('stat-turn').textContent = s.turn ?? '—';
  document.getElementById('stat-enc').textContent  = s.enc  ?? '—';
}

function recordLedger(cmd, text, statsBefore, statsAfter) {
  if (!statsBefore || !statsAfter) return;
  const diff = (statsAfter.pts ?? 0) - (statsBefore.pts ?? 0);
  if (diff === 0) return;
  ledger.push({ cmd, diff, pts: statsAfter.pts });
}

let lastStats = null;

async function send(cmd) {
  const q = cmd || input.value.trim();
  if (!q) return;
  input.value = '';

  const statsBefore = lastStats;

  const wrap = document.createElement('div');
  wrap.className = 'msg-wrap';
  const cmdEl = document.createElement('div');
  cmdEl.className = 'msg-cmd';
  cmdEl.textContent = '▶ ' + q;
  const card = document.createElement('div');
  card.className = 'msg-card';
  card.textContent = '…';
  wrap.appendChild(cmdEl);
  wrap.appendChild(card);
  output.appendChild(wrap);
  output.scrollTop = output.scrollHeight;

  try {
    const r = await fetch('/cmd?q=' + encodeURIComponent(q));
    const d = await r.json();
    card.textContent = d.result;

    const s = parseStats(d.result);
    if (s) {
      recordLedger(q, d.result, statsBefore, s);
      updateTopbar(s);
      lastStats = s;
    }
  } catch(e) {
    card.textContent = '请求失败：' + e;
  }
  output.scrollTop = output.scrollHeight;
}

// 余额弹窗
function openWallet() {
  document.getElementById('wallet-total').innerHTML =
    (lastStats?.pts ?? '—') + ' <span>pts</span>';

  const rows = document.getElementById('wallet-rows');
  if (ledger.length === 0) {
    rows.innerHTML = '<div class="wallet-row"><span class="label">暂无明细</span><span class="amount">—</span></div>';
  } else {
    rows.innerHTML = ledger.slice().reverse().map(e =>
      `<div class="wallet-row">
        <span class="label">${e.cmd}</span>
        <span class="amount ${e.diff < 0 ? 'neg' : ''}">${e.diff > 0 ? '+' : ''}${e.diff} pts</span>
      </div>`
    ).join('');
  }
  document.getElementById('wallet-overlay').classList.add('open');
}

function closeWallet(e) {
  if (!e || e.target === document.getElementById('wallet-overlay')) {
    document.getElementById('wallet-overlay').classList.remove('open');
  }
}

function openSettings() {
  // 暂未实现，占位
  alert('设置页面即将上线');
}

// 初始化
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
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML

@app.get("/cmd")
def cmd(q: str):
    return {"result": engine.cmd(q)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
