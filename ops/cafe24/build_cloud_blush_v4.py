"""Build the evidence-led cloud blush candidate and its production board."""
from pathlib import Path
import json,shutil,re,html
R=Path(__file__).resolve().parents[2]
W=Path('C:/Users/BNK-1/Desktop/tam-cloud-blush-20261015/audit')
O=R/'cloud-blush-v4'; A=O/'assets'; D=O/'review'
A.mkdir(parents=True,exist_ok=True);D.mkdir(exist_ok=True)
facts=json.loads((W/'direction-20261016.json').read_text(encoding='utf-8'))
prompts=json.loads((W/'higgsfield-prompts-20261016.json').read_text(encoding='utf-8'))
shutil.copyfile(W/'hf-candidate-0.png',A/'hero-peach-curve.png')
shutil.copyfile(W/'oy-sales-visible-20261016.png',D/'oliveyoung-sales-20261016.png')
(D/'evidence.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2),encoding='utf-8')
H=html.escape
prompt_text='TAM Beauty / 더 클라우드 블러 크림 블러셔\n2026-10-16 / Higgsfield 촬영 프롬프트 및 검수 기록\n\n원본 제품 01호 닫힘·열림 사진을 참조. C만 실제 1호 제형 사진 추가.\nA: 상세 시안 메인 적용. B와 C: 인쇄 변형으로 미채택. B와 C의 프롬프트는 테스트 기록이며 납품용 이미지로 통과한 것이 아님. 생성 제형은 실제 발색 증거로 사용 금지.\n\n'
for shot,p in zip(facts['shots'],prompts):
    prompt_text+=shot['name']+' / '+shot['ratio']+'\n목적: '+shot['reason']+'\n판단 범위: '+shot['hypothesis']+'\n원본: '+shot['reference']+'\n검수: '+shot['checks']+'\n\n'+p['params']['prompt']+'\n\n'+'='*60+'\n\n'
(D/'higgsfield-prompts.txt').write_text(prompt_text.rstrip()+'\n',encoding='utf-8')
s=(R/'cloud-blush-v3/detail.template.html').read_text(encoding='utf-8')
s=s.replace('assets/','../cloud-blush-v3/assets/')
s=s.replace('부드럽게 물드는<br>보송한 블러 컬러.','크림처럼 부드럽게,<br>마무리는 보송하게.')
s=s.replace('<p class="body">나의 볼에 더하는<br>여섯 가지 쉐이크 컬러.</p>','')
png=(A/'hero-peach-curve.png').read_bytes()
hero_w=int.from_bytes(png[16:20],'big');hero_h=int.from_bytes(png[20:24],'big')
s=s.replace('../cloud-blush-v3/assets/hero-product.jpg','assets/hero-peach-curve.png').replace('width="1080" height="1350" fetchpriority',f'width="{hero_w}" height="{hero_h}" fetchpriority')
s=s.replace('중성 배경 위 라벤더 용기의 크림 블러셔 두 가지 컬러','피치색 곡면 위 백도 쉐이크 제품 두 개를 배치한 AI 연출 이미지')
s=s.replace('크림에서 보송함으로.','바르는 질감부터<br>볼 위의 마무리까지.')
s=s.replace('부드럽게 펴 발리는 크림이<br>볼 위에서는 파우더리하게 마무리돼요.','손끝으로 부드럽게 펴 바르는<br>크림투파우더 제형.')
s=s.replace('나의 볼에 어울리는<br>여섯 가지 쉐이크 컬러.','피치부터 베리까지,<br>여섯 가지 컬러.')
s=s.replace('<p class="body">볼 위의 발색과 제형을<br>함께 비교해 보세요.</p>','')
s=s.replace('소량으로 시작해,<br>원하는 색감만큼.','조금씩 톡톡,<br>원하는 색감으로.')
s=s.replace('<h3>얇게 펴 바르기</h3><p>생기를 더할 부위에<br>가볍게 두드려 주세요.</p>','<h3>얇게 펴 바르기</h3><p>볼에 얇게 펴 바른 뒤<br>가볍게 두드려 주세요.</p>')
s=s.replace('오늘의 볼에 어울리는<br>컬러를 골라보세요.','오늘의 생기를<br>골라보세요.')
s=re.sub(r' <div class="ending-photo">.*?</div>\n','',s)
(O/'detail.template.html').write_text(s,encoding='utf-8')
(O/'detail.css').write_text("@import url('../cloud-blush-v3/detail.css');\n#cloud-blush .hero-copy{background:#f5ece9}\n#cloud-blush .campaign{aspect-ratio:auto}\n#cloud-blush .campaign img{width:100%;height:auto}\n",encoding='utf-8')
head='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>탐뷰티 | 더 클라우드 블러 크림 블러셔 · V4 검토 시안</title><meta name="description" content="크림처럼 부드럽게, 마무리는 보송하게. 더 클라우드 블러 크림 블러셔."><link rel="stylesheet" href="detail.css"><script src="../cloud-blush-v3/detail.js" defer></script></head><body><main>'
(O/'index.html').write_text(head+s+'</main></body></html>',encoding='utf-8')
top=''.join('<tr><td>'+str(x['position'])+'</td><td><a href="'+H(x['url'])+'" target="_blank" rel="noopener">'+H(x['title'])+'</a></td></tr>' for x in facts['top10'])
comp=''.join('<article class="comparison"><p class="eyebrow">판매순 '+str(x['position'])+'번째 · '+str(x['reviews'])+'개 리뷰 · '+str(x['rating'])+'/5</p><h3>'+H(x['brand'])+' <small>'+H(x['product'])+'</small></h3><p><b>확인한 것</b> '+H(x['observed'])+'</p><p><b>TAM에 적용</b> '+H(x['decision'])+'</p><a target="_blank" rel="noopener" href="https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo='+x['id']+'">올리브영 원문 ↗</a></article>' for x in facts['comparisons'])
copy=''.join('<tr><th>'+H(x[0])+'</th><td>'+H(x[1])+'</td><td><strong>'+H(x[2])+'</strong><small>'+H(x[3])+'</small></td></tr>' for x in facts['copy'])
shots=''
for sh,p in zip(facts['shots'],prompts):
    status=['시안 메인에 적용','인쇄 변형으로 미채택','인쇄 변형으로 미채택 · 원본 제형 유지'][sh['index']]
    photo='<img src="../assets/hero-peach-curve.png" alt="피치 곡면 위 제품 연출 A안" loading="lazy">' if sh['index']==0 else ''
    shots+='<article class="shot"><div>'+photo+'</div><div><p class="eyebrow">'+H(status)+'</p><h3>'+H(sh['name'])+'</h3><p>'+H(sh['reason'])+'</p><p class="muted">'+H(sh['hypothesis'])+'</p><dl><dt>원본 참조</dt><dd>'+H(sh['reference'])+'</dd><dt>형식</dt><dd>'+H(sh['ratio'])+' · 2K</dd><dt>검수 기준</dt><dd>'+H(sh['checks'])+'</dd></dl><details><summary>영문 프롬프트 보기</summary><pre>'+H(p['params']['prompt'])+'</pre></details></div></article>'
notes=''.join('<li>'+H(x)+'</li>' for x in facts['observations'])
allowed=''.join('<li>'+H(x)+'</li>' for x in facts['claims']['allowed'])
no=' · '.join(facts['claims']['not_used'])
doc='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TAM · 클라우드 블러 제작 근거와 촬영안</title><style>
@font-face{font-family:P;src:url('../../cloud-blush-v3/assets/PretendardVariable.woff2')}*{box-sizing:border-box}body{margin:0;background:#faf8f5;color:#292425;font:17px/1.7 P,sans-serif;word-break:keep-all}a{color:#825066;text-underline-offset:4px}header,main,footer{max-width:1160px;margin:auto;padding:48px 32px}header{padding-top:76px;border-bottom:1px solid #d7ceca}nav{display:flex;gap:22px;flex-wrap:wrap;margin-top:28px}h1{font-size:clamp(36px,5vw,64px);line-height:1.16;letter-spacing:-.045em;max-width:840px;margin:20px 0}h2{font-size:32px;line-height:1.3;letter-spacing:-.03em;margin:0 0 22px}h3{font-size:24px;line-height:1.4;margin:10px 0}p{margin:14px 0}.lead{font-size:22px;max-width:800px}.eyebrow{font-size:13px;letter-spacing:.06em;color:#825066}.muted,small{color:#706767}small{font-size:14px}section{padding:38px 0 54px;border-bottom:1px solid #ded5d0}img{max-width:100%;height:auto;display:block}figure{margin:25px 0}figcaption{font-size:13px;color:#706767;margin-top:10px}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:15px;text-align:left}td,th{padding:16px 14px;border-bottom:1px solid #dfd6d1;vertical-align:top}thead{background:#eee5e1}td small{display:block;margin-top:8px}th{min-width:82px}.two{display:grid;grid-template-columns:1fr 1fr;gap:34px}.comparison{padding:20px 0;border-bottom:1px solid #ded5d0}.comparison h3 small{display:block}ul{padding-left:22px}li{margin:8px 0}.pull{background:#f0e4e3;padding:28px;margin:24px 0;font-size:25px;font-weight:650}.shot{display:grid;grid-template-columns:44% 1fr;gap:36px;padding:32px 0;border-top:1px solid #d7ceca}.shot:has(div:first-child:empty){display:block}.shot img{border-radius:2px}.shot dl{font-size:14px}.shot dt{font-weight:650}.shot dd{margin:0 0 10px}details{margin-top:20px;border-top:1px solid #d7ceca;padding-top:14px}summary{cursor:pointer;min-height:40px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.65 monospace;background:#f0ebe6;padding:18px}.cta{display:inline-block;background:#613b4a;color:#fff;border-radius:2px;padding:12px 22px;text-decoration:none}footer{font-size:13px}strong{font-weight:650}.flow{font-size:20px;line-height:2}.status{font-size:14px;padding:16px 20px;background:#eee8e3}@media(max-width:700px){header,main,footer{padding:30px 20px}header{padding-top:42px}.lead{font-size:18px}h2{font-size:27px}.two,.shot{grid-template-columns:1fr;gap:20px}.shot img{max-height:560px;margin:auto}table{font-size:13px}td,th{padding:12px 8px}section{padding:30px 0}.pull{font-size:22px;padding:22px}.flow{font-size:17px}}@media print{details{display:none}body{background:white}header{padding-top:20px}section{break-inside:avoid}}
</style></head><body><header><p class="eyebrow">TAM BEAUTY · CLOUD BLUR · 2026.10.16</p><h1>예쁜 연출에서<br>구매할 이유로.</h1><p class="lead">올리브영 판매순과 실제 상세 이미지에서 확인한 내용을, 탐뷰티의 문안·사진·순서에 연결한 제작 보드.</p><nav><a class="cta" href="../">수정 상세 시안 보기 ↗</a><a href="#evidence">조사 근거</a><a href="#shots">촬영안·프롬프트</a><a href="#copy">문안 비교</a></nav></header><main>
'''
doc+='<section><p class="eyebrow">제작 방향</p><h2>발림성은 영상으로,<br>마무리는 볼 위에서.</h2><p>'+H(facts['direction'])+'</p><div class="pull">크림처럼 부드럽게,<br>마무리는 보송하게.</div><p>“크림에서 보송함으로”라는 추상적인 문장과 반복되는 컬러 소개를 줄였다. 크림투파우더는 경쟁사에도 있는 제형이므로 독점 기술처럼 쓰지 않는다.</p><p class="status">이 보드는 관찰 사실과 디자인 가설을 구분한다. 순위는 판매량 공개 자료가 아니며, 시안의 구매 전환 효과도 아직 검증되지 않았다.</p></section>'
doc+='<section id="evidence"><p class="eyebrow">01 · 직접 확인한 시장 정보</p><h2>블러셔 카테고리의 판매순.</h2><p><b>'+H(facts['observed_at'])+'</b> · '+H(facts['category'])+' · '+H(facts['sort'])+'</p><p>'+H(facts['scope'])+'</p><a href="'+H(facts['category_url'])+'" target="_blank" rel="noopener">현재 카테고리 열기 ↗</a><figure><img src="oliveyoung-sales-20261016.png" alt="2026년 10월 16일 올리브영 블러셔 판매순 상단 8개 상품 화면" loading="lazy"><figcaption>선택된 판매순과 상단 상품 8개. 화면 속 ‘1등’ 문구는 상품 판매자의 마케팅 표현이며, 여기서 부여한 순위가 아니다.</figcaption></figure><div class="table-wrap"><table><thead><tr><th>표시 순서</th><th>상품</th></tr></thead><tbody>'+top+'</tbody></table></div><ul>'+notes+'</ul></section>'
doc+='<section><p class="eyebrow">02 · 상세 이미지 검토</p><h2>소구 방식과 가져올 원칙.</h2><div class="two">'+comp+'</div><p class="muted">상세 원본 이미지 131개 조각을 내려받아 구성 흐름을 검토했다. 위 내용은 해당 화면의 관찰이며, 경쟁사 성능 주장을 검증하거나 TAM에 적용한 것이 아니다. 리뷰 수는 해당 기획상품에 합산된 표시 수다.</p></section>'
doc+='<section id="shots"><p class="eyebrow">03 · HIGGSFIELD 촬영 기획</p><h2>제품이 주인공인 연출.</h2><p>용기의 라벤더와 내용물의 피치를 기준으로 색을 잡고, 열린 팬·닫힌 로고를 함께 보여준다. 구름 장식·과일·파우더 폭발을 더하는 대신 매트한 면과 부드러운 곡선으로 촉감을 보조한다. 아래 생성 컷은 AI 연출 이미지다.</p><p><a href="higgsfield-prompts.txt" download>3개 촬영안과 영문 프롬프트 내려받기 ↓</a></p>'+shots+'</section>'
doc+='<section id="copy"><p class="eyebrow">04 · 문안 전체 점검</p><h2>정보는 구체적으로,<br>표현은 짧게.</h2><div class="table-wrap"><table><thead><tr><th>구획</th><th>기존</th><th>수정과 이유</th></tr></thead><tbody>'+copy+'</tbody></table></div></section>'
doc+='<section><p class="eyebrow">05 · 실제 상세에 반영한 순서</p><h2>첫 방향의 틀을 유지한다.</h2><p class="flow">제품 연출 A → 실제 제형 영상 → 모아 연출 원본 → 여섯 색 실제 발색 → 사용법 → 비건 포뮬러 → 컬러 선택</p><p>860px 폭·기존 서체·두 열 발색 비교를 유지했다. 모아 사진은 영상과 같은 3:2 크기로 제한한다. 반복되던 마지막 제품 연출 사진은 덜어내고 컬러 선택으로 마친다.</p><p>제형 영상은 밝기를 조정한 기존 R2 파일을 그대로 사용한다. 여러 촬영을 연결한 편집 영상이며, 동일 조건의 전후 실험이 아니다. 생성 제형 컷 C는 이 영상을 대신하지 않는다.</p><a class="cta" href="../">상세 시안 전체 보기 ↗</a></section>'
doc+='<section><p class="eyebrow">06 · 주장과 근거의 범위</p><h2>제품 자료로 말할 수 있는 것.</h2><ul>'+allowed+'</ul><p><a href="https://tambeauty.kr/product/detail.html?product_no=110" target="_blank" rel="noopener">탐뷰티 공식 제품 정보 ↗</a></p><p class="muted">사용하지 않은 주장: '+H(no)+'.</p></section>'
doc+='</main><footer>'+H(facts['publication'])+'<br>검토용 V4 · 소스 조사 '+H(facts['observed_at'])+' · <a href="evidence.json">근거 데이터</a></footer></body></html>'
(D/'index.html').write_text(doc,encoding='utf-8')
print('Built',O)
