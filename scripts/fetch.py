import os, json, datetime, requests

API_KEY = os.getenv("ODDS_API_KEY")
out_path = "docs/predictions.json"

data = {
    "updated": datetime.datetime.utcnow().isoformat() + "Z",
    "games": []
}

if API_KEY:
    try:
        r = requests.get(
            "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds",
            params={"apiKey": API_KEY, "regions": "us", "markets": "h2h", "oddsFormat": "american"},
            timeout=20
        )
        games = r.json()[:5]
        for g in games:
            data["games"].append({
                "home": g.get("home_team"),
                "away": g.get("away_team"),
                "commence": g.get("commence_time")
            })
    except Exception as e:
        data["error"] = str(e)
else:
    data["error"] = "no API key"

os.makedirs("docs", exist_ok=True)
with open(out_path, "w") as f:
    json.dump(data, f, indent=2)
