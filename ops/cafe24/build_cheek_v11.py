"""Build a responsive continuation of V10 using unchanged brand photographs."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('C:/Users/BNK-1/Desktop/_탐뷰티/물풀치크_상세_V8_261002/assets')
PHOTOS = Path('C:/Users/BNK-1/Desktop/_탐뷰티/물풀치크_상세_V10_261002/assets')
DEST = ROOT / 'storefront-v2/preview/assets/milky-cheek-v11'
DEST.mkdir(parents=True, exist_ok=True)
sources = {name: SOURCE / 'web' / name for name in ['hero-product.jpg', 'formula-pink.jpg']}
sources.update({f'cheek{i:02}.jpg': PHOTOS / f'cheek{i:02}.jpg' for i in range(1, 5)})
sources.update({name: SOURCE / name for name in ['three-steps.mp4', 'three-steps-poster.png', 'tam-logo.svg']})
for name, source in sources.items():
    shutil.copy2(source, DEST / name)

def detail(prefix):
    colours = [('헬로버니', '밀키 핑크'), ('썬플러쉬', '코랄 핑크'), ('누드티', '핑크 베이지'), ('로지댄스', '모브 핑크')]
    figures = ''.join(f'''<figure class="mc-colour">
      <div class="mc-cheek"><img src="{prefix}cheek{i:02}.jpg" width="2992" height="3740" loading="lazy" alt="{name} 실제 볼 발색"></div>
      <figcaption><h3><span>{i:02}</span> {name}</h3><p>{tone}</p></figcaption>
    </figure>''' for i, (name, tone) in enumerate(colours, 1))
    return f'''<section id="milky-cheek-detail" aria-label="더 젤리 밀키 치크 블러셔 상세" data-detail-release="cheek-v11">
  <header class="mc-hero">
    <p class="mc-en">THE JELLY MILKY CHEEK BLUSH</p>
    <h2>밀키하게 물드는 볼.</h2>
    <p class="mc-lead">은은한 젤리광의 비건 치크.</p>
    <div class="mc-hero-photo"><img src="{prefix}hero-product.jpg" width="1800" height="1200" alt="물풀치크 제품과 네 가지 컬러 제형" fetchpriority="high"></div>
    <p class="mc-product-name">더 젤리 밀키 치크 블러셔</p>
  </header>
  <section class="mc-colours mc-inset" aria-labelledby="mc-colours-title">
    <h2 id="mc-colours-title">볼 위에서 만나는<br class="mc-mobile-break"> 네 가지 컬러.</h2>
    <p class="mc-intro">색감과 은은한 윤기를 함께 비교해 보세요.</p>
    {figures}
    <p class="mc-note">피부 톤과 사용량, 조명에 따라 발색이 다를 수 있습니다.</p>
  </section>
  <section class="mc-formula" aria-labelledby="mc-formula-title">
    <div class="mc-formula-photo"><img src="{prefix}formula-pink.jpg" width="1800" height="1200" loading="lazy" alt="헬로버니 제형과 스펀지 팁"></div>
    <div class="mc-formula-copy">
      <h2 id="mc-formula-title">비건 포뮬러에<br>스킨케어 성분까지.</h2>
      <p class="mc-intro">네 가지 컬러 공통 함유.</p>
      <dl>
        <div><dt>히알루론산 계열·스쿠알란</dt><dd>피부를 부드럽게 하는 스쿠알란*</dd></div>
        <div><dt>판테놀·알란토인</dt><dd>피부 컨디셔닝 성분, 판테놀*</dd></div>
        <div><dt>세라마이드NP</dt><dd>전성분명: 세라마이드엔피</dd></div>
      </dl>
      <p class="mc-note">*원료적 특성에 한함.</p>
    </div>
  </section>
  <section class="mc-howto mc-inset" aria-labelledby="mc-howto-title">
    <h2 id="mc-howto-title">짜서 바로, 스펀지로 톡톡.</h2>
    <p class="mc-intro">브러시를 꺼낼 필요 없이, 용기 하나로.</p>
    <div class="mc-howto-grid">
      <div class="mc-film">
        <video muted loop playsinline preload="none" poster="{prefix}three-steps-poster.png" aria-label="물풀치크 실제 사용 영상" controls><source src="{prefix}three-steps.mp4" type="video/mp4"></video>
        <button class="mc-play" type="button" aria-label="사용법 영상 재생" aria-pressed="false" hidden>재생</button>
      </div>
      <ol class="mc-steps">
        <li><h3>ON으로 열기</h3><p>팁에 소량 짜 주세요.</p></li>
        <li><h3>볼 위에 톡톡</h3><p>두드리며 펴 발라 주세요.</p></li>
        <li><h3>OFF로 닫기</h3><p>사용 후 캡을 닫아 주세요.</p></li>
      </ol>
    </div>
    <p class="mc-tip">처음에는 소량,<br class="mc-mobile-break"> 원하는 색감만큼 덧발라 주세요.</p>
  </section>
  <section class="mc-test mc-inset" aria-labelledby="mc-test-title">
    <div class="mc-test-result"><div><h2 id="mc-test-title">피부 일차 자극 시험 완료.</h2><p>4가지 컬러 각각 평균 피부반응도</p></div><strong>0.00</strong></div>
    <p class="mc-note">한국피부과학연구원 · 성인 여성 32명<br>측정기간 2024.11.25 ~ 2024.11.28<br>24시간 첩포 후 제거 30분·24시간·48시간 평가<br>시험 조건에 따른 결과이며 개인차가 있습니다.</p>
    <img class="mc-logo" src="{prefix}tam-logo.svg" width="156" height="44" loading="lazy" alt="TAM BEAUTY">
  </section>
</section>'''

standalone = ROOT / 'cheek-v11'
standalone.mkdir(exist_ok=True)
(standalone / 'index.html').write_text('''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>탐뷰티 | 더 젤리 밀키 치크 블러셔</title><link rel="stylesheet" href="../storefront-v2/preview/assets/milky-cheek-v11/detail.css"><style>body{margin:0;background:#f4f2f3}main{margin:auto;max-width:860px}</style><script src="../storefront-v2/preview/assets/milky-cheek-v11/detail.js" defer></script></head><body><main>''' + detail('../storefront-v2/preview/assets/milky-cheek-v11/') + '</main></body></html>\n', encoding='utf-8')

page = ROOT / 'storefront-v2/preview/product-102.html'
before = page.read_text(encoding='utf-8')
pattern = r'<!-- cheek-v11:start -->.*?<!-- cheek-v11:end -->' if '<!-- cheek-v11:start -->' in before else r'<section class="detail-source container cushion-final-detail" id="product-detail".*?</section>'
replacement = '<!-- cheek-v11:start --><section class="detail-source container cushion-final-detail" id="product-detail" aria-label="물풀치크 제품 상세">' + detail('assets/milky-cheek-v11/') + '<a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section><!-- cheek-v11:end -->'
after, count = re.subn(pattern, lambda _: replacement, before, count=1, flags=re.S)
assert count == 1
includes = '<link rel="stylesheet" href="assets/milky-cheek-v11/detail.css"><script src="assets/milky-cheek-v11/detail.js" defer></script>'
if includes not in before:
    after = after.replace('</head>', includes + '</head>', 1)
assert after.replace(includes, '').replace(replacement, re.search(pattern, before, re.S)[0]) == before.replace(includes, '')
page.write_text(after, encoding='utf-8', newline='\n')

report = {
    'version': 'V11', 'date': '2026-10-13', 'product_no': 102,
    'baseline': 'V10; original section order, photo crops, shade names, formula and test copy retained.',
    'changes': ['Responsive HTML text replaces scaled image text.', 'Readable mobile ingredient and instructional layouts.', 'Original MP4 with pause control and reduced-motion behavior replaces GIF.'],
    'commerce_outside_detail_unchanged': True, 'production_cafe24_changed': False,
    'image_edits': 'None; existing optimized hero/formula files and original V10 cheek photos copied byte-for-byte. Cropping is CSS only.',
    'sources': [{'file': name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'bytes': source.stat().st_size} for name, source in sources.items()],
    'status': 'local_candidate_awaiting_visual_QA',
}
(ROOT / 'ops/cafe24/cheek-detail-v11.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('V11 standalone and product 102 built; surrounding commerce preserved.')
