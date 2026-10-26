"""Read-only public coupon entry checks; never issues coupons or submits orders."""
import argparse
import asyncio
import json
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright


async def run(output):
    report = {'base': 'https://tambeauty.kr/', 'authenticated': False,
              'coupon_issued': False, 'coupon_redeemed': False, 'order_submitted': False,
              'cases': [], 'guest_coupon_access': []}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for width in (320, 390, 1440):
            context = await browser.new_context(viewport={'width': width, 'height': 900}, locale='ko-KR')
            page = await context.new_page()
            for number in (25, 111):
                response = await page.goto(report['base'] + f'product/detail.html?product_no={number}', wait_until='domcontentloaded')
                link = page.locator('a.evt__item[href*="pf.kakao.com/_nxhIxhn"]')
                await link.wait_for(state='visible')
                href = await link.get_attribute('href')
                text = await link.inner_text()
                row = {'width': width, 'product': number, 'http': response.status,
                       'advertised_coupon_krw': 3000, 'link': href,
                       'visible': await link.is_visible(),
                       'native_options': await page.locator('#product_option_id1 option').count(),
                       'overflow': await page.evaluate('document.documentElement.scrollWidth>innerWidth+2')}
                row['passed'] = (row['visible'] and '3,000원' in text and row['native_options'] > 2 and not row['overflow']
                                 and urlparse(href).netloc == 'pf.kakao.com'
                                 and urlparse(href).path == '/_nxhIxhn')
                report['cases'].append(row)
                print('coupon entry', width, number, row['passed'], flush=True)
            page.on('dialog', lambda dialog: dialog.dismiss())
            await page.goto(report['base'] + 'myshop/coupon/coupon.html', wait_until='domcontentloaded')
            await page.wait_for_timeout(1500)
            report['guest_coupon_access'].append({
                'width': width, 'final_path': urlparse(page.url).path,
                'login_field': await page.locator('#member_id').count() > 0,
                'note': 'Anonymous view cannot establish a member coupon balance or eligibility.'})
            await context.close()
        await browser.close()
    report['passed'] = all(row['passed'] for row in report['cases'])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    assert report['passed'], report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(run(parser.parse_args().output))
