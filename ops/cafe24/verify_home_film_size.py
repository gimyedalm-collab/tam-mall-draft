"""Verify public film geometry and sampled frames without changing film bytes."""
import argparse,asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright

async def run(base,out):
    out.mkdir(parents=True,exist_ok=True)
    report={'base':base,'physical_device':False,'cases':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width,height in [(320,844),(390,844),(768,1024),(844,500),(1440,950),(1920,1080)]:
            context=await browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,locale='ko-KR')
            page=await context.new_page()
            await page.goto(base+'?qa=film-size261023',wait_until='domcontentloaded')
            await page.wait_for_selector('#tam-native-film-261023',state='attached')
            await page.wait_for_function('document.querySelector(".home-film-media video")?.readyState>=2 && document.querySelector(".ux-header")?.hasAttribute("data-home-header-ready")')
            video=page.locator('.home-film-media video')
            await video.evaluate('e=>e.pause()')
            info=await video.evaluate('e=>({rect:e.getBoundingClientRect().toJSON(),width:e.videoWidth,height:e.videoHeight,duration:e.duration,fit:getComputedStyle(e).objectFit,src:e.currentSrc})')
            expected=height if width>=height else min(width if width<=600 else width*.75,height*(.72 if width<=600 else .78))
            assert abs(info['rect']['height']-expected)<1 and abs(info['rect']['width']-width)<1,info
            assert info['rect']['x']==0 and info['rect']['y']==0 and info['fit']=='cover',info
            assert not await page.evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth+1')
            info.update(viewport=[width,height],expected_height=expected,passed=True)
            report['cases'].append(info)
            for step,fraction in enumerate([.02,.45,.85]):
                time=min(info['duration']-.1,info['duration']*fraction)
                await video.evaluate('(e,t)=>e.currentTime=t',time)
                await page.wait_for_function('(t)=>{const v=document.querySelector(".home-film-media video");return !v.seeking&&Math.abs(v.currentTime-t)<.1}',arg=time)
                await page.screenshot(path=str(out/f'film-{width}-{step}.png'))
            await context.close()
        await browser.close()
    report['passed']=True
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'cases':len(report['cases'])}))

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--base-url',required=True);a.add_argument('--output',type=Path,required=True)
    v=a.parse_args();asyncio.run(run(v.base_url.rstrip('/')+'/',v.output))
