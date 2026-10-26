"""Public footer layout checks; --overlay previews a local edit without server writes."""
import argparse
import asyncio
import json
import time
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from prepare_footer import FRAGMENT, CSS

ROUTES = {'home': '', 'product': 'product/detail.html?product_no=25',
          'shop': 'product/list.html?cate_no=74', 'about': 'about.html',
          'login': 'member/login.html', 'basket': 'order/basket.html'}


async def run(args):
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'base': args.base_url, 'overlay_only': args.overlay,
              'physical_device': False, 'cases': []}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for width in (320, 390, 760, 768, 1440):
            context = await browser.new_context(viewport={'width': width, 'height': 900}, locale='ko-KR')
            if args.overlay:
                async def overlay(route):
                    if route.request.resource_type != 'document':
                        return await route.continue_()
                    response = await route.fetch()
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    old = soup.select_one('footer.tam-nav-footer')
                    if not old:
                        return await route.fulfill(response=response)
                    company = old.select_one('.tam-nav-footer-company')
                    company.img.decompose()
                    phone = old.select_one('a[href^="tel:"]')
                    runtime = str(phone.parent).split('</a>', 1)[1]
                    runtime = BeautifulSoup(runtime, 'html.parser').get_text(' ', strip=True)
                    fragment = FRAGMENT.read_text(encoding='utf-8').replace('{$phone}', phone.get_text())
                    fragment = fragment.replace('{$runtime}', runtime)
                    fragment = fragment.replace('<!--@import(/moa/import/footer/company_info.html)-->', company.decode_contents())
                    for home in soup.select('footer.ux-footer'):
                        home.decompose()
                    old.replace_with(BeautifulSoup(fragment, 'html.parser'))
                    style = soup.new_tag('style', id='tam-footer-261026')
                    style.string = CSS.read_text(encoding='utf-8')
                    soup.head.append(style)
                    await route.fulfill(response=response, body=str(soup))
                await context.route('**/*', overlay)
            for kind, route in ROUTES.items():
                page = await context.new_page()
                url = urljoin(args.base_url, route)
                url += ('&' if '?' in url else '?') + 'qa_footer=' + str(time.time_ns())
                response = await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                footer = page.locator('#tam-site-footer')
                await footer.wait_for(state='visible', timeout=15000)
                await footer.scroll_into_view_if_needed()
                await page.evaluate('document.fonts.ready')
                await footer.locator('img').evaluate('(e)=>e.decode()')
                result = await page.evaluate(r'''() => {
                  const f=document.querySelector('#tam-site-footer'), r=f.getBoundingClientRect();
                  const links=[...f.querySelectorAll('a')];
                  const visible=[...document.querySelectorAll('footer')].filter(e=>e.getBoundingClientRect().height>0);
                  const company=f.querySelector('.tam-footer-company');
                  return {width:innerWidth, height:r.height, visible_footers:visible.length,
                    overflow:document.documentElement.scrollWidth>innerWidth+2,
                    footer_bounds:r.left>=-1&&r.right<=innerWidth+1,
                    all_items_contained:[...f.querySelectorAll('*')].every(e=>{let q=e.getBoundingClientRect();return !q.width||(q.left>=r.left-1&&q.right<=r.right+1)}),
                    kakao_links:links.filter(e=>e.href.includes('pf.kakao.com')).length,
                    small_targets:links.filter(e=>e.getBoundingClientRect().height<43.5).map(e=>e.textContent),
                    company_check:!!company.querySelector('a[onclick*="bizCommPop"]'),
                    native_order:links.some(e=>new URL(e.href).pathname.replace(/^\/skin-skin\d+/,'')==='/myshop/order/list.html'),
                    native_guide:links.some(e=>new URL(e.href).pathname.replace(/^\/skin-skin\d+/,'')==='/shopinfo/guide.html'),
                    company_after_support:company.getBoundingClientRect().top>f.querySelector('.tam-footer-support').getBoundingClientRect().top,
                    font:getComputedStyle(f).fontFamily,
                    uniform_fonts:[...f.querySelectorAll('p,a,h2')].every(e=>getComputedStyle(e).fontFamily.split(',')[0]===getComputedStyle(f).fontFamily.split(',')[0]),
                    unresolved_variables:/\{\$|@import/.test(f.textContent),
                    logo_loaded:f.querySelector('img').naturalWidth>0,
                    option_count:document.querySelectorAll('#product_option_id1 option').length};
                }''')
                result.update(route=kind, http=response.status)
                result['passed'] = (result['visible_footers']==1 and not result['overflow'] and
                    result['footer_bounds'] and result['all_items_contained'] and result['kakao_links']==1 and
                    (width>760 or not result['small_targets']) and result['company_check'] and
                    result['native_order'] and result['native_guide'] and result['company_after_support'] and
                    result['logo_loaded'] and result['uniform_fonts'] and not result['unresolved_variables'] and
                    (kind!='product' or result['option_count']>2))
                report['cases'].append(result)
                if kind in ('home','product') and width in (320,390,1440):
                    await footer.screenshot(path=str(args.output/f'{kind}-{width}.png'))
                print(kind, width, result['passed'], flush=True)
                await page.close()
            await context.close()
        await browser.close()
    report['passed'] = all(c['passed'] for c in report['cases'])
    (args.output/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    assert report['passed'], 'Footer QA failed; inspect report.json'


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base-url', default='https://tambeauty.kr/')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--overlay', action='store_true')
    asyncio.run(run(ap.parse_args()))
