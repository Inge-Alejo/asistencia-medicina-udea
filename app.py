import streamlit as st
from datetime import datetime
from database import init_db, get_overall_kpis
from styles import apply_custom_styles
from views.student_view import render_student_view
from views.admin_view import render_admin_view

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="Semillero Medicina UdeA - Control de Asistencia",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Base de Datos de forma segura
init_db()

# Aplicar estilos CSS personalizados (Verde Semillero elegante con tarjetas)
apply_custom_styles()

# Obtener KPIs rápidos para mostrar en la barra lateral
kpis = get_overall_kpis()

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) - ELEGANTE Y ESTRUCTURADA
# -------------------------------------------------------------
with st.sidebar:
    # Cabecera institucional del Semillero
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0 1.2rem 0;">
        <div style="font-size: 0.74rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.95;">
            Universidad de Antioquia
        </div>
        <h2 style="color: #ffffff; margin: 0.25rem 0 0 0; font-family: 'Playfair Display', serif; font-weight: 800; font-size: 1.6rem; line-height: 1.15;">
            Semillero Medicina
        </h2>
        <div style="color: #fef08a; font-size: 0.86rem; font-weight: 700; margin-top: 0.35rem;">
            Camino a la Formación en Salud
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Tarjeta de Navegación
    st.markdown('<div class="sidebar-section-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title-badge">Modo de Acceso</div>', unsafe_allow_html=True)
    mode = st.radio(
        "Modo de Acceso",
        options=["Consulta Estudiantes", "Panel de Gestión"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Tarjeta de Monitor en Vivo
    st.markdown('<div class="sidebar-section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-title-badge">
        <span class="pulse-dot"></span> Monitor del Sistema
    </div>
    """, unsafe_allow_html=True)
    
    now_str = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<div style='font-size: 0.85rem; color: #ffffff; margin-bottom: 0.6rem;'>Sincronizado: <b>{now_str}</b></div>", unsafe_allow_html=True)
    
    # Botón de sincronización con texto 100% visible y contraste
    if st.button("Sincronizar Ahora", use_container_width=True):
        st.rerun()
        
    auto_refresh = st.checkbox("Monitoreo continuo (15s)", value=False)
    if auto_refresh:
        st.markdown(
            """
            <script>
            setTimeout(function(){
                window.parent.location.reload();
            }, 15000);
            </script>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Tarjeta de Resumen Rápido
    st.markdown('<div class="sidebar-section-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title-badge">Resumen del Semillero</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; font-size: 0.85rem;">
        <span style="color: #ffffff; opacity: 0.9;">Estudiantes:</span>
        <span style="font-weight: 800; color: #fef08a; font-size: 1rem;">{kpis['total_students']}</span>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem;">
        <span style="color: #ffffff; opacity: 0.9;">Marcaciones:</span>
        <span style="font-weight: 800; color: #fef08a; font-size: 1rem;">{kpis['total_logs']}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Pie de página institucional
    st.markdown("""
    <div style="font-size: 0.76rem; color: #ffffff; text-align: center; line-height: 1.4; padding-top: 0.3rem; opacity: 0.9;">
        <b>Facultad de Medicina • UdeA</b><br>
        Medellín, Colombia<br>
        Control Biométrico de Asistencia
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# ENRUTAMIENTO PRINCIPAL
# -------------------------------------------------------------
if mode == "Consulta Estudiantes":
    render_student_view()
else:
    render_admin_view()
