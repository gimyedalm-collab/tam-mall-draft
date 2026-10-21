"""Check the actual staged image/HTML delivery at mobile and desktop sizes."""
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cloud-blush-v12';D=OUT/'cafe24'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'manifest.json').read_text(encoding='utf-8'));checks=[]
prior=json.loads((ROOT/'cloud-blush-v10/cafe24/manifest.json').read_text(encoding='utf-8'))
assert (OUT/'assets/cream-spread-finish.gif').read_bytes()==(ROOT/'cloud-blush-v11/assets/cream-spread-finish.gif').read_bytes()
motion=json.loads((OUT/'motion-provenance.json').read_text(encoding='utf-8'))
gifs=[i for i in m['files'] if i['kind']=='gif']
assert len(gifs)==1 and gifs[0]['sha256']==motion['sha256']
assert (OUT/'product-information.html').read_bytes()==(ROOT/'cloud-blush-v10/product-information.html').read_bytes()
source=BeautifulSoup((OUT/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
assert not source.select('#howto,.oil-product,.vegan-product')
assert source.select_one('#formula .oil-still img')
assert not source.select('#vegan img')
assert source.select_one('#vegan .vegan-mark')
assert source.select_one('#texture #application') and source.select_one('#texture #formula')
for it in m['files']:
    f=D/it['file'];assert sha(f)==it['sha256'];assert f.stat().st_size<4_900_000
    im=Image.open(f);assert im.size==(it['width'],it['height'])
    if it['kind']=='gif':
        assert im.info['loop']==2 and im.n_frames>1
        for n in range(im.n_frames):im.seek(n);im.load()
assert len({it['sha256'] for it in m['files']})==len(m['files'])
for it in m['files'][4:10]:
    im=Image.open(D/it['file']).convert('RGB')
    # The bottom two rows belong to the neutral gap, never the next photograph.
    assert all(max(abs(a-b) for a,b in zip(im.getpixel((x,y)),(253,249,250)))<=5
               for x in range(im.width) for y in range(im.height-2,im.height))
# Hero intentionally rebuilt from original product cutouts under the latest owner instruction.
info=(D/'product-information.html').read_text(encoding='utf-8')
assert sha(D/'product-information.html')==m['product_information']['sha256']
assert BeautifulSoup(info,'html.parser').get_text(' ',strip=True)==BeautifulSoup((ROOT/'cloud-blush-v9/product-information.html').read_text(encoding='utf-8'),'html.parser').get_text(' ',strip=True)
for fn in ('index.html','detail.local.html','detail.cafe24.html'):
    txt=(D/fn).read_text(encoding='utf-8');assert info in txt
    s=BeautifulSoup(txt,'html.parser');assert not s.select('script,video,iframe,link,button')
    assert len(s.select('img'))==len(m['files'])
for oil in ['살구씨오일','동백나무씨오일','올리브오일','서양자두씨오일']:assert info.count(oil)==6
with zipfile.ZipFile(OUT/'cloud-blush-cafe24.zip') as z:
    assert z.testzip() is None
    for it in m['files']:assert hashlib.sha256(z.read(it['file'])).hexdigest()==it['sha256']
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w in (320,390,860):
        p=b.new_page(viewport={'width':w,'height':900},java_script_enabled=False)
        p.goto((D/'index.html').as_uri(),wait_until='networkidle')
        p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
        p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
        assert p.evaluate('document.documentElement.scrollWidth===innerWidth')
        rs=p.locator('img').evaluate_all('(es)=>es.map(e=>e.getBoundingClientRect().toJSON())')
        assert all(abs(rs[i]['bottom']-rs[i+1]['top'])<.05 for i in range(len(rs)-1))
        font=p.locator('[data-tam-product-info]').evaluate('(e)=>getComputedStyle(e).fontSize');assert font=='12px'
        p.screenshot(path=str(OUT/f'review-delivery-{w}.jpg'),type='jpeg',quality=92,full_page=True)
        checks.append(dict(width=w,no_overflow=True,no_seams=True,images_loaded=True,js_disabled=True,information_font=font,height=p.evaluate('document.body.scrollHeight')));p.close()
    p=b.new_page(viewport={'width':430,'height':900});p.goto((OUT/'index.html').as_uri(),wait_until='networkidle');p.evaluate('document.fonts.ready')
    fonts=p.locator('.wrist-grid figcaption,.face-row .tone,.face-row h3,.texture-grid p,.texture-grid small,.note').evaluate_all('(es)=>es.map(e=>parseFloat(getComputedStyle(e).fontSize)*320/430)');assert min(fonts)>=12
    for cap in p.locator('.face-row figcaption').all():
        assert cap.evaluate('(e)=>e.scrollHeight<=e.clientHeight')
        assert cap.locator('.tone').bounding_box()['y']+cap.locator('.tone').bounding_box()['height']<=cap.bounding_box()['y']+cap.bounding_box()['height']
    headings=p.locator('.heading h2,.intro h2').evaluate_all('(es)=>es.map(e=>getComputedStyle(e).fontSize)');assert set(headings)=={'24px'}
    assert p.locator('.hero h2').evaluate('(e)=>getComputedStyle(e).fontSize')=='28px'
    # Keep actual final browser views of key regions, not only miniatures.
    for sel,name in [('#hero','hero'),('#palette','palette'),('#faces','faces'),('#texture','texture'),('#application','application'),('#vegan','vegan'),('#formula','formula')]:p.locator(sel).screenshot(path=str(OUT/f'review-{name}-430.png'))
    b.close()
result=dict(status='candidate_package_qa_pass',files=len(m['files']),gifs=sum(it['kind']=='gif' for it in m['files']),bytes=sum(it['bytes'] for it in m['files']),largest_file_bytes=max(it['bytes'] for it in m['files']),gif_files=[{'file':it['file'],'bytes':it['bytes']} for it in m['files'] if it['kind']=='gif'],delivery_paths='All flattened into cafe24/images; source ../asset paths are not used in delivery',duplicate_export_images=False,full_gif_decode=True,zip_verified=True,information_text_unchanged=True,information_style_refined=False,oil_INCI_occurrences_each=6,colour_note_min_effective_px_320=min(fonts),widths=checks,owner_acceptance='pending',physical_shade_match='unverified',cafe24_upload='deferred_by_owner',physical_device_playback='pending_at_rollout')
(OUT/'qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))
