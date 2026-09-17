"""Local browser QA for purchase changes; no requests mutate the live store."""
import asyncio
import functools
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'ops/cafe24/runs/purchase-preview'

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

async def run(base):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for width in (1440, 390, 320):
            context = await browser.new_context(viewport={'width': width, 'height': 900})
            page = await context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto(base+'product-112.html', wait_until='domcontentloaded')
            panel = page.locator('.tam-channel-panel')
            assert not await panel.is_visible()
            await page.locator('[data-preview-product] select').select_option(index=1)
            await page.locator('[data-preview-product] input').fill('3')
            assert '쿠폰을 사용해도 유지' in await page.locator('.tam-shipping-text').inner_text()
            assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
            if width == 1440:
                # Beyond the delay, no popup while reading/selecting the product.
                await page.locator('h1').click()
                await page.wait_for_timeout(13000)
                assert not await panel.is_visible()
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await page.wait_for_timeout(1500)
                assert await panel.is_visible()
                assert await page.evaluate('document.activeElement.tagName') == 'BODY'
                await page.keyboard.press('Escape')
                assert not await panel.is_visible()
            trigger = page.locator('.tam-channel-trigger')
            await trigger.click()
            assert await panel.is_visible()
            assert await page.locator('.tam-channel-close').evaluate('(el) => el === document.activeElement')
            assert await page.locator('.tam-channel-link').get_attribute('href') == 'https://pf.kakao.com/_nxhIxhn'
            await page.keyboard.press('Escape')
            assert await trigger.evaluate('(el) => el === document.activeElement')
            await trigger.click()
            await page.screenshot(path=str(OUT/f'product-{width}-popup.png'), full_page=False)
            await page.locator('.tam-channel-snooze').click()
            assert not await panel.is_visible()
            assert await page.evaluate("Number(localStorage.getItem('tam-channel-prompt-v1-until')) > Date.now()")
            await page.evaluate('window.scrollTo(0,0)')
            await page.screenshot(path=str(OUT/f'product-{width}.png'), full_page=False)
            await page.goto(base+'product-23.html', wait_until='domcontentloaded')
            await page.locator('[data-preview-product] select').select_option(index=1)
            assert '쿠폰을 사용해도 유지' in await page.locator('.tam-shipping-text').inner_text()
            await page.goto(base+'design-only.html', wait_until='domcontentloaded')
            await page.locator('.do-products').screenshot(path=str(OUT/f'home-products-{width}.png'))
            assert not await panel.is_visible()
            await page.locator('.tam-channel-trigger').click()
            assert await panel.is_visible()  # explicit reopening remains possible after snooze
            await page.locator('.tam-channel-close').click()
            assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
            assert not errors, errors
            results.append({'width': width, 'shipping': 'pass', 'popup_focus_dismiss_snooze': 'pass', 'overflow': 'pass', 'page_errors': 0})
            await context.close()
        # Persisted suppression must also work on a fresh page without relying on session flag.
        context = await browser.new_context()
        await context.add_init_script("""window.TAM_PURCHASE_CONFIG = {
          popupEnabled:true, popupDelay:0, channelUrl:'https://pf.kakao.com/_nxhIxhn'};
          localStorage.setItem('tam-channel-prompt-v1-until', String(Date.now()+86400000));""")
        page = await context.new_page()
        await page.goto(base+'shop.html', wait_until='domcontentloaded')
        await page.evaluate('scrollTo(0,document.body.scrollHeight)')
        await page.wait_for_timeout(1500)
        assert not await page.locator('.tam-channel-panel').is_visible()
        await context.close()
        await browser.close()
    (OUT/'result.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results))

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'storefront-v2/preview')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(run(f'http://127.0.0.1:{server.server_port}/'))
    finally:
        server.shutdown()
