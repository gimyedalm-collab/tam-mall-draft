"""Content and rendered checks for restored wrist evidence / native information."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cafe24-delivery-20261019';DEST=OUT/'cloud-blush';REVIEW=OUT/'cloud-rebalance-review'
def norm(t):return re.sub(r'\s+','',t.replace('\ufeff',''))
original=BeautifulSoup((ROOT/'cloud-blush-v5/detail.template.html').read_text(encoding='utf-8'),'html.parser')
native=BeautifulSoup((DEST/'product-information.html').read_text(encoding='utf-8'),'html.parser')
old=original.select('.product-info>div>p')
new=native.select('[data-tam-product-info]>div>p')
assert len(new)==6
assert all(norm(p.get_text().split(']',1)[1])==norm(q.get_text()) for p,q in zip(old[1:],new))
assert norm(old[0].get_text())==norm(native.table.get_text(' '))
source=BeautifulSoup((ROOT/'cloud-blush-v6/index.html').read_text(encoding='utf-8'),'html.parser')
assert len(source.select('.arm-shade'))==len(source.select('.shade'))==6
for kind in ('arm','cheek','swatch'):
    for i in range(1,7):assert len(source.select(f'img[src$="/{kind}-{i}.jpg"]'))==1
for rec in json.loads((REVIEW/'arm-provenance.json').read_text(encoding='utf-8')):
    assert hashlib.sha256((ROOT/rec['file']).read_bytes()).hexdigest()==rec['sha256']
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for width in (320,390,860):
        p=browser.new_page(viewport={'width':width,'height':900},java_script_enabled=False)
        p.goto((DEST/'index.html').as_uri(),wait_until='networkidle')
        p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
        p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
        assert p.evaluate('document.documentElement.scrollWidth===innerWidth')
        info=p.locator('[data-tam-product-info]')
        assert info.evaluate('(e)=>getComputedStyle(e).fontSize')=='12px'
        height=info.bounding_box()['height'];total=p.locator('body>div').bounding_box()['height']
        if width in (390,860):
            info.screenshot(path=str(REVIEW/f'after-info-{width}.png'))
            p.locator('img[src*="/05-detail.jpg"]').screenshot(path=str(REVIEW/f'after-colours-{width}.png'))
        results.append({'width':width,'information_height':round(height,1),'page_height':round(total,1),'information_share_percent':round(height/total*100,1),'information_font_px':12,'no_horizontal_overflow':True,'all_images_loaded':True,'javascript_disabled':True})
        p.close()
    p=browser.new_page(viewport={'width':390,'height':900})
    p.goto((ROOT/'cloud-blush-v6/index.html').as_uri(),wait_until='networkidle')
    p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
    p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
    p.locator('.arm-comparison').screenshot(path=str(REVIEW/'arms-390.png'))
    browser.close()
record={'scope':'Local Chromium, not Cafe24 administrator save or physical phone','full_ordered_INCI_preserved':True,'all_product_facts_preserved':True,'six_original_wrist_files_byte_identical':True,'each_arm_cheek_texture_image_used_once':True,'checks':results,'owner_visual_acceptance':'pending'}
(REVIEW/'qa.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record))
