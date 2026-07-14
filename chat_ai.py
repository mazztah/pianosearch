# -*- coding: utf-8 -*-
"""
chat_ai.py — Kontextbewusster KI-Chat für die Pianistinnen-App.

Architektur (angelehnt an ein bewährtes Muster aus einem anderen Projekt):
- Groq (OpenAI-kompatible Chat-API) als LLM-Backend, kostenloses Kontingent verfuegbar.
- Session-Historie pro Browser-Tab (in-memory, TTL-begrenzt).
- Der Frontend-Kontext (welches Profil/Liste gerade offen ist) wird bei jeder Anfrage
  live in den System-Prompt eingespeist -> der Assistent "weiss", was der Mensch gerade
  ansieht, ohne dass wir 40 einzelne Prompts brauchen.
- ECHTES Tool-Calling fuer Live-Infos ("browser use"-aehnlicher Skill, hart codiert):
  Ist TAVILY_API_KEY gesetzt, bekommt das Modell ein Tool `search_live_info`, mit dem es
  aktuelle Konzerttermine/News zu einer Kuenstlerin nachschlagen kann, statt zu raten.
  Ohne Key funktioniert der Chat weiterhin (nur ohne Live-Websuche) - siehe README.

Warum kein autonomer "Browser-Agent"?
  Ein echter, selbststaendig im Web klickender Browser-Agent (Headless-Browser-Steuerung)
  ist eine eigene, deutlich groessere Infrastruktur (Sandboxing, Kostenkontrolle,
  Missbrauchsschutz) und wuerde den Rahmen dieses Projekts sprengen. Stattdessen bekommt
  das Modell ein kontrolliertes, sicheres Such-Tool mit klar begrenztem Scope - das deckt
  den eigentlichen Bedarf ("aktuelle Infos nachschlagen") ab, ohne unkontrollierten
  Programmcode im Browser des Nutzers auszufuehren.
"""
import os
import time
import json
import logging
from collections import defaultdict

import requests

logger = logging.getLogger("chat_ai")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
TAVILY_SEARCH_URL = "https://api.tavily.com/search"
MODEL_LIST = ["llama-3.3-70b-versatile", "llama3-70b-8192"]

MAX_HISTORY_MESSAGES = 16
SESSION_TTL_SECONDS = 60 * 60 * 2
REQUEST_TIMEOUT = 20

_chat_histories: dict[str, list] = defaultdict(list)
_last_seen: dict[str, float] = {}

BASE_SYSTEM_PROMPT = """Du bist der "Klavier-Assistent" auf einer Webseite über Weltklasse-Pianistinnen \
(40 Portraits in drei Listen: "Alltime Icons", "Junge Newcomerinnen", "Aktuell - Stand Juli 2026").

Sprich Deutsch (außer die Person schreibt Englisch), sei warm, kompetent, aber knapp \
(meist 2-5 Sätze). Du kennst die Biografien, Auszeichnungen und Repertoire-Schwerpunkte \
der 40 Künstlerinnen auf dieser Seite. Erfinde KEINE Wettbewerbsergebnisse, Daten oder \
Zitate, die du nicht sicher weißt - sag lieber ehrlich "das weiß ich nicht genau" als zu \
raten. Wenn jemand nach aktuellen Konzertterminen fragt und dir das Such-Tool zur \
Verfügung steht, nutze es aktiv, statt zu spekulieren.

Du darfst Empfehlungen aussprechen ("wenn dir X gefällt, hör dir auch Y an") basierend auf \
Repertoire-Überschneidungen. Bleib beim Thema Pianistinnen/klassische Musik; bei Off-Topic-\
Fragen lenke freundlich zurück.
"""

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_live_info",
        "description": (
            "Sucht im Web nach aktuellen, live Informationen - z. B. Konzerttermine, "
            "Tourneedaten, neue Alben oder aktuelle News zu einer bestimmten Pianistin. "
            "Nutze dieses Tool, wenn nach 'aktuellen' oder 'kommenden' Terminen/News gefragt "
            "wird, die du nicht sicher aus deinem Wissen beantworten kannst."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Präzise Suchanfrage, z. B. 'Alexandra Dovgan Konzerte 2026'",
                }
            },
            "required": ["query"],
        },
    },
}


def _search_live_info(query: str) -> str:
    if not TAVILY_API_KEY:
        return "Live-Websuche ist auf diesem Server nicht konfiguriert (kein TAVILY_API_KEY)."
    try:
        resp = requests.post(
            TAVILY_SEARCH_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 4,
                "include_answer": True,
            },
            timeout=REQUEST_TIMEOUT,
        )
        if not resp.ok:
            return f"Websuche fehlgeschlagen (Status {resp.status_code})."
        data = resp.json()
        parts = []
        if data.get("answer"):
            parts.append(f"Kurzantwort: {data['answer']}")
        for r in data.get("results", [])[:4]:
            parts.append(f"- {r.get('title')}: {r.get('content', '')[:220]} ({r.get('url')})")
        return "\n".join(parts) if parts else "Keine relevanten Ergebnisse gefunden."
    except requests.RequestException as exc:
        logger.warning("Tavily-Suche fehlgeschlagen: %s", exc)
        return "Websuche derzeit nicht erreichbar."


def _build_system_prompt(context: dict) -> str:
    prompt = BASE_SYSTEM_PROMPT
    current_artist = (context or {}).get("current_artist")
    active_list = (context or {}).get("active_list")
    viewed = (context or {}).get("viewed_artists") or []

    ctx_lines = []
    if current_artist:
        ctx_lines.append(f"Die Person betrachtet GERADE das Profil von: {current_artist}. "
                          f"Beziehe dich darauf, falls die Frage dazu passt (z. B. 'wer ist das', 'erzähl mehr').")
    if active_list:
        ctx_lines.append(f"Aktuell geöffnete Listenansicht: {active_list}.")
    if viewed:
        ctx_lines.append(f"Bereits angesehene Profile in dieser Sitzung: {', '.join(viewed[:10])}.")
    if not TAVILY_API_KEY:
        ctx_lines.append("Hinweis: Live-Websuche ist aktuell nicht verfügbar - beantworte Fragen zu "
                          "aktuellen Terminen nur mit dem Hinweis, dass du dafür keinen Live-Zugriff hast.")

    if ctx_lines:
        prompt += "\n\n=== AKTUELLER SEITEN-KONTEXT ===\n" + "\n".join(ctx_lines)
    return prompt


def _ensure_history(session_id: str, context: dict) -> list:
    now = time.time()
    last = _last_seen.get(session_id)
    system_msg = {"role": "system", "content": _build_system_prompt(context)}
    if not _chat_histories[session_id] or (last and now - last > SESSION_TTL_SECONDS):
        _chat_histories[session_id] = [system_msg]
    else:
        # System-Prompt bei jeder Anfrage aktualisieren, da sich der Seiten-Kontext
        # (welches Profil offen ist) zwischen Nachrichten aendern kann.
        _chat_histories[session_id][0] = system_msg
    _last_seen[session_id] = now
    return _chat_histories[session_id]


def generate_reply(session_id: str, message: str, context: dict) -> str:
    if not GROQ_API_KEY:
        return "Der KI-Chat ist aktuell nicht konfiguriert (fehlender GROQ_API_KEY). Sieh dir gerne die Profile direkt an!"

    history = _ensure_history(session_id, context)
    history.append({"role": "user", "content": message})
    if len(history) > MAX_HISTORY_MESSAGES:
        history[:] = [history[0]] + history[-(MAX_HISTORY_MESSAGES - 1):]

    tools = [SEARCH_TOOL] if TAVILY_API_KEY else None
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    for model_name in MODEL_LIST:
        try:
            payload = {"model": model_name, "messages": history, "temperature": 0.6, "max_tokens": 600}
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"

            resp = requests.post(GROQ_CHAT_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
            if not resp.ok:
                logger.warning("Groq-Fehler (%s) mit Modell %s: %s", resp.status_code, model_name, resp.text[:300])
                continue

            data = resp.json()
            choice = data["choices"][0]["message"]
            tool_calls = choice.get("tool_calls")

            if tool_calls:
                # Tool-Ausfuehrung + zweiter Modellaufruf mit dem Ergebnis
                history.append(choice)
                for call in tool_calls:
                    if call["function"]["name"] == "search_live_info":
                        args = json.loads(call["function"].get("arguments") or "{}")
                        result = _search_live_info(args.get("query", message))
                        history.append({
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "content": result,
                        })
                follow_up = requests.post(
                    GROQ_CHAT_URL, headers=headers,
                    json={"model": model_name, "messages": history, "temperature": 0.6, "max_tokens": 600},
                    timeout=REQUEST_TIMEOUT,
                )
                if follow_up.ok:
                    final = follow_up.json()["choices"][0]["message"]["content"].strip()
                    history.append({"role": "assistant", "content": final})
                    return final or "…"
                continue

            reply = (choice.get("content") or "").strip() or "Dazu ist mir gerade nichts Sinnvolles eingefallen."
            history.append({"role": "assistant", "content": reply})
            return reply

        except requests.RequestException as exc:
            logger.warning("Groq-Anfrage fehlgeschlagen mit %s: %s", model_name, exc)
            continue
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            logger.warning("Unerwartete Groq-Antwortstruktur mit %s: %s", model_name, exc)
            continue

    return "🟠 Der KI-Chat ist gerade nicht erreichbar. Bitte versuch es in Kürze erneut."
