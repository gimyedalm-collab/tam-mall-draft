"""Export V10 to a staged Cafe24 package first. Promote only after visual QA."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import hashlib, html, json, shutil, zipfile, subprocess, math
ROOT=Path(__file__).resolve().parents[2]; SOURCE=ROOT/'cloud-blush-v10'
DEST=SOURCE/'cafe24';DEST.mkdir(exist_ok=True);(DEST/'images').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
items=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':430,'height':1000},device_scale_factor=2)
    p.goto((SOURCE/'index.html').as_uri(),wait_until='networkidle');p.evaluate('document.fonts.ready')
    p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
    assert p.evaluate('document.documentElement.scrollWidth===innerWidth')
    for loc in p.locator('.export-panel,.export-motion').all():
        n=len(items)+1; motion='export-motion' in (loc.get_attribute('class') or '')
        if motion:
            src=(SOURCE/loc.get_attribute('data-gif')).resolve();file=f'images/{n:02}-motion.gif'
            img=loc.locator('img');alt=img.get_attribute('alt');kind='gif'
            if 'inset' not in (loc.get_attribute('class') or ''):
                shutil.copy2(src,DEST/file)
            else:
                # Preserve the reference's side margins in the actual GIF canvas.
                rect=loc.bounding_box();ir=img.bounding_box();w=round(ir['width']*2);h=round(ir['height']*2)
                x=round((ir['x']-rect['x'])*2);y=round((ir['y']-rect['y'])*2);ch=math.ceil(rect['height']*2)
                # Same media rectangle, border and background as V8: reuse exact GIF bytes.
                prior=json.loads((ROOT/'cloud-blush-v8/cafe24/manifest.json').read_text(encoding='utf-8'))
                item=[i for i in prior['files'] if i['kind']=='gif'][-1]
                original=ROOT/'cloud-blush-v8/cafe24'/item['file']
                assert Image.open(original).size==(860,ch)
                assert (w,x,y)==(668,96,0)
                shutil.copy2(original,DEST/file)
        else:
            file=f'images/{n:02}-detail.jpg'
            # Locator screenshots round fractional CSS bounds outward, which can
            # include a thin strip from the next face row. Capture only pixels
            # inside this panel, aligned to the 2x device-pixel grid.
            rect=loc.bounding_box()
            top=math.ceil(rect['y']*2-1e-7)/2
            bottom=math.floor((rect['y']+rect['height'])*2+1e-7)/2
            p.screenshot(path=str(DEST/file),type='jpeg',quality=96,full_page=True,
                         clip={'x':rect['x'],'y':top,'width':rect['width'],'height':bottom-top})
            alt=loc.inner_text().strip().replace('\n',' ')+' '+ ' / '.join(loc.locator('img').evaluate_all('(es)=>es.map(e=>e.alt)'))
            kind='jpeg'
        im=Image.open(DEST/file)
        items.append(dict(file=file,width=im.width,height=im.height,kind=kind,alt=alt.strip(),bytes=(DEST/file).stat().st_size,sha256=sha(DEST/file),reference_region=loc.get_attribute('data-ref')))
    p.screenshot(path=str(SOURCE/'review-source-430.jpg'),type='jpeg',quality=90,full_page=True);b.close()
if (DEST/'manifest.json').exists():
    active={i['file'] for i in items}
    for previous in json.loads((DEST/'manifest.json').read_text(encoding='utf-8'))['files']:
        if previous['file'] not in active:
            obsolete=(DEST/previous['file']).resolve()
            assert obsolete.parent==(DEST/'images').resolve()
            obsolete.unlink(missing_ok=True)
info=(SOURCE/'product-information.html').read_text(encoding='utf-8');shutil.copy2(SOURCE/'product-information.html',DEST/'product-information.html')
tags=[]
for it in items:
    assert it['bytes']<4_900_000
    tags.append(f'<img src="{it["file"]}?v={it["sha256"][:10]}" width="{it["width"]}" height="{it["height"]}" alt="{html.escape(it["alt"],quote=True)}" style="display:block;width:100%;height:auto;border:0;margin:0;"'+(' loading="lazy"' if tags else '')+'>')
fragment='<div style="max-width:860px;width:100%;margin:0 auto;line-height:0;font-size:0;">\n'+'\n'.join(tags)+'\n'+info+'\n</div>'
(DEST/'detail.local.html').write_text(fragment,encoding='utf-8')
(DEST/'detail.cafe24.html').write_text(fragment.replace('src="images/','src="/web/upload/tam-detail-20261019/cloud-blush/'),encoding='utf-8')
(DEST/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>탐뷰티 클라우드 블러 · 카페24 등록 준비본 V10</title></head><body style="margin:0;background:#eeeded;">'+fragment+'</body></html>',encoding='utf-8')
m=dict(product='클라우드 블러',source='cloud-blush-v10/index.html',status='exported_candidate; owner acceptance pending; Cafe24 upload deferred',render='430 CSS px at 2x; static raster panels and two distinct source GIFs; native information',files=items,format_limit_bytes=4_900_000,product_information=dict(file='product-information.html',sha256=sha(DEST/'product-information.html'),font_size_css_px=12,cafe24_editor_save_verified=False),notes=['No custom JS, external fonts, MP4, animated WebP, iframe or buttons in delivery','Two source GIFs each play 3 cycles and stop; second GIF padded to reference inset; no creative colour grading','All six cheek assets are provided first revision, not generated; physical shade match unverified','Reference new colours and co-development omitted because TAM evidence unavailable','Product information and INCI text unchanged; native Korean font and table wrapping refined','Generated background is decorative; product cutout remains original'])
(DEST/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
(DEST/'README.txt').write_text(f'클라우드 블러 V10 · 카페24 등록 준비본\n\n이미지 {len(items)}개를 manifest.json 순서대로 사용합니다.\nMP4·외부 폰트·JS 없이 JPG/GIF와 네이티브 상품정보 HTML로 구성됩니다.\n이미지만 업로드하면 전성분이 빠집니다. detail.cafe24.html 전체를 사용합니다.\n실제 업로드·관리자 저장·실기기 재생 확인은 사용자가 미룬 적용 단계입니다.\n얼굴 발색은 제공 1차 자료이며 실물 색 검수 및 소유자 시각 승인은 미완료입니다.\n',encoding='utf-8')
with zipfile.ZipFile(SOURCE/'cloud-blush-cafe24.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(DEST.rglob('*')):
        if f.is_file():z.write(f,f.relative_to(DEST))
print(json.dumps(dict(panels=len(items),gifs=sum(i['kind']=='gif' for i in items),total_bytes=sum(i['bytes'] for i in items))))
