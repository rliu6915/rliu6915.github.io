import { chromium } from 'playwright';
const url = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForTimeout(3500);
const res = await page.evaluate(() => {
  const sec = document.querySelector('#post');
  const h1 = document.querySelector('#post h1');
  const header = document.querySelector('#header');
  const sr = sec.getBoundingClientRect();
  const hr = header.getBoundingClientRect();
  const scs = getComputedStyle(sec), hcs = getComputedStyle(header);
  const blocks = [...document.querySelectorAll('.mermaid')];
  return {
    headerClass: header.className,
    headerComputedPosition: hcs.position,
    headerHeight: Math.round(hr.height),
    headerTop: Math.round(hr.top),
    sectionClass: sec.className,
    sectionOpacity: scs.opacity,
    sectionPosition: scs.position,
    sectionTop: Math.round(sr.top),
    sectionHeight: Math.round(sr.height),
    h1visible: h1 ? Math.round(h1.getBoundingClientRect().top) : null,
    mermaidBlocks: blocks.length,
    mermaidSvg: blocks.filter(b=>b.querySelector('svg')).length,
  };
});
console.log(JSON.stringify(res,null,2));
await page.screenshot({ path: '/tmp/site_inspect/_render_check.png', fullPage: false });
await browser.close();
