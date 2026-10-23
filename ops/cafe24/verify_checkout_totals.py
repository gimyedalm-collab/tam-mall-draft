"""Isolated guest checkout totals; never fills identity or submits an order."""
import asyncio,json,os,re
from pathlib import Path
from playwright.async_api import async_playwright

OUT=Path(os.environ['TAM_CHECKOUT_OUTPUT'])
BASE='https://awiz.cafe24.com/skin-skin24/'

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report={'base':BASE,'order_submitted':False,'payment_submitted':False,'identity_entered':False,'cases':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for quantity in (1,2):
            context=await browser.new_context(viewport={'width':390,'height':844},locale='ko-KR',is_mobile=True,has_touch=True)
            page=await context.new_page();r={'quantity':quantity};report['cases'].append(r)
            try:
                await page.goto(BASE+'product/detail.html?product_no=25',wait_until='domcontentloaded',timeout=90000)
                await page.locator('.custom-opt__current').click()
                await page.locator('.custom-opt__item[data-value="P000000Z000P"]').click()
                await page.wait_for_selector('tr.option_product')
                if quantity==2:
                    await page.locator('tr.option_product input.quantity_opt').fill('2')
                    await page.locator('tr.option_product input.quantity_opt').press('Tab')
                await page.wait_for_function(f"document.querySelector('#totalPrice').innerText.includes('{quantity*17000:,}')")
                buy=page.locator('.xans-product-action a').filter(has_text='구매하기')
                # Use actual native control; do not call platform internals.
                await buy.first.click()
                await page.wait_for_timeout(1000)
                if 'login' in page.url:
                    guest=page.get_by_role('link',name='비회원 구매',exact=False)
                    await guest.click()
                await page.wait_for_url('**/order/orderform.html*',timeout=45000)
                await page.wait_for_load_state('domcontentloaded')
                text=await page.locator('body').inner_text()
                final=int(re.search(r'최종 결제 금액\s*([\d,]+)',text)[1].replace(',',''))
                shipping=int(re.search(r'배송비\s*\+([\d,]+)원',text)[1].replace(',',''))
                assert f'수량: {quantity}개' in text and '더 젤리 플럼핑 립오일' in text
                assert final==(20000 if quantity==1 else 34000) and shipping==(3000 if quantity==1 else 0)
                r.update(product_amount=17000*quantity,shipping=shipping,total=final,name_correct=True)
                r['url']=page.url.split('?')[0]
                r['overflow']=await page.evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth+1')
                await page.screenshot(path=str(OUT/f'quantity-{quantity}.png'),full_page=True)
                r['reached_orderform']=True
                assert not r['overflow']
                r['passed']=True
            except Exception as exc:
                r.update(passed=False,error=str(exc)[:700],url=page.url.split('?')[0])
            (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps({k:v for k,v in r.items() if k not in ('checkout_ui','diagnostic')},ensure_ascii=False),flush=True)
            await context.close()
        await browser.close()
    report['passed']=all(r.get('passed') for r in report['cases'])
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':asyncio.run(main())
