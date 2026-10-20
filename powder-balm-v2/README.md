# Powder Balm V2

Owner authorized this revision after reviewing V1. Keep immediate use clarity,
but restore TAM's photography-led product-detail tone and communicate the
cosmetic benefit beyond an oil-blotting-paper substitute.

Approved headline: **번들거림 잡고, 피부결까지 매끈하게.**
Plain explanation: **코·이마의 번들거림과 모공 부각을 정돈하는 밤 타입 파우더.**

The opening follows the existing Cloud hero's centered benefit copy and large
product photograph, with the neutral typography/white space of the TAM family.
The original flatlay shows product, puff and texture in one photograph. Its
bytes are unchanged; browser framing is geometric only. Literal product type
and location appear above the photograph. Forehead/nose demonstration follows
directly. Blotting-paper language remains only in the external touch-up use case.

V1 source and supplied masters are preserved. V2 reuses its product assets;
new source provenance is in `source-manifest.json`. No synthetic skin, new
colour/exposure correction or quantitative comparative efficacy claim.

Current Cafe24 composition and package:

- `../cafe24-delivery-20261020/powder-balm/index.html`
- `../cafe24-delivery-20261020/powder-balm-cafe24.zip`

Rebuild with `ops/cafe24/build_powder_balm_package.py --source <archive> --facts
<official-product-facts.txt>`; verify with `ops/cafe24/check_powder_balm_package.py
--screenshots <local QA directory>`. Builder now targets V2. Git preserves V1
export history. Five JPGs and two short GIFs, each under 4.9MB; native information
and full ingredient list remain identical to V1. No upload-time fonts or JS.

Evidence: `../ops/cafe24/powder-balm-v2-20261020.json`.
Owner visual acceptance is pending; actual Cafe24 upload remains deferred.
