"""Verify the exported composition, not merely the editable browser layout."""
import argparse, hashlib, json, re, zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cafe24-delivery-20261020/powder-balm'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--screenshots',type=Path,required=True);args=ap.parse_args()
    args.screenshots.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    expected=[m['file'] for m in manifest['media']]
    local=(OUT/'detail.local.html').read_text(encoding='utf-8')
    cafe=(OUT/'detail.cafe24.html').read_text(encoding='utf-8')
    soup=BeautifulSoup(local,'html.parser')
    assert [i['src'].split('?')[0] for i in soup.find_all('img')]==expected
    assert cafe.replace(manifest['delivery_prefix'],'')==local
    assert not soup.find(['script','video','iframe','button'])
    assert not re.search(r'https?://|@font-face',local)
    assert len(soup.find_all('tr'))==9
    for item in manifest['media']:
        f=OUT/item['file']; assert hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256']
        assert f.stat().st_size<4_900_000
        if f.suffix=='.gif':
            with Image.open(f) as im:
                assert im.n_frames>1 and im.info['loop']==2
                for n in [0,im.n_frames//2,im.n_frames-1]:
                    im.seek(n);im.convert('RGB').save(args.screenshots/f'{f.stem}-frame-{n}.png')
    qa={'version':4,'product_no':111,'viewports':[],'composition_matches_cafe24_fragment':True,'source_media_count':len(expected),'custom_js_fonts_or_video_host_required':False,'all_media_below_4_9_MB':True,'native_information_rows':9,'cafe24_live_upload_verified':False,'physical_device_verified':False}
    with sync_playwright() as p:
        browser=p.chromium.launch()
        for width in [320,390,430,860,1280]:
            page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
            errors=[]; page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto((OUT/'index.html').as_uri())
            page.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
            page.wait_for_timeout(1100)
            data=page.evaluate('''()=>({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0,width:i.width,height:i.height})),heroAndApplicationHeight:[...document.images].slice(0,2).reduce((s,i)=>s+i.getBoundingClientRect().height,0),height:document.documentElement.scrollHeight})''')
            assert data['scrollWidth']==width and len(data['images'])==7 and all(i['loaded'] for i in data['images'])
            assert not errors
            page.screenshot(path=str(args.screenshots/f'preview-{width}.png'),full_page=True)
            if width==390:page.screenshot(path=str(args.screenshots/'first-screen-390.png'))
            # Scroll through every exported asset to force actual layout/decoding.
            for img in page.locator('img').all():img.scroll_into_view_if_needed()
            qa['viewports'].append(data);page.close()
        source=browser.new_page(viewport={'width':430,'height':900},device_scale_factor=1)
        source.goto((ROOT/'powder-balm-v4/layout.html').as_uri());source.evaluate('document.fonts.ready')
        source.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
        clipping=source.evaluate('''()=>[...document.querySelectorAll('section')].flatMap(s=>[...s.querySelectorAll('h1,h2,h3,p,img')].filter(e=>{let a=s.getBoundingClientRect(),b=e.getBoundingClientRect();return b.bottom>a.bottom+1||b.right>a.right+1||b.left<a.left-1}).map(e=>({section:s.id,text:e.innerText||e.alt})))''')
        assert not clipping,clipping
        browser.close()
    qa['source_text_and_image_clipping']=[]
    qa['visual_review']='pending'
    record=ROOT/'ops/cafe24/powder-balm-v4-preview-qa-20261021.json'
    record.write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'screenshots':str(args.screenshots),'viewports':[v['viewport'] for v in qa['viewports']],'first_screen_height_at_390':qa['viewports'][1]['heroAndApplicationHeight']},ensure_ascii=False))

if __name__=='__main__':main()
