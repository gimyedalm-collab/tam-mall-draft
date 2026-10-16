"""Apply the decisions frozen in cloud-blush-v3-direction-20261016.md."""
from pathlib import Path
import re,shutil
r=Path(__file__).resolve().parents[2]
v1=r/'cloud-blush-v1';v2=r/'cloud-blush-v2';o=r/'cloud-blush-v3';a=o/'assets'
a.mkdir(parents=True,exist_ok=True)
for f in (v2/'assets').iterdir():
    if f.name!='hero-cloud.jpg':shutil.copyfile(f,a/f.name)
shutil.copyfile(r/'cloud-blush-review/assets/P05.jpg',a/'hero-product.jpg')
s=(v2/'detail.template.html').read_text(encoding='utf8')
s=s.replace('크림처럼 부드럽게,<br>파우더처럼 보송하게.','부드럽게 물드는<br>보송한 블러 컬러.')
s=s.replace('부드럽게 펴 바르고, 보송하게 마무리하는<br>여섯 가지 블러 컬러.','나의 볼에 더하는<br>여섯 가지 쉐이크 컬러.')
s=s.replace('assets/hero-cloud.jpg','assets/hero-product.jpg').replace('구름과 하늘 배경 위 클라우드 크림 블러셔 세 가지 제품','중성 배경 위 라벤더 용기의 크림 블러셔 두 가지 컬러')
s=s.replace('바를 땐 크림,<br>마무리는 보송.','크림에서 보송함으로.')
s=re.sub(r'\s*<ol class="texture-stages".*?</ol>','',s,flags=re.S)
s=s.replace('손끝으로 부드럽게 펴 바르면<br>볼 위에 파우더리하게 마무리돼요.','부드럽게 펴 발리는 크림이<br>볼 위에서는 파우더리하게 마무리돼요.')
s=s.replace('여섯 가지<br>쉐이크 컬러.','나의 볼에 어울리는<br>여섯 가지 쉐이크 컬러.')
s=s.replace('피치부터 베리, 살구까지.<br>내게 어울리는 색을 찾아보세요.','볼 위의 발색과 제형을<br>함께 비교해 보세요.')
s=s.replace('조금씩, 톡톡.<br>원하는 만큼 생기 있게.','소량으로 시작해,<br>원하는 색감만큼.')
s=s.replace('식물성 오일을 담은<br>비건 포뮬러.','네 가지 식물성 오일을 담은<br>비건 포뮬러.')
s=s.replace('피치부터 베리까지,<br>내게 어울리는 생기.','오늘의 볼에 어울리는<br>컬러를 골라보세요.')
(o/'detail.template.html').write_text(s,encoding='utf8')
css=(v2/'detail.css').read_text(encoding='utf8')
css+='''
/* V3: shared TAM spacing; product and cheek outrank the model. */
#cloud-blush .texture{padding-bottom:36px}
#cloud-blush .model{padding:0 6.5% 72px;background:#fff}
#cloud-blush .model-photo{aspect-ratio:3/2;border-radius:16px}
#cloud-blush .model-photo img{object-position:50% 0}
#cloud-blush .formula{padding-top:48px;padding-bottom:48px}
#cloud-blush .formula .label{margin-bottom:22px}
#cloud-blush .formula h2{font-size:clamp(23px,4.18cqw,36px);line-height:1.35}
#cloud-blush .formula .ingredients{margin-top:28px;padding-top:24px;gap:26px 20px}
#cloud-blush .formula .ingredients h3{font-size:clamp(15px,2.55cqw,22px)}
#cloud-blush .formula .ingredients p{margin-top:6px}
@container(max-width:600px){#cloud-blush .texture{padding-bottom:30px}#cloud-blush .model{padding:0 5.6% 44px}#cloud-blush .model-photo{border-radius:10px}#cloud-blush .formula{padding-top:36px;padding-bottom:36px}}
'''
(o/'detail.css').write_text(css,encoding='utf8')
js=(v2/'detail.js').read_text(encoding='utf8')
js=js.replace("  const stages = [...document.querySelectorAll('#cloud-blush .texture-stages li')];\n",'')
js=re.sub(r'  const updateStages = .*?\n  \}\);\n','',js,flags=re.S)
js=js.replace("  video.addEventListener('timeupdate', updateStages);\n",'').replace('  updateStages();\n','')
(o/'detail.js').write_text(js,encoding='utf8')
shell='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>탐뷰티 | 더 클라우드 블러 크림 블러셔 · V3</title><meta name="description" content="부드럽게 물드는 보송한 블러 컬러. 크림투파우더 제형과 여섯 가지 쉐이크 컬러를 만나보세요."><link rel="stylesheet" href="detail.css"><script src="detail.js" defer></script></head><body><main>'
(o/'index.html').write_text(shell+s+'</main></body></html>',encoding='utf8')
print(o)
