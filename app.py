from __future__ import annotations
import base64
from datetime import datetime
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from processpulse_logic import (
    AUTHOR, EMAIL, LINKEDIN_URL, GITHUB_URL, SCENARIOS, REQUIRED, OPTIONAL, RANGES,
    tr, make_sample, template_csv, normalize_csv, detect_signals, strongest_signal,
    readiness, workflow_steps, process_twin_result, oee_estimate, requirements_brief,
    evidence_pack, safe_cpk
)

APP_DIR = Path(__file__).resolve().parent

# ── Logo with fallback ────────────────────────────────────────────────────────
def _logo_b64() -> str | None:
    for p in [APP_DIR/"assets"/"processpulse_logo.svg", APP_DIR/"processpulse_logo.svg"]:
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode("utf-8")
    return None

LOGO_B64 = _logo_b64()

st.set_page_config(page_title="ProcessPulse", page_icon="🟢", layout="wide", initial_sidebar_state="expanded")

PAGES     = ["dashboard","data","signal","workflow","twin","oee","requirements","about"]
MFG_STEPS = ["material","weighing","equipment","charging","mixing","ipc","filling","qc","qa"]
SCENARIO_LABEL = {
    "normal":               ("try_normal","Batch Data"),
    "ph_drift":             ("try_ph","pH"),
    "flow_restriction":     ("try_flow","Flow"),
    "temperature_excursion":("try_temp","Temperature"),
    "missing_ipc":          ("try_missing","pH"),
}

def init_state():
    defaults = dict(lang="en", page="dashboard", reviewer=AUTHOR, scenario="normal",
                    data_mode="sample", audit=[], manual_status={})
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
    if "norm" not in st.session_state:
        st.session_state.norm = normalize_csv(make_sample("normal"),"normal")

def add_audit(event:str):
    st.session_state.audit.append({"time":datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "actor":st.session_state.get("reviewer",AUTHOR),"event":event})

def set_scenario(sc:str):
    st.session_state.scenario=sc; st.session_state.data_mode="sample"
    st.session_state.norm=normalize_csv(make_sample(sc),sc)
    add_audit(f"Demo scenario selected: {sc}")

def navigate(page:str):
    st.session_state.page=page; st.rerun()

def sev_label(sig:dict,lang:str) -> str:
    return {"high":tr("blocked",lang),"medium":tr("review_needed",lang)}.get(sig["severity"],tr("monitor",lang))

def sev_color(sev:str) -> str:
    return {"high":"red","medium":"amber","low":"green","blocked":"red",
            "limited":"amber","trusted":"green","poor":"red","complete":"green",
            "review":"amber","waiting":"blue"}.get(sev,"blue")

# ── CSS ───────────────────────────────────────────────────────────────────────
def css():
    st.markdown("""<style>
:root{--teal:#0EA57A;--blue:#2777B8;--amber:#F4A62A;--red:#E75858;--ink:#153B4A;--muted:#617888;--line:#DDECEF;}
html,body,[class*="css"]{font-family:Inter,Segoe UI,Arial,sans-serif;}
.stApp{background:#F7FBFD;color:var(--ink);}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
.block-container{padding-top:2.5rem;padding-bottom:2rem;max-width:1240px;}
[data-testid="stAppViewContainer"]>[data-testid="stMain"]{overflow:visible;}
header[data-testid="stHeader"]{background:transparent;}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid #DDECEF;}
.logo-box{text-align:center;padding:7px 3px 10px;}
.brand-card{background:#F7FEFB;border:1px solid #CFEDE5;border-radius:14px;padding:10px;font-size:12px;color:#45616E;margin-bottom:8px;}
.nav-title{font-size:10px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#78909A;margin-top:6px;}
.hero{background:linear-gradient(135deg,#fff 0%,#EAF9F4 60%,#EEF6FF 100%);border:1px solid #D7EFE9;border-radius:20px;padding:16px 20px;margin-bottom:10px;}
.hero h1{margin:0;font-size:25px;letter-spacing:-.03em;color:#123947;}
.hero p{margin:5px 0 0;color:#526E7C;font-size:13.5px;}
.expert-box{background:#F0F7FF;border-left:4px solid #2777B8;border-radius:0 12px 12px 0;padding:10px 14px;margin-bottom:10px;font-size:12.5px;color:#1A4A6E;}
.expert-box b{color:#2777B8;}
.issue-ribbon{display:grid;grid-template-columns:1.25fr .75fr .7fr 1fr 1.35fr;gap:8px;margin-bottom:10px;}
.ribbon-cell{background:#fff;border:1px solid #DDECEF;border-radius:13px;padding:9px 12px;min-height:64px;}
.ribbon-label{color:#647887;font-size:10px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px;}
.ribbon-value{color:#123947;font-size:13.5px;font-weight:800;line-height:1.25;overflow-wrap:anywhere;}
.card{background:#fff;border:1px solid #DDECEF;border-radius:18px;padding:15px;margin-bottom:12px;overflow:hidden;}
.card h3{margin:0 0 10px;font-size:17px;color:#123947;}
.help-card{background:#F8FCFD;border:1px solid #DDECEF;border-left:5px solid #2777B8;border-radius:14px;padding:11px 14px;margin-bottom:10px;color:#385462;font-size:13.5px;}
.ticket{border:1px solid #DDECEF;border-radius:16px;padding:13px;background:#fff;margin-bottom:10px;}
.ticket-row{display:grid;grid-template-columns:160px 1fr;gap:10px;padding:7px 0;border-top:1px solid #EEF4F6;}
.ticket-row:first-child{border-top:0;}
.ticket-key{color:#647887;font-weight:850;font-size:12.5px;}
.ticket-val{color:#153B4A;font-weight:600;font-size:13.5px;line-height:1.35;}
.pill{display:inline-flex;align-items:center;padding:4px 9px;border-radius:999px;font-size:11.5px;font-weight:850;margin:2px 3px 2px 0;}
.green{background:#EAF8F2;color:#087958;}
.amber{background:#FFF5DF;color:#9D6500;}
.red{background:#FFE9E9;color:#B93333;}
.blue{background:#EAF2FF;color:#225F9C;}
.purple{background:#F0EEFF;color:#5143CE;}
.flow{display:flex;gap:7px;align-items:stretch;overflow-x:auto;padding-bottom:5px;}
.flow-node{min-width:120px;background:#fff;border:1px solid #DDECEF;border-radius:14px;padding:9px 11px;text-align:center;}
.flow-node.active{border-color:#0EA57A;background:#F2FCF8;}
.flow-node.blocked{border-color:#E75858;background:#FFF8F8;}
.flow-node.review{border-color:#F4A62A;background:#FFFBF1;}
.flow-node.waiting{border-color:#B7D9E6;background:#F7FBFD;}
.flow-title{font-weight:850;color:#123947;font-size:12.5px;}
.flow-sub{color:#647887;font-size:11px;margin-top:3px;}
.xai{border-left:5px solid #0EA57A;background:#F2FCF8;border-radius:14px;padding:13px 15px;margin:8px 0 12px;}
.xai h4{margin:0 0 6px;color:#087958;font-size:15px;}
.xai div{margin:3px 0;font-size:13px;line-height:1.35;}
.xai-rule{background:#fff;border:1px solid #CFEDE5;border-radius:8px;padding:5px 10px;margin:4px 0;font-size:12.5px;}
.legal{color:#5C6F78;font-size:11.5px;padding:12px 4px 6px;border-top:1px solid #DDECEF;margin-top:16px;}
.legal strong{color:#B93333;}
.term{background:#FBFDFE;border:1px solid #E4EEF1;border-radius:12px;padding:10px;font-size:12.5px;color:#385462;}
.term b{color:#2777B8;}
.metric-soft{background:#fff;border:1px solid #DDECEF;border-radius:14px;padding:11px;}
.metric-label{color:#647887;font-size:11px;font-weight:850;text-transform:uppercase;letter-spacing:.05em;}
.metric-value{color:#123947;font-size:21px;font-weight:900;margin-top:3px;line-height:1.15;}
.readiness-big{font-size:42px;font-weight:900;line-height:1;}
.profile-header{display:flex;gap:14px;align-items:center;margin-bottom:12px;}
.avatar{width:66px;height:66px;border-radius:20px;background:linear-gradient(135deg,#0EA57A,#2777B8);color:white;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:900;}
.about-link{display:inline-flex;align-items:center;gap:6px;background:#EAF2FF;color:#225F9C;padding:6px 14px;border-radius:999px;font-size:13px;font-weight:700;text-decoration:none;margin:4px 4px 4px 0;}
div[data-testid="stMetric"]{background:white;border:1px solid #DDECEF;padding:10px;border-radius:13px;}
.slider-spec{font-size:11px;color:#647887;margin-top:2px;}
@media(max-width:1100px){.issue-ribbon{grid-template-columns:1fr 1fr;}}
</style>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
def sidebar() -> str:
    lang = st.session_state.lang
    if LOGO_B64:
        st.sidebar.markdown(f"<div class='logo-box'><img src='data:image/svg+xml;base64,{LOGO_B64}' width='220'></div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div class='logo-box'><h2 style='color:#0EA57A'>ProcessPulse</h2></div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div class='brand-card'><b>{tr('built_by',lang)} {AUTHOR}</b><br>{tr('role',lang)}</div>", unsafe_allow_html=True)
    lc = st.sidebar.radio("Language / Sprache", ["English","Deutsch"], index=1 if lang=="de" else 0, horizontal=True)
    new_lang = "de" if lc=="Deutsch" else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang; st.rerun()
    lang = st.session_state.lang
    st.sidebar.text_input(tr("reviewer",lang), key="reviewer")
    st.sidebar.markdown("<div class='nav-title'>Navigation</div>", unsafe_allow_html=True)
    for page in PAGES:
        t = "primary" if st.session_state.page==page else "secondary"
        if st.sidebar.button(tr(page,lang), key=f"nav_{page}", use_container_width=True, type=t):
            st.session_state.page=page; st.rerun()
    st.sidebar.markdown("---")
    sc = st.sidebar.selectbox(tr("scenario",lang), SCENARIOS, index=SCENARIOS.index(st.session_state.scenario),
                               format_func=lambda s: tr(SCENARIO_LABEL[s][0],lang))
    if sc != st.session_state.scenario: set_scenario(sc)
    uploaded = st.sidebar.file_uploader(tr("upload_csv",lang), type=["csv"], key="global_upload")
    if uploaded:
        try:
            df=pd.read_csv(uploaded); st.session_state.norm=normalize_csv(df,uploaded.name)
            st.session_state.data_mode="uploaded"; add_audit(f"CSV uploaded: {uploaded.name}")
            st.sidebar.success(tr("use_csv",lang))
        except Exception as e: st.sidebar.error(f"CSV error: {e}")
    else:
        if st.session_state.data_mode!="uploaded":
            st.session_state.norm=normalize_csv(make_sample(st.session_state.scenario),st.session_state.scenario)
        st.sidebar.caption(tr("use_sample",lang))
    st.sidebar.download_button(tr("download_template",lang), data=template_csv(),
                                file_name="processpulse_template.csv", mime="text/csv")
    st.sidebar.warning(tr("not_decision",lang))
    st.sidebar.caption(tr("scope",lang))
    return lang

# ── Shared components ─────────────────────────────────────────────────────────
def page_header(page:str, lang:str):
    expert_key = f"expert_{page}"
    st.markdown(f"""<div class='hero'>
<span class='pill green'>● Live</span><span class='pill blue'>Local rules</span><span class='pill amber'>Prototype</span>
<h1>{tr(page,lang)}</h1>
<p style='margin-bottom:6px;'>{tr(page+'_help',lang)}</p>
<div style='font-size:12px;color:#2777B8;border-top:1px solid #D7EFE9;padding-top:7px;margin-top:4px;'><b>Technical scope:</b> {tr(expert_key,lang)}</div>
</div>""", unsafe_allow_html=True)
    issue_ribbon(lang)

def issue_info(lang:str) -> dict:
    norm=st.session_state.norm; sig=strongest_signal(norm)
    if sig["rule"]=="No active rule trigger": title=tr("no_active",lang)
    elif st.session_state.data_mode=="sample": title=tr(SCENARIO_LABEL.get(st.session_state.scenario,("try_normal",""))[0],lang)
    else: title=f"{sig['parameter']} · {sig['rule']}"
    affected=tr(sig.get("step","qc"),lang) if sig.get("step") in MFG_STEPS or sig.get("step")=="data" else sig.get("step","-")
    return {"sig":sig,"title":title,"parameter":sig.get("parameter",SCENARIO_LABEL.get(st.session_state.scenario,("","Batch Data"))[1]),
            "severity":sev_label(sig,lang),"affected":affected,"action":sig.get("action","-")}

def issue_ribbon(lang:str):
    info=issue_info(lang)
    cells=[(tr("selected_issue",lang),info["title"]),(tr("parameter",lang),info["parameter"]),
           (tr("severity",lang),info["severity"]),(tr("affected_step",lang),info["affected"]),
           (tr("next_action",lang),info["action"])]
    html="<div class='issue-ribbon'>"+"".join(f"<div class='ribbon-cell'><div class='ribbon-label'>{l}</div><div class='ribbon-value'>{v}</div></div>" for l,v in cells)+"</div>"
    st.markdown(html, unsafe_allow_html=True)

def help_box(key:str, lang:str):
    st.markdown(f"<div class='help-card'><b>{tr('page_help',lang)}:</b> {tr(key,lang)}</div>", unsafe_allow_html=True)

def legal(lang:str):
    st.markdown(f"<div class='legal'><strong>{tr('not_decision',lang)}:</strong> {tr('scope',lang)}<br><b>Data:</b> {tr('data_privacy',lang)}</div>", unsafe_allow_html=True)

def xai_box(sig:dict, lang:str):
    """Rich XAI box with per-rule plain-language explanation."""
    rule=sig.get("rule",""); evidence=sig.get("evidence",""); message=sig.get("message",""); action=sig.get("action","")
    color=sev_color(sig["severity"])

    if rule=="Missing required column":
        insight = ("Required columns are absent. Without them, the affected analysis is excluded from trusted evidence — consistent with ALCOA+ data-integrity: data must be attributable, legible, contemporaneous, original, and accurate before being used for decisions."
                   if lang=="en" else
                   "Pflichtspalten fehlen. Die betroffene Analyse wird aus vertrauenswürdiger Evidenz ausgeschlossen — konsistent mit ALCOA+ Datenintegrität.")
    elif rule=="Trend / drift":
        insight = ("A systematic shift between the early and late window means is detected. In a controlled GMP process, trends require investigation: is the shift caused by equipment drift, reagent depletion, or environmental change?"
                   if lang=="en" else
                   "Eine systematische Verschiebung zwischen dem frühen und späten Fenster wurde erkannt. In einem kontrollierten GMP-Prozess erfordern Trends eine Untersuchung.")
    elif rule=="Low capability estimate":
        insight = ("Cpk < 1.0 means the process distribution does not comfortably fit inside the review limits. A Cpk of 1.33 is often the minimum target for a validated pharmaceutical process. Values below 1.0 signal that the process needs centering or variability reduction."
                   if lang=="en" else
                   "Cpk < 1,0 bedeutet, die Prozessverteilung passt nicht stabil in die Prüfgrenzen. In validierten pharmazeutischen Prozessen wird oft Cpk ≥ 1,33 als Mindestziel gesetzt.")
    elif rule=="Limit excursion":
        insight = ("One or more values outside the specification limit. In a real MES/eBR environment this would trigger a deviation record, CAPA workflow, and potentially a batch-hold — the affected workflow step reflects this."
                   if lang=="en" else
                   "Ein oder mehrere Werte liegen außerhalb der Spezifikationsgrenze. In einem realen MES/eBR würde dies eine Abweichungsmeldung, CAPA-Workflow und ggf. Charge-Hold auslösen.")
    elif rule=="No usable values":
        insight = ("Column exists in the CSV but contains no parseable numeric values. Common causes: unit suffixes left in the cell, comma vs decimal-point locale mismatch, or text placeholders."
                   if lang=="en" else
                   "Spalte vorhanden, aber ohne lesbare numerische Werte. Häufige Ursachen: Einheitensuffix in der Zelle, Komma-/Dezimalpunkt-Lokalisierung, oder Textplatzhalter.")
    elif rule=="No active rule trigger":
        insight = ("All trusted parameters are within prototype review limits with no detected trend or capability issue. In a real system this would still require documented review and sign-off."
                   if lang=="en" else
                   "Alle vertrauenswürdigen Parameter liegen im Prüfbereich ohne erkannten Trend oder Fähigkeitsproblem. In einem realen System würde trotzdem eine dokumentierte Prüfung erforderlich sein.")
    else:
        insight = message

    st.markdown(f"""<div class='xai'>
<h4>{tr('signal',lang) if 'signal' in tr.__code__.co_consts else 'Signal'} &nbsp;
<span class='pill {color}'>{sev_label(sig,lang)}</span></h4>
<div class='xai-rule'><b>{tr('rule',lang)}:</b> {rule}</div>
<div class='xai-rule'><b>{tr('evidence',lang)}:</b> {evidence}</div>
<div class='xai-rule'><b>{tr('why',lang)}:</b> {insight}</div>
<div class='xai-rule'><b>{tr('action',lang)}:</b> {action}</div>
</div>""", unsafe_allow_html=True)

def ticket_html(sig:dict, lang:str):
    info=issue_info(lang)
    rows=[(tr("selected_issue",lang),info["title"]),(tr("parameter",lang),sig.get("parameter","-")),
          (tr("severity",lang),sev_label(sig,lang)),(tr("rule",lang),sig.get("rule","-")),
          (tr("evidence",lang),sig.get("evidence","-")),(tr("affected_step",lang),info["affected"]),
          (tr("action",lang),sig.get("action","-"))]
    html="<div class='ticket'>"+"".join(f"<div class='ticket-row'><div class='ticket-key'>{k}</div><div class='ticket-val'>{v}</div></div>" for k,v in rows)+"</div>"
    st.markdown(html, unsafe_allow_html=True)

def process_flow_html(lang:str, active:str="Signal"):
    FLOW=["Data","Signal","Workflow","Evidence","Requirements"]
    label_map={"Data":tr("data",lang),"Signal":tr("signal",lang),"Workflow":tr("workflow",lang),"Evidence":tr("oee",lang),"Requirements":tr("requirements",lang)}
    html="<div class='flow'>"+"".join(f"<div class='flow-node {'active' if s==active else ''}'><div class='flow-title'>{label_map[s]}</div><div class='flow-sub'>{s}</div></div>" for s in FLOW)+"</div>"
    st.markdown(html, unsafe_allow_html=True)

def manufacturing_flow_html(lang:str):
    steps=workflow_steps(st.session_state.norm, st.session_state.manual_status)
    sig=strongest_signal(st.session_state.norm); affected=sig.get("step","qc")
    html="<div class='flow'>"+"".join(f"<div class='flow-node {s['status']} {'active' if s['key']==affected else ''}'><div class='flow-title'>{tr(s['label'],lang)}</div><div class='flow-sub'>{tr(s['status'],lang)}</div></div>" for s in steps)+"</div>"
    st.markdown(html, unsafe_allow_html=True)

def plot_spc(param:str, lang:str):
    df=st.session_state.norm["df"]
    if param not in df.columns or pd.to_numeric(df[param],errors="coerce").dropna().empty:
        st.warning(f"{param}: {tr('unavailable',lang)} — {tr('excluded',lang)}."); return
    spec=RANGES[param]; y=pd.to_numeric(df[param],errors="coerce")
    x=df["time"] if "time" in df.columns else list(range(len(df)))
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode="lines+markers",name=param,
                              line=dict(color="#0EA57A",width=2),marker=dict(size=4)))
    fig.add_hline(y=spec["usl"],line_dash="dash",line_color="#E75858",annotation_text=f"USL {spec['usl']:g}")
    fig.add_hline(y=spec["lsl"],line_dash="dash",line_color="#E75858",annotation_text=f"LSL {spec['lsl']:g}")
    fig.add_hline(y=y.mean(),line_dash="dot",line_color="#2777B8",annotation_text=tr("mean",lang))
    fig.add_hrect(y0=spec["lsl"],y1=spec["usl"],fillcolor="rgba(14,165,122,0.05)",line_width=0)
    fig.update_layout(template="plotly_white",height=320,margin=dict(l=20,r=20,t=32,b=20),
                       title=f"{tr('chart',lang)}: {param} ({spec['unit']})" if spec['unit'] else f"{tr('chart',lang)}: {param}")
    st.plotly_chart(fig, use_container_width=True)

def plot_sensors(lang:str):
    df=st.session_state.norm["df"]
    available=[c for c in ["Temperature","Pressure","pH","Flow"] if c in df.columns and pd.to_numeric(df[c],errors="coerce").dropna().shape[0]>0]
    missing=[c for c in ["Temperature","Pressure","pH","Flow"] if c not in available]
    if not available: st.warning(tr("missing_streams",lang)); return
    x=df["time"] if "time" in df.columns else list(range(len(df)))
    colors={"Temperature":"#E75858","Pressure":"#2777B8","pH":"#0EA57A","Flow":"#F4A62A"}
    fig=go.Figure()
    for c in available:
        fig.add_trace(go.Scatter(x=x,y=pd.to_numeric(df[c],errors="coerce"),mode="lines",name=c,
                                  line=dict(color=colors.get(c,"#617888"),width=1.8)))
    fig.update_layout(template="plotly_white",height=320,margin=dict(l=20,r=20,t=32,b=20),title=tr("sensor_streams",lang))
    st.plotly_chart(fig, use_container_width=True)
    if missing: st.info(f"{tr('missing_streams',lang)}: {', '.join(missing)}")

def data_quality_table(lang:str):
    norm=st.session_state.norm; rows=[]
    for col in REQUIRED+OPTIONAL:
        ok=col in norm["available"]
        rows.append({"Column":col,tr("review_status",lang):tr("complete",lang) if ok else tr("unavailable",lang),
                     tr("invalid",lang):norm["invalid_counts"].get(col,"-") if col!="time" else "-",
                     tr("trusted_columns",lang):"✓" if ok else "✗"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── Pages ─────────────────────────────────────────────────────────────────────
def page_dashboard(lang:str):
    page_header("dashboard",lang)
    sig=strongest_signal(st.session_state.norm); ready=readiness(st.session_state.norm)

    # Readiness score prominently on dashboard
    r_color="green" if ready["label"]=="trusted" else ("amber" if ready["label"]=="limited" else "red")
    st.markdown(f"""<div class='card' style='text-align:center;padding:14px;'>
<div class='metric-label'>{tr('readiness_score',lang)}</div>
<div class='readiness-big'><span class='pill {r_color}' style='font-size:28px;padding:8px 20px;'>{ready['score']}/100</span></div>
<div style='color:#617888;font-size:12px;margin-top:6px;'>{tr(ready["label"],lang)} — {tr('data',lang)}: {st.session_state.norm["confidence"]}</div>
</div>""", unsafe_allow_html=True)

    left,right = st.columns([1.2,1])
    with left:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("signal_ticket",lang))
        ticket_html(sig,lang)
        if st.button(f"{tr('open',lang)} {tr('signal',lang)}", type="primary"): navigate("signal")
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("process_flow",lang))
        process_flow_html(lang,"Signal")
        st.write(tr("demo_explain",lang))
        st.subheader(tr("try_demo",lang))
        for sc,key in [("normal","try_normal"),("ph_drift","try_ph"),("flow_restriction","try_flow"),
                        ("temperature_excursion","try_temp"),("missing_ipc","try_missing")]:
            t="primary" if st.session_state.scenario==sc and st.session_state.data_mode=="sample" else "secondary"
            if st.button(tr(key,lang), key=f"demo_{sc}", use_container_width=True, type=t):
                set_scenario(sc); st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)

    # Command modules with meaningful descriptions
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("command_modules",lang))
    cols=st.columns(4)
    modules=[("data","data_help"),("workflow","workflow_help"),("twin","twin_help"),("requirements","requirements_help")]
    for i,(page,hk) in enumerate(modules):
        with cols[i]:
            st.markdown(f"<div class='metric-soft'><div class='metric-label'>{tr(page,lang)}</div><div style='font-size:12px;color:#617888;margin-top:5px;min-height:48px;'>{tr(hk,lang)}</div></div>",unsafe_allow_html=True)
            if st.button(tr("open",lang), key=f"open_{page}"): navigate(page)
    st.markdown("</div>",unsafe_allow_html=True)
    xai_box(sig,lang)
    legal(lang)

def page_data(lang:str):
    page_header("data",lang)
    left,right=st.columns([1,1])
    with left:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("upload_csv",lang))
        st.write(tr("required_columns",lang)+": `"+ ", ".join(REQUIRED)+"`")
        st.caption(tr("accepted_aliases",lang))
        st.info(tr("missing_not_faked",lang))
        up=st.file_uploader(tr("upload_csv",lang), type=["csv"], key="data_upload")
        if up:
            try:
                df=pd.read_csv(up); st.session_state.norm=normalize_csv(df,up.name)
                st.session_state.data_mode="uploaded"; add_audit(f"CSV uploaded: {up.name}"); st.success(tr("use_csv",lang))
            except Exception as e: st.error(f"CSV error: {e}")
        st.download_button(tr("download_template",lang),data=template_csv(),file_name="processpulse_template.csv",mime="text/csv")
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        norm=st.session_state.norm
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("quality_gate",lang))
        c1,c2,c3=st.columns(3)
        c1.metric(tr("rows",lang),norm["row_count"])
        c2.metric(tr("trusted_columns",lang),len(norm["available"]))
        c3.metric(tr("excluded_columns",lang),len([c for c in REQUIRED+OPTIONAL if c not in norm["available"]]))
        if norm["missing_required"]: st.warning(f"{tr('missing',lang)}: {', '.join(norm['missing_required'])}")
        else: st.success(tr("trusted",lang))
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    data_quality_table(lang)
    st.markdown("</div>",unsafe_allow_html=True)
    xai_box(strongest_signal(st.session_state.norm),lang)
    legal(lang)

def page_signal(lang:str):
    page_header("signal",lang)
    sig=strongest_signal(st.session_state.norm)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("signal_ticket",lang))
    ticket_html(sig,lang)
    st.markdown("</div>",unsafe_allow_html=True)

    st.markdown("<div class='card'>",unsafe_allow_html=True)
    available=[p for p in ["pH","Temperature","Pressure","Flow","Yield","Quality"]
               if p in st.session_state.norm["df"].columns and pd.to_numeric(st.session_state.norm["df"][p],errors="coerce").dropna().shape[0]>0]
    if available:
        default=available.index(sig["parameter"]) if sig["parameter"] in available else 0
        param=st.selectbox(tr("focus_parameter",lang),available,index=default)
        plot_spc(param,lang)
        spec=RANGES[param]; s=pd.to_numeric(st.session_state.norm["df"][param],errors="coerce").dropna()
        c1,c2,c3,c4=st.columns(4)
        c1.metric(tr("mean",lang),f"{s.mean():.3g} {spec['unit']}")
        c2.metric(tr("last",lang),f"{s.iloc[-1]:.3g} {spec['unit']}")
        c3.metric(tr("std",lang),f"{s.std(ddof=1) if len(s)>1 else 0:.3g}")
        cpk_val=safe_cpk(s,spec["lsl"],spec["usl"])
        c4.metric(tr("cpk",lang),f"{cpk_val:.2f}" if not pd.isna(cpk_val) else "N/A",
                   help="Cpk ≥ 1.33 = capable process (pharma target). < 1.0 = action needed.")
        st.caption(f"Safe zone: {spec['lsl']:g} – {spec['usl']:g} {spec['unit']} | Center: {spec['center']:g} {spec['unit']}")
    else:
        st.warning(tr("missing_streams",lang))
    st.markdown("</div>",unsafe_allow_html=True)

    # Rich glossary — 5 cards including GMP context
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("plain_terms",lang))
    g1,g2,g3,g4,g5=st.columns(5)
    for col,key in zip([g1,g2,g3,g4,g5],["spc_plain","cpk_plain","xai_plain","oee_plain","gcpk_plain"]):
        with col: st.markdown(f"<div class='term'>{tr(key,lang)}</div>",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    xai_box(sig,lang)
    legal(lang)

def page_workflow(lang:str):
    page_header("workflow",lang)
    sig=strongest_signal(st.session_state.norm)
    steps=workflow_steps(st.session_state.norm,st.session_state.manual_status)
    affected_key=sig.get("step","qc")
    if affected_key=="data": affected_key="material"
    default_idx=next((i for i,s in enumerate(steps) if s["key"]==affected_key),0)
    labels=[tr(s["label"],lang) for s in steps]
    left,right=st.columns([.9,1.1])
    with left:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("affected_first",lang))
        selected=st.selectbox(tr("all_steps",lang),labels,index=default_idx)
        step=steps[labels.index(selected)]
        st.markdown(f"<div class='flow-node {step['status']} active'><div class='flow-title'>{selected}</div><div class='flow-sub'>{tr(step['status'],lang)}</div></div>",unsafe_allow_html=True)
        st.write(f"**{tr('required_fields',lang)}:** {tr(step['required'],lang)}")
        st.write(f"**{tr('why',lang)}:** {tr(step['meaning'],lang)}")
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("workflow",lang))
        note=st.text_area(tr("review_note",lang),key="workflow_note")
        def update(status,meaning):
            st.session_state.manual_status[step["key"]]={"status":status,"meaning":meaning}
            add_audit(f"{selected} → {status}. Note: {note.strip() or '-'}"); st.success(tr("saved",lang))
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button(tr("mark_complete",lang),type="primary",use_container_width=True): update("complete","status_complete")
        with c2:
            if st.button(tr("flag_review",lang),use_container_width=True):
                update("review","status_review") if note.strip() else st.warning(tr("note_required",lang))
        with c3:
            if st.button(tr("block_step",lang),use_container_width=True):
                update("blocked","status_blocked") if note.strip() else st.warning(tr("note_required",lang))
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("manufacturing_flow",lang))
    manufacturing_flow_html(lang)
    st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("audit",lang))
    audit=st.session_state.audit or [{"time":"-","actor":st.session_state.reviewer,"event":"Session ready"}]
    st.dataframe(pd.DataFrame(audit[-20:]),use_container_width=True,hide_index=True)
    st.markdown("</div>",unsafe_allow_html=True)
    xai_box(sig,lang)
    legal(lang)

def page_twin(lang:str):
    page_header("twin",lang)
    sig=strongest_signal(st.session_state.norm)
    focus=sig["parameter"] if sig["parameter"] in ["Temperature","Pressure","pH","Flow"] else SCENARIO_LABEL.get(st.session_state.scenario,("","pH"))[1]
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("process_twin_title",lang))
    st.info(f"🎯 {tr('focus_parameter',lang)}: **{focus}** — pre-set to active signal parameter.")
    c1,c2,c3=st.columns(3)
    with c1:
        temperature=st.slider(("🎯 " if focus=="Temperature" else "")+tr("temperature",lang),18.0,32.0,24.0,0.1)
        st.markdown(f"<div class='slider-spec'>{tr('safe_zone',lang)}: 20–28 °C</div>",unsafe_allow_html=True)
        ph=st.slider(("🎯 " if focus=="pH" else "")+"pH",6.50,7.80,7.10,0.01)
        st.markdown(f"<div class='slider-spec'>{tr('safe_zone',lang)}: 6.80–7.40</div>",unsafe_allow_html=True)
    with c2:
        pressure=st.slider(("🎯 " if focus=="Pressure" else "")+tr("pressure",lang),0.70,1.90,1.25,0.01)
        st.markdown(f"<div class='slider-spec'>{tr('safe_zone',lang)}: 0.90–1.60 bar</div>",unsafe_allow_html=True)
        flow=st.slider(("🎯 " if focus=="Flow" else "")+tr("flow",lang),25.0,65.0,45.0,0.5)
        st.markdown(f"<div class='slider-spec'>{tr('safe_zone',lang)}: 38–52 L/min</div>",unsafe_allow_html=True)
    with c3:
        mixing=st.slider(tr("mixing_speed",lang),120,420,250,5)
        st.markdown(f"<div class='slider-spec'>{tr('safe_zone',lang)}: 200–300 RPM</div>",unsafe_allow_html=True)
        material=st.slider(tr("material_variability",lang),0.0,12.0,2.0,0.5)
        st.markdown(f"<div class='slider-spec'>{tr('safe_zone',lang)}: 0–4%</div>",unsafe_allow_html=True)
    res=process_twin_result(temperature,pressure,ph,flow,mixing,material)
    risk_color="🔴" if res["risk"]>50 else ("🟡" if res["risk"]>20 else "🟢")
    m1,m2,m3,m4=st.columns(4)
    m1.metric(tr("predicted_yield",lang),f"{res['predicted_yield']:.1f}%")
    m2.metric(tr("quality_score",lang),f"{res['quality_score']:.1f}/100")
    m3.metric(tr("risk_score",lang),f"{risk_color} {res['risk']:.0f}/100")
    m4.metric(tr("risk_driver",lang),res["dominant"])
    if st.button(tr("add_sim",lang),type="primary"):
        new=pd.DataFrame([{"time":datetime.now(),"Temperature":temperature,"Pressure":pressure,"pH":ph,"Flow":flow,"Yield":res["predicted_yield"],"Quality":res["quality_score"]}])
        st.session_state.norm=normalize_csv(pd.concat([st.session_state.norm["df"],new],ignore_index=True),"working data + twin")
        add_audit("Process Twin simulation row added"); st.success(tr("sim_added",lang))
    st.markdown("</div>",unsafe_allow_html=True)
    xai_box(sig,lang)
    legal(lang)

def page_oee(lang:str):
    page_header("oee",lang)
    left,right=st.columns([1.25,.8])
    with left:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("sensor_streams",lang))
        plot_sensors(lang)
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("prototype_oee",lang))
        o=oee_estimate(st.session_state.norm)
        st.metric(tr("availability",lang),f"{o['availability']:.1f}%",help="Planned time minus downtime, divided by planned time.")
        st.metric(tr("performance",lang),f"{o['performance']:.1f}%",help="Estimated from Flow stability vs target 45 L/min.")
        st.metric(tr("quality",lang),f"{o['quality']:.1f}%",help="From GoodCount/TotalCount if available, else from signal severity.")
        st.metric(tr("oee",lang),f"{o['oee']:.1f}%",help="OEE = Availability × Performance × Quality / 10,000. World-class ≥ 85%.")
        st.info(tr("oee_plain",lang))
        st.subheader(tr("oee_cause",lang))
        for ev in o["evidence"]: st.write(f"• {ev}")
        st.markdown("</div>",unsafe_allow_html=True)
    xai_box(strongest_signal(st.session_state.norm),lang)
    legal(lang)

def page_requirements(lang:str):
    page_header("requirements",lang)
    sig=strongest_signal(st.session_state.norm)
    param=sig["parameter"]
    affected=tr(sig.get("step","qc"),lang) if sig.get("step") in MFG_STEPS or sig.get("step")=="data" else sig.get("step","QC")
    if lang=="de":
        brief={"current_problem":f"{param}: {sig['message']} Betroffener Schritt: {affected}.",
               "future_state":f"{param}-Evidenz ist direkt im betroffenen Workflow-Schritt sichtbar.",
               "user_req":f"Das System soll {param}-Status, Evidenz, Prüfernotiz und empfohlene Aktion im Schritt {affected} anzeigen.",
               "data_req":f"Benötigt: Zeitindex, {param}-Werte, Grenzbereich, Quellspalte, Prüfer, Workflow-Schritt, Audit-Ereignis.",
               "interface_req":"Mögliche Schnittstellen: Historian, MES/eBR, LIMS, QMS/Abweichung, ERP. Dieser Prototyp nutzt CSV.",
               "role_req":"Rollen sollten Bediener, technische Prüfung, QA-Disposition und Administration trennen.",
               "audit_req":"Statusänderungen, Notizen, Flags und Exporte sollten auditierbar gespeichert werden.",
               "validation":"Echte Implementierung braucht URS, Risikoanalyse, Tests, Zugriffskontrolle, Backup, Cybersecurity, Change Control.",
               "benefit":f"Schnellere Verbindung von {param}-Evidenz mit Workflow-Aktion und Verbesserungsanforderung.",
               "open_questions":"Welches System ist führend? Welche Parameter sind kritisch? Welche Aktionen benötigen QA-Prüfung?"}
    else:
        brief=requirements_brief(st.session_state.norm)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("brief",lang))
    for key,value in brief.items():
        st.markdown(f"**{tr(key,lang)}**"); st.write(value)
    pack=evidence_pack(st.session_state.norm,st.session_state.reviewer)
    st.download_button(tr("download_pack",lang),data=pack,file_name="processpulse_evidence_pack.txt",mime="text/plain",type="primary")
    st.markdown("</div>",unsafe_allow_html=True)
    xai_box(sig,lang)
    legal(lang)

def page_about(lang:str):
    st.markdown(f"""<div class='hero'>
<span class='pill green'>Portfolio</span><span class='pill blue'>Python / Streamlit</span><span class='pill amber'>Synthetic prototype</span>
<h1>{tr('about',lang)}</h1>
<p style='margin-bottom:6px;'>{tr('about_help',lang)}</p>
<div style='font-size:12px;color:#2777B8;border-top:1px solid #D7EFE9;padding-top:7px;margin-top:4px;'><b>Technical scope:</b> {tr('expert_about',lang)}</div>
</div>""", unsafe_allow_html=True)
    left,right=st.columns([.95,1.05])
    with left:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.markdown(f"""<div class='profile-header'>
<div class='avatar'>RM</div>
<div><h3 style='margin:0;'>{AUTHOR}</h3>
<div style='color:#617888;font-size:13px;'>PharmD · MSc Digital Health · Digital Manufacturing</div></div></div>""",unsafe_allow_html=True)
        st.markdown(f"""<a class='about-link' href='mailto:{EMAIL}'>✉ {EMAIL}</a>
<a class='about-link' href='{LINKEDIN_URL}' target='_blank'>🔗 LinkedIn</a>
<a class='about-link' href='{GITHUB_URL}' target='_blank'>💻 GitHub</a>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("profile",lang))
        st.write(tr("profile_text",lang))
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("project_value",lang))
        st.write(tr("project_value_text",lang))
        process_flow_html(lang,"Requirements")
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("skills",lang))
        st.write(tr("skills_text",lang))
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.subheader(tr("ai_scope",lang))
        st.info(tr("ai_scope_text",lang))
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader(tr("not_decision",lang))
    st.error(tr("scope",lang))
    st.markdown("</div>",unsafe_allow_html=True)
    legal(lang)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    css(); init_state(); lang=sidebar(); page=st.session_state.page
    dispatch={"dashboard":page_dashboard,"data":page_data,"signal":page_signal,
              "workflow":page_workflow,"twin":page_twin,"oee":page_oee,
              "requirements":page_requirements,"about":page_about}
    dispatch.get(page,page_dashboard)(lang)

if __name__=="__main__":
    main()