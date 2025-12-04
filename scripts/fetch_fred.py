import os
import csv
import time
import requests
from pathlib import Path

DATA_DIR = Path("data/fred")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Simple downloader using FRED's CSV export (no API key needed)
def download_fred_series(code: str, out_path: Path):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={code}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    out_path.write_bytes(r.content)

def load_series_from_csv(csv_path: Path):
    series = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("Fetch Method","").strip().upper() == "FRED_CSV" 
                and row.get("Code/Endpoint")):
                series.append({
                    "name": row.get("Series Name","").strip(),
                    "code": row["Code/Endpoint"].strip(),
                })
    return series

def main():
    # Look for any "series.csv" files that might contain FRED rows
    candidate_paths = [
        Path("1_MacroEconomy/series.csv"),
        Path("2_Markets/series.csv"),
        Path("3_MonetaryPolicy/series.csv"),
        Path("4_Global/series.csv"),
    ]
    total = 0
    for p in candidate_paths:
        if not p.exists():
            continue
        for s in load_series_from_csv(p):
            code = s["code"]
            out_file = DATA_DIR / f"{code}.csv"
            print(f"[FRED] {code} -> {out_file}")
            try:
                download_fred_series(code, out_file)
                total += 1
                time.sleep(0.7)  # be polite
            except Exception as e:
                print(f"  !! Failed {code}: {e}")
    print(f"Done. FRED files updated: {total}")

if __name__ == "__main__":
    main()
