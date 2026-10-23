"""Read-only Safari checks of public skin21. No login, orders or customer exports.

Apple's macOS VM Safari is not a physical phone or iOS Safari. This runner
does not throttle the network; earlier preview throttle evidence is separate.
"""
import base64
import json
import os
import subprocess
import time
import traceback
import urllib.error
import urllib.request
import urllib.parse
from pathlib import Path

BASE = os.environ.get('TAM_BASE_URL','https://awiz.cafe24.com/skin-skin21/')
IOS_UDID = os.environ.get('TAM_IOS_SIMULATOR_UDID')
OUT = Path('native-ios-results' if IOS_UDID else 'native-safari-results')


def main():
    OUT.mkdir(exist_ok=True)
    report = {'engine': 'macOS VM Apple Safari', 'physical_phone': False,
              'iOS': False, 'network_throttled': False, 'base': BASE,
              'home': [], 'details': [], 'collections': [], 'inner': []}
    if IOS_UDID:
        report.update(engine='Apple iOS Simulator Safari',iOS=True,simulated=True)
    driver = subprocess.Popen(['/usr/bin/safaridriver', '--port', '18765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    session = None
    visit_number = 0

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

    def visit(route, allow_login=False):
        nonlocal visit_number
        visit_number += 1
        url = BASE+route+('&' if '?' in route else '?')+'qa_visit='+str(visit_number)
        cmd('POST','/url',{'url':url})
        expected='location.href==='+json.dumps(url)
        if allow_login:
            login_path=urllib.parse.urlsplit(BASE).path+'member/login.html'
            expected+=' || (location.pathname==='+json.dumps(login_path)+' && new URL(location.href).searchParams.get("returnUrl")==='+json.dumps('/'+route.split('?')[0])+')'
        wait(lambda: js('return ('+expected+") && document.readyState!=='loading' && !!document.body && [...document.querySelectorAll('link[rel=stylesheet]')].every(e=>!!e.sheet)"))

    def click(selector):
        elem = cmd('POST','/element',{'using':'css selector','value':selector})['element-6066-11e4-a52e-4f735466cecf']
        cmd('POST','/element/'+elem+'/click',{})

    try:
        wait(lambda: request('GET','/status'),15)
        # Native app/iframe requests may remain open. Wait for tested UI explicitly.
        capabilities={'browserName':'safari','pageLoadStrategy':'none'}
        if IOS_UDID:
            capabilities.update({'platformName':'iOS','safari:useSimulator':True,'safari:deviceUDID':IOS_UDID})
        created = request('POST','/session',{'capabilities':{'alwaysMatch':capabilities}})
        session = created['sessionId']
        report['browser_version'] = created['capabilities'].get('browserVersion')
        if IOS_UDID:
            report['platform_version']=created['capabilities'].get('safari:platformVersion')
            report['device_name']=created['capabilities'].get('safari:deviceName')
        cmd('POST','/timeouts',{'implicit':3000,'pageLoad':45000,'script':15000})
        report['navigator_language']=js('return navigator.language')
        assert report['navigator_language'].startswith('ko'), report['navigator_language']
        if IOS_UDID:
            fixture='<meta name="viewport" content="width=device-width,initial-scale=1"><button id="probe" style="width:150px;height:60px" onclick="this.textContent=\'clicked\'">probe</button>'
            cmd('POST','/url',{'url':'data:text/html,'+urllib.parse.quote(fixture)})
            wait(lambda: js("return !!document.querySelector('#probe')"))
            click('#probe')
            wait(lambda: js("return document.querySelector('#probe').textContent==='clicked'"),10)
            report['driver_click_preflight']=True
        dimensions=[(320,844),(390,844),(768,1024),(844,500),(1440,950),(1920,1080)]
        if IOS_UDID:
            visit('?qa=ios-initialize')
            dimensions=[tuple(js('return [innerWidth,innerHeight]'))]
        for width,height in dimensions:
            if not IOS_UDID:cmd('POST','/window/rect',{'width':width,'height':height,'x':0,'y':0})
            visit('?qa=native-safari261022')
            wait(lambda: js("return document.querySelector('.ux-header')?.hasAttribute('data-home-header-ready') && document.querySelector('video')?.readyState>=2"))
            js("window.scrollTo({top:0,behavior:'instant'});")
            wait(lambda: js("return scrollY===0 && !document.querySelector('.ux-header').classList.contains('is-solid')"))
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
            # A video may autoplay before deferred control scripts have executed.
            wait(lambda: js("return document.readyState==='complete'"),60)
            if IOS_UDID:
                js("window.__qaFilmEvents=[];for(const type of ['click','pointerdown','touchend','play','pause'])document.addEventListener(type,e=>{if(e.target.matches('video,.film-toggle'))window.__qaFilmEvents.push({type,target:e.target.tagName,trusted:e.isTrusted,time:performance.now(),paused:document.querySelector('video').paused})},true)")
            paused = js("return document.querySelector('video').paused")
            r['initial_video_paused'] = paused
            click('.film-toggle')
            wait(lambda: js("return document.querySelector('video').paused") != paused)
            click('.film-toggle')
            wait(lambda: js("return document.querySelector('video').paused") == paused)
            r['film_controls'] = True
            if IOS_UDID:
                r['film_events']=js('return window.__qaFilmEvents')
                (OUT/'home.png').write_bytes(base64.b64decode(cmd('GET','/screenshot')))
            if width<=900:
                click('.ux-menu-toggle')
                wait(lambda: js("return document.querySelector('.ux-menu-toggle').getAttribute('aria-expanded')==='true' && document.querySelector('.ux-header').classList.contains('is-solid')"))
                click('.ux-menu-toggle')
                r['menu'] = True
            js("window.scrollTo({top:350,behavior:'instant'});")
            wait(lambda: js("return document.querySelector('.ux-header').classList.contains('is-solid')"))
            r['scroll_header'] = True
        widths=[dimensions[0][0]] if IOS_UDID else [390,1440]
        for width in widths:
            if not IOS_UDID:cmd('POST','/window/rect',{'width':width,'height':950,'x':0,'y':0})
            for number, count in [(109,6),(110,18),(111,14),(118,16),(102,9),(24,14),(25,7)]:
                visit(f'product/detail.html?product_no={number}')
                wait(lambda: js("return document.querySelector('#tam-candidate-detail')?.dataset.deliveryStatus==='ready'"))
                r = js("""const box=document.querySelector('#tam-candidate-detail');return {
                  width:innerWidth,client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,
                  images:box.querySelectorAll('img').length,
                  detail_center_error:Math.abs(box.getBoundingClientRect().x+box.getBoundingClientRect().width/2-document.documentElement.clientWidth/2),
                  snaps:[...document.querySelectorAll('.snap_widget')].map(e=>e.id),
                  selects:[...document.querySelectorAll('.xans-product-detail select')].filter(e=>e.getBoundingClientRect().width>0).map(e=>({font:parseFloat(getComputedStyle(e).fontSize),height:e.getBoundingClientRect().height})),
                  viewport:document.querySelector('meta[name=viewport]')?.content};""")
                r['product'] = number
                report['details'].append(r)
                assert r['width']==width and r['scroll']<=r['client']+1 and r['images']==count,r
                assert set(['1','3','4','5']).issubset(r['snaps']),r
                assert r['detail_center_error']<1,r
                if width==390 or IOS_UDID: assert all(s['font']>=16 and s['height']>=44 for s in r['selects']),r
                if number in (109,25):
                    wait(lambda: js("return document.querySelector('.jsMobileLayer')?.dataset.tamPurchaseReady==='true'"))
                    js("window.scrollTo({top:document.querySelector('#prdDetail').getBoundingClientRect().top+scrollY+150,behavior:'instant'});")
                    wait(lambda: js("return document.querySelector('.jsMobileLayer').classList.contains('fixed') && !document.querySelector('.mobile-fix-footer').inert"))
                    click('.mobile-fix-footer .jsLayerBtn')
                    wait(lambda: js("return document.querySelector('.jsMobileLayer').getAttribute('role')==='dialog' && document.activeElement.classList.contains('tam-purchase-close')"))
                    r['purchase_sheet']=js("""const b=document.querySelector('.jsMobileLayer').getBoundingClientRect();return {left:b.left,right:b.right,bottom:b.bottom,width:innerWidth,height:innerHeight,scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth};""")
                    sheet=r['purchase_sheet']
                    assert sheet['left']>=-1 and sheet['right']<=sheet['width']+1 and sheet['bottom']<=sheet['height']+1 and sheet['scroll']<=sheet['client']+1,sheet
                    if IOS_UDID and number==25:
                        codes=js("return [...document.querySelectorAll('#product_option_id1 option')].map(e=>e.value).filter(v=>v.startsWith('P000'))")
                        assert codes==['P000000Z000P','P000000Z000Q','P000000Z000R'],codes
                        for code in codes:
                            selector='.custom-opt__item[data-value="'+code+'"]'
                            if not js('return document.querySelector('+json.dumps(selector)+').getBoundingClientRect().height>0'):
                                click('.custom-opt__current')
                            click(selector)
                        wait(lambda:js("return document.querySelectorAll('tr.option_product').length===3 && document.querySelector('#totalPrice').innerText.includes('51,000')"))
                        r['oil_options_total_verified']=51000
                    click('.tam-purchase-close')
                    wait(lambda: js("return !document.querySelector('.jsMobileLayer').classList.contains('on') && document.activeElement.classList.contains('jsLayerBtn')"))
                    r['purchase_open_close_focus']=True
            for collection, count in [('jelly',6),('cloud',8)]:
                visit('product/list.html?cate_no=74&tam_collection='+collection)
                wait(lambda: js('return document.body.dataset.tamCollection==='+json.dumps(collection)))
                r = js("return {ids:[...document.querySelectorAll('.prdList>li')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.id),width:innerWidth};")
                r['collection'] = collection
                report['collections'].append(r)
                assert len(r['ids'])==count and 'anchorBoxId_129' not in r['ids'],r
        routes = ['product/list.html?cate_no=74', 'about.html',
                  'board/gallery/list.html?board_no=8', 'product/search.html',
                  'member/login.html', 'member/join.html', 'order/basket.html',
                  'myshop/index.html', 'myshop/coupon/coupon.html',
                  'myshop/order/list.html', 'member/privacy.html',
                  'member/mall_agreement.html', 'shopinfo/guide.html']
        for width in widths:
            if not IOS_UDID:cmd('POST','/window/rect',{'width':width,'height':950,'x':0,'y':0})
            for route in routes:
                visit(route, allow_login=route.startswith('myshop/'))
                wait(lambda: js("return !!document.querySelector('.tam-nav-footer')"))
                r = js("""return {width:innerWidth,client:document.documentElement.clientWidth,
                  scroll:document.documentElement.scrollWidth,
                  header:!!document.querySelector('.tam-nav-header'),footer:!!document.querySelector('.tam-nav-footer'),
                  bodyClass:document.body.className,brand:!!document.querySelector('#tam-brand'),finalPath:location.pathname,
                  lookbook:!!document.querySelector('#tam-lookbook'),
                  brokenVisibleImages:[...document.images].filter(i=>{const r=i.getBoundingClientRect();return r.width>0&&r.height>0&&r.top<innerHeight&&r.bottom>0&&i.complete&&!i.naturalWidth}).length};""")
                r['route'] = route
                r['auth_redirect']=route.startswith('myshop/') and r['finalPath'].endswith('/member/login.html')
                report['inner'].append(r)
                assert r['width']==width and r['scroll']<=r['client']+1,r
                assert r['header'] and r['footer'] and 'tam-native' in r['bodyClass'],r
                assert r['brokenVisibleImages']==0,r
                if route=='about.html':
                    assert r['brand'],r
                    wait(lambda: js("return document.querySelectorAll('.tam-explore-grid>li').length===14"))
                    r['native_catalog_cards']=14
                if route.startswith('board/gallery'):assert r['lookbook'],r
                if route.startswith('product/list'):
                    click('button[data-tam-line=cloud]');click('button[data-tam-category=lip]')
                    ids=js("return [...document.querySelectorAll('.prdList>li')].filter(e=>!e.hidden).map(e=>e.id).sort()")
                    assert ids==['anchorBoxId_112','anchorBoxId_118'],ids
                    r['combined_filter']=True
                    if width==390 or IOS_UDID:
                        click('.tam-nav-menu-toggle')
                        assert js("return document.querySelector('.tam-nav-menu-toggle').getAttribute('aria-expanded')==='true'")
                        click('.tam-nav-menu-toggle')
                        r['mobile_menu']=True
        report['passed'] = True
    except Exception:
        report['passed'] = False
        report['failure'] = traceback.format_exc()
        if session:
            try:
                report['failure_ui'] = js("""const b=document.querySelector('.film-toggle'),r=b?.getBoundingClientRect(),top=r?document.elementFromPoint(r.x+r.width/2,r.y+r.height/2):null;
                return {url:location.href,ready:document.readyState,button:r?.toJSON(),coverTag:top?.tagName,coverClass:top?.className,filmEvents:window.__qaFilmEvents,video:document.querySelector('video')?{paused:document.querySelector('video').paused,time:document.querySelector('video').currentTime,error:document.querySelector('video').error?.code}:null};""")
                (OUT/'failure.png').write_bytes(base64.b64decode(cmd('GET','/screenshot')))
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
