# TAM Beauty store

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
