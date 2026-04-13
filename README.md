# TRMNL WNBA Standings & Today's Games

A TRMNL recipe showing live WNBA standings by conference with team logos, plus today's game matchups with times and scores.

![WNBA](https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png)

## Features

- **Conference standings** with team logos, ranks, W-L records, games behind, and streak
- **Today's games** (full layout) with team logos, short names, records, times, and live scores in a 2-column grid
- **All 4 TRMNL layouts**: full, half horizontal, half vertical, quadrant
- **Sans-serif font** (Inter via Google Fonts)
- **Zero inline styles** — uses TRMNL Framework classes + minimal custom CSS
- Data updated **every 4 hours** via GitHub Actions
- No form fields needed — works for all WNBA fans

## Layouts

### Full (800x480)
Left (40%): both conference standings with rank, logo, team name, record, GB, and streak. Tight row spacing to fit all 15 teams. Right (60%): today's games in a 2-column grid with away/home logos, short names, records, and times. Scores shown for completed/in-progress games.

### Half Horizontal (800x240)
West conference on the left, East on the right, separated by a divider. Compact rows with rank, logo, short name, record, and GB. Title bar shows "WNBA Standings (West, East)".

### Half Vertical (400x480)
Both conferences stacked vertically with conference names as headers. Rank, logo, short name, record, GB, and streak columns.

### Quadrant (400x240)
West on left, East on right. Compact with rank, logo, short name, and GB. Title bar shows "WNBA Standings (W, E)".

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

## Project Structure

```
trmnl-wnba-standings/
├── .github/workflows/
│   ├── pages.yml              # Deploy to GitHub Pages (with success check)
│   └── update-data.yml        # Fetch data every 4 hours
├── api/
│   └── standings.json         # Generated data file
├── scripts/
│   └── fetch_standings.py     # ESPN API fetcher for standings + scoreboard
├── templates/
│   ├── shared.liquid          # Google Fonts, custom CSS classes
│   ├── full.liquid            # Conference standings + today's games grid
│   ├── half_horizontal.liquid # West left, East right
│   ├── half_vertical.liquid   # Both conferences stacked
│   └── quadrant.liquid        # Compact West/East with GB
├── form_fields.yml            # Author bio with sports category
├── settings.yml               # Plugin metadata
└── README.md
```

## Data Source

ESPN public API (`site.api.espn.com`). Standings and scoreboard endpoints. No authentication required. Data includes:

- Conference standings with ranks, W-L records, win %, games behind, streak
- Today's game matchups with team names, logos, records, times, venues
- Live scores for in-progress and completed games

## Plugin Icon

`https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png`

## Technical Notes

- Tight row spacing (`tbl-tight` class with 1px vertical padding) fits all 15 teams
- Combined standings sorted by win % available as `standings` array for unified ranking
- Conference standings available as `conferences` array for split views
- Non-WNBA opponents (exhibitions) use WNBA league logo as fallback
- Pages deployment only triggers on successful data updates
