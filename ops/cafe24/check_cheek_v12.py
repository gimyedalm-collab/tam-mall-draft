"""Render all V12 panels and check responsive layout, source loading and motion."""
import asyncio, json, re, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=Path('C:/Users/BNK-1/Desktop/_탐뷰티/물풀치크_상세_V12_261013')
OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8876'

async def run():
    results=[]
    standalone_panels=None
    panel_metrics="""() => [...document.querySelectorAll('[data-panel]')].map(e=>({
      name:e.dataset.panel,width:Math.round(e.getBoundingClientRect().width),
      height:Math.round(e.getBoundingClientRect().height),background:getComputedStyle(e).backgroundColor,
      headline:e.querySelector('h2')?getComputedStyle(e.querySelector('h2')).fontSize:null
    }))"""
    async with async_playwright() as pw:
        browser=await pw.chromium.launch()
        for width in [320,390,860,1440]:
            page=await browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            response=await page.goto(BASE+'/cheek-v12/',wait_until='networkidle')
            assert response.ok
            await page.evaluate('document.fonts.ready')
            for panel in await page.locator('[data-panel]').all():
                await panel.scroll_into_view_if_needed()
                await page.wait_for_timeout(150)
                if width in (390,860):
                    name=await panel.get_attribute('data-panel')
                    await panel.screenshot(path=str(OUT/f'{width}-{name}.png'))
            await page.evaluate('window.scrollTo(0,0)')
            await page.screenshot(path=str(OUT/f'V12-{width}.png'),full_page=True)
            metrics=await page.evaluate('''() => ({
              overflow:document.documentElement.scrollWidth>innerWidth,
              brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
              videos:document.querySelectorAll('video').length,
              shades:document.querySelectorAll('.c12-shade').length,
              heroHeadline:parseFloat(getComputedStyle(document.querySelector('.c12-hero h2')).fontSize),
              heroBody:parseFloat(getComputedStyle(document.querySelector('.c12-hero .c12-body')).fontSize),
              fonts:document.fonts.check('16px Cheek12'),
              height:document.documentElement.scrollHeight
            })''')
            assert not metrics['overflow'] and not metrics['brokenImages'] and not errors, (metrics,errors)
            assert metrics['videos']==1 and metrics['shades']==4 and metrics['fonts'],metrics
            assert metrics['heroHeadline']/metrics['heroBody']>=2,metrics
            results.append({'width':width,**metrics})
            if width==390:
                standalone_panels=await page.evaluate(panel_metrics)
                await page.locator('.c12-film').scroll_into_view_if_needed()
                await page.wait_for_function("document.querySelector('video').currentTime>0")
                await page.get_by_role('button',name='사용법 영상 일시정지').click()
                assert await page.locator('video').evaluate('(v)=>v.paused')
                await page.locator('.c12-colours').scroll_into_view_if_needed()
                await page.locator('.c12-film').scroll_into_view_if_needed()
                await page.wait_for_timeout(200)
                assert await page.locator('video').evaluate('(v)=>v.paused')
                await page.get_by_role('button',name='사용법 영상 재생').click()
                await page.wait_for_function("!document.querySelector('video').paused")
                results.append({'motion':'single source, playback, pause/resume and persistent user pause passed'})
            await page.close()
        page=await browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
        await page.goto(BASE+'/cheek-v12/')
        await page.locator('.c12-film').scroll_into_view_if_needed()
        await page.wait_for_timeout(350)
        assert await page.locator('video').evaluate('(v)=>v.paused && v.currentTime===0')
        await page.get_by_role('button',name='사용법 영상 재생').click()
        await page.wait_for_function("document.querySelector('video').currentTime>0")
        results.append({'reduced_motion':'static initially; explicit play works'})
        await page.close()
        page=await browser.new_page(viewport={'width':390,'height':844})
        await page.route('https://**/*',lambda route:route.abort())
        await page.goto(BASE+'/storefront-v2/preview/product-102.html',wait_until='domcontentloaded')
        assert await page.locator('#milky-cheek-v12').count()==1
        for panel in await page.locator('[data-panel]').all():
            await panel.scroll_into_view_if_needed()
            await page.wait_for_timeout(150)
        await page.evaluate('document.fonts.ready')
        integrated_panels=await page.evaluate(panel_metrics)
        assert integrated_panels==standalone_panels,(standalone_panels,integrated_panels)
        await page.locator('#milky-cheek-v12').screenshot(path=str(OUT/'integrated-detail.png'))
        await page.locator('.c12-hero').screenshot(path=str(OUT/'integrated-hero.png'))
        assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
        await page.locator('.detail-return').click()
        assert page.url.endswith('#purchase-options')
        assert [panel['name'] for panel in integrated_panels]==['hero','application','colours','texture','formula','test','ending']
        assert await page.locator('.c12-finish, img[src*="finish-look"]').count()==0
        results.append({'product_102':'All 7 final panels match standalone geometry, background and headline sizes; no model mood section; return to colour options works; external requests disabled'})
        await browser.close()
    before=subprocess.check_output(['git','show','HEAD:storefront-v2/preview/product-102.html'],cwd=ROOT).decode('utf-8')
    after=(ROOT/'storefront-v2/preview/product-102.html').read_text(encoding='utf-8')
    def shell(s):
        s=re.sub(r'<!-- cheek-v(?:11|12):start -->.*?<!-- cheek-v(?:11|12):end -->','DETAIL',s,flags=re.S)
        s=re.sub(r'(milky-cheek-v(?:11|12)/detail\.css)\?[^"\s]*',r'\1',s)
        return s.replace('milky-cheek-v11','DETAIL_ASSET').replace('milky-cheek-v12','DETAIL_ASSET').replace('\r\n','\n')
    assert shell(before)==shell(after),'Surrounding product page changed'
    results.append({'commerce_preserved':'Outside detail HTML and its CSS/JS references unchanged from HEAD'})
    (OUT/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))

asyncio.run(run())
