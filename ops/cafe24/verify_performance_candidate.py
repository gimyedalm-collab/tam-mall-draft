"""Independent public browser comparison; no owner session or commerce mutations."""
import asyncio,json,time,os
from pathlib import Path
from urllib.parse import urlsplit
from playwright.async_api import async_playwright

OUT=Path(os.environ.get('TAM_PERF_OUTPUT','performance-results'))

async def main():
    OUT.mkdir(exist_ok=True)
    report={'physical_device':False,'cache_disabled':True,'download_bps':1600000,'latency_ms':150,'cases':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        report['browser_version']=browser.version
        for skin in (21,24):
            for route in ('','board/gallery/list.html?board_no=8'):
                context=await browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,locale='ko-KR')
                page=await context.new_page();cdp=await context.new_cdp_session(page)
                await cdp.send('Network.enable')
                await cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
                await cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':93750})
                requests={};start=time.monotonic()
                def received(e):
                    u=urlsplit(e['response']['url'])
                    requests[e['requestId']]={'path':u.path,'host':u.netloc,'type':e.get('type'),'status':e['response']['status']}
                def finished(e):
                    if e['requestId'] in requests:requests[e['requestId']]['bytes']=e.get('encodedDataLength',0)
                cdp.on('Network.responseReceived',received);cdp.on('Network.loadingFinished',finished)
                r={'skin':skin,'route':route or '/'};report['cases'].append(r)
                try:
                    await page.goto(f'https://awiz.cafe24.com/skin-skin{skin}/'+route,wait_until='domcontentloaded',timeout=120000)
                    await page.wait_for_function("[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>!!e.sheet)",timeout=90000)
                    r['shell_seconds']=round(time.monotonic()-start,2)
                    r['initial_bytes']=sum(x.get('bytes',0) for x in requests.values())
                    r['initial_archive_bytes']=sum(x.get('bytes',0) for x in requests.values() if '/gallery/' in x['path'])
                    r['paints']=await page.evaluate("()=>performance.getEntriesByType('paint').map(p=>({name:p.name,seconds:p.startTime/1000}))")
                    r['overflow']=await page.evaluate('()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1')
                    assert not r['overflow']
                    selector='#tam-lookbook img,.tam-board-archive img' if route else '#tam-home-main img'
                    images=page.locator(selector);r['images']=[]
                    for i in range(await images.count()):
                        img=images.nth(i);await img.scroll_into_view_if_needed()
                        await img.evaluate("e=>e.decode()",timeout=90000)
                        item=await img.evaluate("e=>({path:new URL(e.currentSrc).pathname,srcset:e.getAttribute('srcset'),w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height,naturalW:e.naturalWidth,naturalH:e.naturalHeight,loading:e.loading})")
                        assert item['naturalW']>0 and item['w']>0
                        r['images'].append(item)
                    r['all_images_seconds']=round(time.monotonic()-start,2)
                    r['final_bytes']=sum(x.get('bytes',0) for x in requests.values())
                    if skin==24:
                        # A high-density featured image correctly chooses the
                        # existing960px source. Check available candidates, not
                        # that every screen must choose the smallest file.
                        assert sum('perf261023' in (x['srcset'] or '') for x in r['images'])==6,r['images']
                    r['passed']=True
                except Exception as e:r.update(passed=False,error=repr(e)[:500])
                r['largest_resources']=sorted(requests.values(),key=lambda x:x.get('bytes',0),reverse=True)[:12]
                print(json.dumps({k:v for k,v in r.items() if k not in ('images','largest_resources')},ensure_ascii=False),flush=True)
                (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                await context.close()
        await browser.close()
    report['passed']=all(r['passed'] for r in report['cases'])
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':asyncio.run(main())
