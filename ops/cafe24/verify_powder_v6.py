"""Independent CI browser check: image decode, geometry, responsive sources and purchase UI."""
import argparse, asyncio, json, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=Path('powder-v6-results')
BASE='https://awiz.cafe24.com/skin-skin21/'

async def main():
    parser=argparse.ArgumentParser();parser.add_argument('--local',action='store_true');args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    report={'physical_device':False,'product_no':111,'checks':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width,dpr,slow in [(320,2,False),(390,2,False),(768,2,False),(1440,1,False),(1440,2,False),(390,2,True)]:
            if args.local and slow: continue
            context=await browser.new_context(viewport={'width':width,'height':900},device_scale_factor=dpr)
            page=await context.new_page();errors=[]
            page.on('pageerror',lambda e:errors.append(str(e).split('\n')[0][:160]))
            if slow:
                cdp=await context.new_cdp_session(page)
                await cdp.send('Network.enable')
                await cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
                await cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':1600000/8,'uploadThroughput':750000/8})
            result={'width':width,'dpr':dpr,'slow':slow};report['checks'].append(result)
            try:
                start=time.monotonic()
                url=(ROOT/'cafe24-delivery-20261022/powder-balm/index.html').as_uri() if args.local else BASE+'product/detail.html?product_no=111'
                await page.goto(url,wait_until='domcontentloaded',timeout=120000)
                await page.wait_for_selector('[data-tam-powder-version="6"]',timeout=90000)
                result['composition_ready_seconds']=round(time.monotonic()-start,2)
                images=page.locator('[data-tam-powder-version] img')
                assert await images.count()==14
                result['images']=[]
                for index in range(14):
                    img=images.nth(index)
                    await img.scroll_into_view_if_needed()
                    await page.wait_for_function('(n)=>{const i=document.querySelectorAll("[data-tam-powder-version] img")[n];return i.complete&&i.naturalWidth>0}',arg=index,timeout=90000)
                    row=await img.evaluate('''i=>{const b=i.getBoundingClientRect(),r=i.parentElement.getBoundingClientRect();return {source:i.currentSrc.split('/').pop(),width:b.width,height:b.height,center_error:Math.abs(b.x+b.width/2-r.x-r.width/2),width_error:Math.abs(b.width-r.width),natural_width:i.naturalWidth,ratio_error:Math.abs(b.height/b.width-Number(i.getAttribute('height'))/Number(i.getAttribute('width')))}}''')
                    assert row['width']>0 and row['width']<=668.1 and row['center_error']<1 and row['width_error']<1 and row['ratio_error']<.001,row
                    result['images'].append(row)
                result['all_images_seen_seconds']=round(time.monotonic()-start,2)
                assert await page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+1')
                if not args.local:
                    await page.locator('.mobile-fix-footer .jsLayerBtn').click()
                    await page.wait_for_selector('.jsMobileLayer.on .tam-purchase-close')
                    await page.keyboard.press('Escape')
                    await page.wait_for_function('document.activeElement.classList.contains("jsLayerBtn")')
                    result['native_purchase_open_close']=True
                # Store only our generated detail, excluding customer-review content.
                await images.nth(0).scroll_into_view_if_needed()
                await page.screenshot(path=str(OUT/f'{"local" if args.local else "native"}-{width}-{dpr}-{slow}.png'))
                result['errors']=errors; assert not errors,errors
                result['passed']=True
            except Exception as e:
                result['passed']=False;result['failure']=str(e)[:1500]
            await context.close()
        if not args.local:
            page=await browser.new_page()
            await page.goto(BASE+'product/detail.html?product_no=109',wait_until='domcontentloaded')
            await page.wait_for_selector('[data-delivery-product="109"]')
            report['other_product_unchanged']=await page.evaluate('!document.body.classList.contains("tam-powder-balm")&&!document.querySelector("[data-tam-powder-version]")&&document.querySelector("#tam-candidate-detail img").getAttribute("src")==="/tam-detail-20261022/p109-01-hero.png"')
        await browser.close()
    report['passed']=all(c['passed'] for c in report['checks']) and report.get('other_product_unchanged',True)
    (OUT/('local.json' if args.local else 'native.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'checks':len(report['checks'])}))
    assert report['passed']

if __name__=='__main__':asyncio.run(main())
