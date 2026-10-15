"""Responsive R33 rebuild against the approved lipliner and Milky Cheek family."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'highlighter-r33'
template = (OUT/'detail.template.html').read_text(encoding='utf-8')
old_info = BeautifulSoup((ROOT/'highlighter-r32/product-information.html').read_text(encoding='utf-8'), 'html.parser').main
old_info.h1.decompose()
information = old_info.decode_contents()
shades = [
    ('01','문스톤','MOONSTONE','moonstone','아이시 화이트','밝고 시원한 포인트가 끌리는 날.','쿨톤 추천'),
    ('02','구미 핑크','GUMMY PINK','pink','밀키 핑크','핑크 메이크업에 생기를 더할 때.','쿨 · 뉴트럴톤 추천'),
    ('03','테디 골드','TEDDY GOLD','gold','베이지 골드','베이지 · 브라운 룩에 따뜻한 빛.','웜 · 뉴트럴톤 추천'),
]
cards = ''.join('''<figure class="h33-shade"><figcaption><h3>%(n)s %(name)s</h3><p class="h33-shade-en">%(en)s</p></figcaption><div class="h33-cheek"><img src="{{old}}tam-%(key)s.jpg" width="2819" height="3524" loading="lazy" alt="%(name)s 원본 피부 발색"></div><div class="h33-shade-summary"><div class="h33-shade-texture"><img src="{{assets}}shade-%(key)s.webp" loading="lazy" alt="%(name)s 실제 제형"></div><div><p class="h33-tone">%(tone)s</p><p class="h33-shade-description">%(description)s</p><p class="h33-shade-match">%(match)s</p></div></div></figure>''' % dict(n=n,name=name,en=en,key=key,tone=tone,description=description,match=match) for n,name,en,key,tone,description,match in shades)
looks = ''.join('''<figure class="h33-look"><div class="h33-look-image"><img src="{{old}}tam-%(key)s.jpg" width="2819" height="3524" loading="lazy" alt="%(name)s를 바른 광대와 볼의 피부 발색"></div><figcaption><h3>%(n)s %(name)s</h3><p>%(tone)s</p></figcaption></figure>''' % dict(n=n,name=name,key=key,tone=tone) for n,name,en,key,tone,description,match in shades)
template = template.replace('{{shades}}',cards).replace('{{looks}}',looks).replace('{{information}}',information)
def content(prefix):
    choose = '#purchase-options' if prefix=='../../' else '../storefront-v2/preview/product-24.html#purchase-options'
    return template.replace('{{old}}',prefix+'highlighter-r30/assets/').replace('{{motion}}',prefix+'highlighter-r32/assets/').replace('{{assets}}',prefix+'highlighter-r33/assets/').replace('{{choose}}',choose)
def revision(name):
    return hashlib.sha256((OUT/name).read_text(encoding='utf-8').encode()).hexdigest()[:12]
css, js = revision('detail.css'), revision('detail.js')
head = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>TAM BEAUTY | 더 젤리 빔 하이라이터 R33</title><link rel="stylesheet" href="detail.css?v={css}"><script defer src="detail.js?v={js}"></script><style>body{{margin:0;background:#eee}}main{{max-width:860px;margin:auto}}</style></head><body><main>'''
(OUT/'index.html').write_text(head+content('../')+'</main></body></html>\n',encoding='utf-8')
product = ROOT/'storefront-v2/preview/product-24.html'
before = product.read_text(encoding='utf-8')
replacement = '<!-- highlighter-r33:start --><section class="highlighter-final-detail" id="product-detail" aria-label="더 젤리 빔 하이라이터 상세 정보">'+content('../../')+'<a class="highlighter-detail-return" href="#purchase-options">컬러 선택으로 돌아가기 ↑</a></section><!-- highlighter-r33:end -->'
pattern = r'<!-- highlighter-r33:start -->.*?<!-- highlighter-r33:end -->' if '<!-- highlighter-r33:start -->' in before else r'<section\b[^>]*class="highlighter-final-detail"[^>]*>.*?</section>'
assert len(re.findall(pattern,before,re.S))==1
after = re.sub(pattern,lambda _:replacement,before,count=1,flags=re.S)
after = re.sub(r'\s*<link[^>]*href="../../highlighter-r33/detail.css[^>]*>', '', after)
after = re.sub(r'\s*<script[^>]*src="../../highlighter-r33/detail.js[^>]*></script>', '', after)
includes = f'<link rel="stylesheet" href="../../highlighter-r33/detail.css?v={css}"><script defer src="../../highlighter-r33/detail.js?v={js}"></script>'
after = after.replace('</head>', includes+'</head>')
product.write_text(after,encoding='utf-8')
print(f'R33 built. CSS {css}; JS {js}. Existing R32 retained.')
