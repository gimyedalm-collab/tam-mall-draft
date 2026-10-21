"""Add one evidence-grounded purchase-reason block before colour selection."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[2];OLD=ROOT/'cloud-blush-v12';OUT=ROOT/'cloud-blush-v13'
OUT.mkdir(exist_ok=True);(OUT/'assets').mkdir(exist_ok=True);(OUT/'review').mkdir(exist_ok=True)
s=BeautifulSoup((OLD/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
block=BeautifulSoup('''<section id="benefits" class="benefits export-panel" data-ref="Ririmew POINT01–03 structural adaptation"><header class="heading"><h2>손끝으로 완성하는<br>보송한 블러 치크</h2></header><div class="benefit-points"><div class="benefit-point"><div><h3>손끝으로 간편하게</h3><p>손가락으로 얇게 펴 바르고 톡톡.</p></div></div><div class="benefit-point"><div><h3>가볍게 녹아드는 크림</h3><p>피부에 부드럽게 풀리는 멜팅 텍스처.</p></div></div><div class="benefit-point"><div><h3>보송한 블러 마무리</h3><p>보송하고 부드러운 볼 메이크업.</p></div></div></div></section>''','html.parser').section
s.select_one('#palette').insert_before(block)
points=block.select('.benefit-point p')
points[0].string='소량을 얇게 펴 바르고 톡톡.'
points[2].string='크림 투 파우더 포뮬러.'
body=str(s);(OUT/'detail.template.html').write_text(body,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V13 구매 이유 보강</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
css=(OLD/'detail.css').read_text(encoding='utf-8')+'''
/* Method -> feel -> finish. Short supporting copy follows V12 hierarchy. */
.benefits{height:400px;padding:38px 30px 30px;background:#f6f0f5}
.benefits .heading{padding:0}.benefits .heading h2{font-size:24px;line-height:1.4;font-weight:600}
.benefit-points{margin-top:24px;text-align:left}.benefit-point{padding:16px 0;border-top:1px solid #ddd3df}
.point-number{font:500 15px/1.68 Manrope,sans-serif;color:#796a7b}.benefit-point h3{font-size:18px;line-height:1.4;font-weight:600;letter-spacing:-.035em}.benefit-point p{font-size:15px;line-height:1.5;font-weight:400;letter-spacing:-.025em;color:#6a5c68;margin-top:5px}
'''
(OUT/'detail.css').write_text(css,encoding='utf-8')
for f in ['product-information.html','motion-provenance.json','asset-provenance.json']:shutil.copy2(OLD/f,OUT/f)
shutil.copy2(OLD/'assets/cream-spread-finish.gif',OUT/'assets/cream-spread-finish.gif')
# Existing DOM sections are preserved, including single-use source images/GIF.
previous=BeautifulSoup((OLD/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
for sec in previous.select('section[id]'):assert str(sec)==str(s.select_one('#'+sec['id'])),sec['id']
assert len(s.select('.export-panel,.export-motion'))==18
plan={
 'version':13,'objective':'Explain why to choose this cream-to-powder blush before asking the customer to choose a shade.',
 'owner_request':'Still no clear reason to buy; insert a suitable reference section. Continue now and cross-check with Claude.',
 'chosen_structure':'Ririmew official VEIL GLOW CHEEK: three concise benefit points before colour choices. Adapted only method/feel/finish to TAM.',
 'insertion':'After original product introduction/photo, before palette. Existing sequence and images preserved.',
 'copy':{'heading':'손끝으로 완성하는 보송한 블러 치크','points':[{'title':'손끝으로 간편하게','body':'손가락으로 얇게 펴 바르고 톡톡.','basis':'Official TAM usage: fingers or tools, thin application and tapping.'},{'title':'가볍게 녹아드는 크림','body':'피부에 부드럽게 풀리는 멜팅 텍스처.','basis':'Official Korean15.webp says light/fluffy, melting texture. Wording only: source contains excluded Dasha, image not copied into deliverable.'},{'title':'보송한 블러 마무리','body':'보송하고 부드러운 볼 메이크업.','basis':'Owner cream-to-powder brief and official creamblush16_1.png Soft-Focus Blur makeup positioning. Wording only, no model image used.'}]},
 'not_claimed':['Measured pore/wrinkle improvement','Wear duration','No foundation lifting','Unique/better than competitor','Measured conversion or sales uplift','Controlled before-after transformation'],
 'design':{'palette':['#f6f0f5','#39303d','#6a5c68','#ddd3df'],'source_width':430,'section_height':400,'title_px':24,'point_title_px':18,'support_px':15,'images_added':0,'why_text_only':'A compact rest between product photo and colour comparison; no existing image repeated, no synthetic texture evidence.'},
 'claude':'Plan reviewed read-only without session persistence; adopted distinct method/feel/finish and kept original photo/order. Advisory response is not owner acceptance.',
 'limits':'Improves explicit buying rationale; does not prove conversion uplift. Current application GIF is an editorial montage, not controlled finish proof.',
 'cafe24_upload':'deferred_by_owner'}
(OUT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
plan['copy']['points'][0]['body']='소량을 얇게 펴 바르고 톡톡.'
plan['copy']['points'][2]['body']='크림 투 파우더 포뮬러.'
plan['visual_review_repairs']=['Remove point numbers to avoid collision with shade numbers','Remove repeated hand wording','Finish supporting line names cream-to-powder mechanism instead of repeating matte finish','Reduce400px panel height to balance top/bottom whitespace','Keep summary headline intentionally: immediate buying rationale before detail']
(OUT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
evidence={'checked_on':'2026-10-21','references':[{'brand':'Ririmew','url':'https://www.ririmew.com/products/cheek/','observed':'POINT01 transparent colour, POINT02 glow, POINT03 soft texture fit, then COLORS. Official text and mobile rendered layout inspected.','borrowed':'Placement and three short point rows, not product-specific glow/ingredient claims.'},{'brand':'e.l.f.','url':'https://www.elfcosmetics.com/products/putty-blush/','observed':'Official Details links cream-to-powder with feel and application; FAQ asks about tools, layering and amount.','borrowed':'Reasoning from feature to application value; no copied efficacy.'},{'brand':'SHISEIDO','url':'https://brand.shiseido.co.jp/shiseido-minimalist-whipped-powder-blush-4514254085509.html','observed':'Official product introduction describes mousse texture changing to powder and ease of blending.','borrowed':'Useful confirmation that texture should be explained as application/finish, not only a formula name.'}], 'tam_source_claims':[{'file':'C:/Users/BNK-1/Desktop/tam-cloud-blush-20261015/sources/국문/15.webp','observation':'Light fluffy melting texture wording visually read; excluded model image is not delivered.'},{'file':'C:/Users/BNK-1/Desktop/tam-cloud-blush-20261015/sources/국문/creamblush16_1.png','observation':'Soft-Focus Blur makeup positioning visually read; no source photograph or quantified skin smoothing used.'},{'file':'cloud-blush-v12/product-information.html','observation':'Use fingers or tools to spread thinly and tap.'}]}
(OUT/'review/evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print('V13: one benefit section built; all existing sections and assets preserved.')
