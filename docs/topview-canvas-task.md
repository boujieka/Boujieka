# Topview Canvas — setup and queued task

Prepared 2026-09-28. **Not yet run.** The Topview plugin is not installed and not
authorized; this file holds the steps and the brief so neither has to be
reconstructed later.

## 1. Install (run locally, not in a cloud session)

From <https://github.com/topviewai/plugins/blob/main/docs/claude.md>:

```bash
claude plugin marketplace add https://github.com/topviewai/plugins --scope user --sparse .claude-plugin plugins
claude plugin install topview-browser@topview --scope user
```

Then start a **new conversation**. OAuth is negotiated on the first tool call
against the plugin's MCP server (`https://mcp-browser.topview.ai`, HTTP
transport) — there is no auth block to pre-fill.

Setup is not complete until an authorized read-only call succeeds.

> Do not run this inside a Claude Code cloud session. `--scope user` writes into
> an ephemeral container that is reclaimed after the session, and the OAuth
> handshake needs an interactive browser the session does not have.

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
