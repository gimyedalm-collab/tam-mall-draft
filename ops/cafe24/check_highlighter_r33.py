"""Verify the responsive rebuild, original evidence, motion and product shell."""
import asyncio, hashlib, json, re, subprocess
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path('C:/Users/BNK-1/AppData/Local/Temp/highlighter-r33-review')
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:8876'
EXPECTED = ['hero','glow','shades','on-skin','texture','use','formula','ending','information']

def check_sources():
    names = [('highlighter-r30/assets/',name) for name in ['product-trio.jpg','tam-moonstone.jpg','tam-pink.jpg','tam-gold.jpg','tam-pearl-detail.webp']]
    names += [('highlighter-r32/assets/',name) for name in ['real-glow.mp4','howto-four-looks-261012.mp4']]
    for prefix,name in names:
        path=prefix+name
        assert subprocess.check_output(['git','show','22469e7:'+path],cwd=ROOT)==(ROOT/path).read_bytes(),path
    product='storefront-v2/preview/product-24.html'
    old=BeautifulSoup(subprocess.check_output(['git','show','de47e52:'+product],cwd=ROOT).decode('utf-8'),'html.parser')
    new=BeautifulSoup((ROOT/product).read_text(encoding='utf-8'),'html.parser')
    for soup in (old,new):
        soup.select_one('#product-detail').decompose()
        for tag in soup.select('link[href*="highlighter-r33/detail.css"],script[src*="highlighter-r33/detail.js"]'):tag.decompose()
        for node in soup.find_all(string=lambda value:isinstance(value,Comment)):
            if 'highlighter-r33:' in node:node.extract()
    assert old.prettify().replace('\r\n','\n')==new.prettify().replace('\r\n','\n'),'Commerce outside product detail changed'
    old=BeautifulSoup((ROOT/'highlighter-r32/product-information.html').read_text(encoding='utf-8'),'html.parser')
    new=BeautifulSoup((ROOT/'highlighter-r33/index.html').read_text(encoding='utf-8'),'html.parser')
    text=lambda tags:[' '.join(tag.get_text(' ',strip=True).split()) for tag in tags]
    assert text(old.select('main h2,main p'))==text(new.select('.h33-info-copy h2,.h33-info-copy p'))
    for name in ['detail.css','detail.js']:
        revision=hashlib.sha256((ROOT/'highlighter-r33'/name).read_text(encoding='utf-8').encode()).hexdigest()[:12]
        for file in ['highlighter-r33/index.html',product]:
            assert name+'?v='+revision in (ROOT/file).read_text(encoding='utf-8')

async def main():
    check_sources()
    results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width in [320,390,600,720,800,860,1440]:
            page=await browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
            errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            await page.goto(BASE+'/highlighter-r33/',wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            for section in await page.locator('[data-panel]').all():
                await section.scroll_into_view_if_needed()
                await page.wait_for_timeout(100)
                if width in [320,390,600,860]:
                    await section.screenshot(path=str(OUT/f'{width}-{await section.get_attribute("data-panel")}.png'))
            await page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth)')
            values=await page.evaluate('''()=>({width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,
              panels:[...document.querySelectorAll('[data-panel]')].map(e=>e.dataset.panel),
              shades:document.querySelectorAll('.h33-shade').length,videos:document.querySelectorAll('video').length,
              minNote:Math.min(...[...document.querySelectorAll('.h33-note')].map(e=>parseFloat(getComputedStyle(e).fontSize))),
              frames:[...document.querySelectorAll('video')].map(e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,expected:e.width/e.height})),
              rootWidth:document.querySelector('article').getBoundingClientRect().width,
              shadeColumns:getComputedStyle(document.querySelector('.h33-shade-list')).gridTemplateColumns.split(' ').length,
              shadeTops:[...document.querySelectorAll('.h33-cheek')].map(e=>e.getBoundingClientRect().top),
              descriptionWidth:document.querySelector('.h33-shade-description').getBoundingClientRect().width,
              ingredientColumns:getComputedStyle(document.querySelector('.h33-ingredient-grid')).gridTemplateColumns.split(' ').length,
              height:document.documentElement.scrollHeight})''')
            assert not values['overflow'] and not errors,(values,errors)
            assert values['panels']==EXPECTED and values['shades']==3 and values['videos']==3
            assert values['minNote']>=11
            assert values['shadeColumns']==2
            assert abs(values['shadeTops'][0]-values['shadeTops'][1])<1 and values['shadeTops'][2]>values['shadeTops'][1],values
            assert values['descriptionWidth']>=130,values
            assert await page.locator('.h33-look-image').count()==0
            swatches=await page.locator('.h33-swatch-frame').evaluate_all('(els)=>els.map(e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,top:e.getBoundingClientRect().top}))')
            assert len(swatches)==2 and abs(swatches[0]['top']-swatches[1]['top'])<1
            assert all(abs(f['width']/f['height']-.8)<.005 for f in swatches)
            assert abs(swatches[0]['width']-swatches[1]['width'])<1
            assert (await page.locator('.h33-swatch-frame img').get_attribute('src')).endswith('arm-three-pearls-clean-261015.svg')
            assert values['ingredientColumns']==2
            assert all(abs(f['width']/f['height']-ratio)<.005 for f,ratio in zip(values['frames'],[860/1040,.8,.8]))
            assert await page.locator('video').evaluate_all('(els)=>els.every(v=>getComputedStyle(v).objectFit==="contain")')
            assert await page.locator('video').evaluate_all('(els)=>els.every(v=>v.paused&&!v.getAttribute("src"))')
            assert (await page.locator('.h33-macro img').get_attribute('src')).endswith('.jpg')
            await page.screenshot(path=str(OUT/f'{width}-full.png'),full_page=True)
            await page.locator('.h33-information summary').click()
            assert await page.locator('.h33-information details').get_attribute('open') is not None
            assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
            if width==390:
                await page.locator('.h33-information').screenshot(path=str(OUT/'390-information-open.png'))
                for selector in ['.h33-glow','.h33-on-skin','.h33-use']:
                    frame=page.locator(selector+' [data-motion]')
                    await frame.scroll_into_view_if_needed()
                    await frame.locator('button').click()
                    await page.wait_for_function('(selector)=>document.querySelector(selector+" video").currentTime>0',arg=selector)
                    await frame.locator('button').click()
                    assert await frame.locator('video').evaluate('(v)=>v.paused')
                frame=page.locator('.h33-macro');await frame.scroll_into_view_if_needed();await frame.locator('button').click()
                assert (await frame.locator('img').get_attribute('src')).endswith('.webp')
                await frame.locator('button').click()
                assert (await frame.locator('img').get_attribute('src')).endswith('.jpg')
            results.append(values)
            await page.close()
        page=await browser.new_page(viewport={'width':390,'height':844})
        await page.goto(BASE+'/highlighter-r33/',wait_until='networkidle')
        frame=page.locator('.h33-glow [data-motion]');await frame.scroll_into_view_if_needed()
        await page.wait_for_function('document.querySelector(".h33-glow video").currentTime>0')
        await frame.locator('button').click()
        await page.locator('.h33-shades').scroll_into_view_if_needed();await frame.scroll_into_view_if_needed()
        assert await frame.locator('video').evaluate('(v)=>v.paused')
        await page.locator('.h33-glow a').click()
        assert page.url.endswith('#h33-shades')
        await page.close()
        page=await browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
        await page.route('https://**/*',lambda route:route.abort())
        await page.goto(BASE+'/storefront-v2/preview/product-24.html',wait_until='domcontentloaded')
        assert await page.locator('#beam-highlighter-r33').count()==1
        assert await page.locator('#product-detail iframe').count()==0
        for panel in await page.locator('#beam-highlighter-r33 [data-panel]').all():await panel.scroll_into_view_if_needed()
        await page.evaluate('document.fonts.ready')
        assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
        await page.locator('#beam-highlighter-r33 .h33-hero').screenshot(path=str(OUT/'390-integrated-hero.png'))
        await page.locator('#beam-highlighter-r33 .h33-shades').screenshot(path=str(OUT/'390-integrated-shades.png'))
        await page.locator('.highlighter-detail-return').click()
        assert page.url.endswith('#purchase-options')
        # Cafe24 can insert the article into a narrow column on a wide screen.
        # Its layout must follow the article width, not the browser viewport.
        await page.set_viewport_size({'width':1440,'height':900})
        await page.locator('#beam-highlighter-r33').evaluate('(root)=>root.style.maxWidth="390px"')
        await page.locator('.h33-shades').scroll_into_view_if_needed()
        await page.locator('.h33-shades').screenshot(path=str(OUT/'1440-narrow-container-shades.png'))
        assert await page.locator('.h33-shades').evaluate('(el)=>getComputedStyle(el).paddingTop')=='40px'
        assert await page.locator('.h33-shade-description').evaluate_all('(els)=>els.every(el=>el.getBoundingClientRect().width>=130)')
        results.append({'sources':'Original hero, shade photos, two videos and pearl animation unchanged; existing product information text preserved.',
                        'motion':'Autoplay, persistent user pause, reduced-motion initial stills, explicit video and animated-image play/pause passed.',
                        'integration':'Scoped native detail, no iframe; original commerce DOM preserved; colour and purchase return anchors work.'})
        await browser.close()
    (OUT/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))

asyncio.run(main())
