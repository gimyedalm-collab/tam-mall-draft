"""Build the replanned Cloud Blush review candidate from verified existing assets."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'cloud-blush-v5'
OUT.mkdir(exist_ok=True)
OLD = (ROOT / 'cloud-blush-v4/detail.template.html').read_text(encoding='utf-8')
INFO = re.search(r'<details class="product-info">.*?</details>', OLD, re.S).group()
COLOURS = re.search(r'<div class="shade-grid">.*?</section>', OLD, re.S).group()
COLOURS = COLOURS.replace('생기 있는 선명한 핑크', '선명한 핑크')

body = '''<article id="cloud-blush" aria-label="더 클라우드 블러 크림 블러셔 상세페이지">
<section class="hero">
 <header class="hero-copy">
  <img class="logo" src="../cloud-blush-v3/assets/tam-logo.svg" width="156" height="44" alt="TAM BEAUTY">
  <p class="product-name">더 클라우드 블러 크림 블러셔</p>
  <h1>부드럽게 펴 바르고,<br>보송하게 마무리.</h1>
 </header>
 <figure class="campaign"><img src="assets/product-studio.png" width="1856" height="2304" fetchpriority="high" alt="라벤더 배경 위 열린 블러셔와 닫힌 블러셔를 함께 보여주는 제품 연출 이미지"></figure>
</section>
<section class="section texture" id="texture">
 <header class="heading"><span class="label">CREAM TO POWDER</span><h2>크림의 발림성,<br>파우더리한 마무리.</h2></header>
 <div class="wide-film"><video id="texture-film" controls muted loop playsinline preload="metadata" poster="../cloud-blush-v3/assets/cream-to-powder-poster.jpg" aria-label="손끝으로 크림을 덜고 펴 바르는 모습과 볼 메이크업 영상"><source src="../cloud-blush-v3/assets/cream-to-powder.mp4" type="video/mp4"></video></div>
 <div class="film-actions"><button class="film-toggle" type="button" aria-controls="texture-film" aria-pressed="false" hidden>영상 재생</button></div>
 <p class="body">손끝에 소량을 묻혀 얇게 펴 바른 뒤,<br>가볍게 두드려 주세요.</p>
</section>
<section class="model" aria-label="클라우드 블러 크림 블러셔 메이크업 연출">
 <figure class="model-photo"><img src="../cloud-blush-v3/assets/moa-blush.jpg" width="1200" height="1800" loading="lazy" alt="양손과 얼굴, 블러셔가 모두 보이는 모아의 핑크 볼 메이크업 사진"></figure>
</section>
<section class="section colours" id="colours">
 <header class="heading"><h2>여섯 가지 컬러,<br>볼 위에서 비교하세요.</h2></header>
''' + COLOURS + '''
<aside class="formula-note" aria-label="포뮬러와 용량"><p><strong>비건 포뮬러</strong><span aria-hidden="true"> · </span>2.8 g</p><p>살구씨오일 · 동백나무씨오일 · 올리브오일 · 서양자두씨오일 함유</p></aside>
''' + INFO + '\n</article>'
(OUT / 'detail.template.html').write_text(body, encoding='utf-8')
head = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="robots" content="noindex,nofollow"><title>탐뷰티 | 더 클라우드 블러 크림 블러셔 · V5 검토 시안</title><meta name="description" content="부드럽게 펴 바르고, 보송하게 마무리. 크림투파우더 제형과 여섯 가지 실제 볼 발색."><link rel="icon" href="../cloud-blush-v3/assets/tam-logo.svg" type="image/svg+xml"><link rel="stylesheet" href="detail.css"><script src="../cloud-blush-v3/detail.js" defer></script></head><body><main>'''
(OUT / 'index.html').write_text(head + body + '</main></body></html>', encoding='utf-8')
assert INFO in body
assert all(f'../cloud-blush-v3/assets/{kind}-{i}.jpg' in body for kind in ('cheek','swatch') for i in range(1,7))
assert '오늘의 생기' not in body
print('Built cloud-blush-v5; official information and 12 colour assets preserved.')
