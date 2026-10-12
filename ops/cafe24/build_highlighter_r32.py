"""Build the R32 detail from native text, original photos and two short films."""
from pathlib import Path
import base64, copy, html, json, re, shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'highlighter-r32'
OLD = ROOT / 'highlighter-r31'
ASSETS = OUT / 'assets'
OUT.mkdir(exist_ok=True)
base = json.loads((OLD / 'layout.json').read_text('utf-8'))
original = {s['name']: s for s in base['sections']}
sections = []

def section(name, height, bg='#ffffff'):
    s = dict(name=name, width=860, height=height, bg=bg, elements=[])
    sections.append(s)
    return s

def text(s, value, x, y, w=748, size=28, weight=400, color='#1A1A1A', line=None, family='Pretendard', align='left'):
    s['elements'].append(dict(type='text', text=value, x=x, y=y, w=w, size=size, weight=weight, color=color, line=line or round(size*1.5), family=family, align=align, tracking=.045 if family=='Manrope' else -.018))

def photo(s, file, x, y, w, h, alt, crop=None, fit='cover', video=None):
    s['elements'].append(dict(type='image', file=file, x=x, y=y, w=w, h=h, alt=alt, crop=crop, fit=fit, video=video))

def rect(s,x,y,w,h,color):
    s['elements'].append(dict(type='rect', x=x,y=y,w=w,h=h,color=color))

def label(s, value, y, color='#6F6A6B'):
    text(s,value,56,y,size=21,weight=600,color=color,family='Manrope')

hero = copy.deepcopy(original['hero'])
hero_copy = {
    '빛이 닿는 곳에,': '은은한 펄로',
    '입체적인 광채.': '입체적인 광채',
    '세 가지 펄 컬러로 더하는 나만의 광채.\n비건 포뮬러의 스틱 하이라이터.': '부드럽게 펴 발리는 스틱 하이라이터\n비건 포뮬러 · 3가지 컬러',
}
for e in hero['elements']:
    if e.get('text') in hero_copy:
        e['text'] = hero_copy[e['text']]
    if e.get('accent_word'):
        e.pop('accent_word')
    if e.get('text') in ('은은한 펄로', '입체적인 광채'):
        e.update(size=58, line=74, weight=600)
    if e.get('text') == '입체적인 광채':
        e['y'] = 309
    if e.get('emphasis_last_line'):
        e.update(size=30, line=46, y=423)
sections.append(hero)
next(e for e in hero['elements'] if e.get('file')=='product-trio.jpg')['video']='hero-light.mp4'
text(hero,'AI 연출 영상',56,1210,size=18,color='#767074',align='right')

s = section('campaign',1290,'#F2E8E9')
text(s,'움직임을 따라\n섬세하게 빛나는 펄',56,82,size=48,weight=600,line=62)
photo(s,'real-glow-poster.jpg',56,282,748,900,'고개를 돌릴 때 광대의 펄 광택이 보이는 실제 사용 영상',video='real-glow.mp4')
text(s,'각도에 따라 반짝이는 펄이 얼굴에 입체감을 더해줍니다.',56,1210,size=28,color='#625D5F')

s = section('shades',2250)
text(s,'세 가지 컬러,\n다채로운 펄 글로우',56,82,size=48,weight=600,line=62)
text(s,'화이트, 핑크, 골드로 표현하는 세 가지 무드.',56,235,size=30,color='#6F6A6B')
shade_rows=[
    ('01 문스톤','아이시 화이트','tam-moonstone.jpg','맑고 시원하게 빛나는 화이트 펄'),
    ('02 구미 핑크','밀키 핑크','tam-pink.jpg','부드러운 핑크빛으로 더하는 생기'),
    ('03 테디 골드','베이지 골드','tam-gold.jpg','따뜻한 윤기가 감도는 골드 펄'),
]
for i,(name,tone,file,desc) in enumerate(shade_rows):
    y=335+i*590
    text(s,name,56,y,size=34,weight=600,w=370)
    text(s,tone,456,y+4,w=348,size=28,color='#6F6A6B',align='right')
    photo(s,file,56,y+75,748,396,name+' 원본 피부 발색',crop=[150,1550,2550,1350])
    text(s,desc,56,y+495,size=30,color='#6F6A6B')
text(s,'피부 톤과 사용량, 조명에 따라 발색이 다르게 보일 수 있습니다.',56,2160,size=21,color='#767074',line=32)

s=section('texture',650,'#F2F2F2')
text(s,'부드럽게 펴 발리는\n섬세한 펄 텍스처',56,84,size=48,weight=600,line=62)
text(s,'얇게 펴 바를수록 은은하게,\n덧바를수록 더 선명하게.\n원하는 만큼 조절하는 펄감.',56,310,w=400,size=30,line=46,color='#6F6A6B')
photo(s,'tam-pearl-detail-still.jpg',488,250,316,316,'실제 제형의 펄 확대 사진')

s=section('how-to',1190)
label(s,'HOW TO',76)
text(s,'원하는 부위에 가볍게 터치',56,132,size=48,weight=600,line=62)
text(s,'소량씩 바르고, 손끝으로 부드럽게 블렌딩해 주세요.',56,219,size=30,color='#6F6A6B')
photo(s,'howto-touch-261012.jpg',56,305,748,560,'광대에 스틱 하이라이터를 가볍게 바르는 실제 사용 장면',crop=[0,180,1080,809])
text(s,'광대',56,921,w=350,size=34,weight=600)
text(s,'광대 위에 가볍게 바른 뒤\n손끝으로 톡톡 펴 주세요.',56,978,w=360,size=28,line=44,color='#6F6A6B')
text(s,'콧대',450,921,w=354,size=34,weight=600)
text(s,'손끝에 소량을 묻혀\n콧대에 짧게 두드려 주세요.',450,978,w=354,size=28,line=44,color='#6F6A6B')
text(s,'메이크업 위에서는 문지르기보다 소량씩 두드려 사용하세요.',56,1120,size=24,color='#767074')

formula = copy.deepcopy(original['formula'])
formula_copy = {
    '오일과 시어버터를 더한': '보습 성분을 담은',
    '비건 포뮬러.': '비건 포뮬러',
    '세 가지 식물성 오일과 시어버터를 함유했습니다.': '식물성 오일과 시어버터가 함유된 비건 포뮬러.',
    '보습과 피부 컨디셔닝에\n쓰이는 성분을 담았습니다.': '피부 보습을 위한\n오일과 버터의 조합.',
}
for e in formula['elements']:
    if e.get('text') in formula_copy:
        e['text'] = formula_copy[e['text']]
    if e.get('text') in ('보습 성분을 담은', '비건 포뮬러'):
        e.update(size=48, line=62, weight=600)
        e['y'] = 190 if e['text'] == '보습 성분을 담은' else 254
    if e.get('text') == '식물성 오일과 시어버터가 함유된 비건 포뮬러.':
        e.update(size=30, line=46, y=348)
sections.append(formula)
s=section('finish',520,'#F2E8E9')
text(s,'메이크업의 마지막,\n은은한 펄 하이라이팅',56,104,size=48,weight=600,line=62)
rect(s,56,315,748,1,'#D8CED2')
text(s,'3 SHADES',56,361,w=360,size=23,family='Manrope',weight=600)
text(s,'비건 포뮬러 · 9 g',444,357,w=360,size=28,weight=600,color='#925368',align='right')
sections.append(copy.deepcopy(original['information']))

def asset(file):
    return (ASSETS/file) if (ASSETS/file).exists() else ROOT/'highlighter-r30'/'assets'/file

def url(file):
    return 'assets/'+file if (ASSETS/file).exists() else '../highlighter-r30/assets/'+file

def geometry(e):
    with Image.open(asset(e['file'])) as im: sw,sh=im.size
    sx,sy,cw,ch=e.get('crop') or (0,0,sw,sh)
    scale=(min if e.get('fit')=='contain' else max)(e['w']/cw,e['h']/ch)
    return (e['w']-cw*scale)/2-sx*scale,(e['h']-ch*scale)/2-sy*scale,sw*scale,sh*scale

def markup(s):
    out=[f'<section class="sheet" id="{s["name"]}" aria-label="{s["name"]}" style="aspect-ratio:860/{s["height"]};background:{s["bg"]}">']
    for i,e in enumerate(s['elements']):
        pos=f'left:{e["x"]/8.6}%;top:{e["y"]/s["height"]*100}%;width:{e["w"]/8.6}%;'
        if e['type']=='text':
            style=pos+f'font-size:{e["size"]/8.6}cqw;line-height:{e["line"]/e["size"]};font-weight:{e["weight"]};text-align:{e["align"]};color:{e["color"]};font-family:{e["family"]},sans-serif;letter-spacing:{e["tracking"]}em;'
            lines=[html.escape(v) for v in e['text'].splitlines()]
            if e.get('emphasis_last_line'):lines[-1]=f'<strong style="color:#925368;font-weight:600">{lines[-1]}</strong>'
            if e.get('accent_word'):
                lines=[v.replace(e['accent_word'],f'<span style="color:#925368">{e["accent_word"]}</span>') for v in lines]
            content='<br>'.join(lines)
            if e.get('href'):content=f'<a href="{e["href"]}">{content}</a>'
            tag='h1' if s['name']=='hero' and i==0 else 'p'
            out.append(f'<{tag} class="copy" style="{style}">{content}</{tag}>')
        elif e['type']=='image':
            dx,dy,dw,dh=geometry(e)
            imgstyle=f'left:{dx/e["w"]*100}%;top:{dy/e["h"]*100}%;width:{dw/e["w"]*100}%;height:{dh/e["h"]*100}%;'
            frame=pos+f'height:{e["h"]/s["height"]*100}%;'
            if e.get('video'):
                out.append(f'<div class="motion photo" style="{frame}"><video muted loop playsinline preload="none" poster="{url(e["file"])}" data-src="assets/{e["video"]}" aria-label="{html.escape(e["alt"])}" style="{imgstyle}"></video><button class="motion-toggle" type="button" aria-label="영상 재생" aria-pressed="false">재생</button></div>')
            else:out.append(f'<div class="photo" style="{frame}"><img src="{url(e["file"])}" alt="{html.escape(e["alt"])}" loading="lazy" style="{imgstyle}"></div>')
        elif e['type']=='vector':
            out.append(f'<img src="{url(e["file"])}" alt="{html.escape(e["alt"])}" style="{pos}height:{e["h"]/s["height"]*100}%;">')
        else:
            stroke=f'border:{e.get("stroke_width",1)/8.6}cqw solid {e["stroke"]};' if e.get('stroke') else ''
            out.append(f'<div style="{pos}height:{e["h"]/s["height"]*100}%;background:{e["color"]};border-radius:{e.get("radius",0)/8.6}cqw;{stroke}"></div>')
    return '\n'.join(out+['</section>'])

head=(OLD/'index.html').read_text('utf-8').split('<body>')[0]
extra='''<style>.photo video{position:absolute;display:block;max-width:none}.motion-toggle{position:absolute;right:12px;bottom:12px;min-width:52px;min-height:32px;padding:6px 12px;background:rgba(255,255,255,.94);border:1px solid #e4dedf;border-radius:0;font:12px Pretendard,sans-serif;color:#292629;cursor:pointer}.motion-toggle:focus-visible{outline:2px solid #925368;outline-offset:3px}.copy a{color:inherit}</style>'''
head=head.replace('</head>',extra+'</head>')
script='''<script>
const params=new URLSearchParams(location.search);if(params.get('mobile')==='1')document.body.classList.add('mobile');const focus=params.get('focus');if(focus&&document.getElementById(focus)){document.body.dataset.focus=focus;document.getElementById(focus).classList.add('focus');}
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const films=[...document.querySelectorAll('.motion')].map(frame=>({frame,video:frame.querySelector('video'),button:frame.querySelector('button'),visible:false,pausedByUser:false}));
function start(f){if(!f.video.src)f.video.src=f.video.dataset.src;f.video.play().catch(()=>{});}
function sync(f){f.button.textContent=f.video.paused?'재생':'일시정지';f.button.setAttribute('aria-label',f.video.paused?'영상 재생':'영상 일시정지');f.button.setAttribute('aria-pressed',String(!f.video.paused));}
const observer=new IntersectionObserver(entries=>{for(const entry of entries){const f=films.find(x=>x.frame===entry.target);f.visible=entry.isIntersecting;if(f.visible&&!f.pausedByUser&&!reduced.matches&&!document.hidden)start(f);else f.video.pause();}},{threshold:.25});
for(const f of films){observer.observe(f.frame);f.video.addEventListener('play',()=>sync(f));f.video.addEventListener('pause',()=>sync(f));f.button.addEventListener('click',()=>{if(f.video.paused){f.pausedByUser=false;start(f);}else{f.pausedByUser=true;f.video.pause();}});}
document.addEventListener('visibilitychange',()=>films.forEach(f=>{if(document.hidden)f.video.pause();else if(f.visible&&!reduced.matches&&!f.pausedByUser)start(f);}));reduced.addEventListener('change',()=>films.forEach(f=>{if(reduced.matches)f.video.pause();else if(f.visible&&!f.pausedByUser)start(f);}));
</script>'''
page=head+'<body><main>'+''.join(markup(s) for s in sections)+'</main>'+script+'</body></html>'
(OUT/'index.html').write_text(page,'utf-8')
(OUT/'embed.html').write_text(page.replace('</head>','<base target="_top"><style>html,body{overflow:hidden}</style></head>'),'utf-8')
shutil.copy2(OLD/'product-information.html',OUT/'product-information.html')
(OUT/'layout.json').write_text(json.dumps(dict(tokens=base['tokens'],typography=base['typography'],sections=sections),ensure_ascii=False,indent=2),'utf-8')

# Static review export: layout crop only, no changes to the source photographs.
review=ROOT/'ops'/'cafe24'/'runs'/'highlighter-r32'
review.mkdir(parents=True,exist_ok=True)
def svg(s):
    result=[f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{s["height"]}" viewBox="0 0 860 {s["height"]}"><rect width="860" height="{s["height"]}" fill="{s["bg"]}"/>']
    for i,e in enumerate(s['elements']):
        if e['type']=='text':
            align=e['align'];x=e['x']+({'left':0,'center':e['w']/2,'right':e['w']}[align]);anchor={'left':'start','center':'middle','right':'end'}[align]
            for j,line in enumerate(e['text'].splitlines()):
                color='#925368' if e.get('emphasis_last_line') and j==len(e['text'].splitlines())-1 else e['color']
                result.append(f'<text x="{x}" y="{e["y"]+e["size"]+j*e["line"]}" font-family="{e["family"]}" font-size="{e["size"]}" font-weight="{e["weight"]}" fill="{color}" letter-spacing="{e["tracking"]*e["size"]}" text-anchor="{anchor}">{html.escape(line)}</text>')
        elif e['type']=='image':
            dx,dy,dw,dh=geometry(e);p=asset(e['file']);mime='image/'+('jpeg' if p.suffix=='.jpg' else p.suffix[1:]);data=base64.b64encode(p.read_bytes()).decode()
            result.append(f'<defs><clipPath id="c{i}"><rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}"/></clipPath></defs><image href="data:{mime};base64,{data}" x="{e["x"]+dx}" y="{e["y"]+dy}" width="{dw}" height="{dh}" clip-path="url(#c{i})"/>')
        elif e['type']=='rect':result.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}" rx="{e.get("radius",0)}" fill="{e["color"]}" stroke="{e.get("stroke","none")}"/>')
    return ''.join(result+['</svg>'])
for s in sections:(review/(s['name']+'.svg')).write_text(svg(s),'utf-8')
total=sum(s['height'] for s in sections)
product=ROOT/'storefront-v2/preview/product-24.html'
before=product.read_text('utf-8')
after=before.replace('../../highlighter-r31/embed.html','../../highlighter-r32/embed.html')
product.write_text(after,'utf-8',newline='\n')
css=ROOT/'storefront-v2/preview/assets/highlighter-final-detail.css'
value=css.read_text('utf-8');value=re.sub(r'aspect-ratio:860/\d+',f'aspect-ratio:860/{total}',value).replace('Approved R30 artwork','R32 highlighter detail')
css.write_text(value,'utf-8',newline='\n')
print(json.dumps({'height':total,'sections':[(s['name'],s['height']) for s in sections]},ensure_ascii=False))
