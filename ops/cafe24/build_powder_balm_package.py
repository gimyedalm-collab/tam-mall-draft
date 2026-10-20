"""Build Powder Balm only. Preserve supplied masters; rasterize Cafe24 panels.

python -X utf8 ops/cafe24/build_powder_balm_package.py --source PATH --facts PATH
All colour/exposure is inherited from provided originals. GIFs demonstrate
application, not a controlled before/after or duration study.
"""
import argparse, base64, hashlib, html, json, shutil, subprocess, tempfile, zipfile
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / 'powder-balm-v2'
OUT = ROOT / 'cafe24-delivery-20261020/powder-balm'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str,args)], check=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--facts',type=Path,required=True)
    args=parser.parse_args()
    assets=ROOT/'powder-balm-v1/assets'; assets.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    provenance=[]
    for key,rel,box in [
        ('open-puff','누끼/4.png',(2245,558,3683,3241)),
        ('open-balm','누끼/5.png',(1363,590,3726,3120)),
        ('balm-texture','제형/누끼/누끼_3.png',(65,39,940,903))]:
        src=args.source/rel; dest=assets/(key+'.png'); shutil.copy2(src,dest)
        w,h=Image.open(src).size; x,y,r,b=box
        encoded=base64.b64encode(src.read_bytes()).decode('ascii')
        (assets/(key+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{x} {y} {r-x} {b-y}"><image width="{w}" height="{h}" xlink:href="data:image/png;base64,{encoded}"/></svg>',encoding='utf-8')
        provenance.append({'asset':dest.relative_to(ROOT).as_posix(),'source_relative':rel,'sha256':digest(src),'treatment':'Original bytes; transparent-margin framing in SVG; no colour/exposure edits.'})
    still=next((args.source/'연출컷').glob('*２.jpg'))
    shutil.copy2(still,assets/'still-life.jpg')
    provenance.append({'asset':'powder-balm-v1/assets/still-life.jpg','source_relative':still.relative_to(args.source).as_posix(),'sha256':digest(still),'treatment':'Original bytes; square fit.'})
    hero=next((args.source/'연출컷').glob('*１.jpg'))
    hero_dest=DESIGN/'assets/hero-flatlay.jpg'; hero_dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(hero,hero_dest)
    provenance.append({'asset':hero_dest.relative_to(ROOT).as_posix(),'source_relative':hero.relative_to(args.source).as_posix(),'sha256':digest(hero),'treatment':'Original bytes; browser geometric crop only. No creative colour or exposure adjustment.'})
    clips={}
    for key,name,start,duration in [('forehead','이마 수정.mp4',.8,3),('nose','코 수정.mp4',.8,3),('cheek','나비존 수정.mp4',1.2,3)]:
        src=args.source/'외주/파우더 밤 수정'/name
        clips[key]={'path':src,'start':start,'duration':duration}
        run(['-ss',start,'-i',src,'-frames:v','1','-q:v','2',assets/(key+'.jpg')])
        provenance.append({'asset':f'powder-balm-v1/assets/{key}.jpg','source_relative':src.relative_to(args.source).as_posix(),'sha256':digest(src),'start_seconds':start,'duration_seconds':duration,'treatment':'Supplied product-specific application footage; trim, geometric fit, 12fps GIF palette conversion. No creative colour/exposure changes; no inferred upstream retouch or physical colour validation.'})
    (DESIGN/'source-manifest.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
    media=[]
    with tempfile.TemporaryDirectory(prefix='tam-powder-') as tmp:
        tmp=Path(tmp)
        with sync_playwright() as p:
            browser=p.chromium.launch()
            page=browser.new_page(viewport={'width':430,'height':900},device_scale_factor=2)
            page.goto((DESIGN/'layout.html').as_uri()); page.evaluate('document.fonts.ready')
            page.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
            for section in page.locator('section').all():
                name=section.get_attribute('id'); box=section.bounding_box()
                slots=section.locator('[data-video]').all()
                alt=' '.join(section.inner_text().split())
                if not slots:
                    dest=OUT/(name+'.jpg');section.screenshot(path=str(dest),type='jpeg',quality=95)
                else:
                    background=tmp/(name+'.png')
                    items=[]
                    for slot in slots:
                        r=slot.bounding_box(); key=slot.get_attribute('data-video')
                        items.append((key,round((r['x']-box['x'])*2),round((r['y']-box['y'])*2),round(r['width']*2),round(r['height']*2)))
                        slot.evaluate('(e)=>e.style.visibility="hidden"')
                    section.screenshot(path=str(background))
                    inputs=['-loop','1','-framerate','12','-i',background]
                    filters=[]; duration=max(clips[k]['duration'] for k,*_ in items)
                    for i,(key,x,y,w,h) in enumerate(items,1):
                        c=clips[key];inputs+=['-ss',c['start'],'-t',c['duration'],'-i',c['path']]
                        filters.append(f'[{i}:v]fps=12,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,setpts=PTS-STARTPTS[v{i}]')
                    base='0:v'
                    for i,(key,x,y,w,h) in enumerate(items,1):
                        filters.append(f'[{base}][v{i}]overlay={x}:{y}:shortest=1[b{i}]');base=f'b{i}'
                    filters += [f'[{base}]scale=688:-1:flags=lanczos,split[s0][s1]','[s0]palettegen=stats_mode=full:max_colors=256[pal]','[s1][pal]paletteuse=dither=sierra2_4a:diff_mode=rectangle[out]']
                    dest=OUT/(name+'.gif')
                    run([*inputs,'-filter_complex',';'.join(filters),'-map','[out]','-t',duration,'-loop','2',dest])
                    for slot in slots:slot.evaluate('(e)=>e.style.visibility="visible"')
                assert dest.stat().st_size < 4_900_000,(dest,dest.stat().st_size)
                with Image.open(dest) as im:
                    entry={'order':len(media)+1,'file':dest.name,'width':im.width,'height':im.height,'bytes':dest.stat().st_size,'sha256':digest(dest),'alt':alt}
                    if dest.suffix=='.gif':entry.update(frames=im.n_frames,loop=im.info.get('loop'),duration_ms=sum((im.seek(n) or im.info.get('duration',0)) for n in range(im.n_frames)))
                media.append(entry)
                print(dest.name,dest.stat().st_size,flush=True)
            browser.close()
    facts=args.facts.read_text(encoding='utf-8').strip()
    inci=facts.split('전성분 [ 탐 뷰티 더 클라우드 필터 파우더 밤]')[1].strip()
    fields=[('제품명','더 클라우드 필터 파우더 밤'),('용량 및 중량','3.5g I 0.12oz'),('제품 주요 사양','모든 피부'),('사용 기한','개봉 전 36개월 / 개봉 후 12개월'),('사용 방법','퍼프에 본품의 적당량을 취하여 유분기가 있는 부위에 가볍게 두드려 밀착시켜줍니다.'),('화장품책임판매업자','주식회사 에이위즈'),('제조국','한국'),('품질보증 기준','본 제품에 이상이 있을 경우, 공정거래 위원회 고시 소비자 분쟁 해결 기준에 따라 보상해 드립니다.'),('고객상담실','1668-0868 (수신자 요금부담)')]
    rows=''.join(f'<tr><th scope="row" style="width:96px;text-align:left;font-weight:500;padding:9px 10px 9px 0;border-bottom:1px solid #e5ecee;vertical-align:top">{html.escape(k)}</th><td style="padding:9px 0;border-bottom:1px solid #e5ecee;overflow-wrap:anywhere">{html.escape(v)}</td></tr>' for k,v in fields)
    info=f'<div data-tam-product-info="powder-balm" style="padding:30px 5%;background:#fff;color:#40545b;text-align:left;font-family:Arial,sans-serif;font-size:12px;line-height:1.6;box-sizing:border-box"><h2 style="font-size:16px;margin:0 0 16px">상품 정보 · 전성분</h2><table style="border-collapse:collapse;width:100%;table-layout:fixed;font-size:12px;line-height:1.6"><tbody>{rows}</tbody></table><h3 style="font-size:14px;margin:25px 0 8px">전성분</h3><p style="margin:0;overflow-wrap:anywhere">{html.escape(inci)}</p><h3 style="font-size:14px;margin:25px 0 8px">보관 안내</h3><p style="margin:0">고온에 장시간 노출될 경우 내용물 색상이 하늘색에서 연두색으로 변할 수 있습니다. 직사광선을 피해 서늘한 곳에 보관해주세요.</p></div>'
    (OUT/'product-information.html').write_text(info,encoding='utf-8')
    def fragment(prefix):
        tags=''.join(f'<img src="{prefix}{m["file"]}?v=2" width="{m["width"]}" height="{m["height"]}" alt="{html.escape(m["alt"],quote=True)}" style="display:block;width:100%;height:auto;border:0;margin:0"'+(' fetchpriority="high"' if m['order']==1 else '')+'>' for m in media)
        return f'<div style="max-width:860px;margin:0 auto;background:#fff">{tags}{info}</div>'
    local=fragment('')
    (OUT/'detail.local.html').write_text(local,encoding='utf-8')
    (OUT/'detail.cafe24.html').write_text(fragment('/web/upload/tam-detail-20261020/powder-balm/'),encoding='utf-8')
    (OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>탐뷰티 더 클라우드 필터 파우더 밤</title><meta name="robots" content="noindex"><style>body{margin:0;background:#eef3f4}img{max-width:100%}</style></head><body>'+local+'</body></html>',encoding='utf-8')
    manifest={'product_no':111,'product':'더 클라우드 필터 파우더 밤','date':'2026-10-20','version':2,'status':{'delivery_prepared':True,'preview_verified':False,'owner_visual_acceptance':'pending','cafe24_uploaded':False,'actual_device_verified':False},'delivery_prefix':'/web/upload/tam-detail-20261020/powder-balm/','hero_intent':'Benefit-led headline, literal use definition before 200 CSS px, large original product/puff/texture photograph, followed immediately by actual forehead/nose application.','media':media,'product_information_sha256':digest(OUT/'product-information.html'),'source_manifest':'../../powder-balm-v2/source-manifest.json','claims_note':'Oil-control/blur and three use cases reflect existing official product positioning, not new clinical substantiation. No 6h, ZERO, unqualified non-irritation, review counts, or unverified certification claim.','media_note':'Supplied product-specific footage. No Dasha archive imagery or unverified vertical V1–V3 footage. No AI-generated product or skin images. GIF colour quantization is unavoidable; no creative colour correction or claim of physically validated colour.','upload_note':'Owner deferred actual Cafe24 upload. Paths are planned, not live.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.txt').write_text('TAM 파우더 밤 · 카페24 등록 준비본 V2\n\n01~07 파일을 번호순으로 사용합니다. index.html은 동일 파일과 동일 상품정보의 미리보기입니다.\nGIF는 원본 속도, 12fps, 3회 재생 후 정지합니다. 모든 파일은 4.9MB 미만입니다.\n\n예정 업로드 경로: /web/upload/tam-detail-20261020/powder-balm/\n업로드 후 detail.cafe24.html을 상품 111 상세 영역에 사용합니다.\n실제 업로드/관리자 저장/실기기 검증은 소유자 요청으로 보류 상태입니다.\n제작 완료, 소유자 시안 승인, 실제 업로드는 별도 상태입니다.\n\n외부 폰트, 사용자 정의 JavaScript, 영상 호스팅은 업로드 패키지에 필요하지 않습니다.\n원본과 출처·도포 영상 구간은 powder-balm-v2/source-manifest.json에 기록했습니다.\n원본 색상에 새로운 보정을 하지 않았으며 상류 보정 여부나 실물 색 정확도를 보증하지 않습니다.\n',encoding='utf-8')
    pack=OUT.parent/'powder-balm-cafe24.zip'
    with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()):
            if f.is_file():z.write(f,f.name)
    print('PACKAGE',pack,pack.stat().st_size,flush=True)

if __name__=='__main__':main()
