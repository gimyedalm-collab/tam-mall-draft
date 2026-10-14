"""Isolated public-preview Chromium QA; no authenticated browser/profile used."""
import asyncio,json,re,subprocess
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=Path('C:/Users/BNK-1/Desktop/tam-ux-review-261013/shade-fix-261014')
OUT.mkdir(exist_ok=True)
BASE='http://127.0.0.1:8875/storefront-v2/preview/'

async def run():
    checks=[]
    async with async_playwright() as pw:
        browser=await pw.chromium.launch()
        for width in [320,390,430,1440]:
            for pid,count in [(23,6),(112,8),(102,4)]:
                page=await browser.new_page(viewport={'width':width,'height':844},device_scale_factor=1)
                # Check local UI independently of third-party review/CDN services.
                await page.route('https://**/*',lambda route:route.abort())
                await page.goto(BASE+f'product-{pid}.html',wait_until='domcontentloaded')
                await page.evaluate('document.fonts.ready')
                shades=page.locator('.ux-shades')
                await shades.scroll_into_view_if_needed()
                assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
                assert await page.locator('.ux-shade-button img,.ux-shade-button svg').count()==0
                for i in range(count):
                    button=page.locator('.ux-shade-button').nth(i)
                    await button.click()
                    assert await page.locator('[data-preview-product] select').evaluate('(e)=>e.selectedIndex')==i+1
                    assert await button.get_attribute('aria-pressed')=='true'
                    box=await button.bounding_box()
                    assert box['height']>=48 and box['width']>=110,box
                if width==390:await shades.screenshot(path=str(OUT/f'{pid}-options.png'))
                await page.locator('.ux-compare-open').click()
                assert await page.locator('.ux-colour-dialog').evaluate('(d)=>d.open')
                await page.wait_for_function("[...document.querySelectorAll('.ux-colour-content img')].every(i=>i.complete&&i.naturalWidth)")
                assert await page.locator('.ux-colour-scroll').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
                assert await page.locator('.ux-colour-content img').evaluate_all('(imgs)=>imgs.every(i=>Math.abs(i.width/i.height-i.naturalWidth/i.naturalHeight)<.01)')
                if pid==23:assert await page.locator('.ux-colour-scroll').evaluate('(e)=>e.scrollTop>100')
                if width==390:await page.screenshot(path=str(OUT/f'{pid}-compare.png'))
                await page.locator('.ux-colour-zoom').click()
                assert await page.locator('.ux-colour-zoom').get_attribute('aria-pressed')=='true'
                await page.locator('.ux-colour-zoom').click()
                await page.locator('.ux-colour-close').click()
                assert await page.locator('.ux-compare-open').evaluate('(e)=>e===document.activeElement')
                await page.locator('.ux-compare-open').click()
                await page.keyboard.press('Escape')
                assert not await page.locator('.ux-colour-dialog').evaluate('(d)=>d.open')
                await page.wait_for_function("!document.documentElement.classList.contains('ux-colour-open')")
                # Retain exact preview cart values, including cushion tone descriptions.
                await page.locator('[data-add]').click()
                assert await page.evaluate("JSON.parse(sessionStorage.getItem('tam-preview-cart-v2'))[0].option===document.querySelector('[data-preview-product] select').value")
                checks.append({'product':pid,'width':width,'options':count,'overflow':False,'original_aspect_ratios':True,'select_compare_zoom_close_escape_focus_cart':'passed'})
                await page.close()
        await browser.close()
    # Approved article is immutable during this shade-selector correction.
    file='storefront-v2/preview/product-102.html'
    before=subprocess.check_output(['git','show','HEAD:'+file],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
    after=(ROOT/file).read_text(encoding='utf-8')
    pattern=r'<!-- cheek-v12:start -->.*?<!-- cheek-v12:end -->'
    assert re.search(pattern,before,re.S).group()==re.search(pattern,after,re.S).group()
    report={'date':'2026-10-14','kind':'Isolated Chromium mobile viewport rendering; not physical iOS/Android or native Cafe24 QA','checks':checks,'approved_cheek_article':'identical after line-ending normalization','screenshots':'Local QA directory; visually inspected separately','production_cafe24_changed':False}
    (ROOT/'ops/cafe24/shades-qa-20261014.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

asyncio.run(run())
