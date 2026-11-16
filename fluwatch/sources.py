"""Open data sources (all free, attribution required). Downloads go to data/raw/."""
from pathlib import Path
import time

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
GEO = ROOT / "data" / "geo"

_RKI = "https://raw.githubusercontent.com/robert-koch-institut"
_ECDC = "https://raw.githubusercontent.com/EU-ECDC/Respiratory_viruses_weekly_data/main/data"

SOURCES = {
    "ecdc_iliari.csv": {
        "url": f"{_ECDC}/ILIARIRates.csv",
        "name": "ECDC ERVISS - ILI/ARI consultation rates (primary care)",
        "home": "https://github.com/EU-ECDC/Respiratory_viruses_weekly_data",
        "licence": "ECDC copyright, reuse authorised with attribution",
    },
    "are.tsv": {
        "url": f"{_RKI}/ARE-Konsultationsinzidenz/main/ARE-Konsultationsinzidenz.tsv",
        "name": "RKI - ARE-Konsultationsinzidenz (doctor visits for acute respiratory illness)",
        "home": "https://github.com/robert-koch-institut/ARE-Konsultationsinzidenz",
        "licence": "CC BY 4.0",
    },
    "flu.tsv": {
        "url": f"{_RKI}/Influenzafaelle_in_Deutschland/main/IfSG_Influenzafaelle.tsv",
        "name": "RKI - Laborbestätigte Influenzafälle (lab-confirmed flu, IfSG)",
        "home": "https://github.com/robert-koch-institut/Influenzafaelle_in_Deutschland",
        "licence": "CC BY 4.0",
    },
    "grippeweb.tsv": {
        "url": f"{_RKI}/GrippeWeb_Daten_des_Wochenberichts/main/GrippeWeb_Daten_des_Wochenberichts.tsv",
        "name": "RKI - GrippeWeb (people reporting flu-like illness)",
        "home": "https://github.com/robert-koch-institut/GrippeWeb_Daten_des_Wochenberichts",
        "licence": "CC BY 4.0",
    },
    "amelag_sites.tsv": {
        "url": f"{_RKI}/Abwassersurveillance_AMELAG/main/amelag_einzelstandorte.tsv",
        "name": "RKI - AMELAG wastewater monitoring, individual treatment plants",
        "home": "https://github.com/robert-koch-institut/Abwassersurveillance_AMELAG",
        "licence": "CC BY 4.0",
    },
}

GEO_SOURCES = {
    "de_states.geojson": "geoBoundaries DEU ADM1 (BKG, Datenlizenz Deutschland - Namensnennung 2.0)",
    "ww_sites.csv": "Site coordinates from OpenStreetMap Nominatim (© OpenStreetMap contributors, ODbL)",
}


def download(name: str, max_age_hours: float = 12.0) -> Path:
    """Download one source unless a fresh copy is already in data/raw."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / name
    if path.exists() and (time.time() - path.stat().st_mtime) < max_age_hours * 3600:
        return path
    tmp = path.with_suffix(path.suffix + ".part")
    with requests.get(SOURCES[name]["url"], stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    tmp.replace(path)
    return path


def download_all(max_age_hours: float = 12.0):
    return {n: download(n, max_age_hours) for n in SOURCES}
