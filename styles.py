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
    /* BARRA LATERAL (SIDEBAR) - ESTILO CLARO Y LUMINOSO             */
    /* ============================================================= */
    [data-testid="stSidebar"] {
        background: #f2f7f4 !important;
        border-right: 1px solid #dce8e0 !important;
        color: #1f2937 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #1f2937 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #dce8e0 !important;
    }

    [data-testid="stSidebar"] .stCaption {
        color: #4b5563 !important;
    }

    /* ============================================================= */
    /* BANNER ESTILO SEMILLERO MEDICINA UDEA                         */
    /* ============================================================= */
    .semillero-banner {
        background-color: #ffffff;
        background-image: 
            linear-gradient(to right, rgba(46, 125, 50, 0.06) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(46, 125, 50, 0.06) 1px, transparent 1px);
        background-size: 22px 22px;
        border: 1.5px solid #dce8e0;
        border-radius: 20px;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 24px -4px rgba(46, 125, 50, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.02);
        position: relative;
        overflow: hidden;
    }

    .semillero-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1.5rem;
    }

    .semillero-left {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }

    /* Badge Experiencia vocacional */
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
        margin-bottom: 0.4rem;
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
        gap: 10px;
        flex-wrap: wrap;
    }

    .semillero-medicina {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #d97706;
        line-height: 1;
        letter-spacing: -0.02em;
        display: inline-block;
    }

    .semillero-sub-label {
        font-size: 1.55rem;
        font-weight: 800;
        color: #558b2f;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .semillero-tagline {
        color: #2e7d32;
        font-size: 1.18rem;
        font-weight: 700;
        margin-top: 0.4rem;
        letter-spacing: 0.01em;
    }

    /* Pill Nivel 1 en el banner */
    .pill-nivel {
        background-color: #004d40;
        border-radius: 9999px;
        padding: 0.65rem 1.4rem;
        display: inline-flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 14px rgba(0, 77, 64, 0.2);
    }

    .pill-nivel-text {
        font-family: 'Playfair Display', serif;
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .pill-nivel-badge {
        background-color: #e58e12;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 800;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(229, 142, 18, 0.4);
    }

    /* ============================================================= */
    /* BOTONES PÍLDORA VERDES (COMO EN LA IMAGEN)                    */
    /* ============================================================= */
    .pill-btn-group {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }

    .pill-dark-teal {
        background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%);
        color: #ffffff !important;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.45rem 1.15rem;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.25);
        border: none;
    }

    /* ============================================================= */
    /* TARJETAS Y COMPONENTES VISUALES                               */
    /* ============================================================= */
    .glass-card {
        background: #ffffff;
        border: 1px solid #dce8e0;
        border-radius: 16px;
        padding: 1.6rem;
        box-shadow: 0 4px 18px -2px rgba(46, 125, 50, 0.05);
        color: #1f2937;
    }

    .kpi-card {
        background: #ffffff;
        border: 1px solid #dce8e0;
        border-top: 4px solid #2e7d32;
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
        color: #2e7d32;
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
        border-left: 6px solid #e58e12;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px -4px rgba(46, 125, 50, 0.07);
        margin-bottom: 1.8rem;
    }

    .student-avatar {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        color: #ffffff;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
    }

    /* Formulario e inputs */
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        color: #1f2937 !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-size: 1rem !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #2e7d32 !important;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.15) !important;
    }

    /* Botones primarios en verde UdeA / Semillero */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.3rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 3px 10px rgba(46, 125, 50, 0.25) !important;
    }

    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%) !important;
        box-shadow: 0 5px 15px rgba(27, 94, 32, 0.3) !important;
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
    </style>
    """, unsafe_allow_html=True)
