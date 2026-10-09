#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ONE combined long-form article from the 4 parts in _gen_parts.CONTENT,
with an in-article table of contents (chapter anchors) + language toggle."""
import io, os, re

# Reuse the shared pieces
STYLE = open('/tmp/_style.css', encoding='utf-8').read()
HEAD  = open('/tmp/_head_script.html', encoding='utf-8').read()

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
    /* in-article table of contents */
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
      line-height: 1.25;
    }
    .article-toc h2.article-toc-title { margin: 0; color: var(--muted); font-size: 13px; }
    .article-toc ::first-letter {
      float: none !important; font-size: inherit !important; line-height: inherit !important;
      padding: 0 !important; font-weight: inherit !important; color: inherit !important;
      font-family: inherit !important;
    }
    .langtoggle { font-size: 13px; font-weight: 600;
      color: var(--muted); text-decoration: none; padding: 5px 11px; border-radius: 7px;
      border: 1px solid var(--border); transition: all .15s; white-space: nowrap; }
    .langtoggle:hover { color: var(--accent); border-color: var(--accent); }
    .article-toc-list { margin: 0; padding: 0; list-style: none; line-height: 1.5; }
    .article-toc-list li { margin: 0 0 8px; }
    .article-toc-list li:last-child { margin-bottom: 0; }
    .article-toc-list a {
      font-size: 15px; font-weight: 600; color: var(--fg); text-decoration: none;
      border-bottom: 1px solid transparent; transition: color .15s, border-color .15s;
    }
    .article-toc-list a:hover { color: var(--accent); border-bottom-color: rgba(18,214,64,.4); }
    .article-toc-back { margin: 16px 0 0; padding-top: 14px; border-top: 1px solid var(--border); font-size: 13px; line-height: 1.5; }
    .article-toc-back a {
      color: var(--muted); text-decoration: none; font-weight: 600; transition: color .15s;
    }
    .article-toc-back a:hover { color: var(--accent); }
    /* section separation */
    section.part { padding-top: 14px; }
    section.part + section.part { margin-top: 56px; padding-top: 40px; border-top: 1px solid var(--border); }
    .sec-foot { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 30px; padding-top: 18px; border-top: 1px solid var(--border); }
    .footlink { font-family: Raleway, system-ui, sans-serif; font-size: 13px; font-weight: 600;
      color: var(--muted); text-decoration: none; padding: 5px 13px; border-radius: 7px;
      border: 1px solid var(--border); transition: all .15s; }
    .footlink:hover { color: var(--accent); border-color: var(--accent); }
    html { scroll-behavior: smooth; }
"""

def build(lang):
    is_zh = (lang == 'zh')
    other_page = 'hermes-architecture-zh.html' if lang == 'en' else 'hermes-architecture.html'
    lang_label = '中文' if lang == 'en' else 'EN'
    author = AUTHOR_ZH if is_zh else AUTHOR_EN

    blog_index = 'index.html'
    back_label = '← Blog' if lang == 'en' else '← 博客'
    toc_title = 'Contents' if lang == 'en' else '目录'
    toc_aria = 'Table of contents' if lang == 'en' else '文章目录'
    foot_top = '↑ Back to top' if lang == 'en' else '↑ 回到顶部'
    foot_blog = '← Back to Blog' if lang == 'en' else '← 回到博客'
    toc_items = ''
    for slug, secid, label in PARTS:
        toc_items += '      <li><a href="#%s">%s</a></li>\n' % (secid, label)
    toc = (
        '    <nav class="article-toc" aria-label="%s">\n'
        '      <div class="article-toc-head">\n'
        '        <h2 class="article-toc-title">%s</h2>\n'
        '        <a class="langtoggle" href="%s">%s</a>\n'
        '      </div>\n'
        '      <ol class="article-toc-list">\n' % (toc_aria, toc_title, other_page, lang_label) +
        toc_items +
        '      </ol>\n'
        '      <div class="article-toc-back"><a href="%s">%s</a></div>\n'
        '    </nav>\n' % (blog_index, back_label)
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
            '    <div class="sec-foot">\n'
            '      <a class="footlink" href="#%s">%s</a>\n' % (secid, foot_top) +
            '      <a class="footlink" href="index.html">%s</a>\n' % foot_blog +
            '    </div>\n'
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
  <article class="wrap">
%s%s  </article>
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
    })();
  </script>
</body>
</html>
""" % (langattr, title, desc, FONTS, HEAD, HLJS_CSS,
       STYLE, SERIES_CSS, SRC_CSS, COMBINED_CSS,
       toc, sections, HLJS_JS)

    fname = 'hermes-architecture%s.html' % ('' if lang == 'en' else '-zh')
    open(os.path.join('blogs', fname), 'w', encoding='utf-8').write(html)
    print('wrote', fname, len(html), 'bytes')

if __name__ == '__main__':
    build('en')
    build('zh')
