# Powder Balm V1

Purpose: show immediately where this unfamiliar product goes, what it does,
and how to use it. User-approved hook: “기름종이를 바르다.” Follow with the
literal definition “코·이마의 번들거림을 잡는 밤 타입 파우더” and simultaneous
forehead/nose puff application. At 390px wide this introduction occupies 490px.

The source layout is `layout.html`. The customer-facing preview is
`../cafe24-delivery-20261020/powder-balm/index.html`, made entirely from the
actual ordered Cafe24 image files and native product information.

## Design choices

- Sky `#eaf5f8`, ink `#243d45`, muted text `#587078`, blue `#74b6cb`, white.
- Pretendard for Korean copy; restrained Manrope for English captions.
- A compact product-and-hook opening immediately followed by labelled
  application footage. Avoid a long brand mood introduction that delays use.
- Supplied product cutouts, texture and photography. No generated skin,
  colour edits, synthetic before/after, scene controls or new model imagery.
- Sequence: use location/action → oil-control and cosmetic blur → balm texture
  → primer/finishing/touch-up → precise instructions → product → native facts.

## Evidence and limits

The official product 111 description supports the existing use instructions
and marketing positioning. It does not establish new quantitative efficacy.
Keep 6-hour duration, ZERO absolutes, non-irritation absolutes and unverified
certification out of this version. See `../ops/cafe24/powder-balm-v1-20261020.json`.
“수정” in source filenames means a footage revision, not proof of touch-up over
foundation. The footage demonstrates application only. Supplied appearance is
preserved without creative colour correction; upstream treatment and physical
colour accuracy have not been validated. GIF palette reduction is disclosed.

Original masters remain in the supplied product archive. `source-manifest.json`
records exact hashes, relative source names and video segments. No source files
were overwritten. Known Dasha material and uncertain vertical V1–V3 videos are
excluded. The parent archive folder name is not an identity determination.

## Rebuild

From the repository root, run:

```powershell
python -X utf8 ops/cafe24/build_powder_balm_package.py --source "<supplied product archive>" --facts "<official-product-facts.txt>"
python -X utf8 ops/cafe24/check_powder_balm_package.py --screenshots "<local QA folder>"
```

Requires Python, Pillow, Playwright Chromium and FFmpeg. Fonts are local and
used only for raster export. The upload package has no font, script, MP4 or
external video-host dependency. GIFs play three cycles and stop.

Owner visual acceptance and Cafe24 upload remain separate from file preparation
and preview verification. Actual Cafe24 upload is explicitly deferred.
