"""Read-only public image-resolution audit; no owner profile or customer text."""
import argparse
import asyncio
import json
import io
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright


async def run(base, out, verify=False):
    out.mkdir(parents=True, exist_ok=True)
    report={'base':base,'physical_device':False,'cases':[]}
    pixel_cache={}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width,dpr in [(1920,1),(390,3),(768,2)]:
            context=await browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=dpr,locale='ko-KR')
            page=await context.new_page()
            await page.goto(base+'product/list.html?cate_no=74',wait_until='domcontentloaded')
            await page.wait_for_selector('.prdList>li[id^=anchorBoxId_]')
            ids=await page.locator('.prdList>li[id^=anchorBoxId_]').evaluate_all('(es)=>es.map(e=>Number(e.id.replace("anchorBoxId_","")))')
            report['products']=ids
            for number in ids:
                await page.goto(base+f'product/detail.html?product_no={number}',wait_until='domcontentloaded')
                await page.wait_for_selector('.jsPrdThumbSlide img')
                await page.wait_for_function('document.querySelector(".jsPrdThumbSlide img")?.naturalWidth>1 && [...document.querySelectorAll("link[rel=stylesheet]")].every(e=>!!e.sheet)')
                await page.locator('.jsPrdThumbSlide img').evaluate_all('(es)=>Promise.all(es.map(e=>e.decode()))')
                info=await page.evaluate('''() => ({
                    images:[...document.querySelectorAll('.jsPrdThumbSlide img')].map(e=>{const r=e.getBoundingClientRect();return {src:e.currentSrc||e.src,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight,width:r.width,height:r.height,fit:getComputedStyle(e).objectFit}}),
                    overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1,
                    reviewWidgets:[...document.querySelectorAll('.snap_widget')].map(e=>e.id),
                    options:[...document.querySelectorAll('.xans-product-detail select')].map(e=>[...e.options].filter(o=>o.value.startsWith('P000')).length)
                })''')
                info.update(product=number,width=width,dpr=dpr)
                report['cases'].append(info)
                if verify:
                    assert not info['overflow'], info
                    assert all(0<i['width']<=600.5 and i['width']<=i['naturalWidth'] for i in info['images']), info
                    assert {'1','3','4','5'}.issubset(set(info['reviewWidgets'])), info['reviewWidgets']
                if number in [109,23,25,111]:await page.screenshot(path=str(out/f'p{number}-{width}.png'))
                print(json.dumps({'product':number,'width':width,'hero':info['images'][0]},ensure_ascii=False),flush=True)
                (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            await page.goto(base,wait_until='domcontentloaded')
            for img in await page.locator('#tam-home-main img').all():
                await img.scroll_into_view_if_needed()
                await img.evaluate('e=>e.decode()')
            report.setdefault('home',[]).append(await page.evaluate('''()=>({width:innerWidth,reviewSections:document.querySelectorAll('.tam-home-reviews').length,reviewWidgets:document.querySelectorAll('.snap_widget[id="1003"]').length,images:[...document.querySelectorAll('#tam-home-main img')].map(e=>({src:e.currentSrc||e.src,width:e.getBoundingClientRect().width,naturalWidth:e.naturalWidth}))})'''))
            # naturalWidth is density-corrected for srcset width descriptors.
            # Inspect decoded resource pixels, not that CSS intrinsic width.
            for item in report['home'][-1]['images']:
                if item['src'] not in pixel_cache:
                    response=await context.request.get(item['src'])
                    assert response.ok
                    with Image.open(io.BytesIO(await response.body())) as im:pixel_cache[item['src']]=im.width
                item['resourcePixels']=pixel_cache[item['src']]
                item['densityCoverage']=round(item['resourcePixels']/(item['width']*dpr),3)
            if verify:
                assert report['home'][-1]['reviewSections']==0 and report['home'][-1]['reviewWidgets']==0
                assert all(i['resourcePixels']>=i['width']*dpr for i in report['home'][-1]['images']), report['home'][-1]
            await context.close()
        await browser.close()
    report['passed']=True if verify else None
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--base-url',required=True)
    a.add_argument('--output',type=Path,required=True)
    a.add_argument('--verify',action='store_true')
    v=a.parse_args()
    asyncio.run(run(v.base_url.rstrip('/')+'/',v.output,v.verify))
