# FullFinance Data Repository

This repo lists the **official data series** Full Finance uses for videos.
We store **series metadata and links**, not the raw data. During a video build,
Full Finance fetches live data from official sources (FRED, World Bank, etc.).

## How to use
- Update the CSV files in each folder to add/remove series.
- Each row = one series, with the **official code** and a **source link** (when useful).
- Keep names and codes exact so Full Finance can fetch the right series.

## Folders
- `1_MacroEconomy/series.csv` – GDP, CPI, unemployment (mostly U.S.)
- `2_Markets/series.csv` – Equities, oil, gold, dollar index
- `3_MonetaryPolicy/series.csv` – Fed funds, M2, central bank rates
- `4_Global/series.csv` – GDP & unemployment for EU, Japan, China (constant USD where possible)
- `5_PolicyDocs/links.csv` – Treasury, FED Beige Book, SEC EDGAR links
- `6_Events/events.csv` – Big historical events with dates and sources

## Tip
To get a **raw link** for a file: open the file → click the **Raw** button → copy that URL.
Share your repo link with Full Finance and say: “Use my GitHub repository.”
