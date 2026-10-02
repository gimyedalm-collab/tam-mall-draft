"""Package approved vegan detail revisions; preserve all commerce outside detail blocks."""
from pathlib import Path
import hashlib,html,json,re,shutil,sys,subprocess
from PIL import Image

repo=Path(__file__).resolve().parents[2]
source=Path(sys.argv[1])
assets=repo/'storefront-v2/preview/assets'
out=assets/'vegan-details-261002';out.mkdir(exist_ok=True)
records=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
 with Image.open(p) as im:w,h=im.size;frames=getattr(im,'n_frames',1)
 return dict(path=p.relative_to(repo).as_posix(),width=w,height=h,frames=frames,sha256=sha(p),bytes=p.stat().st_size)
def new(p,name):
 dst=out/name;shutil.copy2(p,dst);return dst
def imgs(paths,label):
 tags=[]
 for p in paths:
  v=record(p);records.append(v)
  url=p.relative_to(repo/'storefront-v2/preview').as_posix()
  tags.append(f'<img src="{url}" width="{v["width"]}" height="{v["height"]}" loading="lazy" decoding="async" alt="{label} 상세 {len(tags)+1}"/>')
 return '\n'.join(tags)
def replace_block(no,markup):
 p=repo/f'storefront-v2/preview/product-{no}.html';before=p.read_bytes().decode('utf-8')
 pattern=r'<section\s+class="detail-source container cushion-final-detail".*?</section>'
 old=re.search(pattern,before,re.S);assert old
 after=before[:old.start()]+markup+before[old.end():]
 assert before[:old.start()]==after[:old.start()]
 assert before[old.end():]==after[old.start()+len(markup):]
 p.write_bytes(after.encode('utf-8'))
def section(content,label):
 return f'<section class="detail-source container cushion-final-detail" id="product-detail" data-detail-release="vegan-261002" aria-label="{label} 상세"><h2>제품 상세</h2><div class="detail-images">{content}</div><a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section>'

# Highlighter: approved native HTML; same existing media URLs and frame height.
h=source/'하이라이터_R31';dest=repo/'highlighter-r31';dest.mkdir(exist_ok=True)
for name in ['index.html','product-information.html']:
 t=(h/name).read_text('utf-8').replace('assets/','../highlighter-r30/assets/')
 (dest/name).write_text(t,encoding='utf-8')
t=(dest/'index.html').read_text('utf-8').replace('</head>','<base target="_top"><style>html,body{overflow:hidden}</style></head>')
(dest/'embed.html').write_text(t,encoding='utf-8')
layout=json.loads((h/'layout.json').read_text('utf-8'))
assert sum(s['height'] for s in layout['sections'])==14131
assert '비건 포뮬러의 스틱 하이라이터.' in t
assert t.count('class="animated"')==2
shutil.copy2(h/'layout.json',dest/'layout.json')
p=repo/'storefront-v2/preview/product-24.html';t=p.read_bytes();assert t.count(b'../../highlighter-r30/embed.html')==1
p.write_bytes(t.replace(b'../../highlighter-r30/embed.html',b'../../highlighter-r31/embed.html'))

# Lip liner: replace only four revised static sections; preserve three motions.
l=source/'립라이너_R33';order=json.loads((l/'upload-order.json').read_text('utf-8'));paths=[]
for name in order:
 if name in ['01.png','06.png','07.png','10.png']:p=new(l/'upload'/name,'lipliner-'+name)
 else:
  p=assets/'cloud-plumping-lip-liner-r32'/name
  assert sha(p)==sha(l/'upload'/name),f'Media mismatch: {name}'
 paths.append(p)
replace_block(118,section(imgs(paths,'비건 립 라이너'),'더 클라우드 플럼핑 립 라이너'))

# Cushion: approved header/formula panels and original-strip viewports.
c=source/'쿠션_0908_비건';order=json.loads((c/'upload-order.json').read_text('utf-8'));paths=[]
for rel in order:
 p=c/rel
 if rel.startswith('assets/'):
  n=int(re.search(r'-(\d+)\.',p.name)[1]);dst=assets/'jelly-skin-cushion-0908'/f'{n:02}{p.suffix.lower()}'
  assert sha(dst)==sha(p),f'Media mismatch: {p.name}'
 else:dst=new(p,'cushion-'+p.name)
 paths.append(dst)
replace_block(23,section(imgs(paths,'비건 젤리 스킨 쿠션'),'더 젤리 스킨 쿠션'))

# Structural regression and portable asset references, without browser claims.
checks={'outside_detail_unchanged':{},'missing_files':[],'motion_sections':sum(r['frames']>1 for r in records)}
pat=r'<section\s+class="detail-source container cushion-final-detail".*?</section>'
for no in [23,24,118]:
 rel=f'storefront-v2/preview/product-{no}.html';p=repo/rel
 before=subprocess.check_output(['git','show','HEAD:'+rel],cwd=repo).decode('utf-8');after=p.read_bytes().decode('utf-8')
 if no==24:equal=after.replace('../../highlighter-r31/embed.html','../../highlighter-r30/embed.html')==before
 else:equal=re.sub(pat,'DETAIL',before,flags=re.S)==re.sub(pat,'DETAIL',after,flags=re.S)
 checks['outside_detail_unchanged'][str(no)]=equal;assert equal
for p in [dest/'index.html',dest/'embed.html',dest/'product-information.html',*[repo/f'storefront-v2/preview/product-{n}.html' for n in [23,24,118]]]:
 for url in re.findall(r'(?:src=["\']|url\(["\'])([^"\']+)',p.read_text('utf-8')):
  if url.startswith(('http','data:','/','#')):continue
  if not (p.parent/url.split('?')[0]).exists():checks['missing_files'].append(str(p.relative_to(repo))+':'+url)
assert checks['motion_sections']==6
assert not checks['missing_files'],checks['missing_files']
report={'date':'2026-10-02','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'products':[23,24,118],'source_versions':['cushion 0908 vegan','highlighter R31','lipliner R33'],'checks':checks,'assets':records,'highlighter_motion_count':2,'browser_qa':'not performed','publication':'prepared; awaiting target confirmation','cafe24_production_changed':False}
(repo/'ops/cafe24/vegan-details-261002.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
state=repo/'ops/cafe24/state.json';j=json.loads(state.read_text('utf-8'));j['vegan_details_20261002']={'products':[23,24,118],'status':'prepared','verification':'vegan-details-261002.json','production_cafe24_changed':False};state.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
