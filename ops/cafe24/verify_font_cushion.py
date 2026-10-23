"""Isolated public regression for fonts, cushion media and native options.

Does not access an owner browser profile, create carts/orders or change settings.
"""
import argparse
import asyncio
import json
import traceback
import time
from pathlib import Path
from playwright.async_api import async_playwright


async def main(base, output, slow=False):
    output.mkdir(parents=True, exist_ok=True)
    report = {'base': base, 'physical_device': False, 'cases': []}
    report['network'] = {'download_bps':1600000,'latency_ms':150,'cache_disabled':True} if slow else 'unthrottled'
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for width in ([390] if slow else [320, 390, 1440]):
            context = await browser.new_context(viewport={'width': width, 'height': 900}, locale='ko-KR', device_scale_factor=2)
            page = await context.new_page()
            if slow:
                page.set_default_timeout(90000)
                cdp = await context.new_cdp_session(page)
                await cdp.send('Network.enable')
                await cdp.send('Network.setCacheDisabled', {'cacheDisabled':True})
                await cdp.send('Network.emulateNetworkConditions', {'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':93750})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            case = {'width': width}
            report['cases'].append(case)
            try:
                start = time.monotonic()
                await page.goto(base, wait_until='domcontentloaded')
                await page.wait_for_selector('#tam-native-fonts-261023', state='attached')
                await page.evaluate('document.fonts.ready')
                case['home'] = await page.evaluate('''() => ({
                    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
                    fonts: [...document.querySelectorAll('.tam-nav-header,.do-edit h2,.do-intro h2,.tam-nav-footer')].map(e=>getComputedStyle(e).fontFamily),
                    registeredFontLoaded: [...document.fonts].some(f=>f.family.includes('Pretendard Variable') && f.status==='loaded'),
                    duplicatePreload: !!document.querySelector('link[rel=preload][href*=home-Pretendard]'),
                    optimizedImages: document.querySelectorAll('#tam-home-main img[srcset*="perf261023"]').length
                })''')
                assert not case['home']['overflow'] and not case['home']['duplicatePreload']
                assert case['home']['registeredFontLoaded'] and all('Pretendard Variable' in f for f in case['home']['fonts'])
                assert case['home']['optimizedImages'] == 6
                case['home']['shell_seconds'] = round(time.monotonic()-start, 2)
                await page.screenshot(path=str(output / f'home-{width}.png'))
                start = time.monotonic()
                await page.goto(base + 'product/detail.html?product_no=23', wait_until='domcontentloaded')
                detail = page.locator('[data-tam-cushion-version="261023"]')
                await detail.wait_for()
                case['images'] = []
                for img in await detail.locator('img').all():
                    await img.scroll_into_view_if_needed()
                    # Cafe24's native lazy loader first decodes a 1px placeholder.
                    await page.wait_for_function('(e)=>e.complete && e.naturalWidth===860', arg=await img.element_handle())
                    await img.evaluate('e=>e.decode()')
                    info = await img.evaluate('''e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight,path:new URL(e.currentSrc).pathname})''')
                    assert 0 < info['width'] <= info['naturalWidth'] and info['naturalWidth'] == 860
                    assert abs(info['height']/info['width']-info['naturalHeight']/info['naturalWidth']) < .01
                    case['images'].append(info)
                assert len(case['images']) == 10
                case['videos'] = []
                for video in await detail.locator('video').all():
                    await video.scroll_into_view_if_needed()
                    await video.evaluate('e=>e.play()')
                    await page.wait_for_function('(i)=>document.querySelectorAll("[data-tam-cushion-version] video")[i].currentTime>.1',arg=len(case['videos']))
                    info = await video.evaluate('e=>({width:e.videoWidth,height:e.videoHeight,duration:e.duration,time:e.currentTime,error:e.error?.code,controls:e.controls,inline:e.playsInline})')
                    assert info['width'] == 860 and info['time'] > 0 and info['controls'] and info['inline'] and not info.get('error')
                    case['videos'].append(info)
                    await video.evaluate('e=>e.pause()')
                assert len(case['videos']) == 3
                case['layout'] = await detail.evaluate('e=>({width:e.getBoundingClientRect().width,centerError:Math.abs(e.getBoundingClientRect().x+e.getBoundingClientRect().width/2-document.documentElement.clientWidth/2),overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1})')
                assert not case['layout']['overflow'] and case['layout']['centerError'] < 2
                case['options'] = await page.locator('.xans-product-detail select').evaluate_all('(es)=>es.map(e=>({id:e.id,choices:[...e.options].filter(o=>o.value!=="*"&&o.value!=="**"&&o.value!=="").map(o=>({value:o.value,text:o.textContent}))}))')
                assert any(len(e['choices']) == 6 for e in case['options'])
                await detail.locator('img').first.scroll_into_view_if_needed()
                await page.screenshot(path=str(output / f'cushion-{width}.png'))
                case['script_errors'] = errors
                case['detail_all_media_seconds'] = round(time.monotonic()-start, 2)
                assert not errors, errors
                case['passed'] = True
            except Exception as e:
                case.update(passed=False, error=repr(e), traceback=traceback.format_exc())
            print(json.dumps({'width':width,'passed':case['passed'],'error':case.get('error')},ensure_ascii=False),flush=True)
            (output / 'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            await context.close()
        await browser.close()
    report['passed'] = all(c['passed'] for c in report['cases'])
    (output / 'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--slow',action='store_true')
    args=parser.parse_args()
    asyncio.run(main(args.base_url.rstrip('/')+'/',args.output,args.slow))
