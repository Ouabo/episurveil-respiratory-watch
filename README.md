# EpiSurveil Respiratory Watch

A plain-language dashboard of flu, RSV, coronavirus and other respiratory illness: **Europe** (by country), **Germany** (by federal state)
and **German cities** (virus in wastewater, about 70 treatment plants with current data). No formulas on screen.
Every place gets two labels: a **level** (low, moderate, high, very high, compared with its own recent winters)
and a **trend** (rising, stable, falling). English and German.

Part of the EpiSurveil project. The model-based platform (particle filter, optimal control) is a separate app:
https://episurveil.streamlit.app

## Data (all open, free, attribution required)

| Page | Source | Level | Update |
|---|---|---|---|
| Europe | ECDC ERVISS, ILI/ARI consultation rates (primary care) | country | weekly |
| Germany | RKI ARE-Konsultationsinzidenz (doctor visits) | federal state | weekly |
| Germany | RKI lab-confirmed influenza (IfSG notifications) | federal state | weekly |
| Overview | RKI GrippeWeb (online survey, ILI) | national | weekly |
| My city | RKI AMELAG wastewater, individual treatment plants (flu A+B, RSV, SARS-CoV-2) | treatment plant | ~2 samples/week |

Maps: geoBoundaries DEU ADM1 (BKG); treatment-plant positions geocoded once with OpenStreetMap Nominatim
(`scripts/geocode_sites.py`, stored in `data/geo/ww_sites.csv`).

Not included yet: district (Landkreis) level. Lab-confirmed influenza by district exists only in RKI SurvStat,
which has no simple open file; a later version can query it.

## How the labels are decided

See `fluwatch/status.py` (and the About page in plain words).
- Level: this week vs. the same place in the last four seasons, weeks 40-20; bands at the median,
  75th and 90th percentile of those weeks.
- Trend: mean of the last two weeks vs. the two before; +-15 % (wastewater: +-30 %, on RKI's smoothed curve).
- Grey: no data for more than three weeks, or not enough past seasons.

## Run

```bash
pip install -r requirements.txt
python -m fluwatch.build --download   # fetch fresh data and rebuild data/processed
streamlit run app/Home.py
pytest -q
```

Disclaimer: information tool, not medical advice.
