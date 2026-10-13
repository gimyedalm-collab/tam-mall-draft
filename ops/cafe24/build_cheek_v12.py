"""Build the art-directed Milky Cheek revision against TAM's lipliner reference."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORK = Path('C:/Users/BNK-1/Desktop/_탐뷰티')
SOURCE = WORK / 'PROSTER_젤리라인_SNS소스_260916/05_Product_Cuts/06_Milky_Cheek_Blush/source'
V8 = WORK / '물풀치크_상세_V8_261002/assets'
DEST = ROOT / 'storefront-v2/preview/assets/milky-cheek-v12'
DEST.mkdir(parents=True, exist_ok=True)
records = []
for src, name in [(SOURCE/'1차_070.jpg', 'campaign.jpg'), (SOURCE/'1차_077.jpg', 'sponge.jpg')]:
    out = DEST/name
    if not out.exists():
        subprocess.run(['ffmpeg','-v','error','-i',str(src),'-vf','scale=1720:-2','-q:v','2','-frames:v','1',str(out)], check=True)
    records.append({'file':name,'source_name':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'transformation':'Web resize/JPEG encoding only. No retouch, recolour or generation; full source frame retained.'})
for src, name in [(V8/f'web/swatch{i:02}.jpg',f'swatch{i:02}.jpg') for i in range(1,5)]:
    shutil.copy2(src,DEST/name)
    records.append({'file':name,'source_name':src.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'transformation':'Byte-for-byte reuse of existing brand asset.'})
records.append({'file':'formula-milky-ribbon.webp','source_name':'Dedicated Milky Cheek conceptual illustration','sha256':hashlib.sha256((DEST/'formula-milky-ribbon.webp').read_bytes()).hexdigest(),'transformation':'Built-in imagegen illustration; web encoding only. Not a product, shade or efficacy photograph. Prompt and provenance: ops/cafe24/cheek-formula-image.json'})
cutout=SOURCE.parent/'cutout_png/누끼.png'
out=DEST/'ending-product.webp'
if not out.exists():
    subprocess.run(['ffmpeg','-v','error','-i',str(cutout),'-c:v','libwebp','-lossless','1','-compression_level','6',str(out)],check=True)
records.append({'file':out.name,'source_name':str(cutout.relative_to(SOURCE.parent)),'source_sha256':hashlib.sha256(cutout.read_bytes()).hexdigest(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'transformation':'Existing brand transparent product cutout. Lossless WebP export, no recolouring, retouch or generation. CSS composition on white.'})
finish=SOURCE/'14.jpg'
out=DEST/'finish-look.webp'
records.append({'file':out.name,'source_name':'05_Product_Cuts/06_Milky_Cheek_Blush/source/14.jpg','source_sha256':hashlib.sha256(finish.read_bytes()).hexdigest(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'transformation':'Restored original brand campaign photograph after owner rejected generated model. Web resize and encoding only; no AI, face edits, skin retouch or colour grading. Proportional CSS crop.'})
for row in records:
    with Image.open(DEST/row['file']) as im: row['dimensions']=list(im.size)
    row['bytes']=(DEST/row['file']).stat().st_size

def content(prefix):
    a=prefix+'milky-cheek-v12/'
    old=prefix+'milky-cheek-v11/'
    shades=[('헬로버니','HELLO BUNNY','밀키 핑크','흰빛이 감도는 밝은 핑크.'),('썬플러쉬','SUN FLUSH','코랄 핑크','코랄빛을 더한 따뜻한 핑크.'),('누드티','NUDE TEA','핑크 베이지','핑크를 머금은 부드러운 베이지.'),('로지댄스','ROSY DANCE','모브 핑크','장밋빛이 감도는 차분한 모브.')]
    colourcards=''.join(f'''<figure class="c12-shade">
      <div class="c12-cheek"><img src="{old}cheek{i:02}.jpg" width="2992" height="3740" loading="lazy" alt="{name} 실제 볼 발색"></div>
      <img class="c12-swatch" src="{a}swatch{i:02}.jpg" loading="lazy" alt="{name} 실제 제형 색상 확대">
      <figcaption><div><h3><span>{i:02}</span> {name}</h3><p class="c12-shade-en">{en}</p><p class="c12-tone">{tone}</p></div></figcaption>
      <p class="c12-shade-description">{description}</p>
    </figure>''' for i,(name,en,tone,description) in enumerate(shades,1))
    return f'''<article id="milky-cheek-v12" aria-label="더 젤리 밀키 치크 블러셔 상세" data-detail-release="cheek-v12">
  <section class="c12-hero" data-panel="hero">
    <div class="c12-hero-copy">
      <img class="c12-logo" src="{old}tam-logo.svg" width="156" height="44" alt="TAM BEAUTY">
      <p class="c12-product-name">더 젤리 밀키 치크 블러셔</p>
      <h2>밀키한 생기,<br>은은한 젤리광.</h2>
      <p class="c12-body">스펀지로 가볍게 톡톡.</p>
      <p class="c12-accent">원하는 만큼 물들이는 비건 치크.</p>
    </div>
    <div class="c12-campaign"><img src="{a}campaign.jpg" width="1720" height="2580" fetchpriority="high" alt="네 가지 물풀치크 제품과 밀키한 제형의 원본 촬영 컷"></div>
    <div class="c12-hero-points"><p><b>밀키 컬러</b><span>부드럽게 물드는 생기</span></p><p><b>스펀지 팁</b><span>용기 하나로 간편하게</span></p><p><b>비건 포뮬러</b><span>네 가지 컬러 모두</span></p></div>
  </section>

  <section class="c12-application c12-section" data-panel="application">
    <header class="c12-heading"><span class="c12-label">SPONGE APPLICATOR</span><h2>브러시 없이<br>볼 위에 바로 톡톡.</h2></header>
    <div class="c12-application-media">
      <figure class="c12-sponge-figure"><div class="c12-sponge"><img src="{a}sponge.jpg" width="1720" height="2580" loading="lazy" alt="물풀치크 내장 스펀지와 ON 표시 확대"><span class="c12-mechanism">ON / OFF</span></div><figcaption>바르고 펴 바르는 스펀지 팁<br><span>돌려서 여닫는 ON/OFF 조절부</span></figcaption></figure>
      <figure class="c12-film-figure"><div class="c12-film"><video muted loop playsinline preload="none" controls poster="{old}three-steps-poster.png" aria-label="물풀치크 실제 사용 영상"><source src="{old}three-steps.mp4" type="video/mp4"></video></div><figcaption class="c12-film-caption"><span>볼 위에 가볍게 두드리기</span><button class="c12-play" type="button" aria-label="사용법 영상 재생" aria-pressed="false" hidden>재생</button></figcaption></figure>
    </div>
    <ol class="c12-steps"><li><span>01</span><h3>ON으로 열기</h3><p>팁에 소량 짜 주세요.</p></li><li><span>02</span><h3>톡톡 펴 바르기</h3><p>볼 위에서 두드려 주세요.</p></li><li><span>03</span><h3>OFF로 닫기</h3><p>사용 후 캡을 닫아 주세요.</p></li></ol>
    <p class="c12-use-tip">처음에는 소량, 원하는 색감만큼 덧발라 주세요.</p>
  </section>

  <section class="c12-colours c12-section" data-panel="colours">
    <header class="c12-heading"><span class="c12-label">FIND YOUR SHADE</span><h2>나의 볼에 어울리는<br>네 가지 밀키 컬러.</h2><p class="c12-body">볼 위의 발색과 제형을 함께 비교해 보세요.</p></header>
    <div class="c12-shade-grid">{colourcards}</div>
    <p class="c12-note">피부 톤과 사용량, 조명 및 화면 환경에 따라 발색이 다르게 보일 수 있습니다.</p>
  </section>

  <section class="c12-finish" data-panel="finish" aria-label="메이크업 무드">
    <div class="c12-finish-photo"><img src="{a}finish-look.webp" width="1720" height="2580" loading="lazy" alt="물풀치크를 든 모델의 핑크빛 볼 메이크업 브랜드 촬영 컷"></div>
    <div class="c12-finish-signoff"><img src="{old}tam-logo.svg" width="1080" height="500" loading="lazy" alt="TAM BEAUTY"></div>
  </section>

  <section class="c12-texture" data-panel="texture">
    <header class="c12-heading"><span class="c12-label">MILKY TEXTURE</span><h2>부드럽게 펴 바르는<br>밀키한 텍스처.</h2></header>
    <img class="c12-texture-photo" src="{old}formula-pink.jpg" width="1800" height="1200" loading="lazy" alt="헬로버니의 밀키한 제형과 스펀지 팁 실제 촬영 컷">
  </section>

  <section class="c12-formula c12-section" data-panel="formula">
    <header class="c12-heading"><span class="c12-label">VEGAN FORMULA</span><p class="c12-kicker">밀키한 컬러 속에 담은</p><h2>스킨케어 성분.</h2><p class="c12-body">히알루론산 계열부터 세라마이드NP까지.<br>네 가지 컬러에 공통으로 담았어요.</p></header>
    <img class="c12-formula-art" src="{a}formula-milky-ribbon.webp" width="1536" height="1024" loading="lazy" alt="밀키한 핑크 젤이 부드럽게 흐르는 포뮬러 연출 이미지">
    <div class="c12-ingredients">
      <div class="c12-ingredient"><span class="c12-ingredient-number">01</span><h3>히알루론산 계열</h3><p class="c12-ingredient-note">소듐하이알루로네이트<br>하이알루로닉애씨드</p></div>
      <div class="c12-ingredient"><span class="c12-ingredient-number">02</span><h3>스쿠알란</h3><p class="c12-ingredient-note">피부를 부드럽게 하는<br>스쿠알란*</p></div>
      <div class="c12-ingredient"><span class="c12-ingredient-number">03</span><h3>판테놀·알란토인</h3><p class="c12-ingredient-note">피부 컨디셔닝 성분,<br>판테놀*</p></div>
      <div class="c12-ingredient"><span class="c12-ingredient-number">04</span><h3>세라마이드NP</h3><p class="c12-ingredient-note">전성분명:<br>세라마이드엔피</p></div>
    </div>
    <p class="c12-note">*원료적 특성에 한함.<br>위 이미지는 포뮬러를 표현한 연출 이미지입니다.</p>
  </section>

  <section class="c12-test c12-section" data-panel="test">
    <header class="c12-heading"><span class="c12-label">SKIN TEST</span><h2>피부 일차 자극<br>시험 완료.</h2></header>
    <div class="c12-test-value"><strong>0.00</strong><p>4가지 컬러 각각<br>평균 피부반응도</p></div>
    <p class="c12-note">한국피부과학연구원 · 성인 여성 32명<br>측정기간 2024.11.25 ~ 2024.11.28<br>24시간 첩포 후 제거 30분·24시간·48시간 평가<br>시험 조건에 따른 결과이며 개인차가 있습니다.</p>
  </section>

  <footer class="c12-ending" data-panel="ending"><div class="c12-ending-visual"><div class="c12-ending-product"><img src="{a}ending-product.webp" width="1920" height="3465" loading="lazy" alt="TAM 로고가 보이는 물풀치크 제품 앞면"></div><div class="c12-ending-swatches" aria-hidden="true">{''.join(f'<img src="{a}swatch{i:02}.jpg" width="840" height="840" loading="lazy" alt="">' for i in range(1,5))}</div></div><div class="c12-ending-copy"><p>밀키하게 물드는 나의 컬러.</p><img class="c12-logo" src="{old}tam-logo.svg" width="156" height="44" alt="TAM BEAUTY"></div></footer>
</article>'''

standalone=ROOT/'cheek-v12';standalone.mkdir(exist_ok=True)
css_revision=hashlib.sha256((DEST/'detail.css').read_text(encoding='utf-8').encode('utf-8')).hexdigest()[:12]
def version_detail_css(html):
    return re.sub(r'milky-cheek-v(?:11|12)/detail\.css(?:\?[^"\s]*)?',f'milky-cheek-v12/detail.css?v={css_revision}',html)
def normalize_detail_assets(html):
    return re.sub(r'milky-cheek-v(?:11|12)/detail\.css(?:\?[^"\s]*)?','DETAIL_CSS',html).replace('milky-cheek-v11/detail.js','DETAIL_JS').replace('milky-cheek-v12/detail.js','DETAIL_JS')
head='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>탐뷰티 | 더 젤리 밀키 치크 블러셔</title><link rel="stylesheet" href="../storefront-v2/preview/assets/milky-cheek-v12/detail.css"><script defer src="../storefront-v2/preview/assets/milky-cheek-v12/detail.js"></script><style>body{margin:0;background:#eee}main{max-width:860px;margin:auto}</style></head><body><main>'''
(standalone/'index.html').write_text(version_detail_css(head)+content('../storefront-v2/preview/assets/')+'</main></body></html>\n',encoding='utf-8')

page=ROOT/'storefront-v2/preview/product-102.html';before=page.read_text(encoding='utf-8')
pattern=r'<!-- cheek-v(?:11|12):start -->.*?<!-- cheek-v(?:11|12):end -->'
old=re.search(pattern,before,re.S);assert old
replacement='<!-- cheek-v12:start --><section class="detail-source container cushion-final-detail" id="product-detail" aria-label="물풀치크 제품 상세">'+content('assets/')+'<a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section><!-- cheek-v12:end -->'
after=re.sub(pattern,lambda _:replacement,before,count=1,flags=re.S)
oldincludes='<link rel="stylesheet" href="assets/milky-cheek-v11/detail.css"><script src="assets/milky-cheek-v11/detail.js" defer></script>'
newincludes=oldincludes.replace('milky-cheek-v11','milky-cheek-v12')
after=after.replace(oldincludes,newincludes)
after=version_detail_css(after)
assert normalize_detail_assets(after.replace(replacement,old[0]))==normalize_detail_assets(before)
page.write_text(after,encoding='utf-8',newline='\n')

report={'version':'V12','product_no':102,'date':'2026-10-13','status':'design_in_progress','design_reference':'TAM lipliner R32/R34 typography and photography scale. Dedicated Milky Cheek ingredient art replaces reused lipliner droplets after owner feedback.','direction':{'palette':['#1A1A1A','#6F6A6B','#925368','#F3E8EC','#F5F5F5','#FFFFFF'],'type':'Pretendard 400/600/700 for Korean, Manrope for section labels and numerals','sequence':['Product campaign','Sponge and one approved usage video','Original cheek and texture shade comparison','Real milky texture','Ingredient illustration','Existing test evidence','Product lineup'],'preserved_constraints':['No AI face','No Dasha/legacy person video','Only approved Choi Yeeun 3steps clip','No recolouring swatches','No invented efficacy or before/after'],'claude_review':'Read-only nonpersistent consultation. Accepted hierarchy and compact comparison advice; rejected inaccurate compact/mirror/solid-balm product suggestions.'},'sources':records,'commerce_outside_detail_unchanged':True,'production_cafe24_changed':False}
report['direction']['sequence'].insert(3,'Image-only original brand makeup photograph')
report['direction']['preserved_constraints'][0]='Owner rejected AI model mood image; restore existing brand photograph for this section. Do not reuse rejected AI portrait.'
report_path=ROOT/'ops/cafe24/cheek-detail-v12.json'
previous=json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {}
for key in ('verification','publication'):
    previous.pop(key,None)
previous.update(report)
report_path.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('V12 built: new campaign, sponge/usage, comparative shades, texture/formula and proof.')
