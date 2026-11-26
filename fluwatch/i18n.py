"""All user-facing text, English and German. Plain language only: no formulas, no model terms."""

T = {
    # app
    "app_title": {"en": "EpiSurveil Respiratory Watch", "de": "EpiSurveil Atemwegs-Monitor"},
    "tagline": {"en": "Flu, RSV, coronavirus and other respiratory illnesses: how much is going around in Europe, in Germany and in your city.",
                "de": "Grippe, RSV, Corona und andere Atemwegserkrankungen: wie viel gerade unterwegs ist, in Europa, in Deutschland und in Ihrer Stadt."},
    "language": {"en": "Language", "de": "Sprache"},
    "nav_home": {"en": "Overview", "de": "Überblick"},
    "nav_europe": {"en": "Europe", "de": "Europa"},
    "nav_germany": {"en": "Germany", "de": "Deutschland"},
    "nav_city": {"en": "My city (wastewater)", "de": "Meine Stadt (Abwasser)"},
    "nav_about": {"en": "About the data", "de": "Über die Daten"},
    "share_title": {"en": "Share this dashboard", "de": "Dieses Dashboard teilen"},
    "share_body": {"en": "Scan the code with your phone camera, or copy the link:",
                   "de": "Scannen Sie den Code mit der Handykamera oder kopieren Sie den Link:"},

    # levels and trends
    "low": {"en": "Low", "de": "Niedrig"},
    "moderate": {"en": "Moderate", "de": "Mäßig"},
    "high": {"en": "High", "de": "Hoch"},
    "very_high": {"en": "Very high", "de": "Sehr hoch"},
    "rising": {"en": "Rising", "de": "Steigend"},
    "stable": {"en": "Stable", "de": "Gleichbleibend"},
    "falling": {"en": "Falling", "de": "Fallend"},
    "no_recent": {"en": "No recent data", "de": "Keine aktuellen Daten"},
    "no_history": {"en": "Not enough past data to compare", "de": "Zu wenig Vergleichsdaten"},
    "unknown_trend": {"en": "Trend unclear", "de": "Trend unklar"},

    "level_help": {
        "en": "**Low**: below a typical winter week · **Moderate**: a typical winter week · "
              "**High**: a busy winter week · **Very high**: among the busiest weeks of recent winters.",
        "de": "**Niedrig**: unter einer typischen Winterwoche · **Mäßig**: eine typische Winterwoche · "
              "**Hoch**: eine starke Winterwoche · **Sehr hoch**: unter den stärksten Wochen der letzten Winter."},
    "trend_help": {
        "en": "**Rising / Falling**: the last two weeks compared with the two weeks before.",
        "de": "**Steigend / Fallend**: die letzten zwei Wochen im Vergleich zu den zwei Wochen davor."},

    # measures
    "m_ILI": {"en": "Doctor visits for flu-like illness", "de": "Arztbesuche wegen grippeähnlicher Erkrankung"},
    "m_ARI": {"en": "Doctor visits for respiratory infections", "de": "Arztbesuche wegen Atemwegsinfektionen"},
    "m_are": {"en": "Doctor visits for respiratory illness", "de": "Arztbesuche wegen Atemwegserkrankungen"},
    "m_flu": {"en": "Lab-confirmed flu cases", "de": "Laborbestätigte Grippefälle"},
    "m_gw_ILI": {"en": "People reporting flu-like illness (online survey)",
                 "de": "Menschen mit grippeähnlichen Beschwerden (Online-Befragung)"},
    "m_ww_flu": {"en": "Flu virus in wastewater", "de": "Grippeviren im Abwasser"},
    "m_ww_rsv": {"en": "RSV in wastewater", "de": "RSV im Abwasser"},
    "m_ww_covid": {"en": "Coronavirus in wastewater", "de": "Coronaviren im Abwasser"},
    "u_per100k": {"en": "per 100,000 people per week", "de": "pro 100.000 Menschen pro Woche"},
    "u_ww": {"en": "virus copies per litre", "de": "Viruskopien pro Liter"},

    # sentences
    "sentence": {"en": "In **{place}**, {measure_lc} are **{level}** and **{trend}**.",
                 "de": "In **{place}** sind {measure_lc} **{level}** und **{trend}**."},
    "sentence_ww": {"en": "In **{place}**, the amount of {virus} in wastewater is **{level}** and **{trend}**.",
                    "de": "In **{place}** ist die Menge an {virus} im Abwasser **{level}** und **{trend}**."},
    "sentence_ww_nd": {"en": "In **{place}**, {virus} is **barely detectable** in wastewater right now.",
                       "de": "In **{place}** sind {virus} im Abwasser derzeit **kaum nachweisbar**."},
    "barely": {"en": "Barely detectable", "de": "Kaum nachweisbar"},
    "as_of": {"en": "Latest data: week of {date}", "de": "Neueste Daten: Woche vom {date}"},
    "as_of_day": {"en": "Latest sample: {date}", "de": "Letzte Probe: {date}"},

    # overview
    "ov_germany": {"en": "Germany", "de": "Deutschland"},
    "ov_europe": {"en": "Europe", "de": "Europa"},
    "ov_cities": {"en": "German cities (wastewater)", "de": "Deutsche Städte (Abwasser)"},
    "ov_eu_line": {"en": "{n_high} of {n} countries at high or very high level · {n_rising} rising",
                   "de": "{n_high} von {n} Ländern auf hohem oder sehr hohem Niveau · {n_rising} steigend"},
    "ov_ww_line": {"en": "{n_rising} of {n} treatment plants show rising flu virus · {n_high} at high or very high level",
                   "de": "{n_rising} von {n} Kläranlagen zeigen steigende Grippeviren · {n_high} auf hohem oder sehr hohem Niveau"},
    "how_to_read": {"en": "How to read this page", "de": "So lesen Sie diese Seite"},
    "how_to_read_body": {
        "en": "Each place gets two simple labels.\n\n"
              "- **Level** says how today compares with recent winters in the same place.\n"
              "- **Trend** says whether it is going up or down.\n\n"
              "Colours go from light (low) to dark (very high). Grey means no recent data.",
        "de": "Jeder Ort bekommt zwei einfache Angaben.\n\n"
              "- **Niveau** zeigt, wie die aktuelle Lage im Vergleich zu den letzten Wintern am selben Ort ist.\n"
              "- **Trend** zeigt, ob es nach oben oder unten geht.\n\n"
              "Die Farben gehen von hell (niedrig) bis dunkel (sehr hoch). Grau bedeutet: keine aktuellen Daten."},
    "level": {"en": "Level", "de": "Niveau"},
    "trend": {"en": "Trend", "de": "Trend"},

    # charts
    "this_season": {"en": "This winter", "de": "Dieser Winter"},
    "last_season": {"en": "Last winter", "de": "Letzter Winter"},
    "season_before": {"en": "Winter before", "de": "Vorletzter Winter"},
    "chart_title": {"en": "This winter compared with the last two", "de": "Dieser Winter im Vergleich zu den letzten beiden"},
    "bands_note": {"en": "Background colours show the level bands for this place.",
                   "de": "Die Hintergrundfarben zeigen die Niveau-Stufen für diesen Ort."},
    "months": {"en": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
               "de": ["Okt", "Nov", "Dez", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep"]},
    "show_table": {"en": "Show as table", "de": "Als Tabelle anzeigen"},

    # europe
    "eu_title": {"en": "Europe: flu and respiratory illness by country", "de": "Europa: Grippe und Atemwegserkrankungen nach Land"},
    "eu_intro": {"en": "Based on doctor visits reported to the European Centre for Disease Prevention and Control (ECDC). "
                       "Some countries report flu-like illness, others all respiratory infections; each country is compared only with itself.",
                 "de": "Grundlage sind Arztbesuche, die an das Europäische Zentrum für die Prävention und die Kontrolle von Krankheiten (ECDC) gemeldet werden. "
                       "Manche Länder melden grippeähnliche Erkrankungen, andere alle Atemwegsinfektionen; jedes Land wird nur mit sich selbst verglichen."},
    "pick_country": {"en": "Choose a country", "de": "Land wählen"},

    # germany
    "de_title": {"en": "Germany: by federal state", "de": "Deutschland: nach Bundesland"},
    "de_intro": {"en": "Data from the Robert Koch Institute (RKI).", "de": "Daten des Robert Koch-Instituts (RKI)."},
    "pick_measure": {"en": "What to show", "de": "Was soll gezeigt werden"},
    "pick_state": {"en": "Choose a federal state", "de": "Bundesland wählen"},
    "germany_whole": {"en": "Germany (whole country)", "de": "Deutschland (gesamt)"},
    "measure_note_are": {"en": "All respiratory illnesses seen by family doctors (colds, flu, COVID and others).",
                         "de": "Alle Atemwegserkrankungen in Hausarztpraxen (Erkältung, Grippe, COVID und andere)."},
    "measure_note_flu": {"en": "Only flu confirmed by a laboratory test. Many flu cases are never tested, so this shows the direction more than the size.",
                         "de": "Nur im Labor bestätigte Grippe. Viele Fälle werden nie getestet; die Zahl zeigt eher die Richtung als das Ausmaß."},

    # city
    "city_title": {"en": "My city: virus in wastewater", "de": "Meine Stadt: Viren im Abwasser"},
    "city_intro": {"en": "Treatment plants test wastewater for viruses about twice a week. It shows infections in the "
                         "whole local population, including people who never see a doctor.",
                   "de": "Kläranlagen untersuchen das Abwasser etwa zweimal pro Woche auf Viren. So sieht man Infektionen in der "
                         "ganzen Bevölkerung vor Ort, auch bei Menschen, die nicht zum Arzt gehen."},
    "pick_virus": {"en": "Virus", "de": "Virus"},
    "v_flu": {"en": "Flu", "de": "Grippe"},
    "v_rsv": {"en": "RSV", "de": "RSV"},
    "v_covid": {"en": "Coronavirus", "de": "Coronavirus"},
    "v_flu_lc": {"en": "flu virus", "de": "Grippeviren"},
    "v_rsv_lc": {"en": "RSV", "de": "RSV"},
    "v_covid_lc": {"en": "coronavirus", "de": "Coronaviren"},
    "search_city": {"en": "Search your city or treatment plant", "de": "Stadt oder Kläranlage suchen"},
    "color_by": {"en": "Colour the map by", "de": "Karte einfärben nach"},
    "only_recent": {"en": "Only plants with data in the last 3 weeks are coloured.",
                    "de": "Nur Kläranlagen mit Daten aus den letzten 3 Wochen sind eingefärbt."},
    "last_12m": {"en": "The last 12 months", "de": "Die letzten 12 Monate"},
    "measured": {"en": "Measured sample", "de": "Gemessene Probe"},
    "smoothed": {"en": "Smoothed curve (RKI)", "de": "Geglättete Kurve (RKI)"},
    "people_served": {"en": "people connected", "de": "angeschlossene Menschen"},
    "no_coords": {"en": "Some plants could not be placed on the map; they are still in the search list.",
                  "de": "Einige Kläranlagen konnten nicht auf der Karte platziert werden; sie sind trotzdem in der Suche."},

    # overview (key messages)
    "glance": {"en": "This week at a glance", "de": "Diese Woche auf einen Blick"},
    "head_de": {"en": "Respiratory illness in Germany is **{level}** and **{trend}**.",
                "de": "Atemwegserkrankungen in Deutschland: **{level}** und **{trend}**."},
    "head_flu": {"en": "Lab-confirmed flu is **rising in {n} of {m} federal states**.",
                 "de": "Laborbestätigte Grippe **steigt in {n} von {m} Bundesländern**."},
    "head_flu_none": {"en": "Lab-confirmed flu is not rising in any federal state.",
                      "de": "Laborbestätigte Grippe steigt in keinem Bundesland."},
    "head_hot": {"en": "Places to watch: **{places}**.", "de": "Im Blick behalten: **{places}**."},
    "head_ww": {"en": "{virus} in wastewater is **rising at {n} of {m} treatment plants**",
                "de": "{virus} im Abwasser **steigt an {n} von {m} Kläranlagen**"},
    "head_ww_high": {"en": "; high in **{places}**", "de": "; hoch in **{places}**"},
    "head_flu_ww": {"en": " Flu virus in wastewater is high in **{places}**.",
                    "de": " Grippeviren im Abwasser sind hoch in **{places}**."},
    "head_eu": {"en": "Europe: **{n} of {m} countries** above a typical winter week ({names}).",
                "de": "Europa: **{n} von {m} Ländern** über einer typischen Winterwoche ({names})."},
    "head_eu_none": {"en": "Europe: no country is above a typical winter week.",
                     "de": "Europa: kein Land liegt über einer typischen Winterwoche."},
    "V_flu": {"en": "Flu virus", "de": "Grippevirus"},
    "V_rsv": {"en": "RSV", "de": "RSV"},
    "V_covid": {"en": "Coronavirus", "de": "Coronavirus"},
    "head_calm": {"en": "No place is above a typical winter week right now.",
                  "de": "Derzeit liegt kein Ort über einer typischen Winterwoche."},
    "kp_doctor": {"en": "Doctor visits, Germany", "de": "Arztbesuche, Deutschland"},
    "kp_flu": {"en": "Lab-confirmed flu, Germany", "de": "Laborbestätigte Grippe, Deutschland"},
    "kp_flu_line": {"en": "federal states with rising flu", "de": "Bundesländer mit steigender Grippe"},
    "kp_eu": {"en": "Europe", "de": "Europa"},
    "kp_eu_line": {"en": "countries above a typical winter week", "de": "Länder über einer typischen Winterwoche"},
    "kp_eu_rising": {"en": "{n} rising", "de": "{n} steigend"},
    "kp_ww": {"en": "Wastewater, German cities", "de": "Abwasser, deutsche Städte"},
    "kp_ww_rising": {"en": "rising at {n} of {m} plants", "de": "steigend an {n} von {m} Anlagen"},
    "kp_ww_nd": {"en": "barely detectable at {n} of {m}", "de": "kaum nachweisbar an {n} von {m}"},
    "watch_title": {"en": "Places to watch", "de": "Orte im Blick"},
    "watch_intro": {"en": "Places at a high level, or above a typical winter week and rising.",
                    "de": "Orte auf hohem Niveau oder über einer typischen Winterwoche und steigend."},
    "col_place": {"en": "Place", "de": "Ort"},
    "col_what": {"en": "What is measured", "de": "Was gemessen wird"},
    "t_country": {"en": "Country", "de": "Land"},
    "t_state": {"en": "Federal state", "de": "Bundesland"},
    "t_city": {"en": "City (wastewater)", "de": "Stadt (Abwasser)"},
    "more": {"en": "Details", "de": "Details"},

    # table headers
    "col_country": {"en": "Country", "de": "Land"},
    "col_state": {"en": "Federal state", "de": "Bundesland"},
    "col_site": {"en": "Treatment plant", "de": "Kläranlage"},
    "col_measure": {"en": "Measure", "de": "Messgröße"},
    "col_week": {"en": "Week of", "de": "Woche vom"},
    "col_last": {"en": "Last sample", "de": "Letzte Probe"},
    "col_people": {"en": "People connected", "de": "Angeschlossene Menschen"},

    # about
    "about_title": {"en": "About the data", "de": "Über die Daten"},
    "disclaimer": {"en": "This is an information tool, not medical advice. If you feel ill, follow the advice of your doctor and your local health authority.",
                   "de": "Dies ist ein Informationsangebot und keine medizinische Beratung. Wenn Sie sich krank fühlen, folgen Sie dem Rat Ihrer Ärztin oder Ihres Arztes und Ihres Gesundheitsamts."},
    "how_decided": {"en": "How the labels are decided", "de": "Wie die Angaben entstehen"},
    "how_decided_body": {
        "en": "- **Level**: this week is compared with the same place during the last four winters (October to May). "
              "Below a typical winter week is *low*; a typical winter week is *moderate*; "
              "busier than three out of four winter weeks is *high*; busier than nine out of ten is *very high*.\n"
              "- **Trend**: the last two weeks are compared with the two weeks before. A change of at least 15 % "
              "(30 % for wastewater, which jumps around more) counts as rising or falling.\n"
              "- **Grey**: the place has not sent data for more than three weeks, or there are not yet enough past winters to compare.\n"
              "- The newest week is often updated later, when late reports arrive.",
        "de": "- **Niveau**: Diese Woche wird mit demselben Ort in den letzten vier Wintern (Oktober bis Mai) verglichen. "
              "Unter einer typischen Winterwoche heißt *niedrig*; eine typische Winterwoche heißt *mäßig*; "
              "stärker als drei von vier Winterwochen heißt *hoch*; stärker als neun von zehn heißt *sehr hoch*.\n"
              "- **Trend**: Die letzten zwei Wochen werden mit den zwei Wochen davor verglichen. Eine Änderung von mindestens 15 % "
              "(30 % beim Abwasser, das stärker schwankt) gilt als steigend oder fallend.\n"
              "- **Grau**: Der Ort hat seit mehr als drei Wochen keine Daten geliefert, oder es gibt noch zu wenige Vergleichswinter.\n"
              "- Die neueste Woche wird oft später noch ergänzt, wenn Nachmeldungen eintreffen."},
    "sources": {"en": "Sources", "de": "Quellen"},
    "updated": {"en": "Data last refreshed", "de": "Daten zuletzt aktualisiert"},
    "author": {"en": "Built by Florent Ouabo Kamkumo, BTU Cottbus-Senftenberg. Part of the EpiSurveil project.",
               "de": "Erstellt von Florent Ouabo Kamkumo, BTU Cottbus-Senftenberg. Teil des Projekts EpiSurveil."},
}


def t(key: str, lang: str) -> str:
    v = T[key]
    return v.get(lang, v["en"])
