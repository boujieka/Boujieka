# Design system

Tokens live in `apps/mobile/tailwind.config.js` (NativeWind). Components in `apps/mobile/src/components/ui.tsx`.

## Colour
| Token | Hex | Use |
|---|---|---|
| `petrol` | `#082F35` | dark surfaces, headings on light, dark-mode background |
| `emerald` | `#087F6D` | primary actions, progress, success |
| `gold` | `#C9A44C` | accents, the simulation banner border, active states on dark |
| `gold-700` | `#8A6A1F` | gold for **text** on light backgrounds (contrast) |
| `ivory` | `#FAF8F2` | light background |
| `anthracite` | `#182525` | body text on light |
| `danger` | `#A8432A` | errors, failed/disputed states |

Contrast (WCAG 2.x relative luminance, computed): ivory on petrol 13.47:1; white on emerald 4.92:1 (AA);
anthracite on ivory 14.87:1; `gold-700` on ivory 4.75:1 (AA); petrol on `gold-100` 11.94:1 (simulation banner, light);
gold on `petrol-700` 4.97:1 (banner, dark). Raw gold `#C9A44C` on ivory is 2.22:1: never use it for text on light
backgrounds. `gold-700` on `gold-100` is 4.21:1 (fails AA for small text) and is not used for text.

## Components
`Screen` (safe area + permanent `SimulationBanner`), `Card`, `Button` (primary / secondary / ghost / danger, min
48 px touch target), `Row` (label/value), `StatePill` (16 transfer states), `Progress` (accessible progressbar),
`Chip` (selectable), `ListItem`, `Mark`, `Logo`.

## Principles
- One primary action per screen ("Envoyer de l'argent", "Vérifier l'ordre", "Payer").
- Show cost, rate, fee and amount received **before** confirmation; label estimates as estimates.
- Never show counterparty identity. Never show savings without a documented reference.
- Light and dark mode follow the system setting.
