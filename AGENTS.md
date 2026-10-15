# TAM Beauty store

Current resume entry: `ops/cafe24/COMPACT-HANDOFF.md`. Latest owner instruction is image-only replacement while preserving the restored design. See the final ACTIVE OVERRIDE below.

For Cafe24 implementation and bug work, read
`.agents/skills/tam-cafe24/SKILL.md` and `ops/cafe24/state.json` first.
The user requested a dedicated Cafe24 worker; its configuration is
`.codex/agents/tam_cafe24.toml`. Use it for bounded Cafe24 tasks when the runtime
supports named custom agents, or follow the same skill in the main session.
Do not create simultaneous writers to the same skin or authenticated browser.

The design is frozen at `tam-design-fixed-20260917`. Preserve it during native
integration. `storefront-v2/preview` is a mockup; it is not working checkout.
Do not commit login state, private skin exports, customer data or raw admin
captures. Record sanitized findings and tests in `ops/cafe24`.

## User-confirmed rollout responsibility · 2026-10-13

- The user approved the five-brand UI/UX audit improvements for GitHub preview.
- After the user signs in to Cafe24, the agent must directly implement the approved
  site there: back up the active skin, migrate to the candidate, connect native
  products/options/stock/cart/checkout/reviews/coupons/shipping and verify the flows.
  Do not hand the user a list of manual edits as the final deliverable.
- Keep the current production mall unchanged until the approved work is complete
  and verified. Preserve existing commercial settings; resolve discrepancies from
  administrator evidence. Login/2FA and provider-controlled steps may need the owner.
- GitHub preview completion is not Cafe24 integration completion. Track both.
- Do not use ChatGPT Sites for this project/account. Publish web work through GitHub.

## Milky Cheek final design · 2026-10-14

- Owner approved V12 as final after removing the separate model mood section.
- Preserve seven panels: hero, application, colours, texture, formula, test, ending.
- Colour comparison leads directly into milky texture. Do not restore a model
  interlude, its logo, or generated portrait without a new explicit owner request.
- Preserve original shade imagery, the approved usage video, small supporting
  copy, and the compact ingredient illustration. This lock applies to product 102;
  it does not block other authorized store or native commerce work.

## Highlighter R33 candidate · 2026-10-14

- The owner requested an overall format rebuild against Lip Liner R32/R34 and
  the finished Milky Cheek V12, not only smaller typography adjustments.
- Active candidate: `highlighter-r33/`, built by `ops/cafe24/build_highlighter_r33.py`.
  It replaces the iframe on preview product 24 with scoped responsive HTML.
- Follow `ops/cafe24/highlighter-r33-direction.md`: actual pearl and three-shade
  comparison first; no sponge-led USP, new AI face, or generated pearl evidence.
- Retain original product/shade media and approved use footage. R32 is a rollback
  reference; do not run its builder over the R33 integration. R33 owner review is
  pending and is separate from the final, locked Milky Cheek design.

- On 2026-10-15 the owner rejected R33's feel and then specified mismatched
  image dimensions/layout and consecutive text-heavy glow/shade sections.
  Current rules: two landscape shade columns, third card at equal size centered;
  shared hero/shade/swatch/texture/formula/ending geometry from locked Cheek V12;
  glow heading before footage, then a concise colour heading and photos.
  Do not restore three portrait columns or the post-video heading/copy block.
  See `ops/cafe24/highlighter-r33-spec-alignment-20261015.json` for measured
  before/after evidence. Owner design acceptance is pending; passing browser
  checks does not constitute that acceptance.

- Later on 2026-10-15 the owner rejected the lack of purchase appeal and asked
  for all target-brand persuasion patterns to inform TAM's USP. Keep the shared
  geometry, but lead with the actual on-skin glow video in the hero; the product
  trio belongs at the closing selection step. Explain the makeup occasion for
  each shade, then texture, amount/placement and lower-priority formula support.
  See `ops/cafe24/highlighter-r33-usp-20261015.json` and
  `highlighter-r33/review/usp-review-20261015.html`. Do not restore the opening
  specification strip or present three shades/stick/vegan as exclusive features.
  The current proposal still awaits owner acceptance of its purchase appeal.

- Owner copy correction on 2026-10-15: restore the shade heading to
  `세 가지 펄 컬러.` and remove the added pearl/initial-amount FAQ block.
  Do not reintroduce the rejected question-style shade heading or these FAQs
  without an owner request. The earlier USP report records a superseded draft.

- Owner usage clarification on 2026-10-15: direct facial application can disturb
  the base; the sponge is for softening edges after application. Explain a small
  amount tapped on with fingertips, then optional sponge blending at visible
  edges. Do not promote rubbing/direct application or claim no base disturbance.

- Owner approved the brand-evidenced on-skin expansion on 2026-10-15. Keep the
  two-column comparison, then show the three original skin photos in equal
  larger square frames revealing the wider cheek/nose context, before texture.
  Use only colour names and short shade descriptions; no new claims or generated
  skin evidence. This explicitly extends the previously reviewed shorter page.


## Owner rejection of repeated faces and original-source replacement · 2026-10-15

Supersedes the on-skin expansion above. Owner rejected the three repeated large
face photographs and requested older arm-swatch/product sources, with AI allowed
only if needed. Remove the duplicate faces. Use the original brand filming:
an arm swatch still and hand application clip in equal 4:5 frames, two columns
with the established comparison gutters and spacing. No unverified shade labels,
colour correction, generated skin evidence or new performance claims. The three
original named shade comparisons remain. Original sources were sufficient; no AI
was used. This explicit AI permission supersedes the earlier blanket no-new-AI
rule for this task, but generated visuals must not masquerade as actual swatches.
See `ops/cafe24/highlighter-r33-source-reuse-20261015.json`. Owner acceptance of
this replacement remains pending; passing QA is not design approval.


## Owner-authorized whole-page correction · 2026-10-15

Supersedes the arm/hand source-reuse proposal. Owner rejected its dark/warm arm
image and application-only loop, then approved the whole-page audit direction.
Keep the original opening finished-glow film and official three-shade comparison.
Introduce the clean original product still after the opening film. Replace the
arm/hand insert with ONE different original finished-makeup photograph (not the
three comparison faces enlarged again), showing unobstructed cheek and nose.
Remove the separate thick-pink-texture and extreme-pearl macro section. Keep the
three named texture swatches as colour support. Replace the direct-application
montage with the original stick/sponge cutout and clear fingertip-then-edge-only
sponge instructions. Original media files remain archived unchanged. No AI,
recolouring or skin lightening is used. See highlighter-r33-result-led-20261015.json
in ops/cafe24. The owner has approved this direction, not the final rendered result.
Keep the locked Cheek page and all commerce markup outside the detail intact.


## ACTIVE OVERRIDE: owner rejected latest revision; rollback · 2026-10-15

The owner strongly rejected 7a62cae and ordered rollback to the previous version,
cross-validation and compaction. Active detail is restored exactly to 678f30c
(content e5f525c), including the arm/hand insert. This is a rollback baseline,
NOT owner approval of that insert, which was also criticized. The result-led
revision above is rejected and must not be reapplied. Do not redesign during
this task. Preserve rollback, record the failed decisions and user constraints,
and create a compact resume record. Technical QA or Claude agreement is not
visual acceptance. See state.highlighter_rollback_20261015 for current status.

## ACTIVE OVERRIDE: image-only scope clarification · 2026-10-15

The owner clarified that the request was to change images, not redesign the page.
The earlier interpretation of whole-page authorization was too broad. Keep the
restored 049728c structure/copy/CSS/JS. The owner then authorized trying the
image-only correction, asking whether it affects only ON SKIN. Current change
is confined to the two ON SKIN assets and poster: original three-pearl arm
swatch plus unobstructed finished palm footage. The small caption changes only
hand-back to palm to describe the real source; alt/aria labels also match it.
No other section, typography, geometry, heading, body copy or media changed.
See `ops/cafe24/highlighter-r33-image-only-20261015.json`. Public source commit
171894c. This is a candidate, not owner design approval. Keep source review
limits separate from technical QA and Claude opinion. Do not reapply 7a62cae.

## ACTIVE OVERRIDE: original swatch background cleanup · 2026-10-15

Owner liked the two-source revision but called the dark background dirty-looking,
and authorized reviewing other sources and editing. Keep the exact image-only
scope, including every caption and layout. Current candidate cleans only the
backdrop and cast shadow of the same original arm/palm footage. Native SVG wraps
the byte-identical arm JPEG with a silhouette clip; video uses a per-frame matte
over pale off-white, preserving foreground before encoding. No exposure/colour
or pearl/skin retouch. An ImageGen background attempt was rejected because it
changed pearl microtexture; it is not a published asset. See
`ops/cafe24/highlighter-r33-background-cleanup-20261015.json` and current state.

## ACTIVE OVERRIDE: official arm / texture photograph pair · 2026-10-15

Owner approved trying the best option after clarification that only the existing
ON SKIN two frames would change: candidate1 arm swatches left, candidate3 official
product/texture photograph right. Candidate2 palm comparison was rejected for
visible skin creases. Current assets are `official-arm-three-shades-261015.jpg`
and `official-three-pearl-textures-261015.jpg`, byte-identical official sources.
AI cleanup previews drifted in texture/colour and were not selected. Keep the
source's original shade labels. Remove the ON SKIN video, its controls and motion
binding; caption the right photograph `세 가지 펄 제형`. Do not change other
sections, copy, CSS/JS or geometry. Formula improvements were discussed only,
not implemented. See `highlighter-r33-official-pair-20261015.json` and state.
Owner acceptance of the actual rendered result remains pending.

## Desktop typography finish · 2026-10-15

Owner requested reviewing PC font sizes and finishing the detail. This explicitly
permits the scoped desktop font-size override in `detail.css` for detail containers
at least760px wide: hero64, section headings48, body24/26, swatch captions20 and
footnotes16px. Preserve narrower containers/mobile typography, all wording,
selected original photographs and geometry rules. No wider redesign is implied.
See `highlighter-r33-pc-typography-20261015.json` and current state.
