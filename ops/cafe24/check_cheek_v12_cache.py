"""Reproduce the owner's mixed-version layout with a genuinely cached old CSS."""
import asyncio, hashlib, json, re, subprocess, threading
from collections import Counter
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path('C:/Users/BNK-1/AppData/Local/Temp/cheek-cache-review')
OUT.mkdir(exist_ok=True)
CSS = '/storefront-v2/preview/assets/milky-cheek-v12/detail.css'
old_css = subprocess.check_output(['git', 'show', f'd663b4d:{CSS.lstrip("/")}'], cwd=ROOT)
html = (ROOT/'cheek-v12/index.html').read_text(encoding='utf-8')
revision = hashlib.sha256((ROOT/CSS.lstrip('/')).read_text(encoding='utf-8').encode()).hexdigest()[:12]
for file in ('cheek-v12/index.html', 'storefront-v2/preview/product-102.html'):
    assert f'milky-cheek-v12/detail.css?v={revision}' in (ROOT/file).read_text(encoding='utf-8')
prime = re.sub(r'detail\.css\?v=[a-f0-9]+', 'detail.css', html).replace('../storefront-v2/', '/storefront-v2/').encode()
requests = Counter()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *_):
        pass

    def do_GET(self):
        requests[self.path] += 1
        if urlsplit(self.path).path == '/prime' or self.path == CSS:
            is_css = self.path == CSS
            body = old_css if is_css else prime
            self.send_response(200)
            self.send_header('Content-Type', 'text/css' if is_css else 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'public, max-age=3600' if is_css else 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'

async def run():
    results = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for width in (320, 390, 860):
            context = await browser.new_context(viewport={'width': width, 'height': 900})
            page = await context.new_page()
            count = requests[CSS]
            await page.goto(base+'/prime?visit=1', wait_until='networkidle')
            await page.goto(base+'/prime?visit=2', wait_until='networkidle')
            assert requests[CSS] == count+1, 'Old CSS was not reused from browser cache'
            finish = page.locator('.c12-finish')
            await finish.scroll_into_view_if_needed()
            before = await finish.evaluate('(e)=>({display:getComputedStyle(e).display,height:e.getBoundingClientRect().height,background:getComputedStyle(e).backgroundColor})')
            assert before['display'] == 'block' and before['background'] == 'rgb(253, 241, 246)'
            if width == 860:
                await finish.screenshot(path=str(OUT/'860-stale-css.png'))
            await page.goto(base+'/cheek-v12/?fixed=1', wait_until='networkidle')
            await finish.scroll_into_view_if_needed()
            await page.evaluate('document.fonts.ready')
            after = await finish.evaluate('(e)=>({display:getComputedStyle(e).display,height:e.getBoundingClientRect().height,background:getComputedStyle(e).backgroundColor})')
            photo = await page.locator('.c12-finish-photo').bounding_box()
            assert after['background'] == 'rgb(242, 240, 238)'
            assert after['height'] < before['height']
            assert abs(photo['width']/photo['height']-1.5)<.01
            assert width*.85 < photo['width'] < width*.9
            assert not (await finish.inner_text()).strip()
            assert requests[CSS] == count+1
            await finish.screenshot(path=str(OUT/f'{width}-fixed.png'))
            results.append({'width': width, 'cached_old_css_reproduced': True, 'before': before, 'after': after})
            await context.close()
        await browser.close()
    (OUT/'verification.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'css_revision': revision, 'results': results}, indent=2))

try:
    asyncio.run(run())
finally:
    server.shutdown()
    server.server_close()
