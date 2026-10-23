"""Fresh CI Chromium sessions against real Cafe24 under CDP network throttling.

No credentials, cart changes, orders, customer exports, third-party blocking,
or claim of physical-phone testing. Reports contain geometry and timings only.
"""
import asyncio,json,time,os
from urllib.parse import urlsplit
from pathlib import Path
from playwright.async_api import async_playwright

OUT=Path('native-chromium-results')
BASE=os.environ.get('TAM_BASE_URL','https://awiz.cafe24.com/skin-skin21/')

async def main():
    OUT.mkdir(exist_ok=True)
    report={'base':BASE,'physical_device':False,'download_bps':1600000,'upload_bps':750000,'latency_ms':150,'cache_disabled':True,'results':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        report['browser_version']=browser.version
        for width,route in [(390,''),(390,'product/list.html?cate_no=74'),(390,'about.html'),
                            (390,'board/gallery/list.html?board_no=8'),(390,'product/detail.html?product_no=109'),
                            (390,'product/detail.html?product_no=25'),(1440,'product/list.html?cate_no=74'),
                            (1440,'about.html'),(320,'product/list.html?cate_no=74')]:
            context=await browser.new_context(viewport={'width':width,'height':844},is_mobile=width<500,has_touch=width<500,locale='ko-KR')
            page=await context.new_page();cdp=await context.new_cdp_session(page)
            await cdp.send('Network.enable')
            await cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
            await cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':1600000/8,'uploadThroughput':750000/8})
            r={'route':route or '/','width':width};report['results'].append(r);started=time.monotonic()
            requests={}
            def response_received(event):
                response=event['response'];url=urlsplit(response['url'])
                requests[event['requestId']]={'host':url.netloc,'path':url.path,'type':event.get('type'),
                    'status':response['status'],'mime':response.get('mimeType'),'received_at_seconds':round(time.monotonic()-started,2)}
            def loading_finished(event):
                if event['requestId'] in requests:
                    requests[event['requestId']].update(encoded_bytes=event.get('encodedDataLength',0),finished_at_seconds=round(time.monotonic()-started,2))
            cdp.on('Network.responseReceived',response_received)
            cdp.on('Network.loadingFinished',loading_finished)
            try:
                response=await page.goto(BASE+route,wait_until='domcontentloaded',timeout=120000)
                r['status']=response.status
                await page.wait_for_selector('.ux-footer' if not route else '.tam-nav-footer',state='attached',timeout=120000)
                await page.wait_for_function("[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>!!e.sheet)",timeout=120000)
                r['shell_ready_seconds']=round(time.monotonic()-started,2)
                if not route:
                    await page.wait_for_function("document.querySelector('.ux-header')?.hasAttribute('data-home-header-ready')",timeout=120000)
                    await page.locator('.ux-menu-toggle').click()
                    assert await page.locator('.ux-menu-toggle').get_attribute('aria-expanded')=='true'
                    await page.locator('.ux-menu-toggle').click()
                    r['menu']=True
                    await page.wait_for_function("document.querySelector('video').readyState>=2",timeout=120000)
                    r['video_ready_seconds']=round(time.monotonic()-started,2)
                elif route.startswith('product/list'):
                    await page.wait_for_function("document.querySelector('.tam-count')?.textContent==='14 products'",timeout=120000)
                    await page.locator('button[data-tam-line=cloud]').click();await page.locator('button[data-tam-category=lip]').click()
                    assert await page.locator('.prdList>li:not([hidden])').count()==2
                    r['combined_filter']=True
                elif route=='about.html':
                    await page.wait_for_selector('.tam-explore-grid>li',timeout=120000)
                    r['catalog_cards']=await page.locator('.tam-explore-grid>li').count()
                    assert r['catalog_cards']==14
                elif route.startswith('product/detail'):
                    await page.wait_for_selector('#tam-candidate-detail[data-delivery-status=ready]',timeout=120000)
                    r['detail_images']=await page.locator('#tam-candidate-detail img').count()
                    assert r['detail_images']==(7 if '25' in route else 6)
                r['interaction_ready_seconds']=round(time.monotonic()-started,2)
                r.update(await page.evaluate("""() => ({actual_width:innerWidth,client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,brokenVisibleImages:[...document.images].filter(i=>{const b=i.getBoundingClientRect();return b.width>0&&b.height>0&&b.top<innerHeight&&b.bottom>0&&i.complete&&!i.naturalWidth}).length})"""))
                assert r['actual_width']==width and r['scroll']<=r['client']+1 and r['brokenVisibleImages']==0,r
                r['passed']=True
            except Exception as exc:
                r.update(passed=False,error_type=type(exc).__name__,error=str(exc)[:600])
            finally:
                r['largest_resources']=sorted(requests.values(),key=lambda v:v.get('encoded_bytes',0),reverse=True)[:15]
                r['total_encoded_bytes']=sum(v.get('encoded_bytes',0) for v in requests.values())
                r['response_count']=len(requests)
                await context.close()
                print(json.dumps(r,ensure_ascii=False),flush=True)
        await browser.close()
    report['passed']=all(r['passed'] for r in report['results'])
    (OUT/'slow-network.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':asyncio.run(main())
