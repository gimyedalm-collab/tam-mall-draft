"""Refresh only the Cloud info image and alt text after independent review."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from registration_export_utils import prepare_cloud_info,panel_alt
import json,math,hashlib,re,html,zipfile
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cafe24-delivery-20261019';DEST=OUT/'cloud-blush'
manifest=DEST/'manifest.json';data=json.loads(manifest.read_text(encoding='utf-8'))
before={i['file']:i['sha256'] for i in data['files']}
with sync_playwright() as pw:
    b=pw.chromium.launch();p=b.new_page(viewport={'width':430,'height':1000},device_scale_factor=2,reduced_motion='reduce')
    p.goto((ROOT/'cloud-blush-v6/index.html').as_uri(),wait_until='networkidle');p.evaluate('document.fonts.ready')
    p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
    p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
    p.evaluate('''()=>{document.querySelectorAll('video').forEach(v=>v.pause());document.querySelectorAll('details').forEach(d=>d.open=true);document.querySelectorAll('button,.film-chapters,.film-actions,.film-caption').forEach(e=>e.remove());}''')
    prepare_cloud_info(p)
    info=p.locator('.product-info');box=info.bounding_box();top=math.floor(box['y']);bottom=math.ceil(box['y']+box['height'])
    assert top==data['files'][-1]['source_y'][0]
    assert info.locator('a').count()==0
    assert p.locator('.product-info summary').evaluate('(e)=>getComputedStyle(e).listStyleType')=='none'
    path=DEST/data['files'][-1]['file']
    p.screenshot(path=str(path),type='jpeg',quality=95,full_page=True,clip={'x':0,'y':top,'width':430,'height':bottom-top})
    im=Image.open(path);data['files'][-1].update(width=im.width,height=im.height,source_y=[top,bottom])
    for item in data['files']:
        if item['kind']=='gif':continue
        item['alt']=panel_alt(p,*item['source_y'],item is data['files'][-1])
        file=DEST/item['file'];item.update(bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest())
    b.close()
assert all(i['sha256']==before[i['file']] for i in data['files'][:-1])
data['notes'][2]='Rasterized text is not selectable; alt text carries section content where available'
data['claude_review_fix']='Removed rasterized nonfunctional link and disclosure marker; concise product-info alt; no BOM or duplicate parent captions in alt.'
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ('index.html','detail.local.html','detail.cafe24.html'):
    path=DEST/name;s=path.read_text(encoding='utf-8')
    for item in data['files']:
        filename=Path(item['file']).name
        pattern=r'<img\b[^>]*src="[^"]*/'+re.escape(filename)+r'"[^>]*>'
        def replace(match):
            tag=match[0];tag=re.sub(r'height="\d+"',f'height="{item["height"]}"',tag)
            return re.sub(r'alt="[^"]*"',lambda _: 'alt="'+html.escape(item['alt'],quote=True)+'"',tag)
        s,count=re.subn(pattern,replace,s);assert count==1,(name,filename)
    assert '\ufeff' not in s
    path.write_text(s,encoding='utf-8')
with zipfile.ZipFile(OUT/'cloud-blush-cafe24.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(DEST.rglob('*')):
        if f.is_file():z.write(f,f.relative_to(DEST))
record={'changed_image':'08-detail.jpg','all_other_image_and_gif_hashes_unchanged':True,'removed_static_link_and_disclosure_marker':True,'alt_bom_removed_and_information_alt_shortened':True,'source_information_text_preserved_except_BOM_and_nonfunctional_navigation':True}
(OUT/'cloud-info-fix-qa.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record))
