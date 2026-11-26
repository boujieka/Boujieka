# TestFlight release checklist (iOS)

The repository side is ready: `apps/mobile/eas.json` (profiles `preview` and `production`, remote build numbers with
auto-increment) and `apps/mobile/app.json` (bundle id, export compliance). What remains needs **your Apple accounts**,
which cannot be done from this repository.

> The build is the **simulation** app. Keep it in TestFlight (internal/external testers, e.g. partners and investors).
> A public App Store release of a money-transfer app normally has to come from the licensed financial entity.

## 1. One-time, on your side
1. **Apple Developer Program** membership, preferably as an organisation (company), not an individual.
2. **Decide the bundle identifier before the first upload — it can never be changed afterwards.**
   Current value: `app.diasposwap.simulation` (in `app.json`, `ios.bundleIdentifier`). Reverse-DNS of a domain you
   control is the convention (e.g. `com.<yourcompany>.diasposwap`). Tell Claude the final value to update it.
3. **App Store Connect → Apps → +**: create the app with that bundle id. Note its **Apple ID** (numeric, "ascAppId").
4. **Credentials for EAS** (choose one):
   - simplest: run `npx eas-cli@latest credentials -p ios` once on your machine and log in to Apple when asked;
     EAS creates and stores the distribution certificate and provisioning profile;
   - for unattended builds: create an **App Store Connect API key** (Users and Access → Integrations) and upload it
     with `eas credentials`. Never commit the `.p8` file.
5. Put your `ascAppId` and Apple Team ID in `eas.json` → `submit.production.ios` (`"ascAppId": "…"`,
   `"appleTeamId": "…"`). These are identifiers, not secrets.

## 2. Each release
```bash
cd diasposwap/apps/mobile
npx eas-cli@latest build -p ios --profile production --submit   # build in the cloud, then upload to App Store Connect
```
Build numbers are incremented automatically by EAS (`appVersionSource: remote`). Raise `version` in `app.json` for a
new marketing version.

## 3. In App Store Connect → TestFlight
- **Internal testers** (up to 100, your team): available as soon as processing ends, no review.
- **External testers** (up to 10,000): the first build goes through Beta App Review (about a day), later builds are
  usually immediate. Provide test notes: "Simulation mode, no real money; any 4-digit PIN; demo profile Amina (France)".

## Already checked in this repository (2026-11-26)
- `expo-doctor`: 20/20 checks passed.
- `eas config --platform ios --profile production`: resolves without errors; the generated Info.plist contains
  `ITSAppUsesNonExemptEncryption = false` (the app only uses HTTPS and HMAC for authentication).
- Not done here: an actual iOS build (needs your Apple credentials) and any test on a real iPhone.
