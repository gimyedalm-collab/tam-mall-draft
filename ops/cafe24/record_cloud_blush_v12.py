from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];p=ROOT/'ops/cafe24/state.json'
s=json.loads(p.read_text(encoding='utf-8'));d=s['cafe24_registration_standard_20261019']
d['cloud_texture_usage_v11_20261021']['status']='archived_baseline; owner_requested_oil_restore_copy_type_and_vegan_cleanup'
d['cloud_copy_type_v12_20261021']={'status':'package_verified; owner_visual_acceptance_pending','source':'cloud-blush-v12/index.html','review':'cloud-blush-v12/review/index.html','registration':'cafe24-delivery-20261019/cloud-blush/index.html','plan':'cloud-blush-v12/plan.json','qa':'cloud-blush-v12/qa.json','changes':'Six descriptive shade captions; hero28/section24 source px; restore oil image alone; vegan brand mark without product photo','preserved':'Source shade photos, V11 unified GIF and native information unchanged','vegan_mark':'Brand VEGAN FORMULA typography, not official certification logo; Cloud current certification unverified','physical_shade_verified':False,'cafe24_upload':'deferred_by_owner'}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'AGENTS.md';entry='''

## Cloud V12 copy, type, oil and vegan cleanup - 2026-10-21

Owner says shade descriptions are perfunctory, fonts too large/inconsistent,
vegan section needs only a mark, and oil imagery should return. Current source
cloud-blush-v12; comparison cloud-blush-v12/review; delivery URL unchanged.
This supersedes V10 larger headings and V11 removal of the entire oil image.
Hero28 and all section titles24 source px; shade names18 and captions16.2 retain
mobile readability. Six short descriptive shade captions use supplied image
observations, not measured colour/personal-colour claims. Existing clear oil
illustration returns alone without a product overlay. Vegan plant/product
composite is replaced by botanical VEGAN FORMULA brand typography; this is
not an official certification logo, and current Cloud certification has not
been verified. All original shade images, V11 unified cream/application GIF
and native12px product information/INCI are preserved. Package16JPG+1GIF.
Technical QA and independent critique do not equal owner visual approval or
physical shade matching. Actual Cafe24 upload/save/device checks stay deferred.
'''
if '## Cloud V12 copy, type' not in p.read_text(encoding='utf-8'):
    p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8')
print('V12 state and owner corrections recorded.')
