"""Read-only browser review of the preview, never submits to the live store."""
import asyncio
import functools
import json
import sys
import threading
from http.server import ThreadingHTTPServer
from playwright.async_api import async_playwright
from check_purchase_preview import ROOT, QuietHandler

OUT = ROOT / 'ops/cafe24/runs/overall-review'

async def run(base):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for width in (1440, 390, 320):
            context = await browser.new_context(viewport={'width': width, 'height': 900})
            await context.add_init_script("sessionStorage.setItem('tam-channel-prompt-v1-shown','1')")
            page = await context.new_page()
            for route in ('design-only', 'shop', 'about', 'lookbook', 'jelly', 'cloud', 'product-23', 'product-112', 'search', 'basket', 'login'):
                errors = []
                def on_error(e): errors.append(str(e))
                page.on('pageerror', on_error)
                await page.goto(base + route + '.html', wait_until='domcontentloaded')
                await page.wait_for_timeout(600)
                if route in ('design-only', 'shop', 'about', 'lookbook', 'jelly', 'cloud', 'search'):
                    for img in await page.locator('img').all():
                        if await img.is_visible():
                            await img.scroll_into_view_if_needed()
                            await img.evaluate('(e)=>e.decode().catch(()=>{})')
                    await page.evaluate('document.documentElement.style.scrollBehavior="auto"; scrollTo(0,0)')
                await page.evaluate('document.fonts.ready')
                metrics = await page.evaluate('''() => ({
                  overflow: document.documentElement.scrollWidth > innerWidth,
                  home: document.querySelector('a[aria-label="탐뷰티 홈"], .do-logo')?.getAttribute('href'),
                  brokenLoadedImages: [...document.images].filter(i=>i.complete && !i.naturalWidth).map(i=>i.src),
                  replacementCharacters: document.body.innerText.includes('\uFFFD')
                })''')
                if route in ('design-only', 'about', 'shop', 'product-23') and width != 320:
                    await page.screenshot(path=str(OUT / f'{route}-{width}.png'), full_page=route != 'product-23')
                if width < 760:
                    toggle = page.locator('#menuToggle, .mobile-nav-toggle')
                    if await toggle.count():
                        await toggle.click()
                        metrics['menuOpens'] = await toggle.get_attribute('aria-expanded') == 'true'
                        await page.keyboard.press('Escape')
                        metrics['menuCloses'] = await toggle.get_attribute('aria-expanded') == 'false'
                results.append({'width': width, 'route': route, **metrics, 'errors': errors})
                page.remove_listener('pageerror', on_error)
            await page.goto(base+'product-23.html')
            await page.locator('.brand-logo').click()
            results.append({'width': width, 'logoDestination': page.url, 'approvedHome': await page.locator('.do-hero').count() == 1})
            assert await page.locator('.do-hero').count() == 1, 'Logo must return to approved home'
            await page.goto(base+'product-23.html')
            await page.locator('[data-preview-product] select').select_option(index=1)
            await page.locator('[data-add]').click()
            await page.locator('[data-basket-link]').click()
            assert await page.locator('.cart-row').count() == 1
            await page.get_by_role('button', name='더 젤리 스킨 쿠션 수량 늘리기', exact=True).click()
            assert '60,000' in await page.locator('[data-subtotal]').inner_text()
            await page.get_by_role('button', name='삭제', exact=True).click()
            assert await page.locator('[data-cart-empty]').is_visible()
            await context.close()
        await browser.close()
    (OUT/'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(results, ensure_ascii=False))

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    if len(sys.argv)>1:
        asyncio.run(run(sys.argv[1]))
    else:
        server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'storefront-v2/preview')))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try: asyncio.run(run(f'http://127.0.0.1:{server.server_port}/'))
        finally: server.shutdown()
