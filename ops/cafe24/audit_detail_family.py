"""Measure matching detail roles at equal widths, rather than judging separate pages."""
import asyncio, json, sys, tempfile
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(tempfile.gettempdir())/'tam-detail-family-20261015'
OUT.mkdir(exist_ok=True)
PHASE = sys.argv[1] if len(sys.argv)>1 else 'before'
BASE = 'http://127.0.0.1:8876/'

async def main():
    rows=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        for width in [390,860]:
            for name,url,root,prefix in [
                ('cheek','cheek-v12/','#milky-cheek-v12','c12'),
                ('highlighter','highlighter-r33/','#beam-highlighter-r33','h33')]:
                page=await browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
                await page.goto(BASE+url)
                await page.evaluate('document.fonts.ready')
                for panel in await page.locator('[data-panel]').all():
                    await panel.scroll_into_view_if_needed()
                await page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth)')
                row=await page.evaluate('''({root,prefix})=>{
                  const r=document.querySelector(root),q=s=>r.querySelector(s);
                  const box=s=>{let e=q(s);if(!e)return null;let b=e.getBoundingClientRect(),c=getComputedStyle(e);return {width:b.width,height:b.height,top:b.top,bottom:b.bottom,font:parseFloat(c.fontSize),radius:c.borderRadius,marginTop:c.marginTop,marginBottom:c.marginBottom,paddingTop:c.paddingTop,paddingBottom:c.paddingBottom}};
                  let h=prefix==='h33',colour=h?'.h33-shades':'.c12-colours', grid=h?'.h33-shade-list':'.c12-shade-grid';
                  const video=q('.h33-glow video'),shade=q('.h33-cheek');
                  return {rootWidth:r.getBoundingClientRect().width,
                    hero:box(h?'.h33-hero-image':'.c12-campaign'),
                    colourSection:box(colour),heading:box(colour+' header'),
                    title:box(colour+' h2'),body:box(colour+' .'+prefix+'-body'),
                    grid:{gap:getComputedStyle(q(grid)).gap,columns:getComputedStyle(q(grid)).gridTemplateColumns},
                    shade:box(h?'.h33-cheek':'.c12-cheek'),
                    shadeName:box('.'+prefix+'-shade h3'),
                    swatch:box(h?'.h33-shade-texture':'.c12-swatch'),
                    texture:box('.'+prefix+'-texture-photo'),
                    formula:box(h?'.h33-formula-art, .h33-ingredient-feature>img':'.c12-formula-art'),
                    ending:box('.'+prefix+'-ending-visual'),
                    betweenGlowAndShades:video&&shade?shade.getBoundingClientRect().top-video.getBoundingClientRect().bottom:null,
                    glowHeadingBeforeVideo:h?q('.h33-heading').getBoundingClientRect().top<video.getBoundingClientRect().top:null};
                }''',{'root':root,'prefix':prefix})
                row.update(name=name,width=width);rows.append(row)
                for panel in ['hero','shades' if name=='highlighter' else 'colours','formula','ending']:
                    await page.locator(f'[data-panel="{panel}"]').screenshot(path=str(OUT/f'{PHASE}-{name}-{width}-{panel}.png'))
                if name=='highlighter':
                    await page.locator('.h33-shades').evaluate('(e)=>window.scrollTo(0,e.offsetTop-330)')
                    await page.screenshot(path=str(OUT/f'{PHASE}-{width}-transition.png'))
                await page.close()
        await browser.close()
    if PHASE=='after':
        before=json.loads((OUT/'before.json').read_text(encoding='utf-8'))
        for width in [390,860]:
            reference=next(r for r in rows if r['name']=='cheek' and r['width']==width)
            actual=next(r for r in rows if r['name']=='highlighter' and r['width']==width)
            previous=next(r for r in before if r['name']=='highlighter' and r['width']==width)
            for role in ['hero','shade','swatch','formula','texture','ending']:
                for dimension in ['width','height']:
                    assert abs(actual[role][dimension]-reference[role][dimension])<1,(width,role,dimension)
            for role in ['shadeName','title']:
                assert abs(actual[role]['font']-reference[role]['font'])<.01,(width,role)
            assert actual['glowHeadingBeforeVideo']
            assert actual['betweenGlowAndShades']<previous['betweenGlowAndShades']*.5
    (OUT/f'{PHASE}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ['name','width','rootWidth','hero','shade','swatch','formula','betweenGlowAndShades']} for r in rows],ensure_ascii=False,indent=2))

asyncio.run(main())
