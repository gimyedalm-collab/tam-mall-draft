# Cafe24 production rollout — 2026-10-23

The Korean production storefront at https://tambeauty.kr/ now uses skin21
(editor27). This is an actual Cafe24 representative-skin activation. The owner
authorized the full rollout, superseding the earlier deferred-upload scope.
GitHub main and Pages also contain the corresponding preview and public assets.

## Applied

- Approved full-width home film and transparent-to-solid header; SHOP, ABOUT,
  LOOKBOOK, shared navigation, responsive native pages and seven current details.
- Centered detail content and native purchase sheet; product111 powder image
  sizing and responsive static sources. Original GIF files and masters retained.
- Product25 Korean name: **더 젤리 플럼핑 립오일**. Only oil01/02/03 are selectable,
  retaining SKU P000000Z000P/Q/R. Historical gloss00 SKU P000000Z000O remains in
  the database with Korean display/selling off. Standalone gloss18 remains.
- Seven approved oil panels; no added series explanation or gloss introduction.
- Nine root-route templates saved and read back;15 uploaded rollout assets
  verified against public bytes. Private original templates stay outside Git.
- Twelve rendered LOOKBOOK archive images now load lazily. Their source URLs,
  original board links and visible content are preserved.

Previous production skin18 and rollback copy22 are retained. Candidate copy23
was created before the root-route cutover. English shop5 skin8 and its product
names/options are unchanged. No customer notification was sent.

## Verification

- Production Apple Safari26.6.2 on macOS VM: **50 checks passed**, comprising
  6 home,14 detail,4 collection and26 inner-page checks. Run39896577984.
  Browser language ko-KR was verified. This is not physical iPhone/iOS testing.
- Production Chromium run39896575018: **10 structural scenarios (58 assertions),9 slow-network
  scenarios,14 detail-alignment checks and9 purchase flows passed**. Purchase
  flows cover320/390/768/1440px, three oil codes/51000KRW total, selection
  retention and keyboard focus. Slow tests use1.6Mbps/150ms with cache disabled.
- Actual production native guest order form: oil01 quantity1, correct new name,
  product17000 + shipping3000 = **20000KRW**. No personal data, payment details,
  agreement acceptance, payment submission or new order was entered.
- Prior authenticated administrator inspection confirmed product codes and an
  existing oil order's option quantities, Inicis payment and courier/tracking
  display. This does not substitute for a new end-to-end paid test.
- GitHub Pages product25 HTML matches the local final preview after newline
  normalization; seven approved oil image hashes/order remain unchanged.

The first production CI attempts39895697388/39895700224 are retained. Their
English browser locale caused Cafe24's existing language routing to open the
English store from the Korean root. Tests were rerun with ko-KR; no merchant
language-routing settings were changed. The first Chromium purchase attempt
also timed out navigating product102; the final production retry passed all14
alignment routes and9purchase flows without changing its navigation timeout.

## Performance and limits

Functional slow-network success is not a speed-target pass. Shell readiness
means DOMContentLoaded plus required styles, not LCP. Native apps and analytics
remain enabled; no artificial request blocking is used.

| Route | Width | Shell seconds | Interaction seconds |
| --- | ---: | ---: | ---: |
| / | 390 | 21.31 | 24.75 |
| product/list.html?cate_no=74 | 390 | 14.24 | 14.41 |
| about.html | 390 | 11.92 | 13.22 |
| board/gallery/list.html?board_no=8 | 390 | 35.13 | 35.13 |
| product/detail.html?product_no=109 | 390 | 28.04 | 28.83 |
| product/detail.html?product_no=25 | 390 | 21.84 | 23.13 |
| product/list.html?cate_no=74 | 1440 | 14.92 | 15.02 |
| about.html | 1440 | 11.76 | 13.05 |
| product/list.html?cate_no=74 | 320 | 14.8 | 14.9 |

LOOKBOOK previously measured36.41s and4526564 observed encoded bytes on the
candidate. The final production measurement is35.13s and4187663bytes. This single
comparison is not a controlled benchmark or proof of overall speed completion.

A reversible local Gifsicle tool was installed and verified for lossless GIF
optimization (npm gifsicle7.0.1 MIT wrapper, bundled Gifsicle1.93 Windows binary
under GPL-2.0). It is a local tool only, not a storefront runtime dependency.
Three powder GIFs retained the coalesced rendered RGBA/timing/loop/ICC timeline,
but savings were only2.03–5.47%; these experimental files were not uploaded.
Original delivery GIFs remain unchanged, preserving approved shade/texture.

Still unverified: physical iPhone/Android, a new paid order through payment
return and administrator receipt/refund, coupon redemption/expiry/exclusions,
address-dependent shipping exceptions and external warehouse reconciliation.
Native stock management for the lip variants was already disabled and remains
unchanged. Automatic stock deduction or stockout protection is not established.
The installed external inventory app alone is not proof of working mappings.

The production guest checkout is available to the owner for the proposed
20000KRW paid test followed by cancellation/refund. Test terms are pending;
no payment is authorized merely by elapsed time or a general rollout request.
Earlier original guest-basket cleanup could not be proven across authentication;
do not clear unrelated basket lines. No test order currently exists.

Other previously recorded business-policy questions remain in bugs.json,
including legacy benefit-copy mismatch and special-product search visibility.
Do not describe this rollout as complete verification of every commercial rule.
