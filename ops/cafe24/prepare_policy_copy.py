"""Prepare two factual copy corrections; never save live administrator data."""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(os.environ['TAM_PERF_STAGE'])
notice = '''<section lang="ko" style="max-width:760px;margin:0 auto;padding:24px 16px;color:#262323;font-size:16px;line-height:1.8;word-break:keep-all;overflow-wrap:anywhere;box-sizing:border-box;">
<h2 style="font-size:24px;line-height:1.4;margin:0 0 24px;">회원 혜택 및 쿠폰 이용 안내</h2>
<h3 style="font-size:19px;margin:28px 0 12px;">카카오톡 채널 3,000원 쿠폰</h3>
<p>탐뷰티 카카오톡 채널에서 안내하는 쿠폰을 확인해 주세요.</p>
<ul style="padding-left:22px;">
<li>할인 금액: 3,000원</li>
<li>유효기간: 발급일로부터 365일</li>
<li>최소 주문금액 제한 없이 PC와 모바일에서 사용 가능합니다.</li>
<li>주문 1건당 1장 사용 가능하며, 동일 고객에게 재발급되지 않습니다.</li>
<li>플친 시크릿 파우더 상품과 나무펀 쿠션+글로스 상품은 적용 대상에서 제외됩니다.</li>
</ul>
<p><a href="https://pf.kakao.com/_nxhIxhn" style="color:inherit;text-decoration:underline;">탐뷰티 카카오톡 채널 확인하기</a></p>
<h3 style="font-size:19px;margin:28px 0 12px;">보유 쿠폰 확인</h3>
<p>로그인 후 마이페이지에서 보유 쿠폰과 사용 조건을 확인하실 수 있습니다. 최종 적용 금액은 주문서에서 확인해 주세요.</p>
<p><a href="/myshop/coupon/coupon.html" style="color:inherit;text-decoration:underline;">내 쿠폰 확인하기</a></p>
</section>
'''

before = (ROOT/'exchange-info-before.html').read_text(encoding='utf-8')
assert before.count('배송 기간 : 1일 ~ 7일') == 1
exchange = before.replace('배송 기간 : 1일 ~ 7일', '배송 기간 : 2일 ~ 14일')
assert exchange.count('배송 비용 : 3,000원') == 1
exchange = exchange.replace('배송 비용 : 3,000원', '배송 비용 : 기본 배송비 3,000원 (할인 적용 후 결제금액 30,000원 이상 무료, 상품별 별도 배송비 제외). 최종 배송비는 주문서에서 확인해 주세요.')
(ROOT/'exchange-info-ready.html').write_text(exchange,encoding='utf-8')
(ROOT/'notice-299-ready.html').write_text(notice,encoding='utf-8')
preview = '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>회원 혜택 안내 적용 준비본</title><body style="margin:0;background:#fff;font-family:Arial,sans-serif;">'+notice+'</body></html>'
(ROOT/'notice-299-preview.html').write_text(preview,encoding='utf-8')
items=[]
for name,target in [('exchange-info','shop1 exchange/return HTML setting'),('notice-299','board1 article299 HTML')]:
    items.append({'target':target,'before':name+'-before.html','ready':name+'-ready.html','ready_sha256':hashlib.sha256((ROOT/(name+'-ready.html')).read_bytes()).hexdigest(),'saved_live':False})
manifest={'status':'ready_not_saved_live','notice_title':'회원 혜택 및 쿠폰 이용 안내','scope':'Factual coupon and shipping copy only; no coupon, shipping, returns or member-benefit settings changed. Signup points not independently verified and not represented.','items':items}
(ROOT/'policy-copy-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'prepared':2,'saved_live':False}))
