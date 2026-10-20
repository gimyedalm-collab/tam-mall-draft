"""Refine the approved V8 composition; preserve all source photographs."""
from pathlib import Path
from bs4 import BeautifulSoup
import json, shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'cloud-blush-v9'
OUT.mkdir(exist_ok=True)
plan = {
    'intent': 'V8 배치와 사진 비율을 유지하며 서체·장식·중복 문안을 덜어 탐뷰티 톤으로 정리',
    'retain': ['섹션 순서', '3개 제품 히어로', '한눈에 보는 6색 손목 발색', '6개 얼굴 발색과 크롭', '원본 제형·발색 색상', '크림투파우더 USP', '전성분'],
    'remove': ['Bodoni 세리프·이탤릭', '글자 뒤 흐림 장식', '해시태그·키워드 칩', '영문 색상명 중복', '사용법 타원', '사용기한 연결선·박스', '제형 설명 반복'],
    'type': 'Pretendard Korean / Manrope English; source-only local fonts, baked into Cafe24 images',
    'evidence': 'Existing V8 assets, source provenance and claims retained. This is visual simplification, not a new efficacy or shade claim.',
    'cafe24_upload': 'deferred_by_owner'
}
(OUT/'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
s = BeautifulSoup((ROOT/'cloud-blush-v8/detail.template.html').read_text(encoding='utf-8'), 'html.parser')
for img in s.select('img[src^="assets/"]'):
    img['src'] = '../cloud-blush-v8/' + img['src']
def content(selector, html):
    el=s.select_one(selector); el.clear()
    el.append(BeautifulSoup(html,'html.parser'))
content('.hero h1', 'THE CLOUD BLUR')
s.select_one('.hero-copy p').decompose()
content('.intro header', '<p class="eyebrow">TAM BEAUTY</p><h2>더 클라우드 블러<br>크림 블러셔</h2><p class="intro-meta">6가지 컬러 · 2.8 g</p>')
content('#palette .heading', '<p class="eyebrow">COLOUR PALETTE</p><h2>여섯 가지 컬러</h2>')
for i, figure in enumerate(s.select('.texture-grid figure'), 1):
    content_selector=figure.select_one('figcaption')
    content_selector.string=f'{i:02}'
    figure.select_one('small').decompose()
content('#faces .heading', '<p class="eyebrow">ON CHEEKS</p><h2>볼 위에 올린 컬러</h2>')
for i, row in enumerate(s.select('.face-row'), 1):
    row.select_one('.english').string=f'{i:02}'
content('#texture .heading', '<p class="eyebrow">CREAM TO POWDER</p><h2>펴 바를 땐 부드럽게,<br>마무리는 보송하게.</h2>')
s.select_one('.texture-strip').decompose()
s.select_one('.texture-bottom').decompose()
s.select_one('.howto-end').decompose()
content('#formula .heading', '<p class="eyebrow">FORMULA</p><h2>네 가지 식물성 오일 함유</h2><p class="oil-names">살구씨 · 동백나무씨<br>올리브 · 서양자두씨오일</p>')
content('#howto .heading', '<p class="eyebrow">HOW TO USE</p><h2>얇게 펴 바르고,<br>가볍게 톡톡.</h2><p>손끝이나 도구로 얇게 펴 바른 뒤<br>경계를 가볍게 두드려 주세요.</p>')
content('#vegan .heading', '<p class="eyebrow">VEGAN FORMULA</p><h2>탐뷰티의 비건 포뮬러</h2>')
content('#check', '<div class="expiry"><h2>사용 기한</h2><p>개봉 후 12개월 · 개봉 전 36개월</p></div><img class="logo" src="../cloud-blush-v3/assets/tam-logo.svg" alt="TAM BEAUTY">')
body=str(s)
(OUT/'detail.template.html').write_text(body, encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V9 서체와 장식 정리</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>', encoding='utf-8')
shutil.copy2(ROOT/'cloud-blush-v8/product-information.html', OUT/'product-information.html')
print('V9 typography and copy refinement assembled.')
