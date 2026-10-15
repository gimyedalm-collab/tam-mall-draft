"""Check first-screen product evidence and the new shade/purchase/FAQ paths."""
import asyncio, json, os, tempfile
from pathlib import Path
from playwright.async_api import async_playwright

OUT=Path(tempfile.gettempdir())/'tam-usp-review-20261015'
OUT.mkdir(exist_ok=True)
BASE=os.environ.get('TAM_DETAIL_BASE','http://127.0.0.1:8876').rstrip('/')

async def main():
    results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width in [320,390,860]:
            page=await browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
            await page.goto(BASE+'/highlighter-r33/')
            await page.evaluate('document.fonts.ready')
            pos=await page.locator('.h33-glow video').evaluate('(e)=>({top:e.getBoundingClientRect().top,height:e.getBoundingClientRect().height})')
            if width<=390:
                assert pos['top']<350,pos
            await page.locator('.h33-glow a').click()
            assert page.url.endswith('#h33-shades')
            for summary in await page.locator('.h33-quick-guide summary').all():
                await summary.focus()
                await page.keyboard.press('Enter')
                assert await summary.evaluate('(e)=>e.parentElement.open')
            assert await page.locator('.h33-choice-link').get_attribute('href')=='../storefront-v2/preview/product-24.html#purchase-options'
            await page.locator('.h33-choice-link').click()
            await page.wait_for_url('**/product-24.html#purchase-options')
            await page.locator('.h33-choice-link').click()
            assert page.url.endswith('#purchase-options')
            assert await page.locator('#purchase-options').evaluate('(e)=>{let r=e.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight}')
            results.append({'width':width,'first_result_video':pos,'faq_keyboard':True,'shade_anchor':True,'standalone_and_integrated_choice_links':True})
            await page.close()
        await browser.close()
    (OUT/'story-verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False))

asyncio.run(main())
