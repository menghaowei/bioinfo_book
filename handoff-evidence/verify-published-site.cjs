// Optional browser acceptance check. Requires Playwright; not part of the HTML build.
// Usage: node handoff-evidence/verify-published-site.cjs BASE_URL OUTPUT_DIRECTORY
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = new URL(process.argv[2]);
const output = process.argv[3];
fs.mkdirSync(output, { recursive: true });
const report = { base: base.href, checked_at_utc: new Date().toISOString(), pages: [], mobile: [], redirects: [], errors: [], scope: 'Browser rendering and interaction only; scientific examples not executed.' };

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}),
    ...(process.env.BROWSER_PROXY ? { proxy: { server: process.env.BROWSER_PROXY, bypass: '127.0.0.1,localhost' } } : {})
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
    page.on('pageerror', e => report.errors.push(e.message));
    page.on('response', r => { if (r.status() >= 400 && r.url().startsWith(base.href)) report.errors.push(`HTTP ${r.status()} ${r.url()}`); });
    async function visit(url) {
      const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
      assert.equal(response.status(), 200, url);
      await page.evaluate(async () => { if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise; await document.fonts.ready; });
    }
    async function inspect() {
      return page.evaluate(() => ({
        url: location.href,
        title: document.title,
        heading: document.querySelector('h1')?.innerText,
        math_count: document.querySelectorAll('mjx-container').length,
        math_errors: [...document.querySelectorAll('mjx-merror')].map(x => x.textContent),
        broken_images: [...document.images].filter(x => !x.complete || !x.naturalWidth).map(x => x.src),
        page_overflow: document.documentElement.scrollWidth > innerWidth + 1,
        viewport_width: innerWidth,
        document_width: document.documentElement.scrollWidth
      }));
    }
    function check(result) {
      assert.deepEqual(result.math_errors, []);
      assert.deepEqual(result.broken_images, []);
      assert.equal(result.page_overflow, false, result.url);
    }
    await visit(base.href);
    assert.match(await page.title(), /生物信息学入门/);
    report.build = await page.evaluate(() => fetch('build.json', { cache: 'no-store' }).then(r => r.json()));
    const links = await page.locator('#quarto-sidebar a.sidebar-item-text[href]').evaluateAll(xs => [...new Set(xs.map(x => x.href))]);
    assert.equal(links.length, 20, 'Home, ten chapters and nine appendices');
    await page.screenshot({ path: path.join(output, 'home.png'), fullPage: true });
    for (const url of links) {
      await visit(url);
      const result = await inspect();
      report.pages.push(result);
      check(result);
      console.log('page', result.url, 'math', result.math_count);
    }
    // Use the real chapter navigation, then follow a deep stable anchor.
    await visit(base.href);
    await page.locator('#quarto-sidebar a.sidebar-item-text[href$="manuscript/06-rna-seq.html"]').click();
    await page.waitForURL('**/manuscript/06-rna-seq.html');
    report.chapter_navigation = page.url();
    await visit(new URL('manuscript/08-wgs-and-wes.html#sec-08-04', base).href);
    await page.locator('#sec-08-04').scrollIntoViewIfNeeded();
    assert.ok(await page.locator('#sec-08-04 mjx-container').count());
    await page.locator('#sec-08-04 mjx-container[display="true"]').first().evaluate(x => x.scrollIntoView({ block: 'center' }));
    await page.screenshot({ path: path.join(output, 'math.png') });
    report.deep_anchor = page.url();
    await visit(base.href);
    await page.locator('input.aa-Input').fill('HaplotypeCaller');
    await page.locator('.aa-Panel .search-result-title').first().waitFor();
    report.search = await page.locator('.aa-Panel').innerText();
    const searchLinks = await page.locator('.aa-Panel a').evaluateAll(xs => xs.map(x => x.href));
    assert.ok(searchLinks.some(x => x.includes('08-wgs-and-wes.html')));
    await page.locator('.aa-Panel a[href*="08-wgs-and-wes.html"]').first().click();
    await page.waitForURL(url => url.pathname.includes('/manuscript/'));
    report.search_navigation = page.url();
    // Every generated historical URL must reach its declared destination.
    const docs = path.resolve(__dirname, '../docs');
    for (const name of fs.readdirSync(docs).filter(x => x.endsWith('.html'))) {
      const html = fs.readFileSync(path.join(docs, name), 'utf8');
      const redirect = html.match(/http-equiv="refresh" content="0;url=([^"]+)"/);
      if (!redirect) continue;
      const expected = new URL(redirect[1], base).href;
      await page.goto(new URL(name, base).href, { waitUntil: 'networkidle' });
      await page.waitForURL(expected);
      report.redirects.push({ from: name, to: page.url() });
    }
    for (const width of [390, 360]) {
      await page.setViewportSize({ width, height: 844 });
      for (const chapter of ['04-quality-control-and-alignment', '05-statistics-and-exploration', '06-rna-seq', '08-wgs-and-wes']) {
        await visit(new URL(`manuscript/${chapter}.html`, base).href);
        const result = { width, ...(await inspect()) };
        result.scrollable_containers = await page.evaluate(() => [...document.querySelectorAll('main *')].filter(x => x.scrollWidth > x.clientWidth + 2 && ['auto', 'scroll'].includes(getComputedStyle(x).overflowX)).map(x => {
          const previous = x.scrollLeft; x.scrollLeft = 10; const can_scroll = x.scrollLeft > 0; x.scrollLeft = previous;
          return { tag: x.tagName, can_scroll };
        }));
        report.mobile.push(result);
        if (result.page_overflow) {
          result.overflow_elements = await page.evaluate(() => [...document.querySelectorAll('body *')].map(x => ({ tag: x.tagName, id: x.id, class: String(x.className), width: x.getBoundingClientRect().width, right: x.getBoundingClientRect().right, overflow: getComputedStyle(x).overflowX, text: x.textContent.slice(0, 60) })).filter(x => x.right > innerWidth + 2).slice(0, 50));
          await page.screenshot({ path: path.join(output, 'mobile-overflow.png') });
        }
        check(result);
        assert.ok(result.scrollable_containers.every(x => x.can_scroll));
        if (width === 390 && chapter === '06-rna-seq') {
          await page.screenshot({ path: path.join(output, 'mobile.png') });
          await page.locator('button.quarto-btn-toggle').click();
          await page.locator('#quarto-sidebar').waitFor({ state: 'visible' });
          await page.locator('#quarto-sidebar a.sidebar-item-text[href$="07-chip-seq-and-atac-seq.html"]').click();
          await page.waitForURL('**/07-chip-seq-and-atac-seq.html');
          report.mobile_navigation = page.url();
        }
      }
    }
    assert.equal(report.redirects.length, 12);
    assert.deepEqual(report.errors, []);
    report.passed = true;
  } catch (error) {
    report.passed = false;
    report.failure = error.stack;
    process.exitCode = 1;
  } finally {
    fs.writeFileSync(path.join(output, 'browser-report.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({ passed: report.passed, pages: report.pages.length, redirects: report.redirects.length, mobile: report.mobile.length, errors: report.errors, failure: report.failure }));
    await browser.close();
  }
})();
