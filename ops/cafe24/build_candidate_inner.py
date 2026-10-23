"""Build candidate-only inner templates from owner-approved preview and local backups.

Original app-bearing templates stay outside Git. Native commerce markup is retained.
"""
from pathlib import Path
import argparse, json, re, shutil
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PREVIEW = ROOT / 'storefront-v2/preview'
ASSETS = ROOT / 'storefront-v2/cafe24/tam/assets'
BASE = 'https://awiz.cafe24.com/tam-detail-20261022/'
SKIN = '/skin-skin21'
VERSION = '261022-v4'
ROUTES = {'index.html':'/index.html', 'shop.html':'/product/list.html?cate_no=74',
 'jelly.html':'/product/list.html?cate_no=74&tam_collection=jelly',
 'cloud.html':'/product/list.html?cate_no=74&tam_collection=cloud',
 'lookbook.html':'/board/gallery/list.html?board_no=8', 'about.html':'/about.html',
 'search.html':'/product/search.html', 'login.html':'/member/login.html',
 'basket.html':'/order/basket.html'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
    copied={}
    def source(path):return (args.original/path).read_text(encoding='utf-8')
    def write(path,text):
        target=out/'templates'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    def asset(name):
        match=re.fullmatch(r'packshot-(\d+)\.png',name)
        if match or name=='cushion-pink-original-2.png':
            pid=match[1] if match else '23'
            with Image.open(PREVIEW/'assets'/name) as image:
                for width in (480,800):
                    dest=f'inner-card-{pid}-{width}.png'
                    scaled=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
                    scaled.save(out/dest,optimize=True,icc_profile=image.info.get('icc_profile'))
            copied[name]=dest;return BASE+dest
        if name.startswith('lookbook-') and name.endswith('.jpg'):
            with Image.open(PREVIEW/'assets'/name) as image:
                for width in (960,1600):
                    dest=f'inner-{Path(name).stem}-{width}.jpg'
                    scaled=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
                    scaled.save(out/dest,quality=90,optimize=True,progressive=True,icc_profile=image.info.get('icc_profile'))
            copied[name]=dest;return BASE+dest
        dest='inner-'+name;shutil.copy2(PREVIEW/'assets'/name,out/dest);copied[name]=dest;return BASE+dest
    def transform(node):
        for tag in node.select('[href]'):
            value=tag['href']
            if value in ROUTES:tag['href']=SKIN+ROUTES[value]
            elif re.fullmatch(r'product-\d+\.html',value):tag['href']=SKIN+'/product/detail.html?product_no='+re.search(r'\d+',value)[0]
            elif value.startswith('https://tambeauty.kr/'):
                tag['href']=SKIN+value.removeprefix('https://tambeauty.kr').replace('/member/agreement.html','/member/mall_agreement.html')
        for tag in node.select('img[src^="assets/"]'):
            tag['src']=asset(tag['src'].removeprefix('assets/'))
            if '-800.png' in tag['src']:
                tag['srcset']=tag['src'].replace('-800.png','-480.png')+' 480w, '+tag['src']+' 800w'
                tag['sizes']='(max-width:760px) 58vw, 460px'
            elif '-1600.jpg' in tag['src']:
                tag['srcset']=tag['src'].replace('-1600.jpg','-960.jpg')+' 960w, '+tag['src']+' 1600w'
                tag['sizes']='(max-width:760px) 100vw, 1440px' if 'featured' in tag.parent.get('class',[]) else '(max-width:760px) 50vw, 680px'
        return str(node)
    about=BeautifulSoup((PREVIEW/'about.html').read_text(encoding='utf-8'),'html.parser')
    header=about.select_one('header.ux-header')
    header_html=transform(header).replace('ux-','tam-nav-').replace('class="tam-nav-header"','class="header tam-nav-header"')
    # Auth state remains native. Hidden original Snap identity modules are preserved below.
    header_html=header_html.replace('<a class="tam-nav-account" href="'+SKIN+'/member/login.html">로그인</a>',
        '<a class="tam-nav-account" module="Layout_statelogoff" href="'+SKIN+'/member/login.html">로그인</a><a class="tam-nav-account" module="Layout_statelogon" href="'+SKIN+'/myshop/index.html">마이페이지</a>')
    original=source('moa/layout/header.html')
    write('moa/layout/header.html',re.sub(r'<header\b[\s\S]*?</header>',lambda _:header_html,original,count=1))
    footer=about.select_one('footer.ux-footer')
    company=footer.select_one('.ux-footer-company');company.select_one('p').replace_with(BeautifulSoup('<!--@import(/moa/import/footer/company_info.html)-->','html.parser'))
    footer_html=transform(footer).replace('ux-','tam-nav-').replace('class="tam-nav-footer"','class="footer tam-nav-footer" module="Layout_footer"')
    # Use authoritative shop contact runtime rather than copied mock opening hours.
    footer_html=re.sub(r'<p><a href="tel:1668-0868">[\s\S]*?</p>','<p><a href="tel:{$phone}">{$phone}</a><br>{$runtime}</p>',footer_html,count=1)
    write('moa/layout/footer.html',re.sub(r'<footer\b[\s\S]*?</footer>',lambda _:footer_html,source('moa/layout/footer.html'),count=1))
    write('layout/basic/layout.html',source('layout/basic/layout.html').replace('<body>','<body class="tam-native">'))
    shared_tags=f'<link rel="stylesheet" href="{BASE}candidate-inner-{VERSION}.css">\n<script defer src="{BASE}candidate-inner-{VERSION}.js"></script>\n'
    head=re.sub(r'<script defer src="[^"]*candidate-collections-261022.js"></script>\s*','',source('moa/layout/head.html'))
    write('moa/layout/head.html',head.replace('</head>',shared_tags+'</head>'))
    order=source('order/orderform.html').replace('</head>',f'<link rel="stylesheet" href="{BASE}candidate-inner-{VERSION}.css">\n</head>').replace('<body id="userStyle">','<body id="userStyle" class="tam-checkout">')
    write('order/orderform.html',order)
    filters='''<div class="tam-filters"><div role="group" aria-label="라인 선택"><button type="button" data-tam-line="all" aria-pressed="true">전체 라인</button><button type="button" data-tam-line="jelly" aria-pressed="false">The Jelly</button><button type="button" data-tam-line="cloud" aria-pressed="false">The Cloud</button></div><div role="group" aria-label="제품 종류"><button type="button" data-tam-category="all" aria-pressed="true">전체</button><button type="button" data-tam-category="base" aria-pressed="false">베이스</button><button type="button" data-tam-category="cheek" aria-pressed="false">치크</button><button type="button" data-tam-category="lip" aria-pressed="false">립</button><button type="button" data-tam-category="brow" aria-pressed="false">브로우</button><span class="tam-count" aria-live="polite"></span></div></div>'''
    original=source('product/list.html')
    package=original[original.index('    <div module="product_normalpackage">'):original.index('<!-- 해당 스크립트 삭제')]
    # Last close belongs to the old outer container.
    package=package.rstrip().removesuffix('</div>').rstrip().replace('<div class="product_area">','<div class="product_area" style="margin-left:0;margin-right:0">')
    snap=original[original.index('<!-- 해당 스크립트 삭제'):]
    shop='<!--@layout(/layout/basic/layout.html)-->\n<!--@js(/moa/js/lib/calc_sale_rate.js)-->\n<!--@js(/moa/js/lib/thumbnail_lazyload.js)-->\n<section class="tam-page-intro"><h1 data-tam-shop-title>Shop all</h1><p>The Jelly · The Cloud — 탐뷰티의 전체 제품을 만나보세요.</p></section>\n<section class="tam-catalog" data-tam-catalog><div class="tam-section-heading"><h2>All products</h2><a href="'+SKIN+'/product/list.html?cate_no=74">전체 제품 ↗</a></div>'+filters+package+'<p class="tam-empty" hidden>선택한 조건의 제품이 없습니다. 다른 분류를 선택해 주세요.</p></section>\n'+snap
    write('product/list.html',shop)
    search=source('product/search.html').replace('<div class="gInnerMargin">','<div class="tam-catalog" data-tam-search>')
    search=search.replace('<div class="titleArea">\n    <h2>SEARCH</h2>\n</div>','<section class="tam-page-intro"><h1>Search</h1><p>제품명이나 컬러 이름으로 탐뷰티를 찾아보세요.</p></section>')
    write('product/search.html',search)
    # Keep all native IDs/prices/stock/cart/wish handlers. A real link improves keyboard access.
    card=source('moa/import/product/product_form.html').replace('{$product_name}\n        </strong>','<a href="{$link_product_detail}">{$product_name}</a>\n        </strong>')
    # Native fallback handles future IDs without a prepared packshot; existing cards avoid downloading two hero images.
    card=re.sub(r'<img src="/moa/img/default/empty_thumb.png"[\s\S]*?>', '<img src="'+BASE+'inner-card-{$product_no}-800.png" srcset="'+BASE+'inner-card-{$product_no}-480.png 480w, '+BASE+'inner-card-{$product_no}-800.png 800w" sizes="(max-width:1099px) calc((100vw - 56px)/2), 340px" data-native-src="{$image_medium}" onerror="this.onerror=null;this.removeAttribute(\'srcset\');this.src=this.getAttribute(\'data-native-src\')" class="product-list-img" id="{$image_medium_id}" alt="{$seo_alt_tag}" loading="lazy" decoding="async" width="800" height="800">',card,count=1)
    # The approved cards have one still; remove the hidden hover image request.
    card=re.sub(r'<img src="\{\$add_image_src1\}"[\s\S]*?>','',card,count=1)
    write('moa/import/product/product_form.html',card)
    brand=about.select_one('main')
    catalog=brand.select_one('[data-catalog]')
    catalog.replace_with(BeautifulSoup('<section class="tam-explore"><div class="tam-section-heading"><h2>Explore tam</h2><a href="'+SKIN+'/product/list.html?cate_no=74">전체 제품 ↗</a></div><div data-tam-explore><a href="'+SKIN+'/product/list.html?cate_no=74">전체 제품과 현재 판매가 보기 ↗</a></div></section>','html.parser'))
    brand.name='div';brand['id']='tam-brand'
    write('about.html','<!--@layout(/layout/basic/layout.html)-->\n'+transform(brand))
    look=BeautifulSoup((PREVIEW/'lookbook.html').read_text(encoding='utf-8'),'html.parser').select_one('main');look.name='div';look['id']='tam-lookbook'
    archive=source('board/gallery/list.html').replace('<!--@layout(/layout/basic/layout.html)-->','')
    archive=archive.replace('<img src="{$img_src}"', '<img loading="lazy" decoding="async" src="{$img_src}"')
    write('board/gallery/list.html','<!--@layout(/layout/basic/layout.html)-->\n'+transform(look)+'\n<section class="tam-board-archive"><h2>브랜드 아카이브</h2>'+archive+'</section>')
    # Shared header/footer styles use separate names so the existing film page JS cannot bind to them.
    ux=(PREVIEW/'assets/ux-261013.css').read_text(encoding='utf-8')
    nav=ux[:ux.index('.do-hero{')].replace('ux-','tam-nav-')
    responsive=ux[ux.index('@media(max-width:900px){'):ux.index('@media(max-width:760px){')].replace('ux-','tam-nav-')
    css=(ASSETS/f'candidate-inner-{VERSION}.css').read_text(encoding='utf-8')
    identity=(PREVIEW/'assets/page-identity.css').read_text(encoding='utf-8')
    # All identity selectors are already unique except unrelated .film; omit that opening rule.
    identity=identity[identity.index('.brand-opening{'):]
    lookcss=(PREVIEW/'assets/lookbook.css').read_text(encoding='utf-8')
    (out/f'candidate-inner-{VERSION}.css').write_text(nav+responsive+identity+lookcss+'\n'+css,encoding='utf-8')
    shutil.copy2(ASSETS/f'candidate-inner-{VERSION}.js',out/f'candidate-inner-{VERSION}.js')
    for pid in [18,23,24,25,101,102,109,110,111,112,114,115,118,121]:asset('cushion-pink-original-2.png' if pid==23 else f'packshot-{pid}.png')
    (out/'manifest.json').write_text(json.dumps({'skin':'skin21','assets':copied,'templates':[str(p.relative_to(out/'templates')).replace('\\','/') for p in (out/'templates').rglob('*.html')]},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(out),'assets':len(copied),'templates':len(list((out/'templates').rglob('*.html')))}))

if __name__=='__main__':main()
