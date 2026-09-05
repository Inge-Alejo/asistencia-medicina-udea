import streamlit as st
from datetime import datetime
from database import init_db, get_overall_kpis, save_logs_batch
from importer import parse_attendance_file, get_sample_attendance_text
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

# Inicializar Base de Datos (en nube o local se crea automáticamente)
init_db()

# Aplicar estilos CSS personalizados basados en el diseño del Semillero Medicina
apply_custom_styles()

# -------------------------------------------------------------
# BARRA LATERAL (SIDEBAR) - NAVEGACIÓN INSTITUCIONAL
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0 1rem 0;">
        <div style="font-size: 2.6rem; margin-bottom: 0.2rem;">🩺</div>
        <div style="font-size: 0.72rem; font-weight: 800; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.08em;">
            Universidad de Antioquia
        </div>
        <h3 style="color: #ffffff; margin: 0.2rem 0 0 0; font-family: 'Playfair Display', serif; font-weight: 800; font-size: 1.35rem;">
            Semillero Medicina
        </h3>
        <p style="color: #e58e12; font-size: 0.85rem; font-weight: 700; margin-top: 0.2rem;">
            Nivel 1 • Formación en Salud
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Selector de Rol / Modo
    st.markdown("### 🧭 Modo de Acceso")
    mode = st.radio(
        "Seleccione vista",
        options=["🎓 Consulta Estudiantes (Público)", "🔐 Panel de Gestión"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Monitor de Tiempo Real
    st.markdown("### ⚡ Monitor en Vivo")
    now_str = datetime.now().strftime("%H:%M:%S")
    st.caption(f"🕒 Sincronización: **{now_str}**")
    
    # Botón de refresco manual
    if st.button("🔄 Sincronizar Ahora", use_container_width=True):
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
    <div style="font-size: 0.76rem; color: #cbd5e1; text-align: center; line-height: 1.4; padding-top: 0.5rem;">
        <b>Facultad de Medicina • UdeA</b><br>
        Medellín, Colombia<br>
        Control Biométrico de Asistencia
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# ENRUTAMIENTO PRINCIPAL
# -------------------------------------------------------------
if "Consulta Estudiantes" in mode:
    render_student_view()
else:
    render_admin_view()
