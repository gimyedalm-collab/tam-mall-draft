"""Prepare a PRIVATE activation overlay from saved candidate sources; never upload.

App-bearing native templates must remain outside Git. This is not a full skin
archive and is only for the existing, already-integrated skin21 at cutover.
"""
import argparse,hashlib,json,re,shutil,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser()
p.add_argument('--stage',type=Path,required=True)
p.add_argument('--home',type=Path,required=True)
p.add_argument('--home-assets',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
assert not a.output.resolve().is_relative_to(ROOT.resolve()),'Private templates must stay outside Git'
out=a.output;out.mkdir(parents=True,exist_ok=True)
templates={str(x.relative_to(a.stage/'templates')).replace('\\','/'):x.read_text(encoding='utf-8') for x in (a.stage/'templates').rglob('*') if x.is_file()}
templates['index.html']=a.home.read_text(encoding='utf-8')
names=set(re.findall(r'/tam-detail-20261022/(candidate-[\w.-]+\.(?:css|js))','\n'.join(templates.values())))
assets={}
for name in sorted(names):
    source=next((d/name for d in [a.stage,a.home_assets,ROOT/'storefront-v2/cafe24/tam/assets'] if (d/name).is_file()),None)
    # Latest purchase overrides live in the repository, not the older stage files.
    if name.startswith('candidate-purchase-'):source=ROOT/'storefront-v2/cafe24/tam/assets'/name
    assert source and source.is_file(),name
    assets[name]=source.read_text(encoding='utf-8')
renames={n:n.replace('candidate-','rollout-',1) for n in names}
def transform(text):
    # Candidate pathname guards must not disable the representative skin at root.
    text='\n'.join(line for line in text.splitlines() if not ('skin-skin21' in line and line.strip().startswith('if (') and 'return;' in line))
    text=text.replace('/skin-skin21','')
    for old,new in renames.items():text=text.replace(old,new)
    assert 'skin-skin21' not in '\n'.join(line for line in text.splitlines() if not line.strip().startswith(('*','//','/*')))
    return text+'\n'
for path,text in templates.items():
    dest=out/'templates'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(transform(text),encoding='utf-8')
upload=out/'upload';upload.mkdir(exist_ok=True)
for name,text in assets.items():
    if name.startswith('candidate-detail-'):
        text=text.replace('product-25-series-v9.html','rollout-product-25-series-v9.html').replace('product-111-v6.html','rollout-product-111-v6.html').replace('`product-${product}.html`','`rollout-product-${product}.html`')
    (upload/renames[name]).write_text(transform(text),encoding='utf-8')
delivery=ROOT/'ops/cafe24/native-preparation-20261022/delivery'
for number in [24,25,102,109,110,111,118]:
    name='product-25-series-v9.html' if number==25 else 'product-111-v6.html' if number==111 else f'product-{number}.html'
    (upload/('rollout-'+name)).write_text(transform((delivery/name).read_text(encoding='utf-8')),encoding='utf-8')
readme='''# Private Cafe24 activation overlay

PREPARED ONLY. Not uploaded or activated. Not a full skin backup.
Target: existing integrated Korean skin21 (editor27), not a blank/new skin.
Production rollback: Korean skin18. English shop5 skin8 is out of scope.

1. Retain server backups and capture the candidate immediately before cutover.
2. Upload files under upload/ into the existing ROOT /tam-detail-20261022/.
   These rollout filenames are separate from candidate filenames. Verify bytes.
   Existing verified media and home-* assets are dependencies and remain in place.
3. At the agreed cutover, apply templates/ to the integrated candidate only.
   They preserve native module/app code but change candidate URLs to root routes.
4. Activate the intended representative skin, then verify the actual production
   domain: home,14catalog products,7details, native login/cart/options and checkout.
   Confirm coupon/shipping exceptions and payment-return behavior separately.
5. If production verification fails, restore skin18 as representative. Restore
   the pre-cutover candidate templates before returning to preview validation.

This overlay has static pathname/dependency checks only. Production activation,
physical-device QA, real payment, full stock and coupon redemption are unverified.
Never publish this folder/ZIP: native source contains existing private app hooks.
'''
(out/'APPLY-AND-ROLLBACK.md').write_text(readme,encoding='utf-8')
files=[]
for file in sorted(out.rglob('*')):
    if file.is_file() and file.name!='manifest.json':
        files.append({'path':str(file.relative_to(out)).replace('\\','/'),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
manifest={'status':'prepared_only_not_uploaded_or_activated','target':'existing integrated skin21/editor27','rollback':'Korean skin18; English skin8 untouched','full_skin_archive':False,'template_count':len(templates),'upload_count':len(list(upload.iterdir())),'root_route_static_check':True,'production_e2e_verified':False,'files':files}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(out.with_suffix('.zip'),'w',zipfile.ZIP_DEFLATED) as z:
    for file in out.rglob('*'):
        if file.is_file():z.write(file,str(file.relative_to(out)))
print(json.dumps({k:v for k,v in manifest.items() if k!='files'}))
