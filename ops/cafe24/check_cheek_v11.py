"""Local visual and behavior QA; no customer actions or commerce submissions."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path('C:/Users/BNK-1/Desktop/_탐뷰티/물풀치크_상세_V11_261013')
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'http://127.0.0.1:8876'

async def run():
    results = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for width in [320, 390, 860, 1440]:
            page = await browser.new_page(viewport={'width': width, 'height': 900}, device_scale_factor=1)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(BASE + '/cheek-v11/', wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            for selector in ['.mc-colours', '.mc-formula', '.mc-film', '.mc-test']:
                await page.locator(selector).scroll_into_view_if_needed()
                await page.wait_for_timeout(120)
            await page.evaluate('window.scrollTo(0,0)')
            await page.screenshot(path=str(OUT / f'V11-{width}.png'), full_page=True)
            if width == 860:
                await page.locator('.mc-formula').screenshot(path=str(OUT / 'V11-desktop-formula.png'))
            metrics = await page.evaluate('''() => ({
                overflow: document.documentElement.scrollWidth > innerWidth,
                missingImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i=>i.src),
                minBodyText: Math.min(...[...document.querySelectorAll('.mc-intro,.mc-steps p,dd')].map(e=>parseFloat(getComputedStyle(e).fontSize))),
                colours: document.querySelectorAll('.mc-colour').length,
                fontsLoaded: document.fonts.check('16px TAMCheek'),
                height: document.documentElement.scrollHeight
            })''')
            assert not metrics['overflow'] and not metrics['missingImages'], metrics
            assert metrics['minBodyText'] >= 15 and metrics['colours'] == 4 and metrics['fontsLoaded'], metrics
            assert not errors, errors
            results.append({'width': width, **metrics, 'javascript_errors': errors})
            if width == 390:
                await page.locator('.mc-film').scroll_into_view_if_needed()
                await page.wait_for_function("document.querySelector('video').currentTime > 0")
                await page.get_by_role('button', name='사용법 영상 일시정지').click()
                assert await page.locator('video').evaluate('(v)=>v.paused')
                await page.locator('.mc-test').scroll_into_view_if_needed()
                await page.locator('.mc-film').scroll_into_view_if_needed()
                await page.wait_for_timeout(250)
                assert await page.locator('video').evaluate('(v)=>v.paused')
                await page.get_by_role('button', name='사용법 영상 재생').click()
                await page.wait_for_function("!document.querySelector('video').paused")
                await page.locator('.mc-formula').screenshot(path=str(OUT / 'V11-mobile-formula.png'))
                results.append({'video': 'autoplay, pause, retained user pause and resume passed'})
            await page.close()
        page = await browser.new_page(viewport={'width':390,'height':844}, reduced_motion='reduce')
        await page.goto(BASE + '/cheek-v11/')
        await page.locator('.mc-film').scroll_into_view_if_needed()
        await page.wait_for_timeout(500)
        assert await page.locator('video').evaluate('(v)=>v.paused && v.currentTime===0')
        await page.get_by_role('button', name='사용법 영상 재생').click()
        await page.wait_for_function("document.querySelector('video').currentTime > 0")
        results.append({'reduced_motion': 'poster initially, explicit playback works'})
        await page.close()
        page = await browser.new_page(viewport={'width':390,'height':844})
        await page.route('https://**/*', lambda route: route.abort())
        await page.goto(BASE + '/storefront-v2/preview/product-102.html', wait_until='domcontentloaded')
        await page.locator('#milky-cheek-detail').scroll_into_view_if_needed()
        assert await page.locator('#milky-cheek-detail').count() == 1
        assert not await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        await page.locator('.mc-formula').screenshot(path=str(OUT / 'V11-integrated-formula.png'))
        await page.locator('.detail-return').click()
        assert page.url.endswith('#purchase-options')
        assert await page.locator('#purchase-options').is_visible()
        results.append({'product_102': 'detail integrated, no horizontal overflow, return to options works; external requests disabled'})
        await browser.close()
    (OUT / 'verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(results, ensure_ascii=False, indent=2))

asyncio.run(run())
