"""Check public upload bytes/pixels, including every GIF frame and colour metadata."""
import concurrent.futures, hashlib, io, json, urllib.request
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'cafe24-delivery-20261022/powder-balm'
OUT=ROOT/'ops/cafe24/native-powder-20261022'

def check(file):
    raw=file.read_bytes()
    with urllib.request.urlopen('https://awiz.cafe24.com/tam-detail-20261022/'+file.name,timeout=40) as r: downloaded=r.read()
    row={'file':file.name,'bytes_equal':raw==downloaded,'local_bytes':len(raw),'server_bytes':len(downloaded)}
    if file.suffix in ('.png','.jpg','.gif'):
        with Image.open(io.BytesIO(raw)) as a, Image.open(io.BytesIO(downloaded)) as b:
            row.update(local_size=a.size,server_size=b.size,frames=getattr(a,'n_frames',1),
                       icc_equal=a.info.get('icc_profile')==b.info.get('icc_profile'),
                       local_metadata=list(a.info),server_metadata=list(b.info))
            pixels=a.size==b.size and getattr(a,'n_frames',1)==getattr(b,'n_frames',1)
            timing=a.info.get('loop')==b.info.get('loop')
            if pixels:
                for n in range(getattr(a,'n_frames',1)):
                    a.seek(n);b.seek(n)
                    pixels=pixels and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
                    timing=timing and a.info.get('duration')==b.info.get('duration')
            row.update(pixels_equal=pixels,timing_equal=timing)
            row['passed']=pixels and timing and row['icc_equal']
    else: row['passed']=row['bytes_equal']
    return row

files=list(FOLDER.glob('p111-v6-*'))+[ROOT/'ops/cafe24/native-preparation-20261022/delivery/product-111-v6.html',ROOT/'storefront-v2/cafe24/tam/assets/candidate-detail-261022-v3.js',ROOT/'storefront-v2/cafe24/tam/assets/candidate-purchase-261022-v5.css']
with concurrent.futures.ThreadPoolExecutor(4) as pool: rows=list(pool.map(check,files))
OUT.mkdir(exist_ok=True)
(OUT/'upload-checks.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(rows),'passed':sum(r['passed'] for r in rows),'failed':[r for r in rows if not r['passed']]}))
assert all(r['passed'] for r in rows)
