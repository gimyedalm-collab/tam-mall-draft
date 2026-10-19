from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from bs4 import BeautifulSoup
import json,hashlib,zipfile,sys
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cafe24-delivery-20261019'
QA=OUT/'qa';QA.mkdir(exist_ok=True)
checks=[]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for key in (sys.argv[1:] or ('cloud-blush','milky-cheek','highlighter','lip-oil','lip-liner')):
        dest=OUT/key;m=json.loads((dest/'manifest.json').read_text(encoding='utf-8'))
        gif_count=0
        for item in m['files']:
            f=dest/item['file'];assert f.stat().st_size<4_900_000
            assert hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256']
            im=Image.open(f);assert im.height<25600
            if item['kind']=='gif':
                assert im.info['loop']==2 and im.n_frames>1
                for i in range(im.n_frames):im.seek(i);im.load()
                gif_count+=1
        soup=BeautifulSoup((dest/'index.html').read_text(encoding='utf-8'),'html.parser')
        if m.get('product_information'):
            info=m['product_information'];path=dest/info['file']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==info['sha256']
            for filename in ('index.html','detail.local.html','detail.cafe24.html'):
                assert path.read_text(encoding='utf-8') in (dest/filename).read_text(encoding='utf-8')
            assert len(soup.select('[data-tam-product-info]'))==1
        assert not soup.select('script,video,iframe,link,button')
        assert all(Path(i['src']).suffix in ('.jpg','.jpeg','.png','.gif') for i in soup.select('img'))
        assert len(soup.select('img'))==len(m['files'])
        with zipfile.ZipFile(OUT/f'{key}-cafe24.zip') as z:
            assert z.testzip() is None
            assert all(item['file'] in z.namelist() for item in m['files'])
            if m.get('product_information'):assert z.read(m['product_information']['file'])==(dest/m['product_information']['file']).read_bytes()
        widths=[]
        for width in (320,390,860):
            p=b.new_page(viewport={'width':width,'height':1000},java_script_enabled=False)
            p.goto((dest/'index.html').as_uri(),wait_until='networkidle')
            p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
            p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
            assert p.evaluate('document.documentElement.scrollWidth===innerWidth')
            rects=p.locator('img').evaluate_all('(es)=>es.map(e=>e.getBoundingClientRect().toJSON())')
            assert all(abs(rects[i]['bottom']-rects[i+1]['top'])<1 for i in range(len(rects)-1))
            if width==390:p.screenshot(path=str(QA/f'{key}-390.jpg'),type='jpeg',quality=90,full_page=True)
            widths.append({'width':width,'no_overflow':True,'all_images_loaded':True,'no_seams':True,'javascript_disabled':True});p.close()
        checks.append({'product':key,'files':len(m['files']),'gifs':gif_count,'total_bytes':sum(i['bytes'] for i in m['files']),'largest_file_bytes':max(i['bytes'] for i in m['files']),'widths':widths,'all_gif_frames_decoded':True,'zip_verified':True,'cafe24_actual_upload_verified':False})
    b.close()
if sys.argv[1:] and (OUT/'qa.json').exists():
    previous=json.loads((OUT/'qa.json').read_text(encoding='utf-8'))
    updated={c['product']:c for c in checks}
    records=[updated.get(c['product'],c) for c in previous]
else:records=checks
(OUT/'qa.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks))
