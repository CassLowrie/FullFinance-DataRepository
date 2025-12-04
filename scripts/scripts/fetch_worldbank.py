import os
import csv
import time
import requests
from pathlib import Path

DATA_DIR = Path("data/worldbank")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Code/Endpoint format expected: INDICATOR:COUNTRY
# Example: NY.GDP.MKTP.KD:CHN
def parse_code_endpoint(code_endpoint: str):
    if ":" not in code_endpoint:
        raise ValueError("World Bank Code/Endpoint must look like INDICATOR:COUNTRY (e.g., NY.GDP.MKTP.KD:CHN)")
    indicator, country = code_endpoint.split(":", 1)
    return indicator.strip(), country.strip()

def fetch_worldbank(indicator: str, country: str):
    # Returns JSON from WB API (no key needed)
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=20000"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def save_series(indicator: str, country: str, data_json: dict):
    out = [["Date","Value","Indicator","Country"]]
    # WB JSON structure: [metadata, [ {date, value, ...}, ... ]]
    series = data_json[1] if len(data_json) > 1 and isinstance(data_json[1], list) else []
    for row in series:
        if row.get("value") is None:
            continue
        out.append([row.get("date",""), row.get("value",""), indicator, country])

    # Sort ascending by date (year)
    header, body = out[0], out[1:]
    body_sorted = sorted(body, key=lambda r: r[0])
    out_rows = [header] + body_sorted

    out_path = DATA_DIR / f"{indicator}_{country}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(out_rows)
    return out_path

def load_series_from_csv(csv_path: Path):
    series = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("Fetch Method","").strip().upper() == "WB_API"
                and row.get("Code/Endpoint")):
                series.append({
                    "name": row.get("Series Name","").strip(),
                    "code_endpoint": row["Code/Endpoint"].strip(),
                })
    return series

def main():
    candidate_paths = [
        Path("4_Global/series.csv"),
        Path("1_MacroEconomy/series.csv"),
    ]
    total = 0
    for p in candidate_paths:
        if not p.exists():
            continue
        for s in load_series_from_csv(p):
            indicator, country = parse_code_endpoint(s["code_endpoint"])
            print(f"[WB ] {indicator}:{country}")
            try:
                data = fetch_worldbank(indicator, country)
                out_path = save_series(indicator, country, data)
                print(f"  -> {out_path}")
                total += 1
                time.sleep(0.7)
            except Exception as e:
                print(f"  !! Failed {indicator}:{country} - {e}")
    print(f"Done. World Bank files updated: {total}")

if __name__ == "__main__":
    main()
