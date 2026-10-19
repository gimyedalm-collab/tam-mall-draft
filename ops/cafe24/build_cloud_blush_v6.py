"""Reference-led Cloud Blush detail; source facts and official info stay traceable."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'cloud-blush-v6'
OUT.mkdir(exist_ok=True)
OLD = (ROOT / 'cloud-blush-v5/detail.template.html').read_text(encoding='utf-8')
INFO = re.search(r'<details class="product-info">.*?</details>', OLD, re.S).group()
A = '../cloud-blush-v3/assets/'
SHADES = [
 ('백도 쉐이크', 'WHITE PEACH SHAKE', '부드러운 피치 핑크', '복숭아빛을 머금은 핑크로<br>은은하고 부드러운 볼.'),
 ('구아바 쉐이크', 'GUAVA SHAKE', '차분한 로지 핑크', '차분한 장밋빛으로<br>자연스럽게 물든 볼.'),
 ('아사이베리 쉐이크', 'ACAI BERRY SHAKE', '화사한 라벤더 핑크', '보랏빛이 감도는 핑크로<br>맑고 화사한 볼.'),
 ('파파야 쉐이크', 'PAPAYA SHAKE', '따뜻한 코랄 오렌지', '오렌지를 더한 코랄로<br>따뜻하고 산뜻한 볼.'),
 ('용과 쉐이크', 'DRAGON FRUIT SHAKE', '선명한 핑크', '선명한 핑크 한 겹으로<br>또렷한 포인트를 준 볼.'),
 ('살구 쉐이크', 'APRICOT SHAKE', '차분한 살구 베이지', '베이지가 섞인 살구빛으로<br>차분하고 포근한 볼.'),
]
cards = '\n'.join(f'''<figure class="shade" id="shade-{i}">
 <figcaption><h3><span class="shade-number">0{i}</span> {name}</h3><p class="english">{english}</p></figcaption>
 <div class="cheek"><img src="{A}cheek-{i}.jpg" width="1100" height="1137" loading="lazy" alt="{name} 실제 볼 발색"></div>
 <img class="swatch" src="{A}swatch-{i}.jpg" width="600" height="600" loading="lazy" alt="{name} 실제 제형 발색">
 <p class="tone">{tone}</p><p class="shade-description">{desc}</p>
</figure>''' for i, (name, english, tone, desc) in enumerate(SHADES, 1))

body = f'''<article id="cloud-blush" aria-label="더 클라우드 블러 크림 블러셔 상세페이지">
<section class="hero" aria-labelledby="hero-title">
 <img class="hero-image" src="../cloud-blush-v5/assets/product-studio.jpg" width="1856" height="2304" fetchpriority="high" alt="라벤더 배경에 놓인 열린 크림 블러셔와 닫힌 블러셔">
 <header class="hero-copy"><p class="product-name">더 클라우드 블러 크림 블러셔</p><h1 id="hero-title">크림처럼 사르르,<br>파우더처럼 보송하게.</h1></header>
 <div class="hero-signature"><img src="{A}tam-logo.svg" width="156" height="44" alt="TAM BEAUTY"><p>6 COLOURS · 2.8 g</p></div>
</section>
<section class="section texture" id="texture">
 <header class="heading"><p class="eyebrow">CREAM TO POWDER</p><h2>펴 바를 땐 부드럽게,<br>마무리는 보송하게.</h2></header>
 <div class="wide-film"><video id="texture-film" controls muted loop playsinline preload="metadata" poster="{A}cream-to-powder-poster.jpg" aria-label="크림 제형을 만지고 펴 바르는 모습과 볼 메이크업 영상"><source src="{A}cream-to-powder.mp4" type="video/mp4"></video></div>
 <div class="film-chapters" role="group" aria-label="제형 영상 장면 선택" hidden>
  <button type="button" data-start="0" aria-controls="texture-film" aria-pressed="true"><span>01</span> 부드러운 크림</button>
  <button type="button" data-start="2.6" aria-controls="texture-film" aria-pressed="false"><span>02</span> 얇게 펴 바르기</button>
  <button type="button" data-start="7.4" aria-controls="texture-film" aria-pressed="false"><span>03</span> 볼 메이크업</button>
 </div>
 <div class="film-actions"><button class="film-toggle" type="button" aria-controls="texture-film" aria-pressed="false" hidden>영상 재생</button></div>
 <div class="application-guide" id="howto"><p class="application-label">HOW TO USE</p><p class="application-copy">손끝에 소량 묻혀 얇게 펴 바르고,<br>경계를 톡톡 두드려 주세요.</p></div>
</section>
<section class="section colours" id="colours">
 <header class="heading"><p class="eyebrow">SIX SHADES OF CLOUD</p><h2>은은한 피치부터<br>선명한 핑크까지.</h2><p class="body">제형과 볼 위 발색을 함께 확인하세요.</p></header>
 <div class="shade-grid">{cards}</div>
 <p class="note">피부 톤과 사용량, 조명 및 화면 환경에 따라 발색이 다르게 보일 수 있습니다.</p>
</section>
<section class="formula" id="formula">
 <header class="heading"><p class="eyebrow">VEGAN FORMULA</p><h2>보송한 치크에 담은<br>네 가지 오일.</h2><p class="body">식물성 오일을 담은 비건 포뮬러.</p></header>
 <figure class="formula-photo"><img src="assets/formula-clear-oil-261019.jpg" width="1536" height="1024" loading="lazy" alt="화이트 배경 위 맑은 식물성 오일을 표현한 원료 연출 이미지"></figure>
 <div class="ingredients"><div><h3>살구씨오일</h3><p>APRICOT KERNEL OIL</p></div><div><h3>동백나무씨오일</h3><p>CAMELLIA SEED OIL</p></div><div><h3>올리브오일</h3><p>OLIVE FRUIT OIL</p></div><div><h3>서양자두씨오일</h3><p>PLUM SEED OIL</p></div></div>
 <p class="note">원료를 표현한 연출 이미지입니다.</p>
</section>
<section class="ending" aria-label="더 클라우드 블러 크림 블러셔 컬렉션">
 <header class="heading"><p class="eyebrow">THE CLOUD BLUR CREAM BLUSH</p><h2>부드러운 컬러,<br>보송한 블러 치크.</h2><p class="body">더 클라우드 블러 크림 블러셔<br><span class="ending-spec">6 COLOURS · 2.8 g</span></p></header>
 <figure class="ending-photo"><img src="{A}ending.jpg" width="1080" height="1350" loading="lazy" alt="라벤더 케이스의 여섯 가지 크림 블러셔 컬렉션"></figure>
 <div class="ending-footer"><img src="{A}tam-logo.svg" width="156" height="44" alt="TAM BEAUTY"></div>
</section>
{INFO}
</article>'''
(OUT / 'detail.template.html').write_text(body, encoding='utf-8')
head = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="robots" content="noindex,nofollow"><title>탐뷰티 | 더 클라우드 블러 크림 블러셔 · V6</title><meta name="description" content="크림처럼 사르르, 파우더처럼 보송하게. 크림투파우더 제형과 블러 마무리, 여섯 가지 실제 발색을 만나보세요."><link rel="icon" href="../cloud-blush-v3/assets/tam-logo.svg" type="image/svg+xml"><link rel="stylesheet" href="detail.css"><script src="detail.js" defer></script></head><body><main>'''
(OUT / 'index.html').write_text(head + body + '</main></body></html>', encoding='utf-8')
assert INFO in body
assert all(f'{A}{kind}-{i}.jpg' in body for kind in ('cheek', 'swatch') for i in range(1, 7))
assert len(re.findall(r'<section ', body)) == 5
print('Built V6: five product-led sections with application integrated under the film; official information preserved.')
