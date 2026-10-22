# Native detail alignment and purchase layout — 2026-10-22

Saved to Korean candidate skin21/editor27. Production skin18 and English
shop5 skin8 remain unchanged. Implementation552111f; CSSv4 and purchase JSv3.

## Changed

- Detailed content is centered at a maximum860px; removed the old430px right
  reservation on its parent. All14catalog products have a measured center error
  below1px. Original hero/gallery images and approved detail media are unchanged.
- Kept the top image/purchase two-column structure and reduced its excessive gap.
  Native purchase buttons are black, basket buttons white, coupon notice neutral
  with a small yellow channel icon. Native payment-provider buttons retain their
  branding and handlers.
- Replaced the permanent right purchase rail with a compact bottom bar opening
  the **same native option/purchase nodes** as a sheet. No cloned cart/checkout.
  Existing options, SKU values, totals, add-ons, Snap and payment containers remain.
- Added a real close button, keyboard activation, focus containment/restoration,
  Escape close, background-scroll lock and hidden-state inert handling.
- Repaired legacy common.js scrollHeaderFixed: it assumed a removed
  `.header__bottom` existed and threw on scroll, preventing later native handlers.
  A guard preserves its legacy behavior when that element actually exists.
  Native detail tab offsets now accept the new navigation height.
- Fixed320px inquiry-button overflow. Coupon banners are hidden only inside the
  opened sheet to keep option selection clear; the top purchase section retains
  the actual channel offer.

## Tests and evidence

- [Safari39738505881](https://github.com/gimyedalm-collab/tam-mall-draft/actions/runs/39738505881):
  **50 checks passed**, including14detail center checks and4purchase-sheet
  open/close/focus checks within the existing suite. macOS VM Safari26.6.2;
  this is not physical iPhone/iOS verification.
- [Chromium purchase39738501598](https://github.com/gimyedalm-collab/tam-mall-draft/actions/runs/39738501598):
  **14product alignment +9purchase flows passed**, final CSSv4 verified by URL.
  Products109/25 at320,390,768,1440; additional109/390 case at1.6Mbps/150ms with
  cache disabled. Native option109 selection gives18000KRW and remains selected
  after close/reopen. Keyboard Escape/Enter and focus return pass. Zero recorded
  script errors in these9flows. No cart/order/payment was submitted.
- [Earlier full Chromium39736645385](https://github.com/gimyedalm-collab/tam-mall-draft/actions/runs/39736645385):
  native smoke10 and slow-network9 passed. Its new purchase step failed and is
  **not** called a passing run: it exposed focus-restoration timing and a test
  measuring against viewport width rather than the body area with a reserved
  scrollbar gutter. Both were corrected; the later targeted run above passed.
- Connected Chrome visual reviews: desktop top purchase area, centered detail,
  sheet;390px shading and320px lip-series sheet. All4native lip options retained;
  actual00gloss selection returned17000KRW without cart mutation.
- Final public CSSv4/JSv3 are byte-identical to local sources. The modified native
  common/detail scripts were read back before save; real scrolling and final
  cross-browser flows establish that the saved scripts run.

## Activation preparation

`prepare_native_activation.py` creates a PRIVATE overlay outside Git:14native
templates plus15upload files and apply/rollback instructions. It removes candidate
pathname guards and changes `/skin-skin21` links/fetches to root paths in a separate
rollout variant, including the25→18gloss link. It does not modify the candidate
preview or upload/activate anything. All generated JS passes syntax checks.

Local package:
`C:/Users/BNK-1/.codex/tam-cafe24-output/activation-20261022.zip`

This is an overlay for the existing integrated skin21, **not a full skin archive**.
Existing verified media and home assets are dependencies. App-bearing native
sources and the ZIP stay outside Git. Only the sanitized manifest is versioned.
Korean skin18 remains the production rollback target; English skin8 is excluded.

The requested layout fixes and activation files are prepared. Production-domain
activation/end-to-end verification, physical phones, real payment returns, coupon
redemption/shipping exceptions and full stock reconciliation are still unverified.
The earlier slow-network functional pass does not resolve the documented long
loading times. Do not describe the entire store as performance/transaction-ready.
