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
        wait_for(lambda:script("return !!document.querySelector('.ux-header')"))
        if route.startswith('product-'):
            wait_for(lambda:script("return !!document.querySelector('.tam-purchase')"))

    try:
        wait_for(lambda: driver.poll() is None and port_ready(), 15)
        created=request('POST','/session',{'capabilities':{'alwaysMatch':{'browserName':'safari','pageLoadStrategy':'eager'}}})
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
        command('POST','/window/rect',{'width':600,'height':950,'x':0,'y':0})
        visit('product-109.html')
        # Safari's native option popup does not expose option clicks to WebDriver.
        # Use the select's ordinary keyboard interaction and verify its value.
        select=find('select')
        command('POST','/element/'+select+'/click',{})
        command('POST','/element/'+select+'/value',{'text':'01.'})
        command('POST','/element/'+select+'/value',{'text':'\ue007'})
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
        report['passed']=True
    except Exception:
        report['passed']=False
        report['failure']=traceback.format_exc()
        if session:
            try:
                report['failureUI']=script("return {url:location.href,selects:Array.from(document.querySelectorAll('select')).map(e=>({value:e.value,index:e.selectedIndex,rect:e.getBoundingClientRect().toJSON()})),activeTag:document.activeElement?.tagName};")
                (OUT/'failure.png').write_bytes(base64.b64decode(command('GET','/screenshot')))
            except Exception:
                pass
        raise
    finally:
        if session:
            try: request('DELETE','/session/'+session)
            except Exception: pass
        server.terminate(); driver.terminate()
        server_log.close(); driver_log.close()
        (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'passed':report.get('passed'),'checks':len(report['checks']),'flows':report['flows'],'actual_widths':sorted(set(c['actualWidth'] for c in report['checks']))}))


def port_ready():
    try:
        with urllib.request.urlopen('http://127.0.0.1:18765/status',timeout=1): return True
    except (OSError, urllib.error.URLError): return False


if __name__=='__main__':
    main()
