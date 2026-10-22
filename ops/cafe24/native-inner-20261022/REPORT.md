# Candidate inner-page integration — 2026-10-22

SHOP, ABOUT, LOOKBOOK and shared navigation/footer are **saved on Cafe24 skin21**
(TEST_260921, editor27). This is an actual candidate integration, not just a
GitHub mockup. Korean production skin18 and English shop5 skin8 remain unchanged.
Implementation commit: ae797b1. This report supersedes the earlier six-detail /
inner-pages-pending status in native-preparation-20261022.

## Implemented

- SHOP uses native category74, 14 actual products, native prices/sorting/purchase
  links, Jelly/Cloud and product-type filters. Cloud + lip returns118/112.
- ABOUT and LOOKBOOK use the approved brand composition and photographs.
  ABOUT's14 product cards obtain native prices. The original board archive is
  retained below the new lookbook. No fabricated reviews or prices were added.
- Search, login, account, coupons, basket, signup, guide and policy pages share
  the new navigation/footer and responsive typography/forms. Native page modules
  remain in place. Separate native checkout receives the common field styling.
- All7 latest details are connected:24,25,102,109,110,111,118. Product25 uses a
  combined00gloss /01–03oil introduction and7 approved oil panels, with a native
  gloss18 link. All4 existing SKUs remain selectable; totals17000/34000/51000/
  68000 were checked without adding to cart or submitting an order.
- Home keeps the approved transparent-to-solid navigation and full-width film:
  landscape100svh cover, portrait16:9. Original V16 footage is unchanged.
- Shared Snap initialization, native commerce/identity modules and footer app
  tails were retained. No shared product price, stock, visibility or policy
  setting was changed. Special repurchase129 remains governed by native search.
- Mobile doubled list margins and navigation wrapping were repaired. Display
  assets now use480/800px product images and960/1600px lookbook images with
  responsive srcset; duplicate hidden hover-image downloads were removed.
  Masters are preserved. These derivatives are not new shade/texture evidence.

## Verification

- [Safari run39729935779](https://github.com/gimyedalm-collab/tam-mall-draft/actions/runs/39729935779):
  **50 passed** on macOS VM Safari26.6.2:6home,14detail,4collection,26inner-page
  checks. This is neither physical iPhone nor iOS Safari. Requested320px clamps
  to336px;320px is covered separately by Chromium/Chrome. Anonymous account routes
  correctly redirect to native login; that is not authenticated account-flow QA.
- [Chromium run39729932685](https://github.com/gimyedalm-collab/tam-mall-draft/actions/runs/39729932685):
  **10 native smoke +9 slow-network scenarios passed**. Cache disabled,1.6Mbps
  download,750Kbps upload,150ms latency, real public Cafe24, no third-party blocking.
  Home menu/video, filters, ABOUT catalog, details, width and visible-image checks.
- Connected Chrome:13inner routes at390/1440,6routes at320 before final image
  optimization; final v4 SHOP/filter/ABOUT/LOOKBOOK/search checks are recorded
  separately. Actual signed-in account/coupon screens received layout checks;
  no personal data was exported and no coupon was redeemed.
-42 uploaded v4 files are reachable:28PNG derivatives have identical decoded
  pixels. The2cushion PNGs lost an embedded standard sRGB profile at Cafe24;
  untagged web display uses sRGB. The strict ICC mismatch report is retained,
  and this exception is explicitly recorded rather than called ICC-identical.
  The12 optimized editorial JPEG derivatives also have identical decoded pixels
  after upload. Earlier full-size JPEG uploads were recompressed; that earlier
  result must not be confused with these final derivatives. Both CSS/JS files
  are byte-identical.
- Earlier failed CI runs are retained in the record: anonymous login redirect
  expectation and an ambiguous filter selector were corrected. No site failure
  was hidden by those corrections.

## Performance and rollout limits

The slow test is a **functional pass, not a speed target pass**. Final measured
shell readiness was14.4–36.2s (DOMContentLoaded + required styles, not LCP).
At390px: SHOP15.1s interaction, ABOUT16.7s catalog, LOOKBOOK36.2s shell,
109detail28.3s,25detail22.4s; home video readiness33.8s. Image payloads are reduced,
but these results do not establish an overall speed improvement. Further native
resource/network profiling is required before declaring performance complete.

Still unverified: physical iPhone/Android, post-change checkout/payment-return
flows, coupon redemption/exclusions/expiry, shipping edge cases and complete stock
reconciliation. Earlier native quantity/shipping/checkout baselines are separate
evidence. No paid order was made. No production representative-skin switch occurred.
Selected originals and app-bearing templates remain outside Git; server backups
exist, but a complete downloaded backup archive has not been verified.

## Review links

- [SHOP](https://awiz.cafe24.com/skin-skin21/product/list.html?cate_no=74)
- [ABOUT](https://awiz.cafe24.com/skin-skin21/about.html)
- [LOOKBOOK](https://awiz.cafe24.com/skin-skin21/board/gallery/list.html?board_no=8)
- [Shading duo109](https://awiz.cafe24.com/skin-skin21/product/detail.html?product_no=109)

No ChatGPT Sites copy was created. GitHub main and the existing Pages deployment
contain the builders, assets and sanitized evidence; private native templates
remain in the local Cafe24 work folder.
