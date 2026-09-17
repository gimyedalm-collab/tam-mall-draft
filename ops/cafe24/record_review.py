import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
path=ROOT/'bugs.json'
data=json.loads(path.read_text(encoding='utf-8'))
items=[
 ('TAM-PREVIEW-006','preview/index.html','Click the home logo from a product or the approved main.','Approved main appears.','Previous home appeared.','Redirect preview entry point to design-only.html.'),
 ('TAM-PREVIEW-007','preview/design-only.html','Return home after adding a preview basket item.','Basket navigation remains available.','No basket link in main navigation.','Add basket link to the existing navigation.'),
 ('TAM-PREVIEW-008','preview/product-23.html','Read all ten detail images.','Can return directly to color selection.','No return link after the long detail.','Add anchored color-selection return link.'),
 ('TAM-PREVIEW-009','preview/assets/purchase-experience.js','Open mobile navigation below the product after popup delay; remove button focus.','Popup stays hidden while menu is open.','Open mobile navigation was absent from popup suppression conditions.','Suppress popup for both menu types; support outside-tap dismissal.')
]
for ident,route,reproduce,expected,actual,fix in items:
    data['items']=[x for x in data['items'] if x['id']!=ident]
    data['items'].append(dict(id=ident,type='preview_bug',priority='P2',status='fixed',route=route,reproduce=reproduce,expected=expected,actual=actual,fix=fix,evidence='OVERALL-REVIEW-20260917.md',retest='check_review_fixes.py: Chromium 1440/390/320 passed; no native commerce verification'))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'state.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['verification']['overall_preview_review']='11 routes at 1440/390/320; navigation/cart/mobile popup fixes tested. See OVERALL-REVIEW-20260917.md. Original 43.8MB detail performance and native commerce remain pending.'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
