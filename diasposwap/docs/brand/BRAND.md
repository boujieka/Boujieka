# DiaspoSwap brand

**Slogans** — FR: *L'argent circule localement. La valeur voyage.* · EN: *Money stays local. Value goes global.*

## The mark
Generated from exact geometry by `generate.py` (run `npm run brand`). Three ideas, kept minimal so the mark survives
at 16 px:
- **Two counter-rotating arrows** (gold above, emerald/ivory below): the two opposite transfers that offset each other.
  The arrangement has 180° rotational symmetry: reciprocity.
- **A vertical balance axis** with a feather-like crown in the centre: Maât's balance and feather — equilibrium,
  fairness, truth.
- **Three stepped wing feathers on each side**: a geometric reference to the wings of Horus (protection), drawn as flat
  bars, not as an illustration.

Deliberately avoided: pyramids, pharaonic figures, hieroglyphs, metallic effects, gradients.

The user-supplied concept image (falcon head with two arrows) was used as direction; this mark is a simpler geometric
redraw, not a trace of it.

## Files (`docs/brand/`)
| File | Use |
|---|---|
| `mark-light.svg` / `mark-dark.svg` | symbol on light / dark backgrounds |
| `mark-mono-dark.svg` / `mark-mono-light.svg` | single-colour versions |
| `app-icon.svg`, `icon-square.svg` | rounded and full-bleed app icon sources |
| `adaptive-foreground.svg`, `adaptive-monochrome.svg` | Android adaptive icon layers (safe zone respected) |
| `logo-horizontal-light.svg` / `logo-horizontal-dark.svg` | horizontal lockup |
| `logo-stacked.svg` | stacked lockup with slogan |

PNG exports for Expo are in `apps/mobile/assets/brand/` (icon 1024, adaptive layers 1024, splash 512, favicon 48),
rendered with Chromium from these SVGs.

## Known limits
- The wordmark uses live text (`Plus Jakarta Sans`, falling back to Inter / Arial). The font is not bundled, so it
  renders in a fallback face on most systems. Before production, a designer should choose the typeface, check its
  licence and convert the wordmark to outlines.
- Trademark availability has **not** been checked (OAPI, EUIPO, WIPO, USPTO, CIPO).
