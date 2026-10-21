from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];p=ROOT/'ops/cafe24/state.json'
s=json.loads(p.read_text(encoding='utf-8'));d=s['cafe24_registration_standard_20261019']
d['cloud_mobile_refinement_v10_20261020']['status']='archived_baseline; owner_requested_unified_texture_usage_v11'
d['cloud_texture_usage_v11_20261021']={'status':'package_verified; owner_visual_acceptance_pending','source':'cloud-blush-v11/index.html','review':'cloud-blush-v11/review/index.html','registration':'cafe24-delivery-20261019/cloud-blush/index.html','plan':'cloud-blush-v11/plan.json','qa':'cloud-blush-v11/qa.json','flow_qa':'cloud-blush-v11/flow-qa.json','motion_provenance':'cloud-blush-v11/motion-provenance.json','changes':'One cream-touch/spread/applied-surface GIF with use instructions; remove oil image and product overlay, integrate concise oil information','preserved':'First11 delivery images byte-identical to V10; native product information byte-identical','motion':'5.51sec,640x359,8fps,3cycles; extend original V24 to finger-exit surface using same established r2 brightness recipe','new_AI_generation':False,'physical_shade_verified':False,'cafe24_upload':'deferred_by_owner'}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'AGENTS.md';entry='''

## Cloud V11 unified texture and usage - 2026-10-21

Owner says cream-to-powder is not apparent and explicitly asks to join texture
and thin-application into one flow; dislikes oil/product composite. Current
source cloud-blush-v11; comparison cloud-blush-v11/review; delivery URL unchanged.
This supersedes only the older separation/order of texture, oil and How to Use.
One5.51s GIF uses cream touch and original V24 hand spreading through finger exit,
then holds the actual applied surface. Existing r2 treatment retained: baked
master for touch, established V24 luma1.3 recipe for extended later source frames.
No new creative colour grade or synthetic finish. Caption identifies an edit of
actual texture/application shots; it is not a controlled transformation test.
Use instructions follow immediately; short oil facts remain within same section.
Oil visual and product overlay removed. First11 delivery images, six cheek/wrist
swatches and native12px information are byte-identical to V10. Package16JPG+1GIF,
noMP4/JS/font dependencies; GIF3cycles then stops. Read-only nonpersistent Claude
critique and dispositions recorded. Owner approval/physical colour and Cafe24
upload/save/device checks remain distinct, with actual upload explicitly deferred.
'''
if '## Cloud V11 unified texture and usage' not in p.read_text(encoding='utf-8'):
    p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8')
print('V11 project state recorded.')
