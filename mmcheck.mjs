import { chromium } from 'playwright';
const url = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const errors = [];
page.on('console', m => { if (m.type()==='error') errors.push(m.text()); });
page.on('pageerror', e => errors.push('PAGEERROR: '+e.message));
await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForTimeout(3000);
const res = await page.evaluate(() => {
  const blocks = [...document.querySelectorAll('pre.mermaid, div.mermaid, .mermaid')];
  return {
    mermaidLibLoaded: !!window.mermaid,
    count: blocks.length,
    renderedSvgs: blocks.filter(b => b.querySelector('svg')).length,
    firstHasSvg: blocks[0] ? !!blocks[0].querySelector('svg') : false,
  };
});
console.log("mermaidLibLoaded:", res.mermaidLibLoaded);
console.log("diagram blocks:", res.count, " rendered as SVG:", res.renderedSvgs);
console.log("console errors:", errors.slice(0,5));
await browser.close();
