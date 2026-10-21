"""Cafe24 V4: actual application through finish, original product and hand demo.
Export-only Playwright renderer; user-browser inspection uses Browser skill.
python -X utf8 ops/cafe24/build_powder_balm_v4.py --source PATH
"""
import argparse, hashlib, html, json, shutil, subprocess, tempfile, zipfile
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
DESIGN=ROOT/'powder-balm-v4'
OUT=ROOT/'cafe24-delivery-20261020/powder-balm'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ff(args): subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def dump(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);args=ap.parse_args()
    assets=DESIGN/'assets';assets.mkdir(parents=True,exist_ok=True)
    old=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    facts=(OUT/'product-information.html').read_text(encoding='utf-8')
    provenance=[];media=[];clips={}
    with tempfile.TemporaryDirectory(prefix='tam-powder-v4-') as tmp:
        tmp=Path(tmp)
        for key,name,duration in [('cheek','나비존 수정.mp4',6.95),('forehead','이마 수정.mp4',5.5),('nose','코 수정.mp4',3.8)]:
            src=args.source/'외주/파우더 밤 수정'/name
            clips[key]={'path':src,'duration':duration,'hold':1.25}
            ff(['-i',src,'-frames:v','1','-q:v','2',assets/(key+'.jpg')])
            provenance.append({'key':key,'source_relative':src.relative_to(args.source).as_posix(),'sha256':sha(src),'start_seconds':0,'end_seconds':duration,'finish_hold_seconds':1.25,'treatment':'Continuous original-speed segment including unobstructed finish. Geometric fit only; no skin retouch, colour, exposure or separate before/after pairing.'})
        hand_src=args.source/'상세페이지/26년/국문/11.webp'
        # The hand rectangle excludes all original slogans, labels and person imagery.
        crop=(108,840,428,1150)
        with Image.open(hand_src) as im:
            durations=[]
            for n in range(im.n_frames):
                im.seek(n); frame=im.convert('RGB').crop(crop)
                frame.save(tmp/f'hand-{n:03d}.png');durations.append(im.info.get('duration',33))
                if n==0: frame.save(assets/'hand.jpg',quality=95)
            concat=tmp/'hand.ffconcat'
            concat.write_text('ffconcat version 1.0\n'+''.join(f"file 'hand-{n:03d}.png'\nduration {d/1000}\n" for n,d in enumerate(durations))+f"file 'hand-{len(durations)-1:03d}.png'\n",encoding='utf-8')
            hand_duration=sum(durations)/1000
        hand_mp4=tmp/'hand.mp4'
        ff(['-f','concat','-safe','0','-i',concat,'-vf','fps=12','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',hand_mp4])
        clips['hand']={'path':hand_mp4,'duration':hand_duration,'hold':.75}
        provenance.append({'key':'hand','source_relative':hand_src.relative_to(args.source).as_posix(),'sha256':sha(hand_src),'crop_xyxy':crop,'duration_seconds':hand_duration,'treatment':'All source animation frames; crop only the hand/amount-adjustment area. Original source is a finished detail graphic, not a new camera master. No colour editing; no face or original claims included.'})
        for key,rel in [('flatlay','연출컷/파우더밤１.jpg'),('ending','연출컷/파우더밤２.jpg'),('open-puff','누끼/4.png'),('open-balm','누끼/5.png'),('texture','제형/누끼/누끼_3.png')]:
            src=args.source/rel
            provenance.append({'key':key,'source_relative':rel,'sha256':sha(src),'treatment':'Reuse existing source asset; original colour and typography retained. Geometric framing only.'})
        with sync_playwright() as p:
            browser=p.chromium.launch();page=browser.new_page(viewport={'width':430,'height':900},device_scale_factor=2)
            page.goto((DESIGN/'layout.html').as_uri());page.evaluate('document.fonts.ready')
            page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
            for section in page.locator('section').all():
                name=section.get_attribute('id');box=section.bounding_box();slots=section.locator('[data-video]').all()
                alt=' '.join(section.inner_text().split())
                if not slots:
                    dest=OUT/(name+'.jpg');section.screenshot(path=str(dest),type='jpeg',quality=95)
                else:
                    bg=tmp/(name+'.png');items=[]
                    for slot in slots:
                        r=slot.bounding_box();key=slot.get_attribute('data-video');items.append((key,round((r['x']-box['x'])*2),round((r['y']-box['y'])*2),round(r['width']*2),round(r['height']*2)))
                        slot.evaluate('(e)=>e.style.visibility="hidden"')
                    section.screenshot(path=str(bg));duration=max(clips[k]['duration']+clips[k]['hold'] for k,*_ in items)
                    fps=8 if name=='01-hero' else 10
                    inputs=['-loop','1','-framerate',fps,'-i',bg];filters=[]
                    for i,(key,x,y,w,h) in enumerate(items,1):
                        c=clips[key];inputs+=['-t',c['duration'],'-i',c['path']]
                        filters.append(f'[{i}:v]fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={duration-c["duration"]+.1}[v{i}]')
                    base='0:v'
                    for i,(key,x,y,w,h) in enumerate(items,1):
                        filters.append(f'[{base}][v{i}]overlay={x}:{y}:shortest=1[b{i}]');base=f'b{i}'
                    dest=OUT/(name+'.gif')
                    for export_width in ([516,480] if name=='01-hero' else [640,600,560,516,480]):
                        graph=filters+[f'[{base}]scale={export_width}:-1:flags=lanczos,split[s0][s1]','[s0]palettegen=stats_mode=full:max_colors=256[pal]','[s1][pal]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle[out]']
                        ff([*inputs,'-filter_complex',';'.join(graph),'-map','[out]','-t',duration,'-loop','2',dest])
                        if dest.stat().st_size<4_900_000: break
                    for slot in slots:slot.evaluate('(e)=>e.style.visibility="visible"')
                assert dest.stat().st_size<4_900_000,(name,dest.stat().st_size)
                with Image.open(dest) as im:
                    entry={'order':len(media)+1,'file':dest.name,'width':im.width,'height':im.height,'bytes':dest.stat().st_size,'sha256':sha(dest),'alt':alt}
                    if dest.suffix=='.gif':entry.update(frames=im.n_frames,loop=im.info['loop'],duration_ms=sum((im.seek(n) or im.info.get('duration',0)) for n in range(im.n_frames)))
                media.append(entry);print(dest.name,dest.stat().st_size,flush=True)
            clipping=page.evaluate('''()=>[...document.querySelectorAll('section')].flatMap(s=>[...s.querySelectorAll('h1,h2,h3,p,img')].filter(e=>{let a=s.getBoundingClientRect(),b=e.getBoundingClientRect();return b.bottom>a.bottom+1||b.right>a.right+1||b.left<a.left-1}).map(e=>({section:s.id,text:e.innerText||e.alt})))''')
            assert not clipping,clipping
            browser.close()
    dump(DESIGN/'source-manifest.json',provenance)
    current={m['file'] for m in media}
    # Remove only obsolete generated media enumerated in the previous manifest.
    for m in old['media']:
        f=(OUT/m['file']).resolve()
        assert f.parent==OUT.resolve()
        if f.name not in current and f.exists():f.unlink()
    def fragment(prefix):
        tags=''.join(f'<img src="{prefix}{m["file"]}?v=4" width="{m["width"]}" height="{m["height"]}" alt="{html.escape(m["alt"],quote=True)}" style="display:block;width:100%;height:auto;border:0;margin:0"'+(' fetchpriority="high"' if m['order']==1 else '')+'>' for m in media)
        return '<div style="max-width:860px;margin:0 auto;background:#fff">'+tags+facts+'</div>'
    prefix='/web/upload/tam-detail-20261020/powder-balm/'
    (OUT/'detail.local.html').write_text(fragment(''),encoding='utf-8');(OUT/'detail.cafe24.html').write_text(fragment(prefix),encoding='utf-8')
    (OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>탐뷰티 더 클라우드 필터 파우더 밤</title><meta name="robots" content="noindex"><style>body{margin:0;background:#eef3f4}img{max-width:100%}</style></head><body>'+fragment('')+'</body></html>',encoding='utf-8')
    manifest={'product_no':111,'product':'더 클라우드 필터 파우더 밤','date':'2026-10-21','version':4,'status':{'delivery_prepared':True,'preview_verified':False,'owner_visual_acceptance':'pending','cafe24_uploaded':False,'actual_device_verified':False},'delivery_prefix':prefix,'media':media,'product_information_sha256':sha(OUT/'product-information.html'),'source_manifest':'../../powder-balm-v4/source-manifest.json','claims_note':'Existing official intended use, cosmetic oil-control/blur, puff shape and hand amount adjustment. No selective oil-only removal, intact foundation guarantee, controlled before/after or comparative superiority. Competitor claims and images not reused.','media_note':'Original-speed application through unobstructed finish, held 1.25s; three cycles then stays on finish. Hand crop from supplied existing detail. No Dasha imagery, new AI, 3D or colour/exposure changes. GIF quantization not physical colour validation.','upload_note':'Actual Cafe24 upload deferred by owner.'}
    dump(OUT/'manifest.json',manifest)
    (OUT/'README.txt').write_text('TAM 파우더 밤 · 카페24 등록 준비본 V4\n\n01~07 파일을 번호순으로 사용합니다. JPG 4개 + GIF 3개.\nindex.html은 같은 파일·순서·상품정보를 보여주는 미리보기입니다.\nGIF는 원본 속도, 첫 영상 8fps / 나머지 10fps, 3회 반복 후 마지막 화면에 정지합니다.\n얼굴 도포 영상은 퍼프를 뗀 마무리 장면까지 포함합니다.\n모든 파일은 4.9MB 미만입니다.\n\n예정 경로: '+prefix+'\n실제 Cafe24 업로드·관리자 저장·실기기 검증은 보류 상태입니다.\n제작 완료, 소유자 시각 승인, 실제 업로드는 별도 상태입니다.\n외부 폰트·JavaScript·영상 호스팅이 필요하지 않습니다.\n원본 기록: powder-balm-v4/source-manifest.json\n',encoding='utf-8')
    pack=OUT.parent/'powder-balm-cafe24.zip'
    with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()):
            if f.is_file():z.write(f,f.name)
    print('PACKAGE',pack.stat().st_size,flush=True)
if __name__=='__main__':main()
