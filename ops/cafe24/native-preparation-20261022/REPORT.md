# Cafe24 native preparation · 2026-10-22

This is preparation and a baseline check of the old skin21 candidate. It is
not verification of the approved design on Cafe24 and does not authorize a
production switch based on these results alone.

## Completed

- Authenticated skin list confirms Korean production skin18, existing candidate
  skin21, and English shop5 skin8. No skin selection or administrator save.
- Captured 15 selected original HTML templates from the skin18 editor, including
  homepage, main/general layouts, head/header/footer/aside, product detail,
  detail/review/tab partials, basket, order form, login and join. Raw originals
  remain outside Git. This is not a complete downloadable skin archive.
- Original layout imports its head from a separate file. The integration helper
  previously skipped both real layouts because it required an inline closing
  head tag. It now accepts one unambiguous head import and adds layout-local
  theme directives without changing the shared head file.
- Five regression tests pass. Local patch checks on both actual captured layouts
  pass, retain non-header/footer imports and the content slot, and are idempotent.
  Captured original files are unchanged. Cafe24 rendering remains unverified.
- Existing skin21 product109 option `01. 샌드 쉐이더` resolves to 18,000 KRW.
  The initially empty basket accepts one item: subtotal18,000 + shipping3,000 =
  total21,000 KRW. Changing quantity to two yields subtotal36,000, shipping0,
  total36,000 KRW. The native order form opens and repeats the latter amounts.
  No payment or order submission was performed.
- Snap widget3 loaded and displayed357 reviews on the existing product109 page.
  This does not verify every product mapping or the future migrated skin.

## Unfinished / blocked

- Browser file chooser rejects attachment with `-32000 Not allowed`.
  Official extension guidance requires owner enabling “Allow access to file
  URLs.” Browser URL policy explicitly blocks automated access to
  `chrome://extensions`; owner action requested, no workaround attempted.
- Whole-skin backup download did not produce a verified local archive. The
  administrator download confirmation/browser interaction stalled. Server
  backup presence is confirmed; source capture above is only a partial export.
- **Cleanup pending confirmation:** the test basket contained product109,
  option01, quantity2. Delete was requested, but browser dialog handling timed
  out. The last successful reload still showed the test item. Owner was asked
  to confirm the deletion dialog. Verify basket empty before further cart tests.
- No coupon application control was visible in the inspected order form.
  Coupon redemption, exclusions, expiry, exact30,000 threshold, regional and
  product delivery exceptions, guest/member variants, inventory edge cases,
  payment completion/return and post-migration review mapping remain unverified.
- The original shared head includes `user-scalable=no`; order form also limits
  viewport scales. Record for native mobile accessibility repair and retest.
- Approved fullscreen/overlay layout, latest product details and native commerce
  still need integration into the candidate. Existing package predates them.
- No physical phone or authenticated device-farm session is available. Existing
  macOS Safari VM and slow-connection preview results are separate evidence.

## Next action

Verify test-basket cleanup after dialog recovery. Once the owner enables the
file permission, retry one isolated image attachment and verify its actual
Cafe24 URL. Complete original dependency capture, refresh the native package,
apply only to the backed-up candidate and rerun commerce/mobile/Snap checks.
Production skin18 and English skin8 remain unchanged.
