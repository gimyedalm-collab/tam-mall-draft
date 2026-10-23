"""Public native purchase presentation; no cart, order, login or payment mutation."""
import asyncio,json,time
from pathlib import Path
from playwright.async_api import async_playwright

BASE='https://awiz.cafe24.com/skin-skin21/'
OUT=Path('native-chromium-results')
PRODUCTS=[18,23,24,25,101,102,109,110,111,112,114,115,118,121]

async def main():
    OUT.mkdir(exist_ok=True)
    report={'base':BASE,'physical_device':False,'commerce_mutation':False,'alignment':[],'flows':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        report['browser_version']=browser.version
        context=await browser.new_context(viewport={'width':1440,'height':950})
        page=await context.new_page()
        for number in PRODUCTS:
            await page.goto(BASE+f'product/detail.html?product_no={number}',wait_until='domcontentloaded')
            await page.wait_for_selector('.jsMobileLayer[data-tam-purchase-ready=true]')
            await page.wait_for_function("[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>!!e.sheet)")
            r=await page.evaluate("""()=>{const b=document.querySelector('#tam-candidate-detail').getBoundingClientRect();return {width:innerWidth,client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,detail_width:b.width,center_error:Math.abs(b.x+b.width/2-document.documentElement.clientWidth/2)}}""")
            r['product']=number;r['passed']=r['center_error']<1 and r['scroll']<=r['client']+1
            r['purchase_css']=await page.locator('link[href*="candidate-purchase-"]').get_attribute('href')
            report['alignment'].append(r)
        await context.close()
        for width,number,slow in [(w,n,False) for w in (320,390,768,1440) for n in (109,25)]+[(390,109,True)]:
            context=await browser.new_context(viewport={'width':width,'height':844},is_mobile=width<500,has_touch=width<500)
            page=await context.new_page();errors=[]
            page.on('pageerror',lambda e:errors.append(str(e).split('\n')[0][:160]))
            if slow:
                cdp=await context.new_cdp_session(page)
                await cdp.send('Network.enable')
                await cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
                await cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':1600000/8,'uploadThroughput':750000/8})
            r={'width':width,'product':number,'slow_1_6_mbps_150ms':slow};report['flows'].append(r)
            started=time.monotonic()
            try:
                await page.goto(BASE+f'product/detail.html?product_no={number}',wait_until='domcontentloaded',timeout=120000)
                await page.wait_for_selector('.jsMobileLayer[data-tam-purchase-ready=true]',state='attached',timeout=90000)
                r['purchase_css']=await page.locator('link[href*="candidate-purchase-"]').get_attribute('href')
                await page.wait_for_function("document.querySelector('#tam-candidate-detail')?.dataset.deliveryStatus==='ready'",timeout=90000)
                await page.evaluate("window.scrollTo({top:document.querySelector('#prdDetail').getBoundingClientRect().top+scrollY+150,behavior:'instant'})")
                await page.wait_for_selector('.mobile-layer.fixed')
                await page.locator('.mobile-fix-footer .jsLayerBtn').click()
                await page.wait_for_function("document.activeElement.classList.contains('tam-purchase-close')")
                r['sheet']=await page.evaluate("""()=>{const b=document.querySelector('.mobile-layer').getBoundingClientRect(),d=document.querySelector('#tam-candidate-detail').getBoundingClientRect(),content=document.body.getBoundingClientRect();return {left:b.left,right:b.right,bottom:b.bottom,height:b.height,viewport:innerHeight,client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,content_width:content.width,center_error:Math.abs(d.x+d.width/2-(content.x+content.width/2)),locked:document.documentElement.classList.contains('tam-purchase-open')}}""")
                s=r['sheet'];assert s['left']>=-1 and s['right']<=width+1 and s['bottom']<=s['viewport']+1 and s['scroll']<=s['client']+1 and s['center_error']<1 and s['locked'],s
                if number==109:
                    await page.locator('#product_option_id1').select_option(label='01. 샌드 쉐이더')
                    await page.wait_for_function("document.querySelectorAll('tr.option_product').length===1 && document.querySelector('#totalPrice').innerText.includes('18,000')")
                    r['selected_total']=await page.locator('#totalPrice').inner_text()
                else:
                    assert (await page.locator('h1').inner_text()).strip()=='더 젤리 플럼핑 립오일'
                    r['oil_codes']=await page.locator('#product_option_id1 option').evaluate_all("es=>es.map(e=>e.value).filter(v=>v.startsWith('P000'))")
                    assert r['oil_codes']==['P000000Z000P','P000000Z000Q','P000000Z000R']
                    for code in r['oil_codes']:
                        visible_option=page.locator(f'.custom-opt__item[data-value="{code}"]')
                        if not await visible_option.is_visible():
                            await page.locator('.custom-opt__current').click()
                        await visible_option.click()
                    await page.wait_for_function("document.querySelectorAll('tr.option_product').length===3 && document.querySelector('#totalPrice').innerText.includes('51,000')")
                    r['selected_total']=await page.locator('#totalPrice').inner_text()
                await page.keyboard.press('Escape')
                await page.wait_for_function("!document.querySelector('.jsMobileLayer').classList.contains('on') && document.activeElement.classList.contains('jsLayerBtn')")
                await page.keyboard.press('Enter')
                await page.wait_for_function("document.activeElement.classList.contains('tam-purchase-close')")
                if number==109:
                    assert await page.locator('tr.option_product').count()==1
                    assert '18,000' in await page.locator('#totalPrice').inner_text()
                    r['selection_retained']=True
                else:
                    assert await page.locator('tr.option_product').count()==3
                    assert '51,000' in await page.locator('#totalPrice').inner_text()
                    r['selection_retained']=True
                await page.locator('.tam-purchase-close').click()
                await page.wait_for_function("!document.documentElement.classList.contains('tam-purchase-open')")
                r['interaction_seconds']=round(time.monotonic()-started,2)
                r['script_errors']=errors
                assert not any('scrollHeaderFixed' in x or 'candidate-purchase' in x for x in errors),errors
                r['passed']=True
            except Exception as exc:
                r.update(passed=False,error=str(exc)[:800])
                r['failure_state']=await page.evaluate("""()=>({layer:document.querySelector('.jsMobileLayer')?.className,focus:document.activeElement?.className,focusTag:document.activeElement?.tagName,scroll:scrollY,locked:document.documentElement.classList.contains('tam-purchase-open')})""")
            await context.close()
            print(json.dumps(r,ensure_ascii=False),flush=True)
        await browser.close()
    report['passed']=all(r['passed'] for r in report['alignment']+report['flows'])
    (OUT/'purchase.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':asyncio.run(main())
