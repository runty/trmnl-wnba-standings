# TRMNL WNBA Standings & Today's Games

A TRMNL recipe showing live WNBA standings by conference with team logos, plus today's game matchups with times and scores.

![WNBA](https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png)

## Features

- **Conference standings** with team logos, ranks, W-L records, and games behind
- **Today's games** with team logos, short names, records, times, and live scores
- **All 4 TRMNL layouts**: full, half horizontal, half vertical, quadrant
- **Sans-serif font** (Inter via Google Fonts)
- Data updated **every 4 hours** via GitHub Actions
- No form fields needed — works for all WNBA fans

## Layouts

### Full (800x480)
Left: both conference standings with rank, logo, team name, record, GB. Right: today's games with away/home logos, names, records, time, and scores.

### Half Horizontal (800x240)
Compact standings on the left (logo, abbreviation, record). Today's games on the right (up to 3).

### Half Vertical (400x480)
Standings table for both conferences. Today's games at the bottom (up to 2).

### Quadrant (400x240)
Top 5 teams per conference with logos and records.

## Setup

### 1. Fork this repository

### 2. Enable GitHub Pages
Settings > Pages > Source: **GitHub Actions**

### 3. Run the data fetch
Actions > "Update WNBA Standings Data" > Run workflow

### 4. Create a Private Plugin on TRMNL
1. Plugins > Private Plugin
2. Strategy: **Polling**
3. Polling URL: `https://YOUR_USERNAME.github.io/trmnl-wnba-standings/standings.json`
4. Paste `form_fields.yml` into Custom Fields
5. Paste templates into markup tabs (shared, full, half horizontal, half vertical, quadrant)
6. Save and **Force Refresh**

## Data Source

ESPN public API (`site.api.espn.com`). Standings and scoreboard endpoints. No authentication required.

## Plugin Icon

`https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png`
