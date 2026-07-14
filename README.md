# Weltklasse Pianistinnen — Backend + Deploy

Flask-API + Frontend fuer drei kuratierte Listen:

- **Top 25 Newcomerinnen** — All-Time High 2026
- **Top 25 Alltime High** — 2026 (etablierte/legendaere Pianistinnen)
- **Top 20 Aktuell** — Stand Juli 2026 (redaktionelles Schlaglicht)

Das Frontend ist ein dunkles, auto-blaetterndes "Coffee-Table-Book" (`static/index.html`),
das seine Daten live von der Flask-API bezieht. Portraitbilder werden serverseitig live
von der oeffentlichen Wikipedia-REST-API nachgeladen (frei lizenziert, keine kopierten
Presse-/Agenturfotos) und 12h gecacht.

## Projektstruktur

```
pianistinnen-app/
├── app.py              # Flask-Backend (API + liefert das Frontend aus)
├── data.py              # Datensatz: 40 Kuenstlerinnen, in 3 Listen einsortiert
├── static/index.html    # Frontend (Vanilla JS, keine Build-Tools noetig)
├── requirements.txt
├── Dockerfile
├── fly.toml
├── .gitignore
└── .dockerignore
```

## 1. Lokal testen

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Dann [http://localhost:8080](http://localhost:8080) im Browser oeffnen.

Health-Check: `curl http://localhost:8080/api/health`

## 2. Auf GitHub hochladen

```bash
cd pianistinnen-app
git init
git add .
git commit -m "Initial commit: Weltklasse Pianistinnen App"
git branch -M main

# Erstelle zuerst ein leeres Repository auf github.com (ohne README/gitignore),
# dann:
git remote add origin https://github.com/<dein-username>/<dein-repo>.git
git push -u origin main
```

## 3. Bei Fly.io deployen

Voraussetzung: [Fly.io-Account](https://fly.io) + [flyctl installiert](https://fly.io/docs/flyctl/install/).

```bash
# einmalig einloggen
fly auth login

cd pianistinnen-app

# App initialisieren - WICHTIG: bei "Would you like to copy its configuration
# to the new app?" mit "yes" antworten, da fly.toml bereits vorbereitet ist.
# Der App-Name in fly.toml ("weltklasse-pianistinnen") ist wahrscheinlich schon
# vergeben - beim Prompt nach dem App-Namen einen eigenen, eindeutigen Namen wählen.
fly launch --no-deploy

# danach ausrollen
fly deploy

# App im Browser oeffnen
fly open
```

Spaetere Updates einfach mit `fly deploy` erneut ausrollen.

### Kosten-Hinweis
`fly.toml` ist auf `shared-cpu-1x` / 256 MB und `auto_stop_machines = "stop"` mit
`min_machines_running = 0` eingestellt — die Maschine faehrt bei Inaktivitaet herunter
und startet bei der naechsten Anfrage automatisch neu. Das passt in der Regel in
Fly.ios kostenlose Kontingente fuer kleine Projekte; Preise koennen sich aendern,
bitte aktuelle Konditionen auf fly.io/pricing pruefen.

## 6. Hintergrundbilder & mehr Inhalt (neu)

`static/images/` enthält drei vom Nutzer bereitgestellte Stockfotos (Pixabay-Lizenz):

- `bg-piano-keys.jpg` / `bg-portrait-mood.jpg` — laufen als sanft überblendender
  ("crossfade") Hintergrund hinter dem Buch, abgedunkelt und entsättigt, damit der
  Text immer gut lesbar bleibt.
- `accent-glamour.jpg` — nur als kleines, dezentes Deko-Element auf der Cover-Seite
  (bewusst nicht großflächig verwendet, da es sich um ein reines Fashion-/Glamour-
  Stockfoto ohne Bezug zu einer echten Pianistin handelt und großflächig neben echten
  Künstlerinnenporträts unpassend gewirkt hätte).

Jede Biografie hat jetzt einen dritten, redaktionellen Kontext-Absatz (`extras.py`,
Dict `EXTRA_PARAGRAPHS`) für mehr Tiefe. Der YouTube-Endpunkt liefert jetzt bis zu
**5** echte Videos pro Künstlerin (vorher 3), sofern ein `YOUTUBE_API_KEY` gesetzt ist.

## 7. KI-Chat-Assistent (neu)

Ein kontextbewusster Chat-Button unten rechts. Er weiß, welches Profil / welche Liste
gerade offen ist (wird bei jeder Nachricht live mitgeschickt) und zeigt nach einigen
Sekunden auf einem Profil einen "kann ich helfen?"-Hinweis (Usage-Tracking rein
client-seitig, keine Daten verlassen den Browser außer beim tatsächlichen Chatten).

**Setup (Groq, kostenloses Kontingent):**
```bash
fly secrets set GROQ_API_KEY=dein-groq-key
```
Key erstellen unter https://console.groq.com/keys — kein Kreditkarten-Zwang für den
kostenlosen Tier (Stand heute, bitte aktuelle Konditionen prüfen).

**Optional: echte Live-Websuche als Tool ("browser use"-Skill, hart codiert)**
Ist zusätzlich `TAVILY_API_KEY` gesetzt, bekommt das Modell ein echtes Tool
`search_live_info`, mit dem es bei Fragen nach aktuellen Konzertterminen o. Ä. aktiv
das Web durchsuchen kann (via Tavily), statt zu raten:
```bash
fly secrets set TAVILY_API_KEY=dein-tavily-key
```
Kostenloser Key unter https://tavily.com. Ohne diesen Key beantwortet der Assistent
Fragen weiterhin aus den 40 Profilen, sagt aber ehrlich, dass er keinen Live-Zugriff hat,
statt Termine zu erfinden.

*Bewusst kein autonomer Browser-Agent:* Ein echter, selbstständig klickender
Headless-Browser wäre ein eigenes, deutlich größeres Infrastrukturprojekt (Sandboxing,
Kostenkontrolle, Missbrauchsschutz). Das Such-Tool deckt den eigentlichen Bedarf
("aktuelle Infos nachschlagen") sicher und kontrolliert ab.

Lokal testen:
```bash
export GROQ_API_KEY=dein-key
export TAVILY_API_KEY=dein-key   # optional
python3 app.py
```

## 8. Hero-Bereich, Parallax & Kontaktdaten (neu)

Die Seite startet jetzt mit einem großflächigen Hero-Bild (`static/images/accent-glamour.jpg`)
mit dunklem Verlauf, drei sanft schwebenden "Parallax-Orbs" und einer Kontakt-Leiste.
Scrollt man nach unten, bewegen sich Hero-Bild und Orbs mit unterschiedlicher
Geschwindigkeit (`initParallax()` in `static/index.html`).

**Kontaktdaten:** LinkedIn, Xing und der Telegram-Bot-Link wurden aus den vom Nutzer
bereitgestellten Referenz-Repos (`landingpageFM`) übernommen — dort als echte, öffentliche
Profil-Links hinterlegt. Eine E-Mail-Adresse oder Telefonnummer war in den Repos nicht
enthalten (das dortige Kontaktformular sendet auch nicht wirklich etwas ab, rein optisch);
falls gewünscht, einfach einen weiteren `.contact-chip` mit `mailto:...`-Link in
`static/index.html` (Abschnitt `<div class="contact-bar">`) ergänzen.

## API-Endpunkte

| Endpunkt                    | Beschreibung                                  |
|------------------------------|------------------------------------------------|
| `GET /api/lists`             | Metadaten zu allen drei Listen + Anzahl        |
| `GET /api/list/<name>`       | Kuenstlerinnen einer Liste (`newcomers`\|`icons`\|`current`) |
| `GET /api/pianists`          | Alle 40 Kuenstlerinnen (unabhaengig von Liste) |
| `GET /api/pianists/<slug>`   | Einzelnes Kuenstlerinnen-Profil                |
| `GET /api/media/<slug>`      | `{images: [...bis 3...], instagram}` — live von Wikipedia |
| `GET /api/youtube/<slug>`    | `{videos: [...bis 5 echte Videos...], source}` — live von der YouTube Data API |
| `POST /api/chat`             | Kontextbewusster KI-Chat (siehe Abschnitt 7)   |
| `GET /api/health`            | Health-Check (zeigt auch, ob ein YouTube-API-Key aktiv ist) |

## 4. Echte YouTube-Videos aktivieren (optional, aber empfohlen)

Ohne API-Key zeigt die App fuer jede Kuenstlerin nur einen "Auf YouTube suchen"-Link
(kein Risiko durch erfundene/verrottete Video-Links). Mit einem kostenlosen YouTube-
Data-API-Key lädt die App fuer jede Kuenstlerin automatisch **3 echte, aktuelle Videos**:

1. Google-Cloud-Projekt anlegen: https://console.cloud.google.com/
2. "YouTube Data API v3" aktivieren (APIs & Services → Library)
3. API-Key erstellen (APIs & Services → Credentials → Create Credentials → API Key)
4. Empfehlung: den Key auf die YouTube Data API v3 einschraenken (API restrictions)
5. Als Fly.io-Secret setzen:

```bash
fly secrets set YOUTUBE_API_KEY=dein-api-key
```

Kostenlos enthaltenes Kontingent (Stand heute, bitte auf der Google-Cloud-Konsole
pruefen, da sich Kontingente aendern koennen) reicht fuer mehrere Tausend Suchanfragen
pro Tag — durch das 12h-Caching im Backend wird jede Kuenstlerin ohnehin nur alle
12 Stunden neu abgefragt, nicht bei jedem Seitenaufruf.

Lokal testen:
```bash
export YOUTUBE_API_KEY=dein-api-key
python3 app.py
```

## 5. Bildquelle, Spotify, Instagram & Presskit-Fotos

**Portraitbilder** werden live ueber die Wikipedia-`media-list`-API geladen (bis zu 3 pro
Kuenstlerin, frei lizenziert, mit automatischer Attribution).

**Presskit-/Agenturfotos werden bewusst NICHT heruntergeladen oder eingebettet.** Fotos aus
offiziellen Presskits sind fast immer mit einem Copyright-Vermerk versehen (z. B. "©
Fotograf:in") und in der Regel nur fuer redaktionelle Berichterstattung mit Namensnennung
freigegeben - nicht automatisch fuer die Einbindung in eine App wie diese. Stattdessen
verlinkt jedes Portraet auf die offizielle Presse-/Kuenstlerinnen-Seite (`press_url` in
der API), wo die Original-Pressefotos mit korrektem Copyright-Hinweis abrufbar sind.

**Spotify:** Fuer vier Kuenstlerinnen (Yuja Wang, Khatia Buniatishvili, Isata Kanneh-Mason,
Eva Gevorgyan) wurde das exakte offizielle Spotify-Artist-Profil recherchiert und verifiziert
(`extras.py`, Dict `SPOTIFY`). Fuer alle uebrigen wird automatisch ein Spotify-Suchlink
gebaut (`open.spotify.com/search/<Name>`) - bewusst kein geratener Direktlink, der ins
Leere oder zum falschen Profil fuehren koennte. Die API kennzeichnet das ueber
`spotify.verified` (`true`/`false`); das Frontend beschriftet unverifizierte Links
entsprechend als "Spotify durchsuchen".

**Instagram:** Links werden **nur** angezeigt, wenn das Profil bei der Recherche eindeutig
als offizielles Konto verifiziert werden konnte (siehe `extras.py`, Dict `INSTAGRAM`) - bei
den uebrigen Kuenstlerinnen erscheint bewusst kein Instagram-Button statt eines geratenen
Handles.

Wer weitere Profile (Spotify, Instagram, Presskit-Links) ergaenzen moechte: einfach den
jeweiligen Slug + verifizierte URL/Handle in `extras.py` eintragen.

## Daten pflegen / erweitern

Alle Inhalte liegen in `data.py` in der Liste `PIANISTS`. Jeder Eintrag hat ein Feld
`"lists"` (z. B. `["newcomers", "current"]`), das bestimmt, in welchen Ansichten die
Kuenstlerin erscheint. Die Reihenfolge der "Top 20 Aktuell"-Ansicht wird separat ueber
`CURRENT_ORDER` gesteuert. Neue Kuenstlerinnen einfach als neues Dict-Objekt anhaengen
und mit einem `wikipedia_title` versehen, damit automatisch ein Bild geladen wird.

## Methodik-Hinweis

Es gibt im klassischen Musikbetrieb keine objektive Weltrangliste. Alle drei Listen
sind redaktionell kuratiert. Alle biografischen Angaben wurden gegen offizielle
Kuenstlerinnen-Websites, Wikipedia und Wettbewerbs-/Konzertveranstalter-Quellen
geprueft; Fehler koennen trotzdem vorkommen — bei Unstimmigkeiten gerne in `data.py`
korrigieren.
