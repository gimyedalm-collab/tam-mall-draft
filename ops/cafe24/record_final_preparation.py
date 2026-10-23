"""Publish sanitized QA evidence; keep native templates and inventory exports private."""
import hashlib,json,os,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PRIVATE=Path(os.environ['TAM_PERF_STAGE'])
OUT=ROOT/'ops/cafe24/final-verification-20261023'
OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

reports={
 'macos-safari.json':'safari/native-safari-verification/report.json',
 'ios-layout.json':'ios-layout/native-ios-simulator-verification/report.json',
 'responsive-images.json':'responsive-images-final/report.json',
 'slow-network.json':'qa-final/report.json',
 'checkout-totals.json':'checkout-final/report.json',
 'smoke.json':'smoke-final.json',
 'policy-copy-qa.json':'policy-copy-qa.json',
 'uploaded-images.json':'upload-verification.json',
}
for dest,source in reports.items():
    data=read(PRIVATE/source)
    if isinstance(data,dict):assert data.get('passed',True),source
    write(OUT/dest,data)

summary={
 'date':'2026-10-23','status':'candidate_saved_application_package_ready_with_explicit_verification_gaps',
 'production_skin':'skin21/editor27','candidate_skin':'skin24/editor30','candidate_name':'TAM_최종검증_20261023',
 'candidate_url':'https://awiz.cafe24.com/skin-skin24/',
 'representative_skin_changed_this_turn':False,'production_rechecked_in_admin':True,
 'saved_templates':['index.html','board/gallery/list.html'],
 'saved_template_readback':'Both equal prepared local files after CRLF normalization.',
 'uploaded_assets':16,'uploaded_pixel_equality':True,
 'color_profile_note':'Cafe24 recompressed PNGs; two cushion PNG profiles stripped. Source profile identified as standard sRGB IEC61966-2.1; decoded RGBA equal. Eight JPEGs byte/pixel/profile equal.',
 'checks':{'macos_safari':50,'ios_simulator_layout':23,'chromium_smoke':10,'responsive_image_cases':6,'slow_comparison_cases':4,'guest_checkout_totals':2,'policy_copy_local_widths':2},
 'runs':{'macos_safari':39903626711,'ios_layout':39906045567},
 'ios':{'runtime':'26.5','device':'iPhone 17 Pro Simulator','viewport_width':402,'layout_passed':True,'physical_device':False,'touch_verified':False,'continuous_film_visual_verified':False,'complete_mobile_verification':False,
 'limitation':'Earlier26.5 trusted pointerdown lacked completed click.26.2 plain HTML button failed independently of store; latest26.2 session failed to connect. No storefront workaround added. Layout-only screenshot is a single frame, not continuous film evidence.'},
 'commerce':{'product_no':25,'name':'더 젤리 플럼핑 립오일','options':['01','02','03'],'native_ids_preserved':True,'native_stock_management':'disabled_unchanged','external_option_mapping':'all_three_admin_confirmed','external_stock':'all_three_positive_at_inspection','external_stock_management':'enabled','connection_flags':'configured_on','new_order_sync_e2e':False,'paid_order':False,'coupon_redemption':False,'refund_return':False},
 'policy_copy':{'ready_files':2,'live_saved':False,'notice299':'Replace outdated image benefit claims with verified channel3000KRW coupon conditions; no unverified signup-point claim.','guide':'Match2-14day period and30000KRW free-shipping threshold with per-product exceptions; remaining return terms preserved.'},
 'limits':['Physical iPhone/Android and iOS touch unverified.','Actual payment, return/refund, coupon redemption, discounted shipping edge cases and new-order inventory/invoice sync unverified.','Slow-network comparison improves transferred image bytes but does not establish Core Web Vitals or universal speed targets. Existing large detail GIFs retain their quality and slow-load limitation.','Special-link catalog/search exposure preserved as pre-existing merchant configuration; no visibility policy changed.','EZAdmin2026-10-22 advisory describes token errors for some EZSyncPlus customers; no token error verified for TAM and no credentials refreshed. Automatic flags do not prove running EZAuto.'],
}
write(OUT/'summary.json',summary)

manifest=read(PRIVATE/'manifest.json')
manifest.update(status=summary['status'],uploaded_assets_verified=16,template_readback_verified=True,production_representative='skin21',representative_changed=False,policy_copy='policy-copy-manifest.json',verification_summary='ops/cafe24/final-verification-20261023/summary.json')
manifest['templates']=[{'path':str(p.relative_to(PRIVATE/'templates')).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((PRIVATE/'templates').rglob('*.html'))]
write(PRIVATE/'manifest.json',manifest)

state_path=ROOT/'ops/cafe24/state.json';state=read(state_path)
state={'final_preparation_20261023':{**summary,'evidence':'final-verification-20261023/REPORT.md','next_action':'Candidate24 and two prepared shared-content corrections are ready for application. Keep physical/payment/sync verification gaps explicit; do not auto-activate under prepare-only request.'},**state}
write(state_path,state)
bugs_path=ROOT/'ops/cafe24/bugs.json';bugs=read(bugs_path)
for item in bugs['items']:
    if item['id']=='TAM-C24-005':
        item.update(status='corrected_copy_prepared_not_live',fix='notice299 replacement HTML matches current channel3000KRW/365day/one-order/two-exclusion configuration; removes stale signup claim without assuming points policy.',retest='Prepared HTML320/1440 passed; admin rules confirmed. Live notice and redemption unchanged.',evidence='final-verification-20261023/REPORT.md')
    if item['id']=='TAM-C24-003':
        item.update(status='corrected_copy_prepared_not_live',fix='Exchange-info HTML period changed1-7to2-14days; shipping states3000KRW/below30000after-discount threshold and individual-product exceptions. Other terms preserved.',retest='Exact prepared diff checked; no shared admin save.',evidence='final-verification-20261023/REPORT.md')
    if item['id']=='TAM-C24-004':
        item.update(status='preexisting_visibility_policy_preserved_unresolved',retest='No migration change to native visibility/search policy. Special-link exposure remains an unresolved merchant-policy decision; not counted as a repaired defect.')
bugs['items']=[i for i in bugs['items'] if i['id']!='TAM-C24-006']
bugs['items'].insert(0,{'id':'TAM-C24-006','type':'performance','priority':'P2','status':'candidate_image_optimization_verified_speed_targets_open','route':'home and lookbook','reproduce':'Compare original mobile image requests on throttled network.','expected':'Appropriate image sizes without loss of product fidelity or layout.','actual':'Large original images used for small mobile cards.','fix':'16 responsive variants, dimensions and archive loading priority in skin24; original masters retained.','retest':'6width/route cases and4throttled comparisons pass. Home final bytes7.11MBto2.84MB; FCP not improved. Existing detailGIF speed remains open.','evidence':'final-verification-20261023/REPORT.md'})
write(bugs_path,bugs)

handoff_path=ROOT/'ops/cafe24/COMPACT-HANDOFF.md'
old=handoff_path.read_text(encoding='utf-8-sig').replace('## ACTIVE: Korean production rollout verified','## HISTORICAL: Korean production rollout verified',1)
prefix='''## ACTIVE: Candidate24 prepared; production21 unchanged this turn — 2026-10-23

Latest owner request is prepare and verify before applying. Do not auto-switch.
Candidate24/editor30 TAM_최종검증_20261023 is a copy of production21 with
two image-only template changes and16 uploaded responsive variants. Readback
matched. Production21 and English8 rechecked unchanged in administrator.
Safari50, iOS Simulator26.5 layout23, Chromium smoke10, responsive images6,
slow comparisons4 and native guest checkout2 passed. iOS touch/physical tests
are NOT complete: plain-button driver baseline failed; separate layout-only
run39906045567 passed. See final-verification-20261023/REPORT.md.
EZAdmin lip01/02/03 mappings and positive stock confirmed; automatic flags on.
No new paid order, coupon redemption, refund, invoice or stock sync E2E.
Two copy corrections (notice299 and exchange-info) are prepared, NOT live-saved.
Private templates/copy/originals/apply instructions are in
C:/Users/BNK-1/.codex/tam-cafe24-output/performance-candidate-20261023.
Paid-test terms still undefined. No identity/payment was entered or submitted.

---

'''
if not old.startswith('## ACTIVE: Candidate24 prepared;'):handoff_path.write_text(prefix+old,encoding='utf-8')
print(json.dumps({'reports':len(reports),'summary':str(OUT/'summary.json'),'private_manifest':True}))
