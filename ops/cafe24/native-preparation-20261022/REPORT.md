> Current status: [inner-page integration report](../native-inner-20261022/REPORT.md) supersedes the six-detail/inner-pending items below. All7details and inner pages are saved on skin21; production is unchanged.

# Cafe24 candidate integration ? 2026-10-22

Supersedes earlier upload/cart blockers. Candidate skin21 changed; Korean
production skin18 and English shop5 skin8 remain unchanged. Not rollout-ready.

## Completed

- Owner enabled file-URL access; attachment/upload/public retrieval work.
  Owner cleanup verified: test basket empty. No new cart mutation this turn.
- 84 approved detail media uploaded at mall ROOT `/tam-detail-20261022/`.
  All84 pass decoded RGBA/all frames/timing/loop/ICC comparison;44 byte-identical.
  Seven recompressed JPEGs replaced by lossless PNG derivatives preserving
  original pixels and ICC. Masters untouched. See upload-checks-final.json.
- Seven plain HTML fragments uploaded. Candidate bridge connects products
  24,102,109,110,111,118, retaining original detail on load failure. It runs only
  on skin21; shared administrator product descriptions are not replaced.
- Twelve actual Chrome checks at390/1440 pass: six latest details/media counts,
  no overflow, native options and Snap1/3/4/5 placeholders retained. Actual
  Snap review frames observed; no customer/review text exported.
- Native PDP selects16px/48px; shared viewport permits zoom. Separate order-form
  viewport also repaired and verified in public HTML. See candidate-detail-checks.json.
- Approved home saved on skin21. Original V16 plays from GitHub Pages on actual
  Cafe24. Landscape100svh cover, portrait full-width16:9; transparent header
  becomes white on scroll/menu. Legacy guide overlay and320px minimum repaired.
- Native main layout/app imports, Kakao quick menu, Snap1003 and initialization
  retained. Company information uses native footer module. Four prices come
  from native SHOP HTML with product-link fallback. No preview purchase scripts.
- Home passed six Chrome sizes320?1920, menu open/Escape, pause/resume and scroll
  header.23 home assets pass byte/decoded-media comparison.
- Generic Jelly search exposed special repurchase129. Home collection links now
  filter native category74:6Jelly/8Cloud. Native cards/prices/links/sorting and
  load-more observer retained. No shared visibility/stock settings changed.
- Selected original skin18/skin21 HTML captured outside Git. Five imported-head
  integrator tests passed earlier. Server backups exist; no full local archive.

## Commerce evidence and limits

Before changes, native product109/option01:1x18000+3000shipping=21000;
2x18000+0shipping=36000. Order form showed36000. Owner cleaned test cart and
empty basket was confirmed. No order/payment submitted. This baseline does
not establish post-migration transaction verification.

Native macOS Safari26.6.2 run39717312033 PASSED22checks:6home sizes,
12detail/product viewport checks and4collection checks. Home film pause/resume,
menu and scroll header pass; mobile selects16px/48px. Actual home widths are
336,390,768,844,1440,1920. Safari clamps requested320px to336px;320px coverage
comes from Chrome only. Earlier failed runs exposed runner minimum-window,
third-party page-load waiting and navigation/scroll synchronization issues;
final runner uses explicit UI readiness. No website failure was suppressed.
Earlier Safari/throttled-fixture reports cover GitHub preview, not this new
native integration. No physical phone or authenticated device farm available.

## Remaining before production switch

- Product25 includes00gloss plus01?03oils. Oil assets/HTML uploaded; native
  replacement awaits combined composition and SKU/inventory reconciliation.
  Preserve00, SKUs and historical reviews.
- Complete shared shopping/purchase design and order-form mobile accessibility.
- Verify stock/options, coupon redemption/exclusions/expiry, exact shipping
  threshold/exceptions, guest/member checkout and payment return behavior.
- Updated native slow-network and physical iPhone/Android checks.
- Full local backup archive: administrator download dialog remains unreliable.

Raw original skin/admin data and staged media stay outside Git. Only source
builders/scripts and sanitized evidence are versioned.

Post-integration native product109 option01:1x18000; native plus-button gives
2x18000=36000; real keyboard quantity3 gives54000. No cart/order mutation.
Order-form public HTML confirms zoom restriction removed; production skin18
still has its old head and no candidate home marker. See option and production
check JSON files.

Seven uploaded HTML fragments are byte-identical to the delivery folder.
Final Safari evidence: native-safari-report.json; CI run39717312033.
