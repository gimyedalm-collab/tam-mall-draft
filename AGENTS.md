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
