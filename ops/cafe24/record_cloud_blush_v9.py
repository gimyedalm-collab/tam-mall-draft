from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'ops/cafe24/state.json';s=json.loads(p.read_text(encoding='utf-8'))
d=s['cafe24_registration_standard_20261019']
d['cloud_reference_design_v8_20261020']['status']='reference_geometry_baseline_preserved; typography_refined_in_v9'
d['cloud_typography_refinement_v9_20261020']={
    'status':'package_verified; owner_visual_acceptance_pending',
    'source':'cloud-blush-v9/index.html',
    'review':'cloud-blush-v9/review/index.html',
    'registration':'cafe24-delivery-20261019/cloud-blush/index.html',
    'plan':'cloud-blush-v9/plan.json',
    'qa':'cloud-blush-v9/qa.json',
    'change':'Remove reference-specific serif/italic/halos/chips/oval/frame; TAM sans typography; shorter duplicate copy',
    'preserved':'V8 section order, hero/photo/crop geometry, all source image bytes, two delivery GIF bytes, native information',
    'physical_shade_verified':False,
    'cafe24_upload':'deferred_by_owner'
}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'AGENTS.md'
entry='''

## Cloud V9 typography refinement - 2026-10-20

Owner now asks to remove excess fonts/ornament from V8. Current source is
cloud-blush-v9; before/after review cloud-blush-v9/review; current Cafe24 delivery
path unchanged. V8 reference section order and photo geometry remain; large
Bodoni/italic headings, blur halos, chips, oval how-to, check-point connector
and box are removed. Restore TAM Pretendard Korean / small Manrope English,
with one Korean hierarchy and less repeated colour/texture copy. Original
photo paths, crops, two exported GIF byte hashes and native12px information
are preserved. Six wrist shades and six named face swatches remain present.
Source fonts are rasterized in delivery. Actual Cafe24 upload/save/device
verification remain deferred; owner visual acceptance and physical shade match
are distinct from passed package QA. V8 remains archived as comparison.
'''
if '## Cloud V9 typography refinement' not in p.read_text(encoding='utf-8'):
    p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8')
print('Cloud V9 state recorded.')
