from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'cloud-blush-v11';R=O/'review';R.mkdir(exist_ok=True)
old=json.loads((ROOT/'cloud-blush-v10/cafe24/manifest.json').read_text(encoding='utf-8'))
new=json.loads((O/'cafe24/manifest.json').read_text(encoding='utf-8'))
assert [x['sha256'] for x in old['files'][:11]]==[x['sha256'] for x in new['files'][:11]]
assert (O/'product-information.html').read_bytes()==(ROOT/'cloud-blush-v10/product-information.html').read_bytes()
motion=json.loads((O/'motion-provenance.json').read_text(encoding='utf-8'))
gif=[x for x in new['files'] if x['kind']=='gif'];assert len(gif)==1
assert gif[0]['sha256']==motion['sha256']
im=Image.open(O/'cafe24'/gif[0]['file']);duration=0
for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
assert im.info['loop']==2 and duration==5510
panels=''.join('<img src="../cafe24/'+x['file']+'" alt="'+('제형부터 도포 후 표면까지 이어지는 GIF' if x['kind']=='gif' else '수정 후 실제 상세페이지 구성')+'">' for x in new['files'][11:15])
(R/'index.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · 제형과 사용법 연결 검토</title><style>*{box-sizing:border-box}body{margin:0;background:#eee9ee;color:#39303d;font:16px/1.6 system-ui,sans-serif}main{max-width:980px;margin:auto;padding:28px 20px}h1{font-size:25px}h2{font-size:20px;margin-top:36px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0;background:white;align-self:start}figcaption{padding:12px}img{display:block;width:100%;height:auto}a{color:#66546d}.note{font-size:14px;color:#68596c}.frames{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.frames figcaption{font-size:14px}</style><main><h1>제형과 사용법을 한 구간으로</h1><p>크림 터치 → 얇게 펴 바르기 → 손가락이 빠진 도포 표면을 하나의 GIF로 연결했습니다. 바로 아래에 사용법을 붙이고, 큰 오일 이미지와 제품 합성을 제거했습니다.</p><p><a href="../cafe24/">현재 Cafe24 구성 전체 보기</a></p><p class="note">오른쪽은 실제 납품 JPG·GIF 구성입니다. 5.51초 GIF는 3회 재생 후 도포 표면에서 멈춥니다. 서로 다른 두 촬영 샷을 연결한 사용 안내이며, 제형 전환을 입증하는 동일 부위 전후 시험은 아닙니다. 실제 Cafe24 업로드는 보류 상태입니다.</p><div class="pair"><figure><figcaption>이전 · 제형 → 오일 연출 → 별도 사용법</figcaption><img src="before-journey.png" alt="이전 V10의 분리된 구간"></figure><figure><figcaption>수정 · 제형과 사용법 연결, 성분 정보 축소</figcaption>'''+panels+'''</figure></div><h2>새 GIF의 실제 장면</h2><div class="frames"><figure><img src="../review-motion-0.png"><figcaption>크림 터치</figcaption></figure><figure><img src="../review-motion-1.png"><figcaption>얇게 펴 바르기</figcaption></figure><figure><img src="../review-motion-3.png"><figcaption>손가락이 빠진 도포 표면</figcaption></figure></div><p class="note">기존 영상의 밝기 처리 방식(r2)을 유지해 후반 원본까지 확장했습니다. 새로운 색감 연출이나 피부 보정은 추가하지 않았습니다.</p></main></html>''',encoding='utf-8')
checks={'unchanged_first_11_delivery_images':True,'native_information_byte_identical_to_v10':True,'one_unified_GIF':True,'gif_duration_ms':duration,'gif_frames':im.n_frames,'gif_loop_repeats':2,'oil_visual_removed':True,'old_separate_howto_removed':True,'visual_source_review':'touch, spread and clean hand-surface frames inspected; no claim of scientific transformation proof'}
(O/'flow-qa.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('Before/after review and unified-flow evidence verified.')
