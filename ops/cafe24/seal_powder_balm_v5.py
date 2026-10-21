import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cafe24-delivery-20261020/powder-balm'
def dump(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
qa_path=ROOT/'ops/cafe24/powder-balm-v5-preview-qa-20261021.json'
qa=json.loads(qa_path.read_text(encoding='utf-8'))
assert len(qa['viewports'])==5 and qa['source_media_count']==14 and not qa['source_text_and_image_clipping']
qa['visual_review']='Reviewed final 390px full composition and first screen; GIF final skin frame unobstructed. One-compact clarification checked after final copy adjustment. Browser check separately recorded.'
qa['browser_local_first_screen']={'tool':'Browser extension','viewport':390,'client_width':375,'scroll_width':375,'images_loaded':14,'hero_finish':'Puff removed; final skin visible','caption':'실제 사용 장면'}
for v in qa['viewports']:
    if 'heroAndApplicationHeight' in v:v['heading_and_film_height']=v.pop('heroAndApplicationHeight')
dump(qa_path,qa)
m=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
m['status']['preview_verified']=True;dump(OUT/'manifest.json',m)
pack=OUT.parent/'powder-balm-cafe24.zip'
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):
        if f.is_file():z.write(f,f.name)
    assert len(z.namelist())==20
    assert z.testzip() is None
    for name in z.namelist():assert z.read(name)==(OUT/name).read_bytes()
rp=ROOT/'ops/cafe24/powder-balm-v5-20261021.json';r=json.loads(rp.read_text(encoding='utf-8'))
r.update(status=m['status'],qa=qa_path.relative_to(ROOT).as_posix(),package_bytes=pack.stat().st_size,package_sha256=hashlib.sha256(pack.read_bytes()).hexdigest());dump(rp,r)
sp=ROOT/'ops/cafe24/state.json';state=json.loads(sp.read_text(encoding='utf-8'))
state['powder_balm_v4_20261021']['status']='superseded_by_owner_authorized_v5'
state['powder_balm_v5_20261021']={'status':'delivery_prepared_preview_verified_owner_acceptance_pending','record':rp.relative_to(ROOT).as_posix(),'preview':r['preview'],'package':r['package'],'production_changed':False,'next_action':'Owner visual review of image-quality improvement; actual Cafe24 upload and physical-device validation remain deferred.'};dump(sp,state)
print(json.dumps({'sealed':True,'assets':len(m['media']),'package_bytes':pack.stat().st_size}))
