"""Small, evidence-led refinement of V9. No new claims or media generation."""
from pathlib import Path
from bs4 import BeautifulSoup
import json

ROOT=Path(__file__).resolve().parents[2]; OLD=ROOT/'cloud-blush-v9'; OUT=ROOT/'cloud-blush-v10'
OUT.mkdir(exist_ok=True)
plan={
    'intent':'기존 구성을 유지하며 제목 위계, 도입 여백, 얼굴 발색 면적, 하단 정보 서식을 소폭 조정',
    'basis':'V9 rendered390px audit and owner instruction: 그래 조금 깎아보자',
    'changes':[
        '390px 기준 히어로28.1→30.8px, 제형26.3→29.0px, 일반제목26.3→23.6px',
        '히어로980→900 source px, 소개 여백 축소, 중복 영문 구분 표시 제거',
        '얼굴 사진50→60%, 설명50→40%; 사진 확대율을 보정해 기존 볼 크기 유지',
        '전성분12px 유지, 기본 한글 서체와 표 줄바꿈·색상별 구분 조정'
    ],
    'preserve':['섹션 순서','6색 손목 비교','6개 원본 얼굴 발색','원본 사진 색상','두 GIF 바이트','기존 문안·성분·제품 정보'],
    'limits':['기존 제형 영상은 터치·도포 장면이며 파우더 전환을 입증하는 별도 시험이 아님','실제 색 일치 및 소유자 시각 승인 미확인','Cafe24 실제 업로드 보류']
}
(OUT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
s=BeautifulSoup((OLD/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
for selector in ['.intro .eyebrow','#palette .eyebrow','#faces .eyebrow','#formula .eyebrow','#howto .eyebrow','#vegan .eyebrow']:
    s.select_one(selector).decompose()
info=s.select_one('[data-tam-product-info]')
info['style']=info['style'].replace('font-family:Arial,sans-serif','font-family:Malgun Gothic,Apple SD Gothic Neo,Arial,sans-serif')
for th in info.select('th'):
    th['style']=th['style'].replace('width:100px','width:88px').replace('padding:5px 10px 5px 0','padding:5px 8px 5px 0')
for td in info.select('td'):
    td['style']+='word-break:keep-all;'
for block in info.select(':scope > div'):
    block['style']='margin:0 0 6px;padding-top:8px;border-top:1px solid #eee9ef;'
old_info=BeautifulSoup((OLD/'product-information.html').read_text(encoding='utf-8'),'html.parser')
assert info.get_text(' ',strip=True)==old_info.get_text(' ',strip=True)
(OUT/'product-information.html').write_text(str(info),encoding='utf-8')
body=str(s)
(OUT/'detail.template.html').write_text(body,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V10 모바일 균형 조정</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
css=(OLD/'detail.css').read_text(encoding='utf-8')
changes={
    '.heading{padding:60px 24px 34px}':'.heading{padding:50px 24px 28px}',
    '.heading h2{font-size:29px':'.heading h2{font-size:26px',
    '.hero{height:980px':'.hero{height:900px',
    '.hero-copy{padding-top:104px':'.hero-copy{padding-top:80px',
    '.hero h2{font-size:31px':'.hero h2{font-size:34px',
    'margin:27px 15px 0':'margin:23px 15px 0',
    '.intro header{padding:58px 24px 36px}':'.intro header{padding:40px 24px 28px}',
    '.intro h2{font-size:29px':'.intro h2{font-size:26px',
    '.intro-meta{font-size:17px;margin-top:18px':'.intro-meta{font-size:17px;margin-top:12px',
    '.face-row{display:grid;grid-template-columns:1fr 1fr;padding:0 30px 20px':'.face-row{display:grid;grid-template-columns:3fr 2fr;padding:0 30px 18px',
    '.cheek{height:126px':'.cheek{height:132px',
    '.cheek img{position:absolute;left:-19%;top:-84%;width:138%':'.cheek img{position:absolute;left:-7.5%;top:-80.18%;width:115%',
    '.face-row figcaption{padding:12px 12px 10px':'.face-row figcaption{padding:10px',
    '.face-row h3{font-size:18px;font-weight:600;line-height:1.35':'.face-row h3{font-size:18px;font-weight:600;line-height:1.3',
    '.texture .heading{padding-top:55px}':'.texture .heading{padding-top:52px}.texture .heading h2{font-size:32px}',
    '.formula .heading{padding-top:55px':'.formula .heading{padding-top:48px',
    '.formula .heading h2{font-size:27px}':'.formula .heading h2{font-size:26px}',
    '.howto .heading{padding:55px 24px 26px}':'.howto .heading{padding:48px 24px 26px}',
    '.vegan .heading{padding-top:45px;padding-bottom:32px}':'.vegan .heading{padding-top:45px;padding-bottom:28px}',
}
for before,after in changes.items():
    assert before in css,before
    css=css.replace(before,after)
(OUT/'detail.css').write_text(css,encoding='utf-8')
print('V10 targeted refinement built; facts and source image paths preserved.')
