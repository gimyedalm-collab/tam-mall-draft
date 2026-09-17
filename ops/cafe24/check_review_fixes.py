import asyncio
import functools
import threading
from http.server import ThreadingHTTPServer
from playwright.async_api import async_playwright
from check_purchase_preview import ROOT, QuietHandler

async def run(base):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for width in (1440, 390, 320):
            context = await browser.new_context(viewport={'width': width, 'height': 900})
            await context.add_init_script("window.TAM_PURCHASE_CONFIG={popupEnabled:true,popupDelay:0,channelUrl:'https://pf.kakao.com/_nxhIxhn'}")
            page = await context.new_page()
            await page.goto(base+'product-23.html')
            await page.locator('.brand-logo').click()
            await page.wait_for_url('**/design-only.html')
            assert await page.locator('.do-hero').count()==1
            if width<760:
                await page.locator('.mobile-nav-toggle').click()
            await page.locator('#home-navigation a[href="basket.html"]').click()
            await page.wait_for_url('**/basket.html')
            await page.goto(base+'product-23.html')
            await page.evaluate('document.documentElement.style.scrollBehavior="auto";scrollTo(0,document.body.scrollHeight)')
            if width<760:
                await page.locator('#menuToggle').click()
                # Safari can leave focus on BODY after a tap: test suppression without button focus.
                await page.evaluate('document.activeElement.blur()')
                await page.wait_for_timeout(1200)
                assert not await page.locator('.tam-channel-panel').is_visible()
                await page.mouse.click(width-8,700)
                assert await page.locator('#menuToggle').get_attribute('aria-expanded')=='false'
            await page.locator('.detail-return').click()
            await page.wait_for_timeout(300)
            assert await page.locator('#purchase-options').evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top>=0 && r.top<innerHeight}')
            assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
            print(f'{width}: approved home, basket navigation, detail return, mobile menu/popup safeguards PASS', flush=True)
            await context.close()
        await browser.close()

if __name__=='__main__':
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'storefront-v2/preview')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try: asyncio.run(run(f'http://127.0.0.1:{server.server_port}/'))
    finally: server.shutdown()
