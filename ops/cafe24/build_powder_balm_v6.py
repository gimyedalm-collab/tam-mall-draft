"""Re-export the approved design sharply; preserve original motion and masters."""
import hashlib, json, shutil, zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'cafe24-delivery-20261020/powder-balm'
OUT = ROOT / 'cafe24-delivery-20261022/powder-balm'
PREFIX = '/tam-detail-20261022/'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    old = json.loads((OLD / 'manifest.json').read_text(encoding='utf-8'))
    media = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Render typography and original photographs anew, never enlarge an old panel.
        page = browser.new_page(viewport={'width':430,'height':900}, device_scale_factor=4)
        page.goto((ROOT / 'powder-balm-v5/layout.html').as_uri())
        page.evaluate('document.fonts.ready')
        page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        for item in old['media']:
            source = OLD / item['file']
            motion = source.suffix == '.gif'
            name = 'p111-v6-' + source.stem + ('.gif' if motion else '.png')
            dest = OUT / name
            if motion:
                shutil.copy2(source, dest)
                assert digest(source) == digest(dest)
            else:
                page.locator('[id="'+source.stem+'"]').screenshot(path=str(dest), type='png')
                with Image.open(dest) as im:
                    im.save(dest, optimize=True)
            with Image.open(dest) as im:
                row = {'order':item['order'], 'file':name, 'width':im.width, 'height':im.height,
                       'bytes':dest.stat().st_size,'sha256':digest(dest),'alt':item['alt'],
                       'treatment':'unchanged GIF bytes' if motion else 'new 4x render from editable layout and original photo assets'}
                if motion:
                    row.update(frames=im.n_frames, loop=im.info.get('loop'),
                               duration_ms=sum((im.seek(n) or im.info.get('duration',0)) for n in range(im.n_frames)))
            assert row['bytes'] < 4_900_000, row
            if not motion:
                # Mobile/1x screens reuse the already approved original bytes.
                small = OUT / ('p111-v6-'+source.stem+'-860'+source.suffix)
                shutil.copy2(source, small)
                row['responsive_860']={'file':small.name,'bytes':small.stat().st_size,'sha256':digest(small)}
            media.append(row)
            print(name, row['bytes'], flush=True)
        browser.close()
    facts = (OLD / 'product-information.html').read_text(encoding='utf-8')
    (OUT / 'product-information.html').write_text(facts, encoding='utf-8')
    def fragment(prefix):
        soup = BeautifulSoup('<div data-tam-powder-version="6" style="width:100%;max-width:668px;margin:0 auto;background:#fff;box-sizing:border-box"></div>', 'html.parser')
        root = soup.div
        for m in media:
            tag = soup.new_tag('img', src=prefix+m['file'], width=str(m['width']), height=str(m['height']), alt=m['alt'])
            if 'responsive_860' in m:
                tag['src']=prefix+m['responsive_860']['file']
                tag['srcset']=prefix+m['responsive_860']['file']+' 860w, '+prefix+m['file']+' 1720w'
                tag['sizes']='(max-width:668px) 100vw, 668px'
            # Defeat native width:auto !important, reserve the correct geometry before lazy decode.
            tag['style'] = 'display:block!important;width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:'+str(m['width'])+'/'+str(m['height'])+';border:0;margin:0 auto!important'
            tag['decoding'] = 'async'
            if m['order']==1: tag['fetchpriority']='high'
            else: tag['loading']='lazy'
            root.append(tag)
        root.append(BeautifulSoup(facts, 'html.parser'))
        return str(soup)
    local, native = fragment(''), fragment(PREFIX)
    (OUT/'detail.local.html').write_text(local,encoding='utf-8')
    (OUT/'detail.cafe24.html').write_text(native,encoding='utf-8')
    (OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>파우더 밤 — 선명도 수정본</title><meta name="robots" content="noindex"></head><body style="margin:0;background:#fff">'+local+'</body></html>',encoding='utf-8')
    (ROOT/'ops/cafe24/native-preparation-20261022/delivery/product-111-v6.html').write_text(native,encoding='utf-8')
    preview=ROOT/'storefront-v2/preview/product-111.html'
    doc=BeautifulSoup(preview.read_text(encoding='utf-8'),'html.parser')
    section=doc.select_one('#product-detail'); section.clear()
    section['data-detail-release']='powder-balm-v6'
    section['data-delivery-package']='cafe24-delivery-20261022/powder-balm'
    section.append(BeautifulSoup(fragment('../../cafe24-delivery-20261022/powder-balm/'),'html.parser'))
    preview.write_text(str(doc),encoding='utf-8')
    manifest={'product_no':111,'version':6,'display_max_width':668,'static_width':1720,
              'media':media,'motion_bytes_unchanged':True,'product_information_sha256':digest(OUT/'product-information.html'),
              'source_layout':'powder-balm-v5/layout.html','source_manifest':'powder-balm-v5/source-manifest.json',
              'status':{'prepared':True,'candidate_upload_verified':False,'physical_device_verified':False},
              'limitations':['GIF retains its original palette and frame rate; not original-video fidelity.',
                            'Existing native product gallery remains original photography.']}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'README.txt').write_text('파우더밤 V6 · 14개 파일 순서 유지.\n본문 최대 668px, 정지 패널 1720px 재출력. GIF 3개는 V5와 동일한 원본 바이트.\n기본 등록은 detail.cafe24.html: JPG/PNG/GIF만 사용하며 별도 JavaScript/폰트/영상 호스팅 불필요.\n기존 소스·V5 패키지 보존. 실물 기기와 운영 스킨 검증은 별도.\n',encoding='utf-8')
    with zipfile.ZipFile(OUT.parent/'powder-balm-cafe24-v6.zip','w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(OUT.iterdir()):
            if file.is_file(): z.write(file,file.name)

if __name__=='__main__': main()
