"""Connect the reviewed V9 cheek detail, preserving all surrounding commerce."""
from pathlib import Path
from PIL import Image
import sys,json,hashlib,re,shutil
repo=Path(__file__).resolve().parents[2];src=Path(sys.argv[1]);dest=repo/'storefront-v2/preview/assets/milky-cheek-v9';dest.mkdir(exist_ok=True)
order=json.loads((src/'output/upload-order.json').read_text('utf-8'));tags=[];records=[]
for i,row in enumerate(order,1):
 p=src/row['file'];name=f'{i:02d}{p.suffix}';target=dest/name;shutil.copy2(p,target)
 with Image.open(target) as im:w,h=im.size;frames=getattr(im,'n_frames',1)
 records.append(dict(file=name,width=w,height=h,frames=frames,sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
 tags.append(f'<img src="assets/milky-cheek-v9/{name}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="물풀치크 비건 상세 {i}"'+(' class="cheek-motion"' if row['motion'] else '')+'>')
 if row['motion']:
  shutil.copy2(src/row['poster'],dest/'use-poster.png')
  tags.append(f'<img class="cheek-still" src="assets/milky-cheek-v9/use-poster.png" width="{w}" height="{h}" alt="물풀치크 사용법 정지 화면">')
section='<section class="detail-source container cushion-final-detail" id="product-detail" data-detail-release="cheek-v9" aria-label="물풀치크 제품 상세"><h2>제품 상세</h2><div class="detail-images">'+''.join(tags)+'</div><a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section>'
p=repo/'storefront-v2/preview/product-102.html';before=p.read_bytes().decode('utf-8');pat=r'<details class="detail-source container">.*?</details>'
assert len(re.findall(pat,before,re.S))==1
after=re.sub(pat,lambda _:section,before,count=1,flags=re.S)
css='<link rel="stylesheet" href="assets/cushion-final-detail.css"><style>.cheek-still{display:none!important}@media(prefers-reduced-motion:reduce){.cheek-motion{display:none!important}.cheek-still{display:block!important}}</style>'
after=after.replace('</head>',css+'</head>',1).replace('class="preview-options" data-preview-product="102"','class="preview-options" id="purchase-options" data-preview-product="102"',1)
restored=after.replace(css,'').replace('class="preview-options" id="purchase-options" data-preview-product="102"','class="preview-options" data-preview-product="102"').replace(section,re.search(pat,before,re.S)[0])
assert restored==before
p.write_bytes(after.encode('utf-8'))
report={'source_version':'V9','product_no':102,'scope':'Reviewed V8 with original Real Colors/Color Chart replacing colour board','outside_detail_unchanged_except_style_and_purchase_anchor':True,'sections':records,'motion_count':sum(r['frames']>1 for r in records),'source':json.loads((src/'provenance.json').read_text('utf-8')),'production_cafe24_changed':False}
assert report['motion_count']==1
(repo/'ops/cafe24/cheek-detail-v9.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=repo/'ops/cafe24/state.json';j=json.loads(p.read_text('utf-8'));j['cheek_v9_20261002']={'status':'github_publish_prepared','product_no':102,'real_chart':'Original brand-provided Real Colors and Color Chart used without recolouring.','verification':'cheek-detail-v9.json','production_cafe24_changed':False};p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Cheek V9: 7 strips, one original motion; commerce preserved.')
