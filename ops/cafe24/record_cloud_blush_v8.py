from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];p=ROOT/'ops/cafe24/state.json';s=json.loads(p.read_text(encoding='utf-8'))
d=s['cafe24_registration_standard_20261019'];d['cloud_reference_assembly_v7_20261020']['status']='superseded_by_owner_closer_design_substitution_v8; not_accepted'
d['cloud_reference_design_v8_20261020']={'status':'reference_design_substitution_assembled_and_verified; owner_acceptance_pending','source':'cloud-blush-v8/index.html','review':'cloud-blush-v8/review/index.html','registration':'cafe24-delivery-20261019/cloud-blush/index.html','plan':'cloud-blush-v8/plan.json','qa':'cloud-blush-v8/qa.json','claude_review':'cloud-blush-v8/claude-review.txt','decisions':'cloud-blush-v8/review-resolution.json','hero':'rebuilt from original product cutouts; earlier preserve-hero preference superseded by latest direction','face_source':'same supplied first revision, cheek-focused CSS crop only','new_AI_generation':False,'physical_shade_verified':False,'cafe24_upload':'deferred_by_owner'}
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'AGENTS.md';p.write_text(p.read_text(encoding='utf-8')+'''\n\n## Cloud reference DESIGN substitution V8 - 2026-10-20

Owner explicitly approves closer Freshian DESIGN substitution, not only section
order, then reducing excess. V7 is superseded. Current source cloud-blush-v8;
comparison cloud-blush-v8/review/; current Cafe24 delivery directory unchanged.
Hero is intentionally rebuilt from three original TAM cutouts; this supersedes
earlier unchanged-hero preference. Large editorial serif headings, 3-column
texture cards, shallow50/50 cheek rows (~740x252 at860), oval How to Use,
check-point connector/frame, and muted TAM surface colours follow the reference.
Cheek crop now centres cheek/nose, all6 supplied first revision; no recolouring.
All right label panels share a neutral background to avoid synthetic shade cues.
New-colour/co-development/tone classifications/77% claims remain omitted.
No new AI images in V8. Existing decorative vegan background reused; product
cutouts retain original colour/logo. Existing GIF footage preserved; How to Use
GIF is padded to match reference margins and border. Native12px facts/INCI
unchanged. Source fonts are rasterized; delivery has no external font/JS/MP4.
Read-only nonpersistent Claude critique and dispositions are recorded. Technical
checks are not owner visual acceptance or physical shade validation. Actual
Cafe24 upload/administrator save/physical-device playback remain deferred.
''',encoding='utf-8')
print('V8 current-state record updated; prior versions preserved.')
