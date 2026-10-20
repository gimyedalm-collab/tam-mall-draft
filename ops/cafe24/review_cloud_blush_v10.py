from pathlib import Path
from bs4 import BeautifulSoup
import json, hashlib
ROOT=Path(__file__).resolve().parents[2]; O=ROOT/'cloud-blush-v10'; R=O/'review';R.mkdir(exist_ok=True)
labels=[('hero','첫 화면'),('palette','발색 비교'),('faces','얼굴 발색'),('texture','크림투파우더'),('formula','식물성 오일'),('howto','사용법'),('vegan','비건')]
rows=''.join(f'<section><h2>{label}</h2><div class="pair"><figure><figcaption>이전 · V9</figcaption><img src="../../cloud-blush-v9/review-{key}-430.png"></figure><figure><figcaption>조정 후 · V10</figcaption><img src="../review-{key}-430.png"></figure></div></section>' for key,label in labels)
(R/'index.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · 서체·장식 정리 전후</title><style>*{box-sizing:border-box}body{margin:0;background:#eee9ee;color:#39303d;font:16px/1.6 system-ui,sans-serif}main{max-width:980px;margin:auto;padding:28px 20px}h1{font-size:25px}h2{font-size:20px;margin-top:40px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0;background:white;align-self:start}figcaption{padding:12px}img{display:block;width:100%;height:auto}a{color:#66546d}.status{font-size:14px;color:#68596c}</style><main><h1>폰트와 장식을 덜어낸 상세페이지</h1><p>섹션 순서와 제품·발색 사진은 유지하고, 큰 세리프 영문과 이탤릭·흐림 장식·타원·칩을 정리했습니다. 한글 제목을 중심으로 색상명과 제형 설명의 반복도 줄였습니다.</p><p><a href="../cafe24/">현재 Cafe24 구성 전체 보기</a> · <a href="../../cloud-blush-v9/review/">기존 레퍼런스 대조</a></p><p class="status">사진 재생성·색상 보정 없음. 검토용 비교이며 실제 쇼핑몰 등록은 보류 상태입니다.</p>'''+rows+'</main></html>',encoding='utf-8')
page=R/'index.html'
text=page.read_text(encoding='utf-8').replace('폰트와 장식을 덜어낸 상세페이지','모바일 위계와 비율을 조정한 상세페이지').replace('서체·장식 정리 전후','모바일 균형 조정 전후').replace('섹션 순서와 제품·발색 사진은 유지하고, 큰 세리프 영문과 이탤릭·흐림 장식·타원·칩을 정리했습니다. 한글 제목을 중심으로 색상명과 제형 설명의 반복도 줄였습니다.','섹션 순서와 원본 색상은 유지했습니다. 핵심 제목은 강조하고 일반 제목과 도입 여백을 줄였으며, 얼굴 사진 비율을 60%로 넓혔습니다. 하단 정보는 내용과 12px 크기를 유지하며 서식을 정리했습니다.').replace('기존 레퍼런스 대조','이전 서체 정리 대조')
page.write_text(text,encoding='utf-8')
old=BeautifulSoup((ROOT/'cloud-blush-v9/detail.template.html').read_text(encoding='utf-8'),'html.parser')
new=BeautifulSoup((O/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
provenance=[]
for a,b in zip(old.select('img'),new.select('img')):
    pa=(ROOT/'cloud-blush-v9'/a['src']).resolve();pb=(O/b['src']).resolve()
    assert pa==pb, (a['src'],b['src'])
    provenance.append({'file':str(pb.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(pb.read_bytes()).hexdigest(),'unchanged_from_v9':True})
assert len(old.select('img'))==len(new.select('img'))
for v in ('v9','v10'):
    m=json.loads((ROOT/f'cloud-blush-{v}/cafe24/manifest.json').read_text(encoding='utf-8'))
    gifs=[i['sha256'] for i in m['files'] if i['kind']=='gif']
    if v=='v9':prior=gifs
    else:assert prior==gifs
(O/'asset-provenance.json').write_text(json.dumps({'images':provenance,'two_delivery_GIFs_byte_identical_to_v9':True,'recolouring':False,'new_generation':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('Before/after review and unchanged asset evidence recorded.')
