# Lip series content and native commerce verification

Owner requested removal of added series explanations before rollout, and checks
that the store and administrator can continue handling orders.

## Content changes

- Removed the extra series heading, gloss/oil introduction, product18 link and
  legacy common-information accordion from preview product25.
- Candidate product-25-series-v9.html now contains exactly the existing approved
  seven-panel oil HTML. Original image hashes and order are unchanged.
- Product name, four purchase options, prices and review markup outside the
  detail section are unchanged (exact comparison after newline normalization).
- Updated builders so a later sync does not restore the rejected introduction.
- Refreshed the private activation overlay (14 templates / 15 upload files).
- Cafe24 candidate fragment uploaded and public bytes match (1367 bytes).
  Browser shows seven images, empty added text, status ready, same four SKUs.
  Production is unchanged.

## Actual Cafe24 browser interactions

Tested existing candidate skin21 using the connected Chrome session, not the
GitHub mock checkout. Cart and checkout checks preceded the content upload. After upload, the actual
candidate was rechecked for removed text, seven images and unchanged four SKUs.

| Step | Observed result |
| --- | --- |
| Initial basket | Empty |
| Select 00 gloss | P000000Z000O, quantity1 |
| Select 01 oil | P000000Z000P, quantity1 |
| Select 02 oil | P000000Z000Q, quantity1 |
| Select 03 oil | P000000Z000R, quantity1 |
| Add all four to basket | Four separate correctly named options, 17000 each |
| Basket totals | Products68000, shipping0, total68000 KRW |
| Checkout route | Native login gateway then guest checkout |
| Guest order form | All four correct option names and quantity1 each |
| Checkout total | 68000 KRW, shipping0 |
| Responsive order form | Actual innerWidth390, clientWidth375, scrollWidth375; no horizontal overflow |
| Final payment | Not submitted; no customer details entered or agreements accepted |

The order form visibly offers bank deposit, Kakao Pay, Payco, phone, card,
account transfer and virtual account. Visibility does not verify payment return
or merchant settlement. No order number was generated.

## Administrator verification

Owner authentication completed. Read-only administrator inspection confirmed:

- Product25 has exactly the four public option codes O/P/Q/R under P000000Z.
- All four variants have native stock management set to disabled. This predates
  the detail change; quantities must not be inferred as physical stock.
- Standalone gloss18 has SKU P000000S000D; series gloss25 has P000000Z000O.
  They remain distinct records; no inventory or historical order merge occurred.
- Search by product code returns existing lip-series orders.
- One existing order displays01oil quantity2 and02oil quantity1 separately,
  credit-card payment via Inicis, shipping-in-progress status, CJ Logistics
  selected and a nonempty numeric tracking input.
- Tracking, invoice-edit, order-status, cancellation and refund controls are
  visible. No order, shipment, payment or refund state was changed.
- No customer identifiers, order numbers or tracking numbers are saved here.

## Remaining verification and limits

A new payment -> admin receipt -> stock deduction -> fulfillment -> reversal
chain has NOT been run. Existing successful orders are evidence of current
operations, not an end-to-end test of the new candidate. Member coupons,
address-dependent shipping exceptions, physical iOS and any separate warehouse
integration remain unverified. Do not promise automatic stockout protection:
native inventory management is disabled. Enabling it requires a confirmed stock
source and quantities; no commercial settings were changed.

The original test guest basket was empty before adding four test lines. The
three-line cleanup confirmation timed out. After owner login/browser reconnect,
the current storefront session showed an empty basket. The original guest-state
cleanup cannot be proven across the authentication change; no test order exists.
