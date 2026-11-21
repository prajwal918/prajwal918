#!/usr/bin/env python3
"""
scripts/update_dsa_card.py
Fetches live LeetCode GraphQL & Codeforces REST stats and renders
dark/light TokyoNight SVG telemetry cards plus a daily CS engineering tip.
"""
from __future__ import annotations
import datetime as dt
import html
import json
import os
import pathlib
import time
import urllib.error
import urllib.request

LEETCODE_USER = os.getenv("LEETCODE_USER", "prajwal918")
CODEFORCES_USER = os.getenv("CODEFORCES_USER", "prajwal918")
OUTPUT_DIR = pathlib.Path("assets/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CS_TIPS = [
    ("TCP/IP", "Set SO_REUSEADDR before bind() so restarted servers reclaim TIME_WAIT sockets."),
    ("POSIX", "Restore struct termios via RAII + SIGINT handlers to prevent orphaned raw TTYs."),
    ("DAA", "Dijkstra breaks on negative edges due to greedy settling; switch to Bellman-Ford."),
    ("SPRING", "Set spring.jpa.open-in-view=false to avoid holding DB pools during JSON writes."),
    ("TOC", "Regular languages fail nested parentheses by the Pumping Lemma; use a PDA."),
    ("MYSQL", "Composite B+Tree indexes obey leftmost-prefix: place equality columns before ranges."),
    ("8086/CPU", "Pad hot atomics to 64-byte cache lines to eliminate false sharing across cores."),
]

def http_json(url: str, payload: dict | None = None, headers: dict | None = None) -> dict:
    req_headers = {"User-Agent": "prajwal918-profile-bot/1.0"}
    if headers:
        req_headers.update(headers)
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=req_headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_leetcode(username: str) -> dict:
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum { difficulty count }
        }
      }
    }
    """
    try:
        res = http_json(
            "https://leetcode.com/graphql",
            payload={"query": query, "variables": {"username": username}},
            headers={"Referer": f"https://leetcode.com/u/{username}/"},
        )
        matched = res.get("data", {}).get("matchedUser")
        if not matched:
            return {"ok": False, "all": 0, "easy": 0, "medium": 0, "hard": 0}
        counts = {
            row["difficulty"]: row["count"]
            for row in matched["submitStats"]["acSubmissionNum"]
        }
        return {
            "ok": True,
            "all": counts.get("All", 0),
            "easy": counts.get("Easy", 0),
            "medium": counts.get("Medium", 0),
            "hard": counts.get("Hard", 0),
        }
    except Exception:
        return {"ok": False, "all": 0, "easy": 0, "medium": 0, "hard": 0}

def fetch_codeforces(handle: str) -> dict:
    try:
        info = http_json(f"https://codeforces.com/api/user.info?handles={handle}")
        user = info.get("result", [{}])[0]
        time.sleep(2.1)  # Respect Codeforces 1 req / 2s rate limit
        status = http_json(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000")
        solved = {
            f"{sub['problem'].get('contestId')}-{sub['problem'].get('index')}"
            for sub in status.get("result", [])
            if sub.get("verdict") == "OK"
        }
        return {
            "ok": True,
            "rating": user.get("rating", 0),
            "max_rating": user.get("maxRating", 0),
            "rank": user.get("rank", "unrated"),
            "solved": len(solved),
        }
    except Exception:
        return {"ok": False, "rating": 0, "max_rating": 0, "rank": "unrated", "solved": 0}

def render_svg(lc: dict, cf: dict, tip_topic: str, tip_text: str, dark: bool) -> str:
    bg = "#1a1b26" if dark else "#eff1f5"
    card = "#24283b" if dark else "#e6e9ef"
    fg = "#c0caf5" if dark else "#343b58"
    muted = "#9aa5ce" if dark else "#5c5f77"
    accent = "#7aa2f7" if dark else "#2959aa"
    green = "#9ece6a" if dark else "#385f0d"
    amber = "#e0af68" if dark else "#8f5e15"
    red = "#f7768e" if dark else "#8c4351"
    border = "#2e3440" if dark else "#dce0e8"
    
    updated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d UTC")
    
    lc_line = (
        f"Total {lc['all']} | Easy {lc['easy']} · Med {lc['medium']} · Hard {lc['hard']}"
        if lc["ok"] and lc["all"] > 0
        else f"Active Solver @{LEETCODE_USER} · Grind In Progress"
    )
    cf_line = (
        f"Rating {cf['rating']} (Max {cf['max_rating']}) · {cf['rank'].title()} · {cf['solved']} AC"
        if cf["ok"] and cf["rating"] > 0
        else f"Handle @{CODEFORCES_USER} · Div 2 / Div 3 Cadet"
    )
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="172" viewBox="0 0 800 172" role="img" aria-label="Daily Competitive Programming and Systems Digest">
  <rect width="800" height="172" rx="12" fill="{bg}" stroke="{border}" stroke-width="1"/>
  <rect x="16" y="16" width="376" height="82" rx="8" fill="{card}"/>
  <rect x="408" y="16" width="376" height="82" rx="8" fill="{card}"/>
  <rect x="16" y="110" width="768" height="46" rx="8" fill="{card}"/>
  
  <!-- LeetCode Panel -->
  <text x="32" y="42" fill="{accent}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" font-weight="700">LEETCODE GRAPHQL TELEMETRY</text>
  <text x="32" y="68" fill="{fg}" font-family="system-ui,-apple-system,sans-serif" font-size="14" font-weight="600">{html.escape(lc_line)}</text>
  <circle cx="36" cy="84" r="4" fill="{green}"/><text x="44" y="87" fill="{muted}" font-family="system-ui,-apple-system,sans-serif" font-size="11">Easy</text>
  <circle cx="84" cy="84" r="4" fill="{amber}"/><text x="92" y="87" fill="{muted}" font-family="system-ui,-apple-system,sans-serif" font-size="11">Med</text>
  <circle cx="130" cy="84" r="4" fill="{red}"/><text x="138" y="87" fill="{muted}" font-family="system-ui,-apple-system,sans-serif" font-size="11">Hard</text>
  
  <!-- Codeforces Panel -->
  <text x="424" y="42" fill="{accent}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" font-weight="700">CODEFORCES PUBLIC API</text>
  <text x="424" y="68" fill="{fg}" font-family="system-ui,-apple-system,sans-serif" font-size="14" font-weight="600">{html.escape(cf_line)}</text>
  <text x="424" y="88" fill="{muted}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11">Synced {updated}</text>
  
  <!-- Daily CS Tip -->
  <text x="32" y="138" fill="{accent}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" font-weight="700">[{html.escape(tip_topic)}]</text>
  <text x="140" y="138" fill="{fg}" font-family="system-ui,-apple-system,sans-serif" font-size="12.5">{html.escape(tip_text)}</text>
</svg>
"""

def main() -> None:
    lc = fetch_leetcode(LEETCODE_USER)
    cf = fetch_codeforces(CODEFORCES_USER)
    day_index = dt.datetime.now(dt.timezone.utc).timetuple().tm_yday % len(CS_TIPS)
    topic, tip = CS_TIPS[day_index]
    
    dark_svg = render_svg(lc, cf, topic, tip, True)
    light_svg = render_svg(lc, cf, topic, tip, False)
    
    (OUTPUT_DIR / "dsa-digest-dark.svg").write_text(dark_svg, encoding="utf-8")
    (OUTPUT_DIR / "dsa-digest-light.svg").write_text(light_svg, encoding="utf-8")
    print("Successfully generated dsa-digest-dark.svg and dsa-digest-light.svg")

if __name__ == "__main__":
    main()
