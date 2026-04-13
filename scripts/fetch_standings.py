#!/usr/bin/env python3
"""Fetch WNBA standings and today's games from ESPN API for TRMNL."""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen

ESPN_BASE = "https://site.api.espn.com/apis"
WNBA_LOGO = "https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png"


def fetch_json(url):
    req = Request(url, headers={"User-Agent": "TRMNL-WNBA-Standings/1.0"})
    with urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def get_logo(team):
    """Get team logo URL, with fallback."""
    logos = team.get("logos", [])
    if logos:
        return logos[0].get("href", WNBA_LOGO)
    logo = team.get("logo", "")
    if logo:
        return logo
    abbr = team.get("abbreviation", "")
    if abbr and abbr != "?":
        return f"https://a.espncdn.com/i/teamlogos/wnba/500/{abbr.lower()}.png"
    return WNBA_LOGO


def fetch_standings():
    """Fetch current WNBA standings by conference."""
    data = fetch_json(f"{ESPN_BASE}/v2/sports/basketball/wnba/standings")

    conferences = []
    for group in data.get("children", []):
        conf_name = group.get("abbreviation", group.get("name", ""))
        entries = []
        for i, entry in enumerate(group.get("standings", {}).get("entries", [])):
            team = entry.get("team", {})
            stats = {s["name"]: s["displayValue"] for s in entry.get("stats", [])}
            entries.append({
                "rank": i + 1,
                "name": team.get("displayName", ""),
                "short_name": team.get("shortDisplayName", ""),
                "abbr": team.get("abbreviation", ""),
                "logo": get_logo(team),
                "wins": stats.get("wins", "0"),
                "losses": stats.get("losses", "0"),
                "record": stats.get("overall", "0-0"),
                "pct": stats.get("winPercent", ".000"),
                "gb": stats.get("gamesBehind", "-"),
                "streak": stats.get("streak", "-"),
                "home": stats.get("Home", "0-0"),
                "road": stats.get("Road", "0-0"),
                "conf": stats.get("vs. Conf.", "0-0"),
            })
        conferences.append({
            "name": group.get("name", ""),
            "abbr": conf_name,
            "teams": entries,
        })
    return conferences


def fetch_todays_games():
    """Fetch today's WNBA games from the scoreboard."""
    data = fetch_json(f"{ESPN_BASE}/site/v2/sports/basketball/wnba/scoreboard")

    games = []
    for event in data.get("events", []):
        comp = event.get("competitions", [{}])[0]
        status = comp.get("status", {}).get("type", {})
        venue = comp.get("venue", {})

        away_team = None
        home_team = None
        for c in comp.get("competitors", []):
            t = c.get("team", {})
            record = ""
            for r in c.get("records", []):
                if r.get("type") == "total":
                    record = r.get("summary", "")

            team_data = {
                "name": t.get("displayName", ""),
                "short_name": t.get("shortDisplayName", t.get("name", "")),
                "abbr": t.get("abbreviation", ""),
                "logo": get_logo(t),
                "score": c.get("score", ""),
                "record": record,
            }
            if c.get("homeAway") == "away":
                away_team = team_data
            else:
                home_team = team_data

        if not away_team or not home_team:
            continue

        short_detail = status.get("shortDetail", "")
        try:
            time_part = short_detail.split(" - ")[1] if " - " in short_detail else short_detail
        except IndexError:
            time_part = short_detail

        completed = status.get("completed", False)
        state = status.get("state", "pre")

        games.append({
            "away": away_team,
            "home": home_team,
            "time": time_part,
            "status": status.get("description", "Scheduled"),
            "detail": status.get("detail", ""),
            "short_detail": short_detail,
            "completed": completed,
            "in_progress": state == "in",
            "venue": venue.get("fullName", ""),
            "city": f"{venue.get('address', {}).get('city', '')}, {venue.get('address', {}).get('state', '')}".strip(", "),
        })

    return games


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "api")
    os.makedirs(out_dir, exist_ok=True)

    now = datetime.now(timezone.utc)

    try:
        conferences = fetch_standings()
        print(f"Standings: {sum(len(c['teams']) for c in conferences)} teams across {len(conferences)} conferences")
    except Exception as e:
        print(f"ERR standings: {e}", file=sys.stderr)
        conferences = []

    try:
        games = fetch_todays_games()
        print(f"Today's games: {len(games)}")
    except Exception as e:
        print(f"ERR scoreboard: {e}", file=sys.stderr)
        games = []

    # Build combined standings sorted by win pct, then wins
    all_teams = []
    for conf in conferences:
        for team in conf["teams"]:
            team["conf"] = conf["abbr"]
            all_teams.append(team)
    all_teams.sort(key=lambda t: (-float(t["pct"].lstrip(".")), -int(t["wins"])))
    for i, team in enumerate(all_teams):
        team["overall_rank"] = i + 1

    result = {
        "conferences": conferences,
        "standings": all_teams,
        "games": games,
        "games_count": len(games),
        "date": now.strftime("%B %d, %Y"),
        "date_short": now.strftime("%m/%d"),
        "updated": now.strftime("%Y-%m-%d %H:%M UTC"),
    }

    path = os.path.join(out_dir, "standings.json")
    with open(path, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    print(f"Done. Written to {path}")


if __name__ == "__main__":
    main()
