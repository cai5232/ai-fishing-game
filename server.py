import os
import json
import engine
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

# ── MCP endpoint ──
@app.get("/mcp/fishing")
def mcp_fishing(q: str):
    return {"result": engine.cmd(q)}

@app.get("/mcp/info")
def mcp_info(request: Request):
    base = str(request.base_url).rstrip("/")
    return {
        "name": "fishing",
        "description": "钓鱼游戏工具，用 cmd 指令操作共享存档",
        "endpoint": f"{base}/mcp/fishing",
        "param": "q",
        "example": f"{base}/mcp/fishing?q=cast"
    }

HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Fishing">
<meta name="mobile-web-app-capable" content="yes">
<title>Fishing</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
  body {
    background: #fff; color: #111;
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    height: 100svh; display: flex; flex-direction: column;
    overflow: hidden; position: relative;
  }
  #main { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
  #topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 20px 10px; border-bottom: 1px solid #f0f0f0;
    flex-shrink: 0; gap: 12px;
  }
  #topbar-left { display: flex; align-items: center; gap: 14px; flex: 1; min-width: 0; }
  #title { font-size: 28px; font-weight: 700; letter-spacing: -1px; line-height: 1; color: #111; flex-shrink: 0; }
  #stats { display: flex; gap: 0; align-items: center; flex: 1; min-width: 0; }
  .stat-item { display: flex; flex-direction: column; align-items: center; flex: 1; min-width: 0; }
  .stat-val { font-size: 13px; font-weight: 600; color: #111; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
  .stat-label { font-size: 9px; color: #aaa; letter-spacing: 0.3px; line-height: 1.2; white-space: nowrap; }
  .stat-divider { width: 1px; height: 24px; background: #e8e8e8; flex-shrink: 0; }
  #topbar-right { display: flex; gap: 14px; align-items: center; flex-shrink: 0; }
  .icon-btn {
    background: none; border: none; cursor: pointer; color: #111;
    padding: 8px; display: flex; align-items: center; justify-content: center;
    border-radius: 50%; margin: -4px;
  }
  .icon-btn:active { background: #f0f0f0; }
  .icon-btn svg { width: 22px; height: 22px; display: block; }
  #output { flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 10px; }
  .msg-wrap { display: flex; flex-direction: column; gap: 2px; }
  .msg-card {
    background: #f7f7f7; border-radius: 14px; padding: 12px 14px;
    font-size: 13.5px; line-height: 1.7; color: #222;
    white-space: pre-wrap; word-break: break-all; font-family: monospace;
  }
  #quick-btns {
    display: flex; gap: 8px; padding: 8px 20px;
    overflow-x: auto; flex-shrink: 0;
    border-top: 1px solid #f0f0f0; scrollbar-width: none;
  }
  #quick-btns::-webkit-scrollbar { display: none; }
  .qbtn {
    background: #f2f2f2; color: #333; border: none;
    border-radius: 20px; padding: 6px 14px; font-size: 13px;
    white-space: nowrap; cursor: pointer; flex-shrink: 0; font-family: inherit;
  }
  .qbtn:active { background: #e0e0e0; }
  #input-row {
    display: flex; gap: 10px; padding: 10px 20px;
    padding-bottom: max(20px, env(safe-area-inset-bottom));
    border-top: 1px solid #f0f0f0; flex-shrink: 0;
  }
  #cmd-input {
    flex: 1; background: #f2f2f2; color: #111; border: none;
    border-radius: 22px; padding: 10px 16px; font-size: 14px;
    font-family: monospace; outline: none;
  }
  #send-btn {
    background: #111; color: #fff; border: none; border-radius: 22px;
    padding: 10px 20px; font-size: 14px; cursor: pointer; font-family: inherit; flex-shrink: 0;
  }
  #send-btn:active { background: #333; }

  /* ── 全屏页 ── */
  .fullpage {
    display: none; position: fixed; inset: 0;
    background: #f2f2f7; z-index: 200;
    flex-direction: column; overflow: hidden;
  }
  .fullpage.open { display: flex; }
  .fp-nav {
    display: flex; align-items: center;
    padding: 56px 20px 10px; background: #f2f2f7; flex-shrink: 0; gap: 8px;
  }
  .fp-back {
    background: none; border: none; cursor: pointer;
    color: #007aff; font-size: 16px; display: flex;
    align-items: center; gap: 4px; padding: 4px 0; font-family: inherit;
  }
  .fp-back svg { width: 18px; height: 18px; }
  .fp-title { font-size: 17px; font-weight: 600; color: #111; flex: 1; text-align: center; margin-right: 60px; }

  /* 设置页 */
  #settings-body {
    flex: 1; overflow-y: auto; padding: 0 0 40px;
    padding-bottom: max(40px, env(safe-area-inset-bottom));
  }
  .settings-title { font-size: 34px; font-weight: 700; padding: 8px 20px 16px; color: #111; }
  .account-card {
    margin: 0 16px 24px; background: #fff; border-radius: 14px;
    padding: 16px; display: flex; align-items: center; gap: 14px; cursor: pointer;
  }
  .account-card:active { background: #f5f5f5; }
  .account-avatar {
    width: 60px; height: 60px; border-radius: 50%;
    background: linear-gradient(135deg, #c9d6ff, #e2e2e2);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; flex-shrink: 0; overflow: hidden;
  }
  .account-info { flex: 1; min-width: 0; }
  .account-name { font-size: 20px; font-weight: 600; color: #111; }
  .account-sub { font-size: 13px; color: #888; margin-top: 2px; }
  .account-arrow { color: #c7c7cc; }
  .account-arrow svg { width: 18px; height: 18px; }
  .settings-group { margin: 0 16px 24px; background: #fff; border-radius: 14px; overflow: hidden; }
  .settings-row {
    display: flex; align-items: center; gap: 12px; padding: 12px 16px;
    cursor: pointer; border-bottom: 1px solid #f2f2f2; min-height: 50px;
  }
  .settings-row:last-child { border-bottom: none; }
  .settings-row:active { background: #f5f5f5; }
  .s-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .s-icon svg { width: 18px; height: 18px; color: #fff; }
  .s-label { flex: 1; font-size: 16px; color: #111; }
  .s-arrow { color: #c7c7cc; }
  .s-arrow svg { width: 16px; height: 16px; }

  /* 子页面占位 */
  .subpage-body { flex: 1; overflow-y: auto; padding: 16px; padding-bottom: max(40px, env(safe-area-inset-bottom)); }
  .subpage-empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; color: #aaa; }
  .subpage-empty .ep-icon { font-size: 48px; }
  .subpage-empty .ep-text { font-size: 15px; }

  /* 蓝牙/MCP页面 */
  .mcp-card {
    background: #fff; border-radius: 14px; padding: 20px; margin-bottom: 16px;
  }
  .mcp-card h3 { font-size: 15px; font-weight: 600; color: #111; margin-bottom: 6px; }
  .mcp-card p { font-size: 13px; color: #888; margin-bottom: 14px; line-height: 1.5; }
  .mcp-url {
    background: #f2f2f7; border-radius: 10px; padding: 12px 14px;
    font-family: monospace; font-size: 12px; color: #333;
    word-break: break-all; margin-bottom: 12px; line-height: 1.6;
  }
  .mcp-copy-btn {
    background: #007aff; color: #fff; border: none; border-radius: 10px;
    padding: 10px 20px; font-size: 14px; cursor: pointer; font-family: inherit; width: 100%;
  }
  .mcp-copy-btn:active { background: #0062cc; }
  .mcp-copy-btn.copied { background: #34c759; }
  .mcp-badge {
    display: inline-block; background: #34c75922; color: #34c759;
    font-size: 11px; padding: 2px 8px; border-radius: 20px; margin-left: 8px; font-weight: 600;
  }
</style>
</head>
<body>

<!-- 主页面 -->
<div id="main">
  <div id="topbar">
    <div id="topbar-left">
      <div id="title">Fishing</div>
      <div id="stats">
        <div class="stat-item"><span class="stat-val" id="stat-pts">—</span><span class="stat-label">点数</span></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><span class="stat-val" id="stat-loc">—</span><span class="stat-label">地图</span></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><span class="stat-val" id="stat-turn">—</span><span class="stat-label">回合</span></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><span class="stat-val" id="stat-enc">—</span><span class="stat-label">图鉴</span></div>
      </div>
    </div>
    <div id="topbar-right">
      <button class="icon-btn" onclick="openSettings()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
      </button>
    </div>
  </div>
  <div id="output"></div>
  <div id="quick-btns">
    <button class="qbtn" onclick="send('status')">状态</button>
    <button class="qbtn" onclick="send('cast')">钓一竿</button>
    <button class="qbtn" onclick="send('cast 10')">钓10竿</button>
    <button class="qbtn" onclick="send('inventory')">鱼篓</button>
    <button class="qbtn" onclick="send('help')">帮助</button>
  </div>
  <div id="input-row">
    <input id="cmd-input" placeholder="输入指令，如 cast / buy basic_worm 5" onkeydown="if(event.key==='Enter')send()">
    <button id="send-btn" onclick="send()">发送</button>
  </div>
</div>

<!-- 设置页 -->
<div id="page-settings" class="fullpage">
  <div style="position:absolute;top:16px;right:20px;z-index:10;">
    <button class="icon-btn" onclick="closeSettings()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:20px;height:20px"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  </div>
  <div id="settings-body">
    <div class="settings-title">设置</div>
    <div class="account-card" onclick="switchAccount()">
      <div class="account-avatar" id="account-avatar">🎣</div>
      <div class="account-info">
        <div class="account-name" id="account-name">钓鱼佬</div>
        <div class="account-sub">点击切换账号</div>
      </div>
      <div class="account-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="settings-group">
      <div class="settings-row" onclick="openSubpage('shop')">
        <div class="s-icon" style="background:#ff9500"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg></div>
        <span class="s-label">商店</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('wallet')">
        <div class="s-icon" style="background:#34c759"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="3"/><path d="M16 3H6a2 2 0 0 0-2 2v2"/><circle cx="17" cy="14" r="1.5" fill="currentColor" stroke="none"/></svg></div>
        <span class="s-label">钱包</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('encyclopedia')">
        <div class="s-icon" style="background:#007aff"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div>
        <span class="s-label">图鉴</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('sell')">
        <div class="s-icon" style="background:#ff3b30"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
        <span class="s-label">卖鱼</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('bluetooth')">
        <div class="s-icon" style="background:#5856d6"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"/></svg></div>
        <span class="s-label">蓝牙</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
    </div>
  </div>
</div>

<!-- 子页面 -->
<div id="page-sub" class="fullpage">
  <div class="fp-nav">
    <button class="fp-back" onclick="closeSubpage()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
      设置
    </button>
    <div class="fp-title" id="subpage-title">—</div>
  </div>
  <div class="subpage-body" id="subpage-body">
    <div class="subpage-empty">
      <div class="ep-icon" id="subpage-icon">🚧</div>
      <div class="ep-text">即将上线</div>
    </div>
  </div>
</div>

<script>
const output = document.getElementById('output');
const input  = document.getElementById('cmd-input');
const ledger = [];
const BASE = window.location.origin;

const accounts = [
  { name: '钓鱼佬', avatar: '🎣' },
  { name: '小克', avatar: '🐟' },
];
let currentAccount = 0;

function switchAccount() {
  currentAccount = (currentAccount + 1) % accounts.length;
  const a = accounts[currentAccount];
  document.getElementById('account-name').textContent = a.name;
  document.getElementById('account-avatar').textContent = a.avatar;
}

function parseStats(text) {
  const m = text.match(/📊\\s*(\\{.*\\})/);
  if (!m) return null;
  try { return JSON.parse(m[1]); } catch { return null; }
}
function cleanOutput(text) {
  return text.replace(/\\n?📊\\s*\\{.*\\}\\s*$/, '').trim();
}
function updateTopbar(s) {
  if (!s) return;
  document.getElementById('stat-pts').textContent  = s.pts  ?? '—';
  document.getElementById('stat-loc').textContent  = s.loc  ?? '—';
  document.getElementById('stat-turn').textContent = s.turn ?? '—';
  document.getElementById('stat-enc').textContent  = s.enc  ?? '—';
}
function recordLedger(cmd, before, after) {
  if (!before || !after) return;
  const diff = (after.pts ?? 0) - (before.pts ?? 0);
  if (diff === 0) return;
  ledger.push({ cmd, diff, pts: after.pts });
}
let lastStats = null;

async function send(cmd) {
  const q = cmd || input.value.trim();
  if (!q) return;
  input.value = '';
  const before = lastStats;
  const wrap = document.createElement('div'); wrap.className = 'msg-wrap';
  const card = document.createElement('div'); card.className = 'msg-card';
  card.textContent = '…';
  wrap.appendChild(card); output.appendChild(wrap);
  output.scrollTop = output.scrollHeight;
  try {
    const r = await fetch('/cmd?q=' + encodeURIComponent(q));
    const d = await r.json();
    const s = parseStats(d.result);
    card.textContent = cleanOutput(d.result);
    if (s) { recordLedger(q, before, s); updateTopbar(s); lastStats = s; }
  } catch(e) { card.textContent = '请求失败：' + e; }
  output.scrollTop = output.scrollHeight;
}

function openSettings() { document.getElementById('page-settings').classList.add('open'); }
function closeSettings() { document.getElementById('page-settings').classList.remove('open'); }

const subpageInfo = {
  shop:         { title: '商店', render: renderEmpty('🛒') },
  wallet:       { title: '钱包', render: renderWallet },
  encyclopedia: { title: '图鉴', render: renderEmpty('📖') },
  sell:         { title: '卖鱼', render: renderEmpty('💸') },
  bluetooth:    { title: '蓝牙', render: renderBluetooth },
};

function renderEmpty(icon) {
  return function(body) {
    body.innerHTML = '<div class="subpage-empty"><div class="ep-icon">' + icon + '</div><div class="ep-text">即将上线</div></div>';
  };
}

function renderWallet(body) {
  const total = lastStats?.pts ?? '—';
  let rows = ledger.length === 0
    ? '<div class="wallet-row"><span class="label">暂无明细</span><span class="amount">—</span></div>'
    : ledger.slice().reverse().map(e =>
        '<div class="wallet-row"><span class="label">' + e.cmd + '</span>' +
        '<span class="amount ' + (e.diff < 0 ? 'neg' : '') + '">' + (e.diff > 0 ? '+' : '') + e.diff + ' pts</span></div>'
      ).join('');
  body.innerHTML =
    '<div class="mcp-card">' +
    '<h3>当前余额</h3>' +
    '<div style="font-size:36px;font-weight:700;color:#111;margin:8px 0 16px">' + total + ' <span style="font-size:16px;color:#aaa">pts</span></div>' +
    rows + '</div>';
}

function renderBluetooth(body) {
  const cmdUrl  = BASE + '/mcp/fishing?q={指令}';
  const infoUrl = BASE + '/mcp/info';
  body.innerHTML =
    '<div class="mcp-card">' +
    '<h3>AI 接入 · MCP 工具 <span class="mcp-badge">已上线</span></h3>' +
    '<p>把下面的接口地址配置到 AI 的 MCP 工具里，AI 就能直接操作这个钓鱼存档，和你共享进度。</p>' +
    '<div style="font-size:12px;color:#aaa;margin-bottom:6px">指令接口（GET）</div>' +
    '<div class="mcp-url">' + BASE + '/mcp/fishing?q=cast</div>' +
    '<button class="mcp-copy-btn" id="copy-cmd-btn" onclick="copyUrl(\'' + BASE + '/mcp/fishing\', \'copy-cmd-btn\')">复制指令接口</button>' +
    '</div>' +
    '<div class="mcp-card">' +
    '<h3>工具说明</h3>' +
    '<p>参数 <code style="background:#f2f2f7;padding:2px 6px;border-radius:4px">q</code> 传入钓鱼指令字符串，如 <code style="background:#f2f2f7;padding:2px 6px;border-radius:4px">cast</code>、<code style="background:#f2f2f7;padding:2px 6px;border-radius:4px">status</code>、<code style="background:#f2f2f7;padding:2px 6px;border-radius:4px">buy basic_worm 5</code>，返回 JSON <code style="background:#
