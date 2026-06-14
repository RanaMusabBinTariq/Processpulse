from __future__ import annotations
from datetime import datetime
from typing import Dict, Any, List
import numpy as np
import pandas as pd

LINKEDIN_URL = "https://www.linkedin.com/in/rana-musab-bin-tariq-a70982152/"
GITHUB_URL   = "https://github.com/RanaMusabBinTariq"
EMAIL        = "musabr81@gmail.com"
AUTHOR       = "Rana Musab Bin Tariq"

RANGES = {
    "Temperature": {"lsl":20.0,"usl":28.0,"center":24.0,"unit":"°C","step":"mixing"},
    "Pressure":    {"lsl":0.90,"usl":1.60,"center":1.25,"unit":"bar","step":"equipment"},
    "pH":          {"lsl":6.80,"usl":7.40,"center":7.10,"unit":"","step":"ipc"},
    "Flow":        {"lsl":38.0,"usl":52.0,"center":45.0,"unit":"L/min","step":"filling"},
    "Yield":       {"lsl":92.0,"usl":100.0,"center":96.0,"unit":"%","step":"qc"},
    "Quality":     {"lsl":95.0,"usl":100.0,"center":98.0,"unit":"%","step":"qc"},
}

REQUIRED  = ["time","Temperature","Pressure","pH","Flow"]
OPTIONAL  = ["Yield","Quality"]
SCENARIOS = ["normal","ph_drift","flow_restriction","temperature_excursion","missing_ipc"]

ALIASES = {
    "time":"time","timestamp":"time","datetime":"time","date":"time","sample_time":"time",
    "temperature":"Temperature","temp":"Temperature","temp_c":"Temperature","temperature_c":"Temperature",
    "pressure":"Pressure","pressure_bar":"Pressure","bar":"Pressure",
    "ph":"pH","p_h":"pH","pH":"pH",
    "flow":"Flow","flow_rate":"Flow","flow_l_min":"Flow","flow_lpm":"Flow",
    "yield":"Yield","yield_pct":"Yield","yield_percent":"Yield",
    "quality":"Quality","quality_pct":"Quality","purity":"Quality","purity_pct":"Quality",
    "downtime":"Downtime","downtime_min":"Downtime",
    "good_count":"GoodCount","good_units":"GoodCount",
    "total_count":"TotalCount","total_units":"TotalCount",
    "ideal_rate":"IdealRate","target_rate":"IdealRate",
}

# ── Single unified translation dict (merges both TEXT and I18N) ──────────────
I18N: Dict[str,Dict[str,str]] = {
"en": {
    # meta
    "lang_name":"English","title":"ProcessPulse",
    "subtitle":"Digital Manufacturing Review Assistant",
    "scope":"Synthetic portfolio prototype. Not a validated GMP, MES, ERP, LIMS, QMS, SCADA, eBR, electronic-signature, quality-decision, or batch-release system. Not for real manufacturing, regulatory, patient-impacting, or safety-critical use.",
    "data_privacy":"CSV data is processed locally in this Streamlit session. No external API or cloud AI is used.",
    "not_decision":"Not for decision making",
    # nav
    "dashboard":"Dashboard","data":"Data Intake","signal":"Signal & XAI",
    "workflow":"Workflow / eBR","twin":"Process Twin","oee":"Sensors & OEE",
    "requirements":"Requirements Brief","about":"About",
    # sidebar
    "reviewer":"Reviewer","scenario":"Sample scenario",
    "upload_csv":"Upload CSV","download_template":"Download CSV template",
    "use_sample":"Using sample data","use_csv":"Using uploaded CSV",
    # page help
    "page_help":"What this page does",
    "dashboard_help":"Shows the active process issue, evidence summary, affected manufacturing step, and the next recommended action. Start here to orient yourself.",
    "data_help":"Checks whether the uploaded or sample CSV has enough trusted columns. Missing columns are excluded — never faked.",
    "signal_help":"Applies transparent rules (limit excursion, trend/drift, Cpk capability) to trusted data and explains the result in plain language.",
    "workflow_help":"Shows the affected manufacturing step first, lets you record reviewer actions, and builds a session audit trail.",
    "twin_help":"Change process parameters and see how risk, yield, and quality respond. The focus parameter is pre-set to the active signal.",
    "oee_help":"Displays trusted sensor streams and explains every component of the prototype OEE estimate.",
    "requirements_help":"Translates the active signal into a structured digitalization requirements brief and downloadable evidence pack.",
    "about_help":"Candidate profile, project value, skills demonstrated, AI disclosure, and legal scope.",
    # expert context per page
    "expert_dashboard":"Demonstrates end-to-end process data flow — from raw CSV ingestion through rule-based signal detection to workflow routing — mirroring MES/eBR integration patterns used in Digital Manufacturing teams.",
    "expert_data":"Implements a data-quality gate consistent with data-integrity principles (ALCOA+). Column aliasing handles real-world historian export variability without silent imputation.",
    "expert_signal":"Rule engine covers limit excursions, trend/drift (early vs late window mean), and Cpk capability estimates — all explainable without a black-box model, appropriate for GMP environments.",
    "expert_workflow":"eBR-style step routing with manual override, status propagation, and timestamped audit trail. Demonstrates understanding of MES workflow logic and GMP documentation requirements.",
    "expert_twin":"Parametric process model with sensitivity-weighted penalties per parameter. Shows Digital Twin concept: bidirectional link between process settings and predicted outcomes.",
    "expert_oee":"OEE decomposition (Availability × Performance × Quality) estimated from available data streams, with transparent fallback logic when columns are absent.",
    "expert_requirements":"Requirements brief follows URS-style structure (current state, future state, user/data/interface/role/audit/validation requirements) — the deliverable format used in MES/LIMS implementation projects.",
    "expert_about":"Demonstrates the full stack of a Digital Manufacturing analyst: pharmaceutical domain knowledge (GMP, IPC, batch documentation), Python data engineering (pandas, NumPy, Plotly), process analytics (SPC/Cpk, OEE), workflow digitalization (MES/eBR logic, audit trail), and requirements analysis (URS-style brief) — all in one locally-running prototype.",
    # page descriptions
    # issue ribbon
    "selected_issue":"Selected issue","parameter":"Parameter","severity":"Severity",
    "affected_step":"Affected step","next_action":"Next action",
    "data_source":"Data source","review_status":"Review status",
    # status labels
    "no_active":"No active signal","monitor":"Monitor",
    "review_needed":"Review needed","blocked":"Blocked","active_signal":"Active signal",
    "readiness":"Readiness","readiness_score":"Readiness score",
    # scenarios
    "try_demo":"Try demo scenario","try_normal":"Normal batch","try_ph":"pH drift",
    "try_flow":"Flow restriction","try_temp":"Temperature excursion","try_missing":"Missing IPC / pH",
    "what_changes":"What changes","demo_explain":"The whole app follows one selected issue: ticket → chart → workflow step → twin focus → OEE → requirements brief.",
    # flow labels
    "process_flow":"Review flow","manufacturing_flow":"Manufacturing workflow",
    "data_to_req":"Data → Signal → Workflow → Evidence → Requirements",
    "command_modules":"Command modules","open":"Open",
    # data page
    "required_columns":"Required columns","trusted_columns":"Trusted columns",
    "excluded_columns":"Excluded columns",
    "accepted_aliases":"Accepted aliases: timestamp, temp, pressure_bar, ph, flow_rate, yield_pct, quality_pct.",
    "missing_not_faked":"Missing columns are not filled or plotted as fake data.",
    "quality_gate":"Data-quality gate",
    # signal page
    "signal_ticket":"Review ticket","rule":"Rule","evidence":"Evidence",
    "why":"Why it matters","action":"Action","chart":"Evidence chart",
    "plain_terms":"Plain-language glossary","focus_parameter":"Focus parameter",
    "spc_plain":"SPC: checks whether the process pattern shows unusual variation — run rules, trends, or clustered points outside control limits.",
    "cpk_plain":"Cpk (process capability): measures how well the data fits inside the review range. Cpk < 1.0 means the process is not comfortably inside limits.",
    "xai_plain":"XAI (explainable analytics): every signal is generated from a transparent rule with numeric evidence — no black-box model, safe for GMP audit.",
    "oee_plain":"OEE (Overall Equipment Effectiveness): Availability × Performance × Quality. Prototype estimates from available data streams; real OEE needs historian integration.",
    "gcpk_plain":"GMP relevance: all rules reference ICH Q10 process monitoring concepts — limit excursions, capability, and trend detection align with process analytical technology (PAT) principles.",
    # workflow
    "affected_first":"Affected step first","all_steps":"All workflow steps",
    "review_note":"Reviewer note","mark_complete":"Mark complete",
    "flag_review":"Flag review","block_step":"Block step",
    "note_required":"Add a note before flagging or blocking.",
    "audit":"Session audit trail","saved":"Saved","required_fields":"Required fields",
    # workflow statuses
    "waiting":"Waiting","review":"Review needed","complete":"Complete",
    "status_complete":"Required data is available for this prototype review.",
    "status_waiting":"Required data is not available yet.",
    "status_review":"Human review is needed before proceeding.",
    "status_blocked":"Step should not proceed until the issue is resolved.",
    # workflow step names
    "material":"Material ready","weighing":"Weighing verified","equipment":"Equipment check",
    "charging":"Charging","mixing":"Mixing","ipc":"IPC sample","filling":"Filling / transfer",
    "qc":"QC review","qa":"QA disposition",
    "req_material":"Material lot, quantity, expiry/date check",
    "req_weighing":"Scale check, weight entry, second check",
    "req_equipment":"Line clearance, cleaning state, equipment ID",
    "req_charging":"Start time, operator note, material confirmation",
    "req_mixing":"Mixing speed, temperature, duration",
    "req_ipc":"Result value, sample time, reviewer",
    "req_filling":"Flow trend, yield estimate, transfer status",
    "req_qc":"Test reference, review outcome, comment",
    "req_qa":"Evidence reviewed, disposition note, authorised reviewer",
    # twin
    "process_twin_title":"Interactive process twin",
    "temperature":"Temperature","pressure":"Pressure","flow":"Flow",
    "mixing_speed":"Mixing speed (RPM)","material_variability":"Material variability (%)",
    "predicted_yield":"Predicted yield","quality_score":"Quality score",
    "risk_score":"Risk score","risk_driver":"Risk driver",
    "add_sim":"Add simulation row to working data","sim_added":"Simulation row added.",
    "safe_zone":"Safe zone","current_value":"Current value",
    # oee
    "sensor_streams":"Sensor streams","prototype_oee":"Prototype OEE estimate",
    "oee_cause":"OEE explanation","availability":"Availability",
    "performance":"Performance","quality":"Quality","oee":"OEE",
    # requirements
    "download_pack":"Download evidence pack","brief":"Digitalization requirements brief",
    "current_problem":"Current-state problem","future_state":"Future-state process",
    "user_req":"User requirement","data_req":"Data requirement",
    "interface_req":"Interface assumption","role_req":"Role / access requirement",
    "audit_req":"Audit-trail requirement","validation":"Validation consideration",
    "benefit":"Expected benefit","open_questions":"Open questions",
    # about
    "built_by":"Built by","linkedin":"LinkedIn","github":"GitHub","contact":"Contact",
    "profile":"Profile","project_value":"Project value","skills":"Skills demonstrated",
    "hire_story":"Recruiter story","ai_scope":"AI / XAI disclosure",
    "role":"Portfolio prototype for Digital Manufacturing & Data Analytics",
    "profile_text":"PharmD + MSc Digital Health (Deggendorf Institute of Technology). Five years in pharmaceutical GMP manufacturing, community pharmacy, and healthcare claims operations. Applied projects in Python, Streamlit, data analytics, and process simulation. Designed and built two portfolio apps demonstrating QA/MES workflow, ML-based claims triage, and process monitoring — prior to ever holding a Digital Manufacturing title.",
    "project_value_text":"ProcessPulse connects process data quality, explainable signal detection, eBR-style workflow routing, process twin simulation, OEE estimation, and digitalization requirements analysis in a single local prototype — the full stack of a Digital Manufacturing analyst role.",
    "skills_text":"Python · Streamlit · pandas · NumPy · Plotly · SPC/Cpk · rule-based XAI · MES/eBR workflow logic · process twin simulation · OEE estimation · GMP documentation · bilingual UI (EN/DE) · requirements analysis (URS-style) · data-quality gates (ALCOA+) · audit trail · CSV/historian data handling.",
    "hire_story_text":"I bring pharmaceutical domain knowledge most IT candidates lack, and the Python/Streamlit build skills most pharma candidates lack. ProcessPulse exists because I wanted to show — not just describe — that I can connect process understanding, data integrity, digital workflow, and requirements analysis in one coherent tool.",
    "ai_scope_text":"No external AI or API is used. All signals are generated from transparent, auditable rules: limit checks, trend windows, Cpk estimates, and data-quality gates. This is intentional — GMP environments require explainable, validated logic.",
    # data helpers
    "rows":"Rows","detected":"Detected","missing":"Missing","invalid":"Invalid / empty",
    "confidence":"Confidence","trusted":"Trusted","limited":"Limited","poor":"Poor",
    "unavailable":"Unavailable","excluded":"Excluded from trusted evidence",
    "mean":"Mean","last":"Last value","std":"Std dev","cpk":"Cpk",
    "missing_streams":"Missing streams excluded.",
},
"de": {
    "lang_name":"Deutsch","title":"ProcessPulse",
    "subtitle":"Digital Manufacturing Review Assistant",
    "scope":"Synthetischer Portfolio-Prototyp. Kein validiertes GMP-, MES-, ERP-, LIMS-, QMS-, SCADA-, eBR-, elektronisches Signatur-, Qualitätsentscheidungs- oder Chargenfreigabesystem. Nicht für reale Herstellung, regulatorische, patientenrelevante oder sicherheitskritische Nutzung.",
    "data_privacy":"CSV-Daten werden lokal in dieser Streamlit-Sitzung verarbeitet. Es wird keine externe API oder Cloud-KI genutzt.",
    "not_decision":"Nicht für Entscheidungen",
    "dashboard":"Dashboard","data":"Datenaufnahme","signal":"Signal & XAI",
    "workflow":"Workflow / eBR","twin":"Prozess-Zwilling","oee":"Sensoren & OEE",
    "requirements":"Anforderungsbrief","about":"Über",
    "reviewer":"Prüfer","scenario":"Beispielszenario",
    "upload_csv":"CSV hochladen","download_template":"CSV-Vorlage herunterladen",
    "use_sample":"Beispieldaten aktiv","use_csv":"Hochgeladene CSV aktiv",
    "page_help":"Was diese Seite macht",
    "dashboard_help":"Zeigt das aktive Prozessthema, Evidenzzusammenfassung, betroffenen Herstellungsschritt und die empfohlene nächste Aktion.",
    "data_help":"Prüft, ob die CSV genug vertrauenswürdige Spalten hat. Fehlende Spalten werden ausgeschlossen — niemals gefälscht.",
    "signal_help":"Wendet transparente Regeln an (Grenzwertabweichung, Trend/Drift, Cpk) und erklärt das Ergebnis in einfacher Sprache.",
    "workflow_help":"Zeigt zuerst den betroffenen Herstellungsschritt, ermöglicht Prüferaktionen und erstellt einen Sitzungs-Audit-Trail.",
    "twin_help":"Prozessparameter ändern und sehen, wie Risiko, Ausbeute und Qualität reagieren.",
    "oee_help":"Zeigt vertrauenswürdige Sensortrends und erklärt jede Komponente der Prototyp-OEE-Schätzung.",
    "requirements_help":"Wandelt das aktive Signal in einen strukturierten Digitalisierungs-Anforderungsbrief und ein Evidenzpaket um.",
    "about_help":"Kandidatenprofil, Projektwert, demonstrierte Fähigkeiten, KI-Offenlegung und rechtlicher Scope.",
    "expert_dashboard":"Demonstriert den End-to-End-Prozessdatenfluss — von der CSV-Aufnahme über regelbasierte Signalerkennung bis zum Workflow-Routing — angelehnt an MES/eBR-Integrationsmuster.",
    "expert_data":"Implementiert ein Datenqualitäts-Gate konsistent mit Datenintegritätsprinzipien (ALCOA+). Spalten-Aliasing verarbeitet reale Historian-Export-Varianz ohne stille Imputation.",
    "expert_signal":"Regelwerk deckt Grenzwertabweichungen, Trend/Drift und Cpk-Fähigkeitsschätzungen ab — vollständig erklärbar, geeignet für GMP-Umgebungen.",
    "expert_workflow":"eBR-ähnliches Schritt-Routing mit manuellem Override, Statuspropagierung und Zeitstempel-Audit-Trail.",
    "expert_twin":"Parametrisches Prozessmodell mit sensitiv gewichteten Strafen je Parameter — Digital Twin Konzept mit bidirektionaler Verknüpfung.",
    "expert_oee":"OEE-Zerlegung (Verfügbarkeit × Leistung × Qualität) mit transparenter Fallback-Logik bei fehlenden Spalten.",
    "expert_requirements":"Anforderungsbrief folgt URS-ähnlicher Struktur (Ist/Soll, Benutzer-/Daten-/Schnittstellen-/Rollen-/Audit-/Validierungsanforderungen).",
    "expert_about":"Demonstriert den vollständigen Stack eines Digital Manufacturing Analysten: pharmazeutisches Domänenwissen (GMP, IPC, Chargendokumentation), Python-Datentechnik, Prozessanalytik (SPC/Cpk, OEE), Workflow-Digitalisierung (MES/eBR, Audit-Trail) und Anforderungsanalyse (URS) — alles in einem lokal laufenden Prototyp.",

    "selected_issue":"Ausgewähltes Problem","parameter":"Parameter","severity":"Schweregrad",
    "affected_step":"Betroffener Schritt","next_action":"Nächste Aktion",
    "data_source":"Datenquelle","review_status":"Prüfstatus",
    "no_active":"Kein aktives Signal","monitor":"Überwachen",
    "review_needed":"Prüfung nötig","blocked":"Blockiert","active_signal":"Aktives Signal",
    "readiness":"Prüfbereitschaft","readiness_score":"Bereitschaftsscore",
    "try_demo":"Demo-Szenario testen","try_normal":"Normaler Batch","try_ph":"pH-Trend",
    "try_flow":"Flussrestriktion","try_temp":"Temperaturabweichung","try_missing":"Fehlender IPC / pH",
    "what_changes":"Was sich ändert","demo_explain":"Die App folgt einem ausgewählten Problem: Ticket → Diagramm → Schritt → Zwilling → OEE → Anforderungen.",
    "process_flow":"Prüfablauf","manufacturing_flow":"Herstellungsworkflow",
    "data_to_req":"Daten → Signal → Workflow → Evidenz → Anforderungen",
    "command_modules":"Arbeitsmodule","open":"Öffnen",
    "required_columns":"Pflichtspalten","trusted_columns":"Vertrauenswürdige Spalten",
    "excluded_columns":"Ausgeschlossene Spalten",
    "accepted_aliases":"Akzeptierte Aliasnamen: timestamp, temp, pressure_bar, ph, flow_rate, yield_pct, quality_pct.",
    "missing_not_faked":"Fehlende Spalten werden nicht gefüllt oder als falsche Daten geplottet.",
    "quality_gate":"Datenqualitäts-Gate",
    "signal_ticket":"Prüfticket","rule":"Regel","evidence":"Evidenz",
    "why":"Warum relevant","action":"Aktion","chart":"Evidenzdiagramm",
    "plain_terms":"Glossar (einfache Sprache)","focus_parameter":"Fokusparameter",
    "spc_plain":"SPC: prüft, ob das Prozessmuster ungewöhnliche Variation zeigt — Laufregeln, Trends oder Häufungen außerhalb der Kontrollgrenzen.",
    "cpk_plain":"Cpk (Prozessfähigkeit): misst, wie gut die Daten in den Prüfbereich passen. Cpk < 1,0 bedeutet, der Prozess liegt nicht stabil im Grenzbereich.",
    "xai_plain":"XAI (erklärbare Analytik): jedes Signal wird aus einer transparenten Regel mit numerischer Evidenz erzeugt — kein Black-Box-Modell, GMP-auditierbar.",
    "oee_plain":"OEE (Gesamtanlageneffektivität): Verfügbarkeit × Leistung × Qualität. Prototyp schätzt aus verfügbaren Datenströmen.",
    "gcpk_plain":"GMP-Relevanz: alle Regeln beziehen sich auf ICH Q10 Prozessmonitoringkonzepte — Grenzwertabweichungen, Fähigkeit und Trenderkennung.",
    "affected_first":"Betroffener Schritt zuerst","all_steps":"Alle Workflow-Schritte",
    "review_note":"Prüfnotiz","mark_complete":"Abschließen","flag_review":"Prüfung markieren",
    "block_step":"Blockieren","note_required":"Notiz hinzufügen, bevor markiert oder blockiert wird.",
    "audit":"Sitzungs-Audit-Trail","saved":"Gespeichert","required_fields":"Erforderliche Felder",
    "waiting":"Wartet","review":"Prüfung nötig","complete":"Abgeschlossen",
    "status_complete":"Erforderliche Daten für diese Prototyp-Prüfung verfügbar.",
    "status_waiting":"Erforderliche Daten noch nicht verfügbar.",
    "status_review":"Menschliche Prüfung erforderlich, bevor fortgefahren wird.",
    "status_blocked":"Schritt nicht fortführen, bis das Problem gelöst ist.",
    "material":"Material bereit","weighing":"Wägung verifiziert","equipment":"Anlagenprüfung",
    "charging":"Beschickung","mixing":"Mischen","ipc":"IPC-Probe","filling":"Abfüllung / Transfer",
    "qc":"QC-Prüfung","qa":"QA-Dispositionsprüfung",
    "req_material":"Materialcharge, Menge, Verfallsdatumsprüfung",
    "req_weighing":"Waagenprüfung, Gewichtseintrag, Zweitprüfung",
    "req_equipment":"Line Clearance, Reinigungsstatus, Anlagen-ID",
    "req_charging":"Startzeit, Bedienernotiz, Materialbestätigung",
    "req_mixing":"Mischgeschwindigkeit, Temperatur, Dauer",
    "req_ipc":"Ergebniswert, Probenzeit, Prüfer",
    "req_filling":"Flusstrend, Ausbeuteschätzung, Transferstatus",
    "req_qc":"Prüfreferenz, Prüfergebnis, Kommentar",
    "req_qa":"Evidenz geprüft, Dispositionsnotiz, autorisierter Prüfer",
    "process_twin_title":"Interaktiver Prozess-Zwilling",
    "temperature":"Temperatur","pressure":"Druck","flow":"Fluss",
    "mixing_speed":"Mischgeschwindigkeit (U/min)","material_variability":"Materialvariabilität (%)",
    "predicted_yield":"Prognostizierte Ausbeute","quality_score":"Qualitätsscore",
    "risk_score":"Risikoscore","risk_driver":"Risikotreiber",
    "add_sim":"Simulationszeile hinzufügen","sim_added":"Simulationszeile hinzugefügt.",
    "safe_zone":"Sicherer Bereich","current_value":"Aktueller Wert",
    "sensor_streams":"Sensortrends","prototype_oee":"Prototyp-OEE-Schätzung",
    "oee_cause":"OEE-Erklärung","availability":"Verfügbarkeit",
    "performance":"Leistung","quality":"Qualität","oee":"OEE",
    "download_pack":"Evidenzpaket herunterladen","brief":"Digitalisierungs-Anforderungsbrief",
    "current_problem":"Ist-Prozessproblem","future_state":"Soll-Prozess",
    "user_req":"Benutzeranforderung","data_req":"Datenanforderung",
    "interface_req":"Schnittstellenannahme","role_req":"Rollen-/Zugriffsanforderung",
    "audit_req":"Audit-Trail-Anforderung","validation":"Validierungshinweis",
    "benefit":"Erwarteter Nutzen","open_questions":"Offene Fragen",
    "built_by":"Erstellt von","linkedin":"LinkedIn","github":"GitHub","contact":"Kontakt",
    "profile":"Profil","project_value":"Projektwert","skills":"Demonstrierte Fähigkeiten",
    "hire_story":"Recruiter-Story","ai_scope":"KI-/XAI-Offenlegung",
    "role":"Portfolio-Prototyp für Digital Manufacturing & Data Analytics",
    "profile_text":"PharmD + MSc Digital Health (Hochschule Deggendorf). Fünf Jahre in pharmazeutischer GMP-Herstellung, Apotheke und Healthcare Claims. Angewandte Projekte in Python, Streamlit, Datenanalytik und Prozesssimulation.",
    "project_value_text":"ProcessPulse verbindet Datenqualität, erklärbare Signale, eBR-Workflow-Routing, Prozess-Zwilling-Simulation, OEE-Schätzung und Digitalisierungsanforderungen in einem lokalen Prototyp.",
    "skills_text":"Python · Streamlit · pandas · NumPy · Plotly · SPC/Cpk · regelbasierte XAI · MES/eBR Workflow · Prozess-Zwilling · OEE · GMP-Dokumentation · zweisprachige UI · Anforderungsanalyse (URS) · Audit-Trail.",
    "hire_story_text":"Ich bringe pharmazeutisches Domänenwissen, das den meisten IT-Kandidaten fehlt, und Python/Streamlit-Buildkompetenz, die den meisten Pharma-Kandidaten fehlt. ProcessPulse beweist — statt nur zu beschreiben —, dass ich Prozessverständnis, Datenintegrität, digitalen Workflow und Anforderungsanalyse in einem kohärenten Werkzeug verbinden kann.",
    "ai_scope_text":"Keine externe KI oder API. Alle Signale werden aus transparenten, auditierbaren Regeln erzeugt: Grenzwertprüfungen, Trendfenster, Cpk-Schätzungen und Datenqualitäts-Gates. Bewusste Entscheidung — GMP-Umgebungen erfordern erklärbare, validierte Logik.",
    "rows":"Zeilen","detected":"Erkannt","missing":"Fehlend","invalid":"Ungültig / leer",
    "confidence":"Vertrauen","trusted":"Vertrauenswürdig","limited":"Begrenzt","poor":"Schwach",
    "unavailable":"Nicht verfügbar","excluded":"Aus vertrauenswürdiger Evidenz ausgeschlossen",
    "mean":"Mittelwert","last":"Letzter Wert","std":"Standardabw.","cpk":"Cpk",
    "missing_streams":"Fehlende Sensortrends ausgeschlossen.",
}}

def tr(key:str, lang:str="en") -> str:
    return I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))

def make_sample(scenario:str="normal", n:int=72) -> pd.DataFrame:
    rng = np.random.default_rng(81)
    time = pd.date_range("2026-06-14 08:00", periods=n, freq="5min")
    temperature = rng.normal(24.0,0.22,n); pressure = rng.normal(1.25,0.03,n)
    ph = rng.normal(7.10,0.03,n); flow = rng.normal(45.0,0.75,n)
    yld = rng.normal(96.0,0.45,n); quality = rng.normal(98.0,0.35,n)
    if scenario == "ph_drift":
        ph += np.linspace(0,0.34,n); quality -= np.linspace(0,1.5,n)
    elif scenario == "flow_restriction":
        flow -= np.linspace(0,8.8,n); yld -= np.linspace(0,2.2,n)
    elif scenario == "temperature_excursion":
        temperature[-12:] += np.linspace(1.2,5.2,12); quality[-12:] -= np.linspace(0.4,3.0,12)
    elif scenario == "missing_ipc":
        ph[:] = np.nan
    return pd.DataFrame({"time":time,"Temperature":temperature,"Pressure":pressure,
                         "pH":ph,"Flow":flow,"Yield":yld,"Quality":quality})

def template_csv() -> bytes:
    return make_sample("normal",12).to_csv(index=False).encode("utf-8")

def normalize_columns(df:pd.DataFrame) -> pd.DataFrame:
    rename={}
    for col in df.columns:
        raw=str(col).strip()
        low=raw.lower().replace(" ","_").replace("-","_").replace("(","").replace(")","")
        rename[col]=ALIASES.get(raw,ALIASES.get(low,raw))
    out=df.rename(columns=rename).copy()
    for col in list(dict.fromkeys(out.columns)):
        if list(out.columns).count(col)>1:
            sub=out.loc[:,out.columns==col]; out=out.drop(columns=[col])
            out[col]=sub.bfill(axis=1).iloc[:,0]
    return out

def normalize_csv(df:pd.DataFrame, source_name:str="sample") -> Dict[str,Any]:
    original_columns=list(df.columns); df=normalize_columns(df)
    detected=[c for c in REQUIRED+OPTIONAL if c in df.columns]
    missing_required=[c for c in REQUIRED if c not in df.columns]
    available=[]
    if "time" in df.columns:
        parsed=pd.to_datetime(df["time"],errors="coerce")
        if parsed.notna().sum()>0:
            df["time"]=parsed; available.append("time")
        else:
            missing_required.append("time")
    invalid_counts={}
    for col in REQUIRED+OPTIONAL:
        if col in df.columns and col!="time":
            df[col]=pd.to_numeric(df[col],errors="coerce")
            invalid_counts[col]=int(df[col].isna().sum())
            if df[col].notna().any(): available.append(col)
    quality_notes=[]
    if len(df)<15: quality_notes.append("low row count")
    for col in REQUIRED+OPTIONAL:
        if col in df.columns and col!="time" and len(df)>0 and df[col].isna().mean()>0.2:
            quality_notes.append(f"{col} has >20% missing values")
    missing_required=sorted(set(missing_required),key=lambda x:REQUIRED.index(x) if x in REQUIRED else 999)
    if len(missing_required)>=3 or len(df)<3: confidence="poor"
    elif missing_required or quality_notes or len(df)<25: confidence="limited"
    else: confidence="trusted"
    return {"df":df.reset_index(drop=True),"source_name":source_name,
            "original_columns":original_columns,"detected":detected,
            "missing_required":missing_required,"available":sorted(set(available),
            key=lambda x:(REQUIRED+OPTIONAL).index(x) if x in REQUIRED+OPTIONAL else 999),
            "invalid_counts":invalid_counts,"quality_notes":quality_notes,
            "confidence":confidence,"row_count":int(len(df))}

def safe_cpk(values, lsl:float, usl:float) -> float:
    s=pd.to_numeric(pd.Series(values),errors="coerce").dropna()
    if len(s)==0: return np.nan
    mean=float(s.mean()); sd=float(s.std(ddof=1)) if len(s)>1 else 0.0
    if np.isnan(sd) or sd<1e-12: return 9.99 if lsl<=mean<=usl else -9.99
    return float(min((usl-mean)/(3*sd),(mean-lsl)/(3*sd)))

def detect_signals(norm:Dict[str,Any]) -> List[Dict[str,Any]]:
    df=norm["df"]; signals=[]; rank={"high":3,"medium":2,"low":1}
    if norm["missing_required"]:
        signals.append({"parameter":"Data Quality",
            "severity":"high" if len(norm["missing_required"])>=2 else "medium",
            "rule":"Missing required column","step":"data",
            "evidence":f"Missing: {', '.join(norm['missing_required'])}. Detected: {', '.join(norm['detected']) or '-'}",
            "message":"Required data is not available for full prototype review.",
            "action":"Upload a CSV with time, Temperature, Pressure, pH, and Flow or continue with available trusted evidence."})
    if norm["row_count"]<15:
        signals.append({"parameter":"Data Quality","severity":"medium","rule":"Low sample size","step":"data",
            "evidence":f"{norm['row_count']} rows available.",
            "message":"SPC-style trend rules need more sequential data.",
            "action":"Use a longer time series for trend review."})
    for param,spec in RANGES.items():
        if param not in df.columns: continue
        values=pd.to_numeric(df[param],errors="coerce").dropna()
        if len(values)==0:
            signals.append({"parameter":param,"severity":"high" if param in REQUIRED else "medium",
                "rule":"No usable values","step":spec["step"],
                "evidence":f"{param} column contains no trusted numeric values.",
                "message":f"{param} cannot be evaluated.",
                "action":f"Check {param} source mapping and CSV export."})
            continue
        lsl,usl=spec["lsl"],spec["usl"]
        out=values[(values<lsl)|(values>usl)]
        if len(out):
            signals.append({"parameter":param,"severity":"high","rule":"Limit excursion","step":spec["step"],
                "evidence":f"{len(out)} value(s) outside {lsl:g}–{usl:g} {spec['unit']}. Min {values.min():.3g}, max {values.max():.3g}.",
                "message":f"{param} exceeded the prototype review range.",
                "action":f"Review {param} measurement, instrument state, batch record, and affected process step."})
        if len(values)>=16:
            window=max(8,len(values)//3); early=float(values.iloc[:window].mean())
            late=float(values.iloc[-window:].mean()); drift=late-early; span=usl-lsl
            if abs(drift)>0.18*span:
                signals.append({"parameter":param,"severity":"medium","rule":"Trend / drift","step":spec["step"],
                    "evidence":f"Early mean {early:.3g}; late mean {late:.3g}; shift {drift:.3g} {spec['unit']}.",
                    "message":f"{param} shows a meaningful shift across the run.",
                    "action":f"Check whether the {param} trend is expected, controlled, and documented."})
        cpk=safe_cpk(values,lsl,usl)
        if not np.isnan(cpk) and cpk<1.0:
            signals.append({"parameter":param,"severity":"high" if cpk<0 else "medium",
                "rule":"Low capability estimate","step":spec["step"],
                "evidence":f"Cpk {cpk:.2f}; mean {values.mean():.3g}; std {values.std(ddof=1) if len(values)>1 else 0:.3g}; range {lsl:g}–{usl:g}.",
                "message":f"{param} variability or centering is weak in this dataset.",
                "action":f"Review {param} variability before treating this dataset as stable."})
    if not signals:
        signals.append({"parameter":"Batch Data","severity":"low","rule":"No active rule trigger","step":"qc",
            "evidence":f"{norm['row_count']} rows reviewed with required trusted evidence available.",
            "message":"No active prototype signal was detected.",
            "action":"Continue review and document that no prototype rule was triggered."})
    return sorted(signals,key=lambda x:rank.get(x["severity"],0),reverse=True)

def strongest_signal(norm): return detect_signals(norm)[0]

def readiness(norm):
    sig=strongest_signal(norm); score=94
    if norm["confidence"]=="limited": score-=18
    elif norm["confidence"]=="poor": score-=42
    if sig["severity"]=="medium": score-=20
    elif sig["severity"]=="high": score-=42
    score=int(max(0,min(100,score)))
    label="trusted" if score>=80 else ("limited" if score>=50 else "blocked")
    return {"score":score,"label":label}

WORKFLOW=[("material","req_material"),("weighing","req_weighing"),("equipment","req_equipment"),
          ("charging","req_charging"),("mixing","req_mixing"),("ipc","req_ipc"),
          ("filling","req_filling"),("qc","req_qc"),("qa","req_qa")]

def workflow_steps(norm,manual=None):
    manual=manual or {}; sig=strongest_signal(norm); affected=sig.get("step","qc"); rows=[]
    for key,req in WORKFLOW:
        status="complete"; meaning="status_complete"
        if key==affected:
            status="blocked" if sig["severity"]=="high" else ("review" if sig["severity"]=="medium" else "complete")
            meaning="status_blocked" if status=="blocked" else ("status_review" if status=="review" else "status_complete")
        elif key in ["qc","qa"] and sig["severity"] in ["high","medium"]:
            status="waiting"; meaning="status_waiting"
        if key in manual: status=manual[key]["status"]; meaning=manual[key]["meaning"]
        rows.append({"key":key,"label":key,"required":req,"status":status,"meaning":meaning})
    return rows

def process_twin_result(temperature,pressure,ph,flow,mixing_speed,material_variability):
    penalties={"Temperature":abs(temperature-24.0)/6.0*22,"Pressure":abs(pressure-1.25)/0.7*14,
               "pH":abs(ph-7.10)/0.70*28,"Flow":abs(flow-45.0)/15.0*18,
               "Mixing":abs(mixing_speed-250)/160.0*8,"Material":material_variability*1.0}
    risk=float(max(0,min(100,sum(penalties.values()))))
    return {"risk":risk,"dominant":max(penalties,key=penalties.get),
            "predicted_yield":float(max(80,98-risk*0.16)),
            "quality_score":float(max(70,100-risk*0.25))}

def oee_estimate(norm):
    df=norm["df"]; sig=strongest_signal(norm); evidence=[]
    if "Downtime" in df.columns and pd.to_numeric(df["Downtime"],errors="coerce").notna().any():
        downtime=float(pd.to_numeric(df["Downtime"],errors="coerce").fillna(0).sum())
        planned=max(1.0,norm["row_count"]*5.0)
        availability=max(0,min(100,(planned-downtime)/planned*100))
        evidence.append(f"Availability from Downtime column: {downtime:.1f} min / {planned:.1f} planned min.")
    else:
        availability=78.0 if sig["severity"]=="high" else 92.0
        evidence.append("Availability estimated (no Downtime column available).")
    if "Flow" in df.columns and pd.to_numeric(df["Flow"],errors="coerce").notna().any():
        flow=pd.to_numeric(df["Flow"],errors="coerce").dropna()
        performance=max(55,min(100,100-abs(flow.mean()-45)*3-flow.std(ddof=1)*2))
        evidence.append(f"Performance from Flow mean {flow.mean():.2f}, std {flow.std(ddof=1):.2f}.")
    else:
        performance=70.0; evidence.append("Performance limited — Flow unavailable.")
    if {"GoodCount","TotalCount"}.issubset(df.columns):
        good=pd.to_numeric(df["GoodCount"],errors="coerce").dropna().sum()
        total=pd.to_numeric(df["TotalCount"],errors="coerce").dropna().sum()
        quality=float(good/total*100) if total>0 else 90.0
        evidence.append(f"Quality from counts: {good:.0f} good / {total:.0f} total.")
    else:
        quality=97.0 if sig["severity"]=="low" else (90.0 if sig["severity"]=="medium" else 82.0)
        evidence.append("Quality estimated from signal severity (no GoodCount/TotalCount).")
    oee=availability*performance*quality/10000.0
    return {"availability":availability,"performance":performance,"quality":quality,"oee":oee,"evidence":evidence}

def requirements_brief(norm):
    sig=strongest_signal(norm); param=sig["parameter"]
    return {"current_problem":f"{sig['message']} Affected area: {sig['step']}.",
            "future_state":f"{param} evidence is visible at the workflow step where it is needed, with review status and audit context.",
            "user_req":f"The system shall show {param} status, timestamp/source context, detected rule, reviewer note, and required action for the affected workflow step.",
            "data_req":f"Required data: batch/time index, {param} values, source-column mapping, reviewer, workflow step, session audit event.",
            "interface_req":"Potential real interfaces: equipment historian, MES/eBR, LIMS, QMS/deviation workflow, ERP/material context. This prototype uses CSV only.",
            "role_req":"A real implementation should separate operator entry, technical review, QA disposition review, and administrator configuration roles.",
            "audit_req":"Status changes, notes, review flags, evidence exports, and requirements outputs should create timestamped audit events.",
            "validation":"A production implementation requires approved requirements, risk assessment, traceability, test evidence, access control, backup/restore, cybersecurity review, and change control.",
            "benefit":f"Reduces manual searching for {param} evidence and connects process signals to review actions and improvement requirements.",
            "open_questions":"Which source system owns the record? Which parameters are critical? Which actions require QA review? What retention and access rules apply?"}

def evidence_pack(norm,reviewer="Demo reviewer"):
    sig=strongest_signal(norm); ready=readiness(norm); oee=oee_estimate(norm)
    lines=["ProcessPulse Evidence Pack",
           f"Generated: {datetime.now().isoformat(timespec='minutes')}",
           f"Reviewer: {reviewer}","",
           "Scope:",I18N["en"]["scope"],"",
           "Data:",f"- Rows: {norm['row_count']}",
           f"- Detected: {', '.join(norm['detected']) if norm['detected'] else '-'}",
           f"- Missing required: {', '.join(norm['missing_required']) if norm['missing_required'] else '-'}",
           f"- Confidence: {norm['confidence']}","",
           "Strongest signal:",f"- Parameter: {sig['parameter']}",
           f"- Severity: {sig['severity']}",f"- Rule: {sig['rule']}",
           f"- Message: {sig['message']}",f"- Evidence: {sig['evidence']}",
           f"- Action: {sig['action']}","",
           "Readiness:",f"- Score: {ready['score']}/100",f"- Label: {ready['label']}","",
           "Prototype OEE:",f"- Availability: {oee['availability']:.1f}%",
           f"- Performance: {oee['performance']:.1f}%",f"- Quality: {oee['quality']:.1f}%",
           f"- OEE: {oee['oee']:.1f}%"]
    lines.extend([f"- {e}" for e in oee["evidence"]])
    return "\n".join(lines)