import { chromium } from 'playwright';
const url = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForTimeout(1500);
const res = await page.evaluate(() => {
  const sec = document.querySelector('#post');
  const h1 = document.querySelector('#post h1');
  const r = sec ? sec.getBoundingClientRect() : null;
  const cs = sec ? getComputedStyle(sec) : null;
  return {
    sectionExists: !!sec,
    h1text: h1 ? h1.textContent : null,
    sectionOpacity: cs ? cs.opacity : null,
    sectionPosition: cs ? cs.position : null,
    sectionTop: r ? Math.round(r.top) : null,
    sectionHeight: r ? Math.round(r.height) : null,
    viewportH: window.innerHeight,
  };
});
console.log(JSON.stringify(res, null, 2));
await browser.close();
