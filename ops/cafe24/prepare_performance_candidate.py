"""Prepare image-only changes against the private, deployed template snapshot.

Templates containing native app hooks remain outside Git. No live mutation.
"""
import argparse, hashlib, json, re
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
MEDIA=ROOT/'storefront-v2/preview/assets'
BASE='https://awiz.cafe24.com/tam-detail-20261022/'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    upload=args.output/'upload';upload.mkdir(parents=True,exist_ok=True)
    templates=args.output/'templates';templates.mkdir(exist_ok=True)
    records=[]
    def resized(name,width):
        source=MEDIA/name
        target='perf261023-'+source.stem+f'-{width}'+source.suffix
        if any(r['file']==target for r in records):return BASE+target
        with Image.open(source) as image:
            size=(width,round(image.height*width/image.width))
            result=image.resize(size,Image.Resampling.LANCZOS)
            options={'icc_profile':image.info.get('icc_profile')}
            if source.suffix=='.jpg': options.update(quality=90,optimize=True,progressive=True)
            else: options.update(optimize=True)
            result.save(upload/target,**options)
        records.append({'file':target,'source':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                        'width':size[0],'height':size[1],'bytes':(upload/target).stat().st_size,
                        'sha256':hashlib.sha256((upload/target).read_bytes()).hexdigest()})
        return BASE+target
    home=(args.source/'index.html').read_text(encoding='utf-8')
    for name in ['cushion-pink-original-2.png','retouched-24-v1.png','retouched-111-v1.png','retouched-112-v1.png']:
        small,large=resized(name,480),resized(name,800)
        old='src="'+BASE+'home-'+name+'"'
        assert home.count(old)==1,(name,home.count(old))
        with Image.open(MEDIA/name) as im: original_width=im.width
        # The powder/lip artwork is visually enlarged within its card. Slot
        # widths understated that rendering size and selected blurry sources.
        sizes='(max-width:760px) 90vw, (max-width:1023px) 48vw, 640px' if name in ('retouched-111-v1.png','retouched-112-v1.png') else '(max-width:760px) 52vw, 340px'
        home=home.replace(old,f'src="{large}" srcset="{small} 480w, {large} 800w, {BASE}home-{name} {original_width}w" sizes="{sizes}" fetchpriority="low"')
    # Existing editorial photos use the same source composition with bounded sizes.
    for name in ['lookbook-jelly-1.jpg','lookbook-cloud-1.jpg']:
        small,large=resized(name,480),resized(name,960)
        old='src="'+BASE+'home-'+name+'"'
        assert home.count(old)==1
        with Image.open(MEDIA/name) as im:w,h=im.size
        home=home.replace(old,f'src="{large}" srcset="{small} 480w, {large} 960w, {BASE}inner-{Path(name).stem}-1600.jpg 1600w, {BASE}home-{name} {w}w" sizes="(max-width:760px) 50vw, (max-width:1500px) 48vw, 760px" width="{w}" height="{h}" fetchpriority="low"')
    (templates/'index.html').write_text(home,encoding='utf-8')
    look=(args.source/'board/gallery/list.html').read_text(encoding='utf-8')
    for line in ['jelly','cloud']:
        for number in [1,2,3]:
            name=f'lookbook-{line}-{number}.jpg'; small=resized(name,480)
            old=f'srcset="{BASE}inner-lookbook-{line}-{number}-960.jpg 960w, '
            assert look.count(old)==1
            look=look.replace(old,f'srcset="{small} 480w, {BASE}inner-lookbook-{line}-{number}-960.jpg 960w, ')
    look=look.replace('loading="eager"','loading="eager" fetchpriority="high"')
    # Reserve the square native archive thumbnails before they decode. Missing
    # intrinsic geometry lets off-screen lazy images start during early layout.
    old='<img loading="lazy" decoding="async" src="{$img_src}"'
    assert look.count(old)==6
    look=look.replace(old,'<img loading="lazy" decoding="async" fetchpriority="low" width="1000" height="1000" src="{$img_src}"')
    path=templates/'board/gallery/list.html';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(look,encoding='utf-8')
    # Assert all modifications are image attributes, not native module/app code.
    strip=lambda s:re.sub(r'<img\b[^>]*>','<img>',s)
    for rel in ['index.html','board/gallery/list.html']:
        assert strip((args.source/rel).read_text(encoding='utf-8'))==strip((templates/rel).read_text(encoding='utf-8'))
    manifest={'status':'prepared_only','target_skin':'skin24/editor30','representative_changed':False,
              'source_skin':'skin21','image_attributes_only':True,'assets':records}
    (args.output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'assets':len(records),'unique_files':len(list(upload.iterdir())),'bytes':sum(p.stat().st_size for p in upload.iterdir()),'templates':2}))

if __name__=='__main__':main()
