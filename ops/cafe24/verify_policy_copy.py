"""Render prepared notice HTML locally; no administrator save or policy change."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(os.environ['TAM_PERF_STAGE'])
async def main():
    results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width in (320,1440):
            page=await browser.new_page(viewport={'width':width,'height':900})
            await page.set_content((ROOT/'notice-299-preview.html').read_text(encoding='utf-8'))
            text=await page.locator('body').inner_text()
            assert '3,000원' in text and '365일' in text and '2,000' not in text
            assert await page.locator('a').count()==2
            overflow=await page.evaluate('document.documentElement.scrollWidth>innerWidth')
            assert not overflow
            await page.screenshot(path=str(ROOT/f'notice-ready-{width}.png'),full_page=True)
            results.append({'width':width,'overflow':overflow,'passed':True})
            await page.close()
        await browser.close()
    (ROOT/'policy-copy-qa.json').write_text(json.dumps({'rendered_locally':True,'saved_live':False,'cases':results,'passed':True},indent=2),encoding='utf-8')
    print(json.dumps(results))
if __name__=='__main__':asyncio.run(main())
