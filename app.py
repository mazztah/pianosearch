# -*- coding: utf-8 -*-
"""
Weltklasse Pianistinnen — Flask-Backend

Endpunkte:
  GET /                          -> Frontend (static/index.html)
  GET /api/lists                 -> Metadaten zu den drei Listen (Titel, Untertitel, Anzahl)
  GET /api/list/<name>           -> Kuenstlerinnen einer Liste ("newcomers" | "icons" | "current")
  GET /api/pianists              -> alle Kuenstlerinnen
  GET /api/pianists/<slug>       -> einzelne Kuenstlerin
  GET /api/media/<slug>          -> {"images": [...bis zu 3...], "instagram": handle|null}
                                     Bilder werden live von der Wikipedia media-list-API
                                     geholt (frei lizenziert) und 12h gecacht.
  GET /api/youtube/<slug>        -> {"videos": [...bis zu 5 echte Videos...], "source": "api"|"fallback"}
                                     Nutzt die YouTube Data API v3, falls die Umgebungsvariable
                                     YOUTUBE_API_KEY gesetzt ist (siehe README). Ohne Key liefert
                                     der Endpunkt eine leere Liste + einen Fallback-Suchlink,
                                     damit NIE erfundene/geratene Video-URLs ausgeliefert werden.
  GET /api/health                -> Health-Check fuer Fly.io

Warum kein direktes Hosting von Presse-/Agenturfotos?
  Presse- und Agenturfotos sind in aller Regel urheberrechtlich geschuetzt. Wikipedia-
  Bilder sind dagegen entweder gemeinfrei oder frei lizenziert (z. B. CC-BY-SA). Fehlt
  ein Bild, zeigt das Frontend einen Monogramm-Platzhalter statt eines nicht lizenzierten Fotos.

Warum keine hart codierten YouTube-Video-IDs?
  Von einem Sprachmodell "erinnerte" YouTube-Video-IDs sind ein bekanntes Fehlerrisiko
  (Halluzination) und verrotten zudem (Videos werden geloescht/privat). Ein Live-Abruf ist
  die einzige Methode, die garantiert echte, aktuell gueltige Links liefert.
"""
import os
import time
import logging

from flask import Flask, jsonify, request, send_from_directory, abort
import requests

from data import PIANISTS, CURRENT_ORDER
from extras import INSTAGRAM, LISTENING_NOTES, SPOTIFY, PRESS_URL, EXTRA_PARAGRAPHS
import chat_ai

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pianistinnen")

app = Flask(__name__, static_folder="static", static_url_path="")

WIKIPEDIA_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKIPEDIA_MEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/media-list/{title}"
YOUTUBE_SEARCH_API = "https://www.googleapis.com/youtube/v3/search"
REQUEST_TIMEOUT = 6  # seconds
CACHE_TTL = 60 * 60 * 12  # 12 Stunden
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

_media_cache = {}    # slug -> (timestamp, payload)
_youtube_cache = {}  # slug -> (timestamp, payload)
_PIANISTS_BY_SLUG = {p["slug"]: p for p in PIANISTS}

LIST_META = {
    "newcomers": {
        "key": "newcomers",
        "title": "Top 25 Junge Newcomerinnen",
        "subtitle": "All-Time High 2026",
        "description": "Nachwuchspianistinnen im internationalen Aufstieg — von Wettbewerbs-Debüts bis zu ersten großen Orchesterengagements.",
    },
    "icons": {
        "key": "icons",
        "title": "Top 25 Alltime High",
        "subtitle": "2026",
        "description": "Etablierte Weltklasse-Pianistinnen und historische Legenden, die das klassische Klavierspiel nachhaltig geprägt haben.",
    },
    "current": {
        "key": "current",
        "title": "Top 20 Aktuell",
        "subtitle": "Stand: Juli 2026",
        "description": "Redaktionelles Schlaglicht auf Künstlerinnen, die im Juli 2026 durch neue Alben, Debüts oder Konzerttermine besonders im Gespräch sind.",
    },
}


def _spotify_url(p):
    verified = SPOTIFY.get(p["slug"])
    if verified:
        return {"url": verified, "verified": True}
    # Fallback: Spotify-Suchergebnis fuer den Namen - niemals eine geratene Artist-ID
    query = requests.utils.quote(p["name"])
    return {"url": f"https://open.spotify.com/search/{query}", "verified": False}


def _full_bio(p):
    extra = EXTRA_PARAGRAPHS.get(p["slug"])
    return p["bio"] + ("\n\n" + extra if extra else "")


def _public_fields(p):
    return {
        "slug": p["slug"],
        "name": p["name"],
        "flag": p["flag"],
        "born": p["born"],
        "bio": _full_bio(p),
        "listening_note": LISTENING_NOTES.get(p["slug"]),
        "awards": p["awards"],
        "focus": p["focus"],
        "current_note": p.get("current_note"),
        "official_url": p["official_url"],
        "official_label": p["official_label"],
        "youtube_search": p["youtube"],
        "instagram": INSTAGRAM.get(p["slug"]),
        "spotify": _spotify_url(p),
        "press_url": PRESS_URL.get(p["slug"], p["official_url"]),
        "lists": p["lists"],
    }


@app.get("/api/lists")
def api_lists():
    out = []
    for key, meta in LIST_META.items():
        count = len(CURRENT_ORDER) if key == "current" else sum(1 for p in PIANISTS if key in p["lists"])
        out.append({**meta, "count": count})
    return jsonify(out)


@app.get("/api/list/<name>")
def api_list(name):
    if name not in LIST_META:
        abort(404)
    if name == "current":
        ordered = [_PIANISTS_BY_SLUG[s] for s in CURRENT_ORDER if s in _PIANISTS_BY_SLUG]
    else:
        ordered = [p for p in PIANISTS if name in p["lists"]]
    return jsonify({"meta": LIST_META[name], "items": [_public_fields(p) for p in ordered]})


@app.get("/api/pianists")
def api_pianists():
    return jsonify([_public_fields(p) for p in PIANISTS])


@app.get("/api/pianists/<slug>")
def api_pianist_detail(slug):
    p = _PIANISTS_BY_SLUG.get(slug)
    if not p:
        abort(404)
    return jsonify(_public_fields(p))


IMAGE_EXT_BLOCKLIST = (".svg", ".ogg", ".oga", ".ogv", ".webm", ".mid")


@app.get("/api/media/<slug>")
def api_media(slug):
    p = _PIANISTS_BY_SLUG.get(slug)
    if not p:
        abort(404)

    cached = _media_cache.get(slug)
    if cached and (time.time() - cached[0]) < CACHE_TTL:
        return jsonify(cached[1])

    images = []
    title = p.get("wikipedia_title")
    headers = {"User-Agent": "weltklasse-pianistinnen/1.0 (educational demo)"}

    if title:
        encoded = requests.utils.quote(title)
        # 1) Haupt-Vorschaubild aus der Zusammenfassung (meist das Infobox-Foto)
        try:
            resp = requests.get(WIKIPEDIA_SUMMARY_API.format(title=encoded), timeout=REQUEST_TIMEOUT, headers=headers)
            if resp.ok:
                d = resp.json()
                thumb = d.get("thumbnail", {}).get("source")
                page_url = d.get("content_urls", {}).get("desktop", {}).get("page")
                if thumb:
                    images.append({"url": thumb, "attribution": page_url})
        except requests.RequestException as exc:
            log.warning("media-summary fehlgeschlagen fuer %s: %s", slug, exc)

        # 2) Weitere Bilder aus der media-list des Artikels (bis insgesamt 3)
        try:
            resp = requests.get(WIKIPEDIA_MEDIA_API.format(title=encoded), timeout=REQUEST_TIMEOUT, headers=headers)
            if resp.ok:
                d = resp.json()
                page_url = f"https://en.wikipedia.org/wiki/{encoded}"
                for item in d.get("items", []):
                    if len(images) >= 3:
                        break
                    if item.get("type") != "image":
                        continue
                    src = (item.get("original") or {}).get("source") or ""
                    if not src or src.lower().endswith(IMAGE_EXT_BLOCKLIST):
                        continue
                    if src.startswith("//"):
                        src = "https:" + src
                    if any(im["url"] == src for im in images):
                        continue
                    images.append({"url": src, "attribution": page_url})
        except requests.RequestException as exc:
            log.warning("media-list fehlgeschlagen fuer %s: %s", slug, exc)

    payload = {"images": images, "instagram": INSTAGRAM.get(slug)}
    _media_cache[slug] = (time.time(), payload)
    return jsonify(payload)


@app.get("/api/youtube/<slug>")
def api_youtube(slug):
    p = _PIANISTS_BY_SLUG.get(slug)
    if not p:
        abort(404)

    cached = _youtube_cache.get(slug)
    if cached and (time.time() - cached[0]) < CACHE_TTL:
        return jsonify(cached[1])

    payload = {"videos": [], "source": "fallback"}

    if YOUTUBE_API_KEY:
        try:
            params = {
                "part": "snippet",
                "q": f"{p['name']} piano",
                "type": "video",
                "maxResults": 5,
                "order": "relevance",
                "key": YOUTUBE_API_KEY,
                "safeSearch": "strict",
            }
            resp = requests.get(YOUTUBE_SEARCH_API, params=params, timeout=REQUEST_TIMEOUT)
            if resp.ok:
                items = resp.json().get("items", [])
                videos = []
                for it in items:
                    vid = it.get("id", {}).get("videoId")
                    sn = it.get("snippet", {})
                    if not vid:
                        continue
                    videos.append({
                        "videoId": vid,
                        "title": sn.get("title"),
                        "channel": sn.get("channelTitle"),
                        "thumbnail": (sn.get("thumbnails", {}).get("medium") or sn.get("thumbnails", {}).get("default") or {}).get("url"),
                        "url": f"https://www.youtube.com/watch?v={vid}",
                    })
                if videos:
                    payload = {"videos": videos, "source": "api"}
            else:
                log.warning("YouTube API Fehler (%s) fuer %s", resp.status_code, slug)
        except requests.RequestException as exc:
            log.warning("YouTube-Abruf fehlgeschlagen fuer %s: %s", slug, exc)

    _youtube_cache[slug] = (time.time(), payload)
    return jsonify(payload)


@app.post("/api/chat")
def api_chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Bitte gib eine Nachricht ein."}), 400
    message = message[:2000]

    session_id = payload.get("session_id") or request.remote_addr or "anon"
    context = {
        "current_artist": payload.get("current_artist"),
        "active_list": payload.get("active_list"),
        "viewed_artists": payload.get("viewed_artists") or [],
    }
    try:
        reply = chat_ai.generate_reply(session_id, message, context)
    except Exception:
        log.exception("Fehler in /api/chat")
        reply = "Entschuldigung, es gab ein technisches Problem."
    return jsonify({"reply": reply})


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "count": len(PIANISTS),
        "youtube_api": bool(YOUTUBE_API_KEY),
        "chat_api": bool(os.environ.get("GROQ_API_KEY")),
        "live_search": bool(os.environ.get("TAVILY_API_KEY")),
    })


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
