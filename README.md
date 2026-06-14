# ProcessPulse

A hireable Streamlit portfolio prototype for Digital Manufacturing & Data Analytics job applications.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What it demonstrates

ProcessPulse connects one selected manufacturing issue across the full review path:

Data Intake -> Signal & XAI -> Workflow/eBR -> Process Twin -> Sensors/OEE -> Requirements Brief.

The app supports CSV upload, sample scenarios, rule-based XAI, SPC/Cpk, workflow actions, audit trail, process twin simulation, sensor trends, prototype OEE, evidence pack export, bilingual UI, and legal scope statements.

## CSV format

Recommended:

```csv
time,Temperature,Pressure,pH,Flow,Yield,Quality
2026-06-14 09:00,24.5,1.25,7.10,45.0,96,98
```

Accepted aliases include timestamp, temp, pressure_bar, ph, flow_rate, yield_pct, and quality_pct.

## Scope

Synthetic portfolio prototype only. Not a validated GMP, MES, ERP, LIMS, QMS, SCADA, eBR, electronic signature, quality decision, or batch-release system. Not for real manufacturing, regulatory, patient-impacting, or safety-critical use.

No external API or cloud AI is used.
