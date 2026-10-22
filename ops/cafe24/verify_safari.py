"""CI regression on Apple's real macOS Safari, not iOS or a physical phone.

Runs only against this repository on loopback. No admin session, credentials,
payment, or customer content is sent to the runner or included in evidence.
Uses Apple's built-in safaridriver and the W3C WebDriver protocol; no install.
"""
import base64
import json
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'safari-results'
ROUTES = ['design-only.html', 'shop.html', 'search.html', 'cloud.html', 'jelly.html',
          'about.html', 'lookbook.html', 'login.html']
ROUTES += [f'product-{n}.html' for n in [110,111,25,118,102,24,23,109,101,112,114,115,121,18]]
ROUTES += ['basket.html', 'checkout.html', 'coupons.html']
MEASURE = """return {
 route:location.pathname.split('/').pop(), actualWidth:innerWidth,
 clientWidth:document.documentElement.clientWidth,
 documentWidth:document.documentElement.scrollWidth,
 overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1,
 mobileFields:Array.from(document.querySelectorAll('.field input:not([type=search]),.field select,.field textarea')).filter(e=>e.getBoundingClientRect().width>0).map(e=>parseFloat(getComputedStyle(e).fontSize)),
 mobileControlHeights:Array.from(document.querySelectorAll('.field input:not([type=search]),.field select,.field textarea')).filter(e=>e.getBoundingClientRect().width>0).map(e=>e.getBoundingClientRect().height),
 detailImages:document.querySelectorAll('#product-detail img').length,
 detailLazy:document.querySelectorAll('#product-detail img[loading=lazy]').length,
 headerReady:!!document.querySelector('.ux-header'),
 purchaseReady:!!document.querySelector('.tam-purchase'),
 viewportMeta:document.querySelector('meta[name=viewport]')?.content
};"""


def main():
    OUT.mkdir(exist_ok=True)
    report = {'engine': 'Apple Safari via safaridriver on GitHub macOS VM',
              'physical_device': False, 'iOS_Safari': False,
              'commit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
              'checks': [], 'flows': {}}
    server_log = (OUT/'http.log').open('w')
    driver_log = (OUT/'safaridriver.log').open('w')
    server = subprocess.Popen([sys.executable,'-m','http.server','18764','--bind','127.0.0.1'], cwd=ROOT, stdout=server_log, stderr=subprocess.STDOUT)
    driver = subprocess.Popen(['/usr/bin/safaridriver','--port','18765'], stdout=driver_log, stderr=subprocess.STDOUT)
    session = None
    slow_server = None

    def request(method, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        req = urllib.request.Request('http://127.0.0.1:18765'+path, data=data,
                                     headers={'Content-Type':'application/json'}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.load(response).get('value')
        except urllib.error.HTTPError as exc:
            raise RuntimeError(exc.read().decode()) from exc
        if isinstance(result, dict) and result.get('error'):
            raise RuntimeError(str(result))
        return result

    def command(method, path, payload=None):
        return request(method, '/session/'+session+path, payload)

    def script(source):
        return command('POST','/execute/sync',{'script':source,'args':[]})

    def wait_for(predicate, timeout=20):
        deadline=time.monotonic()+timeout
        while time.monotonic()<deadline:
            if predicate(): return
            time.sleep(.2)
        raise AssertionError('Timed out waiting for rendered UI')

    def find(selector, using='css selector'):
        value=command('POST','/element',{'using':using,'value':selector})
        return value['element-6066-11e4-a52e-4f735466cecf']

    def click(selector, using='css selector'):
        command('POST','/element/'+find(selector,using)+'/click',{})

    def visit(route):
        command('POST','/url',{'url':'http://127.0.0.1:18764/storefront-v2/preview/'+route})
        wait_for(lambda:script("return document.readyState==='complete' && Array.from(document.querySelectorAll('link[rel=stylesheet]')).every(e=>!!e.sheet)"),45)
        wait_for(lambda:script("return !!document.querySelector('.ux-header')"))
        if route.startswith('product-'):
            wait_for(lambda:script("return !!document.querySelector('.tam-purchase')"))

    def screenshot(name):
        (OUT/name).write_bytes(base64.b64decode(command('GET','/screenshot')))

    def header_state():
        return script("""const h=document.querySelector('.ux-header'),v=document.querySelector('.do-hero video'),b=document.querySelector('.film-toggle');
        return {width:innerWidth,height:innerHeight,scrollY,header:h.getBoundingClientRect().toJSON(),
        background:getComputedStyle(h).backgroundColor,color:getComputedStyle(h).color,solid:h.classList.contains('is-solid'),
        video:v.getBoundingClientRect().toJSON(),fit:getComputedStyle(v).objectFit,
        filmButton:b.getBoundingClientRect().toJSON(),overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1};""")

    try:
        wait_for(lambda: driver.poll() is None and port_ready(), 15)
        created=request('POST','/session',{'capabilities':{'alwaysMatch':{'browserName':'safari','pageLoadStrategy':'normal'}}})
        session=created['sessionId']
        report['capabilities']=created['capabilities']
        report['safari_version']=subprocess.check_output(['/usr/bin/safaridriver','--version'],text=True).strip()
        command('POST','/timeouts',{'implicit':5000,'pageLoad':45000,'script':15000})
        for width in [390,1440]:
            command('POST','/window/rect',{'width':width,'height':950,'x':0,'y':0})
            for route in ROUTES:
                visit(route)
                result=script(MEASURE)
                result['requestedWindowWidth']=width
                report['checks'].append(result)
                assert not result['overflow'], result
                if result['actualWidth']<=900:
                    assert all(size>=16 for size in result['mobileFields']), result
                    assert all(height>=44 for height in result['mobileControlHeights']), result
        command('POST','/window/rect',{'width':600,'height':950,'x':0,'y':0})
        visit('product-109.html')
        # Open the native select before clicking its option in Safari.
        select=find('select')
        command('POST','/element/'+select+'/click',{})
        click('select option:nth-child(2)')
        wait_for(lambda:script("return document.querySelector('select').selectedIndex===1"))
        quantity=find('input[type=number]')
        command('POST','/element/'+quantity+'/clear',{})
        command('POST','/element/'+quantity+'/value',{'text':'2'})
        click("//button[normalize-space()='장바구니에 담기']",'xpath')
        wait_for(lambda:script("return document.querySelector('[role=status]')?.textContent.includes('담았습니다')"))
        visit('basket.html')
        wait_for(lambda:script("return !!document.querySelector('.quantity-control')"))
        report['flows']['cart']=script("return {quantity:document.querySelector('.quantity-control').textContent,amountCorrect:document.querySelector('main').textContent.includes('36,000원')};")
        assert report['flows']['cart']['amountCorrect']
        visit('product-111.html')
        wait_for(lambda:script("return !!document.querySelector('.rvg')"))
        click('.rvg button[aria-label="다음 페이지"]')
        wait_for(lambda:script("return document.querySelector('.rvg [aria-current=page]')?.textContent==='2'"))
        report['flows']['reviewNext']=True
        visit('design-only.html')
        click('.ux-menu-toggle')
        report['flows']['menu']=script("return document.querySelector('.ux-menu-toggle').getAttribute('aria-expanded')==='true';")
        assert report['flows']['menu']
        report['home_header']=[]
        for width,height in [(320,844),(390,844),(768,1024),(1440,950),(1920,950),(844,500)]:
            command('POST','/window/rect',{'width':width,'height':height,'x':0,'y':0})
            visit('design-only.html')
            script("document.querySelector('video').pause();document.querySelector('video').currentTime=1;window.scrollTo({top:0,behavior:'instant'});")
            wait_for(lambda:script("return !document.querySelector('video').seeking && !document.querySelector('.ux-header').classList.contains('is-solid')"))
            top=header_state()
            assert top['video']['top']==0 and top['video']['bottom']<=top['height']+1,top
            assert top['fit']=='contain' and not top['overflow'],top
            assert abs(top['video']['width']/top['video']['height']-16/9)<.02,top
            assert top['filmButton']['top']>=top['header']['bottom'],top
            screenshot(f'home-{width}-top.png')
            script("window.scrollTo({top:300,behavior:'instant'})")
            wait_for(lambda:script("return document.querySelector('.ux-header').classList.contains('is-solid')"))
            scrolled=header_state()
            assert scrolled['header']['top']==0 and scrolled['background']=='rgb(250, 249, 248)',scrolled
            script("window.scrollTo({top:0,behavior:'instant'})")
            wait_for(lambda:script("return !document.querySelector('.ux-header').classList.contains('is-solid')"))
            if top['width']<=900:
                click('.ux-menu-toggle')
                wait_for(lambda:script("return document.querySelector('.ux-header').classList.contains('is-solid')"))
                assert script("return getComputedStyle(document.querySelector('.ux-links')).color==='rgb(40, 35, 38)'")
                screenshot(f'home-{width}-menu.png')
                command('POST','/element/'+find('.ux-menu-toggle')+'/value',{'text':'\ue00c'})
                wait_for(lambda:script("return document.querySelector('.ux-menu-toggle').getAttribute('aria-expanded')==='false'"))
            script("document.querySelector('video').currentTime=7;")
            wait_for(lambda:script("return document.querySelector('.ux-header').hasAttribute('data-film-ending')"))
            ending=header_state()
            assert ending['color']=='rgb(40, 35, 38)' and not ending['solid'],ending
            screenshot(f'home-{width}-ending.png')
            report['home_header'].append(dict(top=top,scrolled=scrolled,ending=ending,menu_verified=top['width']<=900))
        # Finish the previously missing slow-network mobile check in real Safari.
        slow_server=subprocess.Popen([sys.executable,'-u','ops/cafe24/slow_preview_server.py','--root',str(ROOT),'--port','18766','--bytes-per-second','200000','--latency-ms','150','--log',str(OUT/'slow-requests.jsonl')],cwd=ROOT,stdout=server_log,stderr=subprocess.STDOUT)
        def slow_ready():
            try:
                with urllib.request.urlopen('http://127.0.0.1:18766/storefront-v2/preview/assets/home-header.js',timeout=2): return True
            except OSError: return False
        wait_for(slow_ready,10)
        # A fresh Safari session allows early UI checks without waiting for all media.
        request('DELETE','/session/'+session)
        session=None
        created=request('POST','/session',{'capabilities':{'alwaysMatch':{'browserName':'safari','pageLoadStrategy':'eager'}}})
        session=created['sessionId']
        command('POST','/timeouts',{'implicit':5000,'pageLoad':60000,'script':15000})
        command('POST','/window/rect',{'width':390,'height':844,'x':0,'y':0})
        report['slow_network']={'bytes_per_second':200000,'request_delay_ms':150,'physical_network':False,'checks':[]}
        for route in ['design-only.html','product-109.html','product-111.html']:
            started=time.monotonic()
            command('POST','/url',{'url':'http://127.0.0.1:18766/storefront-v2/preview/'+route})
            wait_for(lambda:script("return document.querySelector('.ux-header') && Array.from(document.querySelectorAll('link[rel=stylesheet]')).every(e=>!!e.sheet)"),45)
            if route.startswith('product'):
                wait_for(lambda:script("return !!document.querySelector('.tam-purchase')"),45)
            else:
                wait_for(lambda:script("return document.querySelector('.ux-header').hasAttribute('data-home-header-ready')"),45)
            result=script(MEASURE)
            result['ui_ready_seconds']=round(time.monotonic()-started,3)
            assert result['actualWidth']==390 and not result['overflow'],result
            if route.startswith('product'):
                click('select');click('select option:nth-child(2)')
                quantity=find('input[type=number]')
                command('POST','/element/'+quantity+'/clear',{})
                command('POST','/element/'+quantity+'/value',{'text':'2'})
                click("//button[normalize-space()='장바구니에 담기']",'xpath')
                wait_for(lambda:script("return document.querySelector('[role=status]')?.textContent.includes('담았습니다')"))
                result['add_to_cart']=True
            else:
                click('.ux-menu-toggle')
                result['menu_open']=script("return document.querySelector('.ux-menu-toggle').getAttribute('aria-expanded')==='true' && document.querySelector('.ux-header').classList.contains('is-solid')")
                assert result['menu_open']
            result['loaded_detail_images']=script("return Array.from(document.querySelectorAll('#product-detail img')).filter(e=>e.complete&&e.naturalWidth>0).length")
            report['slow_network']['checks'].append(result)
        report['passed']=True
    except Exception:
        report['passed']=False
        report['failure']=traceback.format_exc()
        if session:
            try:
                report['failureUI']=script("return {url:location.href,selects:Array.from(document.querySelectorAll('select')).map(e=>({value:e.value,index:e.selectedIndex,rect:e.getBoundingClientRect().toJSON()})),activeTag:document.activeElement?.tagName};")
                if report['failureUI']['url'].endswith('/design-only.html'):
                    (OUT/'failure.png').write_bytes(base64.b64decode(command('GET','/screenshot')))
            except Exception:
                pass
        raise
    finally:
        if session:
            try: request('DELETE','/session/'+session)
            except Exception: pass
        server.terminate(); driver.terminate()
        if slow_server: slow_server.terminate()
        server_log.close(); driver_log.close()
        (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'passed':report.get('passed'),'checks':len(report['checks']),'flows':report['flows'],'actual_widths':sorted(set(c['actualWidth'] for c in report['checks']))}))


def port_ready():
    try:
        with urllib.request.urlopen('http://127.0.0.1:18765/status',timeout=1): return True
    except (OSError, urllib.error.URLError): return False


if __name__=='__main__':
    main()
