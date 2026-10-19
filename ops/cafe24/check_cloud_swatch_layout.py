"""Verify the selected wrist comparison and the actual Cafe24-format export."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'cafe24-delivery-20261019/cloud-blush'
REVIEW=ROOT/'cafe24-delivery-20261019/cloud-swatch-review'
BASE=Path(sys.argv[1])
REVIEW.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda t:re.sub(r'\s+','',t.replace('\ufeff',''))
source=BeautifulSoup((ROOT/'cloud-blush-v6/index.html').read_text(encoding='utf-8'),'html.parser')
old=BeautifulSoup((BASE/'before-index.html').read_text(encoding='utf-8'),'html.parser')
for selector in ('.hero','.texture','.formula','.ending','.product-info','.shade-grid'):
    assert str(source.select_one(selector))==str(old.select_one(selector)),selector
assert len(source.select('.arm-shade'))==len(source.select('.shade'))==6
for kind in ('arm','cheek','swatch'):
    for i in range(1,7):assert len(source.select(f'img[src$="/{kind}-{i}.jpg"]'))==1
for rec in json.loads((ROOT/'cafe24-delivery-20261019/cloud-rebalance-review/arm-provenance.json').read_text(encoding='utf-8')):
    assert sha(ROOT/rec['file'])==rec['sha256']
assert sha(DEST/'product-information.html')==sha(BASE/'before-information.html')
before=json.loads((BASE/'before-manifest.json').read_text(encoding='utf-8'))
after=json.loads((DEST/'manifest.json').read_text(encoding='utf-8'))
unchanged=[];changed=[]
for a,b in zip(before['files'],after['files']):
    (unchanged if a['sha256']==b['sha256'] else changed).append(b['file'])
assert all(f'images/{i:02}-'+('motion.gif' if i==3 else 'detail.jpg') in unchanged for i in range(1,5))
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    p=browser.new_page(viewport={'width':430,'height':1000},device_scale_factor=2)
    p.goto((ROOT/'cloud-blush-v6/index.html').as_uri(),wait_until='networkidle')
    p.evaluate('document.fonts.ready')
    p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
    p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
    arm=p.locator('.arm-comparison').bounding_box();cheek=p.locator('.cheek-comparison').bounding_box()
    assert arm['y']+arm['height']<=cheek['y']
    labels=p.locator('.arm-shade figcaption').evaluate_all('(es)=>es.map(e=>({font:parseFloat(getComputedStyle(e).fontSize),lineHeight:parseFloat(getComputedStyle(e).lineHeight),height:e.getBoundingClientRect().height}))')
    assert all(x['font']*320/430>=12 for x in labels)
    assert all(x['height']<=x['lineHeight']+1 for x in labels)
    photos=p.locator('.arm-shade img').evaluate_all('(es)=>es.map(e=>{let r=e.getBoundingClientRect();return {width:r.width,height:r.height,fit:getComputedStyle(e).objectFit}})')
    assert all(abs(x['width']-x['height'])<1 and x['fit']=='cover' for x in photos)
    p.close()
    for width in (320,390,860):
        p=browser.new_page(viewport={'width':width,'height':900},java_script_enabled=False)
        p.goto((DEST/'index.html').as_uri(),wait_until='networkidle')
        p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
        p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
        assert p.evaluate('document.documentElement.scrollWidth===innerWidth')
        assert p.locator('[data-tam-product-info]').evaluate('(e)=>getComputedStyle(e).fontSize')=='12px'
        p.locator('img[src*="/05-detail.jpg"]').screenshot(path=str(REVIEW/f'final-colours-{width}.png'))
        if width==390:p.screenshot(path=str(REVIEW/'final-page-390.jpg'),full_page=True,type='jpeg',quality=90)
        results.append({'width':width,'all_images_loaded':True,'javascript_disabled':True,'no_horizontal_overflow':True,'native_information_px':12,'wrist_label_effective_px':round(labels[0]['font']*width/430,2)})
        p.close()
    browser.close()
record={'scope':'Local Chromium on actual Cafe24-format export, not Cafe24 admin save or physical devices',
        'selected':'A: two-column, three-row overview before cheek details',
        'original_wrist_files_unchanged':True,'each_wrist_cheek_texture_used_once':True,
        'full_information_byte_identical':True,'other_source_sections_and_cheek_cards_unchanged':True,
        'unchanged_media':unchanged,'regenerated_media':changed,'checks':results,
        'owner_visual_acceptance':'pending','actual_cafe24_upload':False}
(REVIEW/'qa.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record))
