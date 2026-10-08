# NicoTV

Eine schlanke, eigenständige Twitch-Client-Web-App (HTML/CSS/JS), optimiert für den Einsatz auf dem Fernseher und mobilen Geräten. Verpackt und bereitgestellt als:

- **LG webOS** App (`.ipk`) für LG Smart TVs
- **Android / Android TV** App (WebView-Shell, `.apk`)

---

## Features

| Funktion | Beschreibung & Bedienung |
|---|---|
| **Eigene AFK-Nachricht** | Einstellungen -> *AFK-Nachricht* (max. 40 Zeichen, leer = "AFK") |
| **Erweitertes Emote-Menü** | Twitch + 7TV + BetterTTV (über das 😀-Symbol neben dem Chat, die `E`-Taste oder `/emotes`) |
| **Dynamische Tabs** | 7TV oder BetterTTV in den Einstellungen deaktivieren blendet die entsprechenden Tabs aus |
| **Gesperrte Emotes mit Hinweis** | Kanal-Abos/Follower/Bits-Emotes, die du nicht nutzen kannst, werden mit 🔒 grau dargestellt (Antippen für Details) |
| **Sub-Button & QR-Code** | ⭐-Button öffnet direkt einen QR-Code zu `twitch.tv/subs/<kanal>` |
| **Nachrichten kopieren** | Nachricht gedrückt halten |
| **Mod-Menü per Geste** | Dreifach-Tipp auf eine Nachricht (nur für Moderatoren) |
| **Nachrichten beantworten** | Nachricht nach rechts wischen |
| **Zentrierter AFK-Bildschirm** | Inklusive minimalem Anti-Burn-In-Schutz |

> **Hinweis zur Anmeldung:** Damit die App anzeigt, welche Emotes *du* besitzt (und alle anderen als gesperrt markieren kann), benötigt die App den Scope `user:read:emotes`. Logge dich nach dem Update einmal kurz aus und wieder ein.

---

## Installation auf LG webOS Fernsehern

Die App ist **vollkommen kostenlos** und kann direkt heruntergeladen werden.

1. Lade die aktuelle `.ipk`-Datei der App aus dem **[Releases-Tab](https://github.com/USERNAME/REPOSITORY/releases)** herunter.
2. Aktiviere auf deinem LG Smart TV den **Developer Mode** (über die offizielle webOS Developer App).
3. Verbinde deinen PC mit dem Fernseher und installiere die App entweder:
   - Ganz bequem über den grafischen **[webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop)** oder
   - Über die Kommandozeile mittels `ares-install`.

---

## Sicherheit & Transparenz

Diese App ist zu **100% sicher und frei von Schadsoftware**. 
- Der gesamte Quellcode ist offen in diesem Repository einsehbar.
- Die App kommuniziert ausschließlich direkt mit den offiziellen APIs (kein versteckter Backend-Server, der Daten abgreift).

---

## Repository-Struktur

```
android/www/   Web-App für die Android-APK (index.html + Assets)
webos/         Web-App + Metadaten für das webOS-IPK
tools/build.py Build-Helfer (IPK + signierte APK)
```

`android/www/index.html` und `webos/index.html` teilen sich denselben Code und unterscheiden sich lediglich im `<head>` (Viewport- und Plattform-Handling). Die Benutzeroberfläche ist auf Deutsch gehalten.

---

## Authentifizierung & Netzwerkzugriff

Der Login erfolgt sicher über den offiziellen Twitch OAuth Device-Code-Flow (`id.twitch.tv`). Die App verbindet sich direkt mit folgenden Diensten:
- **Twitch:** Helix API, GQL, Usher (Streams), IRC-Chat, Badges und Emote-CDN
- **7TV:** `7tv.io`, `cdn.7tv.app`
- **BetterTTV:** `api.betterttv.net`, `cdn.betterttv.net`
- **Google Fonts:** `fonts.googleapis.com`

---

## Build & Lokale Entwicklung

Voraussetzung: Python 3. Für den APK-Build wird zusätzlich `openssl` im `PATH` benötigt.

### webOS IPK erstellen
```bash
python3 tools/build.py ipk
# -> erzeugt die IPK im Ordner dist/
```

### Android APK erstellen
```bash
python3 tools/build.py apk --base path/to/base.apk
# -> erzeugt die signierte APK im Ordner dist/
```

### Lokaler Test im Browser
Die App kann über einen lokalen Webserver direkt im Browser getestet werden:
```bash
python3 -m http.server -d android/www
```
*Füge `?m=phone` an die URL an, um das Smartphone-Layout zu erzwingen.*

---

## Lizenz

Entwickelt von Nico. Alle Rechte vorbehalten.
