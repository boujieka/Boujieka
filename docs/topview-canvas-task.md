# Topview Canvas — setup and queued task

Status as of 2026-09-28:

- **Marketplace added** — `topview` (git, github.com/topviewai/plugins), registered in user settings.
- **Plugin installed** — `topview-browser@topview` v1.0.4, scope user, enabled.
- **Authorization NOT completed** — the MCP server is unreachable from this
  environment, so OAuth never starts. See below.

## 1. Install

From <https://github.com/topviewai/plugins/blob/main/docs/claude.md>:

```bash
claude plugin marketplace add https://github.com/topviewai/plugins --scope user --sparse .claude-plugin plugins
claude plugin install topview-browser@topview --scope user
```

Then start a **new conversation** — the plugin's MCP server is loaded at session
start, so it is not live in the session that installed it. OAuth is negotiated on
the first tool call against `https://mcp-browser.topview.ai` (HTTP transport);
there is no auth block to pre-fill.

### Blocker hit here: network egress

```
claude mcp list
plugin:topview-browser:topview-browser: https://mcp-browser.topview.ai (HTTP)
  x Failed to connect - ERR_PROXY_TUNNEL: Proxy refused to open a tunnel: 403 Forbidden
```

The environment's network policy denies `CONNECT mcp-browser.topview.ai:443`.
Authorization cannot begin until that host is reachable — either raise the
environment's network access level or add `mcp-browser.topview.ai` to its allowed
domains, in the cloud environment's settings. On a normal local machine this does
not apply.

## 2. The queued task

Paste into a fresh, authorized session:

> Using Topview Canvas, create a project called **"MoU Trap — social cutdowns"**.
> Build four 9:16 vertical teasers, one per audience (Ministers, Finance,
> Regulators, Developers), each 20–30 seconds. Each teaser takes the key
> statistic and the single sharpest ask from that audience's module. Keep the
> dark institutional palette of the source films. Assemble on the Timeline and
> export each separately.

### Source material for the four cutdowns

| Teaser | Statistic to lead on | Ask to close on |
| --- | --- | --- |
| Ministers | 1,125 MW signed in 2016 → 0 electrons delivered | Publish a register of power MoUs with status and expiry dates |
| Finance | Ghana: US$2.75bn net sector arrears at the 2019 recovery programme | See every MoU that could create fixed payments or state support, at MoU stage |
| Regulators | 11.5 US¢/kWh set administratively → 7.5¢ sought in 2019 → deadlock | Compete by default; test unsolicited proposals against the least-cost plan |
| Developers | Fewer than 10% of African infrastructure projects reach financial close | Measure pipelines by projects passing both tests, not MoUs signed |

Full copy, narration and sourcing for each is in `src/mou/content/en.ts` and
`docs/evidence.md`. Every figure carries the chapter's own caveats — keep them on
screen in any derived cut.

## 3. What the plugin provides once authorized

One plugin, `topview-browser` v1.0.4, with three skills:

- **`operate-topview-canvas`** — project lifecycle, node placement and layout,
  approval-gated image/video/audio/storyboard generation, scene cards, Timeline
  assembly and export.
- **`canvas-agent-workflows`** — routes a brief to the right production path
  (storyboard, remake, replication, product/social video, narrative adaptation).
  Treats one-shot `direct-generation` as a gated fast path, not the default.
- **`marketing-studio`** — Amazon, TikTok Shop, Shopee, plus YouTube and
  Instagram creator discovery and outreach. States it will not fabricate
  proprietary platform metrics.
