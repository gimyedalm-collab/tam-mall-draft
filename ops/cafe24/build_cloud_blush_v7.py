"""Assemble the frozen reference crosswalk; never uploads to Cafe24."""
from pathlib import Path
from PIL import Image, ImageOps
from bs4 import BeautifulSoup
import hashlib, json, shutil, subprocess

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cloud-blush-v7'; A=OUT/'assets'; A.mkdir(parents=True,exist_ok=True)
ARCHIVE=next((Path.home()/'Desktop').glob('_*디모멘텀'))
SRC=next(ARCHIVE.glob('*/08. 더 클라우드 블러 크림 블러셔'))
GENERATED=Path.home()/'.codex/generated_images/01a13e85-859c-7641-a346-0f91933fce82/exec-f7e8241f-75ea-4e99-88d2-015c1d4965df.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=[]
def record(src,dest,operation,**extra):
    ledger.append(dict(file=dest.relative_to(OUT).as_posix(),source=str(src),source_sha256=sha(src),sha256=sha(dest),operation=operation,**extra))
names=['백도 쉐이크','구아바 쉐이크','아사이베리 쉐이크','파파야 쉐이크','용과 쉐이크','살구 쉐이크']
tones=['부드러운 피치 핑크','차분한 로지 핑크','화사한 라벤더 핑크','따뜻한 코랄 오렌지','선명한 핑크','차분한 살구 베이지']
for i,name in enumerate(names,1):
    src=SRC/'외주 발색컷/1차/크림 블러셔'/f'{i:02} {name.replace(" ","")}.JPG'
    dest=A/f'cheek-{i}-r1.jpg'
    im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');im.thumbnail((1100,1200),Image.Resampling.LANCZOS);im.save(dest,quality=96,subsampling=0)
    record(src,dest,'EXIF orientation, proportional resize, JPEG encoding only; no colour/skin edits',revision='provided first revision',physical_colour_verified=False)
for i in range(1,7):
    src=SRC/'제형/누끼'/f'{i}호 누끼.png';dest=A/f'texture-{i}-original.png'
    im=Image.open(src).convert('RGBA');bbox=im.getchannel('A').getbbox();im=im.crop(bbox);im.thumbnail((600,600),Image.Resampling.LANCZOS);im.save(dest)
    record(src,dest,'Original transparent texture set, alpha bbox and proportional resize only; no recolouring',physical_colour_verified=False)
src=SRC/'누끼/01호 백도쉐이크1.png'; dest=A/'compact-original.png'
im=Image.open(src).convert('RGBA');bbox=im.getchannel('A').getbbox();im=im.crop(bbox);im.thumbnail((1300,1300),Image.Resampling.LANCZOS);im.save(dest)
record(src,dest,'Trim transparent padding to alpha bbox; proportional resize; no creative edits',crop_bbox=bbox)
shutil.copy2(GENERATED,A/'vegan-background.png');record(GENERATED,A/'vegan-background.png','GPT Image decorative background only; exact product cutout layered separately in HTML',not_product_evidence=True)

film=ROOT/'cloud-blush-v3/assets/cream-to-powder.mp4'
for name,start,end in [('texture-touch',.3,1.5),('howto-spread',3.1,5.1)]:
    dest=A/f'{name}.gif'
    if not dest.exists() or dest.stat().st_size>=4_900_000:
        width=688 if name=='howto-spread' else 860
        filt=f'trim=start={start}:end={end},setpts=PTS-STARTPTS,fps=12,scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(film),'-filter_complex',filt,'-loop','2',str(dest)],check=True)
    assert dest.stat().st_size<4_900_000
    record(film,dest,'Distinct source segment to 256-colour GIF; no exposure/colour grading',segment=[start,end],fps=12,loop_repeats=2)
for reused in [ROOT/'cloud-blush-v3/assets/ending.jpg',ROOT/'cloud-blush-v6/assets/formula-clear-oil-261019.jpg']+[ROOT/f'cloud-blush-v6/assets/arm-{i}.jpg' for i in range(1,7)]:
    ledger.append(dict(file=reused.relative_to(ROOT).as_posix(),source='Existing supplied/reviewed repository asset; see previous source provenance',sha256=sha(reused),operation='Unchanged reuse in HTML; no recolouring'))
(OUT/'asset-provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
V3='../cloud-blush-v3/assets/';V6='../cloud-blush-v6/assets/'
hero_file=A/'hero-preserved.jpg'
if not hero_file.exists():shutil.copy2(ROOT/'cafe24-delivery-20261019/cloud-blush/images/01-detail.jpg',hero_file)
hero='<section class="hero"><img src="assets/hero-preserved.jpg" width="860" height="1066" alt="더 클라우드 블러 크림 블러셔. 크림처럼 사르르, 파우더처럼 보송하게. 6 COLOURS · 2.8 g"></section>'
def heading(en,ko,body=''):
    return f'<header class="heading"><p class="eyebrow">{en}</p><h2>{ko}</h2>'+ (f'<p class="body">{body}</p>' if body else '')+'</header>'
wrists=''.join(f'<figure><img src="{V6}arm-{i}.jpg" alt="{i:02} {n} 제공 손목 발색"><figcaption><span>{i:02}</span> {n.replace(" 쉐이크","<br>쉐이크")}</figcaption></figure>' for i,n in enumerate(names,1))
textures=''.join(f'<figure><img src="assets/texture-{i}-original.png" alt="{i:02} {n} 제공 투명 누끼 원본 제형 색상"><figcaption>{i:02}</figcaption></figure>' for i,n in enumerate(names,1))
faces=''.join(f'<figure class="face-row export-panel" id="face-{i}" data-ref="04–06"><img src="assets/cheek-{i}-r1.jpg" alt="{i:02} {n} 얼굴 발색"><figcaption><p class="shade-number">{i:02}</p><h3>{n.replace(" 쉐이크","<br>쉐이크")}</h3><p class="tone">{t}</p></figcaption></figure>' for i,(n,t) in enumerate(zip(names,tones),1))
info=(ROOT/'cafe24-delivery-20261019/cloud-blush/product-information.html').read_text(encoding='utf-8')
shutil.copy2(ROOT/'cafe24-delivery-20261019/cloud-blush/product-information.html',OUT/'product-information.html')
body=f'''<article id="cloud-blush">
<div class="export-panel" data-ref="01">{hero}</div>
<section id="introduction" class="introduction export-panel" data-ref="01">{heading('THE CLOUD BLUR CREAM BLUSHER','더 클라우드 블러<br>크림 블러셔.','크림의 부드러운 발림,<br>파우더의 보송한 마무리.')}<img src="{V3}ending.jpg" alt="탐뷰티 여섯 가지 크림 블러셔 원본 제품 사진"></section>
<section id="palette" class="palette export-panel" data-ref="03">{heading('BLUSH COLOUR SHADES','여섯 가지 컬러를<br>한눈에.')}<div class="wrist-grid">{wrists}</div><div class="texture-grid">{textures}</div><p class="note">피부색·사용량·조명 및 화면 환경에 따라<br>발색이 다르게 보일 수 있습니다.</p></section>
<section id="faces" class="faces" data-ref="04–06"><div class="export-panel face-heading">{heading('COLOUR ON CHEEKS','볼 위에서 만나는<br>여섯 가지 컬러.')}</div>{faces}<p class="note export-panel face-note">피부색·사용량·조명 및 화면 환경에 따라<br>발색이 다르게 보일 수 있습니다.</p></section>
<section id="texture" class="texture" data-ref="07"><div class="export-panel texture-heading">{heading('CREAM TO POWDER','펴 바를 땐 부드럽게,<br>마무리는 보송하게.')}</div><img class="motion export-motion" src="assets/texture-touch.gif" alt="원본 영상의 크림 제형을 손가락으로 묻히는 장면"><div class="texture-pair export-panel"><div><span>CREAM</span><p>부드러운 발림</p></div><div><span>POWDER</span><p>보송한 마무리</p></div></div></section>
<section id="formula" class="formula export-panel" data-ref="09">{heading('FOUR BOTANICAL OILS','네 가지<br>식물성 오일 함유.')}<img class="oil-photo" src="{V6}formula-clear-oil-261019.jpg" alt="맑은 오일을 표현한 원료 연출 이미지"><div class="ingredients"><p>살구씨오일</p><p>동백나무씨오일</p><p>올리브오일</p><p>서양자두씨오일</p></div><p class="note">원료를 표현한 연출 이미지입니다.</p></section>
<section id="howto" class="howto" data-ref="10"><div class="howto-heading export-panel">{heading('HOW TO USE','소량으로 얇게,<br>경계는 톡톡.','손끝이나 도구로 얇게 펴 바른 뒤<br>경계를 가볍게 두드려 주세요.')}</div><img class="motion export-motion" src="assets/howto-spread.gif" alt="원본 영상의 손으로 크림 블러셔를 얇게 펴 바르는 장면"></section>
<section id="vegan" class="vegan export-panel" data-ref="11">{heading('VEGAN FORMULA','탐뷰티의<br>비건 포뮬러.')}<figure class="vegan-still"><img class="vegan-bg" src="assets/vegan-background.png" alt="밝은 식물 배경"><img class="vegan-product" src="assets/compact-original.png" alt="원본 탐뷰티 블러셔 제품 누끼"></figure></section>
<section id="check" class="check export-panel" data-ref="12"><p class="eyebrow">CHECK POINT</p><h2>개봉 후 12개월 이내<br>사용해 주세요.</h2><p class="body">개봉 전 사용 기한은 36개월입니다.</p><img class="logo" src="{V3}tam-logo.svg" alt="TAM BEAUTY"></section>
{info}</article>'''
(OUT/'detail.template.html').write_text(body,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM · Cloud Blush V7 조립 원본</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
print('V7 source assembled; first-revision face provenance and two distinct source GIF segments recorded.',flush=True)
