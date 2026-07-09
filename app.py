import streamlit as st
import pickle
import os

st.set_page_config(
    page_title="Breast Cancer Prediction Platform",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Clash+Display:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap');

/* ── Base ── */
html, body, [class*="css"], [data-testid] {
    font-family: 'DM Sans', sans-serif !important;
}
h1,h2,h3,h4,h5 { font-family: 'Manrope', sans-serif !important; }

/* ── Layout ── */
.block-container { padding: 2.2rem 3rem 5rem !important; max-width: 1280px !important; }

/* ── Keep toolbar visible ── */
[data-testid="stToolbar"] { z-index: 999 !important; }
header button span.material-symbols-rounded {
    font-size: 0 !important; overflow: hidden !important;
    width: 20px !important; display: inline-block !important;
}
[data-testid="stMainMenuPopover"] li:first-child span { font-size: 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #f0f2f8 !important;
    box-shadow: 2px 0 20px rgba(0,0,0,0.04) !important;
}

/* ── Sidebar collapse button ── */
[data-testid="stSidebarCollapseButton"] { visibility: visible !important; opacity: 1 !important; }
[data-testid="stSidebarCollapseButton"] button {
    background: #3b82f6 !important; border-radius: 8px !important;
    border: none !important; width: 28px !important; height: 28px !important;
    padding: 0 !important; box-shadow: 0 2px 6px rgba(59,130,246,0.3) !important;
}
[data-testid="stSidebarCollapseButton"] button span { font-size: 0 !important; overflow: hidden !important; }
[data-testid="stSidebarCollapseButton"] button svg { fill: white !important; width: 16px !important; height: 16px !important; }

/* ── Nav buttons — fully clickable styled buttons ── */
[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100% !important;
    min-height: 56px !important;
    opacity: 1 !important;
    cursor: pointer !important;
    border-radius: 11px !important;
    border: 1.5px solid #e8edf5 !important;
    background: #ffffff !important;
    margin-bottom: 0.2rem !important;
    padding: 0.6rem 0.8rem !important;
    text-align: left !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    color: #334155 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    position: relative !important;
    margin-top: 0 !important;
    line-height: 1.3 !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #f0f7ff !important;
    border-color: #3b82f6 !important;
    color: #1e40af !important;
    box-shadow: 0 3px 12px rgba(59,130,246,0.18) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    color: inherit !important;
    margin: 0 !important;
    white-space: pre-line !important;
}

/* ── Radio hidden ── */
[data-testid="stSidebar"] .stRadio { display: none !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important; border-color: #e8edf5 !important;
    font-family: 'DM Sans', sans-serif !important;
    background: #f8faff !important;
}

/* ── Hero ── */
.hero-wrap {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%);
    border-radius: 22px; padding: 3rem 3.5rem; margin-bottom: 2rem;
    position: relative; overflow: hidden;
    box-shadow: 0 24px 64px rgba(37,99,235,0.28);
    max-width: calc(100% - 120px) !important;
}
.hero-wrap::before {
    content:''; position:absolute; top:-120px; right:-80px;
    width:420px; height:420px;
    background:radial-gradient(circle,rgba(96,165,250,0.2) 0%,transparent 65%);
    border-radius:50%; pointer-events:none;
}
.hero-wrap::after {
    content:''; position:absolute; bottom:-80px; left:38%;
    width:280px; height:280px;
    background:radial-gradient(circle,rgba(139,92,246,0.15) 0%,transparent 65%);
    border-radius:50%; pointer-events:none;
}
.hero-eyebrow {
    display:inline-flex; align-items:center;
    background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.22);
    color:#bfdbfe !important; font-size:0.68rem; font-weight:700;
    letter-spacing:0.16em; text-transform:uppercase;
    padding:0.28rem 0.9rem; border-radius:100px; margin-bottom:1.2rem;
}
.hero-h1 {
    font-family:'Manrope',sans-serif !important; font-size:2.6rem !important;
    font-weight:800 !important; color:#ffffff !important; line-height:1.15 !important;
    margin:0 0 1rem !important; letter-spacing:-0.03em;
}
.hero-h1 em { color:#93c5fd; font-style:normal; }
.hero-p { font-size:1.02rem; color:rgba(255,255,255,0.7) !important; max-width:560px; line-height:1.72; margin:0; }
.hero-stats {
    display:flex; gap:3rem; margin-top:2.2rem;
    padding-top:2rem; border-top:1px solid rgba(255,255,255,0.1);
}
.hstat-val { font-family:'Manrope',sans-serif; font-size:2.1rem; font-weight:800; color:#93c5fd !important; line-height:1; }
.hstat-lbl { font-size:0.68rem; color:rgba(255,255,255,0.42) !important; text-transform:uppercase; letter-spacing:0.12em; margin-top:0.3rem; }

/* ── Cards ── */
.pcard {
    background:#ffffff; border:1px solid #eef1f8;
    border-radius:18px; padding:1.7rem 2rem; margin-bottom:1.2rem;
    box-shadow:0 2px 16px rgba(15,23,42,0.05);
    transition:box-shadow 0.2s, border-color 0.2s;
}
.pcard:hover { box-shadow:0 8px 32px rgba(15,23,42,0.09); border-color:#d4e0f7; }
.pcard-title {
    font-family:'Manrope',sans-serif; font-size:1rem; font-weight:800;
    color:#0f172a !important; margin:0 0 1.1rem !important;
    display:flex; align-items:center; gap:0.6rem;
}
.pcard-accent {
    width:4px; height:20px; flex-shrink:0;
    background:linear-gradient(180deg,#3b82f6,#8b5cf6);
    border-radius:3px; display:inline-block;
}

/* ── Step list ── */
.step-row { display:flex; align-items:flex-start; gap:1rem; padding:0.85rem 0; border-bottom:1px solid #f8fafc; }
.step-row:last-child { border-bottom:none; }
.step-num {
    width:30px; height:30px; flex-shrink:0;
    background:linear-gradient(135deg,#3b82f6,#6366f1); border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-family:'Manrope',sans-serif; font-size:0.78rem; font-weight:800; color:white !important;
}
.step-text { font-size:0.9rem; color:#475569 !important; line-height:1.6; padding-top:0.25rem; }

/* ── Metric strip ── */
.mstrip { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.8rem; }
.mcard {
    background:#fff; border:1px solid #eef1f8; border-radius:16px;
    padding:1.3rem 1.5rem; box-shadow:0 2px 10px rgba(15,23,42,0.05);
    position:relative; overflow:hidden;
}
.mcard::after {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,#3b82f6,#8b5cf6);
}
.mcard-lbl { font-size:0.67rem; font-weight:700; text-transform:uppercase; letter-spacing:0.12em; color:#94a3b8 !important; margin-bottom:0.45rem; }
.mcard-val { font-family:'Manrope',sans-serif; font-size:1.6rem; font-weight:800; color:#0f172a !important; line-height:1; }
.mcard-sub { font-size:0.68rem; color:#cbd5e1 !important; margin-top:0.35rem; }

/* ── Verdict ── */
.verdict-m { background:linear-gradient(135deg,#fff1f2,#ffe4e6); border:2px solid #fecaca; border-radius:18px; padding:2rem; text-align:center; box-shadow:0 6px 24px rgba(239,68,68,0.12); }
.verdict-b { background:linear-gradient(135deg,#f0fdf4,#dcfce7); border:2px solid #bbf7d0; border-radius:18px; padding:2rem; text-align:center; box-shadow:0 6px 24px rgba(34,197,94,0.12); }
.vlabel-m { font-family:'Manrope',sans-serif; font-size:2.4rem; font-weight:800; color:#dc2626 !important; letter-spacing:-0.03em; }
.vlabel-b { font-family:'Manrope',sans-serif; font-size:2.4rem; font-weight:800; color:#16a34a !important; letter-spacing:-0.03em; }
.vconf { font-size:0.85rem; color:#94a3b8 !important; margin-top:0.4rem; }

/* ── Prob bars ── */
.prob-wrap { margin:1.1rem 0; }
.prob-hd { display:flex; justify-content:space-between; font-size:0.83rem; color:#64748b !important; margin-bottom:0.4rem; font-weight:500; }
.pbar-bg { height:10px; background:#f1f5f9; border-radius:100px; overflow:hidden; }
.pbar-m { height:100%; border-radius:100px; background:linear-gradient(90deg,#ef4444,#f87171); }
.pbar-b { height:100%; border-radius:100px; background:linear-gradient(90deg,#22c55e,#86efac); }

/* ── Model pills ── */
.mpill { display:inline-block; background:#eff6ff; border:1px solid #bfdbfe; color:#3b82f6 !important; font-size:0.76rem; font-weight:600; padding:0.22rem 0.7rem; border-radius:100px; margin:0.15rem 0.1rem; }

/* ── Input group header ── */
.ig-header {
    background:linear-gradient(90deg,#eff6ff,transparent);
    border-left:3px solid #3b82f6; padding:0.5rem 1rem;
    border-radius:0 8px 8px 0; margin:1.6rem 0 0.9rem;
    font-family:'Manrope',sans-serif; font-size:0.8rem; font-weight:700;
    color:#1d4ed8 !important; text-transform:uppercase; letter-spacing:0.07em;
}

/* ── Submit button ── */
[data-testid="stFormSubmitButton"] > button {
    background:linear-gradient(135deg,#2563eb 0%,#7c3aed 100%) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    font-family:'Manrope',sans-serif !important; font-weight:700 !important;
    font-size:1rem !important; padding:0.75rem 2rem !important;
    box-shadow:0 4px 20px rgba(37,99,235,0.38) !important;
    letter-spacing:0.01em !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow:0 6px 28px rgba(37,99,235,0.52) !important;
    transform:translateY(-1px) !important;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input {
    border-radius:9px !important; border-color:#e8edf5 !important;
    font-family:'DM Sans',sans-serif !important; font-size:0.88rem !important;
    background:#fafbff !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color:#3b82f6 !important; box-shadow:0 0 0 3px rgba(59,130,246,0.12) !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label { font-size:0.88rem !important; color:#475569 !important; font-weight:500 !important; }

/* ── Table ── */
.ptable { width:100%; border-collapse:collapse; font-size:0.86rem; }
.ptable th { background:#f8faff; color:#64748b !important; font-family:'Manrope',sans-serif; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; padding:0.7rem 1rem; text-align:left; border-bottom:2px solid #eef1f8; }
.ptable td { padding:0.65rem 1rem; color:#334155 !important; border-bottom:1px solid #f8fafc; }
.ptable tr:last-child td { border-bottom:none; }
.ptable td:first-child { font-weight:700; color:#1e40af !important; }

/* ── Dataset mini cards ── */
.ds-grid { display:grid; grid-template-columns:1fr 1fr; gap:0.9rem; margin-top:1rem; }
.ds-card { border-radius:12px; padding:1rem 1.1rem; }
.ds-val { font-family:'Manrope',sans-serif; font-size:1.6rem; font-weight:800; line-height:1; }
.ds-lbl { font-size:0.72rem; color:#94a3b8 !important; margin-top:0.25rem; }

/* ── Model info cards ── */
.mic { background:#fff; border:1px solid #eef1f8; border-radius:13px; padding:1.1rem 1.3rem; margin-bottom:0.65rem; box-shadow:0 1px 6px rgba(15,23,42,0.04); transition:all 0.18s; }
.mic:hover { border-color:#bfdbfe; box-shadow:0 4px 16px rgba(59,130,246,0.09); }
.mic.active { border-color:#3b82f6; background:linear-gradient(135deg,#f8fbff,#eff6ff); box-shadow:0 4px 16px rgba(59,130,246,0.12); }
.mic-name { font-family:'Manrope',sans-serif; font-size:0.93rem; font-weight:800; color:#0f172a !important; margin-bottom:0.35rem; }
.mic-desc { font-size:0.83rem; color:#64748b !important; line-height:1.58; margin-bottom:0.65rem; }
.tag-g { display:inline-block; background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d !important; font-size:0.7rem; padding:0.12rem 0.55rem; border-radius:100px; margin:0.12rem; font-weight:600; }
.tag-a { display:inline-block; background:#fffbeb; border:1px solid #fde68a; color:#92400e !important; font-size:0.7rem; padding:0.12rem 0.55rem; border-radius:100px; margin:0.12rem; font-weight:600; }
.badge-active { display:inline-block; background:#dbeafe; border:1px solid #93c5fd; color:#1d4ed8 !important; font-size:0.64rem; font-weight:800; padding:0.1rem 0.45rem; border-radius:100px; margin-left:0.4rem; text-transform:uppercase; letter-spacing:0.08em; }

/* ── SHAP ── */
.shap-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; margin:1rem 0; }
.shap-item { background:#f5f3ff; border:1px solid #ddd6fe; border-radius:12px; padding:1rem 1.1rem; }
.shap-title { font-family:'Manrope',sans-serif; font-weight:800; color:#6d28d9 !important; font-size:0.87rem; margin-bottom:0.4rem; }
.shap-desc { font-size:0.8rem; color:#6b7280 !important; line-height:1.55; }

/* ── Info/warn bars ── */
.info-bar { background:#eff6ff; border:1px solid #bfdbfe; border-left:4px solid #3b82f6; border-radius:10px; padding:0.85rem 1.2rem; font-size:0.85rem; color:#1e40af !important; margin-top:1.2rem; }
.warn-bar { background:#fff7ed; border:1px solid #fed7aa; border-left:4px solid #f97316; border-radius:10px; padding:0.85rem 1.2rem; font-size:0.85rem; color:#9a3412 !important; margin-top:1.2rem; }

/* ── Sidebar brand ── */
.sb-brand { padding:0.4rem 0 1.5rem; border-bottom:1px solid #f0f2f8; margin-bottom:1.3rem; }
.sb-brand-name { font-family:'Manrope',sans-serif; font-size:1.3rem; font-weight:800; color:#0f172a !important; letter-spacing:-0.03em; }
.sb-brand-name span { color:#3b82f6; }
.sb-brand-sub { font-size:0.66rem; color:#94a3b8 !important; margin-top:0.15rem; letter-spacing:0.07em; text-transform:uppercase; }
.sec-label { font-size:0.66rem; font-weight:800; text-transform:uppercase; letter-spacing:0.14em; color:#94a3b8 !important; margin-bottom:0.65rem; }
.active-chip { margin-top:0.7rem; padding:0.8rem 1rem; background:#f0f7ff; border:1.5px solid #bfdbfe; border-radius:12px; }
.active-chip-lbl { font-size:0.66rem; font-weight:700; color:#94a3b8 !important; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.25rem; }
.active-chip-val { font-family:'Manrope',sans-serif; font-size:0.95rem; font-weight:800; color:#1d4ed8 !important; }

/* ── Empty state ── */
.empty-state { text-align:center; padding:4rem 2rem; }
.empty-title { font-family:'Manrope',sans-serif; font-size:1.15rem; font-weight:800; color:#0f172a !important; margin-bottom:0.4rem; }
.empty-sub { font-size:0.88rem; color:#94a3b8 !important; line-height:1.6; }
</style>

""", unsafe_allow_html=True)

# ─── Model registry ───────────────────────────────────────────────────────────
MODEL_REGISTRY = {
    "Logistic Regression": ("logistic_regression.pkl", True),
    "Random Forest":       ("random_forest.pkl",       False),
    "Decision Tree":       ("decision_tree.pkl",       False),
    "SVM":                 ("svm.pkl",                 True),
    "KNN":                 ("knn.pkl",                 True),
}
MODEL_ICONS = {"Logistic Regression":"LR","Random Forest":"RF","Decision Tree":"DT","SVM":"SVM","KNN":"KNN"}

def _default_model():
    path = os.path.join("models","model_name.pkl")
    if os.path.exists(path):
        with open(path,"rb") as f:
            name = pickle.load(f)
        if name in MODEL_REGISTRY: return name
    return "Logistic Regression"

for k,v in [("selected_model",_default_model()),("prediction_result",None),("feature_values",None),("page","Home")]:
    if k not in st.session_state: st.session_state[k] = v

# ─── Inject JS via components to hide contrast_mode text ─────────────────────
import streamlit.components.v1 as components
components.html("""
<script>
(function() {
    function fix() {
        document.querySelectorAll('span').forEach(function(s) {
            var t = s.innerText ? s.innerText.trim() : '';
            if (t === 'contrast_mode' || t === 'keyboard_double_arrow_left' ||
                t === 'keyboard_double_arrow_right' || t === 'arrow_downward' ||
                t === 'expand_more' || t === 'close' || t === 'menu') {
                s.style.cssText = 'font-size:0!important;width:0!important;overflow:hidden!important;';
            }
        });
    }
    fix();
    setInterval(fix, 300);
    new MutationObserver(fix).observe(document.documentElement, {childList:true,subtree:true});
})();
</script>
""", height=0)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
NAV_ITEMS = [
    ("Home",       "H", "Overview & statistics"),
    ("Assessment", "A", "Input measurements"),
    ("Results",    "R", "Prediction dashboard"),
    ("About",      "I", "Models & methodology"),
]

with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-name">🩺 Breast<span>AI</span></div>
        <div class="sb-brand-sub">Clinical Prediction Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Navigation</div>', unsafe_allow_html=True)

    NAV_CONFIG = [
        ("Home",       "⌂", "#3b82f6", "Overview"),
        ("Assessment", "✦", "#8b5cf6", "Input data"),
        ("Results",    "◈", "#0891b2", "Dashboard"),
        ("About",      "◉", "#059669", "Methodology"),
    ]
    for name, icon_chr, colour, sub in NAV_CONFIG:
        is_active = st.session_state.page == name
        bg_icon  = colour if is_active else "#f1f5f9"
        fg_icon  = "white" if is_active else "#94a3b8"
        card_bg  = f"linear-gradient(135deg,{colour}18,{colour}08)" if is_active else "#ffffff"
        border   = colour if is_active else "#e8edf5"
        shadow   = f"0 2px 10px {colour}30" if is_active else "0 1px 3px rgba(0,0,0,0.04)"
        lbl_col  = colour if is_active else "#334155"
        sub_col  = colour + "bb" if is_active else "#94a3b8"

        # Inject per-button active styling
        active_bg = f"linear-gradient(135deg,{colour}18,{colour}08)" if is_active else "#ffffff"
        active_border = colour if is_active else "#e8edf5"
        active_color = colour if is_active else "#334155"
        active_shadow = f"0 2px 10px {colour}30" if is_active else "0 1px 4px rgba(0,0,0,0.05)"
        st.markdown(f"""<style>
        div[data-testid="stSidebar"] div[data-testid="stButton"]:has(button[key="nav_{name}"]) button,
        div[data-testid="stSidebar"] div[data-testid="stButton"] button[data-testid="baseButton-secondary"]:nth-of-type(1) {{}}
        </style>""", unsafe_allow_html=True)

        btn_label = f"{icon_chr}  {name}\n{sub}"
        if st.button(btn_label, key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Model Selection</div>', unsafe_allow_html=True)
    selected = st.selectbox("", list(MODEL_REGISTRY.keys()),
        index=list(MODEL_REGISTRY.keys()).index(st.session_state.selected_model),
        label_visibility="collapsed")
    st.session_state.selected_model = selected

    icon_sel = MODEL_ICONS[selected]
    st.markdown(f"""
    <div class="active-chip">
        <div class="active-chip-lbl">Active Model</div>
        <div class="active-chip-val">{selected}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.68rem;color:#cbd5e1;text-align:center;padding-top:1rem;border-top:1px solid #e2e8f5;">Wisconsin Diagnostic Dataset · UCI ML Repository<br>MSc Data Science</div>', unsafe_allow_html=True)

# ─── Helpers ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model(fn):
    path = os.path.join("models", fn)
    if not os.path.exists(path): return None
    with open(path,"rb") as f: return pickle.load(f)

@st.cache_resource
def load_scaler():
    path = os.path.join("models","scaler.pkl")
    if not os.path.exists(path): return None
    with open(path,"rb") as f: return pickle.load(f)

FEATURE_GROUPS = {
    "Mean Values": [
        ("radius_mean",14.13,6.98,28.11),("texture_mean",19.29,9.71,39.28),
        ("perimeter_mean",91.97,43.79,188.5),("area_mean",654.9,143.5,2501.0),
        ("smoothness_mean",0.096,0.053,0.163),("compactness_mean",0.104,0.019,0.345),
        ("concavity_mean",0.089,0.0,0.427),("concave points_mean",0.049,0.0,0.201),
        ("symmetry_mean",0.181,0.106,0.304),("fractal_dimension_mean",0.063,0.05,0.097),
    ],
    "Standard Error Values": [
        ("radius_se",0.405,0.112,2.873),("texture_se",1.217,0.36,4.885),
        ("perimeter_se",2.866,0.757,21.98),("area_se",40.34,6.802,542.2),
        ("smoothness_se",0.007,0.002,0.031),("compactness_se",0.025,0.002,0.135),
        ("concavity_se",0.032,0.0,0.396),("concave points_se",0.012,0.0,0.053),
        ("symmetry_se",0.021,0.008,0.079),("fractal_dimension_se",0.004,0.001,0.03),
    ],
    "Worst Values": [
        ("radius_worst",16.27,7.93,36.04),("texture_worst",25.68,12.02,49.54),
        ("perimeter_worst",107.3,50.41,251.2),("area_worst",880.6,185.2,4254.0),
        ("smoothness_worst",0.132,0.071,0.223),("compactness_worst",0.254,0.027,1.058),
        ("concavity_worst",0.272,0.0,1.252),("concave points_worst",0.115,0.0,0.291),
        ("symmetry_worst",0.290,0.156,0.664),("fractal_dimension_worst",0.084,0.055,0.208),
    ],
}
FEATURE_NAMES = [f for grp in FEATURE_GROUPS.values() for f,*_ in grp]

page = st.session_state.page

# ─── PAGE: Home ──────────────────────────────────────────────────────────────
if page == "Home":
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow">+ Clinical Decision Support · MSc Prototype</div>
        <h1 class="hero-h1">Breast Cancer<br><em>Prediction Platform</em></h1>
        <p class="hero-p">A multi-model clinical AI platform that analyses 30 diagnostic measurements from fine needle aspirate imaging to classify tumours — with SHAP-powered interpretability and live model switching.</p>
        <div class="hero-stats">
            <div><div class="hstat-val">569</div><div class="hstat-lbl">Training Samples</div></div>
            <div><div class="hstat-val">30</div><div class="hstat-lbl">Diagnostic Features</div></div>
            <div><div class="hstat-val">5</div><div class="hstat-lbl">ML Models</div></div>
            <div><div class="hstat-val">SHAP</div><div class="hstat-lbl">Interpretability</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9], gap="large")
    with col1:
        st.markdown("""
        <div class="pcard">
            <div class="pcard-title"><span class="pcard-accent"></span>About this Platform</div>
            <p style="color:#475569;font-size:0.92rem;line-height:1.72;margin:0 0 1.1rem;">
            This platform uses the <strong style="color:#1d4ed8;">Breast Cancer Wisconsin Diagnostic Dataset</strong>
            (UCI ML Repository) to train and compare five machine learning classifiers. It is designed
            as a professional decision-support prototype — not a replacement for clinical diagnosis.
            </p>
            <div>
                <span class="mpill">Logistic Regression</span>
                <span class="mpill">Random Forest</span>
                <span class="mpill">Decision Tree</span>
                <span class="mpill">SVM</span>
                <span class="mpill">KNN</span>
            </div>
        </div>
        <div class="pcard">
            <div class="pcard-title"><span class="pcard-accent"></span>Platform Modules</div>
            <table class="ptable">
                <tr><th>Module</th><th>Purpose</th></tr>
                <tr><td>Home</td><td>Platform overview and statistics</td></tr>
                <tr><td>Assessment</td><td>Input 30 diagnostic values and run prediction</td></tr>
                <tr><td>Results</td><td>Confidence scores, probability breakdown, interpretation</td></tr>
                <tr><td>About</td><td>Model details, metrics, and SHAP explainability</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="pcard">
            <div class="pcard-title"><span class="pcard-accent"></span>Quick Start</div>
            <div class="step-row">
                <div class="step-num">1</div>
                <div class="step-text">Select a model from the <strong style="color:#2563eb;">Model Selection</strong> dropdown in the sidebar</div>
            </div>
            <div class="step-row">
                <div class="step-num">2</div>
                <div class="step-text">Navigate to <strong style="color:#2563eb;">Assessment</strong> and enter the 30 diagnostic measurements</div>
            </div>
            <div class="step-row">
                <div class="step-num">3</div>
                <div class="step-text">Click <strong style="color:#2563eb;">Run Clinical Assessment</strong> to generate a prediction</div>
            </div>
            <div class="step-row">
                <div class="step-num">4</div>
                <div class="step-text">Open <strong style="color:#2563eb;">Results</strong> for the full dashboard with confidence scores</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        active_icon = MODEL_ICONS[st.session_state.selected_model]
        st.markdown(f"""
        <div class="pcard" style="border-color:#bfdbfe;background:#f0f7ff;">
            <div class="pcard-title"><span class="pcard-accent"></span>Active Model</div>
            <div style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:800;color:#1d4ed8;margin:0.3rem 0 0.4rem;">{active_icon} {st.session_state.selected_model}</div>
            <div style="font-size:0.82rem;color:#64748b;">Switch anytime from the sidebar — predictions update instantly.</div>
        </div>
        """, unsafe_allow_html=True)

# ─── PAGE: Assessment ─────────────────────────────────────────────────────────
elif page == "Assessment":
    st.markdown("""
    <div class="hero-wrap" style="padding:2rem 2.8rem;">
        <div class="hero-eyebrow">01  ·  Data Input</div>
        <h1 class="hero-h1" style="font-size:2.1rem;">Clinical <em>Assessment</em></h1>
        <p class="hero-p" style="font-size:0.95rem;">Enter the 30 FNA diagnostic measurements. Default values represent dataset means.</p>
    </div>
    """, unsafe_allow_html=True)

    icon = MODEL_ICONS[st.session_state.selected_model]
    st.markdown(f"""
    <div style="display:inline-flex;align-items:center;gap:0.6rem;background:#eff6ff;
         border:1px solid #bfdbfe;border-radius:100px;padding:0.4rem 1rem;margin-bottom:1.5rem;">
        <span>{icon}</span>
        <span style="font-size:0.83rem;color:#1d4ed8;font-weight:600;">Active Model: {st.session_state.selected_model}</span>
        <span style="font-size:0.75rem;color:#94a3b8;">· Change in sidebar</span>
    </div>
    """, unsafe_allow_html=True)

    feature_values = {}
    with st.form("assessment_form"):
        for group_name, features in FEATURE_GROUPS.items():
            st.markdown(f'<div class="ig-header">{group_name}</div>', unsafe_allow_html=True)
            cols = st.columns(2)
            for i, (name, default, min_v, max_v) in enumerate(features):
                with cols[i % 2]:
                    feature_values[name] = st.number_input(
                        label=name.replace("_"," ").title(),
                        min_value=float(min_v), max_value=float(max_v),
                        value=float(default), step=float((max_v-min_v)/200),
                        format="%.5f", key=f"feat_{name}"
                    )
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔬  Run Clinical Assessment", use_container_width=True)

    if submitted:
        model_file, needs_scaling = MODEL_REGISTRY[st.session_state.selected_model]
        model = load_model(model_file)
        scaler = load_scaler()
        if model is None:
            st.error(f"Model file models/{model_file} not found. Run the training notebook first.")
        else:
            import numpy as np
            X = np.array([[feature_values[n] for n in FEATURE_NAMES]])
            Xs = scaler.transform(X) if (needs_scaling and scaler) else X
            pred = model.predict(Xs)[0]
            prob = model.predict_proba(Xs)[0]
            st.session_state.prediction_result = {
                "model": st.session_state.selected_model,
                "prediction": int(pred),
                "prob_benign": float(prob[0]),
                "prob_malignant": float(prob[1]),
            }
            st.session_state.feature_values = feature_values
            label = "Malignant" if pred == 1 else "Benign"
            conf = prob[1] if pred == 1 else prob[0]
            colour = "#dc2626" if pred == 1 else "#16a34a"
            bg = "#fff1f2" if pred == 1 else "#f0fdf4"
            border = "#fecaca" if pred == 1 else "#bbf7d0"
            icon2 = '!' if pred == 1 else '✓'
            st.markdown(
                f'<div style="margin-top:1.5rem;background:{bg};border:1.5px solid {border};'
                f'border-radius:14px;padding:1.4rem 1.8rem;display:flex;align-items:center;gap:1.2rem;">'
                f'<div style="width:40px;height:40px;border-radius:50%;background:{"#fee2e2" if pred==1 else "#dcfce7"};display:flex;align-items:center;justify-content:center;flex-shrink:0;font-family:Outfit,sans-serif;font-size:1.3rem;font-weight:900;color:{"#dc2626" if pred==1 else "#16a34a"}">{icon2}</div>'
                f'<div><div style="font-family:Outfit,sans-serif;font-size:1.15rem;font-weight:800;color:{colour};">'
                f'{label} — {conf:.1%} Confidence</div>'
                f'<div style="font-size:0.84rem;color:#64748b;margin-top:0.2rem;">'
                f'Assessment complete · Navigate to Results for the full dashboard</div></div></div>',
                unsafe_allow_html=True
            )

# ─── PAGE: Results ────────────────────────────────────────────────────────────
elif page == "Results":
    st.markdown("""
    <div class="hero-wrap" style="padding:2rem 2.8rem;">
        <div class="hero-eyebrow">02  ·  Prediction Dashboard</div>
        <h1 class="hero-h1" style="font-size:2.1rem;">Diagnosis <em>Results</em></h1>
        <p class="hero-p" style="font-size:0.95rem;">Confidence scores, probability breakdown, and clinical interpretation.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.prediction_result is None:
        st.markdown("""
        <div class="pcard empty-state">
            <div style="width:64px;height:64px;border-radius:16px;background:#eff6ff;display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;color:#3b82f6;">Rx</div>
            <div class="empty-title">No Assessment Completed Yet</div>
            <div class="empty-sub">Go to Assessment, enter the diagnostic measurements, and run the model first.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        res = st.session_state.prediction_result
        pred = res["prediction"]
        prob_b = res["prob_benign"]
        prob_m = res["prob_malignant"]
        model_used = res["model"]
        label = "Malignant" if pred == 1 else "Benign"
        conf = prob_m if pred == 1 else prob_b
        result_colour = "#dc2626" if pred == 1 else "#16a34a"

        st.markdown(
            f'<div class="mstrip">'
            f'<div class="mcard"><div class="mcard-lbl">Prediction</div>'
            f'<div class="mcard-val" style="color:{result_colour};">{label}</div>'
            f'<div class="mcard-sub">Primary classification</div></div>'
            f'<div class="mcard"><div class="mcard-lbl">Confidence</div>'
            f'<div class="mcard-val">{conf:.1%}</div>'
            f'<div class="mcard-sub">Model certainty</div></div>'
            f'<div class="mcard"><div class="mcard-lbl">Model Used</div>'
            f'<div class="mcard-val" style="font-size:1.1rem;">{MODEL_ICONS[model_used]} {model_used}</div>'
            f'<div class="mcard-sub">Active classifier</div></div>'
            f'<div class="mcard"><div class="mcard-lbl">Benign Probability</div>'
            f'<div class="mcard-val">{prob_b:.1%}</div>'
            f'<div class="mcard-sub">P(Benign)</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1.1], gap="large")
        with col1:
            vc = "verdict-m" if pred == 1 else "verdict-b"
            lc = "vlabel-m" if pred == 1 else "vlabel-b"
            icon_big = '!' if pred == 1 else '✓'
            pm_pct = f"{prob_m*100:.1f}%"
            pb_pct = f"{prob_b*100:.1f}%"
            st.markdown(
                f'<div class="{vc}">'
                f'<div style="width:52px;height:52px;border-radius:50%;background:{"#fee2e2" if pred==1 else "#dcfce7"};display:flex;align-items:center;justify-content:center;margin:0 auto 0.8rem;font-family:Outfit,sans-serif;font-size:1.6rem;font-weight:900;color:{"#dc2626" if pred==1 else "#16a34a"}">{icon_big}</div>'
                f'<div class="{lc}">{label}</div>'
                f'<div class="vconf">{conf:.1%} confidence · {model_used}</div></div>'
                f'<div class="pcard" style="margin-top:1rem;">'
                f'<div class="pcard-title"><span class="pcard-accent"></span>Probability Breakdown</div>'
                f'<div class="prob-wrap"><div class="prob-hd"><span>Malignant</span>'
                f'<span style="color:#dc2626;font-weight:700;">{prob_m:.1%}</span></div>'
                f'<div class="pbar-bg"><div class="pbar-m" style="width:{pm_pct};"></div></div></div>'
                f'<div class="prob-wrap"><div class="prob-hd"><span>Benign</span>'
                f'<span style="color:#16a34a;font-weight:700;">{prob_b:.1%}</span></div>'
                f'<div class="pbar-bg"><div class="pbar-b" style="width:{pb_pct};"></div></div></div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            if pred == 1:
                heading = "The model predicts this tumour is likely Malignant."
                heading_colour = "#b91c1c"
                body = ("The measured characteristics are consistent with malignant tissue patterns. "
                        "Further clinical evaluation, biopsy confirmation, and specialist review are strongly recommended.")
                disclaimer_class = "warn-bar"
            else:
                heading = "The model predicts this tumour is likely Benign."
                heading_colour = "#15803d"
                body = ("The measured features are consistent with benign tissue patterns. "
                        "Routine monitoring and follow-up with a clinical professional is advised.")
                disclaimer_class = "info-bar"

            disclaimer = "This tool is a decision-support prototype and must not be used as a sole clinical diagnosis."

            st.markdown(
                f'<div class="pcard">'
                f'<div class="pcard-title"><span class="pcard-accent"></span>Clinical Interpretation</div>'
                f'<p style="color:{heading_colour};font-weight:700;margin:0 0 0.8rem;font-size:0.95rem;">{heading}</p>'
                f'<p style="color:#475569;font-size:0.88rem;line-height:1.72;margin:0;">{body}</p>'
                f'<div class="{disclaimer_class}">{disclaimer}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        if st.session_state.feature_values:
            show = st.checkbox("View submitted feature values", value=False)
            if show:
                import pandas as pd
                fv = st.session_state.feature_values
                df = pd.DataFrame({"Feature": list(fv.keys()), "Value": [round(v,5) for v in fv.values()]})
                st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown(
            '<div class="info-bar">💡 Switch the active model in the sidebar and re-run the assessment to compare predictions across all five classifiers.</div>',
            unsafe_allow_html=True
        )

# ─── PAGE: About ─────────────────────────────────────────────────────────────
elif page == "About":
    st.markdown("""
    <div class="hero-wrap" style="padding:2rem 2.8rem;">
        <div class="hero-eyebrow">03  ·  Documentation</div>
        <h1 class="hero-h1" style="font-size:2.1rem;">Models &amp; <em>Methodology</em></h1>
        <p class="hero-p" style="font-size:0.95rem;">Dataset, model rationale, evaluation metrics, and SHAP interpretability.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        st.markdown("""
        <div class="pcard">
            <div class="pcard-title"><span class="pcard-accent"></span>Dataset</div>
            <p style="color:#475569;font-size:0.88rem;line-height:1.7;margin:0 0 0.5rem;">
                <strong style="color:#1d4ed8;">Breast Cancer Wisconsin (Diagnostic) Dataset</strong><br>
                <span style="color:#94a3b8;">UCI Machine Learning Repository</span>
            </p>
            <div class="ds-grid">
                <div class="ds-card" style="background:#eff6ff;border:1px solid #bfdbfe;">
                    <div class="ds-val" style="color:#1d4ed8;">569</div><div class="ds-lbl">Patient samples</div>
                </div>
                <div class="ds-card" style="background:#eff6ff;border:1px solid #bfdbfe;">
                    <div class="ds-val" style="color:#1d4ed8;">30</div><div class="ds-lbl">Numeric features</div>
                </div>
                <div class="ds-card" style="background:#f0fdf4;border:1px solid #bbf7d0;">
                    <div class="ds-val" style="color:#16a34a;">357</div><div class="ds-lbl">Benign cases</div>
                </div>
                <div class="ds-card" style="background:#fff1f2;border:1px solid #fecaca;">
                    <div class="ds-val" style="color:#dc2626;">212</div><div class="ds-lbl">Malignant cases</div>
                </div>
            </div>
        </div>
        <div class="pcard">
            <div class="pcard-title"><span class="pcard-accent"></span>Evaluation Metrics</div>
            <table class="ptable">
                <tr><th>Metric</th><th>Clinical rationale</th></tr>
                <tr><td>Recall</td><td>Minimise false negatives — missed malignancies</td></tr>
                <tr><td>ROC-AUC</td><td>Overall discriminative power</td></tr>
                <tr><td>Precision</td><td>Avoid unnecessary false alarms</td></tr>
                <tr><td>F1-Score</td><td>Harmonic mean of precision &amp; recall</td></tr>
                <tr><td>Accuracy</td><td>Overall correctness (secondary)</td></tr>
                <tr><td>FN / FP</td><td>Absolute clinical risk counts</td></tr>
            </table>
            <div style="margin-top:0.9rem;font-size:0.78rem;color:#94a3b8;font-style:italic;">Selection priority: Recall → ROC-AUC → Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-label" style="margin-bottom:0.7rem;">Deployed Models</div>', unsafe_allow_html=True)
        model_data = {
            "Logistic Regression":{"icon":"📈","desc":"Linear model estimating malignancy probability via logistic function. Fast, interpretable, strong clinical baseline.","pros":["Interpretable","Fast","Probabilistic"],"cons":["Linear boundary only"],"scale":True},
            "Random Forest":{"icon":"🌲","desc":"Ensemble of decision trees on random feature subsets. Captures non-linear patterns, robust to outliers.","pros":["Non-linear","Robust","Feature importance"],"cons":["Less interpretable"],"scale":False},
            "Decision Tree":{"icon":"🌿","desc":"Single tree splitting on the most informative feature at each node. Transparent and easy to visualise.","pros":["Fully transparent","No scaling","Visual"],"cons":["Overfitting risk"],"scale":False},
            "SVM":{"icon":"⚡","desc":"RBF-kernel SVM finds maximum-margin hyperplane. Excellent in high-dimensional spaces. Calibrated for probabilities.","pros":["High-dim strength","Strong generalisation"],"cons":["Less interpretable"],"scale":True},
            "KNN":{"icon":"🔍","desc":"Classifies by majority label among 5 nearest neighbours. Intuitive and non-parametric.","pros":["Simple","Non-parametric"],"cons":["Slow at scale","Feature sensitive"],"scale":True},
        }
        for name, info in model_data.items():
            is_active = name == st.session_state.selected_model
            ac = "mic active" if is_active else "mic"
            badge = '<span class="badge-active">Active</span>' if is_active else ""
            scale = '<span style="font-size:0.7rem;color:#94a3b8;"> · requires scaling</span>' if info["scale"] else ""
            pros = "".join([f'<span class="tag-g">{p}</span>' for p in info["pros"]])
            cons = "".join([f'<span class="tag-a">{c}</span>' for c in info["cons"]])
            st.markdown(
                f'<div class="{ac}"><div class="mic-name">{info["icon"]} {name}{badge}{scale}</div>'
                f'<div class="mic-desc">{info["desc"]}</div><div>{pros}{cons}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("""
    <div class="pcard" style="margin-top:0.5rem;border-color:#ddd6fe;background:#faf5ff;">
        <div class="pcard-title">
            <span class="pcard-accent" style="background:linear-gradient(180deg,#8b5cf6,#a78bfa);"></span>
            SHAP — Interpretability Layer
        </div>
        <p style="color:#475569;font-size:0.88rem;line-height:1.7;margin:0 0 1rem;">
            SHAP (SHapley Additive exPlanations) answers: <em>"How much did each feature push this prediction toward Malignant or Benign?"</em>
            Applied to <strong style="color:#7c3aed;">Random Forest</strong> (TreeExplainer) and
            <strong style="color:#7c3aed;">Logistic Regression</strong> (LinearExplainer).
        </p>
        <div class="shap-grid">
            <div class="shap-item"><div class="shap-title">■ Summary Plot</div>
                <div class="shap-desc">Global feature influence across all test samples. Dot colour shows feature magnitude.</div></div>
            <div class="shap-item"><div class="shap-title">▪ Bar Plot</div>
                <div class="shap-desc">Mean absolute SHAP values ranked by importance — overall feature ranking.</div></div>
            <div class="shap-item"><div class="shap-title">▾ Waterfall Plot</div>
                <div class="shap-desc">Single patient explanation — each bar shows one feature's contribution to the prediction.</div></div>
        </div>
        <div style="margin-top:0.8rem;font-size:0.82rem;color:#6b7280;">
            Top predictive features:
            <code style="background:#ede9fe;color:#6d28d9;padding:0.1rem 0.45rem;border-radius:5px;font-size:0.78rem;">worst concave points</code>
            <code style="background:#ede9fe;color:#6d28d9;padding:0.1rem 0.45rem;border-radius:5px;font-size:0.78rem;">worst radius</code>
            <code style="background:#ede9fe;color:#6d28d9;padding:0.1rem 0.45rem;border-radius:5px;font-size:0.78rem;">mean concave points</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
