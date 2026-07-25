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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Fishing">
<meta name="mobile-web-app-capable" content="yes">
<title>Fishing</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
  body {
    background: #fff;
    color: #111;
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    height: 100svh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }

  /* ── 主页面 ── */
  #main {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow: hidden;
  }

  #topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 20px 10px;
    border-bottom: 1px solid #f0f0f0;
    flex-shrink: 0;
    gap: 12px;
  }
  #topbar-left { display: flex; align-items: center; gap: 14px; flex: 1; min-width: 0; }
  #title {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    color: #111;
    flex-shrink: 0;
  }
  #stats { display: flex; gap: 0; align-items: center; flex: 1; min-width: 0; }
  .stat-item { display: flex; flex-direction: column; align-items: center; flex: 1; min-width: 0; }
  .stat-val {
    font-size: 13px; font-weight: 600; color: #111;
    line-height: 1.2; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis; max-width: 100%;
  }
  .stat-label { font-size: 9px; color: #aaa; letter-spacing: 0.3px; line-height: 1.2; white-space: nowrap; }
  .stat-divider { width: 1px; height: 24px; background: #e8e8e8; flex-shrink: 0; }
  #topbar-right { display: flex; gap: 14px; align-items: center; flex-shrink: 0; }

  .icon-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #111;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    margin: -4px;
  }
  .icon-btn:active { background: #f0f0f0; }
  .icon-btn svg { width: 22px; height: 22px; display: block; }

  #output {
    flex: 1; overflow-y: auto;
    padding: 16px 20px;
    display: flex; flex-direction: column; gap: 10px;
  }
  .msg-wrap { display: flex; flex-direction: column; gap: 2px; }
  .msg-card {
    background: #f7f7f7; border-radius: 14px;
    padding: 12px 14px; font-size: 13.5px;
    line-height: 1.7; color: #222;
    white-space: pre-wrap; word-break: break-all;
    font-family: monospace;
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
    white-space: nowrap; cursor: pointer; flex-shrink: 0;
    font-family: inherit; -webkit-tap-highlight-color: transparent;
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
    background: #111; color: #fff; border: none;
    border-radius: 22px; padding: 10px 20px; font-size: 14px;
    cursor: pointer; font-family: inherit; flex-shrink: 0;
  }
  #send-btn:active { background: #333; }

  /* ── 全屏覆盖页（设置/子页面） ── */
  .fullpage {
    display: none;
    position: fixed;
    inset: 0;
    background: #f2f2f7;
    z-index: 200;
    flex-direction: column;
    overflow: hidden;
  }
  .fullpage.open { display: flex; }

  .fp-nav {
    display: flex;
    align-items: center;
    padding: 16px 20px 10px;
    background: #f2f2f7;
    flex-shrink: 0;
    gap: 8px;
  }
  .fp-back {
    background: none; border: none; cursor: pointer;
    color: #007aff; font-size: 16px; display: flex;
    align-items: center; gap: 4px; padding: 4px 0;
    font-family: inherit;
  }
  .fp-back svg { width: 18px; height: 18px; }
  .fp-title {
    font-size: 17px; font-weight: 600; color: #111;
    flex: 1; text-align: center; margin-right: 60px;
  }

  /* ── 设置页专属 ── */
  #settings-body {
    flex: 1; overflow-y: auto;
    padding: 0 0 40px;
    padding-bottom: max(40px, env(safe-area-inset-bottom));
  }

  .settings-title {
    font-size: 34px; font-weight: 700;
    padding: 8px 20px 16px; color: #111;
  }

  /* 账户卡片 */
  .account-card {
    margin: 0 16px 24px;
    background: #fff;
    border-radius: 14px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }
  .account-card:active { background: #f5f5f5; }
  .account-avatar {
    width: 60px; height: 60px; border-radius: 50%;
    background: linear-gradient(135deg, #c9d6ff, #e2e2e2);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; flex-shrink: 0; overflow: hidden;
  }
  .account-avatar img { width: 100%; height: 100%; object-fit: cover; }
  .account-info { flex: 1; min-width: 0; }
  .account-name { font-size: 20px; font-weight: 600; color: #111; }
  .account-sub { font-size: 13px; color: #888; margin-top: 2px; }
  .account-arrow { color: #c7c7cc; }
  .account-arrow svg { width: 18px; height: 18px; }

  /* 设置分组 */
  .settings-group {
    margin: 0 16px 24px;
    background: #fff;
    border-radius: 14px;
    overflow: hidden;
  }
  .settings-row {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 16px; cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    border-bottom: 1px solid #f2f2f2;
    min-height: 50px;
  }
  .settings-row:last-child { border-bottom: none; }
  .settings-row:active { background: #f5f5f5; }
  .s-icon {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .s-icon svg { width: 18px; height: 18px; color: #fff; }
  .s-label { flex: 1; font-size: 16px; color: #111; }
  .s-arrow { color: #c7c7cc; }
  .s-arrow svg { width: 16px; height: 16px; }

  /* ── 子页面空占位 ── */
  .subpage-empty {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 12px;
    color: #aaa;
  }
  .subpage-empty .ep-icon { font-size: 48px; }
  .subpage-empty .ep-text { font-size: 15px; }

  /* ── 余额弹窗 ── */
  #wallet-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.15); z-index: 300;
    align-items: flex-end; justify-content: center;
  }
  #wallet-overlay.open { display: flex; }
  #wallet-sheet {
    background: #fff; border-radius: 20px 20px 0 0;
    padding: 24px 24px 40px; width: 100%;
    max-width: 480px; max-height: 60vh; overflow-y: auto;
  }
  #wallet-sheet h2 {
    font-size: 18px; font-weight: 700; margin-bottom: 18px;
    display: flex; justify-content: space-between; align-items: center;
  }
  #wallet-sheet h2 button {
    background: none; border: none; font-size: 20px;
    cursor: pointer; color: #aaa; line-height: 1;
  }
  .wallet-total { font-size: 32px; font-weight: 700; color: #111; margin-bottom: 20px; }
  .wallet-total span { font-size: 16px; font-weight: 400; color: #aaa; margin-left: 4px; }
  .wallet-row {
    display: flex; justify-content: space-between;
    padding: 10px 0; border-bottom: 1px solid #f2f2f2; font-size: 14px;
  }
  .wallet-row .label { color: #555; }
  .wallet-row .amount { font-weight: 600; color: #111; }
  .wallet-row .amount.neg { color: #e55; }
</style>
</head>
<body>

<!-- ══ 主页面 ══ -->
<div id="main">
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
      <button class="icon-btn" ontouchend="openSettings()" onclick="openSettings()" title="设置">
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
    <input id="cmd-input" placeholder="输入指令，如 cast / buy basic_worm 5"
      onkeydown="if(event.key==='Enter')send()">
    <button id="send-btn" onclick="send()">发送</button>
  </div>
</div>

<!-- ══ 设置页 ══ -->
<div id="page-settings" class="fullpage">
  <div id="settings-body">
    <div class="settings-title">设置</div>

    <!-- 账户卡片 -->
    <div class="account-card" onclick="switchAccount()">
      <div class="account-avatar" id="account-avatar">🎣</div>
      <div class="account-info">
        <div class="account-name" id="account-name">钓鱼佬</div>
        <div class="account-sub">点击切换账号</div>
      </div>
      <div class="account-arrow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
      </div>
    </div>

    <!-- 功能分组 -->
    <div class="settings-group">
      <div class="settings-row" onclick="openSubpage('shop')">
        <div class="s-icon" style="background:#ff9500">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        </div>
        <span class="s-label">商店</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('wallet')">
        <div class="s-icon" style="background:#34c759">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="3"/><path d="M16 3H6a2 2 0 0 0-2 2v2"/><circle cx="17" cy="14" r="1.5" fill="currentColor" stroke="none"/></svg>
        </div>
        <span class="s-label">钱包</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('encyclopedia')">
        <div class="s-icon" style="background:#007aff">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        </div>
        <span class="s-label">图鉴</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <div class="settings-row" onclick="openSubpage('sell')">
        <div class="s-icon" style="background:#ff3b30">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
        <span class="s-label">卖鱼</span>
        <div class="s-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
    </div>
  </div>

  <!-- 设置页关闭按钮（右上角） -->
  <div style="position:absolute;top:16px;right:20px;">
    <button class="icon-btn" onclick="closeSettings()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:20px;height:20px"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  </div>
</div>

<!-- ══ 子页面（商店/钱包/图鉴/卖鱼） ══ -->
<div id="page-sub" class="fullpage">
  <div class="fp-nav">
    <button class="fp-back" onclick="closeSubpage()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
      设置
    </button>
    <div class="fp-title" id="subpage-title">—</div>
  </div>
  <div class="subpage-empty">
    <div class="ep-icon" id="subpage-icon">🚧</div>
    <div class="ep-text">即将上线</div>
  </div>
</div>

<!-- ══ 余额弹窗 ══ -->
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
const ledger = [];

// 账号列表
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
  const m = text.match(/📊\s*(\{.*\})/);
  if (!m) return null;
  try { return JSON.parse(m[1]); } catch { return null; }
}

function cleanOutput(text) {
  return text.replace(/\n?📊\s*\{.*\}\s*$/, '').trim();
}

function updateTopbar(s) {
  if (!s) return;
  document.getElementById('stat-pts').textContent  = s.pts  ?? '—';
  document.getElementById('stat-loc').textContent  = s.loc  ?? '—';
  document.getElementById('stat-turn').textContent = s.turn ?? '—';
  document.getElementById('stat-enc').textContent  = s.enc  ?? '—';
}

function recordLedger(cmd, statsBefore, statsAfter) {
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
  const card = document.createElement('div');
  card.className = 'msg-card';
  card.textContent = '…';
  wrap.appendChild(card);
  output.appendChild(wrap);
  output.scrollTop = output.scrollHeight;
  try {
    const r = await fetch('/cmd?q=' + encodeURIComponent(q));
    const d = await r.json();
    const s = parseStats(d.result);
    card.textContent = cleanOutput(d.result);
    if (s) { recordLedger(q, statsBefore, s); updateTopbar(s); lastStats = s; }
  } catch(e) {
    card.textContent = '请求失败：' + e;
  }
  output.scrollTop = output.scrollHeight;
}

// 设置页
function openSettings() {
  document.getElementById('page-settings').classList.add('open');
}
function closeSettings() {
  document.getElementById('page-settings').classList.remove('open');
}

// 子页面
const subpageInfo = {
  shop:         { title: '商店',   icon: '🛒' },
  wallet:       { title: '钱包',   icon: '💰' },
  encyclopedia: { title: '图鉴',   icon: '📖' },
  sell:         { title: '卖鱼',   icon: '💸' },
};
function openSubpage(key) {
  const info = subpageInfo[key] || { title: key, icon: '🚧' };
  document.getElementById('subpage-title').textContent = info.title;
  document.getElementById('subpage-icon').textContent  = info.icon;
  document.getElementById('page-sub').classList.add('open');
}
function closeSubpage() {
  document.getElementById('page-sub').classList.remove('open');
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
      '<div class="wallet-row"><span class="label">' + e.cmd + '</span><span class="amount ' +
      (e.diff < 0 ? 'neg' : '') + '">' + (e.diff > 0 ? '+' : '') + e.diff + ' pts</span></div>'
    ).join('');
  }
  document.getElementById('wallet-overlay').classList.add('open');
}
function closeWallet(e) {
  if (!e || e.target === document.getElementById('wallet-overlay'))
    document.getElementById('wallet-overlay').classList.remove('open');
}

// 初始化，带重试
async function init() {
  try {
    const r = await fetch('/cmd?q=status');
    const d = await r.json();
    const s = parseStats(d.result);
    const card = document.createElement('div');
    card.className = 'msg-card';
    card.textContent = cleanOutput(d.result);
    const wrap = document.createElement('div');
    wrap.className = 'msg-wrap';
    wrap.appendChild(card
