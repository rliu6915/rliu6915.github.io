#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ONE combined long-form article from the 4 parts in _gen_parts.CONTENT,
with a sticky top option bar: 4-part switcher (smooth scroll) + language toggle."""
import io, os, re

# Reuse the shared pieces
STYLE = open('/tmp/_style.css', encoding='utf-8').read()
HEAD  = open('/tmp/_head_script.html', encoding='utf-8').read()
ZOOM  = open('/tmp/_zoom_script.html', encoding='utf-8').read()

from _gen_parts import (CONTENT, FONTS, HLJS_CSS, HLJS_JS, SERIES_CSS, SRC_CSS,
                        BYLINE, AUTHOR_EN, AUTHOR_ZH)

# Order of the 4 parts + section ids + switcher labels
PARTS = [
    ('gateway',     'gateway',  '1 · Gateway'),
    ('whatsapp',    'whatsapp', '2 · WhatsApp'),
    ('self-improving','self',   '3 · Self-Improving'),
    ('memory',      'memory',   '4 · Memory'),
]

COMBINED_CSS = """
    /* sticky option bar */
    .optbar { position: sticky; top: 0; z-index: 50;
      background: var(--surface); border-bottom: 1px solid var(--border);
      box-shadow: 0 1px 0 rgba(0,0,0,.04); }
    .optbar-inner { max-width: 740px; margin: 0 auto; padding: 10px 22px;
      display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap; }
    .opt-left { display: flex; align-items: center; gap: 10px; }
    .backlink { font-family: Raleway, system-ui, sans-serif; font-size: 13px; font-weight: 600;
      color: var(--muted); text-decoration: none; padding: 5px 11px; border-radius: 7px;
      border: 1px solid var(--border); transition: all .15s; white-space: nowrap; }
    .backlink:hover { color: var(--accent); border-color: var(--accent); }
    .parts { display: flex; gap: 4px; flex-wrap: wrap; }
    .parts a { font-family: Raleway, system-ui, sans-serif; font-size: 13px; font-weight: 600;
      color: var(--muted); text-decoration: none; padding: 5px 11px; border-radius: 7px;
      border: 1px solid transparent; transition: all .15s; }
    .parts a:hover { color: var(--accent); border-color: var(--border); }
    .parts a.cur { color: var(--accent); background: color-mix(in srgb, var(--accent) 12%, transparent); }
    .langtoggle { font-family: Raleway, system-ui, sans-serif; font-size: 13px; font-weight: 600;
      color: var(--muted); text-decoration: none; padding: 5px 11px; border-radius: 7px;
      border: 1px solid var(--border); transition: all .15s; white-space: nowrap; }
    .langtoggle:hover { color: var(--accent); border-color: var(--accent); }
    /* section separation */
    section.part { padding-top: 14px; }
    section.part + section.part { margin-top: 56px; padding-top: 40px; border-top: 1px solid var(--border); }
    html { scroll-behavior: smooth; }
    @media (max-width: 640px) {
      .optbar-inner { padding: 8px 14px; }
      .parts a { padding: 4px 8px; font-size: 12px; }
    }
"""

def build(lang):
    is_zh = (lang == 'zh')
    other_page = 'hermes-architecture-zh.html' if lang == 'en' else 'hermes-architecture.html'
    lang_label = '中文' if lang == 'en' else 'EN'
    author = AUTHOR_ZH if is_zh else AUTHOR_EN

    # Option bar
    parts_html = ''
    for slug, secid, label in PARTS:
        parts_html += '<a href="#%s" data-sec="%s">%s</a>\n      ' % (secid, secid, label)
    blog_index = 'index.html' if lang == 'en' else 'index.html'
    back_label = '← Blog' if lang == 'en' else '← 博客'
    optbar = (
        '  <div class="optbar">\n'
        '    <div class="optbar-inner">\n'
        '      <div class="opt-left">\n'
        '        <a class="backlink" href="%s">%s</a>\n' % (blog_index, back_label) +
        '        <nav class="parts">\n      ' + parts_html + '      </nav>\n'
        '      </div>\n'
        '      <a class="langtoggle" href="%s">%s</a>\n' % (other_page, lang_label) +
        '    </div>\n'
        '  </div>'
    )

    # Sections
    sections = ''
    for slug, secid, label in PARTS:
        c = dict(CONTENT[slug][lang])
        # strip the leading "part N of 4-part series" intro paragraph if present
        c['body'] = re.sub(r"^\s*<p>.*?</p>\s*\n", "", c['body'], flags=re.S)
        sections += (
            '  <section class="part" id="%s">\n' % secid +
            '    <div class="eyebrow">%s</div>\n' % c['eyebrow'] +
            '    <h1>%s</h1>\n' % c['h1'] +
            '    %s\n' % c['hero'] +
            '    <div data-od-id="body">\n%s\n    </div>\n' % c['body'] +
            '  </section>\n\n'
        )

    langattr = 'zh-CN' if is_zh else 'en'
    title = 'Hermes Agent 架构深潜' if is_zh else 'Deep Dive into Hermes Agent'
    desc = ('四篇合一：消息网关、WhatsApp、自我进化、长期记忆——基于真实源码的架构深潜。'
            if is_zh else
            'All four parts in one: Message Gateway, WhatsApp, Self-Improving, and Long-Term Memory — a source-grounded architecture deep-dive.')

    html = """<!doctype html>
<html lang="%s">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>%s</title>
  <meta content="%s" name="description" />
  %s
  %s
  %s
  <style>%s%s%s%s</style>
</head>
<body>
%s
  <article class="wrap">
%s  </article>
  %s
  %s
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
      // highlight the active part in the switcher as you scroll
      var links = Array.prototype.slice.call(document.querySelectorAll('.parts a'));
      var secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-sec')); });
      function onScroll() {
        var pos = window.scrollY + 120;
        var cur = secs[0];
        secs.forEach(function (s) { if (s && s.offsetTop <= pos) cur = s; });
        links.forEach(function (a) {
          a.classList.toggle('cur', cur && a.getAttribute('data-sec') === cur.id);
        });
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    })();
  </script>
</body>
</html>
""" % (langattr, title, desc, FONTS, HEAD, HLJS_CSS,
       STYLE, SERIES_CSS, SRC_CSS, COMBINED_CSS,
       optbar, sections, ZOOM, HLJS_JS)

    fname = 'hermes-architecture%s.html' % ('' if lang == 'en' else '-zh')
    open(os.path.join('blogs', fname), 'w', encoding='utf-8').write(html)
    print('wrote', fname, len(html), 'bytes')

if __name__ == '__main__':
    build('en')
    build('zh')
