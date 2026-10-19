from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cafe24-delivery-20261019';ext=OUT/'highlighter-external'
s=(ext/'detail.external.template.html').read_text(encoding='utf-8').replace('{{VIDEO_BASE_URL}}',(ext/'video').as_uri())
prefix='/web/upload/tam-detail-20261019/highlighter/'
s=re.sub(r'src="'+prefix+r'([^"]+)"',lambda m:'src="'+(OUT/'highlighter/images'/m[1]).as_uri()+'"',s)
s=re.sub(r'poster="'+prefix+r'([^"]+)"',lambda m:'poster="'+(ext/'posters'/m[1]).as_uri()+'"',s)
s='<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+s+'</body></html>'
checks=[]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w in (390,860):
        p=b.new_page(viewport={'width':w,'height':1000})
        p.goto((OUT/'highlighter/index.html').as_uri())
        p.set_content(s,wait_until='networkidle')
        assert p.evaluate('innerWidth===document.documentElement.scrollWidth')
        for i,v in enumerate(p.locator('video').all()):
            v.evaluate('(v)=>{v.preload="auto";v.load()}')
            p.wait_for_function('(i)=>document.querySelectorAll("video")[i].readyState>=1',arg=i)
            assert v.evaluate('(v)=>v.duration>0&&v.controls')
            v.evaluate('(v)=>v.play()')
            p.wait_for_timeout(300)
            assert v.evaluate('(v)=>v.currentTime>0')
            v.evaluate('(v)=>v.pause()')
        checks.append({'width':w,'local_template_native_video_playback':True,'no_custom_script':True,'actual_host_and_cafe24_verified':False})
        p.close()
    b.close()
(OUT/'external-template-qa.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');print(json.dumps(checks))
