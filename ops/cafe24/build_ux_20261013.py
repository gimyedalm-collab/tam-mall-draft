"""Apply approved audit changes to GitHub preview, preserving native migration boundary."""
from pathlib import Path
from bs4 import BeautifulSoup
import re,json,shutil
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'storefront-v2/preview';A=P/'assets/ux-261013';A.mkdir(exist_ok=True)
if 'ux-261013.css' in (P/'design-only.html').read_text(encoding='utf-8'):
 raise SystemExit('One-time migration already applied; edit current assets directly.')
catalog=json.loads((P/'assets/preview-catalog.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
products={p['id']:p for p in catalog}
nav='''<header class="ux-header{home_class}">
<button class="ux-menu-toggle" type="button" aria-controls="ux-navigation" aria-expanded="false">메뉴</button>
<nav class="ux-links" id="ux-navigation" aria-label="주요 메뉴"><a href="shop.html">제품</a><a href="lookbook.html">룩북</a><a href="about.html">브랜드</a><a class="ux-mobile-only" href="jelly.html">The Jelly · 글로우</a><a class="ux-mobile-only" href="cloud.html">The Cloud · 블러</a><a class="ux-mobile-only" href="login.html">로그인</a><a class="ux-mobile-only" href="https://tambeauty.kr/myshop/order/list.html">주문조회</a><a class="ux-mobile-only" href="https://pf.kakao.com/_nxhIxhn" target="_blank" rel="noopener">고객문의</a></nav>
<a class="ux-logo" href="index.html" aria-label="탐뷰티 홈"><img src="assets/38d19c7e8e86.png" alt="tam BEAUTY" width="720" height="330"></a>
<nav class="ux-utilities" aria-label="쇼핑 메뉴"><a href="search.html">검색</a><a class="ux-account" href="login.html">로그인</a><a href="basket.html">장바구니</a></nav></header>'''
footer='''<footer class="ux-footer"><div class="ux-footer-grid">
<div class="ux-footer-company"><img src="assets/38d19c7e8e86.png" alt="tam BEAUTY" width="720" height="330" loading="lazy"><p>주식회사 에이위즈 · 대표 김영훈<br>서울 강남구 봉은사로22길 18 지하1층(역삼동)<br>사업자등록번호 228-88-02579 · 통신판매업신고 제 2024-서울강남-02503 호<br>개인정보보호책임자 김영훈 · tambeautyofficial@gmail.com</p></div>
<div><h2>고객센터</h2><p><a href="tel:1668-0868">1668-0868</a><br>평일 10:00 – 17:00 · 주말 · 공휴일 휴무</p><div class="ux-footer-links"><a href="https://pf.kakao.com/_nxhIxhn" target="_blank" rel="noopener">카카오톡 문의 ↗</a><a href="https://tambeauty.kr/myshop/order/list.html">주문조회 ↗</a></div></div>
<div><h2>입금 계좌</h2><p>우리은행 1005-804-651153<br>예금주 (주)에이위즈<br>입금 시 주문자 성함 기재</p><a href="https://tambeauty.kr/shopinfo/guide.html">배송·교환·반품 안내 ↗</a></div></div>
<div class="ux-footer-bottom"><div class="ux-footer-links"><a href="about.html">브랜드 소개</a><a href="https://tambeauty.kr/member/privacy.html">개인정보처리방침</a><a href="https://tambeauty.kr/member/agreement.html">이용약관</a><a href="https://tambeauty.kr/shopinfo/guide.html">이용안내</a></div><p>© TAM BEAUTY. All rights reserved.</p></div></footer>'''
changed=[]
for path in sorted(P.glob('*.html')):
 if path.name.startswith(('design-before','video-review','design-retouch')):continue
 text=path.read_text(encoding='utf-8')
 if not re.search(r'<header[^>]+class="(?:brand-header|do-header)"',text):continue
 home=path.name=='design-only.html'
 text=re.sub(r'<header[^>]+class="(?:brand-header|do-header)"[^>]*>.*?</header>',nav.format(home_class=' do-header' if home else ''),text,count=1,flags=re.S)
 text=re.sub(r'<nav[^>]+class="mobile-nav"[^>]*>.*?</nav>','',text,flags=re.S)
 text=re.sub(r'<footer\b[^>]*class="(?:ft|do-foot)"[^>]*>.*?</footer>',footer,text,count=1,flags=re.S)
 text=text.replace('</head>','<link rel="stylesheet" href="assets/ux-261013.css?v=1"><script defer src="assets/ux-261013.js?v=1"></script></head>')
 text=text.replace('assets/purchase-experience.js?v=review1','assets/purchase-experience.js?v=ux1')
 text=text.replace('<main>','<main id="main">',1)
 if home:
  text=text.replace('<main id="main">','<a class="ux-skip" href="#main">본문 바로가기</a><main id="main">',1)
  text=text.replace('<div class="do-hero-copy">','<button type="button" class="film-toggle" aria-label="브랜드 영상 일시정지" aria-pressed="false">영상 멈춤</button><div class="do-hero-copy">',1)
  s=BeautifulSoup(text,'html.parser')
  s.select_one('.do-edit h2').string='탐뷰티 대표 제품'
  s.select_one('.do-edit-copy p').clear();s.select_one('.do-edit-copy p').append('피부의 윤기부터 부드러운 립 컬러까지.')
  for a in s.select('.do-product'):
   pid=int(re.search(r'product-(\d+)',a['href'])[1]);product=products[pid]
   cap=a.find('figcaption');detail=cap.select_one('.product-detail').get_text();category=cap.small.get_text()
   cap.clear();cap.append(BeautifulSoup(f'<small>{category}</small><span class="ux-product-name">{product["name"]}</span><span class="product-detail">{detail}</span><span class="ux-product-price">{product["price"]:,}원</span>','html.parser'))
  s.select_one('.brand-note').decompose()
  s.select_one('.do-intro p').string='윤기 있는 Jelly, 보송한 Cloud. 원하는 마무리감으로 골라보세요.'
  for fig,pids in zip(s.select('.do-look-grid figure'),[(18,102),(112,111)]):
   links=''.join(f'<a href="product-{pid}.html">{products[pid]["name"].replace("[물풀치크]","")} ↗</a>' for pid in pids)
   fig.append(BeautifulSoup(f'<figcaption class="ux-look-products"><p>이 무드와 어울리는 제품</p>{links}</figcaption>','html.parser'))
  text=str(s)
 # Every product keeps its original gallery/content; only navigation wrappers change.
 if re.fullmatch(r'product-\d+\.html',path.name):
  s=BeautifulSoup(text,'html.parser');options=s.select_one('[data-preview-product]');detail=s.select_one('.detail-source');review=s.select_one('#review')
  if options:options['id']='purchase-options'
  if detail:
   detail['id']='product-detail'
   if detail.name=='details':detail['open']=''
   detail.insert_before(BeautifulSoup('<nav class="ux-detail-nav container" aria-label="제품 상세 바로가기"><a href="#purchase-options">색상 선택</a><a href="#product-detail">제품 상세·사용법</a><a href="#review">구매 후기</a><a href="https://tambeauty.kr/shopinfo/guide.html">배송·교환 안내 ↗</a></nav>','html.parser'))
  # Shorten display labels only. Original option values remain unchanged for cart mapping.
  if options:
   for opt in options.select('option[value]'):
    full=opt.get_text(' ',strip=True)
    if opt.get('value') and re.search(r'\d{2}\.\s*',full):
     match=re.search(r'(\d{2}\.\s*[가-힣]+(?:\s[가-힣]+)?)',full)
     if match:opt['data-description']=full;opt.string=match[1]
  text=str(s)
 if path.name=='lookbook.html':
  s=BeautifulSoup(text,'html.parser')
  for chapter,pids in zip(s.select('.lookbook-chapter'),[(18,102),(112,111)]):
   links=''.join(f'<a href="product-{pid}.html">{products[pid]["name"].replace("[물풀치크]","")} ↗</a>' for pid in pids)
   chapter.append(BeautifulSoup(f'<div class="ux-look-products"><p>이 무드와 어울리는 제품</p>{links}</div>','html.parser'))
  text=str(s)
 path.write_text(text,encoding='utf-8');changed.append(path.name)

# Original brand colour photographs are displayed through SVG viewports, not recoloured.
shutil.copy2('C:/Users/BNK-1/Desktop/tam-ux-review-261013/blurtint06.png',A/'tint-original-color-chart.jpg')
def svg(src,size,box):
 return f'<svg viewBox="{" ".join(map(str,box))}" aria-hidden="true" focusable="false"><image href="{src}" width="{size[0]}" height="{size[1]}"/></svg>'
lip_y=[570,1152,1735,2342,2948,3533,4119,4701]
cushion_boxes=[(135,2430,235,140),(188,2610,250,150),(392,2670,230,150),(499,2830,242,160),(440,3010,255,150),(587,3150,233,160)]
for pid in [23,112,102]:
 path=P/f'product-{pid}.html';s=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser');options=s.select_one('[data-preview-product]');select=options.select_one('select');buttons=[]
 for i,opt in enumerate(select.select('option')[1:]):
  if pid==112:photo=svg('assets/ux-261013/tint-original-color-chart.jpg',(840,5380),(130,lip_y[i],280,230))
  elif pid==23:photo=svg('assets/jelly-skin-cushion-0908/04.jpg',(860,4200),cushion_boxes[i])
  else:photo=f'<img src="assets/milky-cheek-v12/swatch{i+1:02d}.jpg" alt="" width="600" height="600" loading="lazy">'
  label=opt.get_text(' ',strip=True)
  buttons.append(f'<button class="ux-shade-button" type="button" data-option-index="{i+1}" aria-pressed="false" aria-label="{label} 선택">{photo}<span>{label}</span></button>')
 markup='<div class="ux-shades"><fieldset><legend>발색으로 컬러 선택</legend><div class="ux-shade-grid">'+''.join(buttons)+'</div></fieldset><p class="ux-shade-selected" aria-live="polite">컬러를 눌러 선택해 주세요.</p><p class="ux-shade-note">브랜드 원본 발색 이미지입니다. 피부 톤·사용량·화면 환경에 따라 다르게 보일 수 있습니다.</p></div>'
 options.insert(0,BeautifulSoup(markup,'html.parser'));path.write_text(str(s),encoding='utf-8')

# Animated original details become controlled, viewport-loaded video with an original link.
path=P/'product-23.html';s=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
for name in ['02','05','07']:
 img=s.find('img',src=f'assets/jelly-skin-cushion-0908/{name}.webp');w,h=img['width'],img['height']
 markup=f'<figure class="ux-detail-media"><video muted playsinline loop preload="none" poster="assets/ux-261013/cushion-{name}-poster.jpg" width="{w}" height="{h}" aria-label="쿠션 원본 사용 장면"><source src="assets/ux-261013/cushion-{name}.mp4" type="video/mp4"></video><figcaption><button type="button" aria-pressed="false">사용 장면 재생</button> <a href="assets/jelly-skin-cushion-0908/{name}.webp" target="_blank" rel="noopener">원본 보기 ↗</a><span class="ux-media-status" role="status"></span></figcaption></figure>'
 img.replace_with(BeautifulSoup(markup,'html.parser'))
path.write_text(str(s),encoding='utf-8')

# Retain manual coupon access, remove unsolicited panel opening and redundant footer trigger.
path=P/'assets/purchase-experience.js';s=path.read_text(encoding='utf-8')
s=s.replace("popupDelay: 12000, couponAmount: 3000", "popupDelay: 12000, autoPopupEnabled: false, couponAmount: 3000")
s=s.replace("if (shown || read('sessionStorage'", "if (config.autoPopupEnabled === false || shown || read('sessionStorage'")
s=s.replace("const triggerHost = info.isConnected ? info : document.querySelector('[data-tam-channel-trigger-host], .do-footer, footer');", "const triggerHost = info.isConnected ? info : document.querySelector('[data-tam-channel-trigger-host]');")
path.write_text(s,encoding='utf-8')
print(json.dumps({'updated_pages':changed,'count':len(changed)},ensure_ascii=False))
