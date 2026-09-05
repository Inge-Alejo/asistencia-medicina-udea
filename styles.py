import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Fondo general: Blanco marfil luminoso y limpio */
    .stApp {
        background: #f8faf9;
        color: #1f2937;
    }

    /* ============================================================= */
    /* BARRA LATERAL (SIDEBAR) - VERDE SEMILLERO ELEGANTE CON CARDS  */
    /* ============================================================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4d7c26 0%, #3f681e 50%, #345618 100%) !important;
        border-right: 1px solid #3b5f1c !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
        margin: 1.2rem 0 !important;
    }

    /* Tarjetas contenedoras de secciones en el Sidebar */
    .sidebar-section-card {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .sidebar-title-badge {
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #fef08a;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Selector de Radio en Sidebar */
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(0, 0, 0, 0.15);
        border-radius: 12px;
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 6px 10px !important;
        border-radius: 8px !important;
        transition: background 0.2s ease !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.15) !important;
    }

    /* FIX CRÍTICO: Botones en Sidebar (Texto 100% visible, fondo blanco y contraste perfecto) */
    [data-testid="stSidebar"] button {
        background: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] button *,
    [data-testid="stSidebar"] button p,
    [data-testid="stSidebar"] button span,
    [data-testid="stSidebar"] button div {
        color: #2b4c13 !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
    }

    [data-testid="stSidebar"] button:hover {
        background: #fef9c3 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25) !important;
    }

    [data-testid="stSidebar"] button:hover * {
        color: #1e3a0c !important;
    }

    /* Checkbox en sidebar */
    [data-testid="stSidebar"] [data-baseweb="checkbox"] span {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* Indicador de pulso en vivo */
    .pulse-dot {
        width: 9px;
        height: 9px;
        background-color: #4ade80;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 rgba(74, 222, 128, 0.7);
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(74, 222, 128, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
    }

    /* ============================================================= */
    /* BANNER PRINCIPAL: SEMILLERO MEDICINA UDEA                     */
    /* ============================================================= */
    .semillero-banner {
        background-color: #ffffff;
        background-image: 
            linear-gradient(to right, rgba(85, 139, 47, 0.06) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(85, 139, 47, 0.06) 1px, transparent 1px);
        background-size: 20px 20px;
        border: 1.5px solid #dce8e0;
        border-radius: 20px;
        padding: 2.2rem 2.8rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 22px -4px rgba(85, 139, 47, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.02);
        position: relative;
    }

    .badge-vocacional {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background-color: #004d40;
        color: #ffffff;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.35rem 0.95rem;
        border-radius: 9999px;
        width: fit-content;
        letter-spacing: 0.02em;
        margin-bottom: 0.6rem;
    }

    .dot-gold {
        width: 8px;
        height: 8px;
        background-color: #e58e12;
        border-radius: 50%;
        display: inline-block;
    }

    .semillero-title-group {
        display: flex;
        align-items: baseline;
        gap: 14px;
        flex-wrap: wrap;
        margin-bottom: 0.2rem;
    }

    .semillero-medicina {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.6rem;
        font-weight: 800;
        color: #d97706;
        line-height: 1;
        letter-spacing: -0.02em;
        display: inline-block;
    }

    .semillero-sub-label {
        font-size: 1.7rem;
        font-weight: 800;
        color: #558b2f;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .semillero-tagline {
        color: #2e7d32;
        font-size: 1.22rem;
        font-weight: 700;
        margin-top: 0.45rem;
        letter-spacing: 0.01em;
    }

    /* Píldoras verdes del banner */
    .pill-btn-group {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 1.6rem;
    }

    .pill-dark-teal {
        background: #558b2f;
        color: #ffffff !important;
        font-size: 0.86rem;
        font-weight: 700;
        padding: 0.45rem 1.2rem;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        box-shadow: 0 2px 6px rgba(85, 139, 47, 0.25);
        border: none;
    }

    /* ============================================================= */
    /* TARJETAS KPI Y COMPONENTES DEL CUERPO                         */
    /* ============================================================= */
    .glass-card {
        background: #ffffff;
        border: 1px solid #dce8e0;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 18px -2px rgba(85, 139, 47, 0.05);
        color: #1f2937;
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #dce8e0;
        border-top: 4px solid #558b2f;
        border-radius: 14px;
        padding: 1.25rem 1.3rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
    }

    .kpi-label {
        color: #4b5563;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #558b2f;
        line-height: 1.1;
    }

    .kpi-subtext {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 0.35rem;
    }

    /* Badges de estado */
    .badge-success {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ecfdf5;
        color: #15803d;
        border: 1px solid #86efac;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 700;
    }

    .badge-warning {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 700;
    }

    /* Tarjeta Perfil de Estudiante */
    .student-profile-card {
        background: #ffffff;
        border: 1px solid #dce8e0;
        border-left: 6px solid #d97706;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px -4px rgba(85, 139, 47, 0.07);
        margin-bottom: 1.8rem;
    }

    .student-avatar {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        background: linear-gradient(135deg, #558b2f 0%, #388e3c 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        color: #ffffff;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(85, 139, 47, 0.25);
    }

    /* Inputs de texto en el cuerpo principal */
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        color: #1f2937 !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-size: 1rem !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #558b2f !important;
        box-shadow: 0 0 0 3px rgba(85, 139, 47, 0.15) !important;
    }

    /* Botones primarios en el cuerpo */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.3rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button[kind="primary"] {
        background: #558b2f !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 3px 10px rgba(85, 139, 47, 0.25) !important;
    }

    .stButton>button[kind="primary"]:hover {
        background: #3f6820 !important;
        box-shadow: 0 5px 15px rgba(63, 104, 32, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #f0f5f2;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid #dce8e0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #4b5563;
        font-weight: 700;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #d97706 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    /* Tablas Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #dce8e0 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
    }

    .divider-custom {
        height: 1px;
        background: #dce8e0;
        margin: 1.5rem 0;
    }

    /* ============================================================= */
    /* SEMÁFORO Y PROGRESO DE CERTIFICACIÓN ACADÉMICA                */
    /* ============================================================= */
    .cert-progress-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.3rem 1.6rem;
        border: 1.5px solid #dce8e0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        margin: 1.2rem 0;
    }

    .cert-header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-bottom: 0.8rem;
    }

    .cert-title {
        font-weight: 800;
        color: #1b4332;
        font-size: 1.12rem;
        margin-bottom: 0.2rem;
    }

    .cert-subtitle {
        font-size: 0.84rem;
        color: #6b7280;
    }

    .cert-pct-badge {
        font-weight: 800;
        font-size: 1.4rem;
        padding: 0.25rem 0.8rem;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
    }

    .cert-bar-track {
        width: 100%;
        background-color: #e5e7eb;
        height: 12px;
        border-radius: 999px;
        overflow: hidden;
        margin: 0.6rem 0;
    }

    .cert-bar-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.6s ease;
    }

    .cert-footer-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        font-size: 0.86rem;
        margin-top: 0.5rem;
    }

    /* ============================================================= */
    /* MINI-CALENDARIO DE ASISTENCIAS MENSUAL                        */
    /* ============================================================= */
    .cal-card {
        background: #ffffff;
        border: 1.5px solid #dce8e0;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
    }

    .cal-month-title {
        font-weight: 800;
        color: #2e7d32;
        font-size: 1.15rem;
        margin-bottom: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    .cal-grid-header {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        margin-bottom: 8px;
        text-align: center;
    }

    .cal-header-cell {
        font-size: 0.78rem;
        font-weight: 800;
        color: #4b5563;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 4px 0;
    }

    .cal-grid-days {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
    }

    .cal-day-cell {
        min-height: 48px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        font-weight: 700;
        transition: all 0.2s ease;
        position: relative;
        background: #f9fafb;
        color: #374151;
        border: 1px solid #f3f4f6;
    }

    .cal-day-cell.empty {
        background: transparent;
        border-color: transparent;
    }

    .cal-day-cell.attended {
        background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%) !important;
        color: #ffffff !important;
        border: 1px solid #1b5e20 !important;
        box-shadow: 0 2px 6px rgba(46, 125, 50, 0.25);
    }

    .cal-day-cell.today {
        border: 2px solid #e58e12 !important;
    }

    .cal-check-badge {
        font-size: 0.65rem;
        line-height: 1;
        margin-top: 2px;
        opacity: 0.95;
    }

    .cal-legend {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #4b5563;
    }

    .cal-legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .cal-legend-dot {
        width: 14px;
        height: 14px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

