"""Review actual exported V11/V12 media; record source preservation."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,html
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'cloud-blush-v12'; D=OUT/'review';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((ROOT/'cloud-blush-v11/asset-provenance.json').read_text(encoding='utf-8'))
new=json.loads((OUT/'asset-provenance.json').read_text(encoding='utf-8'))
prior={a['file']:a['sha256'] for a in old}
for a in new:
    if a['file'] in prior:assert a['sha256']==prior[a['file']]
assert sha(OUT/'product-information.html')==sha(ROOT/'cloud-blush-v11/product-information.html')
assert sha(OUT/'assets/cream-spread-finish.gif')==sha(ROOT/'cloud-blush-v11/assets/cream-spread-finish.gif')
sections=[('글자 크기','히어로 34→28, 제형 32→24, 일반 제목 26→24. 발색명·설명과 12px 전성분은 가독성을 유지합니다.',[0]),('여섯 색 설명','색 이름 반복을 줄이고 원본 발색에서 관찰되는 컬러 성격을 두 줄로 설명합니다. 개인별 발색이나 퍼스널컬러를 보장하는 표현은 쓰지 않습니다.',list(range(3,11))),('제형에서 사용법까지','기존 5.51초 GIF를 그대로 유지합니다. 제목 크기만 다른 섹션과 맞췄습니다.',[11,12,13]),('오일 이미지 복원','제품 합성 없이 기존 오일 연출 컷만 복원했습니다. 네 가지 오일명은 여섯 색 전성분에 모두 기재되어 있습니다.',[14]),('비건 마크만','제품·식물 배경 합성을 덜었습니다. 현재 표시는 브랜드 VEGAN FORMULA 그래픽이며 공식 인증 로고가 아닙니다.',[15])]
manifests={v:json.loads((ROOT/f'cloud-blush-v{v}/cafe24/manifest.json').read_text(encoding='utf-8')) for v in [11,12]}
def images(v,indices):
 return ''.join(f'<img loading="lazy" src="../../cloud-blush-v{v}/cafe24/{manifests[v]["files"][n]["file"]}" alt="{html.escape(manifests[v]["files"][n]["alt"],quote=True)}">' for n in indices)
cards=''.join(f'<section><h2>{title}</h2><p>{desc}</p><div class="pair"><div><h3>이전 V11</h3>{images(11,ix)}</div><div><h3>수정 V12</h3>{images(12,ix)}</div></div></section>' for title,desc,ix in sections)
doc='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V12 수정 비교</title><style>*{box-sizing:border-box}body{margin:0;background:#eee9ed;color:#39303d;font:15px/1.65 'Malgun Gothic',sans-serif}main{max-width:960px;margin:40px auto;padding:0 20px}h1{font-size:26px}h2{font-size:20px;margin-bottom:4px}h3{font-size:14px;font-weight:500;background:#e7dfe8;padding:10px;margin:0}p{max-width:760px;color:#635668}a{color:inherit}section{margin-top:50px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}.pair>div{align-self:start;min-width:0}.pair img{display:block;width:100%;height:auto}nav{display:flex;gap:20px;flex-wrap:wrap}.status{border-top:1px solid #cdbfce;margin-top:40px;padding-top:20px}@media(max-width:600px){main{padding:0 12px;margin-top:24px}.pair{gap:8px}h1{font-size:23px}h2{font-size:18px}}</style><main><h1>클라우드 블러 · 수정 비교</h1><p>요청한 네 가지를 중심으로 수정했습니다. 아래 비교 이미지는 실제 Cafe24 등록용 JPG/GIF입니다. 이미지·파일 검증과 소유자의 디자인 승인은 별개이며, Cafe24 실제 업로드는 보류 상태입니다.</p><nav><a href="../cafe24/">수정안 전체 보기</a><a href="../../cloud-blush-v11/cafe24/">이전안 전체 보기</a><a href="../plan.json">문안·소재 근거</a></nav>'''+cards+'''<p class="status">320·390·860px에서 이미지 로딩·가로 넘침·연결부·상품정보를 확인했습니다. 실제 발색의 실물 일치와 공식 인증마크는 확인되지 않았습니다. 발색 원본과 V11 제형 GIF, 상품정보·전성분은 유지했습니다.</p></main></html>'''
(D/'index.html').write_text(doc,encoding='utf-8')
result=dict(source_photo_hashes_preserved=True,gif_byte_identical_v11=True,native_information_byte_identical_v11=True,oil_image_restored=True,oil_product_overlay=False,vegan_product_photo=False,vegan_graphic='brand typography, not certification',review='actual exported images')
(OUT/'review-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('V12 actual-media comparison built; unchanged sources verified.')
