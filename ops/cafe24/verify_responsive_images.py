"""Public candidate image decode, aspect ratio and overflow at three widths."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright

OUT=Path(os.environ['TAM_IMAGES_OUTPUT'])
async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report={'base':'https://awiz.cafe24.com/skin-skin24/','physical_device':False,'cases':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width in (320,768,1440):
            for route in ('','board/gallery/list.html?board_no=8'):
                context=await browser.new_context(viewport={'width':width,'height':900},device_scale_factor=2,locale='ko-KR')
                page=await context.new_page();r={'width':width,'route':route or '/'};report['cases'].append(r)
                try:
                    await page.goto(report['base']+route,wait_until='domcontentloaded',timeout=90000)
                    await page.wait_for_function("[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>!!e.sheet)")
                    images=page.locator('#tam-lookbook img,.tam-board-archive img' if route else '#tam-home-main img')
                    r['images']=[]
                    for i in range(await images.count()):
                        img=images.nth(i);await img.scroll_into_view_if_needed();await img.evaluate('e=>e.decode()',timeout=60000)
                        d=await img.evaluate('e=>({w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height,nw:e.naturalWidth,nh:e.naturalHeight,fit:getComputedStyle(e).objectFit})')
                        assert d['nw']>0 and d['w']>0 and d['h']>0,d
                        if d['fit']=='fill':assert abs(d['w']/d['h']-d['nw']/d['nh'])<.02,d
                        r['images'].append(d)
                    r['overflow']=await page.evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth+1')
                    assert not r['overflow']
                    await page.evaluate('window.scrollTo(0,0)')
                    await page.screenshot(path=str(OUT/f'{width}-{"lookbook" if route else "home"}.png'))
                    r['passed']=True
                except Exception as e:r.update(passed=False,error=str(e)[:400])
                print(json.dumps({k:v for k,v in r.items() if k!='images'}),flush=True)
                await context.close()
        await browser.close()
    report['passed']=all(r.get('passed') for r in report['cases'])
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':asyncio.run(main())
