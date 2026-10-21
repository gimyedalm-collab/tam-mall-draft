"""Finalize measured Cafe24 assets and quality record; never mark live upload done."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cafe24-delivery-20261020/powder-balm'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

# Refresh the final single-compact clarification, including its accessible text.
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={'width':430,'height':900},device_scale_factor=2)
    page.goto((ROOT/'powder-balm-v5/layout.html').as_uri());page.evaluate('document.fonts.ready')
    page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
    section=page.locator('[id="04-balm-and-puff"]')
    section.screenshot(path=str(OUT/'04-balm-and-puff.jpg'),type='jpeg',quality=96)
    alt=' '.join(section.inner_text().split());browser.close()
m=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
oldalt=m['media'][3]['alt']
for name in ['index.html','detail.local.html','detail.cafe24.html']:
    p=OUT/name;p.write_text(p.read_text(encoding='utf-8').replace(oldalt.replace('&','&amp;'),alt.replace('&','&amp;')),encoding='utf-8')
m['media'][3].update(alt=alt,bytes=(OUT/'04-balm-and-puff.jpg').stat().st_size,sha256=sha(OUT/'04-balm-and-puff.jpg'))
m.update(version=5,source_manifest='../../powder-balm-v5/source-manifest.json',media_note='Original-speed continuous final application segments through unobstructed finish, with 2-second hold; three cycles then stays on finish. Typography exported separately at 860px. Hand crop kept at its native pixel width. No Dasha imagery, AI skin, 3D, colour/exposure changes or controlled before/after claim.')
gif_checks=[]
for item in m['media']:
    assert item['sha256']==sha(OUT/item['file'])
    if item['file'].endswith('.gif'):
        with Image.open(OUT/item['file']) as im:
            hashes=[];durations=[]
            for n in range(im.n_frames):
                im.seek(n);hashes.append(hashlib.sha256(im.convert('RGB').tobytes()).hexdigest());durations.append(im.info.get('duration',0))
            hold=0
            for h,d in zip(reversed(hashes),reversed(durations)):
                if h!=hashes[-1]:break
                hold+=d
            assert len(set(hashes))>5 and im.info['loop']==2
            if 'puff' not in item['file']:assert hold>=1900
            gif_checks.append({'file':item['file'],'width':im.width,'frames':im.n_frames,'duration_ms':sum(durations),'final_hold_ms':hold,'loop':im.info['loop']})
old=json.loads(subprocess.check_output(['git','show','HEAD:cafe24-delivery-20261020/powder-balm/manifest.json'],cwd=ROOT))
oldfacts=subprocess.check_output(['git','show','HEAD:cafe24-delivery-20261020/powder-balm/product-information.html'],cwd=ROOT)
assert oldfacts.replace(b'\r\n',b'\n')==(OUT/'product-information.html').read_bytes().replace(b'\r\n',b'\n')
m['encoding']={'hero_fps':8,'other_gif_fps':10,'palette_colors':256,'dither':'Bayer scale 4','static_width':860,'gif_widths':[x['width'] for x in gif_checks],'max_asset_bytes':max(x['bytes'] for x in m['media'])}
m['status']['preview_verified']=False
dump(OUT/'manifest.json',m)
(OUT/'README.txt').write_text('TAM 파우더 밤 · 카페24 등록 준비본 V5\n\n01~14 파일을 번호순으로 사용합니다. PNG 7개 + JPG 4개 + GIF 3개.\nindex.html은 같은 파일·순서·상품정보를 보여주는 미리보기입니다.\n제목·설명·캡션은 860px 정지 이미지로 분리했습니다.\nGIF는 원본 속도, 첫 영상 8fps / 나머지 10fps, 3회 반복 후 마지막 화면에 정지합니다.\n얼굴 영상은 연속된 마지막 도포 구간을 사용하고 퍼프를 뗀 마무리 화면을 2초 유지합니다.\n모든 미디어 파일은 4.9MB 미만입니다.\n\n예정 경로: '+m['delivery_prefix']+'\n실제 Cafe24 업로드·관리자 저장·실기기 검증은 보류 상태입니다.\n제작 완료, 소유자 시각 승인, 실제 업로드는 별도 상태입니다.\n외부 폰트·JavaScript·영상 호스팅이 필요하지 않습니다.\n원본 기록: powder-balm-v5/source-manifest.json\n',encoding='utf-8')
record={'version':5,'date':'2026-10-21','request':'Apply image-quality, visible-finish and product-format improvements on GitHub.','layout':'powder-balm-v5/layout.html','builder':'ops/cafe24/build_powder_balm_v5.py','source_manifest':'powder-balm-v5/source-manifest.json','preview':'cafe24-delivery-20261020/powder-balm/?v=5','package':'cafe24-delivery-20261020/powder-balm-cafe24.zip','changes':['Separate text from GIF into 860px static PNGs','Hero GIF width 480 to 668; nose/forehead 640 to 760; hand panel 640 to 860','Continuous original-speed last application segment with unobstructed finish held 2 seconds','Real open-balm and puff/compact photographs immediately after hero; clarify one compact','Reduce hand display to 160 CSS pixels to avoid enlarging the 320-pixel source crop'],'gif_checks':gif_checks,'quality_limits':['GIF remains 256 colours; no claim of original-video fidelity or physical shade matching','Hero keeps 8fps; shorter source segment makes room for higher spatial resolution','Separate before/after clips inspected but not combined: lighting/angle/exposure controls unverified','No evidence added for guaranteed foundation retention or selective oil-only removal'],'capabilities':'Existing source photography, FFmpeg and raster export pipeline; no installation, synthetic evidence or 3D mockup needed.','native_product_information_unchanged':True,'previous_version':old['version'],'status':m['status']}
dump(ROOT/'ops/cafe24/powder-balm-v5-20261021.json',record)
print(json.dumps({'prepared':True,'gif_checks':gif_checks},ensure_ascii=False))
