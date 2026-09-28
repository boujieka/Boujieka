# The MoU Trap — training films

Animated training films built from **Chapter 1, "The MoU Trap"**, of *Bankable Is Not
Enough* by Emmanuel Boujieka Kamga. Ten compositions: one core film plus four
audience modules, each in English and French.

Built with [Remotion](https://remotion.dev) — the films are React components, so
the copy, the figures and the timing are all version-controlled text.

## The core message

> An MoU costs almost nothing to sign and can cost a great deal later, either as
> power that never arrives or as a contract the system cannot carry. The trap
> persists because those who will bear the risk are absent when the commitment is
> made. Closing it means bringing the risk bearers, and the tests they would
> apply, to the start of the process.

Everything in these films serves that claim. The chapter's two tests are the spine:
the **lender's test** (can the project repay its debt?) and the **state's test**
(can the power system and the public finances carry this project's obligations for
twenty years or more?). The first is applied rigorously and late. The second is
usually not applied at all.

## The films

| Composition | Audience | EN | FR |
| --- | --- | --- | --- |
| `MoUTrap-Core` | All stakeholders — the full argument | 8:13 | 9:02 |
| `MoUTrap-Ministers` | Ministers and Cabinet — the signature moment | 2:40 | 2:59 |
| `MoUTrap-Finance` | Ministries of Finance and Treasury — the state's test | 3:10 | 3:35 |
| `MoUTrap-Regulators` | Regulators — price discovery and the tariff benchmark | 2:16 | 2:31 |
| `MoUTrap-Developers` | Developers and development partners — what counts as a pipeline | 2:47 | 3:21 |

Composition IDs take a locale suffix: `MoUTrap-Core-EN`, `MoUTrap-Core-FR`, and so on.

Each module ends with an **ask card** — the concrete actions that audience can take,
drawn from the chapter's own "Implications for decision makers".

## Running it

```bash
npm install
npm run dev        # Remotion Studio — preview and scrub every composition
npm run lint       # eslint + tsc
npm run cues       # regenerate the voiceover cue sheets in docs/cues/
```

Render a film:

```bash
npx remotion render MoUTrap-Core-EN out/core.en.mp4
```

Render everything:

```bash
npm run render:all
```

### Rendering in a restricted environment

Remotion downloads its own Chrome Headless Shell on first render. Where that host
is blocked, point it at a local Chromium instead:

```bash
npx remotion render MoUTrap-Core-EN out/core.en.mp4 \
  --browser-executable=/path/to/chromium
```

## Adding the voiceover

The films are built to play **silent** — the argument is carried on screen, which
is how most officials watch. They are also built to take narration without
re-timing anything.

1. Open the cue sheet for the film and locale you are recording:
   `docs/cues/<slug>.<locale>.md`. It gives every scene's in-point, duration, word
   count and estimated read time.
2. Record against it. One file per film is simplest; one clip per scene also works.
3. Drop the audio into `public/audio/`.
4. Register it in `src/mou/audio.ts`. Nothing else changes.

Scene durations are **derived from the narration**, not guessed: each scene takes
whichever is longer, the time its animation needs or the time its script needs.
Timing is computed per locale, because French runs roughly a fifth longer than
English. `npm run cues` re-derives everything and flags any scene where a rewritten
line would no longer fit.

To shorten every film without touching the copy, lower `PACING` and `PAD_SEC` in
`src/mou/structure.ts`.

## How it is put together

```
src/mou/
  types.ts        Scene kinds as a discriminated union — a new kind that isn't
                  handled is a type error, not a blank frame
  structure.ts    Which scenes, in what order, and the timing engine
  content/
    en.ts fr.ts   All copy and narration. Both locales share one type, so a
                  scene missing from one language will not compile
  theme.ts        Colour, type scale, spacing. Colour is semantic: signal /
                  trap / liability / pass mean the same thing in every scene
  scenes/         Fifteen scene components
  components/     Frame, typography, the institutional figures
  Film.tsx        Assembles a film from its blueprint and locale
```

To change a number or a phrase, edit `src/mou/content/`. To change how a scene
looks, edit `src/mou/scenes/`. To change how long anything runs, edit the
`minSeconds` values in `src/mou/structure.ts` — or just rewrite the narration and
let the timing follow.

## Evidence and its limits

Every figure on screen is traceable to the chapter, and **carries the chapter's own
caveats**. Where the source is press reporting rather than a primary document, the
on-screen citation says so. See [`docs/evidence.md`](docs/evidence.md) for the full
list of claims, sources and the qualifications attached to each.

This matters for a training film: the argument is strong enough that it does not
need the numbers to be firmer than they are.
