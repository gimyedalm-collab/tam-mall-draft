# Powder balm image correction — 2026-10-22

Owner narrowed this change to product111 only. Candidate skin21/editor27;
production18 and English8 were not switched or edited.

Observed: desktop gallery840px source displayed at807px. The body combined
860px static panels with668px/760px GIFs; native width:auto!important caused
different widths and left alignment. All14 powder assets loaded, so this was
not an observed404 issue. Earlier layout tests did not assess this visual quality.

Fix: body max668px with consistent image width, automatic height, reserved
aspect ratio and centered margins. Eleven static panels re-rendered at1720px
from the editable approved layout and source photography; responsive860px
variants reuse the prior approved files. All3GIFs preserve exact original
bytes, palette, frames and timing. No source retouch or invented detail.
The original upper gallery is constrained to600px only for product111.
Other products keep their prior media and presentation.

Candidate saved: detail bridgev3 and purchase CSSv5; native template changes
are exactly two asset references. Fresh pre-change source saved privately.
Upload28/28: decoded image pixels, ICC, every GIF frame/timing preserved;
18PNGs were losslessly recompressed by Cafe24. See upload-checks.json.

Local preview:5 viewport/DPR cases passed14-image geometry/decode checks.
Actual native browser, Chromium slow network and Safari rerun pending.
Physical phone/iOS and actual transactions remain unverified.
GIFs remain4.8MB/4.6MB/1.5MB; no fast-load or original-video-fidelity claim.

Delivery: cafe24-delivery-20261022/powder-balm, matching product111 GitHub
preview and native product-111-v6.html. V5 sources/packages remain preserved.
