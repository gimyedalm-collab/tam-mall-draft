from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cloud-blush-v13';p=ROOT/'ops/cafe24/state.json'
s=json.loads(p.read_text(encoding='utf-8'));d=s['cafe24_registration_standard_20261019']
d['cloud_copy_type_v12_20261021']['status']='archived_baseline; V13 adds one purchase-reason panel, existing media preserved'
d['cloud_purchase_reason_v13_20261021']={'status':'package_verified; owner_visual_acceptance_pending','source':'cloud-blush-v13/index.html','review':'cloud-blush-v13/review/index.html','registration':'cafe24-delivery-20261019/cloud-blush/index.html','plan':'cloud-blush-v13/plan.json','qa':'cloud-blush-v13/qa.json','changes':'One three-point method/feel/finish benefit section after intro, before palette; Ririmew structure adapted to verified TAM claims','preserved':'All17 previous media byte-identical, native information unchanged','new_media':'One static JPG text panel; no new product/shade photo, AI generation or video','claude':'Nonpersistent read-only planning critique, then visual critique','conversion_uplift_verified':False,'cafe24_upload':'deferred_by_owner'}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'AGENTS.md';entry='''

## Cloud V13 purchase-reason section - 2026-10-21

Owner says the page does not explain why to buy and asks to adopt a suitable
reference section, explicitly continuing now with Claude analysis. Current
source cloud-blush-v13; review cloud-blush-v13/review; delivery URL unchanged.
Add one compact three-point section between product introduction and palette:
method (fingertip use), feel (light melting cream), finish (soft powder/blur
makeup). Structure comes from Ririmew's official POINT01–03 before COLORS;
claims come only from TAM's official usage, melting-texture brand material,
Soft-Focus Blur makeup positioning and owner's cream-to-powder brief. Do not
transfer competitor glow, quantified efficacy, clinical smoothing or wear.
This insertion supersedes older 'no new USP section' limitations. Existing
17 JPG/GIF media and native information are byte-identical to latest V12;
one400CSS-px text panel added (title24,point18,support15). No repeated image,
new model photo, synthetic shade/finish, extra FAQ or page-wide reorder.
Planning and visual Claude critiques use nonpersistent read-only CLI. Claiming
conversion improvement or actual Cafe24 integration remains unsupported.
Owner visual acceptance and physical shade matching stay separate from QA;
actual Cafe24 upload/save/device verification remains deferred.
'''
if '## Cloud V13 purchase-reason section' not in p.read_text(encoding='utf-8'):
    p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8')
m=json.loads((OUT/'cafe24/manifest.json').read_text(encoding='utf-8'))
(OUT/'output-manifest.json').write_text(json.dumps({'delivery_directory':'cafe24','preview':'cafe24/index.html','upload_html':'cafe24/detail.cafe24.html','zip':'cloud-blush-cafe24.zip','source_master':'index.html','review':'review/index.html','media':[{'file':'cafe24/'+f['file'],'sha256':f['sha256']} for f in m['files']],'cafe24_upload':'deferred','owner_visual_acceptance':'pending'},indent=2),encoding='utf-8')
print('V13 records saved.')
