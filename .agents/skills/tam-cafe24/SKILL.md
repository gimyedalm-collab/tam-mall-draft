---
name: tam-cafe24
description: "Resume TAM Beauty Cafe24 migration, native commerce integration, and bug fixing. Use for requests to proceed with the TAM store, preserve existing shop functions, inspect coupons/shipping/reviews, or verify a candidate skin."
---

# TAM Cafe24

## Resume from evidence

Work in the `tam-mall-draft` repository. On this workstation it is at
`C:/Users/BNK-1/Desktop/tam-mall-draft-backup`.
Read `CAFE24-IMPLEMENTATION-PLAN.md`, `ops/cafe24/state.json`,
`ops/cafe24/bugs.json`, and the latest `ops/cafe24/feature-inventory.json`.
Check git status before editing. Keep the approved design at
`tam-design-fixed-20260917`; do not reopen visual direction or video editing
unless the user asks. The existing Cafe24 package predates this design.

Choose the highest-priority actionable item and complete it. The user has asked
for implementation, configuration, verification, and fixes, not instructions
they must carry out themselves. Reuse authorization already given. Obtain
settings from the administrator instead of asking the user to transcribe them.
When authentication is missing, complete independent preparation and state the
specific access needed. Do not repeatedly retry an unavailable login.

## Preserve actual commerce

- Back up and clone the active PC/mobile skins before migration. Record the
  actual mall, shop number, skin IDs and rollback target locally.
- Use native Cafe24 modules, variables, option selectors and purchase/cart
  handlers. A mock cart, hardcoded review, or coupon label is not integration.
- Retain product IDs, visibility rules, original board links, Snap review
  product/widget mappings, Naver Pay, Kakao checkout, social login, channel
  coupon, analytics, and other installed app hooks found in the source skin.
- Public pages are an inventory, not authoritative admin policy. Read existing
  discount/coupon/shipping settings and preserve them unless changes are
  specified. A cloned skin shares live commerce settings and customer data.
- Never label a service functional solely because its button/script exists.
  Record separately: visible, browser-interaction checked, admin confirmed,
  and end-to-end verified. External widget/payment UI may have fixed limits.
- Use owner-entered login/2FA. Keep credentials, browser profiles, raw admin
  exports, and customer data outside Git. Do not publish review/customer text
  in bug evidence. No customer messages or coupon notification broadcasts are
  implied by a skin migration. Real paid test orders need defined test terms.

## Reproduce, repair, verify

For each issue update `ops/cafe24/bugs.json` with affected route, reproduction,
expected/actual result, priority, evidence, fix, and retest outcome. Distinguish
observed bugs from unverified risks and implementation tasks. Fix the smallest
relevant surface. Verify the original failing flow on desktop and mobile;
broaden checks only for affected dependencies.

Run `python -X utf8 ops/cafe24/smoke.py --base-url <candidate-base-url>` for
public structural regression checks. This does not issue orders or prove
coupon, member, delivery policy, or payment correctness. Authenticated QA must
cover options/stock, cart quantities, coupon restrictions, shipping thresholds
and exceptions, member/nonmember flows, actual review matching, checkout, and
the relevant payment return behavior. Use platform/provider test methods when
available. Do not invent a successful test when its environment is unavailable.

The integration helper `storefront-v2/integrate_skin.py` creates a separate
candidate from an original skin; read its usage and report. It does not finish
the homepage migration or publish a skin. Preserve native modules while
updating templates to the frozen design.

At the end update `state.json` with concrete completion, remaining work, and
the next action. Report what was tested and what still requires access. Use the
repo's commit/push authorization; review staged files for private data first.
This skill/agent resumes on invocation; it is not an always-running monitor.

## Browser and agent

The repository contains `.codex/agents/tam_cafe24.toml`. It inherits the parent
model/permissions and has a separate persistent Playwright profile for TAM.
Read `ops/cafe24/README.md` for startup and access status. Only one worker owns
that authenticated browser at a time. Use isolated headless contexts for
independent public audits. If profile contention occurs, do not kill the user's
browser or delete its profile; release the owning task or reconnect properly.
