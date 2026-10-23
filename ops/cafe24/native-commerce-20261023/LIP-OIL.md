# Lip oil identity — 2026-10-23

Owner requested a comprehensive review and changing product25 from a lip series
to lip oil. Native Korean product25 now uses **더 젤리 플럼핑 립오일**.

## Applied in Cafe24

- Product25 retains its product ID and all four historical SKU records.
- Korean variant00 P000000Z000O: display off, selling off; not deleted.
- Oil01/02/03 retain P000000Z000P/Q/R, display/selling on, unchanged prices.
- Standalone gloss18 remains available with its existing separate SKU.
- English shop product name and variant visibility/selling are unchanged.
- Existing stock settings, orders, reviews, coupon and shipping policies unchanged.

A complete pre-edit form snapshot is stored privately outside Git. The pre-save
comparison contained exactly three changed controls: Korean product name and
Korean00 visibility/selling. Cafe24 returned “상품이 수정되었습니다.”.
A fresh administrator page confirmed persisted values and all four SKU records.
A fresh candidate product page confirmed the oil title, three selectable codes,
seven approved oil panels and existing Snap review count38.

Installed apps include 이지어드민 이지오토, 배송완료 자동체크, 뱅크다 and Snap.
Installation alone does not prove active inventory synchronization or mappings.
Existing disabled native stock management has not been changed blindly.

## Public preview and production verification

SHOP, ABOUT, Jelly, search and product25 preview names match the native name.
Preview cart/catalog data now contain only the three oil choices. Historical
reviews and source archives are not rewritten. Catalog cache revision refreshed.
Powder package sync now points to V6 and preserves responsive source paths.

Candidate Safari run39892437365 passed50 checks. Candidate Chromium purchase
run39893661237 passed14 alignment and9 purchase-sheet cases, including all three
oil options and their51000KRW combined total at320/390/768/1440px.

Korean production representative skin21 was activated on2026-10-23. Production
Safari run39896577984 passed50 checks. The actual production guest checkout
showed oil01 quantity1, product17000 + shipping3000 =20000KRW, with the new name.
Earlier four-option checkout is historical evidence predating this change.
No payment or new order was submitted. Physical phone/iOS, payment return,
coupon redemption and external inventory reconciliation remain unverified.
See [current rollout report](../production-20261023/REPORT.md) for the final
production Chromium and slow-network evidence and remaining limitations.
