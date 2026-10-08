# NicoTV (modified)

A lightweight Twitch client built as a single-page web app (HTML/CSS/JS), packaged as

- an **Android / Android TV** app (WebView shell, `.apk`)
- an **LG webOS** app (`.ipk`)

This repository contains the web app source and a small build script. It is a modified version of **Nicominecith TV 2.15.0**; all credit for the original app goes to its author.

## Features added in this fork

| Feature | How to use |
|---|---|
| Custom AFK message | Settings -> *AFK-Nachricht* (max. 40 chars, empty = "AFK") |
| Emote menu (Twitch + 7TV + BetterTTV) | 😀 button next to the chat input, `E` key, or `/emotes` |
| 7TV / BTTV tabs follow settings | Disable 7TV or BetterTTV in settings and the tab disappears |
| Locked emotes with hint | Channel sub/follower/bits emotes you can't use are greyed out with 🔒; tap for details |
| Sub button + QR code | ⭐ Sub button opens a QR code to `twitch.tv/subs/<channel>` |
| Copy a chat message | Long-press a message |
| Moderation menu via gesture | Triple-tap a message (moderators only) |
| Reply to a message | Swipe a message to the right |
| Centered AFK screen | Only a tiny anti burn-in drift remains |

See [CHANGELOG.md](CHANGELOG.md) for details.

> **Note:** To see which emotes *you* own (and to mark the rest as locked) the app needs the `user:read:emotes` scope. Log out and log in again once after updating.

## Repository layout

```
android/www/   web app for the Android APK (index.html + assets)
webos/         web app + metadata for the webOS IPK
tools/build.py build helper (IPK + re-signed APK)
```

`android/www/index.html` and `webos/index.html` share the same app code and only differ in the `<head>` (viewport / phone handling).
The user interface text is currently in German.

## Building

Requirements: Python 3. For the APK additionally `openssl` in your `PATH`.

### webOS IPK

```bash
python3 tools/build.py ipk
# -> dist/com_nico_nicotv_<version>_all.ipk
```

Install it with the [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop) or `ares-install` (needs developer mode / Homebrew Channel on the TV).

### Android APK

The native Android part (WebView shell: `classes.dex`, resources, manifest) is **not** included in this repository because its source is not available. The script reuses it from an existing NicoTV APK and swaps in the web app:

```bash
python3 tools/build.py apk --base path/to/NicoTV-2_15_0.apk
# -> dist/NicoTV-custom.apk
```

The APK is signed with a v1 (JAR) signature using a self-generated key (`tools/key.pem`, created on first run and git-ignored). Because the key differs from the original one, **uninstall the original app before installing**, and keep your own key if you want future builds to install as updates.

### Local testing

The app can be opened in a desktop browser by serving `android/www/` with any static server, e.g. `python3 -m http.server -d android/www`. Add `?m=phone` to force the phone layout.

## Authentication & network access

Login uses the Twitch OAuth device-code flow (`id.twitch.tv`). The app talks directly to these services:

- Twitch: Helix API, GQL, Usher (streams), IRC chat, badges and emote CDN
- 7TV (`7tv.io`, `cdn.7tv.app`) and BetterTTV (`api.betterttv.net`, `cdn.betterttv.net`)
- Google Fonts (`fonts.googleapis.com`)

There is no backend of its own. Review `android/www/index.html` before using it with your account, as with any third-party client.

## Disclaimer

Unofficial project, not affiliated with or endorsed by Twitch, 7TV or BetterTTV. Twitch is a trademark of Twitch Interactive, Inc.

## License

The original app does not ship a license, so none is granted here. If you are the original author or want to reuse this code, please contact the maintainers / add a license of your choice before publishing.
