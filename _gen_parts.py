#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, os, re

STYLE = open('/tmp/_style.css', encoding='utf-8').read()
HEAD  = open('/tmp/_head_script.html', encoding='utf-8').read()
ZOOM  = open('/tmp/_zoom_script.html', encoding='utf-8').read()

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
"""

NAV = """    <nav class="top">
      <span class="wordmark">Daniel Liu</span>
      <a href="../index.html">Home</a>
      <a href="index.html" class="active">Blog</a>
      <a href="../index.html#projects">Projects</a>
      <a href="../index.html#skills">Skills</a>
    </nav>"""

BYLINE = """    <div class="byline">
      <div class="avatar">DL</div>
      <span>By Daniel Liu &middot; August 23, 2026 &middot; 8 min read</span>
    </div>"""

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
    'desc': 'How Hermes turns 20+ chat platforms into one normalized event stream — and why the Gateway owns protocol complexity while the Agent owns a single conversation loop.',
    'eyebrow': 'Architecture &middot; Part 1 of 4',
    'h1': 'The Message Gateway: Decoupling Platforms from the Agent',
    'deck': 'A source-grounded look at the entry contract every platform adapter shares, and the two layers inside GatewayRunner that keep platform protocol complexity away from the agent core.',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  U["User"] --> PA["Platform Adapters (WhatsApp, Telegram, ...)"]
  PA --> GR["Gateway (orchestration, sessions, auth)"]
  GR --> AG["AIAgent (one conversation loop)"]
  AG --> GR
  GR --> PA
  PA --> U
      </pre>
      <figcaption>The core layering: the Agent owns only one conversation; all platform complexity lives in the Gateway and its adapters.</figcaption>
    </figure>''',
    'body': '''      <p>This is part 1 of a 4-part architecture series on Hermes Agent, based on the <strong>real source</strong> (repo <code>hermes-agent</code>). The series: (1) Message Gateway, (2) WhatsApp, (3) Self-Improving, (4) Long-Term Memory. Here we open with the piece everything else hangs off: how a message from any of ~20 platforms becomes one normalized event the agent can reason about.</p>

      <h2>The entry contract</h2>
      <p>Every platform adapter — Telegram, Discord, Slack, WhatsApp, Signal, and the rest — extends <code>BasePlatformAdapter.handle_message(event)</code> (<code>gateway/platforms/base.py:6045</code>). The adapter's only job is to <strong>normalize</strong> the platform's raw message into a <code>MessageEvent</code> and hand it to <code>GatewayRunner._handle_message</code> (<code>gateway/run.py:16462</code>). That normalization is the seam: the agent never sees a Telegram update vs. a WhatsApp webhook — it only ever sees a <code>MessageEvent</code>.</p>
      <p>Here is the method for real. Note it <strong>returns immediately</strong>: the actual work is spawned as a background task, so a new message can interrupt a running agent instead of being queued behind it (<code>gateway/platforms/base.py:6045</code>):</p>
      <pre class="src"><code>async def handle_message(self, event: MessageEvent) -> None:
    """Process an incoming message. Returns quickly by spawning
    background tasks, so new messages can be processed even while an
    agent is running (interruption support)."""
    if not self._message_handler:
        return
    if event.allow_gateway_control:
        coerce_plaintext_gateway_command(event)
    # ... Telegram topic recovery, then build the session_key ...
    session_key = build_session_key(event.source, ...)
    # route into GatewayRunner._handle_message(event, session_key, ...)</code></pre>
      <p>The line that matters is <code>build_session_key(event.source, ...)</code>: the same platform + chat always yields the same key, which is exactly what the next layer routes on. The adapter hands off here; everything after belongs to the Gateway.</p>

      <h2>Two layers inside GatewayRunner</h2>
      <p>Inside, GatewayRunner splits into a <strong>session-routing layer</strong> (resolve or create a session by <code>session_key</code>, take an active-session lock, run the tool-approval flow) and the <strong>TurnRunner</strong> (<code>gateway/run.py:5348</code>), which actually runs one agent loop, streams output, and feeds tool results back. This split is what keeps "platform protocol complexity" and "agent core logic" from contaminating each other.</p>

      <blockquote class="inline">Design intuition: the Gateway isn't the agent's "frontend" — it's the agent's "post office." It only delivers the letter (MessageEvent) correctly and sends the reply (final_response) correctly. It never thinks for the agent.</blockquote>

      <figure class="diagram">
        <pre class="mermaid">
flowchart TD
  W["Webhook / inbox"] --> A["Adapter.handle_message()"]
  A --> E["MessageEvent"]
  E --> H["GatewayRunner._handle_message()"]
  H --> S{"session_key resolved?"}
  S -->|yes| L["acquire active-session lock"]
  S -->|no| C["create session"]
  C --> L
  L --> T["TurnRunner (run.py:5348)"]
  T --> AG["AIAgent loop"]
  AG --> F["final_response"]
  F --> H
  H --> O["send() back to adapter"]
        </pre>
        <figcaption>Figure 1 — One inbound message's path: normalize, route by session, run a turn, stream the reply. The adapter and gateway own everything outside the AIAgent box.</figcaption>
      </figure>

      <h2>Why this layering matters</h2>
      <p>The key constraint (from <code>AGENTS.md</code>) is that <strong>per-conversation prompt caching is sacred</strong>: every turn reuses a cached prefix, and any change to the system prompt or tool schema mid-conversation invalidates that cache and doubles cost. Because the Gateway owns session/scoping while the agent stays a pure "one conversation loop," the same agent instance can be reused per session without ever mutating its context — caching survives across platforms.</p>

      <h2>Takeaways</h2>
      <ul>
        <li><strong>One contract, many platforms:</strong> <code>BasePlatformAdapter.handle_message</code> is the only seam; adapters normalize, the agent stays platform-blind.</li>
        <li><strong>Two internal layers:</strong> session routing (resolve/lock/approve) vs. TurnRunner (run the loop) — protocol complexity never reaches the agent core.</li>
        <li><strong>Caching is the reason:</strong> a pure "one conversation loop" agent is what lets prompt caching stay intact across 20+ platforms.</li>
      </ul>''',
  },
  'zh': {
    'title': '消息网关：把平台与 Agent 彻底解耦',
    'desc': 'Hermes 如何把 20+ 聊天平台归一化成一条事件流——以及为什么 Gateway 承担协议复杂度，而 Agent 只跑一次对话循环。',
    'eyebrow': '架构 &middot; 第 1 / 4 篇',
    'h1': '消息网关：把平台与 Agent 彻底解耦',
    'deck': '基于真实源码：每个平台适配器共享的入口契约，以及 GatewayRunner 内部把"协议复杂度"挡在 agent 核心之外的两层结构。',
    'hero': '''    <figure class="hero-diagram">
      <pre class="mermaid">
flowchart LR
  U["User"] --> PA["Platform Adapters (WhatsApp, Telegram, ...)"]
  PA --> GR["Gateway (orchestration, sessions, auth)"]
  GR --> AG["AIAgent (one conversation loop)"]
  AG --> GR
  GR --> PA
  PA --> U
      </pre>
      <figcaption>核心分层：Agent 只管一次对话，所有平台复杂度都在 Gateway 与各适配器里。</figcaption>
    </figure>''',
    'body': '''      <p>这是 Hermes Agent 架构系列的第 1 / 4 篇，基于<strong>真实源码</strong>（仓库 <code>hermes-agent</code>）。四篇分别是：(1) 消息网关、(2) WhatsApp、(3) 自我进化、(4) 长期记忆。开篇先讲承载其余一切的这块：任意约 20 个平台的消息，如何变成 agent 能推理的一条归一化事件。</p>

      <h2>入口契约</h2>
      <p>每个平台适配器——Telegram、Discord、Slack、WhatsApp、Signal 等——都继承 <code>BasePlatformAdapter.handle_message(event)</code>（<code>gateway/platforms/base.py:6045</code>）。适配器的唯一职责是把平台原始消息<strong>归一化</strong>成 <code>MessageEvent</code>，交给 <code>GatewayRunner._handle_message</code>（<code>gateway/run.py:16462</code>）。这条归一化就是接缝：agent 从来看不到"Telegram 更新 vs WhatsApp webhook"的区别，它只看到 <code>MessageEvent</code>。</p>
      <p>方法本身长这样（<code>gateway/platforms/base.py:6045</code>）。注意它<strong>立刻 return</strong>：真正的处理被 spawn 成后台任务，好让消息能一边跑 agent 一边被新消息打断，而不是排在后面：</p>
      <pre class="src"><code>async def handle_message(self, event: MessageEvent) -> None:
    """Process an incoming message. Returns quickly by spawning
    background tasks, so new messages can be processed even while an
    agent is running (interruption support)."""
    if not self._message_handler:
        return
    if event.allow_gateway_control:
        coerce_plaintext_gateway_command(event)
    # ... Telegram topic recovery, then build the session_key ...
    session_key = build_session_key(event.source, ...)
    # route into GatewayRunner._handle_message(event, session_key, ...)</code></pre>
      <p>关键在 <code>build_session_key(event.source, ...)</code>：同一平台同一会话永远算出同一个 key，这正是下一层"按会话路由"的依据。适配器到此交权，后面全归 Gateway。</p>

      <h2>GatewayRunner 内部的两层</h2>
      <p>内部，GatewayRunner 分成<strong>会话路由层</strong>（按 <code>session_key</code> 找/建会话、取活跃会话锁、跑工具审批流）和 <strong>TurnRunner</strong>（<code>gateway/run.py:5348</code>，真正跑一轮 agent 循环、流式输出、把 tool 结果喂回去）。这套切分让"平台协议复杂度"和"agent 核心逻辑"互不污染。</p>

      <blockquote class="inline">设计直觉：Gateway 不是 agent 的"前端"，而是 agent 的"邮局"——它只负责把信（MessageEvent）正确投递、把回信（final_response）正确发出，绝不替 agent 思考。</blockquote>

      <figure class="diagram">
        <pre class="mermaid">
flowchart TD
  W["Webhook / inbox"] --> A["Adapter.handle_message()"]
  A --> E["MessageEvent"]
  E --> H["GatewayRunner._handle_message()"]
  H --> S{"session_key resolved?"}
  S -->|yes| L["acquire active-session lock"]
  S -->|no| C["create session"]
  C --> L
  L --> T["TurnRunner (run.py:5348)"]
  T --> AG["AIAgent loop"]
  AG --> F["final_response"]
  F --> H
  H --> O["send() back to adapter"]
        </pre>
        <figcaption>图 1 — 一条入站消息的路径：归一化、按会话路由、跑一轮、流式回传。适配器与 Gateway 包揽了 AIAgent 方框之外的一切。</figcaption>
      </figure>

      <h2>为什么这个分层重要</h2>
      <p>关键约束（来自 <code>AGENTS.md</code>）是 <strong>Per-conversation prompt caching is sacred</strong>：每轮对话复用缓存前缀，任何中途改动 system prompt 或 tool schema 都会让缓存失效、成本翻倍。因为 Gateway 管会话/作用域、agent 保持"纯一次对话循环"，同一个 agent 实例得以按会话复用而不改其上下文——缓存在 20+ 平台间都保得住。</p>

      <h2>小结</h2>
      <ul>
        <li><strong>一个契约，多平台：</strong><code>BasePlatformAdapter.handle_message</code> 是唯一的接缝；适配器归一化，agent 对平台无感。</li>
        <li><strong>内部两层：</strong>会话路由（解析/加锁/审批）与 TurnRunner（跑循环）——协议复杂度永不触及 agent 核心。</li>
        <li><strong>分层是为了缓存：</strong>"纯一次对话循环"的 agent，才让 prompt caching 在 20+ 平台间不被破坏。</li>
      </ul>''',
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
      <p>Hermes's self-improvement does <strong>not</strong> let the model edit its own source online. Instead, it <strong>crystallizes reusable experience into a skill</strong> — procedural knowledge in <code>SKILL.md</code> form — and a background <strong>Curator</strong> keeps that collection healthy. The agent gets smarter by accumulating vetted playbooks, not by rewriting itself.</p>

      <blockquote class="pull">"Self-Improving isn't about letting the agent edit its own code — it's about crystallizing experience into a skill."</blockquote>

      <h2>The Curator state machine</h2>
      <p><code>agent/curator.py</code>'s <code>run_curator_review</code> (<code>:1511</code>) is a <strong>pure-function state machine</strong>: it scans existing skills, decides whether to merge / archive / update, and optionally calls an LLM for "semantic merge." The function signature exposes the knobs — a synchronous/daemon choice, a dry-run that reports without mutating, and a <code>consolidate</code> flag that gates the LLM umbrella-building pass:</p>
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
        <li><strong>Not self-editing:</strong> the model never rewrites agent code; it produces skills.</li>
        <li><strong>Pure-function curator:</strong> <code>run_curator_review</code> is deterministic and testable.</li>
        <li><strong>Zero cost by default:</strong> LLM is used only for genuine semantic merges.</li>
        <li><strong>Safe by design:</strong> dry-run preview + pinned-skills-untouched keep curation from destroying hand-written content.</li>
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
      <p>Hermes 的自我进化<strong>不是</strong>让模型在线改自己的源码，而是把<strong>可复用的经验固化为 skill</strong>——<code>SKILL.md</code> 形式的流程知识——再由后台 <strong>Curator</strong> 维护这套收藏的健康度。agent 是通过积累经过把关的 playbook 变聪明，而不是靠重写自己。</p>

      <blockquote class="pull">"Self-Improving 不是让 agent 改自己的代码，而是把经验固化为 skill。"</blockquote>

      <h2>Curator 状态机</h2>
      <p><code>agent/curator.py</code> 的 <code>run_curator_review</code>（<code>:1511</code>）是一个<strong>纯函数状态机</strong>：扫描现有 skill、判断该合并/归档/更新，可选调用 LLM 做"语义合并"。函数签名露出它的旋钮：同步/守护进程选择、dry-run 只报告不改动、<code>consolidate</code> 开关门控 LLM 合并：</p>
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
        <li><strong>不是自我改写：</strong>模型从不去改 agent 代码，它产出的是 skill。</li>
        <li><strong>纯函数 curtor：</strong><code>run_curator_review</code> 确定且可测。</li>
        <li><strong>默认零成本：</strong>只有真正的语义合并才用 LLM。</li>
        <li><strong>设计即安全：</strong>dry-run 预演 + pinned 不动，策展不会毁掉手写内容。</li>
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
for slug, langs in CONTENT.items():
    for lang in ('en', 'zh'):
        c = langs[lang]
        # strip the leading "part N of 4-part series" intro paragraph
        c = dict(c)
        c['body'] = re.sub(r"^\s*<p>.*?</p>\s*\n", "", c['body'], flags=re.S)
        other = 'hermes-%s-zh.html' % slug if lang == 'en' else 'hermes-%s.html' % slug
        lang_switch = ('Prefer 中文? <a href="%s">Read this article in 中文 &rarr;</a>' % other) if lang == 'en' \
                      else ('Read in English? <a href="%s">Read this article in English &rarr;</a>' % other)
        author = AUTHOR_EN if lang == 'en' else AUTHOR_ZH
        langattr = 'zh-CN' if lang == 'zh' else 'en'
        html = """<!doctype html>
<html lang="{langattr}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Daniel Liu</title>
  <meta content="{desc}" name="description" />
  {fonts}
  {head}
  <style>{style}{seriescss}{srccss}</style>
</head>
<body>
  <article class="wrap">
    {nav}
    <div class="eyebrow" data-od-id="headline">{eyebrow}</div>
    <h1 data-od-id="headline">{h1}</h1>
    <p class="deck" data-od-id="headline">{deck}</p>
    {byline}
    {hero}
    <div data-od-id="body">
{body}
    </div>
    {author}
    <p class="lang-switch">{langswitch}</p>
  </article>
  {zoom}
  <script>
    document.querySelectorAll('pre.src').forEach(function (pre) {
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
      btn.textContent = '复制';
      btn.addEventListener('click', function () {
        var t = pre.innerText;
        var done = function () { btn.textContent = '已复制'; setTimeout(function () { btn.textContent = '复制'; }, 1500); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(t).then(done, function () { fallbackCopy(t, btn); });
        } else { fallbackCopy(t, btn); }
      });
      bar.appendChild(lang);
      bar.appendChild(btn);
      wrap.insertBefore(bar, pre);
    });
    function fallbackCopy(text, btn) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); btn.textContent = '已复制'; } catch (e) {}
      document.body.removeChild(ta);
      setTimeout(function () { btn.textContent = '复制'; }, 1500);
    }
  </script>
</body>
</html>
""".format(langattr=langattr, lang=lang, title=c['title'], desc=c['desc'], fonts=FONTS, head=HEAD,
           style=STYLE, seriescss=SERIES_CSS, srccss=SRC_CSS, nav=NAV, eyebrow=c['eyebrow'], h1=c['h1'],
           deck=c['deck'], byline=BYLINE, hero=c['hero'], body=c['body'],
           author=author, langswitch=lang_switch, zoom=ZOOM)
        fname = 'hermes-%s%s.html' % (slug, '' if lang == 'en' else '-zh')
        open(os.path.join(out_dir, fname), 'w', encoding='utf-8').write(html)
        print('wrote', fname, len(html), 'bytes')

print('DONE')
