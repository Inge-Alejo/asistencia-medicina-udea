import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Fondo general: Verde oscuro institucional UdeA y esmeralda profundo */
    .stApp {
        background: linear-gradient(135deg, #03140e 0%, #062319 50%, #021a12 100%);
        color: #f0fdf4;
    }

    /* Hero Banner Institucional UdeA */
    .hero-container {
        background: linear-gradient(135deg, rgba(6, 46, 33, 0.85) 0%, rgba(3, 26, 18, 0.95) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 20px;
        padding: 2.2rem 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(14px);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: -40%;
        right: -15%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-badge-udea {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border: 1px solid rgba(52, 211, 153, 0.35);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 40%, #a7f3d0 80%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.5rem 0;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1.02rem;
        font-weight: 400;
        margin: 0;
        max-width: 780px;
        line-height: 1.55;
    }

    /* Tarjetas Glassmorphic estilo UdeA */
    .glass-card {
        background: rgba(6, 35, 25, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .glass-card:hover {
        border-color: rgba(52, 211, 153, 0.45);
        transform: translateY(-2px);
    }

    /* Tarjetas de Métricas KPI */
    .kpi-card {
        background: linear-gradient(135deg, rgba(8, 48, 35, 0.75) 0%, rgba(4, 28, 20, 0.85) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.35);
        position: relative;
        overflow: hidden;
    }

    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #059669, #34d399);
    }

    .kpi-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #f0fdf4;
        line-height: 1.1;
    }

    .kpi-subtext {
        font-size: 0.8rem;
        color: #86efac;
        margin-top: 0.3rem;
    }

    /* Badges */
    .badge-success {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .badge-warning {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(245, 158, 11, 0.15);
        color: #fcd34d;
        border: 1px solid rgba(251, 191, 36, 0.35);
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .badge-info {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(5, 150, 105, 0.2);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Tarjeta Perfil de Estudiante */
    .student-profile-card {
        background: linear-gradient(135deg, rgba(8, 48, 35, 0.9) 0%, rgba(3, 24, 17, 0.95) 100%);
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.5), 0 0 35px -10px rgba(16, 185, 129, 0.2);
        margin-bottom: 2rem;
    }

    .student-avatar {
        width: 68px;
        height: 68px;
        border-radius: 18px;
        background: linear-gradient(135deg, #006837 0%, #059669 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        color: #ffffff;
        font-weight: 800;
        box-shadow: 0 8px 16px rgba(0, 104, 55, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }

    /* Inputs y Formularios */
    .stTextInput>div>div>input {
        background-color: rgba(6, 32, 23, 0.85) !important;
        border: 1px solid rgba(52, 211, 153, 0.25) !important;
        color: #f0fdf4 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3) !important;
    }

    /* Botones estilo Verde UdeA */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #006837 0%, #059669 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(0, 104, 55, 0.4) !important;
    }

    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(4, 25, 18, 0.7);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(16, 185, 129, 0.15);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 8px 18px;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(16, 185, 129, 0.2) !important;
        color: #34d399 !important;
        font-weight: 700;
    }

    /* Tablas Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    /* Separador sutil */
    .divider-custom {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(52, 211, 153, 0.25), transparent);
        margin: 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
