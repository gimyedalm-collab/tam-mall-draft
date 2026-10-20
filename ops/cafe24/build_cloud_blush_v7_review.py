from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cloud-blush-v7';R=OUT/'review';R.mkdir(exist_ok=True)
p=json.loads((OUT/'plan.json').read_text(encoding='utf-8'))
rows=''.join(f'<tr><td>{r["ref"]}</td><td><b>{r["purpose"]}</b><br>{r["asset"]}</td><td>{r["evidence"]}</td></tr>' for r in p['sections'])
claims=''.join(f'<tr><td>{r["copy"]}</td><td>{r["evidence"]}</td><td>{r.get("limit","자료 내 사실만 사용")}</td></tr>' for r in p['claims'])
exceptions=''.join(f'<li>{x}</li>' for x in p['exceptions'])
doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TAM V7 · 섹션 조립과 근거 검토</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#f4f1f5;color:#302934;font:15px/1.7 Arial,sans-serif}}main{{max-width:1160px;margin:auto;padding:34px 24px}}h1{{font-size:30px;line-height:1.35}}h2{{font-size:23px;margin-top:36px}}p{{max-width:850px}}a{{color:#71516e}}.meta{{background:white;border:1px solid #dfd5e1;padding:18px 22px}}.links{{display:flex;gap:20px;flex-wrap:wrap}}table{{width:100%;border-collapse:collapse;background:white}}td,th{{text-align:left;padding:16px;border-bottom:1px solid #e5dde7;vertical-align:top}}td:first-child{{min-width:80px}}.compare{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}.window{{height:800px;overflow:auto;background:white;border:1px solid #d8cddc}}.window>img{{display:block;width:100%}}iframe{{display:block;width:100%;height:800px;border:0}}.label{{position:sticky;top:0;background:#fff;padding:12px;border-bottom:1px solid #ddd}}.asset{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}}.asset img{{width:100%;display:block}}.asset figure{{margin:0}}small{{font-size:13px}}@media(max-width:700px){{main{{padding:20px 14px}}.compare{{grid-template-columns:1fr}}table{{font-size:13px}}td,th{{padding:10px}}.asset{{grid-template-columns:1fr}}}}</style></head><body><main>
<p>TAM BEAUTY · CLOUD BLUSH · V7 / 2026.10.20</p><h1>레퍼런스 순서대로 조립하고,<br>탐뷰티의 자료로 채웠습니다.</h1>
<div class="meta"><b>카페24 등록 준비본 · 소유자 시각 승인 대기</b><br>얼굴 발색은 제공된 1차 사진 6장입니다. AI 발색·임의 색 보정은 없으며, 실물 색 일치 여부는 미검수입니다.<br>실제 카페24 업로드·관리자 저장·실기기 재생 확인은 요청대로 보류했습니다.</div>
<p class="links"><a href="../cafe24/" target="_blank">카페24 구성 미리보기 ↗</a><a href="../cloud-blush-cafe24.zip">등록 준비 ZIP</a><a href="https://www.freshian.com/product/detail.html?product_no=157" target="_blank">프레시안 공식 원문 ↗</a><a href="../plan.json">기획·문안 근거 기록</a><a href="../qa.json">출력 검증 기록</a></p>
<h2>왜 이 순서인가</h2><p>선정한 프레시안 원본의 제품 소개 → 전체 색 비교 → 개별 얼굴 발색 → 제형 → 성분 → 사용법 → 비건 → 확인사항 흐름을 적용했습니다. 전체 비교는 색의 차이를, 얼굴 사진은 개별 착용 결과를 보여줍니다. 같은 사진을 두 역할에 중복 사용하지 않았습니다.</p>
<table><thead><tr><th>원본 구간</th><th>탐뷰티 적용</th><th>근거</th></tr></thead><tbody>{rows}</tbody></table>
<h2>그대로 가져오지 않은 부분</h2><ul>{exceptions}</ul><p>참고한 것은 순서와 이미지의 역할입니다. 따라서 원본 12개 구간을 모두 똑같이 복제한 상세페이지라고 부르지 않습니다. 타사의 문안·로고·사진은 탐뷰티 판매용 이미지에 넣지 않았습니다.</p>
<h2>원본과 조립본 나란히 보기</h2><p>각 창을 독립적으로 스크롤할 수 있습니다. 오른쪽은 JS·외부 폰트 없이 JPG/GIF와 상품정보 HTML로 구성한 실제 등록 준비본입니다.</p>
<div class="compare"><div><div class="label">프레시안 · 수집 원본 / 비교용</div><div class="window"><img src="../../cloud-blush-v6/review/reference-exact-20261020/reference.jpg" alt="프레시안 공식 제품157 수집 원본 상세페이지" loading="lazy"></div></div><div><div class="label">탐뷰티 V7 · 카페24 구성</div><iframe src="../cafe24/" title="탐뷰티 V7 실제 카페24 준비본"></iframe></div></div>
<h2>이미지와 생성 작업의 범위</h2><div class="asset"><figure><img src="../review-palette-430.png" alt="전체 컬러 비교"><figcaption>손목·제형: 제공 원본 유지. 피부 사진을 한 팔처럼 합성하지 않았습니다.</figcaption></figure><figure><img src="../review-faces-430.png" alt="개별 얼굴 발색"><figcaption>얼굴: 제공 1차 세트 통일. 사진 출처 확인과 실물 색 정확성은 별도입니다.</figcaption></figure><figure><img src="../review-vegan-430.png" alt="비건 제품 연출"><figcaption>신규 디자인: GPT 생성 배경 + 원본 제품 누끼. 제품 색·로고는 생성하지 않았습니다.</figcaption></figure></div>
<h2>문안의 근거와 한계</h2><table><thead><tr><th>문안</th><th>사용 근거</th><th>범위</th></tr></thead><tbody>{claims}</tbody></table>
<h2>검수 상태</h2><p id="qa">320·390·860px에서 이미지 로딩, 가로 넘침, 이미지 사이 틈, JS 비활성 상태를 검사합니다. 전성분은 기존 HTML을 그대로 유지하고 12px로 표시합니다. 두 GIF는 서로 다른 원본 장면이며 각 3회 재생 후 멈춥니다.</p><p><a href="../asset-provenance.json">이미지 원본·변환 기록</a> · <a href="../claude-review.txt">Claude 교차 검토</a></p>
</main></body></html>'''
doc=doc.replace('<a href="../claude-review.txt">Claude 교차 검토</a>','<a href="../claude-review.txt">Claude 교차 검토</a> · <a href="../claude-review-resolution.json">의견별 반영 판단</a>')
(R/'index.html').write_text(doc,encoding='utf-8')
print('V7 evidence and side-by-side review written.')
