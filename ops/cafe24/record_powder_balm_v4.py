import hashlib,json,subprocess,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cafe24-delivery-20261020/powder-balm'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
qa_path=ROOT/'ops/cafe24/powder-balm-v4-preview-qa-20261021.json'
qa=json.loads(qa_path.read_text(encoding='utf-8'))
qa['visual_review']='Reviewed 390px full composition, first screen, mid and final GIF frames. Original skin/hand/product sources retained; final face frames unobstructed.'
qa['gif_checks']=[]
for f in OUT.glob('*.gif'):
    with Image.open(f) as im:
        hashes=[];durations=[]
        for n in range(im.n_frames):
            im.seek(n);hashes.append(hashlib.sha256(im.convert('RGB').tobytes()).hexdigest());durations.append(im.info.get('duration',0))
        tail=0
        for h,d in zip(hashes[::-1],durations[::-1]):
            if h!=hashes[-1]:break
            tail+=d
        assert len(set(hashes))>5
        if f.name!='05-puff-and-amount.gif':assert tail>=1000,(f.name,tail)
        qa['gif_checks'].append({'file':f.name,'frames':len(hashes),'duration_ms':sum(durations),'identical_final_hold_ms':tail,'loop':im.info['loop']})
for v in qa['viewports']:
    v['hero_height']=v['images'][0]['height']
    v['first_two_panels_height']=v.pop('heroAndApplicationHeight')
qa['browser_live_view']='Browser extension: 390px local exported page, all seven images loaded, no horizontal overflow beyond client width; scrolled through sections. Separate isolated export QA covers 320/390/430/860/1280.'
dump(qa_path,qa)
manifest_path=OUT/'manifest.json';m=json.loads(manifest_path.read_text(encoding='utf-8'))
m['status']['preview_verified']=True
m['encoding']={'hero_fps':8,'other_gif_fps':10,'palette_colors':256,'dither':'Bayer scale 4','max_asset_bytes':max(x['bytes'] for x in m['media'])}
dump(manifest_path,m)
readme=OUT/'README.txt';readme.write_text(readme.read_text(encoding='utf-8').replace('원본 속도, 10fps','원본 속도, 첫 영상 8fps / 나머지 10fps'),encoding='utf-8')
builder=ROOT/'ops/cafe24/build_powder_balm_v4.py'
builder.write_text(builder.read_text(encoding='utf-8').replace('원본 속도, 10fps','원본 속도, 첫 영상 8fps / 나머지 10fps'),encoding='utf-8')
pack=OUT.parent/'powder-balm-cafe24.zip'
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):
        if f.is_file():z.write(f,f.name)
    assert len(z.namelist())==13
old_info=subprocess.check_output(['git','show','HEAD:cafe24-delivery-20261020/powder-balm/product-information.html'],cwd=ROOT)
assert old_info.replace(b'\r\n',b'\n')==(OUT/'product-information.html').read_bytes().replace(b'\r\n',b'\n')
record={'date':'2026-10-21','version':4,'product_no':111,'request':'Learn competitor section usage and apply appropriate patterns to TAM.','section_study':'powder-balm-v4/section-study.json','source_layout':'powder-balm-v4/layout.html','source_manifest':'powder-balm-v4/source-manifest.json','qa':qa_path.relative_to(ROOT).as_posix(),'preview':'cafe24-delivery-20261020/powder-balm/?v=4','package':'cafe24-delivery-20261020/powder-balm-cafe24.zip','package_bytes':pack.stat().st_size,'package_sha256':sha(pack),'changes':['Large continuous application in hero replaces product-only opening','Full source-speed application through unobstructed finish; final hold','Product and original texture support oil-control plus cosmetic blur','Actual hand amount-adjustment crop plus shaped puff/compact explanation','Compact three-use section with touch-up first'],'native_information_unchanged':True,'status':m['status'],'claim_review':{'supported':'Existing official use areas, oil-control and cosmetic-blur intended benefits, solid format, puff shape, mirror and small-amount tapping method.','not_claimed':'Unchanged foundation, selective removal of only oil, superior absorption vs paper, clinical B/A, duration or competitor-specific ingredients.','limitations':'Source application filming does not establish makeup-retention conditions. No new clinical evidence or performance comparison. GIF format quantization is not physical colour matching.'},'installations':[],'capability_decision':'Existing source photos/footage and export pipeline sufficient. No generated imagery, Blender scene or third-party asset reuse.'}
dump(ROOT/'ops/cafe24/powder-balm-v4-20261021.json',record)
statep=ROOT/'ops/cafe24/state.json';state=json.loads(statep.read_text(encoding='utf-8'))
state['powder_balm_v3_20261021']['status']='superseded_by_owner_authorized_v4'
state['powder_balm_v4_20261021']={'status':'delivery_prepared_preview_verified_owner_acceptance_pending','record':'ops/cafe24/powder-balm-v4-20261021.json','preview':record['preview'],'package':record['package'],'production_changed':False,'next_action':'Owner review of demonstration-led section adaptation. Actual Cafe24 upload and physical-device verification stay deferred.'}
dump(statep,state)
agents=ROOT/'AGENTS.md';note='''

## Powder Balm V4 demonstration-led section adaptation - 2026-10-21

Owner authorized learning competitor sections and applying suitable patterns.
Active source: powder-balm-v4/layout.html; builder ops/cafe24/build_powder_balm_v4.py.
Existing Cafe24 preview/package URL now serves V4. Large continuous cheek-use
hero retains makeup-touch-up copy, includes unobstructed finish and a final hold.
Nose/forehead clips likewise finish without the puff; product/texture support
oil-control and cosmetic blur. Hand-only crop from original detail11 demonstrates
amount adjustment next to the mirror/puff cutout. Three uses remain, touch-up first.
Study: powder-balm-v4/section-study.json. Never transfer competitor efficacy,
retention guarantees, testimonials or before/after claims to TAM. V1-V3 source
and original masters preserved; native facts unchanged. JPG4+GIF3, each<4.9MB,
no custom JS/fonts/video hosting dependency. Hero8fps, other GIF10fps, original
speed, three cycles then holds the final frame. Technical/browser checks are
not owner visual approval, clinical proof or physical colour verification.
Actual Cafe24 upload/save/device verification remain explicitly deferred.
'''
if '## Powder Balm V4 demonstration-led' not in agents.read_text(encoding='utf-8'):
    with agents.open('a',encoding='utf-8') as f:f.write(note)
print(json.dumps({'recorded':True,'package_bytes':pack.stat().st_size,'gif_checks':qa['gif_checks']},ensure_ascii=False))
