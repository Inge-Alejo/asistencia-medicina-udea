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

# Aplicar estilos CSS personalizados (Verde Semillero #558b2f en barra lateral)
apply_custom_styles()

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) - VERDE SEMILLERO (#558b2f)
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0 1rem 0;">
        <div style="font-size: 0.74rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.95;">
            Universidad de Antioquia
        </div>
        <h3 style="color: #ffffff; margin: 0.2rem 0 0 0; font-family: 'Playfair Display', serif; font-weight: 800; font-size: 1.45rem;">
            Semillero Medicina
        </h3>
        <p style="color: #fef08a; font-size: 0.86rem; font-weight: 700; margin-top: 0.2rem;">
            Camino a la Formación en Salud
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Selector de Rol / Modo (Sin emojis y sin palabra '(Público)')
    st.markdown("### Modo de Acceso")
    mode = st.radio(
        "Seleccione vista",
        options=["Consulta Estudiantes", "Panel de Gestión"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Monitor de Tiempo Real
    st.markdown("### Monitor en Vivo")
    now_str = datetime.now().strftime("%H:%M:%S")
    st.caption(f"Sincronización: **{now_str}**")
    
    # Botón de refresco manual
    if st.button("Sincronizar Ahora", use_container_width=True):
        st.rerun()
        
    # Auto-refresco opcional
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

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.78rem; color: #ffffff; text-align: center; line-height: 1.4; padding-top: 0.5rem; opacity: 0.95;">
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
