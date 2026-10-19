"""Cafe24 image-only delivery from current approved source layouts.

No live-store writes. Local FFmpeg conversion; original media remains untouched.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from bs4 import BeautifulSoup
import hashlib, html, json, math, shutil, subprocess, tempfile, zipfile, sys
from registration_export_utils import prepare_cloud_info, panel_alt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cafe24-delivery-20261019'
WORK=Path(tempfile.gettempdir())/'tam-cafe24-media-20261019'
OUT.mkdir(exist_ok=True);WORK.mkdir(exist_ok=True)
LIMIT=4_900_000
GIFSICLE=next((Path.home()/'AppData/Local/npm-cache/_npx').glob('*/node_modules/gifsicle/vendor/gifsicle.exe'),None)
def run(args):
    p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode:raise RuntimeError(p.stderr[-3000:])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def savejson(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def decode_webp(src):
    dest=WORK/src.stem;dest.mkdir(exist_ok=True)
    im=Image.open(src);lines=[]
    for i in range(im.n_frames):
        im.seek(i);f=dest/f'{i:04}.png';im.convert('RGB').save(f)
        lines.extend([f"file '{f.as_posix()}'",f"duration {im.info.get('duration',42)/1000}"])
    (dest/'frames.txt').write_text('\n'.join(lines),encoding='utf-8')
    result=dest/'source.mkv'
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(dest/'frames.txt'),'-fps_mode','vfr','-c:v','ffv1',str(result)])
    return result

def gif(src,bg,rect,dest,fit='contain',cloud=False):
    original=src
    if src.suffix.lower()=='.webp':src=decode_webp(src)
    duration=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(src)]))['format']['duration'])
    # Cloud montage preserves all three original shots, shortening dwell only.
    segment='[1:v]trim=0.3:1.5,setpts=PTS-STARTPTS[a];[1:v]trim=3.1:5.1,setpts=PTS-STARTPTS[b];[1:v]trim=7.6:8.8,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[clip];' if cloud else ''
    if cloud:duration=4.4
    full=Image.open(bg).size
    for width,fps,dither in [(860,12,'sierra2_4a'),(688,12,'sierra2_4a'),(688,12,'bayer:bayer_scale=3'),(688,10,'bayer:bayer_scale=3'),(600,10,'bayer:bayer_scale=3'),(600,8,'bayer:bayer_scale=3')]:
        ratio=width/860;w=max(2,round(rect['width']*2*ratio));h=max(2,round(rect['height']*2*ratio));x=round(rect['x']*2*ratio);y=round(rect['offset']*2*ratio);height=round(full[1]*ratio)
        sizing=f'format=rgb24,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}' if fit=='cover' else f'format=rgb24,scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:white'
        filt=segment+f'[0:v]scale={width}:{height}[bg];'+('[clip]' if cloud else '[1:v]')+f'fps={fps},{sizing}[fg];[bg][fg]overlay={x}:{y}:shortest=1:format=rgb,fps={fps},split[p][q];[p]palettegen=max_colors=256:stats_mode=diff[pal];[q][pal]paletteuse=dither={dither}:diff_mode=rectangle[out]'
        run(['ffmpeg','-v','error','-y','-loop','1','-i',str(bg),'-i',str(src),'-filter_complex',filt,'-map','[out]','-t',str(duration),'-loop','2',str(dest)])
        if GIFSICLE:
            optimized=WORK/'optimized.gif'
            run([str(GIFSICLE),'-O3','--lossy=20',str(dest),'-o',str(optimized)])
            if optimized.stat().st_size<dest.stat().st_size:shutil.copy2(optimized,dest)
        if dest.stat().st_size<LIMIT:break
    if dest.stat().st_size>=LIMIT:raise RuntimeError(f'GIF too large: {dest}')
    im=Image.open(dest)
    return {'source':original.relative_to(ROOT).as_posix(),'source_sha256':sha(original),'width':im.width,'height':im.height,'frames':im.n_frames,'fps_target':fps,'dither':dither,'gifsicle_lossy':20 if GIFSICLE else None,'duration_seconds':duration,'loop_repeats':2,'conversion':'256-colour palette and GIF compression; no creative colour/exposure adjustment; original CSS framing','segments':[[.3,1.5],[3.1,5.1],[7.6,8.8]] if cloud else 'full source'}

CONFIG=[
 ('cloud-blush','클라우드 블러','cloud-blush-v6/index.html','#cloud-blush',[('video','cloud-blush-v3/assets/cream-to-powder.mp4')]),
 ('milky-cheek','밀키치크','cheek-v12/index.html','#milky-cheek-v12',[('video','storefront-v2/preview/assets/milky-cheek-v11/three-steps.mp4')]),
 ('highlighter','하이라이터','highlighter-r33/index.html','#beam-highlighter-r33',[('video:nth-of-type(1)','highlighter-r32/assets/real-glow.mp4'),('.h33-macro-image img','highlighter-r30/assets/tam-pearl-detail.webp'),('.h33-use video','highlighter-r32/assets/howto-four-looks-261012.mp4')]),
]

def finish(key,name,items,source):
    dest=OUT/key
    tags=[]
    for it in items:
        file=dest/it['file'];it.update(bytes=file.stat().st_size,sha256=sha(file))
        assert file.stat().st_size<LIMIT
        alt=html.escape(it.get('alt',name+' 상세 '+str(len(tags)+1)),quote=True)
        tags.append(f'<img src="{it["file"]}" width="{it["width"]}" height="{it["height"]}" alt="{alt}" style="display:block;width:100%;height:auto;border:0;margin:0;"'+(' loading="lazy"' if tags else '')+'>')
    fragment='<div style="max-width:860px;width:100%;margin:0 auto;line-height:0;font-size:0;">\n'+'\n'.join(tags)+'\n</div>'
    (dest/'detail.local.html').write_text(fragment,encoding='utf-8')
    (dest/'detail.cafe24.html').write_text(fragment.replace('src="images/','src="/web/upload/tam-detail-20261019/'+key+'/'),encoding='utf-8')
    (dest/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+name+' · 카페24 등록본</title></head><body style="margin:0;background:#eee;">'+fragment+'</body></html>',encoding='utf-8')
    render='existing860px source panels preserved; animated sources converted only' if key in ('lip-liner','lip-oil') else 'mobile-first 430 CSS pixels at2x; fixed860px static image canvas'
    savejson(dest/'manifest.json',{'product':name,'source':source,'status':'exported; Cafe24 upload and actual-device check pending','render':render,'files':items,'format_limit_bytes':LIMIT,'notes':['No custom JS, external font or animated WebP in default package','GIFs play3cycles then stop; original masters retained','Rasterized text is not selectable; alt text carries section content where available','Highlighter external-MP4 alternative requires verified hosting']})
    (dest/'README.txt').write_text(f'{name} — 카페24 등록 패키지\n\nimages 폴더 파일을 /web/upload/tam-detail-20261019/{key}/ 에 업로드한 뒤 detail.cafe24.html을 상세설명 HTML에 사용합니다.\nindex.html은 동일 파일로 구성한 검토본입니다. 실제 업로드/모바일 상품 저장/기기 검증은 미완료입니다.\n숫자 순서대로 파일을 직접 등록하는 방법도 가능합니다. 모든 파일은 4.9MB 미만입니다.\nGIF는 3회 재생 후 멈춥니다. 원본 색상 보정 없이 팔레트 변환했으나 GIF의 색상수 제한은 있습니다.\n',encoding='utf-8')
    if key=='lip-oil':
        manifest=json.loads((dest/'manifest.json').read_text(encoding='utf-8'))
        manifest['integration_scope']={'product_no':25,'component':'lip oils 01-03 only','safe_to_replace_entire_product_detail':False,'preserve_option':'00 Himalaya Pink lip gloss','requirements':['Preserve native product/option/stock/cart/review mappings','Keep 00 gloss description and its own ingredient/product information','Do not describe all four options as lip oils or apply oil ingredient copy to gloss','Compose the series guide and gloss/oil sections before full product25 replacement']}
        savejson(dest/'manifest.json',manifest)
        with (dest/'README.txt').open('a',encoding='utf-8') as note:
            note.write('\n적용 범위: 상품25 립 시리즈 중 립오일01~03 설명 구간입니다. 00 히말라야 핑크는 립글로스입니다. 이 패키지만으로 상품25 전체 상세를 덮어쓰지 마세요. 기존00 옵션·글로스 설명·전성분을 보존하고, 전체 시리즈 안내와 결합한 뒤 직접 적용·검수합니다.\n')
    with zipfile.ZipFile(OUT/f'{key}-cafe24.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(dest.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(dest))

with sync_playwright() as pw:
    b=pw.chromium.launch()
    for key,name,source,selector,motions in CONFIG:
        if len(sys.argv)>1 and key not in sys.argv[1:]:continue
        print('Building',key,flush=True)
        dest=OUT/key;(dest/'images').mkdir(parents=True,exist_ok=True)
        work=WORK/key;work.mkdir(exist_ok=True)
        p=b.new_page(viewport={'width':430,'height':1000},device_scale_factor=2,reduced_motion='reduce')
        p.goto((ROOT/source).as_uri(),wait_until='networkidle');p.evaluate('document.fonts.ready')
        p.locator('img').evaluate_all('(es)=>es.forEach(e=>e.loading="eager")')
        p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
        p.evaluate('''()=>{document.querySelectorAll('video').forEach(v=>v.pause());document.querySelectorAll('details').forEach(d=>d.open=true);document.querySelectorAll('button,.film-chapters,.film-actions,.film-caption,.h33-choice-link,.h33-motion-caption a').forEach(e=>e.remove());}''')
        p.add_style_tag(content='html{scroll-behavior:auto!important}body{margin:0!important}*{animation:none!important;transition:none!important}')
        if key=='cloud-blush':prepare_cloud_info(p)
        body=p.locator(selector);box=body.bounding_box();total=math.ceil(box['y']+box['height']);start=math.floor(box['y'])
        bounds={start,total};motion_rows=[]
        for i,(sel,src) in enumerate(motions):
            loc=p.locator(sel).first;rect=loc.bounding_box();top=math.floor(rect['y']);bottom=math.ceil(rect['y']+rect['height'])
            # Capture the complete row for the side-by-side pearl macro copy.
            if 'macro' in sel:
                row=p.locator('.h33-macro').bounding_box();top=math.floor(row['y']);bottom=math.ceil(row['y']+row['height'])
            fit=loc.evaluate('(e)=>getComputedStyle(e).objectFit')
            if fit not in ('cover','contain'):fit='contain'
            loc.evaluate('(e)=>e.style.visibility="hidden"')
            bg=work/f'background-{i}.png';p.screenshot(path=str(bg),full_page=True,clip={'x':0,'y':top,'width':430,'height':bottom-top})
            rect['offset']=rect['y']-top
            motion_rows.append({'top':top,'bottom':bottom,'rect':rect,'src':src,'bg':bg,'fit':fit,'alt':loc.get_attribute('aria-label') or loc.get_attribute('alt') or name+' 실제 사용'})
            bounds.update([top,bottom])
        for el in body.locator(':scope > section,:scope > footer,:scope > details').all():
            y=math.floor(el.bounding_box()['y'])
            if not any(m['top']<y<m['bottom'] for m in motion_rows):bounds.add(y)
        ordered=sorted(bounds);items=[]
        for top,bottom in zip(ordered,ordered[1:]):
            if bottom<=top:continue
            motion=next((m for m in motion_rows if m['top']==top and m['bottom']==bottom),None)
            number=len(items)+1
            if motion:
                file=f'images/{number:02}-motion.gif'
                meta=gif(ROOT/motion['src'],motion['bg'],motion['rect'],dest/file,motion['fit'],key=='cloud-blush')
                meta.update(file=file,alt=motion['alt'],kind='gif',layout={'x':motion['rect']['x'],'y':motion['rect']['offset'],'width':motion['rect']['width'],'height':motion['rect']['height'],'canvas_width':430,'canvas_height':bottom-top})
                items.append(meta)
            else:
                file=f'images/{number:02}-detail.jpg'
                p.screenshot(path=str(dest/file),type='jpeg',quality=95,full_page=True,clip={'x':0,'y':top,'width':430,'height':bottom-top})
                im=Image.open(dest/file)
                is_info=key=='cloud-blush' and top>=math.floor(p.locator('.product-info').bounding_box()['y'])
                text=panel_alt(p,top,bottom,is_info)
                items.append({'file':file,'width':im.width,'height':im.height,'kind':'jpeg','alt':text[:1800] or name+' 상세 이미지','source_y':[top,bottom]})
        finish(key,name,items,source)
        p.close()
    b.close()

# Preserve the concurrent, newest V9 lip-oil exports byte-for-byte.
if len(sys.argv)==1 or 'lip-oil' in sys.argv[1:]:
    dest=OUT/'lip-oil';(dest/'images').mkdir(parents=True,exist_ok=True)
    previous=dest/'manifest.json'
    if previous.exists():
        for item in json.loads(previous.read_text(encoding='utf-8'))['files']:
            old=(dest/item['file']).resolve()
            assert old.parent==(dest/'images').resolve()
            old.unlink(missing_ok=True)
    items=[]
    for i,src in enumerate(sorted((ROOT/'lipoil-v9/export').glob('*.png')),1):
        file='images/'+src.name;shutil.copy2(src,dest/file);im=Image.open(src)
        items.append({'file':file,'width':im.width,'height':im.height,'kind':'static','alt':'립오일 상세 '+str(i),'source':src.relative_to(ROOT).as_posix(),'source_sha256':sha(src)})
    finish('lip-oil','립오일',items,'lipoil-v9/export (existing approved-direction static panels, unchanged)')

# Lip liner uses the current integrated R34 files, never the older R32 standalone.
if len(sys.argv)>1 and 'lip-liner' not in sys.argv[1:]:sys.exit(0)
dest=OUT/'lip-liner';(dest/'images').mkdir(parents=True,exist_ok=True)
source=ROOT/'storefront-v2/preview/product-118.html'
soup=BeautifulSoup(source.read_text(encoding='utf-8'),'html.parser');items=[]
for i,tag in enumerate(soup.select('#product-detail .detail-images img'),1):
    src=(source.parent/tag['src']).resolve();im=Image.open(src);animated=getattr(im,'n_frames',1)>1
    if animated:
        bg=WORK/f'liner-bg-{i}.png';Image.new('RGB',im.size,'white').save(bg)
        file=f'images/{i:02}-motion.gif';rect={'x':0,'offset':0,'width':im.width/2,'height':im.height/2}
        meta=gif(src,bg,rect,dest/file)
    else:
        ext=src.suffix if src.suffix.lower() in ('.jpg','.jpeg','.png') else '.png';file=f'images/{i:02}-detail{ext}'
        if ext==src.suffix:shutil.copy2(src,dest/file)
        else:im.save(dest/file)
        if (dest/file).stat().st_size>=LIMIT:
            file=f'images/{i:02}-detail.jpg';im.convert('RGB').save(dest/file,quality=95,subsampling=0)
        meta={'width':im.width,'height':im.height,'source':src.relative_to(ROOT).as_posix(),'source_sha256':sha(src)}
    meta.update(file=file,kind='gif' if animated else 'static',alt=tag.get('alt','립라이너 상세'))
    items.append(meta)
finish('lip-liner','립라이너',items,'storefront-v2/preview/product-118.html #product-detail (R34)')
print('All five packages exported',flush=True)
