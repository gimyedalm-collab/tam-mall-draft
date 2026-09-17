"""Verify the final cushion detail package loads in order on desktop and mobile."""
import asyncio
import functools
import hashlib
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import threading
from playwright.async_api import async_playwright
from check_purchase_preview import QuietHandler, ROOT

OUT = ROOT/'ops/cafe24/runs/cushion-detail-0908'

async def run(base):
    manifest = json.loads((ROOT/'ops/cafe24/cushion-detail-0908.json').read_text(encoding='utf-8'))
    for folder in ('storefront-v2/preview/assets', 'storefront-v2/cafe24/tam/assets'):
        for item in manifest['sections']:
            path = ROOT/folder/'jelly-skin-cushion-0908'/item['file']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for width in (1440, 390, 320):
            context = await browser.new_context(viewport={'width': width, 'height': 900})
            await context.add_init_script("sessionStorage.setItem('tam-channel-prompt-v1-shown','1')")
            page = await context.new_page()
            errors, failed = [], []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('response', lambda r: failed.append(r.url) if r.status >= 400 else None)
            await page.goto(base+'product-23.html', wait_until='domcontentloaded')
            images = page.locator('#product-detail .detail-images img')
            assert await images.count() == 10
            assert await page.locator('#product-detail').evaluate('(e)=>e.tagName') == 'SECTION'
            for index, record in enumerate(manifest['sections']):
                image = images.nth(index)
                await image.scroll_into_view_if_needed()
                await image.evaluate('(e)=>e.decode()')
                size = await image.evaluate('(e)=>[e.naturalWidth,e.naturalHeight]')
                assert size == [record['width'], record['height']], (record, size)
            metrics = await images.evaluate_all('es=>es.map(e=>{const r=e.getBoundingClientRect();return {width:r.width,top:r.top,bottom:r.bottom}})')
            assert all(x['width'] <= min(860, width) for x in metrics)
            assert all(abs(metrics[i]['bottom']-metrics[i+1]['top']) <= 1 for i in range(9)), metrics
            assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
            await page.locator('#product-detail').evaluate('(e)=>{document.documentElement.style.scrollBehavior="auto";window.scrollTo(0,e.offsetTop-90)}')
            await page.screenshot(path=str(OUT/f'detail-top-{width}.png'))
            await images.last.scroll_into_view_if_needed()
            await page.screenshot(path=str(OUT/f'detail-bottom-{width}.png'))
            assert not errors, errors
            assert not failed, failed
            results.append({'width': width, 'images_loaded': 10, 'order_and_dimensions': 'pass',
                'no_gaps_or_overflow': 'pass', 'network_errors': 0, 'page_errors': 0})
            await context.close()
        await browser.close()
    (OUT/'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results))

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'storefront-v2/preview')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        asyncio.run(run(f'http://127.0.0.1:{server.server_port}/'))
    finally:
        server.shutdown()
