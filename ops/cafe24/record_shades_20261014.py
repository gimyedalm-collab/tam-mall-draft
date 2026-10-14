"""Save sanitized correction and native follow-through status."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
record={
 'status':'preview_mobile_viewports_verified_ready_for_publication',
 'owner_feedback':'Small cropped shade photographs looked poor and mobile/native readiness was unclear.',
 'changes':['Removed all fragmented photographic shade buttons on products 23/112/102','Two-column readable option names and source-backed tone labels','Large comparison dialog using unchanged complete original images, with zoom, keyboard close and focus restoration','Approved cheek article and v16 homepage film preserved'],
 'verification':'shades-qa-20261014.json; 12 isolated Chromium product/viewport combinations at 320/390/430/1440; 25-page DOM suite 152 checks passed',
 'visual_review':'390px screenshots of all three comparison dialogs and option layout reviewed',
 'limits':'Physical iOS/Android devices and authenticated native Cafe24 not tested. Third-party network requests excluded from isolated layout QA.',
 'production_cafe24_changed':False,
 'native_action':'Agent will migrate after owner sign-in, deriving option identity/availability from Cafe24 product_option and retaining native price/cart/order handlers. Static preview catalog/cart must not be used in production.',
 'official_option_reference':'https://sdsupport.cafe24.com/module/product/detail.html'
}
path=ROOT/'ops/cafe24/state.json'
state=json.loads(path.read_text(encoding='utf-8-sig'));state['shade_ui_20261014']=record
path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'ops/cafe24/bugs.json'
bugs=json.loads(path.read_text(encoding='utf-8-sig'))
issue={'id':'TAM-SHADE-CROP-20261014','type':'observed_preview_bug','priority':'P1','status':'fixed_verified_preview','route':'product-23.html / product-112.html / product-102.html','reproduce':'View tiny 4-column shade thumbnails on mobile; SVG viewport fragments show cut labels/background.','expected':'Readable options and faithful, large original colour comparison.','actual':'Owner rejected cropped photo buttons; previous DOM-only QA missed visual defect.','fix':record['changes'],'retest':record['verification'],'evidence':'shades-qa-20261014.json','native_status':'Not yet integrated; owner sign-in needed for agent execution.'}
entries=next(v for v in bugs.values() if isinstance(v,list))
entries[:]=[v for v in entries if v.get('id')!=issue['id']];entries.append(issue)
path.write_text(json.dumps(bugs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
