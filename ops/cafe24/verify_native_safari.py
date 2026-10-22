"""Read-only Safari checks of public skin21. No login, orders or customer exports.

Apple's macOS VM Safari is not a physical phone or iOS Safari. This runner
does not throttle the network; earlier preview throttle evidence is separate.
"""
import json
import subprocess
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

BASE = 'https://awiz.cafe24.com/skin-skin21/'
OUT = Path('native-safari-results')


def main():
    OUT.mkdir(exist_ok=True)
    report = {'engine': 'macOS VM Apple Safari', 'physical_phone': False,
              'iOS': False, 'network_throttled': False, 'base': BASE,
              'home': [], 'details': [], 'collections': []}
    driver = subprocess.Popen(['/usr/bin/safaridriver', '--port', '18765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    session = None

    def request(method, path, data=None):
        payload = None if data is None else json.dumps(data).encode()
        req = urllib.request.Request('http://127.0.0.1:18765'+path, data=payload,
                                     headers={'Content-Type':'application/json'}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=55) as response:
                return json.load(response)['value']
        except urllib.error.HTTPError as exc:
            raise RuntimeError(exc.read().decode('utf-8','replace')) from exc

    def cmd(method, path, data=None):
        return request(method, '/session/'+session+path, data)

    def js(code):
        return cmd('POST','/execute/sync',{'script':code,'args':[]})

    def wait(predicate, seconds=40):
        deadline = time.monotonic()+seconds
        while time.monotonic()<deadline:
            try:
                if predicate(): return
            except (OSError, urllib.error.URLError):
                pass
            time.sleep(.25)
        raise AssertionError('Timed out waiting for native UI')

    def visit(route):
        cmd('POST','/url',{'url':BASE+route})
        wait(lambda: js("return document.readyState!=='loading' && !!document.body && [...document.querySelectorAll('link[rel=stylesheet]')].every(e=>!!e.sheet)"))

    def click(selector):
        elem = cmd('POST','/element',{'using':'css selector','value':selector})['element-6066-11e4-a52e-4f735466cecf']
        cmd('POST','/element/'+elem+'/click',{})

    try:
        wait(lambda: request('GET','/status'),15)
        # Native app/iframe requests may remain open. Wait for tested UI explicitly.
        created = request('POST','/session',{'capabilities':{'alwaysMatch':{'browserName':'safari','pageLoadStrategy':'none'}}})
        session = created['sessionId']
        report['browser_version'] = created['capabilities'].get('browserVersion')
        cmd('POST','/timeouts',{'implicit':3000,'pageLoad':45000,'script':15000})
        for width,height in [(320,844),(390,844),(768,1024),(844,500),(1440,950),(1920,1080)]:
            cmd('POST','/window/rect',{'width':width,'height':height,'x':0,'y':0})
            visit('?qa=native-safari261022')
            wait(lambda: js("return document.querySelector('.ux-header')?.hasAttribute('data-home-header-ready') && document.querySelector('video')?.readyState>=2"))
            r = js("""const v=document.querySelector('video'), b=v.getBoundingClientRect();
              return {width:innerWidth,height:innerHeight,client:document.documentElement.clientWidth,
              scroll:document.documentElement.scrollWidth,video:{x:b.x,y:b.y,width:b.width,height:b.height,fit:getComputedStyle(v).objectFit},
              viewport:document.querySelector('meta[name=viewport]')?.content,headerSolid:document.querySelector('.ux-header').classList.contains('is-solid')};""")
            r['requested_width'] = width
            report['home'].append(r)
            # Safari26.6.2 clamps a requested320px outer window to336px.
            # Record actual width; never report this as a320px Safari check.
            r['minimum_window_clamp'] = width==320 and r['width']==336
            assert (r['width']==width or r['minimum_window_clamp']) and r['scroll']<=r['client']+1,r
            assert abs(r['video']['x'])<1 and abs(r['video']['width']-r['client'])<1,r
            expected = r['height'] if r['width']>=r['height'] else r['client']*9/16
            assert abs(r['video']['height']-expected)<1 and not r['headerSolid'],r
            paused = js("return document.querySelector('video').paused")
            r['initial_video_paused'] = paused
            click('.film-toggle')
            wait(lambda: js("return document.querySelector('video').paused") != paused)
            click('.film-toggle')
            wait(lambda: js("return document.querySelector('video').paused") == paused)
            r['film_controls'] = True
            if width<=900:
                click('.ux-menu-toggle')
                wait(lambda: js("return document.querySelector('.ux-menu-toggle').getAttribute('aria-expanded')==='true' && document.querySelector('.ux-header').classList.contains('is-solid')"))
                click('.ux-menu-toggle')
                r['menu'] = True
            js("window.scrollTo({top:350,behavior:'instant'});")
            wait(lambda: js("return document.querySelector('.ux-header').classList.contains('is-solid')"))
            r['scroll_header'] = True
        for width in (390,1440):
            cmd('POST','/window/rect',{'width':width,'height':950,'x':0,'y':0})
            for number, count in [(109,6),(110,18),(111,14),(118,16),(102,9),(24,14)]:
                visit(f'product/detail.html?product_no={number}')
                wait(lambda: js("return document.querySelector('#tam-candidate-detail')?.dataset.deliveryStatus==='ready'"))
                r = js("""const box=document.querySelector('#tam-candidate-detail');return {
                  width:innerWidth,client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,
                  images:box.querySelectorAll('img').length,
                  snaps:[...document.querySelectorAll('.snap_widget')].map(e=>e.id),
                  selects:[...document.querySelectorAll('.xans-product-detail select')].filter(e=>e.getBoundingClientRect().width>0).map(e=>({font:parseFloat(getComputedStyle(e).fontSize),height:e.getBoundingClientRect().height})),
                  viewport:document.querySelector('meta[name=viewport]')?.content};""")
                r['product'] = number
                report['details'].append(r)
                assert r['width']==width and r['scroll']<=r['client']+1 and r['images']==count,r
                assert set(['1','3','4','5']).issubset(r['snaps']),r
                if width==390: assert all(s['font']>=16 and s['height']>=44 for s in r['selects']),r
            for collection, count in [('jelly',6),('cloud',8)]:
                visit('product/list.html?cate_no=74&tam_collection='+collection)
                wait(lambda: js('return document.body.dataset.tamCollection==='+json.dumps(collection)))
                r = js("return {ids:[...document.querySelectorAll('.prdList>li')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.id),width:innerWidth};")
                r['collection'] = collection
                report['collections'].append(r)
                assert len(r['ids'])==count and 'anchorBoxId_129' not in r['ids'],r
        report['passed'] = True
    except Exception:
        report['passed'] = False
        report['failure'] = traceback.format_exc()
        if session:
            try:
                report['failure_ui'] = js("""const b=document.querySelector('.film-toggle'),r=b?.getBoundingClientRect(),top=r?document.elementFromPoint(r.x+r.width/2,r.y+r.height/2):null;
                return {url:location.href,ready:document.readyState,button:r?.toJSON(),coverTag:top?.tagName,coverClass:top?.className};""")
            except Exception:
                pass
        raise
    finally:
        if session:
            try: request('DELETE','/session/'+session)
            except Exception: pass
        driver.terminate()
        (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'passed':report.get('passed'),'home':len(report['home']),'details':len(report['details']),'collections':len(report['collections'])}))


if __name__=='__main__':
    main()
