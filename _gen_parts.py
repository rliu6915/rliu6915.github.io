#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, os, re

from _blog_zoom import ZOOM_SNIPPET as ZOOM

_ROOT = os.path.dirname(os.path.abspath(__file__))

def _read_fragment(name: str) -> str:
    path = os.path.join(_ROOT, 'fragments', name)
    with open(path, encoding='utf-8') as f:
        return f.read()

_STYLE_PATH = '/tmp/_style.css'
if not os.path.isfile(_STYLE_PATH):
    _STYLE_PATH = os.path.join(_ROOT, 'blogs', 'hermes-gateway-p1.html')
    _raw = open(_STYLE_PATH, encoding='utf-8').read()
    _m = re.search(r'<style>(.*?)</style>', _raw, re.S)
    _style_blob = _m.group(1) if _m else ''
    _style_blob = re.sub(r'\.series\s*\{.*', '', _style_blob, flags=re.S)
    open('/tmp/_style.css', 'w', encoding='utf-8').write(_style_blob)
    _head_m = re.search(
        r'(<script src="https://cdn.jsdelivr.net/npm/mermaid.*?</script>\s*<script>document\.addEventListener.*?</script>)',
        _raw, re.S)
    open('/tmp/_head_script.html', 'w', encoding='utf-8').write(_head_m.group(1) if _head_m else '')

STYLE = open('/tmp/_style.css', encoding='utf-8').read()
HEAD  = open('/tmp/_head_script.html', encoding='utf-8').read()

FONTS = '<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">'

SERIES_CSS = """
    .series { margin-top: 56px; padding-top: 22px; border-top: 1px solid var(--border);
      font-family: Raleway, -apple-system, system-ui, sans-serif; font-size: 14px;
      color: var(--muted); text-align: center; line-height: 2; }
    .series a { color: var(--muted); text-decoration: none; }
    .series a:hover { color: var(--accent); }
    .series a.cur { color: var(--accent); font-weight: 600; }
"""

SRC_CSS = """
    .src-wrap { margin: 22px 0; }
    .src-bar { display: flex; justify-content: space-between; align-items: center;
      background: #161b22; border: 1px solid var(--border); border-bottom: none;
      border-radius: 10px 10px 0 0; padding: 7px 14px; }
    .src-lang { font-family: Raleway, -apple-system, system-ui, sans-serif;
      font-size: 12px; letter-spacing: .05em; text-transform: uppercase; color: var(--muted); }
    .src-copy { font-family: Raleway, -apple-system, system-ui, sans-serif;
      font-size: 12px; color: var(--muted); background: transparent;
      border: 1px solid var(--border); border-radius: 6px; padding: 3px 11px;
      cursor: pointer; transition: color .15s, border-color .15s; }
    .src-copy:hover { color: var(--accent); border-color: var(--accent); }
    pre.src { background: #0e1117; border: 1px solid var(--border); border-radius: 0 0 10px 10px;
      padding: 18px 20px; overflow-x: auto; margin: 0; }
    pre.src code { font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
      font-size: 13px; line-height: 1.7; color: #d7dde8; white-space: pre; }
    /* highlight.js token colors tuned to the block's dark theme */
    pre.src code.hljs { background: transparent; padding: 0; }
    pre.src .hljs-keyword, pre.src .hljs-built_in { color: #ff7b72; }
    pre.src .hljs-string, pre.src .hljs-comment { color: #a5d6ff; }
    pre.src .hljs-comment { font-style: italic; opacity: .8; }
    pre.src .hljs-title, pre.src .hljs-title.function_, pre.src .hljs-function .hljs-title { color: #d2a8ff; }
    pre.src .hljs-number, pre.src .hljs-type { color: #79c0ff; }
    pre.src .hljs-attr, pre.src .hljs-params { color: #e3b341; }
"""
HLJS_CSS = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">'
HLJS_JS = """    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>document.addEventListener('DOMContentLoaded', function () { if (window.hljs) hljs.highlightAll(); });</script>"""

BLOG_HEAD_ASSETS = """  <link rel="icon" type="image/png" href="../assets/img/logo.png" />
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">
  <link href="../assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet" />
  <link href="../assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet" />
  <link href="../assets/css/style.css" rel="stylesheet" />
  <link rel="stylesheet" href="blog.css" />"""

BLOG_SITE_HEADER = """  <header id="header" class="header-top">
    <div class="container">
      <h1><a href="../index.html">Daniel Liu</a></h1>
      <nav class="nav-menu d-none d-lg-block">
        <ul>
          <li><a href="../index.html"><span>About</span></a></li>
          <li class="active"><a href="index.html"><span>Blog</span></a></li>
          <li><a href="../index.html#projects"><span>Projects</span></a></li>
          <li><a href="../index.html#toy-projects"><span>Toy Projects</span></a></li>
        </ul>
      </nav>
      <div class="social-links">
        <a href="mailto:rliu6915@163.com" target="_blank" class="google" rel="noopener"><i class="bx bxl-google"></i></a>
        <a href="https://github.com/rliu6915" target="_blank" class="github" rel="noopener"><i class="bx bxl-github"></i></a>
      </div>
    </div>
  </header>"""

BYLINE = """    <div class="byline">
      <div class="avatar">DL</div>
      <span>By Daniel Liu &middot; August 23, 2026 &middot; 8 min read</span>
    </div>"""

GATEWAY_BYLINE = """    <div class="byline">
      <div class="avatar">DL</div>
      <span>By Daniel Liu &middot; October 9, 2026 &middot; 20 min read</span>
    </div>"""

ARTICLE_TOC_CSS = """
    .article-toc {
      margin: 0 0 48px; padding: 22px 24px;
      background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
      font-family: Raleway, system-ui, sans-serif;
    }
    .article-toc-head {
      display: flex; align-items: center; justify-content: space-between; gap: 14px;
      margin-bottom: 14px; flex-wrap: wrap;
    }
    .article-toc-title {
      margin: 0; font-size: 13px; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: var(--muted);
    }
    .article-toc-lang { font-size: 13px; font-weight: 600;
      color: var(--muted); text-decoration: none; padding: 5px 11px; border-radius: 7px;
      border: 1px solid var(--border); transition: all .15s; white-space: nowrap; }
    .article-toc-lang:hover { color: var(--accent); border-color: var(--accent); }
    .article-toc-list { margin: 0; padding: 0; list-style: none; line-height: 1.5; }
    .article-toc-list li { margin: 0 0 8px; }
    .article-toc-list li:last-child { margin-bottom: 0; }
    .article-toc-list a {
      font-size: 15px; font-weight: 600; color: var(--fg); text-decoration: none;
      border-bottom: 1px solid transparent; transition: color .15s, border-color .15s;
    }
    .article-toc-list a:hover { color: var(--accent); border-bottom-color: rgba(18,214,64,.4); }
    html { scroll-behavior: smooth; }
"""

def gateway_article_toc(lang: str) -> str:
    if lang == 'zh':
        items = [
            ('entry-contract', '入口契约'),
            ('session-key', '会话：key、Store、缓存'),
            ('authorization', '鉴权'),
            ('slash-commands', '斜杠命令'),
            ('pipeline', 'GatewayRunner 流水线'),
            ('dual-layer-guard', '排队与 busy'),
            ('delivery-ledger', '投递与 ledger'),
            ('circuit-breaker', '熔断器'),
            ('prompt-cache', 'Prompt cache'),
            ('takeaways', '小结'),
        ]
        title, aria, other = '目录', '文章目录', 'hermes-gateway-p1.html'
        lang_link = 'EN'
    else:
        items = [
            ('entry-contract', 'Entry contract'),
            ('session-key', 'Session: key, store &amp; cache'),
            ('authorization', 'Authorization'),
            ('slash-commands', 'Slash commands'),
            ('pipeline', 'GatewayRunner pipeline'),
            ('dual-layer-guard', 'Queue &amp; busy guards'),
            ('delivery-ledger', 'Delivery &amp; ledger'),
            ('circuit-breaker', 'Circuit breaker'),
            ('prompt-cache', 'Prompt cache'),
            ('takeaways', 'Takeaways'),
        ]
        title, aria, other = 'Contents', 'Table of contents', 'hermes-gateway-p1-zh.html'
        lang_link = '中文'
    lis = ''.join('        <li><a href="#%s">%s</a></li>\n' % (a, b) for a, b in items)
    return (
        '    <nav class="article-toc" aria-label="%s">\n'
        '      <div class="article-toc-head">\n'
        '        <h2 class="article-toc-title">%s</h2>\n'
        '        <a class="article-toc-lang" href="%s">%s</a>\n'
        '      </div>\n'
        '      <ol class="article-toc-list">\n%s'
        '      </ol>\n'
        '    </nav>\n' % (aria, title, other, lang_link, lis)
    )

AUTHOR_EN = """    <div class="author">
      <div class="avatar">DL</div>
      <div class="bio">
        <strong>Daniel Liu</strong>
        Software engineer writing about AI agents, infrastructure, and the small tools that wire them into everyday chat apps. This blog is where I document what I learn by building.
      </div>
    </div>"""

AUTHOR_ZH = """    <div class="author">
      <div class="avatar">DL</div>
      <div class="bio">
        <strong>Daniel Liu</strong>
        软件工程师，写 AI Agent、基础设施，以及把它们接进日常聊天软件的小工具。这个博客记录边做边学的东西。
      </div>
    </div>"""

SERIES_EN = {
 'gateway': '1 &middot; Gateway', 'whatsapp': '2 &middot; WhatsApp',
 'self-improving': '3 &middot; Self-Improving', 'memory': '4 &middot; Memory'}
SERIES_ZH = {
 'gateway': '1 &middot; 网关', 'whatsapp': '2 &middot; WhatsApp',
 'self-improving': '3 &middot; 自我进化', 'memory': '4 &middot; 记忆'}

def series(cur, lang):
    order = ['gateway','whatsapp','self-improving','memory']
    label = SERIES_EN if lang=='en' else SERIES_ZH
    parts = []
    for s in order:
        cls = ' class="cur"' if s==cur else ''
        parts.append('<a href="hermes-%s.html"%s>%s</a>' % (s, cls, label[s]))
    prefix = 'Part of a 4-part series: ' if lang=='en' else '本系列共 4 篇：'
    return '<p class="series">%s%s</p>' % (prefix, ' &middot; '.join(parts))

# ---------- content ----------
# Conventions:
#  * hero/body use ''' (single-quote triple) because code blocks embed Python
#    docstrings written with """ (double-quote triple) — they must not clash.
#  * Source code is shown INLINE at the point of reference, not in a separate
#    trailing "Source walkthrough" section.
CONTENT = {
 'gateway': {
  'en': {
    'title': 'The Message Gateway: Decoupling Platforms from the Agent',
    'desc': 'Session (key + SessionStore + agent LRU), auth, slash commands, queue, and delivery (delivery.py + ledger) — a source-grounded tour of Hermes GatewayRunner with links to official gateway docs.',
    'eyebrow': 'Architecture &middot; Part 1 of 4',
    'h1': 'The Message Gateway: Decoupling Platforms from the Agent',
    'deck': 'From MessageEvent normalization through session key and SessionStore, ordered auth and DM pairing, slash resolve and busy_policy, dual-layer queueing with /queue FIFO, and delivery.py plus the ledger — how GatewayRunner keeps 20+ platforms on one agent loop.',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  U[User] <-->|chat| PA[Platform adapters]
  PA <-->|events| GW[Gateway]
  GW <-->|turn| AG[AI agent]
      </pre>
      <figcaption>One agent loop; platform details stay in the Gateway and adapters.</figcaption>
    </figure>''',
    'body': _read_fragment('gateway-body-en.html'),
  },
  'zh': {
    'title': '消息网关：把平台与 Agent 彻底解耦',
    'desc': '会话（key + SessionStore + agent LRU）、鉴权、斜杠命令、排队与投递（delivery.py + ledger）——链到官方 gateway 文档与源码的 GatewayRunner 深潜。',
    'eyebrow': '架构 &middot; 第 1 / 4 篇',
    'h1': '消息网关：把平台与 Agent 彻底解耦',
    'deck': '从 MessageEvent 归一化、session key 与 SessionStore、有序鉴权与 DM pairing、斜杠解析与 busy_policy、双层排队与 /queue FIFO、delivery.py 与 ledger——GatewayRunner 如何把 20+ 平台接到同一条 agent 循环上。',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  U[用户] <-->|消息| PA[平台适配器]
  PA <-->|事件| GW[网关]
  GW <-->|轮次| AG[Agent]
      </pre>
      <figcaption>Agent 只跑一轮对话；平台细节留在网关与适配器。</figcaption>
    </figure>''',
    'body': _read_fragment('gateway-body-zh.html'),
  },
 },
 'whatsapp': {
  'en': {
    'title': 'WhatsApp Integration: Cloud API, Webhooks, and Failure Isolation',
    'desc': 'Walking the Meta Cloud API path: webhook ingestion, Graph API delivery, and the three engineering details that keep a group chat from becoming a spam bot.',
    'eyebrow': 'Architecture &middot; Part 2 of 4',
    'h1': 'WhatsApp Integration: Cloud API, Webhooks, and Failure Isolation',
    'deck': "A source-grounded walk through Hermes's WhatsApp path — and the retry-, failure-, and mention-handling details that make it safe in a busy group chat.",
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  M["Meta Webhook"] -->|"POST message"| C["WhatsAppCloudAdapter.connect()"]
  C -->|"MessageEvent"| G["GatewayRunner"]
  G --> A["AIAgent"]
  A -->|"final_response"| G
  G -->|"send()"| API["Graph API"]
  API --> U["User / Group"]
      </pre>
      <figcaption>The WhatsApp path: a webhook delivers inbound messages; the Graph API carries replies back out.</figcaption>
    </figure>''',
    'body': '''      <p>This is part 2 of a 4-part series (1: Message Gateway, 2: WhatsApp, 3: Self-Improving, 4: Long-Term Memory), based on the <strong>real source</strong> of <code>hermes-agent</code>. Here we go one level down into a concrete adapter: WhatsApp, which rides Meta's <strong>Cloud API</strong>.</p>

      <h2>The Cloud API shape</h2>
      <p>WhatsApp uses a webhook to <em>receive</em> messages and the Graph API to <em>send</em> them. <code>WhatsAppCloudAdapter.connect()</code> (<code>gateway/platforms/whatsapp_cloud.py:435</code>) registers the webhook verification handshake and the inbound message callback. Once verified, every user message arrives as a webhook POST, gets normalized into a <code>MessageEvent</code>, and flows into the GatewayRunner we covered in part 1. For real, the method first <strong>refuses to start</strong> if deps or config are missing, then builds the two transports — an inbound webhook server and an outbound <code>httpx</code> client:</p>
      <pre class="src"><code>async def connect(self, *, is_reconnect: bool = False) -> bool:
    if not check_whatsapp_cloud_requirements():
        self._set_fatal_error("whatsapp_cloud_deps_missing", ...)
        return False
    if not self._phone_number_id or not self._access_token:
        self._set_fatal_error("whatsapp_cloud_unconfigured", ...)
        return False
    # Outbound HTTP client with tight keepalive.
    self._http_client = httpx.AsyncClient(
        timeout=30.0, limits=platform_httpx_limits())
    # Inbound webhook server next ...</code></pre>
      <p>Note the two <strong>fail-closed</strong> guards up front: a missing dependency or an unconfigured phone number id / token stops the adapter before it can half-start. That discipline is what keeps a misconfigured bot from silently eating webhooks.</p>

      <h2>Retry-resistance</h2>
      <p>Meta's webhook <strong>redelivers</strong> — a message can arrive two or three times. The adapter guards with <code>_dedup_wamid</code>, keyed on the platform's message id, so one message never triggers two replies. Without it, every flaky delivery would double your agent's answer (and its cost).</p>

      <h2>Failure containment</h2>
      <p>When dispatch to a recipient fails, the handler only <code>log</code>s — it does <strong>not throw</strong>. One undeliverable message must not crash the entire webhook-processing loop, or every other conversation on that adapter goes dark. Containment at the edge keeps one bad send from cascading.</p>

      <figure class="diagram">
        <pre class="mermaid">
flowchart TD
  W["Webhook POST"] --> D{"_dedup_wamid?"}
  D -->|"seen before"| X["drop duplicate"]
  D -->|"new"| N["normalize to MessageEvent"]
  N --> H["GatewayRunner"]
  H --> S["send via Graph API"]
  S -->|"ok"| OK["delivered"]
  S -->|"error"| L["log only — do NOT throw"]
        </pre>
        <figcaption>Figure 1 — Inbound dedup and outbound failure containment. Redelivery is dropped; a failed send is logged, not thrown.</figcaption>
      </figure>

      <h2>Who actually gets a reply</h2>
      <p>In a group, you don't want the bot answering every line. A mention / allowlist policy in the adapter mixin decides "only reply when @-mentioned," so it stays a helper instead of a spam bot. This is the same pattern every chatty adapter needs; WhatsApp just makes it visible because groups are noisy.</p>

      <h2>Takeaways</h2>
      <ul>
        <li><strong>In / out split:</strong> webhook for receive, Graph API for send; <code>connect()</code> wires both.</li>
        <li><strong>Retry-resistance:</strong> <code>_dedup_wamid</code> stops redelivery from producing duplicate replies.</li>
        <li><strong>Failure containment:</strong> a failed <code>send()</code> logs and moves on — one bad message never kills the loop.</li>
        <li><strong>Mention gating:</strong> only @-mentions get a reply in groups, keeping it a helper, not a spammer.</li>
      </ul>''',
  },
  'zh': {
    'title': 'WhatsApp 接入：Cloud API、Webhook 与失败隔离',
    'desc': '走一遍 Meta Cloud API 路径：webhook 收消息、Graph API 发消息，以及让群聊不至于变成垃圾机器人的三个工程细节。',
    'eyebrow': '架构 &middot; 第 2 / 4 篇',
    'h1': 'WhatsApp 接入：Cloud API、Webhook 与失败隔离',
    'deck': '基于真实源码拆解 Hermes 的 WhatsApp 路径——以及抗重试、抗错误扩散、@ 提及门控这些让它在嘈杂群聊里安全的细节。',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  M["Meta Webhook"] -->|"POST message"| C["WhatsAppCloudAdapter.connect()"]
  C -->|"MessageEvent"| G["GatewayRunner"]
  G --> A["AIAgent"]
  A -->|"final_response"| G
  G -->|"send()"| API["Graph API"]
  API --> U["User / Group"]
      </pre>
      <figcaption>WhatsApp 路径：webhook 收消息，Graph API 把回复发回去。</figcaption>
    </figure>''',
    'body': '''      <p>这是 4 篇系列的第 2 / 4 篇（1 消息网关、2 WhatsApp、3 自我进化、4 长期记忆），基于 <code>hermes-agent</code> 的<strong>真实源码</strong>。这里下钻到一个具体适配器：走 Meta <strong>Cloud API</strong> 的 WhatsApp。</p>

      <h2>Cloud API 的形态</h2>
      <p>WhatsApp 用 webhook <em>收</em>消息、用 Graph API <em>发</em>消息。<code>WhatsAppCloudAdapter.connect()</code>（<code>gateway/platforms/whatsapp_cloud.py:435</code>）注册 webhook 校验握手与入站消息回调。校验通过后，每条用户消息以 webhook POST 到达，被归一化成 <code>MessageEvent</code>，流入第 1 篇讲的 GatewayRunner。真实代码里，它先<strong>拒绝启动</strong>（缺依赖或配置缺失就返回），再建两条传输——入站 webhook 服务、出站 <code>httpx</code> 客户端：</p>
      <pre class="src"><code>async def connect(self, *, is_reconnect: bool = False) -> bool:
    if not check_whatsapp_cloud_requirements():
        self._set_fatal_error("whatsapp_cloud_deps_missing", ...)
        return False
    if not self._phone_number_id or not self._access_token:
        self._set_fatal_error("whatsapp_cloud_unconfigured", ...)
        return False
    # Outbound HTTP client with tight keepalive.
    self._http_client = httpx.AsyncClient(
        timeout=30.0, limits=platform_httpx_limits())
    # Inbound webhook server next ...</code></pre>
      <p>注意开头的两道<strong>失败即停</strong>护栏：缺依赖、或 phone number id / token 没配，适配器在半启动前就停下。正是这份纪律，让一个配错的 bot 不会默默吞掉 webhook。</p>

      <h2>抗重试</h2>
      <p>Meta 的 webhook 会<strong>重复投递</strong>——一条消息可能到两三次。适配器用 <code>_dedup_wamid</code>（按平台消息 id 去重）守住，让一条消息绝不触发两次回复。没有它，每次抖动投递都会让你的 agent 答两遍（也多花一倍钱）。</p>

      <h2>抗错误扩散</h2>
      <p>当发给某接收者失败时，处理器只 <code>log</code>，<strong>不抛异常</strong>。一条发不出去的消息不该炸掉整个 webhook 处理循环，否则该适配器上的其他对话全黑。在边缘做隔离，才能避免一次坏发送连锁拖垮全部。</p>

      <figure class="diagram">
        <pre class="mermaid">
flowchart TD
  W["Webhook POST"] --> D{"_dedup_wamid?"}
  D -->|"seen before"| X["drop duplicate"]
  D -->|"new"| N["normalize to MessageEvent"]
  N --> H["GatewayRunner"]
  H --> S["send via Graph API"]
  S -->|"ok"| OK["delivered"]
  S -->|"error"| L["log only — do NOT throw"]
        </pre>
        <figcaption>图 1 — 入站去重与出站失败隔离。重复投递被丢弃；发送失败只记日志、不抛出。</figcaption>
      </figure>

      <h2>到底谁会被回复</h2>
      <p>在群里你不会想让机器人句句都答。适配器 mixin 里的 mention / allowlist 策略决定"只有被 @ 才回"，让它始终是个帮手而非垃圾机器人。这是每个话痨适配器都需要的同款模式；WhatsApp 因为群聊吵而格外显眼。</p>

      <h2>小结</h2>
      <ul>
        <li><strong>收发分离：</strong>webhook 收、Graph API 发；<code>connect()</code> 把两边接上。</li>
        <li><strong>抗重试：</strong><code>_dedup_wamid</code> 阻止重复投递产生重复回复。</li>
        <li><strong>失败隔离：</strong><code>send()</code> 失败只记日志不抛出——一条坏消息永不拖垮循环。</li>
        <li><strong>@ 门控：</strong>群里只有被 @ 才回，保持帮手定位，不做喷子。</li>
      </ul>''',
  },
 },
 'self-improving': {
  'en': {
    'title': 'Self-Improving: Crystallizing Experience into Skills',
    'desc': 'The most-misread part of Hermes. Self-improvement is not the model editing code — it is the Curator turning hard-won experience into reusable skills.',
    'eyebrow': 'Architecture &middot; Part 3 of 4',
    'h1': 'Self-Improving: Crystallizing Experience into Skills',
    'deck': 'A source-grounded look at the Curator — a pure-function state machine that turns experience into skills, with optional LLM merge and zero cost by default.',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  EXP["Hard-won experience"] --> SK["Skill (SKILL.md)"]
  SK --> CUR["Curator: run_curator_review"]
  CUR -->|"needs judgment"| LLM["optional LLM semantic merge"]
  CUR -->|"no judgment"| WRITE["merge / archive / update"]
      </pre>
      <figcaption>Self-improving is experience → skill → curator. The model never edits agent code.</figcaption>
    </figure>''',
    'body': '''      <p>This is part 3 of a 4-part series (1: Message Gateway, 2: WhatsApp, 3: Self-Improving, 4: Long-Term Memory), based on the <strong>real source</strong> of <code>hermes-agent</code>. This is the most commonly misread part of the system, so let's be precise.</p>

      <h2>What "self-improving" actually means</h2>
      <p>Hermes's self-improvement does <strong>not</strong> let the model edit its own source online. Two things happen instead, through <strong>two independent tools</strong>:</p>
      <ul>
        <li><strong>Procedural memory &rarr; a skill.</strong> When the agent works out a reusable way to do a task, it calls <code>skill_manage(action="create")</code> and writes a <code>SKILL.md</code> into <code>~/.hermes/skills/</code>. Skills are narrow and actionable — "how to do X."</li>
        <li><strong>Declarative memory &rarr; MEMORY.md / USER.md.</strong> When the agent learns a fact, a user preference, or an environment detail, it calls the <code>memory</code> tool, which appends to <code>MEMORY.md</code> (observations) or <code>USER.md</code> (the user). This is broad and declarative — "what is true."</li>
      </ul>
      <p>The agent gets smarter by accumulating both: vetted playbooks <em>and</em> a durable record of facts about the user and the world. It rewrites neither itself nor its core code.</p>

      <blockquote class="pull">"Self-Improving isn't about letting the agent edit its own code — it's about crystallizing experience into a skill, and facts into memory, through two separate tools."</blockquote>

      <h2>How it triggers: the nudge</h2>
      <p>Neither tool fires on its own — the model decides. But Hermes runs two <strong>nudge counters</strong> in the background that periodically spawn a forked review agent to read recent conversation and decide what's worth saving:</p>
      <ul>
        <li><strong>Skill nudge</strong> counts <em>tool-calling iterations</em>. In <code>agent/conversation_loop.py:2026</code> the counter <code>_iters_since_skill</code> ticks up each iteration; in <code>agent/turn_finalizer.py:772</code> it fires when <code>&gt;= agent._skill_nudge_interval</code>. The default interval is <strong>10</strong> (<code>agent/agent_init.py:1956</code>), read from <code>skills.creation_nudge_interval</code>.</li>
        <li><strong>Memory nudge</strong> counts <em>user turns</em>. In <code>agent/turn_context.py:714</code> the counter <code>_turns_since_memory</code> ticks up per turn; it fires at <code>&gt;= agent._memory_nudge_interval</code>. Same default <strong>10</strong> (<code>agent/agent_init.py:1827</code>), from <code>memory.nudge_interval</code>.</li>
      </ul>
      <p>Both thresholds only <em>summon a background review agent</em> (prompt: <code>agent/background_review.py:412</code> for skills, <code>:401</code> for memory). That forked agent reads the conversation and decides whether to actually call <code>skill_manage</code> or <code>memory</code>. Reaching the count never writes a file by itself. Using either tool resets its own counter (<code>agent/tool_executor.py:689-692</code>).</p>

      <h2>The Curator: a later skill-ops layer</h2>
      <p>With skills being created, a question arises: who keeps the collection from rotting? That is the <strong>Curator</strong> (<code>agent/curator.py</code>, added 2026-04-26 — <em>after</em> <code>skill_manage</code> itself, 2026-02-19). It is <strong>not</strong> self-improvement; it is the maintenance layer on top of it: a background task that ages unused skills (active&rarr;stale&rarr;archived) and, optionally, merges narrow siblings into class-level "umbrella" skills. Its entry point <code>run_curator_review</code> (<code>:1511</code>) is a <strong>pure-function state machine</strong>:</p>
      <pre class="src"><code>def run_curator_review(
    on_summary=None, synchronous=False,
    dry_run=False, consolidate=None) -> Dict[str, Any]:
    """Execute a single curator review pass.
      1. Apply automatic state transitions (pure, no LLM).
      2. If consolidation enabled AND agent-created skills exist,
         spawn a forked AIAgent for the LLM review prompt.
      3. Update .curator_state with last_run_at + summary.
      4. Invoke on_summary with a user-visible description.
    """
    if consolidate is None:
        consolidate = get_consolidate()   # OFF by default
    ...</code></pre>
      <p>The comment on step 2 is the key: <strong>"consolidate OFF by default"</strong> means the forked LLM review is skipped entirely on a normal run — only the deterministic inactivity prune runs. That is exactly why the default costs zero tokens. The remaining trade-offs fall out of the same shape:</p>
      <ol>
        <li><strong>Zero LLM cost by default</strong> — the state machine itself never calls a model; tokens are spent only when genuine semantic judgment is required.</li>
        <li><strong>dry-run previewable</strong> — it prints "what it will do" first, so you confirm before anything lands on disk.</li>
        <li><strong>pinned skills are never touched</strong> — an explicitly pinned skill skips all automation, so curation can't flush content someone hand-wrote with care.</li>
        <li><strong>Skills only</strong> — the Curator manages agent-created skills; it never touches memory files.</li>
      </ol>

      <figure class="diagram">
        <pre class="mermaid">
flowchart TD
  S["scan skills"] --> D{"merge / archive / update?"}
  D -->|"needs semantic judgment"| M["optional LLM merge"]
  D -->|"mechanical"| W["apply change"]
  M --> W
  W --> P{"pinned?"}
  P -->|yes| K["skip — leave untouched"]
  P -->|no| OK["write result"]
        </pre>
        <figcaption>Figure 1 — The Curator's decision flow. Mechanical changes apply directly; only semantic cases spend tokens, and pinned skills are always protected.</figcaption>
      </figure>

      <h2>Takeaways</h2>
      <ul>
        <li><strong>Not self-editing:</strong> the model never rewrites agent code; it produces skills and memory via two separate tools.</li>
        <li><strong>Two tools, decoupled:</strong> <code>skill_manage</code> writes procedural <code>SKILL.md</code>; <code>memory</code> writes declarative <code>MEMORY.md</code> / <code>USER.md</code>. Creating a skill never auto-writes memory.</li>
        <li><strong>Nudged, not spontaneous:</strong> skill nudge (10 tool iterations) and memory nudge (10 user turns) summon a background review agent that decides what to save.</li>
        <li><strong>Curator is ops, not core:</strong> added later, it only maintains agent-created skills — merge / age / archive — and never touches memory.</li>
      </ul>''',
  },
  'zh': {
    'title': '自我进化：把经验固化为 Skill',
    'desc': 'Hermes 最常被误读的部分。自我进化不是让模型改自己的代码，而是 Curator 把来之不易的经验固化成可复用的 skill。',
    'eyebrow': '架构 &middot; 第 3 / 4 篇',
    'h1': '自我进化：把经验固化为 Skill',
    'deck': '基于真实源码看 Curator——一个纯函数状态机，把经验变成 skill，默认零成本、可选 LLM 合并。',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  EXP["Hard-won experience"] --> SK["Skill (SKILL.md)"]
  SK --> CUR["Curator: run_curator_review"]
  CUR -->|"needs judgment"| LLM["optional LLM semantic merge"]
  CUR -->|"no judgment"| WRITE["merge / archive / update"]
      </pre>
      <figcaption>自我进化是 经验 → skill → curator。模型从不去改 agent 代码。</figcaption>
    </figure>''',
    'body': '''      <p>这是 4 篇系列的第 3 / 4 篇（1 消息网关、2 WhatsApp、3 自我进化、4 长期记忆），基于 <code>hermes-agent</code> 的<strong>真实源码</strong>。这是系统里最常被误读的一块，所以务必精确。</p>

      <h2>"自我进化"到底指什么</h2>
      <p>Hermes 的自我进化<strong>不是</strong>让模型在线改自己的源码，而是经由<strong>两个相互独立的工具</strong>发生两件事：</p>
      <ul>
        <li><strong>程序性记忆 &rarr; skill。</strong>当 agent 摸索出一种可复用的做法，它调 <code>skill_manage(action="create")</code>，把一个 <code>SKILL.md</code> 写进 <code>~/.hermes/skills/</code>。skill 是窄而可执行的——"怎么做 X"。</li>
        <li><strong>陈述性记忆 &rarr; MEMORY.md / USER.md。</strong>当 agent 学到一条事实、一条用户偏好或一个环境细节，它调 <code>memory</code> 工具，追加到 <code>MEMORY.md</code>（观察）或 <code>USER.md</code>（用户）。这是宽泛而陈述性的——"什么是真的"。</li>
      </ul>
      <p>agent 是通过同时积累两者变聪明的：经过把关的 playbook<em>加上</em>一份关于用户和世界的持久事实记录。它既不改写自己，也不改写核心代码。</p>

      <blockquote class="pull">"Self-Improving 不是让 agent 改自己的代码，而是把经验固化为 skill、把事实写进记忆——通过两个独立的工具。"</blockquote>

      <h2>怎么触发：nudge 计数器</h2>
      <p>两个工具都不会自己跑——由模型决定。但 Hermes 在后台跑两个 <strong>nudge 计数器</strong>，定期 fork 一个 review agent 去读最近的对话、判断什么值得存：</p>
      <ul>
        <li><strong>Skill nudge</strong> 计<em>工具调用迭代轮数</em>。在 <code>agent/conversation_loop.py:2026</code> 里计数器 <code>_iters_since_skill</code> 每轮 +1；在 <code>agent/turn_finalizer.py:772</code> 里当 <code>&gt;= agent._skill_nudge_interval</code> 时触发。默认间隔是 <strong>10</strong>（<code>agent/agent_init.py:1956</code>），取自 <code>skills.creation_nudge_interval</code>。</li>
        <li><strong>Memory nudge</strong> 计<em>user turn 数</em>。在 <code>agent/turn_context.py:714</code> 里计数器 <code>_turns_since_memory</code> 每个 turn +1；到达 <code>&gt;= agent._memory_nudge_interval</code> 时触发。默认同样是 <strong>10</strong>（<code>agent/agent_init.py:1827</code>），取自 <code>memory.nudge_interval</code>。</li>
      </ul>
      <p>两个阈值都只是<em>唤起一个后台 review agent</em>（prompt：skill 在 <code>agent/background_review.py:412</code>，memory 在 <code>:401</code>）。那个 fork 出来的 agent 读对话、自己决定要不要真的调 <code>skill_manage</code> 或 <code>memory</code>。计数到了并不会自己写文件。用了任一工具就把自己这条计数器清零（<code>agent/tool_executor.py:689-692</code>）。</p>

      <h2>Curator：后来加的 skill 运维层</h2>
      <p>skill 会被不断创建，自然就有一个问题：谁保证这套收藏不腐烂？那就是 <strong>Curator</strong>（<code>agent/curator.py</code>，2026-04-26 加入——<em>晚于</em> <code>skill_manage</code> 本身，2026-02-19）。它<strong>不是</strong>自我进化，而是架在上面的维护层：一个后台任务，把不用的 skill 按 active&rarr;stale&rarr;archived 老化，并在可选时把窄 sibling 合并成 class-level 的"umbrella" skill。入口 <code>run_curator_review</code>（<code>:1511</code>）是一个<strong>纯函数状态机</strong>：</p>
      <pre class="src"><code>def run_curator_review(
    on_summary=None, synchronous=False,
    dry_run=False, consolidate=None) -> Dict[str, Any]:
    """Execute a single curator review pass.
      1. Apply automatic state transitions (pure, no LLM).
      2. If consolidation enabled AND agent-created skills exist,
         spawn a forked AIAgent for the LLM review prompt.
      3. Update .curator_state with last_run_at + summary.
      4. Invoke on_summary with a user-visible description.
    """
    if consolidate is None:
        consolidate = get_consolidate()   # 默认 OFF
    ...</code></pre>
      <p>第 2 步的注释是关键：<strong>"consolidate 默认 OFF"</strong> 意味着普通运行完全跳过 fork 出来的 LLM 评审——只跑确定性的闲置 prune。这正解释了为什么默认零 token。其余取舍都从同一结构里长出来：</p>
      <ol>
        <li><strong>默认零 LLM 成本</strong>——状态机本身不调模型，只有在真正需要语义判断时才花 token。</li>
        <li><strong>dry-run 可预演</strong>——先打印"将要做什么"，确认无误再落盘。</li>
        <li><strong>pinned skill 永不动</strong>——被显式钉住的 skill 跳过所有自动化，策展不会冲掉人工精心写的内容。</li>
        <li><strong>只管 skill</strong>——Curator 只维护 agent 创建的 skill，从不碰记忆文件。</li>
      </ol>

      <figure class="diagram">
        <pre class="mermaid">
flowchart TD
  S["scan skills"] --> D{"merge / archive / update?"}
  D -->|"needs semantic judgment"| M["optional LLM merge"]
  D -->|"mechanical"| W["apply change"]
  M --> W
  W --> P{"pinned?"}
  P -->|yes| K["skip — leave untouched"]
  P -->|no| OK["write result"]
        </pre>
        <figcaption>图 1 — Curator 的决策流。机械改动直接应用；只有语义情形才花 token，pinned skill 始终受保护。</figcaption>
      </figure>

      <h2>小结</h2>
      <ul>
        <li><strong>不是自我改写：</strong>模型从不去改 agent 代码，它通过两个独立工具产出 skill 和记忆。</li>
        <li><strong>两个工具，解耦：</strong><code>skill_manage</code> 写程序性的 <code>SKILL.md</code>；<code>memory</code> 写陈述性的 <code>MEMORY.md</code> / <code>USER.md</code>。创建 skill 不会自动写记忆。</li>
        <li><strong>靠 nudge，不靠自发：</strong>skill nudge（10 轮工具迭代）与 memory nudge（10 个 user turn）唤起后台 review agent 来决定存什么。</li>
        <li><strong>Curator 是运维，不是核心：</strong>后加的，只维护 agent 创建的 skill——合并/老化/归档——从不碰记忆。</li>
      </ul>''',
  },
 },
 'memory': {
  'en': {
    'title': 'Long-Term Memory: Facts on Disk, Sessions in FTS5',
    'desc': 'Two memory tracks: durable facts through MemoryManager to Provider (and the simplest MemoryStore writing MEMORY.md), and cross-session recall through SessionDB + FTS5.',
    'eyebrow': 'Architecture &middot; Part 4 of 4',
    'h1': 'Long-Term Memory: Facts on Disk, Sessions in FTS5',
    'deck': "A source-grounded tour of Hermes's two memory tracks — fact memory written to disk, and session memory indexed for cross-session search.",
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  F["Fact memory"] --> MM["MemoryManager → Provider"]
  MM --> D["MEMORY.md on disk"]
  S["Session memory"] --> DB["SessionDB (hermes_state.py)"]
  DB --> FT["FTS5 index (messages_fts_cjk)"]
  FT --> Q["session_search"]
      </pre>
      <figcaption>Two tracks: facts land on disk; sessions get a full-text index for cross-session retrieval.</figcaption>
    </figure>''',
    'body': '''      <p>This is part 4 of 4 (1: Message Gateway, 2: WhatsApp, 3: Self-Improving, 4: Long-Term Memory), based on the <strong>real source</strong> of <code>hermes-agent</code>. Memory runs on two independent tracks.</p>

      <h2>Fact memory</h2>
      <p>Facts flow through <code>MemoryManager → MemoryProvider</code> — a background thread, serial, de-noised. The simplest implementation, <code>MemoryStore</code> (<code>tools/memory_tool.py:159</code>), writes <code>MEMORY.md</code> straight to disk via <code>save_to_disk()</code> (<code>:387</code>). The method itself is tiny; the safety lives in <code>_write_file</code>, which uses an <strong>atomic temp-file + rename</strong> so concurrent readers never see a half-written file:</p>
      <pre class="src"><code>def save_to_disk(self, target: str):
    """Persist entries to the appropriate file. Called after every mutation."""
    get_memory_dir().mkdir(parents=True, exist_ok=True)
    self._write_file(self._path_for(target), self._entries_for(target))

@staticmethod
def _write_file(path: Path, entries: List[str]):
    """Atomic temp-file + rename: readers see old OR new, never empty."""
    content = ENTRY_DELIMITER.join(entries) if entries else ""
    atomic_write_text(path, content, tmp_prefix=".mem_")</code></pre>
      <p>This is the durable "what I know about the user" store.</p>

      <h2>Session memory</h2>
      <p>The other track is conversational: <code>hermes_state.py</code> builds a full-text index with FTS5, including a CJK tokenizer <code>messages_fts_cjk</code> (<code>:2685</code>). That index is the foundation behind <code>session_search</code> — the ability to retrieve across past sessions, not just within one.</p>

      <h2>Writing safely under concurrency</h2>
      <p>The naive <code>MemoryStore</code> had a race: two reads of the file with a write between them could silently clobber an external edit. The fix reloads the target <strong>once</strong>, then runs both the drift check and the parse on that <strong>same snapshot</strong> — so an external write between operations can't be overwritten unnoticed. The <code>add()</code> path (<code>:414</code>) that calls <code>save_to_disk()</code> shows the real discipline: re-read from disk <strong>under a lock</strong> before mutating, reject exact duplicates, and refuse to write if the file read as empty (a transient blip that would otherwise wipe every prior memory):</p>
      <pre class="src"><code>def add(self, target, content):
    with self._file_lock(self._path_for(target)):
        if self._reload_target(target, skip_drift=True) is _READ_FAILED:
            return _read_failed_error(self._path_for(target))
        ...
        if content in entries:               # reject exact duplicate
            return self._success_response(target, "Entry already exists.")
        if new_total > limit:                # char-limit guard
            return self._consolidation_failure({...})
        entries.append(content)
        self._set_entries(target, entries)
        self.save_to_disk(target)            # durable write</code></pre>

      <figure class="diagram">
        <pre class="mermaid">
flowchart LR
  IN["Incoming memory op"] --> ADD{"add?"}
  ADD -->|yes| AP["append (skip drift guard)"]
  ADD -->|no| RE["replace / remove / apply_batch"]
  RE --> DR["_reload_target(): read disk ONCE"]
  DR --> DT["drift check + parse on SAME snapshot"]
  DT -->|"drifted"| AB["abort change"]
  DT -->|"clean"| W["write file"]
  AP --> W
        </pre>
        <figcaption>Figure 1 — Race-condition protection on memory writes. One disk read, one snapshot for both the drift check and the parse.</figcaption>
      </figure>

      <h2>Takeaways</h2>
      <ul>
        <li><strong>Two tracks:</strong> facts go through <code>MemoryManager → Provider</code> (disk); sessions go through <code>SessionDB + FTS5</code> (search).</li>
        <li><strong>FTS5 + CJK:</strong> <code>messages_fts_cjk</code> is what makes <code>session_search</code> work across sessions, including Chinese text.</li>
        <li><strong>Concurrency fixed:</strong> the write path now reloads once and checks drift + parses on one snapshot, closing the clobber race.</li>
      </ul>
      <p style="color:var(--muted);font-size:14px;">This closes the 4-part series. Every <code>file:line</code> reference comes from the current <code>hermes-agent</code> source and can be used as a coordinate to read along.</p>''',
  },
  'zh': {
    'title': '长期记忆：事实落盘，会话进 FTS5',
    'desc': '两条记忆线：事实经 MemoryManager → Provider 落盘（最朴素的 MemoryStore 写 MEMORY.md），会话经 SessionDB + FTS5 支持跨会话检索。',
    'eyebrow': '架构 &middot; 第 4 / 4 篇',
    'h1': '长期记忆：事实落盘，会话进 FTS5',
    'deck': '基于真实源码拆解 Hermes 的两条记忆线——写盘的事实记忆，与建全文索引、可跨会话检索的会话记忆。',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  F["Fact memory"] --> MM["MemoryManager → Provider"]
  MM --> D["MEMORY.md on disk"]
  S["Session memory"] --> DB["SessionDB (hermes_state.py)"]
  DB --> FT["FTS5 index (messages_fts_cjk)"]
  FT --> Q["session_search"]
      </pre>
      <figcaption>两条线：事实落盘；会话建全文索引以支持跨会话检索。</figcaption>
    </figure>''',
    'body': '''      <p>这是第 4 / 4 篇（1 消息网关、2 WhatsApp、3 自我进化、4 长期记忆），基于 <code>hermes-agent</code> 的<strong>真实源码</strong>。记忆跑在两条独立的线上。</p>

      <h2>事实记忆</h2>
      <p>事实经 <code>MemoryManager → MemoryProvider</code>——后台线程、串行、去噪。最朴素的实现 <code>MemoryStore</code>（<code>tools/memory_tool.py:159</code>）通过 <code>save_to_disk()</code>（<code>:387</code>）把 <code>MEMORY.md</code> 直接落盘。方法本身很小；安全性在 <code>_write_file</code>：它用<strong>原子临时文件 + rename</strong>，并发读取者永远不会看到一个写一半的文件：</p>
      <pre class="src"><code>def save_to_disk(self, target: str):
    """Persist entries to the appropriate file. Called after every mutation."""
    get_memory_dir().mkdir(parents=True, exist_ok=True)
    self._write_file(self._path_for(target), self._entries_for(target))

@staticmethod
def _write_file(path: Path, entries: List[str]):
    """Atomic temp-file + rename: readers see old OR new, never empty."""
    content = ENTRY_DELIMITER.join(entries) if entries else ""
    atomic_write_text(path, content, tmp_prefix=".mem_")</code></pre>
      <p>这就是耐久的"我对用户已知什么"的存储。</p>

      <h2>会话记忆</h2>
      <p>另一条线是会话级的：<code>hermes_state.py</code> 用 FTS5 建全文索引，含 CJK 分词器 <code>messages_fts_cjk</code>（<code>:2685</code>）。这个索引是 <code>session_search</code> 的底座——能跨历史会话检索，而不只是单次会话内。</p>

      <h2>并发下的安全写入</h2>
      <p>朴素的 <code>MemoryStore</code> 曾有一个竞态：两次读文件中间夹一次写，可能静默覆盖外部编辑。修复是<strong>只重读一次</strong>目标，然后在<strong>同一份快照</strong>上同时做 drift 检测与解析——这样两次操作之间的外部写入不会被无察觉地覆盖。调用 <code>save_to_disk()</code> 的 <code>add()</code> 路径（<code>:414</code>）才露出真纪律：改动前<strong>在锁内重读磁盘</strong>、拒绝完全重复、若文件读成空（瞬时抖动，否则会清空所有历史记忆）则拒绝写：</p>
      <pre class="src"><code>def add(self, target, content):
    with self._file_lock(self._path_for(target)):
        if self._reload_target(target, skip_drift=True) is _READ_FAILED:
            return _read_failed_error(self._path_for(target))
        ...
        if content in entries:               # 拒绝完全重复
            return self._success_response(target, "Entry already exists.")
        if new_total > limit:                # 字符上限护栏
            return self._consolidation_failure({...})
        entries.append(content)
        self._set_entries(target, entries)
        self.save_to_disk(target)            # 耐久写入</code></pre>

      <figure class="diagram">
        <pre class="mermaid">
flowchart LR
  IN["Incoming memory op"] --> ADD{"add?"}
  ADD -->|yes| AP["append (skip drift guard)"]
  ADD -->|no| RE["replace / remove / apply_batch"]
  RE --> DR["_reload_target(): read disk ONCE"]
  DR --> DT["drift check + parse on SAME snapshot"]
  DT -->|"drifted"| AB["abort change"]
  DT -->|"clean"| W["write file"]
  AP --> W
        </pre>
        <figcaption>图 1 — 记忆写入的竞态防护。一次读盘、一份快照同时做 drift 检测 + 解析。</figcaption>
      </figure>

      <h2>小结</h2>
      <ul>
        <li><strong>两条线：</strong>事实走 <code>MemoryManager → Provider</code>（落盘）；会话走 <code>SessionDB + FTS5</code>（检索）。</li>
        <li><strong>FTS5 + CJK：</strong><code>messages_fts_cjk</code> 让 <code>session_search</code> 能跨会话检索，含中文。</li>
        <li><strong>修过并发：</strong>写入路径现在只重读一次、在同一快照上做 drift 检测与解析，堵住了被覆盖的竞态。</li>
      </ul>
      <p style="color:var(--muted);font-size:14px;">本系列到此结束。文中所有 <code>file:line</code> 引用均来自 <code>hermes-agent</code> 当前源码，可作对照阅读的坐标。</p>''',
  },
 },
}

out_dir = 'blogs'

def generate_all_parts():
    for slug, langs in CONTENT.items():
        _write_part(slug, langs)

def _write_part(slug, langs):
    for lang in ('en', 'zh'):
        c = langs[lang]
        # strip the leading "part N of 4-part series" intro paragraph
        c = dict(c)
        c['body'] = re.sub(r"^\s*<p>.*?</p>\s*\n", "", c['body'], flags=re.S)
        FNAMES = {'gateway': 'hermes-gateway-p1'}
        other_base = FNAMES.get(slug, 'hermes-%s' % slug)
        other = '%s-zh.html' % other_base if lang == 'en' else '%s.html' % other_base
        lang_switch = ('Prefer 中文? <a href="%s">Read this article in 中文 &rarr;</a>' % other) if lang == 'en' \
                      else ('Read in English? <a href="%s">Read this article in English &rarr;</a>' % other)
        author = AUTHOR_EN if lang == 'en' else AUTHOR_ZH
        byline = GATEWAY_BYLINE if slug == 'gateway' else BYLINE
        extra_css = ARTICLE_TOC_CSS if slug == 'gateway' else ''
        article_toc = gateway_article_toc(lang) if slug == 'gateway' else ''
        langattr = 'zh-CN' if lang == 'zh' else 'en'
        html = """<!doctype html>
<html lang="{langattr}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Daniel Liu</title>
  <meta content="{desc}" name="description" />
  {blogheadassets}
  {fonts}
  {head}
  {hljscss}
  <style>{style}{seriescss}{srccss}{extracss}</style>
</head>
<body class="blog-shell">
{blogheader}
  <article class="wrap">
    <div class="eyebrow" data-od-id="headline">{eyebrow}</div>
    <h1 data-od-id="headline">{h1}</h1>
    <p class="deck" data-od-id="headline">{deck}</p>
    {byline}
    {articletoc}
    {hero}
    <div data-od-id="body">
{body}
    </div>
    {author}
    <p class="lang-switch">{langswitch}</p>
  </article>
  {zoom}
  {hljsjs}
  <script>
    (function () {
      var isZh = document.documentElement.lang === 'zh-CN';
      var COPY = isZh ? '复制' : 'Copy';
      var COPIED = isZh ? '已复制' : 'Copied';
      document.querySelectorAll('pre.src').forEach(function (pre) {
        var code = pre.querySelector('code');
        if (code && !/language-/.test(code.className)) code.className = 'language-python';
        if (window.hljs && code) { try { window.hljs.highlightElement(code); } catch (e) {} }
        var wrap = document.createElement('div');
        wrap.className = 'src-wrap';
        pre.parentNode.insertBefore(wrap, pre);
        wrap.appendChild(pre);
        var bar = document.createElement('div');
        bar.className = 'src-bar';
        var lang = document.createElement('span');
        lang.className = 'src-lang';
        lang.textContent = 'Python';
        var btn = document.createElement('button');
        btn.className = 'src-copy';
        btn.type = 'button';
        btn.textContent = COPY;
        btn.addEventListener('click', function () {
          var t = code ? code.innerText : pre.innerText;
          var done = function () { btn.textContent = COPIED; setTimeout(function () { btn.textContent = COPY; }, 1500); };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(t).then(done, function () { fallbackCopy(t, btn, COPY, COPIED); });
          } else { fallbackCopy(t, btn, COPY, COPIED); }
        });
        bar.appendChild(lang);
        bar.appendChild(btn);
        wrap.insertBefore(bar, pre);
      });
      function fallbackCopy(text, btn, copy, copied) {
        var ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0'; ta.style.top = '0';
        document.body.appendChild(ta); ta.focus(); ta.select();
        try { document.execCommand('copy'); btn.textContent = copied; } catch (e) {}
        document.body.removeChild(ta);
        setTimeout(function () { btn.textContent = copy; }, 1500);
      }
    })();
  </script>
</body>
</html>
"""
        repl = {
            '{langattr}': langattr, '{lang}': lang, '{title}': c['title'], '{desc}': c['desc'],
            '{blogheadassets}': BLOG_HEAD_ASSETS, '{fonts}': FONTS, '{head}': HEAD, '{style}': STYLE, '{seriescss}': SERIES_CSS,
            '{srccss}': SRC_CSS, '{blogheader}': BLOG_SITE_HEADER, '{eyebrow}': c['eyebrow'], '{h1}': c['h1'],
            '{deck}': c['deck'], '{byline}': byline, '{extracss}': extra_css,
            '{articletoc}': article_toc, '{hero}': c['hero'], '{body}': c['body'],
            '{author}': author, '{langswitch}': lang_switch, '{zoom}': ZOOM,
            '{hljscss}': HLJS_CSS, '{hljsjs}': HLJS_JS,
        }
        for k, v in repl.items():
            html = html.replace(k, v)
        FNAMES = {'gateway': 'hermes-gateway-p1'}  # fresh filename -> fresh CDN object (old build stuck)
        base = FNAMES.get(slug, 'hermes-%s' % slug)
        fname = '%s%s.html' % (base, '' if lang == 'en' else '-zh')
        open(os.path.join(out_dir, fname), 'w', encoding='utf-8').write(html)
        print('wrote', fname, len(html), 'bytes')

if __name__ == '__main__':
    generate_all_parts()
    print('DONE')
